from PySide6.QtCore import Qt
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
    def __init__(self, label, options):
        super().__init__()
        layout = QVBoxLayout()

        labelWidget = QLabel(label)
        layout.addWidget(labelWidget)

        self.base_selector = QComboBox()
        for option in BASE_OPTIONS:
            self.base_selector.addItem(option)
        self.base_selector.currentIndexChanged.connect(self.update_from_base)
        layout.addWidget(self.base_selector)

        self.multiselect = MultiComboBox()
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