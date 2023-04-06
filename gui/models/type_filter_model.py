from typing import Union
from PySide6.QtCore import QModelIndex, QPersistentModelIndex
from gui.models.sort_model import SearchableListModel

TYPE = "type"


class TypeFilterModel(SearchableListModel):
    def __init__(self, parent, full_list, type_meta):
        super().__init__(parent, full_list)
        self.type_meta = type_meta
        self.type_filter = ""

    def filterAcceptsRow(
        self, source_row: int, source_parent: Union[QModelIndex, QPersistentModelIndex]
    ) -> bool:
        if self.type_filter:
            index = self.sourceModel().index(source_row, 0, source_parent)
            data = self.sourceModel().data(index)

            if (
                self.type_meta[data][TYPE] is None
                or self.type_filter not in self.type_meta[data][TYPE]
            ):
                return False
        return super().filterAcceptsRow(source_row, source_parent)

    def filterType(self, type_filter):
        self.type_filter = type_filter
        self.invalidateFilter()
