from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from gui.components.list_pair import ListPair
from gui.dialogs.tricks.ui_tricks_dialog import Ui_TricksDialog

from options import OPTIONS


class TricksDialog(QDialog):
    tricksChanged = Signal(bool)

    def __init__(
        self, enabled_tricks: str, tricks_command: str, style_sheet: str = None
    ):
        super().__init__()
        self.ui = Ui_TricksDialog()
        self.ui.setupUi(self)

        self.setStyleSheet(style_sheet)

        self.tricks_command = tricks_command

        self.enabled_tricks_pair = ListPair(
            self.ui.enabled_tricks, self.ui.disabled_tricks, self.tricks_command
        )

        self.enabled_tricks_pair.update(enabled_tricks)

        self.enabled_tricks_pair.set_add_button(self.ui.enable_trick)
        self.enabled_tricks_pair.set_remove_button(self.ui.disable_trick)

        self.ui.enabled_tricks_free_search.textChanged.connect(
            self.enabled_tricks_pair.update_option_list_filter
        )
        self.ui.disabled_tricks_free_search.textChanged.connect(
            self.enabled_tricks_pair.update_non_option_list_filter
        )

        self.ui.bbox_tricks.accepted.connect(self.accept)
        self.ui.bbox_tricks.rejected.connect(self.reject)

    def getTrickValues(self) -> list[str]:
        return self.enabled_tricks_pair.get_added()
