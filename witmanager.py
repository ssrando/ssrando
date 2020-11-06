import sys
import os
import zipfile
import tarfile
from io import BytesIO
from urllib import request
from pathlib import Path
import subprocess
import shutil

# currently, only win and linux (both 64bit) are supported
IS_WINDOWS = sys.platform == 'win32'

class WitManager:
    def __init__(self, rootpath: Path):
        self.rootpath = rootpath
        self.witcommand = None
    
    def update_wit_command(self):
        # check globally installed wit
        try:
            completed = subprocess.run(['wit','--version'])
            if completed.returncode == 0:
                self.witcommand = 'wit'
                return self.witcommand
        except FileNotFoundError:
            pass
        if self.get_local_wit_path().is_file():
            self.witcommand = str(self.get_local_wit_path().resolve())
            return self.witcommand
        return None

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

    def extract_game(self, iso_path):
        iso_path = str(iso_path)
        # check if game is already extracted
        # TODO: there seemed to be issues with wit sometimes, that it doesn't properly extract the first time?
        datapath = self.rootpath / 'actual-extract' / 'DATA'
        if not self.actual_extract_already_exists():
            return_code = subprocess.call([self.witcommand, "-P", "extract",
                iso_path, str(self.rootpath / "actual-extract")])
            assert return_code == 0
            # delete all videos, they take up way too much space
            for hint_vid in (datapath / 'files' / 'THP').glob('*.thp'):
                os.remove(str(hint_vid))
    
    def modified_extract_already_exists(self):
        return (self.rootpath / 'modified-extract' / 'DATA' / 'sys' / 'main.dol').is_file()

    def copy_to_modified(self):
        # check if it already exists
        if not self.modified_extract_already_exists():
            shutil.copytree(str(self.rootpath / 'actual-extract'), str(self.rootpath / 'modified-extract'))
    
    def reapack_game(self, modified_iso_dir: Path, seed, use_wbfs=False):
        filename = f'SOUE01-{seed}.wbfs' if use_wbfs else f'SS Randomizer {seed}.iso'
        modified_iso_path = modified_iso_dir / filename
        if modified_iso_path.is_file():
            os.remove(str(modified_iso_path))
        return_code = subprocess.call([self.witcommand, "-P", "copy", "--split",
                str(self.rootpath / "modified-extract"), str(modified_iso_path)])
        assert return_code == 0
    

