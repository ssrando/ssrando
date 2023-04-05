from PySide6.QtCore import QObject, QStringListModel, Signal
from PySide6.QtWidgets import QListView, QPushButton

from gui.models.sort_model import SearchableListModel
from gui.models.type_filter_model import TypeFilterModel

from options import OPTIONS


class ListPair(QObject):
    listPairChanged = Signal(bool)

    def __init__(
        self,
        option_list: QListView,
        non_option_list: QListView,
        option_string: str,
        add_button: QPushButton,
        remove_button: QPushButton,
        type_meta: dict = {},
    ):
        super().__init__()
        self.option_list = option_list
        self.non_option_list = non_option_list
        self.option_string = str(option_string)
        self._stored_filter_option_list = ""
        self._stored_filter_non_option_list = ""

        self.option_list_model = QStringListModel()
        if type_meta:
            self.option_list_proxy = TypeFilterModel(
                self.option_list, OPTIONS[self.option_string]["choices"], type_meta
            )
        else:
            self.option_list_proxy = SearchableListModel(
                self.option_list, OPTIONS[self.option_string]["choices"]
            )
        self.option_list_proxy.setSourceModel(self.option_list_model)
        self.option_list_model.setStringList(OPTIONS[self.option_string]["default"])
        self.option_list.setModel(self.option_list_proxy)

        self.non_option_list_model = QStringListModel()
        if type_meta:
            self.non_option_list_proxy = TypeFilterModel(
                self.non_option_list, OPTIONS[self.option_string]["choices"], type_meta
            )
        else:
            self.non_option_list_proxy = SearchableListModel(
                self.non_option_list, OPTIONS[self.option_string]["choices"]
            )
        self.non_option_list_proxy.setSourceModel(self.non_option_list_model)
        self.non_option_list_model.setStringList(OPTIONS[self.option_string]["choices"])
        self.non_option_list.setModel(self.non_option_list_proxy)

        add_button.clicked.connect(self.add)
        remove_button.clicked.connect(self.remove)

    def update_option_list_filter(self, new_text: str | None):
        self.option_list_proxy.filterRows(new_text)

    def update_option_list_type_filter(self, type_filter):
        self.option_list_proxy.filterType(type_filter)

    def update_non_option_list_filter(self, new_text: str | None):
        self.non_option_list_proxy.filterRows(new_text)

    def update_non_option_list_type_filter(self, type_filter):
        self.non_option_list_proxy.filterType(type_filter)

    def add(self):
        self.move_selected_rows(self.non_option_list, self.option_list)
        self.listPairChanged.emit(self.option_list_model.stringList())

    def remove(self):
        self.move_selected_rows(self.option_list, self.non_option_list)
        self.listPairChanged.emit(self.option_list_model.stringList())

    @staticmethod
    def append_row(model, value):
        model.insertRow(model.rowCount())
        new_row = model.index(model.rowCount() - 1, 0)
        model.setData(new_row, value)
        model.sort(0)

    def move_selected_rows(self, source: QListView, dest: QListView):
        self._store_and_remove_filters()

        selection = source.selectionModel().selectedIndexes()
        # Remove starting from the last so the previous indices remain valid
        selection.sort(reverse=True, key=lambda x: x.row())
        for item in selection:
            value = item.data()
            source.model().removeRow(item.row())
            self.append_row(dest.model(), value)

        self._restore_filters()

    def update(self, current_setting):
        self._store_and_remove_filters()

        not_chosen = OPTIONS[self.option_string]["choices"].copy()
        for choice in current_setting:
            not_chosen.remove(choice)

        self.option_list_model.setStringList(current_setting)
        self.non_option_list_model.setStringList(not_chosen)
        self.option_list.setModel(self.option_list_proxy)
        self.non_option_list.setModel(self.non_option_list_proxy)

        self._restore_filters()

    def get_added(self) -> list:
        return self.option_list_model.stringList()

    def _store_and_remove_filters(self):
        self._stored_filter_option_list = self.option_list_proxy.free_text_filter
        self._stored_filter_non_option_list = (
            self.non_option_list_proxy.free_text_filter
        )
        self.option_list_proxy.filterRows("")
        self.non_option_list_proxy.filterRows("")

    def _restore_filters(self):
        self.option_list_proxy.filterRows(self._stored_filter_option_list)
        self.non_option_list_proxy.filterRows(self._stored_filter_non_option_list)
