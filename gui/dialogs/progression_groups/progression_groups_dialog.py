from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from gui.components.list_pair import ListPair
from gui.dialogs.progression_groups.ui_progression_groups_dialog import (
    Ui_ProgressionGroupsDialog,
)


class ProgressionGroupsDialog(QDialog):
    groupsChanged = Signal(bool)

    def __init__(
        self,
        randomized_groups: str,
        # disabled_groups: str,
        randomized_groups_command: str,
        # disabled_groups_command: str,
        style_sheet: str = None,
    ):
        super().__init__()
        self.ui = Ui_ProgressionGroupsDialog()
        self.ui.setupUi(self)

        self.setStyleSheet(style_sheet)

        # DISABLING LOCATIONS NOT YET INTEGRATED -------------------------
        self.ui.disable_location.setEnabled(False)  # Keep these disabled
        self.ui.randomize_location1.setEnabled(False)
        self.ui.disabled_locations.setEnabled(False)
        self.ui.label_disabled_locations.setEnabled(False)
        self.ui.disabled_locations_free_search.setEnabled(False)
        # ----------------------------------------------------------------

        self.randomized_groups_command = randomized_groups_command
        # self.disabled_groups_command = disabled_groups_command

        self.randomized_locations_pair = ListPair(
            self.ui.randomized_locations,
            self.ui.enabled_locations,
            self.randomized_groups_command,
            self.ui.randomize_location2,
            self.ui.enable_location,
        )
        # self.disabled_locations_pair = ListPair(
        #    self.ui.disabled_locations,
        #    self.ui.randomized_locations,
        #    self.disabled_groups_command,
        #    self.ui.disable_location,
        #    self.ui.randomize_location1,
        # )

        self.randomized_locations_pair.update(randomized_groups)
        # self.disabled_locations_pair.update(disabled_groups)

        self.ui.enabled_locations_free_search.textChanged.connect(
            self.randomized_locations_pair.update_non_option_list_filter
        )
        self.ui.randomized_locations_free_search.textChanged.connect(
            self.randomized_locations_pair.update_option_list_filter
        )
        # self.ui.disabled_locations_free_search.textChanged.connect(
        #    self.disabled_locations_pair.update_option_list_filter
        # )

        self.ui.bbox_progression_locations.accepted.connect(self.accept)
        # self.ui.bbox_progression_locations.rejected.connect(self.reject)

    def getRandomgroupsValues(self) -> list[str]:
        return self.randomized_locations_pair.get_added()

    # def getDisabledgroupsValues(self) -> list[str]:
    #    return self.disabled_locations_pair.get_added()
