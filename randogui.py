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
from PySide2.QtCore import Qt, QTimer, QEvent
from PySide2.QtWidgets import QMainWindow, QAbstractButton, QComboBox, QSpinBox, QListView, QCheckBox, \
    QRadioButton, QFileDialog, QMessageBox, QErrorMessage

from logic.constants import ALL_TYPES
from options import OPTIONS, Options
from progressdialog import ProgressDialog
from guithreads import RandomizerThread, ExtractSetupThread
from ssrando import Randomizer
from ui_randogui import Ui_MainWindow
from witmanager import WitManager

# Allow keyboard interrupts on the command line to instantly close the program.
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class RandoGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.wit_manager = WitManager(Path('.').resolve())
        self.randothread = None
        self.error_msg = None
        self.progress_dialog = None
        self.randomize_after_iso_extract = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.output_folder = ""

        self.options = Options()

        self.option_map = {}
        for option_key, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                ui_name = option.get('ui', None)
                self.option_map[ui_name] = option
                if not ui_name:
                    continue
                widget = getattr(self.ui, ui_name)
                widget.installEventFilter(self)
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

        self.ui.ouput_folder_browse_button.clicked.connect(self.browse_for_output_dir)
        self.ui.randomize_button.clicked.connect(self.randomize)
        self.update_ui_for_settings()
        self.set_option_description(None)

        if not self.wit_manager.actual_extract_already_exists():
            self.ask_for_clean_iso()

    def ask_for_clean_iso(self):
        selected = QMessageBox.question(self,'Extract now?', 'For randomizing purposes, a clean NTSC-U 1.00 ISO is needed, browse for it now? This is only needed once',
            defaultButton=QMessageBox.Yes)
        if selected == QMessageBox.Yes:
            self.browse_for_iso()
        else:
            self.randomize_after_iso_extract = False

    def randomize(self):
        if not self.randothread is None:
            print('ERROR: tried to randomize multiple times at once!')
            return
        dry_run = self.options['dry-run']
        if not (dry_run or self.wit_manager.actual_extract_already_exists()):
            self.randomize_after_iso_extract = True
            self.ask_for_clean_iso()
            return
        # make sure user can't mess with the options now
        rando = Randomizer(self.options.copy())

        if dry_run:
            extra_steps = 1 # done
        else:
            extra_steps = 101 # wit create wbfs + done

        self.progress_dialog = ProgressDialog("Randomizing", "Initializing...", rando.get_total_progress_steps() + extra_steps)
        self.randomizer_thread = RandomizerThread(rando, self.wit_manager, self.output_folder)
        self.randomizer_thread.update_progress.connect(self.ui_progress_callback)
        self.randomizer_thread.randomization_complete.connect(self.randomization_complete)
        self.randomizer_thread.error_abort.connect(self.on_error)
        self.randomizer_thread.start()

    def ui_progress_callback(self, current_action, completed_steps, total_steps=None):
        self.progress_dialog.setValue(completed_steps)
        self.progress_dialog.setLabelText(current_action)
        if not total_steps is None:
            self.progress_dialog.setMaximum(total_steps)

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
        clean_iso_path, selected_filter = QFileDialog.getOpenFileName(self, "Select Clean Skyward Sword NTSC-U 1.0 ISO",
                                                                      None, "Wii ISO Files (*.iso)")
        if not clean_iso_path:
            return
        self.progress_dialog = ProgressDialog("Extracting Game Files", "Initializing...", 100)
        self.progress_dialog.setAutoClose(True)
        self.extract_thread = ExtractSetupThread(self.wit_manager, clean_iso_path, None)
        self.extract_thread.update_total_steps.connect(lambda total_steps: self.progress_dialog.setMaximum(total_steps))
        self.extract_thread.update_progress.connect(self.ui_progress_callback)
        def on_complete():
            self.progress_dialog.reset()
            if self.randomize_after_iso_extract:
                self.randomize()
        self.extract_thread.extract_complete.connect(on_complete)
        def on_error(msg):
            self.progress_dialog.reset()
            self.error_msg = QMessageBox.critical(self, "Error", msg)
        self.extract_thread.error_abort.connect(on_error)
        self.extract_thread.start()

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

    def eventFilter(self, target, event):
        if event.type() == QEvent.Enter:
            ui_name = target.objectName()

            if ui_name.startswith("label_for_"):
                ui_name = ui_name[len("label_for_"):]

            option = self.option_map[ui_name]
            print(option)
            self.set_option_description(option["help"])

            return True
        elif event.type() == QEvent.Leave:
            self.set_option_description(None)
            return True

        return QMainWindow.eventFilter(self, target, event)

    def set_option_description(self, new_description):
        if new_description is None:
            self.ui.option_description.setText("(Hover over an option to see a description of what it does.)")
            self.ui.option_description.setStyleSheet("color: grey;")
        else:
            self.ui.option_description.setText(new_description)
            self.ui.option_description.setStyleSheet("")


def run_main_gui():
    app = QtWidgets.QApplication([])

    widget = RandoGUI()
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main_gui()
