from pathlib import Path

from PySide6.QtCore import QThread, Signal

from ssrando import Randomizer, StartupException
from extractmanager import ExtractManager


class RandomizerThread(QThread):
    update_progress = Signal(str, int)
    update_progress_dialog = Signal(str, int)
    error_abort = Signal(str)
    randomization_complete = Signal()

    def __init__(
        self, randomizer: Randomizer, extract_manager: ExtractManager, output_folder
    ):
        QThread.__init__(self)

        self.randomizer = randomizer
        self.extract_manager = extract_manager
        self.output_folder = output_folder
        self.steps = 0

    def create_ui_progress_callback(self, start_steps):
        def progress_cb(action, current_steps=None):
            if not current_steps is None:
                self.steps = start_steps + current_steps
            self.update_progress.emit(action, self.steps)
            if current_steps is None:
                self.steps += 1

        return progress_cb

    def run(self):
        dry_run = self.randomizer.options["dry-run"]
        default_ui_progress_callback = self.create_ui_progress_callback(0)
        if not dry_run:
            try:
                self.randomizer.check_valid_directory_setup()
            except StartupException as e:
                self.error_abort.emit(str(e))
                return
        self.randomizer.set_progress_callback(self.create_ui_progress_callback(0))
        try:
            self.randomizer.randomize(self.update_progress_dialog.emit)
        except Exception as e:
            self.error_abort.emit(str(e))
            import traceback

            print(traceback.format_exc())
            return
        if not dry_run:
            default_ui_progress_callback("repacking game...")
            repack_progress_cb = self.create_ui_progress_callback(self.steps)
            self.extract_manager.repack_game(
                Path(self.output_folder),
                progress_cb=repack_progress_cb,
            )

        default_ui_progress_callback("done")
        self.randomization_complete.emit()


class ExtractSetupThread(QThread):
    update_total_steps = Signal(int)
    update_progress = Signal(str, int)
    error_abort = Signal(str)
    extract_complete = Signal()

    def __init__(
        self, extract_manager: ExtractManager, clean_iso_path: Path, output_folder: Path
    ):
        QThread.__init__(self)

        self.extract_manager = extract_manager
        self.clean_iso_path = clean_iso_path
        self.output_folder = output_folder
        self.steps = 0

    def create_ui_progress_callback(self, start_steps):
        def progress_cb(action, current_steps=None):
            if not current_steps is None:
                self.steps = start_steps + current_steps
            self.update_progress.emit(action, self.steps)
            if current_steps is None:
                self.steps += 1

        return progress_cb

    def run(self):
        total_steps = 2 + 100 + 100  # verify, extract, copy
        self.update_total_steps.emit(total_steps)
        default_ui_progress_callback = self.create_ui_progress_callback(0)

        default_ui_progress_callback("extracting game...")
        if not self.extract_manager.actual_extract_already_exists():
            try:
                self.extract_manager.extract_game(
                    self.clean_iso_path, self.create_ui_progress_callback(1)
                )
            except Exception as e:
                print(e)
                self.error_abort.emit(str(e))
                return
        else:
            default_ui_progress_callback("already extracted", 101)

        default_ui_progress_callback("copying extract...")
        if not self.extract_manager.modified_extract_already_exists():
            self.extract_manager.copy_to_modified(self.create_ui_progress_callback(101))
        else:
            default_ui_progress_callback("already copied", 201)
        self.extract_complete.emit()
