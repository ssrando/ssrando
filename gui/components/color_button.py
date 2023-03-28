from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QColorDialog, QErrorMessage

from enum import Enum, auto

import re

NO_COLOR = "Default"
DEFAULT_COLOR = 0xFFFFFFFF
COLOR_REGEX = re.compile("#([0-9]|[A-F]|[a-f]){8}")


class ColorFormat(Enum):
    RGB = auto()
    RGBA = auto()
    ARGB = auto()


class ColorButton(QPushButton):
    colorChanged = Signal(str, str)

    def __init__(self, name: str, color: str = None, showAlpha: bool = True):
        super().__init__()

        self.color = self.color_int_from_str(color)
        self.initialColor = color
        self.name = name
        self.showAlpha = showAlpha

        self.setMinimumHeight(32)
        self.update()

        self.clicked.connect(self.change_color)

    def set_color(self, newColor: str|None):
        if newColor is None or newColor == NO_COLOR:
            self.color = None
            self.colorChanged.emit(NO_COLOR, self.name)
        else:
            if not COLOR_REGEX.match(newColor): 
                raise ValueError(
                    f"Invalid color value in model metadata, expected format '#XXXXXXXX' but got {newColor}."
                )
            self.color = self.color_int_from_str(newColor)
            self.colorChanged.emit(newColor, self.name)
        self.update()

    def change_color(self):
        new_color = QColorDialog.getColor(
            self.color_str_from_int(self.color, ColorFormat.ARGB),
            options=QColorDialog.ShowAlphaChannel & self.showAlpha,
        )
        self.color = self.color_int_from_str(self.color_str_from_qcolor(new_color))
        self.update()
        self.colorChanged.emit(self.color_str_from_int(self.color), self.name)

    def reset_color(self):
        self.set_color(self.initialColor)

    def update(self):
        r, g, b, a = self.color_parts_from_int(self.color)
        # https://en.wikipedia.org/wiki/Relative_luminance
        luminance = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
        textColor = "white"
        if luminance > 128:
            textColor = "black"

        rgba = self.color_str_from_int(self.color)
        self.setText(rgba)
        if self.color is None:
            self.setText(NO_COLOR)
        self.setStyleSheet(
            "QPushButton {background-color: "
            + rgba[:-2]
            + "; color: "
            + textColor
            + "; }"
        )

    def color_str_from_qcolor(
        self, color: QColor, format: ColorFormat = ColorFormat.RGBA
    ) -> str:
        match format:
            case ColorFormat.RGB:
                return color.name(QColor.HexRgb)
            case ColorFormat.RGBA:
                argb = color.name(QColor.HexArgb)
                return argb[0] + argb[3:] + argb[1:3]
            case ColorFormat.ARGB:
                return color.name(QColor.HexArgb)

    def color_str_from_int(
        self, color_int: int|None, format: ColorFormat = ColorFormat.RGBA
    ) -> str:
        if color_int is None:
            color_int = DEFAULT_COLOR
        color = QColor(*self.color_parts_from_int(color_int))

        return self.color_str_from_qcolor(color, format)

    def color_int_from_str(self, color: str|None) -> int:
        if color is None:
            return DEFAULT_COLOR
        return int(color[1:], 16)

    def color_parts_from_int(self, color_int: int|None) -> tuple:
        if color_int is None:
            color_int = DEFAULT_COLOR
        r = color_int >> 24
        g = color_int >> 16 & 0xFF
        b = color_int >> 8 & 0xFF
        a = color_int & 0xFF
        return (r, g, b, a)
