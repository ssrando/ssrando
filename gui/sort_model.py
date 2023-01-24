from typing import Union
from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, QPersistentModelIndex, Qt
from yaml_files import checks

check_order = list(checks.keys())

class LocationsModel(QSortFilterProxyModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.free_text_filter = ""
        self.setSortCaseSensitivity(Qt.CaseInsensitive)

    def lessThan(self, right, left):
        leftCheck = self.sourceModel().data(left)
        rightCheck = self.sourceModel().data(right)
        return check_order.index(leftCheck) > check_order.index(rightCheck)

    def filterAcceptsRow(self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        index = self.sourceModel().index(source_row, 0, source_parent)
        return self.free_text_filter.lower() in self.sourceModel().data(index).lower()

    def filterRows(self, free_text_filter):
        self.free_text_filter = free_text_filter
        self.invalidateFilter()
