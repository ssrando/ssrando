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
        MainWindow.resize(952, 690)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 931, 58))
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
        self.groupBox.setGeometry(QRect(10, 140, 931, 151))
        self.gridLayoutWidget_3 = QWidget(self.groupBox)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 911, 121))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.progression_short = QCheckBox(self.gridLayoutWidget_3)
        self.progression_short.setObjectName(u"progression_short")

        self.gridLayout_3.addWidget(self.progression_short, 4, 0, 1, 1)

        self.progression_miscellaneous = QCheckBox(self.gridLayoutWidget_3)
        self.progression_miscellaneous.setObjectName(u"progression_miscellaneous")

        self.gridLayout_3.addWidget(self.progression_miscellaneous, 1, 4, 1, 1)

        self.progression_free_gift = QCheckBox(self.gridLayoutWidget_3)
        self.progression_free_gift.setObjectName(u"progression_free_gift")

        self.gridLayout_3.addWidget(self.progression_free_gift, 1, 2, 1, 1)

        self.progression_song = QCheckBox(self.gridLayoutWidget_3)
        self.progression_song.setObjectName(u"progression_song")

        self.gridLayout_3.addWidget(self.progression_song, 2, 4, 1, 1)

        self.progression_mini_dungeon = QCheckBox(self.gridLayoutWidget_3)
        self.progression_mini_dungeon.setObjectName(u"progression_mini_dungeon")

        self.gridLayout_3.addWidget(self.progression_mini_dungeon, 1, 1, 1, 1)

        self.progression_silent_realm = QCheckBox(self.gridLayoutWidget_3)
        self.progression_silent_realm.setObjectName(u"progression_silent_realm")

        self.gridLayout_3.addWidget(self.progression_silent_realm, 2, 0, 1, 1)

        self.progression_freestanding = QCheckBox(self.gridLayoutWidget_3)
        self.progression_freestanding.setObjectName(u"progression_freestanding")

        self.gridLayout_3.addWidget(self.progression_freestanding, 1, 3, 1, 1)

        self.progression_long = QCheckBox(self.gridLayoutWidget_3)
        self.progression_long.setObjectName(u"progression_long")

        self.gridLayout_3.addWidget(self.progression_long, 4, 1, 1, 1)

        self.progression_dungeon = QCheckBox(self.gridLayoutWidget_3)
        self.progression_dungeon.setObjectName(u"progression_dungeon")

        self.gridLayout_3.addWidget(self.progression_dungeon, 1, 0, 1, 1)

        self.progression_minigame = QCheckBox(self.gridLayoutWidget_3)
        self.progression_minigame.setObjectName(u"progression_minigame")

        self.gridLayout_3.addWidget(self.progression_minigame, 3, 1, 1, 1)

        self.progression_digging = QCheckBox(self.gridLayoutWidget_3)
        self.progression_digging.setObjectName(u"progression_digging")

        self.gridLayout_3.addWidget(self.progression_digging, 2, 1, 1, 1)

        self.progression_bombable = QCheckBox(self.gridLayoutWidget_3)
        self.progression_bombable.setObjectName(u"progression_bombable")

        self.gridLayout_3.addWidget(self.progression_bombable, 2, 2, 1, 1)

        self.progression_combat = QCheckBox(self.gridLayoutWidget_3)
        self.progression_combat.setObjectName(u"progression_combat")

        self.gridLayout_3.addWidget(self.progression_combat, 2, 3, 1, 1)

        self.progression_spiral_charge = QCheckBox(self.gridLayoutWidget_3)
        self.progression_spiral_charge.setObjectName(u"progression_spiral_charge")

        self.gridLayout_3.addWidget(self.progression_spiral_charge, 3, 0, 1, 1)

        self.progression_batreaux = QCheckBox(self.gridLayoutWidget_3)
        self.progression_batreaux.setObjectName(u"progression_batreaux")

        self.gridLayout_3.addWidget(self.progression_batreaux, 3, 2, 1, 1)

        self.progression_crystal = QCheckBox(self.gridLayoutWidget_3)
        self.progression_crystal.setObjectName(u"progression_crystal")

        self.gridLayout_3.addWidget(self.progression_crystal, 3, 3, 1, 1)

        self.progression_scrapper = QCheckBox(self.gridLayoutWidget_3)
        self.progression_scrapper.setObjectName(u"progression_scrapper")

        self.gridLayout_3.addWidget(self.progression_scrapper, 4, 4, 1, 1)

        self.progression_crystal_quest = QCheckBox(self.gridLayoutWidget_3)
        self.progression_crystal_quest.setObjectName(u"progression_crystal_quest")

        self.gridLayout_3.addWidget(self.progression_crystal_quest, 4, 3, 1, 1)

        self.progression_fetch = QCheckBox(self.gridLayoutWidget_3)
        self.progression_fetch.setObjectName(u"progression_fetch")

        self.gridLayout_3.addWidget(self.progression_fetch, 4, 2, 1, 1)

        self.progression_peatrice = QCheckBox(self.gridLayoutWidget_3)
        self.progression_peatrice.setObjectName(u"progression_peatrice")

        self.gridLayout_3.addWidget(self.progression_peatrice, 3, 4, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 420, 931, 161))
        self.gridLayoutWidget_2 = QWidget(self.groupBox_2)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 20, 911, 141))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 4, 1, 1)

        self.option_swordless = QCheckBox(self.gridLayoutWidget_2)
        self.option_swordless.setObjectName(u"option_swordless")

        self.gridLayout_2.addWidget(self.option_swordless, 0, 0, 1, 2)

        self.option_empty_unrequired_dungeons = QCheckBox(self.gridLayoutWidget_2)
        self.option_empty_unrequired_dungeons.setObjectName(u"option_empty_unrequired_dungeons")

        self.gridLayout_2.addWidget(self.option_empty_unrequired_dungeons, 1, 0, 1, 2)

        self.label_for_option_starting_tablet_count = QLabel(self.gridLayoutWidget_2)
        self.label_for_option_starting_tablet_count.setObjectName(u"label_for_option_starting_tablet_count")

        self.gridLayout_2.addWidget(self.label_for_option_starting_tablet_count, 0, 3, 1, 1)

        self.option_skip_skykeep = QCheckBox(self.gridLayoutWidget_2)
        self.option_skip_skykeep.setObjectName(u"option_skip_skykeep")

        self.gridLayout_2.addWidget(self.option_skip_skykeep, 2, 0, 1, 2)

        self.option_closed_thunderhead = QCheckBox(self.gridLayoutWidget_2)
        self.option_closed_thunderhead.setObjectName(u"option_closed_thunderhead")

        self.gridLayout_2.addWidget(self.option_closed_thunderhead, 1, 2, 1, 3)

        self.option_starting_tablet_count = QSpinBox(self.gridLayoutWidget_2)
        self.option_starting_tablet_count.setObjectName(u"option_starting_tablet_count")
        self.option_starting_tablet_count.setMaximumSize(QSize(41, 16777215))

        self.gridLayout_2.addWidget(self.option_starting_tablet_count, 0, 2, 1, 1)

        self.label_for_option_required_dungeon_count = QLabel(self.gridLayoutWidget_2)
        self.label_for_option_required_dungeon_count.setObjectName(u"label_for_option_required_dungeon_count")

        self.gridLayout_2.addWidget(self.label_for_option_required_dungeon_count, 2, 3, 1, 1)

        self.option_required_dungeon_count = QSpinBox(self.gridLayoutWidget_2)
        self.option_required_dungeon_count.setObjectName(u"option_required_dungeon_count")
        self.option_required_dungeon_count.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.option_required_dungeon_count.sizePolicy().hasHeightForWidth())
        self.option_required_dungeon_count.setSizePolicy(sizePolicy2)
        self.option_required_dungeon_count.setMaximumSize(QSize(41, 16777215))

        self.gridLayout_2.addWidget(self.option_required_dungeon_count, 2, 2, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")

        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 4, 1, 1)

        self.option_start_pouch = QCheckBox(self.gridLayoutWidget_2)
        self.option_start_pouch.setObjectName(u"option_start_pouch")

        self.gridLayout_2.addWidget(self.option_start_pouch, 3, 0, 1, 2)

        self.option_max_batreaux_reward = QComboBox(self.gridLayoutWidget_2)
        self.option_max_batreaux_reward.setObjectName(u"option_max_batreaux_reward")

        self.gridLayout_2.addWidget(self.option_max_batreaux_reward, 3, 3, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 650, 931, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.option_dry_run = QCheckBox(self.horizontalLayoutWidget)
        self.option_dry_run.setObjectName(u"option_dry_run")

        self.horizontalLayout.addWidget(self.option_dry_run)

        self.option_hero_mode = QCheckBox(self.horizontalLayoutWidget)
        self.option_hero_mode.setObjectName(u"option_hero_mode")

        self.horizontalLayout.addWidget(self.option_hero_mode)

        self.option_no_spoiler_log = QCheckBox(self.horizontalLayoutWidget)
        self.option_no_spoiler_log.setObjectName(u"option_no_spoiler_log")

        self.horizontalLayout.addWidget(self.option_no_spoiler_log)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.randomize_button = QPushButton(self.horizontalLayoutWidget)
        self.randomize_button.setObjectName(u"randomize_button")

        self.horizontalLayout.addWidget(self.randomize_button)

        self.option_description = QLabel(self.centralwidget)
        self.option_description.setObjectName(u"option_description")
        self.option_description.setEnabled(True)
        self.option_description.setGeometry(QRect(10, 590, 931, 20))
        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 620, 931, 27))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.permalink_label = QLabel(self.horizontalLayoutWidget_2)
        self.permalink_label.setObjectName(u"permalink_label")

        self.horizontalLayout_3.addWidget(self.permalink_label)

        self.permalink = QLineEdit(self.horizontalLayoutWidget_2)
        self.permalink.setObjectName(u"permalink")

        self.horizontalLayout_3.addWidget(self.permalink)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 300, 931, 111))
        self.gridLayoutWidget_4 = QWidget(self.groupBox_3)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 20, 911, 83))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.progression_eldin_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_eldin_goddess.setObjectName(u"progression_eldin_goddess")

        self.gridLayout_4.addWidget(self.progression_eldin_goddess, 1, 1, 1, 1)

        self.progression_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_goddess.setObjectName(u"progression_goddess")

        self.gridLayout_4.addWidget(self.progression_goddess, 0, 0, 1, 1)

        self.progression_faron_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_faron_goddess.setObjectName(u"progression_faron_goddess")

        self.gridLayout_4.addWidget(self.progression_faron_goddess, 1, 0, 1, 1)

        self.progression_lanayru_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_lanayru_goddess.setObjectName(u"progression_lanayru_goddess")

        self.gridLayout_4.addWidget(self.progression_lanayru_goddess, 1, 2, 1, 1)

        self.progression_summit_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_summit_goddess.setObjectName(u"progression_summit_goddess")

        self.gridLayout_4.addWidget(self.progression_summit_goddess, 2, 1, 1, 1)

        self.progression_floria_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_floria_goddess.setObjectName(u"progression_floria_goddess")

        self.gridLayout_4.addWidget(self.progression_floria_goddess, 2, 0, 1, 1)

        self.progression_sand_sea_goddess = QCheckBox(self.gridLayoutWidget_4)
        self.progression_sand_sea_goddess.setObjectName(u"progression_sand_sea_goddess")

        self.gridLayout_4.addWidget(self.progression_sand_sea_goddess, 2, 2, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 80, 931, 51))
        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 20, 911, 25))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.progression_skyloft = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_skyloft.setObjectName(u"progression_skyloft")

        self.horizontalLayout_4.addWidget(self.progression_skyloft)

        self.progression_sky = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_sky.setObjectName(u"progression_sky")

        self.horizontalLayout_4.addWidget(self.progression_sky)

        self.progression_thunderhead = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_thunderhead.setObjectName(u"progression_thunderhead")

        self.horizontalLayout_4.addWidget(self.progression_thunderhead)

        self.progression_faron = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_faron.setObjectName(u"progression_faron")

        self.horizontalLayout_4.addWidget(self.progression_faron)

        self.progression_eldin = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_eldin.setObjectName(u"progression_eldin")

        self.horizontalLayout_4.addWidget(self.progression_eldin)

        self.progression_lanayru = QCheckBox(self.horizontalLayoutWidget_3)
        self.progression_lanayru.setObjectName(u"progression_lanayru")

        self.horizontalLayout_4.addWidget(self.progression_lanayru)

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
        self.progression_short.setText(QCoreApplication.translate("MainWindow", u"Short Quests", None))
        self.progression_miscellaneous.setText(QCoreApplication.translate("MainWindow", u"Miscellaneous", None))
        self.progression_free_gift.setText(QCoreApplication.translate("MainWindow", u"Free Gifts", None))
        self.progression_song.setText(QCoreApplication.translate("MainWindow", u"Songs", None))
        self.progression_mini_dungeon.setText(QCoreApplication.translate("MainWindow", u"Mini Dungeons", None))
        self.progression_silent_realm.setText(QCoreApplication.translate("MainWindow", u"Silent Realms", None))
        self.progression_freestanding.setText(QCoreApplication.translate("MainWindow", u"Freestanding Items", None))
        self.progression_long.setText(QCoreApplication.translate("MainWindow", u"Long Quests", None))
        self.progression_dungeon.setText(QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.progression_minigame.setText(QCoreApplication.translate("MainWindow", u"Minigames", None))
        self.progression_digging.setText(QCoreApplication.translate("MainWindow", u"Digging Spots", None))
        self.progression_bombable.setText(QCoreApplication.translate("MainWindow", u"Bombable Walls", None))
        self.progression_combat.setText(QCoreApplication.translate("MainWindow", u"Combat Rewards", None))
        self.progression_spiral_charge.setText(QCoreApplication.translate("MainWindow", u"Spiral Charge Chests", None))
        self.progression_batreaux.setText(QCoreApplication.translate("MainWindow", u"Batreaux", None))
        self.progression_crystal.setText(QCoreApplication.translate("MainWindow", u"Loose Crystals", None))
        self.progression_scrapper.setText(QCoreApplication.translate("MainWindow", u"Scrapper Quests", None))
        self.progression_crystal_quest.setText(QCoreApplication.translate("MainWindow", u"Crystal Quests", None))
        self.progression_fetch.setText(QCoreApplication.translate("MainWindow", u"Fetch Quests", None))
        self.progression_peatrice.setText(QCoreApplication.translate("MainWindow", u"Peatrice", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Additional Options", None))
        self.option_swordless.setText(QCoreApplication.translate("MainWindow", u"Swordless", None))
        self.option_empty_unrequired_dungeons.setText(QCoreApplication.translate("MainWindow", u"Race Mode", None))
        self.label_for_option_starting_tablet_count.setText(QCoreApplication.translate("MainWindow", u"Starting Tablets", None))
        self.option_skip_skykeep.setText(QCoreApplication.translate("MainWindow", u"Skip Skykeep", None))
        self.option_closed_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Closed Thunderhead", None))
        self.label_for_option_required_dungeon_count.setText(QCoreApplication.translate("MainWindow", u"Required Dungeon Count", None))
        self.option_start_pouch.setText(QCoreApplication.translate("MainWindow", u"Start with Adventure Pouch", None))
        self.option_dry_run.setText(QCoreApplication.translate("MainWindow", u"Dry Run", None))
        self.option_hero_mode.setText(QCoreApplication.translate("MainWindow", u"Hero Mode", None))
        self.option_no_spoiler_log.setText(QCoreApplication.translate("MainWindow", u"No Spoiler Log", None))
        self.randomize_button.setText(QCoreApplication.translate("MainWindow", u"Randomize", None))
        self.option_description.setText("")
        self.permalink_label.setText(QCoreApplication.translate("MainWindow", u"Permalink (copy paste to share your settings)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Goddess Cube Options", None))
        self.progression_eldin_goddess.setText(QCoreApplication.translate("MainWindow", u"Eldin Volcano", None))
        self.progression_goddess.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.progression_faron_goddess.setText(QCoreApplication.translate("MainWindow", u"Faron Woods", None))
        self.progression_lanayru_goddess.setText(QCoreApplication.translate("MainWindow", u"Lanayru Desert", None))
        self.progression_summit_goddess.setText(QCoreApplication.translate("MainWindow", u"Volcano Summit", None))
        self.progression_floria_goddess.setText(QCoreApplication.translate("MainWindow", u"Lake Floria", None))
        self.progression_sand_sea_goddess.setText(QCoreApplication.translate("MainWindow", u"Sand Sea", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"What areas of the world should progress items appear?", None))
        self.progression_skyloft.setText(QCoreApplication.translate("MainWindow", u"Skyloft", None))
        self.progression_sky.setText(QCoreApplication.translate("MainWindow", u"The Sky", None))
        self.progression_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Thunderhead", None))
        self.progression_faron.setText(QCoreApplication.translate("MainWindow", u"Faron", None))
        self.progression_eldin.setText(QCoreApplication.translate("MainWindow", u"Eldin", None))
        self.progression_lanayru.setText(QCoreApplication.translate("MainWindow", u"Lanayru", None))
    # retranslateUi

