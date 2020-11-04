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
from PySide2.QtWidgets import QMainWindow, QAbstractButton, QComboBox, QSpinBox, QListView, QCheckBox, \
    QRadioButton, QFileDialog

from options import *
from ssrando import Randomizer
from ui_randogui import Ui_MainWindow


class RandoGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.wit_url = "https://wit.wiimm.de/download/wit-v3.03a-r8245-cygwin.zip"
        self.wit_folder = "wit-v3.03a-r8245-cygwin"

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = {
            "clean_iso_path": "",
            "output_folder": "",
            "seed": ""
        }

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
        if not self.settings["dry-run"]:
            if not (Path(".") / self.wit_folder).is_dir():
                # fetch and unzip wit dependency
                print("wit not found, installing")
                with zipfile.ZipFile(BytesIO(request.urlopen(self.wit_url).read())) as wit_zip:
                    wit_zip.extractall(Path(".") / self.wit_folder)

            clean_iso_path = self.settings.pop("clean_iso_path")

            if not (Path(".") / "actual-extract").is_dir():
                subprocess.run(
                    [(Path(".") / self.wit_folder / self.wit_folder / "bin" / "wit"), "-P", "extract",
                     (Path(clean_iso_path)), "actual-extract"])
            if not (Path(".") / "modified-extract").is_dir():
                subprocess.run(["xcopy", "/E", "/I", "actual-extract", "modified-extract"])

        output_folder = self.settings.pop("output_folder")
        if self.settings["seed"] == "":
            self.settings["seed"] = -1
        rando = Randomizer(self.settings)
        print(rando.seed)
        rando.randomize()
        if not self.settings["dry-run"]:
            iso_name = "SS Randomizer " + str(rando.seed) + ".iso"
            subprocess.run([(Path(".") / self.wit_folder / "bin" / "wit").name, "-P", "copy", "modified-extract",
                            (Path(output_folder) / iso_name)])

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

        for option in OPTIONS:
            if option["name"] != "Banned Types" and option["name"] != "Seed":
                self.settings[option["command"]] = self.get_option_value(option["ui"])

        self.settings["banned-types"] = self.get_banned_types()
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

    def get_banned_types(self):
        banned_types = []
        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            if not widget.isChecked():
                banned_types.append(check_type)
        return ",".join(banned_types)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = RandoGUI()
    widget.show()

    sys.exit(app.exec_())
