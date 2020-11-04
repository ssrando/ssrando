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
    
    def get_wit_path(self) -> Path:
        if IS_WINDOWS:
            return self.rootpath / 'wit-v3.03a-r8245-cygwin' / 'bin' / 'wit'
        else:
            return self.rootpath / 'wit-v3.03a-r8245-x86_64' / 'bin' / 'wit'

    def ensure_wit_installed(self):
        if not self.get_wit_path().is_file():
            print('wit not installed, installing')
            if IS_WINDOWS:
                with zipfile.ZipFile(BytesIO(request.urlopen('https://wit.wiimm.de/download/wit-v3.03a-r8245-cygwin.zip').read())) as wit_zip:
                    wit_zip.extractall(self.rootpath)
            else:
                with tarfile.open(mode='r:gz', fileobj=BytesIO(request.urlopen('https://wit.wiimm.de/download/wit-v3.03a-r8245-x86_64.tar.gz').read())) as wit_zip:
                    wit_zip.extractall(self.rootpath)
    
    def extract_game(self, iso_path):
        # check if game is already extracted
        # TODO: there seemed to be issues with wit sometimes, that it doesn't properly extract the first time?
        datapath = self.rootpath / 'actual-extract' / 'DATA'
        if not (datapath / 'sys' / 'main.dol').is_file():
            subprocess.call([self.get_wit_path(), "-P", "extract",
                 iso_path, self.rootpath / "actual-extract"])
            # delete hint videos, they take up way too much space
            for hint_vid in (datapath / 'files' / 'THP').glob('HINT_*.thp'):
                os.remove(hint_vid)

    def copy_to_modified(self):
        # check if it already exists
        if not (self.rootpath / 'modified-extract' / 'DATA' / 'sys' / 'main.dol').is_file():
            shutil.copy(self.rootpath / 'actual-extract', self.rootpath / 'modified-extract')


