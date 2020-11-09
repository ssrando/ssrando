import sys
import re
import os
import zipfile
import tarfile
from io import BytesIO
from urllib import request
from pathlib import Path
import subprocess
import shutil

WIT_PROGRESS_REGEX = re.compile(rb' +([0-9]+)%.*')

NOP = lambda *args, **kwargs: None

# currently, only win and linux (both 64bit) are supported
IS_WINDOWS = sys.platform == 'win32'

class WitException(Exception):
    pass

class WitManager:
    def __init__(self, rootpath: Path):
        self.rootpath = rootpath
        self.witcommand = None
        self.update_wit_command()
    
    def update_wit_command(self):
        if not self.witcommand is None:
            return
        # check globally installed wit
        try:
            completed = subprocess.run(['wit','--version'])
            if completed.returncode == 0:
                self.witcommand = 'wit'
                return
        except FileNotFoundError:
            pass
        if self.get_local_wit_path().is_file():
            self.witcommand = str(self.get_local_wit_path().resolve())
            return
        self.witcommand = None

    def get_local_wit_path(self) -> Path:
        if IS_WINDOWS:
            return self.rootpath / 'wit-v3.03a-r8245-cygwin' / 'bin' / 'wit.exe'
        else:
            return self.rootpath / 'wit-v3.03a-r8245-x86_64' / 'bin' / 'wit'

    def ensure_wit_installed(self):
        self.update_wit_command()
        if self.witcommand is None:
            print('wit not installed, installing')
            if IS_WINDOWS:
                with zipfile.ZipFile(BytesIO(request.urlopen('https://wit.wiimm.de/download/wit-v3.03a-r8245-cygwin.zip').read())) as wit_zip:
                    wit_zip.extractall(self.rootpath)
            else:
                with tarfile.open(mode='r:gz', fileobj=BytesIO(request.urlopen('https://wit.wiimm.de/download/wit-v3.03a-r8245-x86_64.tar.gz').read())) as wit_zip:
                    wit_zip.extractall(self.rootpath)
            self.update_wit_command()
    
    def actual_extract_already_exists(self):
        return (self.rootpath / 'actual-extract' / 'DATA' / 'sys' / 'main.dol').is_file()

    def extract_game(self, iso_path, progress_cb=NOP):
        iso_path = str(iso_path)
        # check if game is already extracted
        # TODO: there seemed to be issues with wit sometimes, that it doesn't properly extract the first time?
        datapath = self.rootpath / 'actual-extract' / 'DATA'
        if True or not self.actual_extract_already_exists():
            extract_process = subprocess.Popen([self.witcommand, "-P", "extract",
                iso_path, str(self.rootpath / "actual-extract")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                current_progress_str = bytearray()
                char = b''
                while char != b'\r' and extract_process.poll() is None: # \r is written by wit to reset the line, so a new one begins
                    char = extract_process.stdout.read(1)
                    current_progress_str.extend(char)
                progress_match = WIT_PROGRESS_REGEX.match(current_progress_str)
                if progress_match:
                    # get the percentage out of the log
                    percent = int(progress_match[1].decode('ascii'))
                    progress_cb('Extracting files...', percent)
                return_code = extract_process.poll()
                if not return_code is None:
                    if return_code != 0:
                        raise WitException(f'ERROR: {extract_process.stderr.read().decode("UTF-8")}')
                    break
            # delete all videos, they take up way too much space
            for hint_vid in (datapath / 'files' / 'THP').glob('*.thp'):
                os.remove(str(hint_vid))
    
    def modified_extract_already_exists(self):
        return (self.rootpath / 'modified-extract' / 'DATA' / 'sys' / 'main.dol').is_file()


    def copy_to_modified(self, progress_cb=NOP):
        # check if it already exists
        if not self.modified_extract_already_exists():
            progress_cb('copy to modified...',0)
            src = str(self.rootpath / 'actual-extract')
            dest = str(self.rootpath / 'modified-extract')
            file_count = 0
            for path, dirs, filenames in os.walk(src):
                file_count += len(filenames)
        
            def makedirs(dest):
                if not os.path.exists(dest):
                    os.makedirs(dest)
        
            makedirs(dest)
            num_copied = 0
            # manual copy of each file to show progress
            for path, dirs, filenames in os.walk(src):
                for directory in dirs:
                    destDir = path.replace(src,dest)
                    makedirs(os.path.join(destDir, directory))
                for sfile in filenames:
                    srcFile = os.path.join(path, sfile)
                    destFile = os.path.join(path.replace(src, dest), sfile)
                    shutil.copy(srcFile, destFile)
                    num_copied += 1
                    progress_cb('copy to modified...', (num_copied/file_count)*100)
    
    def reapack_game(self, modified_iso_dir: Path, seed, use_wbfs=False, progress_cb=NOP):
        filename = f'SOUE01.wbfs' if use_wbfs else f'SS Randomizer {seed}.iso'
        modified_iso_path = modified_iso_dir / filename
        if modified_iso_path.is_file():
            os.remove(str(modified_iso_path))
        extract_process = subprocess.Popen([self.witcommand, "-P", "copy", "--split",
                str(self.rootpath / "modified-extract"), str(modified_iso_path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            current_progress_str = bytearray()
            char = b''
            while char != b'\r' and extract_process.poll() is None: # \r is written by wit to reset the line, so a new one begins
                char = extract_process.stdout.read(1)
                current_progress_str.extend(char)
            progress_match = WIT_PROGRESS_REGEX.match(current_progress_str)
            if progress_match:
                # get the percentage out of the log
                percent = int(progress_match[1].decode('ascii'))
                progress_cb('Writing patched game...', percent)
            return_code = extract_process.poll()
            if not return_code is None:
                if return_code != 0:
                    raise WitException(f'ERROR: {extract_process.stderr.read().decode("UTF-8")}')
                break
        assert return_code == 0
    

