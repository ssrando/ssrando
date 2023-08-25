import sys
import re
import os
from pathlib import Path
import shutil

import disc_riider_py

WIT_PROGRESS_REGEX = re.compile(rb" +([0-9]+)%.*")
CLEAN_NTSC_U_1_00_DOL_HASH = "450a6806f46d59dcf8278db08e06f94865a4b18a"

WRONG_VERSION_DOL_HASHES = {
    "2848bb574bfcbf97f075adc4e0f4692ddd7fd0e8": "JP 1.00",
    # "TODO": "US 1.01",
    "30cad7e8a88442b1388867f01bc6461097f4a152": "US 1.02",
    "8f6bf468447d9f10172cc4a472a56e1f526a5cb4": "PAL 1.00",
    # "TODO": "PAL 1.01",
    # "TODO": "PAL 1.02",
}

NOP = lambda *args, **kwargs: None

# currently, only win and linux (both 64bit) are supported
IS_WINDOWS = sys.platform == "win32"


class WrongChecksumException(Exception):
    pass


class ExtractManager:
    def __init__(self, rootpath: Path):
        self.rootpath = rootpath

    def actual_extract_already_exists(self):
        return (
            self.rootpath / "actual-extract" / "DATA" / "sys" / "main.dol"
        ).is_file()

    def extract_game(self, iso_path, progress_cb=NOP):
        if not self.actual_extract_already_exists():
            dest_path = self.rootpath / "actual-extract"
            extractor = disc_riider_py.WiiIsoExtractor(iso_path)
            extractor.prepare_extract_section("DATA")
            # remove hint videos, but keep credits
            extractor.remove_files_by_callback(
                "DATA", lambda x: x.startswith("THP") and not "Demo" in x
            )
            checksum = bytes(extractor.get_dol_hash("DATA")).hex()
            if CLEAN_NTSC_U_1_00_DOL_HASH != checksum:
                if wrong_version := WRONG_VERSION_DOL_HASHES.get(checksum):
                    raise WrongChecksumException(
                        f"This ISO is {wrong_version}, but the rando only support NTSC-U 1.00 (North American).",
                    )
                else:
                    raise WrongChecksumException(
                        f"Unrecognized DOL hash, probably bad dump or invalid version: {checksum}",
                    )
            extractor.extract_to(
                dest_path, lambda x: progress_cb("Extracting files...", x)
            )

    def modified_extract_already_exists(self):
        return (
            self.rootpath / "modified-extract" / "DATA" / "sys" / "main.dol"
        ).is_file()

    def copy_to_modified(self, progress_cb=NOP):
        # check if it already exists
        if not self.modified_extract_already_exists():
            progress_cb("copy to modified...", 0)
            src = str(self.rootpath / "actual-extract")
            dest = str(self.rootpath / "modified-extract")
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
                    destDir = path.replace(src, dest)
                    makedirs(os.path.join(destDir, directory))
                for sfile in filenames:
                    srcFile = os.path.join(path, sfile)
                    destFile = os.path.join(path.replace(src, dest), sfile)
                    shutil.copy(srcFile, destFile)
                    num_copied += 1
                    progress_cb("copy to modified...", (num_copied / file_count) * 100)

    def repack_game(self, modified_iso_dir: Path, progress_cb=NOP):
        modified_iso_path = modified_iso_dir / "SOUE01.iso"
        if modified_iso_path.is_file():
            modified_iso_path.unlink()
        legacy_wbfs_path = modified_iso_dir / "SOUE01.wbfs"
        if legacy_wbfs_path.is_file():
            legacy_wbfs_path.unlink()
        disc_riider_py.rebuild_from_directory(
            self.rootpath / "modified-extract",
            modified_iso_path,
            lambda x: progress_cb("Writing patched game...", x),
        )
