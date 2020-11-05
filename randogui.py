from collections import OrderedDict
from io import BytesIO
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from urllib import request
import os

import subprocess
import zipfile

import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from ui_randogui import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow, QAbstractButton, QComboBox, QSpinBox, QListView, QCheckBox, \
    QRadioButton, QFileDialog, QProgressDialog
from PySide2.QtCore import QFile, QThread, Signal

from ssrando import Randomizer
from witmanager import WitManager
from options import OPTIONS, Options
from logic.constants import ALL_TYPES


class RandoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.wit_manager = WitManager(Path('.').resolve())
        self.randothread = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = {
            "clean_iso_path": "",
            "output_folder": "",
            "seed": "",
        }

        self.options = Options()

        for option_key, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                ui_name = option.get('ui',None)
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

    def set_iso_location(self):
        iso_path = filedialog.askopenfile()
        if iso_path is not None:
            self.iso_location.delete(0, 'end')
            self.iso_location.insert(0, iso_path.name)

    def randomize(self):
        if not self.randothread is None:
            print('ERROR: tried to randomize multiple times at once!')
            return
        if self.settings["seed"] == "":
            self.settings["seed"] = -1
        self.options.set_option("seed",int(self.settings["seed"]))
        dry_run = self.options['dry-run']
        # make sure user can't mess with the options now
        rando = Randomizer(self.options.copy())

        # progress bar
        self.progress_dialog=QProgressDialog(self)
        self.progress_dialog.setWindowTitle('Randomizing')
        self.progress_dialog.setMinimum(0)
        if dry_run:
            extra_steps=1
        else:
            extra_steps=5 #wit setup, extract, copy, wit copy
        self.progress_dialog.setMaximum(rando.get_total_progress_steps()+extra_steps)
        def ui_progress_callback(current_action, completed_steps):
            self.progress_dialog.setValue(completed_steps)
            self.progress_dialog.setLabelText(current_action)
        self.randothread = RandomizerThread(rando, self.wit_manager, self.settings)
        self.randothread.update_progress.connect(ui_progress_callback)
        self.randothread.randomization_complete.connect(self.wait_for_randothread)
        self.randothread.start()

    def wait_for_randothread(self):
        if not self.randothread is None:
            self.randothread.wait()
            self.randothread = None

    def browse_for_iso(self):
        if self.settings["clean_iso_path"] and os.path.isfile(self.settings["clean_iso_path"]):
            default_dir = os.path.dirname(self.settings["clean_iso_path"])
        else:
            default_dir = None

        clean_iso_path, selected_filter = QFileDialog.getOpenFileName(self, "Select Clean Skyward Sword NTSC-U 1.0 ISO",
                                                                      default_dir, "Wii ISO Files (*.iso)")
        if not clean_iso_path:
            return
        self.ui.clean_iso_path.setText(clean_iso_path)
        self.update_settings()

    def browse_for_output_dir(self):
        if self.settings["output_folder"] and os.path.isfile(self.settings["output_folder"]):
            default_dir = os.path.dirname(self.settings["output_folder"])
        else:
            default_dir = None

        output_folder = QFileDialog.getExistingDirectory(self, "Select output folder", default_dir)
        if not output_folder:
            return
        self.ui.output_folder.setText(output_folder)
        self.update_settings()

    def update_ui_for_settings(self):
        self.ui.clean_iso_path.setText(self.settings["clean_iso_path"])
        self.ui.output_folder.setText(self.settings["output_folder"])
        self.ui.seed.setText(self.settings["seed"])
        for option_key, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                ui_name = option.get('ui',None)
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
        self.settings["clean_iso_path"] = self.ui.clean_iso_path.text()
        self.settings["output_folder"] = self.ui.output_folder.text()
        self.settings["seed"] = self.ui.seed.text()

        for option_command, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                ui_name = option.get('ui',None)
                if not ui_name:
                    continue
                self.options.set_option(option_command, self.get_option_value(ui_name))

        self.options.set_option("banned-types", self.get_banned_types())
        print(self.settings)
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

class RandomizerThread(QThread):
    update_progress = Signal(str, int)
    randomization_complete = Signal()

    def __init__(self, randomizer: Randomizer, wit_manager: WitManager, settings):
        QThread.__init__(self)
    
        self.randomizer = randomizer
        self.wit_manager = wit_manager
        self.settings = settings
        self.steps = 0
  
    def ui_progress_callback(self, action):
        self.update_progress.emit(action, self.steps)
        self.steps += 1
    
    def run(self):
        dry_run = self.randomizer.options['dry-run']
        if not dry_run:
            self.ui_progress_callback('setting up wiimms ISO tools...')
            self.wit_manager.ensure_wit_installed()

            clean_iso_path = self.settings["clean_iso_path"]

            self.ui_progress_callback('extracting game...')
            if not self.wit_manager.actual_extract_already_exists():
                self.wit_manager.extract_game(clean_iso_path)

            self.ui_progress_callback('copying extract...')
            if not self.wit_manager.modified_extract_already_exists():
                self.wit_manager.copy_to_modified()

            output_folder = self.settings["output_folder"]
        print(self.randomizer.seed)
        self.randomizer.set_progress_callback(self.ui_progress_callback)
        self.randomizer.randomize()
        if not dry_run:
            self.ui_progress_callback('repacking game...')
            self.wit_manager.reapack_game(Path(output_folder), self.randomizer.seed, use_wbfs=True)

        self.ui_progress_callback('done')
        self.randomization_complete.emit()

def run_main_gui():
    app = QtWidgets.QApplication([])

    widget = RandoGUI()
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main_gui()