import os
import sys
from pathlib import Path
from gui.components.list_pair import ListPair
import pyclip
import qdarktheme
import random
import colorReplace as cr
import cv2

import json
from PySide6.QtCore import Qt, QEvent, QObject, QStringListModel
from PySide6.QtGui import QFontDatabase, QIcon, QImage, QPixmap
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QCheckBox,
    QComboBox,
    QErrorMessage,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSpinBox,
)
from gui.components.color_button import ColorButton
from gui.dialogs.tricks.tricks_dialog import TricksDialog
from gui.dialogs.custom_theme.custom_theme_dialog import CustomThemeDialog

from logic.logic_input import Areas
from options import OPTIONS, Options
from gui.dialogs.progressbar.progressdialog import ProgressDialog
from gui.guithreads import RandomizerThread, ExtractSetupThread
from ssrando import Randomizer, VERSION
from paths import RANDO_ROOT_PATH
from gui.ui_randogui import Ui_MainWindow
from witmanager import WitManager

# Allow keyboard interrupts on the command line to instantly close the program.
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

LOGIC_MODE_TO_TRICKS_SETTING = {
    "Glitchless": None,
    "BiTless": "enabled-tricks-bitless",
    "Glitched": "enabled-tricks-glitched",
    "No Logic": None,
}

NEW_PRESET = "[New Preset]"
DEFAULT_PRESETS_PATH = RANDO_ROOT_PATH / "gui" / "presets" / "default_presets.json"
DEFAULT_THEME_PATH = RANDO_ROOT_PATH / "gui" / "themes" / "default_theme.json"
HIGH_CONTRAST_THEME_PATH = (
    RANDO_ROOT_PATH / "gui" / "themes" / "high_contrast_theme.json"
)
READABILITY_THEME_PATH = RANDO_ROOT_PATH / "gui" / "themes" / "readability_theme.json"
CUSTOM_THEME_PATH = "custom_theme.json"

LINK_MODEL_DATA_PATH = RANDO_ROOT_PATH / "assets" / "default-link-data"
CUSTOM_MODELS_PATH = Path("models")

# Add stylesheet overrides here.
BASE_STYLE_SHEET_OVERRIDES = ""


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

        QFontDatabase.addApplicationFont(
            str(RANDO_ROOT_PATH / "assets" / "Lato-Regular.ttf")
        )
        QFontDatabase.addApplicationFont(
            str(RANDO_ROOT_PATH / "assets" / "OpenDyslexic3-Regular.ttf")
        )

        self.setWindowTitle("Skyward Sword Randomizer v" + VERSION)

        self.setWindowIcon(QIcon(str(RANDO_ROOT_PATH / "assets" / "icon.ico")))

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
                    if option["name"] == "Font Family":
                        widget.currentFontChanged.connect(self.update_font)
                        widget.currentIndexChanged.connect(self.update_settings)
                        continue
                    if option["name"] == "Selected Model Pack":
                        widget.addItem(option["default"])
                        widget.currentIndexChanged.connect(self.update_settings)
                        continue
                    for option_val in option["choices"]:
                        widget.addItem(str(option_val))
                    widget.setCurrentIndex(
                        option["choices"].index(self.options[option_key])
                    )
                    if option["name"] == "Logic Mode":
                        widget.currentIndexChanged.connect(self.logic_mode_changed)
                    elif option["name"] == "GUI Theme Mode":
                        widget.currentTextChanged.connect(self.update_theme)
                    elif option["name"] == "GUI Theme Preset":
                        widget.currentTextChanged.connect(self.update_theme_preset)
                    widget.currentIndexChanged.connect(self.update_settings)
                elif isinstance(widget, QListView):
                    pass
                elif isinstance(widget, QSpinBox):
                    if "min" in option:
                        widget.setMinimum(option["min"])
                    if "max" in option:
                        widget.setMaximum(option["max"])
                    widget.setValue(self.options[option_key])

                    if option["name"] == "Font Size":
                        widget.valueChanged.connect(self.update_font)
                    else:
                        widget.valueChanged.connect(self.update_settings)

        # Accessibility setup.
        self.custom_theme_path = CUSTOM_THEME_PATH
        match self.options["gui-theme-preset"]:
            case "Default":
                self.default_theme_path = DEFAULT_THEME_PATH
            case "High Contrast":
                self.default_theme_path = HIGH_CONTRAST_THEME_PATH
            case "Readability":
                self.default_theme_path = READABILITY_THEME_PATH
            case _:
                raise ValueError(
                    f"Invalid option for gui-theme-preset option. Expected one of ('Default', 'High Contrast', 'Readability') but found {self.options['gui-theme-preset']}."
                )

        if not os.path.isfile(self.custom_theme_path):
            with open(self.default_theme_path) as f:
                default_theme_json = json.load(f)
            with open(self.custom_theme_path, "w") as f:
                json.dump(default_theme_json, f)

        self.ui.custom_theme_button.clicked.connect(self.open_custom_theme_picker)
        self.ui.option_use_custom_theme.stateChanged.connect(self.toggle_custom_theme)
        if self.options["use-custom-theme"]:
            self.toggle_custom_theme(1)
        else:
            self.toggle_custom_theme(0)
        self.ui.option_use_sharp_corners.stateChanged.connect(self.toggle_sharp_corners)
        if self.options["use-sharp-corners"]:
            self.toggle_sharp_corners(1)
        else:
            self.toggle_sharp_corners(0)

        self.ui.reset_font_button.clicked.connect(self.reset_font)

        # setup misc controls
        self.ui.edit_tricks.clicked.connect(self.launch_tricks_dialog)
        self.logic_mode_changed()

        # Exlcuded Locations UI
        self.exclude_locations_pair = ListPair(
            self.ui.excluded_locations,
            self.ui.included_locations,
            "excluded-locations",
            self.ui.exclude_location,
            self.ui.include_location,
        )
        self.exclude_locations_pair.listPairChanged.connect(self.update_settings)

        self.ui.excluded_free_search.textChanged.connect(
            self.exclude_locations_pair.update_option_list_filter
        )
        self.ui.included_free_search.textChanged.connect(
            self.exclude_locations_pair.update_non_option_list_filter
        )

        # Starting Items UI
        self.starting_items_pair = ListPair(
            self.ui.starting_items,
            self.ui.randomized_items,
            "starting-items",
            self.ui.start_with_item,
            self.ui.randomize_item,
        )
        self.starting_items_pair.listPairChanged.connect(self.update_settings)

        self.ui.starting_items_free_search.textChanged.connect(
            self.starting_items_pair.update_option_list_filter
        )
        self.ui.randomized_items_free_search.textChanged.connect(
            self.starting_items_pair.update_non_option_list_filter
        )

        # setup presets
        self.default_presets = {}
        self.user_presets = {}
        self.ui.presets_list.addItem(NEW_PRESET)
        sep_idx = 1
        with (DEFAULT_PRESETS_PATH).open("r") as f:
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

        # cosmetics stuff - move to func and connect to dropdown
        self.color_box = getattr(self.ui, "vlay_texture_colors")
        self.color_buttons = []

        if not CUSTOM_MODELS_PATH.is_dir():
            CUSTOM_MODELS_PATH.mkdir()

        self.ui.option_model_pack_select.currentIndexChanged.connect(
            self.change_model_pack
        )

        self.ui.option_model_type_select.currentIndexChanged.connect(
            self.change_model_type
        )

        self.ui.button_reset_all_colors.clicked.connect(self.reset_all_colors)

        self.ui.button_randomize_all_colors.clicked.connect(self.randomize_all_colors)

        self.ui.option_model_type_select.addItem("Player")
        self.ui.option_model_type_select.addItem("Loftwing")

        # hide currently unsupported options to make this version viable for public use
        getattr(self.ui, "label_for_option_got_starting_state").setVisible(False)
        getattr(self.ui, "option_got_starting_state").setVisible(False)
        getattr(self.ui, "label_for_option_got_dungeon_requirement").setVisible(False)
        getattr(self.ui, "option_got_dungeon_requirement").setVisible(False)

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
        self.ui.copy_permalink_button.clicked.connect(self.copy_permalink_to_clipboard)
        self.update_ui_for_settings()
        self.update_font()
        self.update_settings()
        self.set_option_description(None)

        self.ui.tabWidget.setCurrentIndex(0)

        arc_replacements_path = Path(RANDO_ROOT_PATH / "arc-replacements")
        if not arc_replacements_path.exists():
            arc_replacements_path.mkdir(exist_ok=True, parents=True)

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

    def ui_progress_callback(
        self, current_action: str, completed_steps: int, total_steps: int = None
    ):
        self.progress_dialog.setValue(completed_steps)
        self.progress_dialog.set_current_action(current_action)
        if not total_steps is None:
            self.progress_dialog.setMaximum(total_steps)

    def on_error(self, message: str):
        self.error_msg = QErrorMessage(self)
        self.progress_dialog.reset()
        if self.rando.seed:
            self.error_msg.showMessage(
                f"{message}<br/>Seed: {self.rando.seed}<br/>Settings: {self.rando.options.get_permalink()}"
            )
        else:
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
                    if option["name"] == "Font Family":
                        widget.setCurrentIndex(
                            widget.findText(current_settings[option_key])
                        )
                    elif option["name"] == "Selected Model Pack":
                        widget.setCurrentIndex(
                            widget.findText(current_settings[option_key])
                        )
                    else:
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
        # Update tricks.
        if (
            tricks_cmd := LOGIC_MODE_TO_TRICKS_SETTING[self.options["logic-mode"]]
        ) is not None:
            self.enabled_tricks = current_settings[tricks_cmd]

        # Update locations.
        self.exclude_locations_pair.update(current_settings["excluded-locations"])

        # Update starting items.
        self.starting_items_pair.update(current_settings["starting-items"])

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
            self.options.set_option("enabled-tricks-bitless", self.enabled_tricks)
            self.options.set_option("enabled-tricks-glitched", [])
        elif "Glitched" in logic_mode:
            self.options.set_option("enabled-tricks-bitless", [])
            self.options.set_option("enabled-tricks-glitched", self.enabled_tricks)
        else:  # this should only be no logic
            self.options.set_option("enabled-tricks-bitless", [])
            self.options.set_option("enabled-tricks-glitched", [])

        self.options.set_option(
            "excluded-locations", self.exclude_locations_pair.get_added()
        )

        self.options.set_option("starting-items", self.starting_items_pair.get_added())

        self.save_settings()
        self.ui.permalink.setText(self.options.get_permalink())

    def logic_mode_changed(self):
        value = getattr(self.ui, "option_logic_mode").currentText()
        if (tricks_cmd := LOGIC_MODE_TO_TRICKS_SETTING[value]) is not None:
            self.enabled_tricks = self.options[tricks_cmd]
            self.enable_trick_interface()
        else:  # Glitchless and No Logic
            self.disable_trick_interface()
            self.enabled_tricks = []

    def toggle_sharp_corners(self, state: int):
        self.options.set_option("use-sharp-corners", bool(state))
        self.update_theme()

    def toggle_custom_theme(self, state: int):
        self.options.set_option("use-custom-theme", bool(state))

        if state:
            self.enable_theme_interface()
        else:
            self.disable_theme_interface()

        self.update_theme()

    def update_theme(self):
        if self.options["use-custom-theme"]:
            with open(self.custom_theme_path) as f:
                theme = json.load(f)
        else:
            with open(self.default_theme_path) as f:
                theme = json.load(f)

        if self.options["use-sharp-corners"]:
            corners = "sharp"
        else:
            corners = "rounded"

        qdarktheme.setup_theme(
            self.options["gui-theme"].lower(), custom_colors=theme, corner_shape=corners
        )

    def update_theme_preset(self, preset: str):
        if preset == "Default":
            self.default_theme_path = DEFAULT_THEME_PATH
        elif preset == "High Contrast":
            self.default_theme_path = HIGH_CONTRAST_THEME_PATH
        elif preset == "Readability":
            self.default_theme_path = READABILITY_THEME_PATH
            font_index = self.ui.option_font_family.findText("OpenDyslexic3")
            self.ui.option_font_family.setCurrentIndex(font_index)
            self.ui.option_font_size.setValue(OPTIONS["font-size"]["default"])

        self.update_theme()

    def open_custom_theme_picker(self):
        custom_theme_picker = CustomThemeDialog(
            self.default_theme_path, self.custom_theme_path, self.styleSheet()
        )
        custom_theme_picker.themeSaved.connect(self.update_custom_theme)
        custom_theme_picker.exec()

    def update_custom_theme(self, theme: dict):
        with open(self.custom_theme_path, "w") as f:
            json.dump(theme, f)

        self.update_theme()

    def enable_theme_interface(self):
        getattr(self.ui, "custom_theme_button").setEnabled(True)

    def disable_theme_interface(self):
        getattr(self.ui, "custom_theme_button").setEnabled(False)

    def update_font(self):
        self.update_settings()
        self.setStyleSheet(
            BASE_STYLE_SHEET_OVERRIDES
            + f"QWidget {{ font-family: { self.options['font-family'] }; font-size: { self.options['font-size'] }pt }}"
        )

    def reset_font(self):
        font_index = self.ui.option_font_family.findText(
            OPTIONS["font-family"]["default"]
        )
        self.ui.option_font_family.setCurrentIndex(font_index)
        self.ui.option_font_size.setValue(OPTIONS["font-size"]["default"])

    def enable_trick_interface(self):
        getattr(self.ui, "edit_tricks").setEnabled(True)

    def disable_trick_interface(self):
        getattr(self.ui, "edit_tricks").setEnabled(False)

    def get_option_value(self, option_name: str) -> bool | str | int | list:
        widget = getattr(self.ui, option_name)
        if isinstance(widget, QCheckBox) or isinstance(widget, QRadioButton):
            return widget.isChecked()
        elif isinstance(widget, QComboBox):
            return widget.itemText(widget.currentIndex())
        elif isinstance(widget, QSpinBox):
            return widget.value()
        elif isinstance(widget, QListView):
            items = []
            model = widget.model()
            for int_index in range(0, model.rowCount()):
                index = model.index(int_index, 0)
                items.append(index.data())
            return items
        else:
            print("Option widget is invalid: %s" % option_name)

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

    def launch_tricks_dialog(self):
        dialog = TricksDialog(
            self.enabled_tricks,
            LOGIC_MODE_TO_TRICKS_SETTING[self.options["logic-mode"]],
            self.styleSheet(),
        )
        if dialog.exec():
            self.enabled_tricks = dialog.getTrickValues()
            self.update_settings()

    # Custom model customisation funcs

    def change_model_type(self, index: int):
        self.current_model_type = self.ui.option_model_type_select.currentText()
        arcPath: str
        currentPack: str

        match self.current_model_type:
            case "Player":
                arcPath = "Player/Alink.arc"
                currentPack = self.options["selected-player-model-pack"]
            case "Loftwing":
                arcPath = "Loftwing/Bird_Link.arc"
                currentPack = self.options["selected-loftwing-model-pack"]

        self.ui.option_model_pack_select.blockSignals(True)
        self.ui.option_model_pack_select.clear()
        self.ui.option_model_pack_select.addItem("Default")
        for path in CUSTOM_MODELS_PATH.glob(f"*/{arcPath}"):
            packName = path.parts[-3]
            if (
                packName == "Default"
            ):  # ignore packs called default so they don't clash with default link
                continue
            self.ui.option_model_pack_select.addItem(packName)
            if packName == currentPack:
                self.ui.option_model_pack_select.setCurrentText(packName)
        self.ui.option_model_pack_select.blockSignals(False)
        self.change_model_pack()

    def change_model_pack(self, index: int = 0):
        if self.ui.option_model_pack_select.count() < 1:
            return
        self.current_model_pack = self.ui.option_model_pack_select.currentText()

        self.read_metadata()

        match self.current_model_type:
            case "Player":
                self.options.set_option(
                    "selected-player-model-pack", self.current_model_pack
                )
                if allowTunicSwap := self.metadata.get("AllowTunicSwap"):
                    if allowTunicSwap == "True":
                        self.ui.option_tunic_swap.setEnabled(True)
                    else:
                        self.ui.option_tunic_swap.setChecked(False)
                        self.ui.option_tunic_swap.setEnabled(False)
                        self.options.set_option("tunic-swap", False)
                else:
                    self.ui.option_tunic_swap.setEnabled(True)

                self.save_settings()
            case "Loftwing":
                self.options.set_option(
                    "selected-loftwing-model-pack", self.current_model_pack
                )
                self.save_settings()

        self.update_model_customisation()

    def read_metadata(self):
        if self.current_model_pack == "Default":
            self.metadata_path = (
                LINK_MODEL_DATA_PATH / self.current_model_type / "metadata.json"
            )
            if not os.path.isfile(self.metadata_path):
                self.metadata_path.write_bytes(
                    (
                        LINK_MODEL_DATA_PATH
                        / self.current_model_type
                        / "defaultMetadata.json"
                    ).read_bytes()
                )
        else:
            self.metadata_path = (
                CUSTOM_MODELS_PATH
                / self.current_model_pack
                / self.current_model_type
                / "metadata.json"
            )

        if os.path.isfile(self.metadata_path):
            with open(self.metadata_path) as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def model_color_changed(self, color: str, name: str):
        self.metadata["Colors"][name] = color

        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f)

        self.update_model_preview()

    def update_model_customisation(self):
        counter = 0

        while self.color_box.count() > 2:
            layout = self.color_box.takeAt(0).layout()
            while layout.count() > 0:
                widget = layout.takeAt(0).widget()
                widget.deleteLater()
            layout.deleteLater()

        self.color_buttons.clear()

        if authorName := self.metadata.get("ModelAuthorName"):
            authorNameLabel = QLabel(f"Model Author: {authorName}")
            authorNameLayout = QHBoxLayout()
            authorNameLayout.insertWidget(0, authorNameLabel)
            self.color_box.insertLayout(counter, authorNameLayout)
            counter += 1

        if authorComment := self.metadata.get("ModelAuthorComment"):
            authorCommentLabel = QLabel(f"Model Author Comment: {authorComment}")
            authorCommentLayout = QHBoxLayout()
            authorCommentLayout.insertWidget(0, authorCommentLabel)
            self.color_box.insertLayout(counter, authorCommentLayout)
            counter += 1

        if colorData := self.metadata.get("Colors"):
            for mask_name in colorData:
                color_label = QLabel(mask_name)

                random_color_button = QPushButton("Random")
                color_button = ColorButton(mask_name)
                color_button.set_color(colorData[mask_name])
                color_button.showAlpha = False
                reset_color_button = QPushButton("Reset Color")

                self.color_buttons.append(color_button)

                random_color_button.clicked.connect(color_button.randomize_color)
                color_button.colorChanged.connect(self.model_color_changed)
                reset_color_button.clicked.connect(color_button.reset_color)

                color_button_layout = QHBoxLayout()
                color_button_layout.insertWidget(0, color_label)
                color_button_layout.insertWidget(1, random_color_button)
                color_button_layout.insertWidget(2, color_button)
                color_button_layout.insertWidget(3, reset_color_button)

                self.color_box.insertLayout(counter, color_button_layout)
                counter += 1

        self.update_model_preview()

    def reset_all_colors(self):
        for button in self.color_buttons:
            button.blockSignals(True)
            button.reset_color()
            button.blockSignals(False)

        for colorGroup in self.metadata["Colors"]:
            self.metadata["Colors"][colorGroup] = "Default"

        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f)

        self.update_model_preview()

    def randomize_all_colors(self):
        self.ui.button_randomize_all_colors.setEnabled(False)
        self.ui.button_randomize_all_colors.repaint()
        colors = []

        for button in self.color_buttons:
            button.blockSignals(True)
            colors.append(button.randomize_color())
            button.blockSignals(False)

        for i, colorGroup in enumerate(self.metadata["Colors"]):
            self.metadata["Colors"][colorGroup] = colors[i]

        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata, f)

        self.update_model_preview()
        self.ui.button_randomize_all_colors.setEnabled(True)

    def update_model_preview(self):
        if self.current_model_pack == "Default":
            previewDataPath = LINK_MODEL_DATA_PATH / self.current_model_type / "Preview"
        else:
            previewDataPath = (
                CUSTOM_MODELS_PATH
                / self.current_model_pack
                / self.current_model_type
                / "Preview"
            )

        if not os.path.isfile(previewDataPath / "Preview.png"):
            print("No preview supplied")
            self.ui.label_preview_image.clear()
            self.ui.label_preview_image.setText("No preview provided")
            return

        data = cv2.imread(str(previewDataPath / "Preview.png"), cv2.IMREAD_UNCHANGED)
        data = cv2.cvtColor(data, cv2.COLOR_RGBA2BGRA)
        height = data.shape[0]
        width = data.shape[1]

        colorData = self.metadata.get("Colors")

        maskPaths = []
        colors = []
        for colorGroup in colorData:
            if colorData[colorGroup] == "Default":
                continue
            maskPath = previewDataPath / f"Preview__{colorGroup}.png"
            if os.path.isfile(maskPath):
                maskPaths.append(str(maskPath))
                colors.append(colorData[colorGroup])
            else:
                print(f"No preview mask found at {maskPath}")

        modifiedData = cr.process_texture(
            texture=data, maskPaths=maskPaths, colors=colors
        )

        qimage = QImage(
            modifiedData.tobytes(), width, height, QImage.Format.Format_RGBA8888
        )
        qpixmap = QPixmap.fromImage(qimage).scaled(
            500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.ui.label_preview_image.setPixmap(qpixmap)

    def eventFilter(self, target: QObject, event: QEvent) -> bool:
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

    def set_option_description(self, new_description: str | None):
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
            self.save_settings()
        except ValueError as e:
            # Ignore errors from faultly permalinks, with updating ui it gets reset anyways
            print(e)
        except IndexError as e:
            print(e)
        self.update_ui_for_settings()

    def copy_permalink_to_clipboard(self):
        pyclip.copy(self.ui.permalink.text())

    def gen_new_seed(self):
        self.ui.seed.setText(str(random.randrange(0, 1_000_000)))


def run_main_gui(areas: Areas, options: Options):
    app = QApplication([])

    widget = RandoGUI(areas, options)

    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main_gui()
