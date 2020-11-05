import os
import subprocess
import sys
import zipfile
from io import BytesIO
from pathlib import Path
from threading import Thread
from tkinter import filedialog
from urllib import request

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QAbstractButton, QComboBox, QSpinBox, QListView, QCheckBox, \
    QRadioButton, QFileDialog, QMessageBox, QErrorMessage

from logic.constants import ALL_TYPES
from options import OPTIONS, Options
from progressdialog import ProgressDialog
from randomizerthread import RandomizerThread
from ssrando import Randomizer
from ui_randogui import Ui_MainWindow
from witmanager import WitManager


class RandoGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.wit_manager = WitManager(Path('.').resolve())
        self.randothread = None
        self.error_msg = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.clean_iso_path = ""
        self.output_folder = ""

        self.options = Options()

        for option_key, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                ui_name = option.get('ui', None)
                if not ui_name:
                    continue
                widget = getattr(self.ui, ui_name)
                if isinstance(widget, QAbstractButton):
                    widget.setChecked(self.options[option_key])
                    widget.clicked.connect(self.update_settings)
                elif isinstance(widget, QComboBox):
                    widget.clicked.connect(self.update_settings)
                elif isinstance(widget, QListView):
                    pass
                elif isinstance(widget, QSpinBox):
                    if 'min' in option:
                        widget.setMinimum(option['min'])
                    if 'max' in option:
                        widget.setMaximum(option['max'])
                    widget.setValue(self.options[option_key])
                    widget.valueChanged.connect(self.update_settings)

        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            widget.setChecked(not check_type in self.options['banned-types'])
            if check_type == 'crystal':
                widget.setEnabled(False)
            widget.clicked.connect(self.update_settings)

        self.ui.clean_iso_browse_button.clicked.connect(self.browse_for_iso)
        self.ui.ouput_folder_browse_button.clicked.connect(self.browse_for_output_dir)
        self.ui.randomize_button.clicked.connect(self.randomize)
        self.update_ui_for_settings()

    def randomize(self):
        if not self.randothread is None:
            print('ERROR: tried to randomize multiple times at once!')
            return
        if not self.wit_manager.actual_extract_already_exists() and not self.clean_iso_path:
            self.error_msg = QErrorMessage(self)
            self.error_msg.showMessage('please enter a valid clean iso path!')
            return
        dry_run = self.options['dry-run']
        # make sure user can't mess with the options now
        rando = Randomizer(self.options.copy())

        if dry_run:
            extra_steps = 1
        else:
            extra_steps = 5  # wit setup, extract, copy, wit copy

        self.progress_dialog = ProgressDialog("Randomizing", "Initializing...", rando.get_total_progress_steps() + extra_steps)
        self.randomizer_thread = RandomizerThread(rando, self.wit_manager, self.clean_iso_path, self.output_folder)
        self.randomizer_thread.update_progress.connect(self.ui_progress_callback)
        self.randomizer_thread.randomization_complete.connect(self.randomization_complete)
        self.randomizer_thread.error_abort.connect(self.on_error)
        self.randomizer_thread.start()

    def ui_progress_callback(self, current_action, completed_steps):
        self.progress_dialog.setValue(completed_steps)
        self.progress_dialog.setLabelText(current_action)

    def on_error(self, message):
        self.error_msg = QErrorMessage(self)
        self.error_msg.showMessage(message)

    def randomization_complete(self):
        self.progress_dialog.reset()

        text = """Randomization complete.<br><br>
                 If you get stuck, check the progression spoiler log in the output folder."""

        self.complete_dialog = QMessageBox()
        self.complete_dialog.setTextFormat(Qt.TextFormat.RichText)
        self.complete_dialog.setWindowTitle("Randomization complete")
        self.complete_dialog.setText(text)
        self.complete_dialog.setWindowIcon(self.windowIcon())
        self.complete_dialog.show()
        self.randomizer_thread = None

    def browse_for_iso(self):
        if self.clean_iso_path and os.path.isfile(self.clean_iso_path):
            default_dir = os.path.dirname(self.clean_iso_path)
        else:
            default_dir = None

        clean_iso_path, selected_filter = QFileDialog.getOpenFileName(self, "Select Clean Skyward Sword NTSC-U 1.0 ISO",
                                                                      default_dir, "Wii ISO Files (*.iso)")
        if not clean_iso_path:
            return
        self.ui.clean_iso_path.setText(clean_iso_path)
        self.update_settings()

    def browse_for_output_dir(self):
        if self.output_folder and os.path.isfile(self.output_folder):
            default_dir = os.path.dirname(self.output_folder)
        else:
            default_dir = None

        output_folder = QFileDialog.getExistingDirectory(self, "Select output folder", default_dir)
        if not output_folder:
            return
        self.ui.output_folder.setText(output_folder)
        self.update_settings()

    def update_ui_for_settings(self):
        self.ui.clean_iso_path.setText(self.clean_iso_path)
        self.ui.output_folder.setText(self.output_folder)
        self.ui.seed.setText(str(self.options["seed"]))
        for option_key, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                ui_name = option.get('ui', None)
                if not ui_name:
                    continue
                widget = getattr(self.ui, ui_name)
                if isinstance(widget, QAbstractButton):
                    widget.setChecked(self.options[option_key])
                elif isinstance(widget, QComboBox):
                    pass
                elif isinstance(widget, QListView):
                    pass
                elif isinstance(widget, QSpinBox):
                    widget.setValue(self.options[option_key])

        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            widget.setChecked(not check_type in self.options['banned-types'])

    def update_settings(self):
        self.clean_iso_path = self.ui.clean_iso_path.text()
        self.output_folder = self.ui.output_folder.text()
        try:
            self.options.set_option("seed", int(self.ui.seed.text()))
        except ValueError:
            if self.ui.seed.text() == "":
                self.options.set_option("seed", -1)
            else:
                # TODO: give an error dialog or some sort of error message that the seed is invalid
                pass

        for option_command, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                ui_name = option.get('ui', None)
                if not ui_name:
                    continue
                self.options.set_option(option_command, self.get_option_value(ui_name))

        self.options.set_option("banned-types", self.get_banned_types())
        print(self.options.get_permalink())

    def get_option_value(self, option_name):
        widget = getattr(self.ui, option_name)
        if isinstance(widget, QCheckBox) or isinstance(widget, QRadioButton):
            return widget.isChecked()
        elif isinstance(widget, QComboBox):
            return widget.itemText(widget.currentIndex())
        elif isinstance(widget, QSpinBox):
            return widget.value()
        elif isinstance(widget, QListView):
            pass
        else:
            print("Option widget is invalid: %s" % option_name)

    def get_banned_types(self):
        banned_types = []
        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            if not widget.isChecked():
                banned_types.append(check_type)
        return banned_types


def run_main_gui():
    app = QtWidgets.QApplication([])

    widget = RandoGUI()
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main_gui()
