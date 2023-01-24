from typing import Union
from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, QPersistentModelIndex, Qt


class LocationsModel(QSortFilterProxyModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.free_text_filter = ""
        self.setSortCaseSensitivity(Qt.CaseInsensitive)

    def lessThan(self, right, left):
        return False

    def filterAcceptsRow(self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]) -> bool:
        index = self.sourceModel().index(source_row, 0, source_parent)
        return self.free_text_filter.lower() in self.sourceModel().data(index).lower()

    def filterRows(self, free_text_filter):
        self.free_text_filter = free_text_filter
        self.invalidateFilter()
