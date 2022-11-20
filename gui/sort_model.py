from PySide6.QtCore import QSortFilterProxyModel

class LocationsModel(QSortFilterProxyModel):

    def lessThan(self, right, left):
        return False