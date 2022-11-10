import os
import sys
from pathlib import Path
import random

import yaml
import json
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer, QEvent, QStringListModel
from PySide6.QtGui import QFontDatabase, QPalette, QColor
from PySide6.QtWidgets import (
    QMainWindow,
    QAbstractButton,
    QComboBox,
    QSpinBox,
    QListView,
    QCheckBox,
    QRadioButton,
    QFileDialog,
    QMessageBox,
    QErrorMessage,
    QInputDialog,
    QLineEdit,
    QApplication,
    QStyleFactory,
)
from gui.sort_model import LocationsModel
from hints.hint_distribution import InvalidHintDistribution

from logic.logic_input import Areas
from options import OPTIONS, Options
from gui.progressdialog import ProgressDialog
from gui.guithreads import RandomizerThread, ExtractSetupThread
from ssrando import Randomizer, VERSION
from paths import RANDO_ROOT_PATH
from gui.ui_randogui import Ui_MainWindow
from witmanager import WitManager

# Allow keyboard interrupts on the command line to instantly close the program.
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

NEW_PRESET = "[New Preset]"


class RandoGUI(QMainWindow):
    def __init__(self, areas: Areas, options: Options):
        super().__init__()

        self.wit_manager = WitManager(Path(".").resolve())
        self.randothread = None
        self.error_msg = None
        self.progress_dialog = None
        self.randomize_after_iso_extract = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        font_id = QFontDatabase.addApplicationFont(
            str(RANDO_ROOT_PATH / "assets" / "Lato-Regular.ttf")
        )
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = self.font()
        font.setFamily(family)
        font.setPointSize(9)
        self.setFont(font)

        self.setWindowTitle("Skyward Sword Randomizer v" + VERSION)

        self.areas = areas
        self.options = options
        self.settings_path = "settings.txt"
        if os.path.isfile(self.settings_path):
            with open(self.settings_path) as f:
                try:
                    self.options.update_from_dict(json.load(f))
                except Exception as e:
                    print("couldn't update from saved settings!", e)

        self.option_map = {}
        for option_key, option in OPTIONS.items():
            if option["name"] != "Seed":
                ui_name = option.get("ui", None)
                self.option_map[ui_name] = option
                if not ui_name:
                    continue
                widget = getattr(self.ui, ui_name)
                widget.installEventFilter(self)
                if isinstance(widget, QAbstractButton):
                    widget.setChecked(self.options[option_key])
                    widget.clicked.connect(self.update_settings)
                elif isinstance(widget, QComboBox):
                    for option_val in option["choices"]:
                        widget.addItem(str(option_val))
                    widget.setCurrentIndex(
                        option["choices"].index(self.options[option_key])
                    )
                    if option["name"] == "Logic Mode":
                        widget.currentIndexChanged.connect(self.logic_mode_changed)
                    widget.currentIndexChanged.connect(self.update_settings)
                elif isinstance(widget, QListView):
                    pass
                elif isinstance(widget, QSpinBox):
                    if "min" in option:
                        widget.setMinimum(option["min"])
                    if "max" in option:
                        widget.setMaximum(option["max"])
                    widget.setValue(self.options[option_key])
                    widget.valueChanged.connect(self.update_settings)

        # Tricks ui.
        self.enabled_tricks_model = QStringListModel()
        self.enabled_tricks_model.setStringList(
            OPTIONS["enabled-tricks-bitless"]["default"]
        )
        self.disabled_tricks_model = QStringListModel()
        self.disabled_tricks_model.setStringList(
            OPTIONS["enabled-tricks-bitless"]["choices"]
        )
        self.ui.enabled_tricks.setModel(self.enabled_tricks_model)
        self.ui.disabled_tricks.setModel(self.disabled_tricks_model)
        self.ui.enable_trick.clicked.connect(self.enable_trick)
        self.ui.disable_trick.clicked.connect(self.disable_trick)

        # setup exlcuded locations
        self.excluded_locations_model = QStringListModel()
        self.excluded_locations_proxy = LocationsModel()
        self.excluded_locations_proxy.setSourceModel(self.excluded_locations_model)
        self.excluded_locations_model.setStringList(
            OPTIONS["excluded-locations"]["default"]
        )
        self.included_locations_model = QStringListModel()
        self.included_locations_proxy = LocationsModel()
        self.included_locations_proxy.setSourceModel(self.included_locations_model)
        self.included_locations_model.setStringList(
            OPTIONS["excluded-locations"]["choices"]
        )
        self.ui.excluded_locations.setModel(self.excluded_locations_model)
        self.ui.included_locations.setModel(self.included_locations_model)
        self.ui.exclude_location.clicked.connect(self.exclude_location)
        self.ui.include_location.clicked.connect(self.include_location)

        # Starting Items ui.
        self.randomized_items_model = QStringListModel()
        self.randomized_items_model.setStringList(OPTIONS["starting-items"]["choices"])
        self.starting_items_model = QStringListModel()
        self.starting_items_model.setStringList(OPTIONS["starting-items"]["default"])
        self.ui.randomized_items.setModel(self.randomized_items_model)
        self.ui.starting_items.setModel(self.starting_items_model)
        self.ui.randomize_item.clicked.connect(self.remove_starting_item)
        self.ui.start_with_item.clicked.connect(self.add_starting_item)

        # setup presets
        self.default_presets = {}
        self.user_presets = {}
        self.ui.presets_list.addItem(NEW_PRESET)
        sep_idx = 1
        with (RANDO_ROOT_PATH / "gui" / "default_presets.json").open("r") as f:
            try:
                load_default_presets = json.load(f)
                for preset in load_default_presets:
                    self.ui.presets_list.addItem(preset)
                    self.default_presets[preset] = load_default_presets[preset]
                    sep_idx += 1
            except Exception as e:
                print("couldn't load default presets")
        self.ui.presets_list.insertSeparator(sep_idx)
        self.user_presets_path = "presets.txt"
        if os.path.isfile(self.user_presets_path):
            with open(self.user_presets_path) as f:
                try:
                    load_user_presets = json.load(f)
                    for preset in load_user_presets:
                        self.ui.presets_list.addItem(preset)
                        self.user_presets[preset] = load_user_presets[preset]
                except Exception as e:
                    print("couldn't load user presets", e)
        self.ui.presets_list.currentIndexChanged.connect(self.preset_selection_changed)
        self.ui.load_preset.clicked.connect(self.load_preset)
        self.ui.save_preset.clicked.connect(self.save_preset)
        self.ui.delete_preset.clicked.connect(self.delete_preset)
        self.preset_selection_changed()

        # hide currently unsupported options to make this version viable for public use
        getattr(self.ui, "label_for_option_got_starting_state").setVisible(False)
        getattr(self.ui, "option_got_starting_state").setVisible(False)
        getattr(self.ui, "label_for_option_got_dungeon_requirement").setVisible(False)
        getattr(self.ui, "option_got_dungeon_requirement").setVisible(False)
        self.enable_trick_interface()

        # hide supporting elements
        getattr(self.ui, "option_plando").setVisible(False)
        getattr(self.ui, "plando_file").setVisible(False)
        getattr(self.ui, "plando_file_browse").setVisible(False)
        getattr(self.ui, "option_json_spoiler").setVisible(False)

        self.ui.ouput_folder_browse_button.clicked.connect(self.browse_for_output_dir)
        self.ui.randomize_button.clicked.connect(self.randomize)
        self.ui.permalink.textChanged.connect(self.permalink_updated)
        self.ui.seed.textChanged.connect(self.update_settings)
        self.ui.seed_button.clicked.connect(self.gen_new_seed)
        self.update_ui_for_settings()
        self.update_settings()
        self.set_option_description(None)

        self.ui.tabWidget.setCurrentIndex(0)

        if "NOGIT" in VERSION:
            self.error_msg = QErrorMessage()
            self.error_msg.showMessage(
                "Running from source without git is not supported!"
            )

        elif not self.wit_manager.actual_extract_already_exists():
            self.ask_for_clean_iso()

    def ask_for_clean_iso(self):
        selected = QMessageBox.question(
            self,
            "Extract now?",
            "For randomizing purposes, a clean NTSC-U 1.00 ISO is needed, browse for it now? This is only needed once",
            defaultButton=QMessageBox.Yes,
        )
        if selected == QMessageBox.Yes:
            self.browse_for_iso()
        else:
            self.randomize_after_iso_extract = False

    def randomize(self):
        if not self.randothread is None:
            print("ERROR: tried to randomize multiple times at once!")
            return
        dry_run = self.options["dry-run"]
        if not (dry_run or self.wit_manager.actual_extract_already_exists()):
            self.randomize_after_iso_extract = True
            self.ask_for_clean_iso()
            return
        # make sure user can't mess with the options now
        self.rando = Randomizer(self.areas, self.options.copy())

        if dry_run:
            extra_steps = 1  # done
        else:
            extra_steps = 101  # wit create wbfs + done

        self.progress_dialog = ProgressDialog(
            "Randomizing",
            "Initializing...",
            self.rando.get_total_progress_steps + extra_steps,
        )
        self.randomizer_thread = RandomizerThread(
            self.rando, self.wit_manager, self.options["output-folder"]
        )
        self.randomizer_thread.update_progress.connect(self.ui_progress_callback)
        self.randomizer_thread.randomization_complete.connect(
            self.randomization_complete
        )
        self.randomizer_thread.error_abort.connect(self.on_error)
        self.randomizer_thread.start()

    def ui_progress_callback(self, current_action, completed_steps, total_steps=None):
        self.progress_dialog.setValue(completed_steps)
        self.progress_dialog.setLabelText(current_action)
        if not total_steps is None:
            self.progress_dialog.setMaximum(total_steps)

    def on_error(self, message):
        self.error_msg = QErrorMessage(self)
        if self.progress_dialog:
            self.progress_dialog.reset()
        self.error_msg.showMessage(message)

    def randomization_complete(self):
        self.progress_dialog.reset()

        if self.options["no-spoiler-log"]:
            text = f"""Randomization complete.<br>RANDO HASH: {self.rando.randomizer_hash}"""
        else:
            text = f"""Randomization complete.<br>RANDO HASH: {self.rando.randomizer_hash}<br>
                    If you get stuck, check the progression spoiler log in the output folder."""

        self.complete_dialog = QMessageBox()
        self.complete_dialog.setTextFormat(Qt.TextFormat.RichText)
        self.complete_dialog.setWindowTitle("Randomization complete")
        self.complete_dialog.setText(text)
        self.complete_dialog.setWindowIcon(self.windowIcon())
        self.complete_dialog.show()
        self.randomizer_thread = None

    def browse_for_iso(self):
        clean_iso_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Select Clean Skyward Sword NTSC-U 1.0 ISO",
            None,
            "Wii ISO Files (*.iso)",
        )
        if not clean_iso_path:
            return
        self.progress_dialog = ProgressDialog(
            "Extracting Game Files", "Initializing...", 100
        )
        self.progress_dialog.setAutoClose(True)
        self.extract_thread = ExtractSetupThread(self.wit_manager, clean_iso_path, None)
        self.extract_thread.update_total_steps.connect(
            lambda total_steps: self.progress_dialog.setMaximum(total_steps)
        )
        self.extract_thread.update_progress.connect(self.ui_progress_callback)

        def on_complete():
            self.progress_dialog.reset()
            if self.randomize_after_iso_extract:
                self.randomize()

        self.extract_thread.extract_complete.connect(on_complete)

        self.extract_thread.error_abort.connect(self.on_error)
        self.extract_thread.start()

    def browse_for_output_dir(self):
        if self.options["output-folder"] and os.path.isfile(
            self.options["output-folder"]
        ):
            default_dir = os.path.dirname(self.options["output-folder"])
        else:
            default_dir = None

        output_folder = QFileDialog.getExistingDirectory(
            self, "Select output folder", default_dir
        )
        if not output_folder:
            return
        self.ui.output_folder.setText(output_folder)
        self.update_settings()

    def update_ui_for_settings(self):
        current_settings = self.options.copy()
        self.ui.output_folder.setText(str(self.options["output-folder"]))
        self.ui.seed.setText(str(self.options["seed"]))
        for option_key, option in OPTIONS.items():
            if option["name"] != "Seed":
                ui_name = option.get("ui", None)
                if not ui_name:
                    continue
                widget = getattr(self.ui, ui_name)
                if isinstance(widget, QAbstractButton):
                    widget.setChecked(current_settings[option_key])
                elif isinstance(widget, QComboBox):
                    widget.setCurrentIndex(
                        option["choices"].index(current_settings[option_key])
                    )
                elif isinstance(widget, QListView):
                    pass
                elif isinstance(widget, QSpinBox):
                    widget.setValue(current_settings[option_key])
                    getattr(self.ui, f"label_for_{ui_name}").installEventFilter(self)
                    # Update health counter label.
                    if ui_name in (
                        "option_starting_heart_containers",
                        "option_starting_heart_pieces",
                    ):
                        heart_string = getattr(
                            self.ui, "current_starting_health_counter"
                        )
                        heart_containers = current_settings["starting-heart-containers"]
                        heart_pieces = current_settings["starting-heart-pieces"]
                        health = 24 + heart_containers * 4 + heart_pieces
                        health_string = str(health // 4) + " hearts"
                        if health % 4 == 1:
                            health_string += " and 1 piece"
                        elif health % 4 > 1:
                            health_string += " and " + str(health % 4) + " pieces"
                        heart_string.setText(health_string)

        self.enabled_tricks_model = QStringListModel()
        self.disabled_tricks_model = QStringListModel()
        if "Glitchless" in current_settings["logic-mode"]:
            self.enabled_tricks_model.setStringList([])
            self.disabled_tricks_model.setStringList([])
        elif "BiTless" in current_settings["logic-mode"]:
            self.enabled_tricks_model.setStringList(
                current_settings["enabled-tricks-bitless"]
            )
            self.disabled_tricks_model.setStringList(
                [
                    choice
                    for choice in OPTIONS["enabled-tricks-bitless"]["choices"]
                    if choice not in current_settings["enabled-tricks-bitless"]
                ]
            )
        elif "Glitched" in current_settings["logic-mode"]:
            self.enabled_tricks_model.setStringList(
                current_settings["enabled-tricks-glitched"]
            )
            self.disabled_tricks_model.setStringList(
                [
                    choice
                    for choice in OPTIONS["enabled-tricks-glitched"]["choices"]
                    if choice not in current_settings["enabled-tricks-glitched"]
                ]
            )
        else:
            self.enabled_tricks_model.setStringList([])
            self.disabled_tricks_model.setStringList([])

        # Update tricks.
        self.enabled_tricks_model.sort(0)
        self.disabled_tricks_model.sort(0)
        self.ui.enabled_tricks.setModel(self.enabled_tricks_model)
        self.ui.disabled_tricks.setModel(self.disabled_tricks_model)

        # Update locations.
        self.excluded_locations_model.setStringList(
            current_settings["excluded-locations"]
        )
        self.included_locations_model.setStringList(
            [
                choice
                for choice in OPTIONS["excluded-locations"]["choices"]
                if choice not in current_settings["excluded-locations"]
            ]
        )
        self.ui.excluded_locations.setModel(self.excluded_locations_model)
        self.ui.included_locations.setModel(self.included_locations_model)

        # Update starting items.
        self.randomized_items_model = QStringListModel()
        self.starting_items_model = QStringListModel()
        randomized_items_list = [
            choice for choice in OPTIONS["starting-items"]["choices"]
        ]
        for item in current_settings["starting-items"]:
            randomized_items_list.remove(item)
        self.randomized_items_model.setStringList(randomized_items_list)
        self.starting_items_model.setStringList(current_settings["starting-items"])
        self.ui.randomized_items.setModel(self.randomized_items_model)
        self.ui.starting_items.setModel(self.starting_items_model)
        self.ui.permalink.setText(current_settings.get_permalink())

    def save_settings(self):
        with open(self.settings_path, "w") as f:
            json.dump(self.options.to_dict(), f)

    def update_settings(self):
        self.options.set_option("output-folder", self.ui.output_folder.text())
        try:
            self.options.set_option("seed", int(self.ui.seed.text()))
        except ValueError:
            if self.ui.seed.text() == "":
                self.options.set_option("seed", -1)
            else:
                # TODO: give an error dialog or some sort of error message that the seed is invalid
                pass

        for option_command, option in OPTIONS.items():
            if option["name"] != "Seed" and "Enabled Tricks" not in option["name"]:
                ui_name = option.get("ui", None)
                if not ui_name:
                    continue
                self.options.set_option(option_command, self.get_option_value(ui_name))

        # handle tricks
        logic_mode = getattr(self.ui, "option_logic_mode").currentText()
        if "Glitchless" in logic_mode:
            self.options.set_option("enabled-tricks-bitless", [])
            self.options.set_option("enabled-tricks-glitched", [])
        elif "BiTless" in logic_mode:
            self.options.set_option(
                "enabled-tricks-bitless", self.get_option_value("enabled_tricks")
            )
            self.options.set_option("enabled-tricks-glitched", [])
        elif "Glitched" in logic_mode:
            self.options.set_option("enabled-tricks-bitless", [])
            self.options.set_option(
                "enabled-tricks-glitched", self.get_option_value("enabled_tricks")
            )
        else:  # this should only be no logic
            self.options.set_option("enabled-tricks-bitless", [])
            self.options.set_option("enabled-tricks-glitched", [])

        self.options.set_option(
            "excluded-locations", self.get_option_value("excluded_locations")
        )

        self.save_settings()
        self.ui.permalink.setText(self.options.get_permalink())

    def logic_mode_changed(self):
        value = getattr(self.ui, "option_logic_mode").currentText()
        if "Glitchless" in value:
            self.disable_trick_interface()
        elif "BiTless" in value:
            # swap bitless tricks into the ui
            self.enable_trick_interface()
            self.enabled_tricks_model.setStringList(
                OPTIONS["enabled-tricks-bitless"]["default"]
            )
            self.disabled_tricks_model.setStringList(
                OPTIONS["enabled-tricks-bitless"]["choices"]
            )
        elif "Glitched" in value:
            # swap the glitched tricks into the ui
            self.enable_trick_interface()
            self.enabled_tricks_model.setStringList(
                OPTIONS["enabled-tricks-glitched"]["default"]
            )
            self.disabled_tricks_model.setStringList(
                OPTIONS["enabled-tricks-glitched"]["choices"]
            )
        else:  # this should only be no logic
            # disable the trick interface
            self.disable_trick_interface()

    def enable_trick_interface(self):
        getattr(self.ui, "enable_trick").setEnabled(True)
        getattr(self.ui, "disable_trick").setEnabled(True)
        getattr(self.ui, "enabled_tricks").setEnabled(True)
        getattr(self.ui, "disabled_tricks").setEnabled(True)

    def disable_trick_interface(self):
        getattr(self.ui, "enable_trick").setEnabled(False)
        getattr(self.ui, "disable_trick").setEnabled(False)
        getattr(self.ui, "enabled_tricks").setEnabled(False)
        getattr(self.ui, "disabled_tricks").setEnabled(False)

    def get_option_value(self, option_name):
        widget = getattr(self.ui, option_name)
        if isinstance(widget, QCheckBox) or isinstance(widget, QRadioButton):
            return widget.isChecked()
        elif isinstance(widget, QComboBox):
            return widget.itemText(widget.currentIndex())
        elif isinstance(widget, QSpinBox):
            return widget.value()
        elif isinstance(widget, QListView):
            return widget.model().stringList()
        else:
            print("Option widget is invalid: %s" % option_name)

    @staticmethod
    def append_row(model, value):
        model.insertRow(model.rowCount())
        new_row = model.index(model.rowCount() - 1, 0)
        model.setData(new_row, value)

    def move_selected_rows(self, source, dest):
        selection = source.selectionModel().selectedIndexes()
        # Remove starting from the last so the previous indices remain valid
        selection.sort(reverse=True, key=lambda x: x.row())
        for item in selection:
            value = item.data()
            source.model().removeRow(item.row())
            self.append_row(dest.model(), value)

    def enable_trick(self):
        self.move_selected_rows(self.ui.disabled_tricks, self.ui.enabled_tricks)
        self.ui.enabled_tricks.model().sort(0)
        self.update_settings()

    def disable_trick(self):
        self.move_selected_rows(self.ui.enabled_tricks, self.ui.disabled_tricks)
        self.ui.disabled_tricks.model().sort(0)
        self.update_settings()

    def exclude_location(self):
        self.move_selected_rows(self.ui.included_locations, self.ui.excluded_locations)
        self.update_settings()

    def include_location(self):
        self.move_selected_rows(self.ui.excluded_locations, self.ui.included_locations)
        self.update_settings()

    def remove_starting_item(self):
        self.move_selected_rows(self.ui.starting_items, self.ui.randomized_items)
        self.ui.starting_items.model().sort(0)
        self.ui.randomized_items.model().sort(0)
        self.update_settings()

    def add_starting_item(self):
        self.move_selected_rows(self.ui.randomized_items, self.ui.starting_items)
        self.ui.starting_items.model().sort(0)
        self.ui.randomized_items.model().sort(0)
        self.update_settings()

    def load_preset(self):
        preset = self.ui.presets_list.currentText()
        # prevent loading the new preset option
        if preset == NEW_PRESET:
            return
        if preset in self.default_presets:
            self.options.update_from_dict(self.default_presets[preset])
        else:
            self.options.update_from_dict(self.user_presets[preset])
        self.update_ui_for_settings()
        self.update_settings()

    def save_preset(self):
        preset = self.ui.presets_list.currentText()
        if preset in self.default_presets:
            self.error_msg = QErrorMessage()
            self.error_msg.showMessage(
                "Default presets are protected and cannot be updated"
            )
            return
        if preset == NEW_PRESET:
            (name, ok) = QInputDialog.getText(
                self,
                "Create New Preset",
                "Enter a name for the new preset",
                QLineEdit.Normal,
            )
            if ok:
                if name in self.default_presets or name in self.user_presets:
                    self.error_msg = QErrorMessage()
                    self.error_msg.showMessage("Cannot have duplicate preset names")
                    return
                elif name == NEW_PRESET:
                    self.error_msg = QErrorMessage()
                    self.error_msg.showMessage("Invalid preset name")
                    return
                else:
                    preset = name
                    self.ui.presets_list.addItem(preset)
                    self.ui.presets_list.setCurrentText(preset)
        self.user_presets[preset] = self.options.to_dict(
            True,
            [
                "no-spoiler-log",
            ],
        )
        self.write_presets()

    def preset_selection_changed(self):
        preset = self.ui.presets_list.currentText()
        if preset == NEW_PRESET:
            self.ui.load_preset.setDisabled(True)
            self.ui.save_preset.setDisabled(False)
            self.ui.delete_preset.setDisabled(True)
        elif preset in self.default_presets:
            self.ui.load_preset.setDisabled(False)
            self.ui.save_preset.setDisabled(True)
            self.ui.delete_preset.setDisabled(True)
        else:
            self.ui.load_preset.setDisabled(False)
            self.ui.save_preset.setDisabled(False)
            self.ui.delete_preset.setDisabled(False)

    def delete_preset(self):
        preset = self.ui.presets_list.currentText()
        # protect from deleting default presets
        if preset == NEW_PRESET or preset in self.default_presets:
            self.error_msg = QErrorMessage()
            self.error_msg.showMessage(
                "Default presets are protected and cannot be deleted"
            )
            return
        index = self.ui.presets_list.currentIndex()
        del self.user_presets[preset]
        self.ui.presets_list.removeItem(index)
        self.ui.presets_list.setCurrentIndex(0)
        self.write_presets()

    def write_presets(self):
        with open(self.user_presets_path, "w") as f:
            json.dump(self.user_presets, f)

    def eventFilter(self, target, event):
        if event.type() == QEvent.Enter:
            ui_name = target.objectName()

            if ui_name.startswith("label_for_"):
                ui_name = ui_name[len("label_for_") :]

            option = self.option_map[ui_name]
            self.set_option_description(option["help"])

            return True
        elif event.type() == QEvent.Leave:
            self.set_option_description(None)
            return True

        return QMainWindow.eventFilter(self, target, event)

    def set_option_description(self, new_description):
        if new_description is None:
            self.ui.option_description.setText(
                "(Hover over an option to see a description of what it does.)"
            )
            self.ui.option_description.setStyleSheet("color: grey;")
        else:
            self.ui.option_description.setText(new_description)
            self.ui.option_description.setStyleSheet("")

    def permalink_updated(self):
        try:
            self.options.update_from_permalink(self.ui.permalink.text())
        except ValueError as e:
            # Ignore errors from faultly permalinks, with updating ui it gets reset anyways
            print(e)
        except IndexError as e:
            print(e)
        self.update_ui_for_settings()

    def gen_new_seed(self):
        self.ui.seed.setText(str(random.randrange(0, 1_000_000)))


def run_main_gui(areas: Areas, options: Options):
    app = QApplication([])
    app.setStyle(QStyleFactory.create("fusion"))

    # darkPalette = QPalette()
    # darkColor = QColor(45, 45, 45)
    # disabledColor = QColor(127, 127, 127)
    # darkPalette.setColor(QPalette.Window, darkColor)
    # darkPalette.setColor(QPalette.WindowText, Qt.white)
    # darkPalette.setColor(QPalette.Base, QColor(18, 18, 18))
    # darkPalette.setColor(QPalette.AlternateBase, darkColor)
    # darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
    # darkPalette.setColor(QPalette.ToolTipText, Qt.white)
    # darkPalette.setColor(QPalette.Text, Qt.white)
    # darkPalette.setColor(QPalette.Disabled, QPalette.Text, disabledColor)
    # darkPalette.setColor(QPalette.Button, darkColor)
    # darkPalette.setColor(QPalette.ButtonText, Qt.white)
    # darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, disabledColor)
    # darkPalette.setColor(QPalette.BrightText, Qt.red)
    # darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))

    # darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # darkPalette.setColor(QPalette.HighlightedText, Qt.black)
    # darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, disabledColor)

    # app.setPalette(darkPalette)
    app.setStyleSheet(
        "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
    )

    widget = RandoGUI(areas, options)
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main_gui()
