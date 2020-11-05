import subprocess
import traceback
import time
import zipfile
from io import BytesIO
from pathlib import Path
from urllib import request

from PySide2.QtCore import QThread, Signal

from ssrando import Randomizer


class RandomizerThread(QThread):
    update_progress = Signal(str, int)
    randomization_complete = Signal()
    randomization_failed = Signal()

    def __init__(self, options, clean_iso_path, output_folder):
        QThread.__init__(self)

        self.options = options
        self.clean_iso_path = clean_iso_path
        self.output_folder = output_folder

        self.wit_url = "https://wit.wiimm.de/download/wit-v3.03a-r8245-cygwin.zip"
        self.wit_folder = "wit-v3.03a-r8245-cygwin"

    def run(self):

        if not self.options["dry-run"]:
            if not (Path(".") / self.wit_folder).is_dir():
                # fetch and unzip wit dependency
                print("wit not found, installing")
                with zipfile.ZipFile(BytesIO(request.urlopen(self.wit_url).read())) as wit_zip:
                    wit_zip.extractall(Path(".") / self.wit_folder)

            if not (Path(".") / "actual-extract").is_dir():
                subprocess.run(
                    [(Path(".") / self.wit_folder / self.wit_folder / "bin" / "wit"), "-P", "extract",
                     (Path(self.clean_iso_path)), "actual-extract"])
            if not (Path(".") / "modified-extract").is_dir():
                subprocess.run(["xcopy", "/E", "/I", "actual-extract", "modified-extract"])

        if self.options["seed"] == "":
            self.options["seed"] = -1
        self.options.set_option("seed", int(self.options["seed"]))
        rando = Randomizer(self.options)
        print(rando.seed)
        rando.randomize()
        if not self.options["dry-run"]:
            iso_name = "SS Randomizer " + str(rando.seed) + ".iso"
            subprocess.run([(Path(".") / self.wit_folder / "bin" / "wit").name, "-P", "copy", "modified-extract",
                            (Path(self.output_folder) / iso_name)])

        self.randomization_complete.emit()
        # try:
        #     randomizer_generator = self.randomizer.randomize()
        #     last_update_time = time.time()
        #     while True:
        #         next_option_description, options_finished = next(randomizer_generator)
        #         if options_finished == -1:
        #             break
        #         if time.time() - last_update_time < 0.1:
        #             # Limit how frequently the signal is emitted to 10 times per second.
        #             continue
        #         self.update_progress.emit(next_option_description, options_finished)
        #         last_update_time = time.time()
        # except Exception as e:
        #     stack_trace = traceback.format_exc()
        #     error_message = "Randomization failed with error:\n" + str(e) + "\n\n" + stack_trace
        #     self.randomization_failed.emit(error_message)
        #     return