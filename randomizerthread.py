from pathlib import Path

from PySide2.QtCore import QThread, Signal

from ssrando import Randomizer, StartupException
from witmanager import WitManager


class RandomizerThread(QThread):
    update_progress = Signal(str, int)
    error_abort = Signal(str)
    randomization_complete = Signal()

    def __init__(self, randomizer: Randomizer, wit_manager: WitManager, clean_iso_path, output_folder):
        QThread.__init__(self)

        self.randomizer = randomizer
        self.wit_manager = wit_manager
        self.clean_iso_path = clean_iso_path
        self.output_folder = output_folder
        self.steps = 0

    def ui_progress_callback(self, action):
        self.update_progress.emit(action, self.steps)
        self.steps += 1

    def run(self):
        dry_run = self.randomizer.options['dry-run']
        if not dry_run:
            self.ui_progress_callback('setting up wiimms ISO tools...')
            self.wit_manager.ensure_wit_installed()

            self.ui_progress_callback('extracting game...')
            if not self.wit_manager.actual_extract_already_exists():
                self.wit_manager.extract_game(self.clean_iso_path)

            self.ui_progress_callback('copying extract...')
            if not self.wit_manager.modified_extract_already_exists():
                self.wit_manager.copy_to_modified()

        print(self.randomizer.seed)
        if not dry_run:
            try:
                self.randomizer.check_valid_directory_setup()
            except StartupException as e:
                self.error_abort.emit(str(e))
                return
        self.randomizer.set_progress_callback(self.ui_progress_callback)
        try:
            self.randomizer.randomize()
        except Exception as e:
            self.error_abort.emit(str(e))
            return
        if not dry_run:
            self.ui_progress_callback('repacking game...')
            self.wit_manager.reapack_game(Path(self.output_folder), self.randomizer.seed, use_wbfs=True)

        self.ui_progress_callback('done')
        self.randomization_complete.emit()
