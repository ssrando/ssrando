from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLayout,
)
from gui.ui_custom_theme_dialog import Ui_CustomThemeDialog
from gui.colour_button import ColourButton

import json
from paths import RANDO_ROOT_PATH
from yaml_files import yaml_load

LIGHT = "[light]"
DARK = "[dark]"


class CustomThemeDialog(QDialog):
    themeSaved = Signal(dict)

    def __init__(self):
        super().__init__()
        self.ui = Ui_CustomThemeDialog()
        self.ui.setupUi(self)

        self.theme_info_path = RANDO_ROOT_PATH / "gui/default_theme_info.yaml"
        self.theme_info = yaml_load(self.theme_info_path)

        self.default_theme_path = RANDO_ROOT_PATH / "gui/default_theme.json"
        self.custom_theme_path = RANDO_ROOT_PATH / "custom_theme.json"

        with open(self.default_theme_path) as f:
            self.default_theme = json.load(f)
        with open(self.custom_theme_path) as f:
            self.custom_theme = json.load(f)
        
        self.ui.widget_category_choice.currentTextChanged.connect(self.on_category_change)

        for category in self.theme_info:
            self.ui.widget_category_choice.addItem(category)
        
        self.category_widget_colours = {}
        
        self.ui.custom_theme_tabWidget.setCurrentIndex(0)

        self.ui.restore_defaults_button.clicked.connect(self.restore_default_theme)
        self.ui.bbox_theme.accepted.connect(self.save_custom_theme)
        # self.ui.bbox_theme.rejected.connect(self.cancel)
    
    def on_category_change(self, category: str):
        name_box = getattr(self.ui, "vlay_widget_name")
        colour_light_box = getattr(self.ui, "vlay_color_light")
        colour_dark_box = getattr(self.ui, "vlay_color_dark")

        self.remove_widgets(name_box)
        self.remove_widgets(colour_light_box)
        self.remove_widgets(colour_dark_box)

        self.category_widget_colours = {}

        widgets = self.theme_info[category]

        for name_index, widget_name in enumerate(widgets):
            insert_index = name_index + 1

            colour_light_button = ColourButton(self.custom_theme[LIGHT][widget_name["name"]], widget_name["name"])
            colour_dark_button = ColourButton(self.custom_theme[DARK][widget_name["name"]], widget_name["name"])
            widget_name_label = QLabel(widget_name["name"])
            widget_name_label.setMinimumHeight(32)

            self.category_widget_colours[widget_name["name"]] = (colour_light_button, colour_dark_button)
            colour_light_button.colourChanged.connect(self.update_light_theme)
            colour_dark_button.colourChanged.connect(self.update_dark_theme)

            name_box.insertWidget(insert_index, widget_name_label)
            colour_light_box.insertWidget(insert_index, colour_light_button)
            colour_dark_box.insertWidget(insert_index, colour_dark_button)
    
    def update_light_theme(self, colour: str, name: str):
        self.custom_theme[LIGHT][name] = colour
    
    def update_dark_theme(self, colour: str, name: str):
        self.custom_theme[DARK][name] = colour
    
    def restore_default_theme(self):
        self.custom_theme = self.default_theme
        
        self.on_category_change(self.ui.widget_category_choice.currentText())
    
    def remove_widgets(self, layout: QLayout):
        while layout.count() > 2:
            widget = layout.takeAt(1).widget()
            widget.deleteLater()
    
    def save_custom_theme(self):
        self.themeSaved.emit(self.custom_theme)
            