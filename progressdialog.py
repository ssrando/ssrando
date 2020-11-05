from PySide2.QtCore import Qt
from PySide2.QtWidgets import QProgressDialog


class ProgressDialog(QProgressDialog):
    def __init__(self, title, description, max_value):
        QProgressDialog.__init__(self)
        self.setWindowTitle(title)
        self.setLabelText(description)
        self.setMaximum(max_value)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setFixedSize(self.size())
        self.setAutoReset(False)
        self.setCancelButton(None)
        self.show()
