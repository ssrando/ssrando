import os
import sys
from pathlib import Path
import random

import yaml
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QTimer, QEvent, QStringListModel
from PySide2.QtWidgets import (
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
)

from logic.constants import ALL_TYPES
from options import OPTIONS, Options
from gui.progressdialog import ProgressDialog
from gui.guithreads import RandomizerThread, ExtractSetupThread
from ssrando import Randomizer, VERSION
from gui.ui_randogui import Ui_MainWindow
from witmanager import WitManager

# Allow keyboard interrupts on the command line to instantly close the program.
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


class RandoGUI(QMainWindow):
    def __init__(self, options: Options):
        super().__init__()

        self.wit_manager = WitManager(Path(".").resolve())
        self.randothread = None
        self.error_msg = None
        self.progress_dialog = None
        self.randomize_after_iso_extract = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Skyward Sword Randomizer v" + VERSION)

        self.options = options
        self.settings_path = "settings.txt"
        # if os.path.isfile(self.settings_path):
        #     with open(self.settings_path) as f:
        #         try:
        #             self.options.update_from_permalink(f.readline())
        #         except Exception as e:
        #             print("couldn't update from saved settings!", e)

        self.option_map = {}
        for option_key, option in OPTIONS.items():
            if option["name"] != "Banned Types" and option["name"] != "Seed":
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

        self.location_descriptions = {
            "skyloft": "Enables progression items to appear on Skyloft",
            "sky": "Enables progression items to appear in The Sky",
            "thunderhead": "Enables progression items to appear in The Thunderhead",
            "faron": "Enables progression items to appear in the Faron Province",
            "eldin": "Enables progression items to appear in the Eldin Province",
            "lanayru": "Enables progression items to appear in the Lanayru Province",
            "dungeon": "Enables progression items to appear in dungeons",
            "mini_dungeon": "Enables progression items to appear inside Mini Dungeons (i.e. the nodes in "
            "Lanayru Desert)",
            "free_gift": "Enables progression items to appear as free gifts from NPCs (i.e. the shield from "
            "Professor Owlan)",
            "freestanding": "Enables progression items to appear as freestanding items in the world "
            "(does not include the freestanding gratitude crystals)",
            "miscellaneous": "Enables progression items to appear in miscellaneous locations that don't fit into "
            "any other category (i.e. overworld chests) ",
            "silent_realm": "Enables progression items to appear as rewards for completing Silent Realm trials",
            "digging": "Enables progression items to appear in digging spots in the world (does not include Mogma "
            "Mitts checks, such as the one in Volcano Summit or in Fire Sanctuary)",
            "bombable": "Enables progression items to appear behind bombable walls or other bombable structures",
            "combat": "Enables progression items to appear as rewards for combat or completing a quest involving "
            "combat (i.e. Digging Mitts fight, Kikwi rescue). Does not impact combat within dungeons",
            "song": "Enables progression items to appear in place of learning songs (from Isle of Song, Ballad of the "
            "Goddess in Sealed Temple, Song of the Hero from Levias)",
            "spiral_charge": "Enables progression items to appear in the chests in the sky requiring Spiral Charge to"
            " access",
            "minigame": "Enables progression items to appear as rewards from winning minigames",
            "crystal": "Enables progression items to appear as loose crystals (currently not randomized and must "
            "always be enabled)",
            "short": "Enables progression items to appear as rewards for completing short quests (i.e. rescuing"
            " Orielle)",
            "long": "Enables progression items to appear as rewards for completing long quests (i.e. Peatrice)",
            "fetch": "Enables progression items to appear as rewards for returning items to NPCs ",
            "crystal_quest": "Enables progression items to appear as rewards for completing Gratitude Crystal quests",
            "scrapper": "Enables progression items to appear as rewards for Scrapper Quests",
            "peatrice": "Enables a progression item to appear as the reward for completing the Peatrice side quest",
            "beedle": "Enables progression items to be sold in Beedle's shop",
            "cheap": "Enables progression items to be sold for 300 rupees or less. Applies to all shops where "
            "progression items can appear.",
            "medium": "Enables progression items to be sold for between 300 and 1000 rupees. Applies to all "
            "shops where progression items can appear",
            "expensive": "Enables progression items to be sold for more than 1000 rupees. Appleis to all shops"
            "where progression items can appear",
            "goddess": "Enables progression items to appear as items in Goddess Chests",
            "faron_goddess": "Enables progression items to appear in the Goddess Chests linked to the Goddess Cubes in "
            "Faron Woods and Deep Woods",
            "eldin_goddess": "Enables progression items to appear in the Goddess Chests linked to the Goddess Cubes in "
            "the main part of Eldin Volcano and Mogma Turf",
            "lanayru_goddess": "Enables progression items to appear in the Goddess Chests linked to the Goddess Cubes "
            "in the main part of Lanayru Desert, Temple of Time and Lanayru Mines",
            "floria_goddess": "Enables progression items to appear in the Goddess Chests linked to the Goddess Cubes "
            "in Lake Floria",
            "summit_goddess": "Enables progression items to appear in the Goddess Chests linked to the Goddess Cubes "
            "in Volcano Summit",
            "sand_sea_goddess": "Enables progression items to appear in the Goddess Chests linked to the Goddess Cubes "
            "in Sand Sea",
        }
        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            widget.setChecked(not check_type in self.options["banned-types"])
            if check_type == "crystal":
                widget.setEnabled(False)
            widget.clicked.connect(self.update_settings)
            widget.installEventFilter(self)

        # hide currently unsupported options to make this version viable for public use
        getattr(self.ui, "option_got_starting_state").setVisible(False)
        getattr(self.ui, "option_got_dungeon_requirement").setVisible(False)
        getattr(self.ui, "option_horde").setVisible(False)
        getattr(self.ui, "option_g3").setVisible(False)
        getattr(self.ui, "option_demise").setVisible(False)
        getattr(self.ui, "option_sometimes_hints").setVisible(False)
        self.enable_trick_interface()
        getattr(self.ui, "enable_location").setVisible(False)
        getattr(self.ui, "disable_location").setVisible(False)
        getattr(self.ui, "enabled_locations").setVisible(False)
        getattr(self.ui, "disabled_locations").setVisible(False)
        getattr(self.ui, "randomize_item").setVisible(False)
        getattr(self.ui, "start_with_item").setVisible(False)
        getattr(self.ui, "randomized_items").setVisible(False)
        getattr(self.ui, "starting_items").setVisible(False)

        # hide supporting elements
        getattr(self.ui, "tabWidget").removeTab(5)
        getattr(self.ui, "label").setVisible(False)
        getattr(self.ui, "label_for_option_sometimes_hints").setVisible(False)
        getattr(self.ui, "option_plando").setVisible(False)
        getattr(self.ui, "plando_file").setVisible(False)
        getattr(self.ui, "plando_file_browse").setVisible(False)
        getattr(self.ui, "option_json_spoiler").setVisible(False)

        self.ui.ouput_folder_browse_button.clicked.connect(self.browse_for_output_dir)
        self.ui.randomize_button.clicked.connect(self.randomize)
        self.ui.permalink.textChanged.connect(self.permalink_updated)
        self.ui.seed.textChanged.connect(self.update_settings)
        self.ui.progression_goddess.clicked.connect(self.goddess_cubes_toggled)
        self.ui.seed_button.clicked.connect(self.gen_new_seed)
        self.update_ui_for_settings()
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
        self.rando = Randomizer(self.options.copy())

        if dry_run:
            extra_steps = 1  # done
        else:
            extra_steps = 101  # wit create wbfs + done

        self.progress_dialog = ProgressDialog(
            "Randomizing",
            "Initializing...",
            self.rando.get_total_progress_steps() + extra_steps,
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

        def on_error(msg):
            self.progress_dialog.reset()
            self.error_msg = QMessageBox.critical(self, "Error", msg)

        self.extract_thread.error_abort.connect(on_error)
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
            if option["name"] != "Banned Types" and option["name"] != "Seed":
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

        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            widget.setChecked(not check_type in current_settings["banned-types"])
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
        self.ui.enabled_tricks.setModel(self.enabled_tricks_model)
        self.ui.disabled_tricks.setModel(self.disabled_tricks_model)
        self.ui.permalink.setText(current_settings.get_permalink())

    def save_settings(self):
        with open(self.settings_path, "w") as f:
            f.write(self.options.get_permalink())

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
            if (
                option["name"] != "Banned Types"
                and option["name"] != "Seed"
                and "Enabled Tricks" not in option["name"]
            ):
                ui_name = option.get("ui", None)
                if not ui_name:
                    continue
                self.options.set_option(option_command, self.get_option_value(ui_name))

        self.options.set_option("banned-types", self.get_banned_types())

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

    def get_banned_types(self):
        banned_types = []
        for check_type in ALL_TYPES:
            widget = getattr(self.ui, "progression_" + check_type.replace(" ", "_"))
            if not widget.isChecked():
                banned_types.append(check_type)
        return banned_types

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

    def eventFilter(self, target, event):
        if event.type() == QEvent.Enter:
            ui_name = target.objectName()

            if ui_name.startswith("progression_"):
                ui_name = ui_name[len("progression_") :]
                self.set_option_description(self.location_descriptions[ui_name])

            else:
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

    def goddess_cubes_toggled(self):
        enabled = self.ui.progression_goddess.isChecked()
        self.ui.progression_faron_goddess.setEnabled(enabled)
        self.ui.progression_eldin_goddess.setEnabled(enabled)
        self.ui.progression_lanayru_goddess.setEnabled(enabled)
        self.ui.progression_floria_goddess.setEnabled(enabled)
        self.ui.progression_summit_goddess.setEnabled(enabled)
        self.ui.progression_sand_sea_goddess.setEnabled(enabled)

    def gen_new_seed(self):
        self.ui.seed.setText(str(random.randrange(0, 1_000_000)))


def run_main_gui(options: Options):
    app = QtWidgets.QApplication([])

    widget = RandoGUI(options)
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_main_gui()
