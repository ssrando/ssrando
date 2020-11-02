from collections import OrderedDict
from io import BytesIO
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from ssrando import Randomizer
from urllib import request

import subprocess
import zipfile

import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
from ui_randogui import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow, QAbstractButton, QComboBox, QSpinBox, QListView, QCheckBox, \
    QRadioButton
from PySide2.QtCore import QFile

from options import *


class RandoGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.wit_url = "https://wit.wiimm.de/download/wit-v3.03a-r8245-cygwin.zip"
        self.wit_folder = "wit-v3.03a-r8245-cygwin"

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = {}

        for option in OPTIONS:
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

        self.ui.randomize_button.clicked.connect(self.randomize)

    def randomize(self):
        Thread(target=self.offthread_randomize).start()

    def set_iso_location(self):
        iso_path = filedialog.askopenfile()
        if iso_path is not None:
            self.iso_location.delete(0, 'end')
            self.iso_location.insert(0, iso_path.name)

    def offthread_randomize(self):
        if not (Path(".") / self.wit_folder).is_dir():
            # fetch and unzip wit dependency
            print("wit not found, installing")
            with zipfile.ZipFile(BytesIO(request.urlopen(self.wit_url).read())) as wit_zip:
                wit_zip.extractall(Path(".") / self.wit_folder)

        if not (Path(".") / "actual-extract").is_dir():
            subprocess.run([(Path(".") / self.wit_folder / self.wit_folder / "bin" / "wit"), "-P", "extract", "disc.iso", "actual-extract"])
        if not (Path(".") / "modified-extract").is_dir():
            subprocess.run(["xcopy", "/E", "/I", "actual-extract", "modified-extract"])
        rando = Randomizer(OrderedDict([('dry-run', False), ('randomize-tablets', False), ('closed-thunderhead', True), ('swordless', False), ('invisible-sword', False), ('empty-unrequired-dungeons', True), ('banned-types', ''), ('seed', -1)]))
        print(rando.seed)
        rando.randomize()
        iso_name = "SS Randomizer " + str(rando.seed) + ".iso"
        subprocess.run([(Path(".") / self.wit_folder / "bin" / "wit").name, "-P", "copy", "modified-extract", iso_name])

    def browse_for_iso(self):
        pass

    def browse_for_output_dir(self):
        pass

    def update_settings(self):
        self.settings["clean_iso_path"] = self.ui.clean_iso_path.text()
        self.settings["output_folder"] = self.ui.output_folder.text()
        self.settings["seed"] = self.ui.seed.text()

        for option in OPTIONS:
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                self.settings[option["command"]] = self.get_option_value(option["ui"])
        print(self.settings)

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


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = RandoGUI()
    widget.show()

    sys.exit(app.exec_())