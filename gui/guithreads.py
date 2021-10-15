from pathlib import Path
import os
from typing import Optional

from PySide2.QtCore import QThread, Signal

from ssrando import Randomizer, StartupException
from witmanager import WitManager, WitException, WrongChecksumException


class RandomizerThread(QThread):
    update_progress = Signal(str, int)
    error_abort = Signal(str)
    randomization_complete = Signal()

    def __init__(self, randomizer: Randomizer, wit_manager: WitManager, output_folder):
        QThread.__init__(self)

        self.randomizer = randomizer
        self.wit_manager = wit_manager
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
            self.randomizer.randomize()
        except Exception as e:
            self.error_abort.emit(str(e))
            import traceback

            print(traceback.format_exc())
            return
        if not dry_run:
            self.wit_manager.ensure_wit_installed()
            default_ui_progress_callback("repacking game...")
            repack_progress_cb = self.create_ui_progress_callback(
                self.randomizer.get_total_progress_steps()
            )
            self.wit_manager.reapack_game(
                Path(self.output_folder),
                self.randomizer.seed,
                use_wbfs=True,
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
        self, wit_manager: WitManager, clean_iso_path: Path, output_folder: Path
    ):
        QThread.__init__(self)

        self.wit_manager = wit_manager
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
        total_steps = 2 + 100 + 100 + 100  # wit + done, verify, extract, copy
        self.update_total_steps.emit(total_steps)
        default_ui_progress_callback = self.create_ui_progress_callback(0)
        default_ui_progress_callback("setting up wiimms ISO tools...")
        self.wit_manager.ensure_wit_installed()

        default_ui_progress_callback("extracting game...")
        if not self.wit_manager.actual_extract_already_exists():
            try:
                self.wit_manager.iso_integrity_check(
                    self.clean_iso_path, self.create_ui_progress_callback(1)
                )
                self.wit_manager.extract_game(
                    self.clean_iso_path, self.create_ui_progress_callback(101)
                )
            except (WitException, WrongChecksumException) as e:
                print(e)
                self.error_abort.emit(str(e))
                return
        else:
            default_ui_progress_callback("already extracted", 201)

        default_ui_progress_callback("copying extract...")
        if not self.wit_manager.modified_extract_already_exists():
            self.wit_manager.copy_to_modified(self.create_ui_progress_callback(201))
        else:
            default_ui_progress_callback("already copied", 301)
        self.extract_complete.emit()
