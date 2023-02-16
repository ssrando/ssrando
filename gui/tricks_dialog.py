from PySide6.QtCore import Qt, QTimer, QEvent, QStringListModel
from PySide6.QtWidgets import QDialog
from gui.ui_tricks_dialog import Ui_TricksDialog

from options import OPTIONS


class TricksDialog(QDialog):
    def __init__(self, enabled_model, disabled_model, style_sheet: str = None):
        super().__init__()
        self.ui = Ui_TricksDialog()
        self.ui.setupUi(self)

        self.setStyleSheet(style_sheet)

        self.enabled_tricks_model = enabled_model
        self.disabled_tricks_model = disabled_model
        self.ui.enabled_tricks.setModel(self.enabled_tricks_model)
        self.ui.disabled_tricks.setModel(self.disabled_tricks_model)
        self.ui.enable_trick.clicked.connect(self.enable_trick)
        self.ui.disable_trick.clicked.connect(self.disable_trick)

        self.ui.bbox_tricks.accepted.connect(self.accept)
        self.ui.bbox_tricks.rejected.connect(self.reject)

    @staticmethod
    def append_row(model, value):
        model.insertRow(model.rowCount())
        new_row = model.index(model.rowCount() - 1, 0)
        model.setData(new_row, value)

    def move_selected_rows(self, source, dest):
        selection = source.selectionModel().selectedIndexes()
        last_selection = source.currentIndex()
        # Remove starting from the last so the previous indices remain valid
        selection.sort(reverse=True, key=lambda x: x.row())
        for item in selection:
            value = item.data()
            source.model().removeRow(item.row())
            self.append_row(dest.model(), value)
        # source.selectionModel().setCurrentIndex(last_selection)

    def enable_trick(self):
        self.move_selected_rows(self.ui.disabled_tricks, self.ui.enabled_tricks)
        self.ui.enabled_tricks.model().sort(0)

    def disable_trick(self):
        self.move_selected_rows(self.ui.enabled_tricks, self.ui.disabled_tricks)
        self.ui.disabled_tricks.model().sort(0)

    def getTrickValues(self):
        return (
            self.disabled_tricks_model.stringList(),
            self.enabled_tricks_model.stringList(),
        )
