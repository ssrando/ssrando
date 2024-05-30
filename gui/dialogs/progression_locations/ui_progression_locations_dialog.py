# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progression_locations_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit,
    QListView, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ProgressionLocationsDialog(object):
    def setupUi(self, ProgressionLocationsDialog):
        if not ProgressionLocationsDialog.objectName():
            ProgressionLocationsDialog.setObjectName(u"ProgressionLocationsDialog")
        ProgressionLocationsDialog.resize(1123, 481)
        self.verticalLayout = QVBoxLayout(ProgressionLocationsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.vlay_progression_locations = QVBoxLayout()
        self.vlay_progression_locations.setObjectName(u"vlay_progression_locations")
        self.hlay_progression_locations_body = QHBoxLayout()
        self.hlay_progression_locations_body.setObjectName(u"hlay_progression_locations_body")
        self.vlay_disabled_locations = QVBoxLayout()
        self.vlay_disabled_locations.setObjectName(u"vlay_disabled_locations")
        self.label_disabled_locations = QLabel(ProgressionLocationsDialog)
        self.label_disabled_locations.setObjectName(u"label_disabled_locations")

        self.vlay_disabled_locations.addWidget(self.label_disabled_locations)

        self.disabled_locations_free_search = QLineEdit(ProgressionLocationsDialog)
        self.disabled_locations_free_search.setObjectName(u"disabled_locations_free_search")
        self.disabled_locations_free_search.setClearButtonEnabled(True)

        self.vlay_disabled_locations.addWidget(self.disabled_locations_free_search)

        self.disabled_locations = QListView(ProgressionLocationsDialog)
        self.disabled_locations.setObjectName(u"disabled_locations")
        self.disabled_locations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.disabled_locations.setProperty("showDropIndicator", False)
        self.disabled_locations.setSelectionMode(QAbstractItemView.MultiSelection)
        self.disabled_locations.setSelectionRectVisible(False)

        self.vlay_disabled_locations.addWidget(self.disabled_locations)


        self.hlay_progression_locations_body.addLayout(self.vlay_disabled_locations)

        self.vlay_locations_controls_disable = QVBoxLayout()
        self.vlay_locations_controls_disable.setObjectName(u"vlay_locations_controls_disable")
        self.vspace_tricks_controls_upper1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_locations_controls_disable.addItem(self.vspace_tricks_controls_upper1)

        self.disable_location = QPushButton(ProgressionLocationsDialog)
        self.disable_location.setObjectName(u"disable_location")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disable_location.sizePolicy().hasHeightForWidth())
        self.disable_location.setSizePolicy(sizePolicy)

        self.vlay_locations_controls_disable.addWidget(self.disable_location)

        self.vspace_tricks_controls_middle1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_locations_controls_disable.addItem(self.vspace_tricks_controls_middle1)

        self.randomize_location1 = QPushButton(ProgressionLocationsDialog)
        self.randomize_location1.setObjectName(u"randomize_location1")
        sizePolicy.setHeightForWidth(self.randomize_location1.sizePolicy().hasHeightForWidth())
        self.randomize_location1.setSizePolicy(sizePolicy)

        self.vlay_locations_controls_disable.addWidget(self.randomize_location1)

        self.vspace_tricks_controls_lower1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_locations_controls_disable.addItem(self.vspace_tricks_controls_lower1)


        self.hlay_progression_locations_body.addLayout(self.vlay_locations_controls_disable)

        self.vlay_randomized_locations = QVBoxLayout()
        self.vlay_randomized_locations.setObjectName(u"vlay_randomized_locations")
        self.label_randomized_locations = QLabel(ProgressionLocationsDialog)
        self.label_randomized_locations.setObjectName(u"label_randomized_locations")

        self.vlay_randomized_locations.addWidget(self.label_randomized_locations)

        self.randomized_locations_free_search = QLineEdit(ProgressionLocationsDialog)
        self.randomized_locations_free_search.setObjectName(u"randomized_locations_free_search")

        self.vlay_randomized_locations.addWidget(self.randomized_locations_free_search)

        self.randomized_locations = QListView(ProgressionLocationsDialog)
        self.randomized_locations.setObjectName(u"randomized_locations")
        self.randomized_locations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.randomized_locations.setProperty("showDropIndicator", False)
        self.randomized_locations.setSelectionMode(QAbstractItemView.MultiSelection)

        self.vlay_randomized_locations.addWidget(self.randomized_locations)


        self.hlay_progression_locations_body.addLayout(self.vlay_randomized_locations)

        self.vlay_locations_controls_enable = QVBoxLayout()
        self.vlay_locations_controls_enable.setObjectName(u"vlay_locations_controls_enable")
        self.vspace_tricks_controls_upper2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_locations_controls_enable.addItem(self.vspace_tricks_controls_upper2)

        self.randomize_location2 = QPushButton(ProgressionLocationsDialog)
        self.randomize_location2.setObjectName(u"randomize_location2")
        sizePolicy.setHeightForWidth(self.randomize_location2.sizePolicy().hasHeightForWidth())
        self.randomize_location2.setSizePolicy(sizePolicy)

        self.vlay_locations_controls_enable.addWidget(self.randomize_location2)

        self.vspace_tricks_controls_middle2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_locations_controls_enable.addItem(self.vspace_tricks_controls_middle2)

        self.enable_location = QPushButton(ProgressionLocationsDialog)
        self.enable_location.setObjectName(u"enable_location")
        sizePolicy.setHeightForWidth(self.enable_location.sizePolicy().hasHeightForWidth())
        self.enable_location.setSizePolicy(sizePolicy)

        self.vlay_locations_controls_enable.addWidget(self.enable_location)

        self.vspace_tricks_controls_lower2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_locations_controls_enable.addItem(self.vspace_tricks_controls_lower2)


        self.hlay_progression_locations_body.addLayout(self.vlay_locations_controls_enable)

        self.vlay_enabled_locations = QVBoxLayout()
        self.vlay_enabled_locations.setObjectName(u"vlay_enabled_locations")
        self.label_enabled_locations = QLabel(ProgressionLocationsDialog)
        self.label_enabled_locations.setObjectName(u"label_enabled_locations")

        self.vlay_enabled_locations.addWidget(self.label_enabled_locations)

        self.enabled_locations_free_search = QLineEdit(ProgressionLocationsDialog)
        self.enabled_locations_free_search.setObjectName(u"enabled_locations_free_search")
        self.enabled_locations_free_search.setClearButtonEnabled(True)

        self.vlay_enabled_locations.addWidget(self.enabled_locations_free_search)

        self.enabled_locations = QListView(ProgressionLocationsDialog)
        self.enabled_locations.setObjectName(u"enabled_locations")
        self.enabled_locations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.enabled_locations.setProperty("showDropIndicator", False)
        self.enabled_locations.setSelectionMode(QAbstractItemView.MultiSelection)
        self.enabled_locations.setSelectionRectVisible(False)

        self.vlay_enabled_locations.addWidget(self.enabled_locations)


        self.hlay_progression_locations_body.addLayout(self.vlay_enabled_locations)


        self.vlay_progression_locations.addLayout(self.hlay_progression_locations_body)


        self.verticalLayout.addLayout(self.vlay_progression_locations)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dialog_description = QLabel(ProgressionLocationsDialog)
        self.dialog_description.setObjectName(u"dialog_description")
        self.dialog_description.setEnabled(True)
        font = QFont()
        font.setPointSize(8)
        font.setItalic(False)
        font.setKerning(True)
        self.dialog_description.setFont(font)
        self.dialog_description.setStyleSheet(u"color: grey;")

        self.horizontalLayout.addWidget(self.dialog_description)

        self.bbox_progression_locations = QDialogButtonBox(ProgressionLocationsDialog)
        self.bbox_progression_locations.setObjectName(u"bbox_progression_locations")
        self.bbox_progression_locations.setOrientation(Qt.Horizontal)
        self.bbox_progression_locations.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout.addWidget(self.bbox_progression_locations)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ProgressionLocationsDialog)
        self.bbox_progression_locations.accepted.connect(ProgressionLocationsDialog.accept)
        self.bbox_progression_locations.rejected.connect(ProgressionLocationsDialog.reject)

        QMetaObject.connectSlotsByName(ProgressionLocationsDialog)
    # setupUi

    def retranslateUi(self, ProgressionLocationsDialog):
        ProgressionLocationsDialog.setWindowTitle(QCoreApplication.translate("ProgressionLocationsDialog", u"Edit Progression Locations", None))
        self.label_disabled_locations.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Non-Progression Locations", None))
        self.disabled_locations_free_search.setText("")
        self.disabled_locations_free_search.setPlaceholderText(QCoreApplication.translate("ProgressionLocationsDialog", u"Search", None))
        self.disable_location.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Disable\n"
"<--", None))
        self.randomize_location1.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Randomize\n"
"-->", None))
        self.label_randomized_locations.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Randomized Locations", None))
        self.randomized_locations_free_search.setText("")
        self.randomized_locations_free_search.setPlaceholderText(QCoreApplication.translate("ProgressionLocationsDialog", u"Search", None))
        self.randomize_location2.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Randomize\n"
"<--", None))
        self.enable_location.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Enable\n"
"-->", None))
        self.label_enabled_locations.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Enabled Progression Locations", None))
        self.enabled_locations_free_search.setText("")
        self.enabled_locations_free_search.setPlaceholderText(QCoreApplication.translate("ProgressionLocationsDialog", u"Search", None))
        self.dialog_description.setText(QCoreApplication.translate("ProgressionLocationsDialog", u"Enabled progression locations can have progress items. Randomized locations can be progression or non-progression, which will be randomly selected when\n"
"the seed is generated. Individual locations that are \"excluded locations\" on the main page will remain non-progression locations.", None))
    # retranslateUi

