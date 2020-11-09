# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randogui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(956, 441)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 931, 89))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.seed_button = QPushButton(self.gridLayoutWidget)
        self.seed_button.setObjectName(u"seed_button")

        self.gridLayout.addWidget(self.seed_button, 1, 7, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setToolTipDuration(-1)
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.ouput_folder_browse_button = QPushButton(self.gridLayoutWidget)
        self.ouput_folder_browse_button.setObjectName(u"ouput_folder_browse_button")

        self.gridLayout.addWidget(self.ouput_folder_browse_button, 0, 7, 1, 1)

        self.seed = QLineEdit(self.gridLayoutWidget)
        self.seed.setObjectName(u"seed")

        self.gridLayout.addWidget(self.seed, 1, 1, 1, 1)

        self.output_folder = QLineEdit(self.gridLayoutWidget)
        self.output_folder.setObjectName(u"output_folder")

        self.gridLayout.addWidget(self.output_folder, 0, 1, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 100, 931, 131))
        self.gridLayoutWidget_3 = QWidget(self.groupBox)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 911, 101))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.progression_goddess = QCheckBox(self.gridLayoutWidget_3)
        self.progression_goddess.setObjectName(u"progression_goddess")

        self.gridLayout_3.addWidget(self.progression_goddess, 0, 1, 1, 1)

        self.progression_crystal = QCheckBox(self.gridLayoutWidget_3)
        self.progression_crystal.setObjectName(u"progression_crystal")

        self.gridLayout_3.addWidget(self.progression_crystal, 1, 0, 1, 1)

        self.progression_dungeon = QCheckBox(self.gridLayoutWidget_3)
        self.progression_dungeon.setObjectName(u"progression_dungeon")

        self.gridLayout_3.addWidget(self.progression_dungeon, 2, 0, 1, 1)

        self.progression_batreaux = QCheckBox(self.gridLayoutWidget_3)
        self.progression_batreaux.setObjectName(u"progression_batreaux")

        self.gridLayout_3.addWidget(self.progression_batreaux, 0, 0, 1, 1)

        self.progression_quest = QCheckBox(self.gridLayoutWidget_3)
        self.progression_quest.setObjectName(u"progression_quest")

        self.gridLayout_3.addWidget(self.progression_quest, 0, 2, 1, 1)

        self.progression_minigame = QCheckBox(self.gridLayoutWidget_3)
        self.progression_minigame.setObjectName(u"progression_minigame")

        self.gridLayout_3.addWidget(self.progression_minigame, 1, 1, 1, 1)

        self.progression_overworld = QCheckBox(self.gridLayoutWidget_3)
        self.progression_overworld.setObjectName(u"progression_overworld")

        self.gridLayout_3.addWidget(self.progression_overworld, 2, 1, 1, 1)

        self.progression_silent_realm = QCheckBox(self.gridLayoutWidget_3)
        self.progression_silent_realm.setObjectName(u"progression_silent_realm")

        self.gridLayout_3.addWidget(self.progression_silent_realm, 2, 2, 1, 1)

        self.progression_sidequest = QCheckBox(self.gridLayoutWidget_3)
        self.progression_sidequest.setObjectName(u"progression_sidequest")

        self.gridLayout_3.addWidget(self.progression_sidequest, 1, 2, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 240, 931, 121))
        self.gridLayoutWidget_2 = QWidget(self.groupBox_2)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 911, 97))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.option_closed_thunderhead = QCheckBox(self.gridLayoutWidget_2)
        self.option_closed_thunderhead.setObjectName(u"option_closed_thunderhead")

        self.gridLayout_2.addWidget(self.option_closed_thunderhead, 1, 1, 1, 1)

        self.option_swordless = QCheckBox(self.gridLayoutWidget_2)
        self.option_swordless.setObjectName(u"option_swordless")

        self.gridLayout_2.addWidget(self.option_swordless, 0, 0, 1, 1)

        self.option_skip_skykeep = QCheckBox(self.gridLayoutWidget_2)
        self.option_skip_skykeep.setObjectName(u"option_skip_skykeep")

        self.gridLayout_2.addWidget(self.option_skip_skykeep, 2, 0, 1, 1)

        self.option_empty_unrequired_dungeons = QCheckBox(self.gridLayoutWidget_2)
        self.option_empty_unrequired_dungeons.setObjectName(u"option_empty_unrequired_dungeons")

        self.gridLayout_2.addWidget(self.option_empty_unrequired_dungeons, 1, 0, 1, 1)

        self.option_randomize_tablets = QCheckBox(self.gridLayoutWidget_2)
        self.option_randomize_tablets.setObjectName(u"option_randomize_tablets")

        self.gridLayout_2.addWidget(self.option_randomize_tablets, 0, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.option_required_dungeon_count = QSpinBox(self.gridLayoutWidget_2)
        self.option_required_dungeon_count.setObjectName(u"option_required_dungeon_count")
        self.option_required_dungeon_count.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.option_required_dungeon_count.sizePolicy().hasHeightForWidth())
        self.option_required_dungeon_count.setSizePolicy(sizePolicy1)
        self.option_required_dungeon_count.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_2.addWidget(self.option_required_dungeon_count)

        self.label_for_option_required_dungeon_count = QLabel(self.gridLayoutWidget_2)
        self.label_for_option_required_dungeon_count.setObjectName(u"label_for_option_required_dungeon_count")

        self.horizontalLayout_2.addWidget(self.label_for_option_required_dungeon_count)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 400, 931, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.option_dry_run = QCheckBox(self.horizontalLayoutWidget)
        self.option_dry_run.setObjectName(u"option_dry_run")

        self.horizontalLayout.addWidget(self.option_dry_run)

        self.option_invisible_sword = QCheckBox(self.horizontalLayoutWidget)
        self.option_invisible_sword.setObjectName(u"option_invisible_sword")

        self.horizontalLayout.addWidget(self.option_invisible_sword)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.randomize_button = QPushButton(self.horizontalLayoutWidget)
        self.randomize_button.setObjectName(u"randomize_button")

        self.horizontalLayout.addWidget(self.randomize_button)

        self.option_description = QLabel(self.centralwidget)
        self.option_description.setObjectName(u"option_description")
        self.option_description.setEnabled(True)
        self.option_description.setGeometry(QRect(10, 370, 931, 20))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Skyward Sword Randomizer", None))
        self.seed_button.setText(QCoreApplication.translate("MainWindow", u"New Seed", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Output Folder", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_3.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Seed", None))
        self.ouput_folder_browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Where should progress items appear?", None))
        self.progression_goddess.setText(QCoreApplication.translate("MainWindow", u"Goddess Cubes/Chests", None))
        self.progression_crystal.setText(QCoreApplication.translate("MainWindow", u"Loose Crystals", None))
        self.progression_dungeon.setText(QCoreApplication.translate("MainWindow", u"Dungeon", None))
        self.progression_batreaux.setText(QCoreApplication.translate("MainWindow", u"Batreaux", None))
        self.progression_quest.setText(QCoreApplication.translate("MainWindow", u"Main Quest", None))
        self.progression_minigame.setText(QCoreApplication.translate("MainWindow", u"Minigames", None))
        self.progression_overworld.setText(QCoreApplication.translate("MainWindow", u"Overworld", None))
        self.progression_silent_realm.setText(QCoreApplication.translate("MainWindow", u"Silent Realms", None))
        self.progression_sidequest.setText(QCoreApplication.translate("MainWindow", u"Sidequests", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Additional Options", None))
        self.option_closed_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Closed Thunderhead", None))
        self.option_swordless.setText(QCoreApplication.translate("MainWindow", u"Swordless", None))
        self.option_skip_skykeep.setText(QCoreApplication.translate("MainWindow", u"Skip Skykeep", None))
        self.option_empty_unrequired_dungeons.setText(QCoreApplication.translate("MainWindow", u"Race Mode", None))
        self.option_randomize_tablets.setText(QCoreApplication.translate("MainWindow", u"Tablet Randomizer", None))
        self.label_for_option_required_dungeon_count.setText(QCoreApplication.translate("MainWindow", u"Required Dungeon Count", None))
        self.option_dry_run.setText(QCoreApplication.translate("MainWindow", u"Dry Run", None))
        self.option_invisible_sword.setText(QCoreApplication.translate("MainWindow", u"Invisible Sword", None))
        self.randomize_button.setText(QCoreApplication.translate("MainWindow", u"Randomize", None))
        self.option_description.setText("")
    # retranslateUi

