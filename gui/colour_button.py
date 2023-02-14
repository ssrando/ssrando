from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QColorDialog

from enum import Enum, auto


class ColourFormat(Enum):
    RGB = auto()
    RGBA = auto()
    ARGB = auto()


class ColourButton(QPushButton):
    colourChanged = Signal(str, str)

    def __init__(self, colour: str, name: str, showAlpha: bool = True):
        super().__init__()
        self.colour = self.colour_int_from_str(colour)
        self.name = name
        self.showAlpha = showAlpha

        self.setMinimumHeight(32)
        self.update()

        self.clicked.connect(self.change_colour)

    def change_colour(self):
        new_colour = QColorDialog.getColor(
            self.colour_str_from_int(self.colour, ColourFormat.ARGB),
            options=QColorDialog.ShowAlphaChannel & self.showAlpha
        )
        self.colour = self.colour_int_from_str(
            self.colour_str_from_qcolor(new_colour)
        )
        self.update()
        self.colourChanged.emit(self.colour_str_from_int(self.colour), self.name)

    def update(self):
        rgba = self.colour_str_from_int(self.colour)
        self.setText(rgba)
        self.setStyleSheet("QPushButton {background-color: " + rgba[:-2] + " ;}")
    
    def colour_str_from_qcolor(self, colour: QColor, format: ColourFormat = ColourFormat.RGBA) -> str:
        match format:
            case ColourFormat.RGB:
                return colour.name(QColor.HexRgb)
            case ColourFormat.RGBA:
                argb = colour.name(QColor.HexArgb)
                return argb[0] + argb[3:] + argb[1:3]
            case ColourFormat.ARGB:
                return colour.name(QColor.HexArgb)
    
    def colour_str_from_int(self, colour_int: int, format: ColourFormat = ColourFormat.RGBA) -> str:
        colour = QColor( # r, g, b, a
            colour_int >> 24,
            colour_int >> 16 & 0xFF,
            colour_int >> 8 & 0xFF,
            colour_int & 0xFF,
        )

        return self.colour_str_from_qcolor(colour, format)
    
    def colour_int_from_str(self, colour: str) -> int:
        return int(colour[1:], 16)
