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
    QRadioButton, QFileDialog
from PySide2.QtCore import QFile

from ssrando import Randomizer
from witmanager import WitManager
from options import OPTIONS, Options
from logic.constants import ALL_TYPES


class RandoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.wit_manager = WitManager(Path('.').resolve())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = {
            "clean_iso_path": "",
            "output_folder": "",
            "seed": "",
        }

        self.options = Options()

        for option in OPTIONS.values():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                widget = getattr(self.ui, option["ui"])
                if isinstance(widget, QAbstractButton):
                    widget.clicked.connect(self.update_settings)
                elif isinstance(widget, QComboBox):
                    widget.clicked.connect(self.update_settings)
                elif isinstance(widget, QListView):
                    pass
                elif isinstance(widget, QSpinBox):
                    widget.valueChanged.connect(self.update_settings)

        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            widget.clicked.connect(self.update_settings)

        self.ui.clean_iso_browse_button.clicked.connect(self.browse_for_iso)
        self.ui.ouput_folder_browse_button.clicked.connect(self.browse_for_output_dir)
        self.ui.randomize_button.clicked.connect(self.randomize)

    def randomize(self):
        Thread(target=self.offthread_randomize).start()

    def set_iso_location(self):
        iso_path = filedialog.askopenfile()
        if iso_path is not None:
            self.iso_location.delete(0, 'end')
            self.iso_location.insert(0, iso_path.name)

    def offthread_randomize(self):
        dry_run = self.options['dry-run']
        if not dry_run:
            self.wit_manager.ensure_wit_installed()

            clean_iso_path = self.settings.pop("clean_iso_path")

            if not self.wit_manager.actual_extract_already_exists():
                print('extracting game...')
                self.wit_manager.extract_game(clean_iso_path)

            if not self.wit_manager.modified_extract_already_exists():
                print('copying extract...')
                self.wit_manager.copy_to_modified()

            output_folder = self.settings.pop("output_folder")
        if self.settings["seed"] == "":
            self.settings["seed"] = -1
        self.options.set_option("seed",int(self.settings["seed"]))
        rando = Randomizer(self.options)
        print(rando.seed)
        rando.randomize()
        if not dry_run:
            self.wit_manager.reapack_game(Path(output_folder), rando.seed, use_wbfs=True)

        self.update_settings()

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

    def update_settings(self):
        self.settings["clean_iso_path"] = self.ui.clean_iso_path.text()
        self.settings["output_folder"] = self.ui.output_folder.text()
        self.settings["seed"] = self.ui.seed.text()

        for option_command, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                self.options.set_option(option_command, self.get_option_value(option["ui"]))

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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = RandoGUI()
    widget.show()

    sys.exit(app.exec_())
