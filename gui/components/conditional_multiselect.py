from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QComboBox, QLabel
from PySide6.QtGui import QStandardItem

from gui.components.multi_combo_box import MultiComboBox

BASE_OPTIONS = [
    'Off',
    'Random Selection',
    'Choose',
    'All'
]

CHOOSE_TEXT = 'Choose'

class ConditionalMultiselect(QWidget):
    compositeChanged = Signal()

    def __init__(self, label, options):
        super().__init__()
        layout = QVBoxLayout()

        label_widget = QLabel(label + " Mode")
        layout.addWidget(label_widget)

        self.base_selector = QComboBox()
        for option in BASE_OPTIONS:
            self.base_selector.addItem(option)
        self.base_selector.currentIndexChanged.connect(self.update_from_base)
        self.base_selector.currentIndexChanged.connect(self.changed)
        layout.addWidget(self.base_selector)

        choice_label_widget = QLabel(label)
        layout.addWidget(choice_label_widget)

        self.multiselect = MultiComboBox()
        self.multiselect.closedPopup.connect(self.changed)
        for option in options:
            item = QStandardItem(option)
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.multiselect.model().appendRow(item)
        layout.addWidget(self.multiselect)
        
        self.setLayout(layout)

        self.update_from_base()
    
    def update_from_base(self):
        if self.base_selector.currentText() == CHOOSE_TEXT:
            self.multiselect.setEnabled(True)
        else:
            self.multiselect.setEnabled(False)

    def changed(self):
        self.compositeChanged.emit()

    def update_from_settings(self, option_value):
        self.base_selector.setCurrentText(option_value[0])
        self.multiselect.set_from_list(option_value[1:])