# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randogui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
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
        MainWindow.resize(956, 704)
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
        self.option_description = QLabel(self.centralwidget)
        self.option_description.setObjectName(u"option_description")
        self.option_description.setEnabled(True)
        self.option_description.setGeometry(QRect(10, 570, 931, 31))
        self.option_description.setWordWrap(True)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 931, 541))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayoutWidget_9 = QWidget(self.tab)
        self.verticalLayoutWidget_9.setObjectName(u"verticalLayoutWidget_9")
        self.verticalLayoutWidget_9.setGeometry(QRect(10, 10, 901, 101))
        self.verticalLayout_29 = QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.verticalLayoutWidget_9)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_2)

        self.output_folder = QLineEdit(self.verticalLayoutWidget_9)
        self.output_folder.setObjectName(u"output_folder")

        self.horizontalLayout_7.addWidget(self.output_folder)

        self.ouput_folder_browse_button = QPushButton(self.verticalLayoutWidget_9)
        self.ouput_folder_browse_button.setObjectName(u"ouput_folder_browse_button")

        self.horizontalLayout_7.addWidget(self.ouput_folder_browse_button)


        self.verticalLayout_29.addLayout(self.horizontalLayout_7)

        self.verticalLayout_32 = QVBoxLayout()
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.option_plando = QCheckBox(self.verticalLayoutWidget_9)
        self.option_plando.setObjectName(u"option_plando")

        self.verticalLayout_32.addWidget(self.option_plando)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.plando_file = QLineEdit(self.verticalLayoutWidget_9)
        self.plando_file.setObjectName(u"plando_file")

        self.horizontalLayout_19.addWidget(self.plando_file)

        self.plando_file_browse = QPushButton(self.verticalLayoutWidget_9)
        self.plando_file_browse.setObjectName(u"plando_file_browse")

        self.horizontalLayout_19.addWidget(self.plando_file_browse)


        self.verticalLayout_32.addLayout(self.horizontalLayout_19)


        self.verticalLayout_29.addLayout(self.verticalLayout_32)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_12)

        self.groupBox_12 = QGroupBox(self.tab)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setGeometry(QRect(10, 120, 181, 111))
        self.verticalLayoutWidget_13 = QWidget(self.groupBox_12)
        self.verticalLayoutWidget_13.setObjectName(u"verticalLayoutWidget_13")
        self.verticalLayoutWidget_13.setGeometry(QRect(10, 20, 160, 80))
        self.verticalLayout_33 = QVBoxLayout(self.verticalLayoutWidget_13)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.option_no_spoiler_log = QCheckBox(self.verticalLayoutWidget_13)
        self.option_no_spoiler_log.setObjectName(u"option_no_spoiler_log")

        self.verticalLayout_33.addWidget(self.option_no_spoiler_log)

        self.option_json_spoiler = QCheckBox(self.verticalLayoutWidget_13)
        self.option_json_spoiler.setObjectName(u"option_json_spoiler")

        self.verticalLayout_33.addWidget(self.option_json_spoiler)

        self.option_out_placement_file = QCheckBox(self.verticalLayoutWidget_13)
        self.option_out_placement_file.setObjectName(u"option_out_placement_file")

        self.verticalLayout_33.addWidget(self.option_out_placement_file)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_33.addItem(self.verticalSpacer_13)

        self.groupBox_13 = QGroupBox(self.tab)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setGeometry(QRect(210, 120, 131, 111))
        self.verticalLayoutWidget_14 = QWidget(self.groupBox_13)
        self.verticalLayoutWidget_14.setObjectName(u"verticalLayoutWidget_14")
        self.verticalLayoutWidget_14.setGeometry(QRect(10, 20, 111, 81))
        self.verticalLayout_34 = QVBoxLayout(self.verticalLayoutWidget_14)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.option_dry_run = QCheckBox(self.verticalLayoutWidget_14)
        self.option_dry_run.setObjectName(u"option_dry_run")

        self.verticalLayout_34.addWidget(self.option_dry_run)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_34.addItem(self.verticalSpacer_14)

        self.groupBox_14 = QGroupBox(self.tab)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setGeometry(QRect(350, 120, 131, 111))
        self.option_tunic_swap = QCheckBox(self.groupBox_14)
        self.option_tunic_swap.setObjectName(u"option_tunic_swap")
        self.option_tunic_swap.setGeometry(QRect(10, 20, 111, 23))
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.groupBox_4 = QGroupBox(self.tab_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 10, 901, 51))
        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_4)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 20, 891, 25))
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

        self.groupBox = QGroupBox(self.tab_3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 70, 901, 161))
        self.gridLayoutWidget_3 = QWidget(self.groupBox)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 891, 131))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.progression_miscellaneous = QCheckBox(self.gridLayoutWidget_3)
        self.progression_miscellaneous.setObjectName(u"progression_miscellaneous")

        self.gridLayout_3.addWidget(self.progression_miscellaneous, 1, 4, 1, 1)

        self.progression_long = QCheckBox(self.gridLayoutWidget_3)
        self.progression_long.setObjectName(u"progression_long")

        self.gridLayout_3.addWidget(self.progression_long, 4, 1, 1, 1)

        self.progression_short = QCheckBox(self.gridLayoutWidget_3)
        self.progression_short.setObjectName(u"progression_short")

        self.gridLayout_3.addWidget(self.progression_short, 4, 0, 1, 1)

        self.progression_free_gift = QCheckBox(self.gridLayoutWidget_3)
        self.progression_free_gift.setObjectName(u"progression_free_gift")

        self.gridLayout_3.addWidget(self.progression_free_gift, 1, 2, 1, 1)

        self.progression_digging = QCheckBox(self.gridLayoutWidget_3)
        self.progression_digging.setObjectName(u"progression_digging")

        self.gridLayout_3.addWidget(self.progression_digging, 2, 1, 1, 1)

        self.progression_dungeon = QCheckBox(self.gridLayoutWidget_3)
        self.progression_dungeon.setObjectName(u"progression_dungeon")

        self.gridLayout_3.addWidget(self.progression_dungeon, 1, 0, 1, 1)

        self.progression_spiral_charge = QCheckBox(self.gridLayoutWidget_3)
        self.progression_spiral_charge.setObjectName(u"progression_spiral_charge")

        self.gridLayout_3.addWidget(self.progression_spiral_charge, 3, 0, 1, 1)

        self.progression_crystal = QCheckBox(self.gridLayoutWidget_3)
        self.progression_crystal.setObjectName(u"progression_crystal")

        self.gridLayout_3.addWidget(self.progression_crystal, 3, 3, 1, 1)

        self.progression_bombable = QCheckBox(self.gridLayoutWidget_3)
        self.progression_bombable.setObjectName(u"progression_bombable")

        self.gridLayout_3.addWidget(self.progression_bombable, 2, 2, 1, 1)

        self.progression_minigame = QCheckBox(self.gridLayoutWidget_3)
        self.progression_minigame.setObjectName(u"progression_minigame")

        self.gridLayout_3.addWidget(self.progression_minigame, 3, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.option_max_batreaux_reward = QComboBox(self.gridLayoutWidget_3)
        self.option_max_batreaux_reward.setObjectName(u"option_max_batreaux_reward")

        self.horizontalLayout_6.addWidget(self.option_max_batreaux_reward)

        self.label_for_option_max_batreaux_reward = QLabel(self.gridLayoutWidget_3)
        self.label_for_option_max_batreaux_reward.setObjectName(u"label_for_option_max_batreaux_reward")

        self.horizontalLayout_6.addWidget(self.label_for_option_max_batreaux_reward)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 3, 2, 1, 1)

        self.progression_combat = QCheckBox(self.gridLayoutWidget_3)
        self.progression_combat.setObjectName(u"progression_combat")

        self.gridLayout_3.addWidget(self.progression_combat, 2, 3, 1, 1)

        self.progression_mini_dungeon = QCheckBox(self.gridLayoutWidget_3)
        self.progression_mini_dungeon.setObjectName(u"progression_mini_dungeon")

        self.gridLayout_3.addWidget(self.progression_mini_dungeon, 1, 1, 1, 1)

        self.progression_freestanding = QCheckBox(self.gridLayoutWidget_3)
        self.progression_freestanding.setObjectName(u"progression_freestanding")

        self.gridLayout_3.addWidget(self.progression_freestanding, 1, 3, 1, 1)

        self.progression_crystal_quest = QCheckBox(self.gridLayoutWidget_3)
        self.progression_crystal_quest.setObjectName(u"progression_crystal_quest")

        self.gridLayout_3.addWidget(self.progression_crystal_quest, 4, 3, 1, 1)

        self.progression_song = QCheckBox(self.gridLayoutWidget_3)
        self.progression_song.setObjectName(u"progression_song")

        self.gridLayout_3.addWidget(self.progression_song, 2, 4, 1, 1)

        self.progression_scrapper = QCheckBox(self.gridLayoutWidget_3)
        self.progression_scrapper.setObjectName(u"progression_scrapper")

        self.gridLayout_3.addWidget(self.progression_scrapper, 4, 4, 1, 1)

        self.progression_silent_realm = QCheckBox(self.gridLayoutWidget_3)
        self.progression_silent_realm.setObjectName(u"progression_silent_realm")

        self.gridLayout_3.addWidget(self.progression_silent_realm, 2, 0, 1, 1)

        self.progression_peatrice = QCheckBox(self.gridLayoutWidget_3)
        self.progression_peatrice.setObjectName(u"progression_peatrice")

        self.gridLayout_3.addWidget(self.progression_peatrice, 3, 4, 1, 1)

        self.progression_fetch = QCheckBox(self.gridLayoutWidget_3)
        self.progression_fetch.setObjectName(u"progression_fetch")

        self.gridLayout_3.addWidget(self.progression_fetch, 4, 2, 1, 1)

        self.progression_beedle = QCheckBox(self.gridLayoutWidget_3)
        self.progression_beedle.setObjectName(u"progression_beedle")

        self.gridLayout_3.addWidget(self.progression_beedle, 5, 1, 1, 1)

        self.progression_cheap = QCheckBox(self.gridLayoutWidget_3)
        self.progression_cheap.setObjectName(u"progression_cheap")

        self.gridLayout_3.addWidget(self.progression_cheap, 5, 2, 1, 1)

        self.progression_medium = QCheckBox(self.gridLayoutWidget_3)
        self.progression_medium.setObjectName(u"progression_medium")

        self.gridLayout_3.addWidget(self.progression_medium, 5, 3, 1, 1)

        self.progression_expensive = QCheckBox(self.gridLayoutWidget_3)
        self.progression_expensive.setObjectName(u"progression_expensive")

        self.gridLayout_3.addWidget(self.progression_expensive, 5, 4, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.option_shopsanity = QComboBox(self.gridLayoutWidget_3)
        self.option_shopsanity.setObjectName(u"option_shopsanity")

        self.horizontalLayout_11.addWidget(self.option_shopsanity)

        self.label_10 = QLabel(self.gridLayoutWidget_3)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_11.addWidget(self.label_10)


        self.gridLayout_3.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 240, 901, 111))
        self.gridLayoutWidget_4 = QWidget(self.groupBox_3)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 20, 891, 83))
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

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.groupBox_5 = QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(10, 10, 181, 251))
        self.verticalLayoutWidget = QWidget(self.groupBox_5)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 19, 164, 221))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_for_option_got_starting_state = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_starting_state.setObjectName(u"label_for_option_got_starting_state")

        self.verticalLayout_3.addWidget(self.label_for_option_got_starting_state)

        self.option_got_starting_state = QComboBox(self.verticalLayoutWidget)
        self.option_got_starting_state.setObjectName(u"option_got_starting_state")

        self.verticalLayout_3.addWidget(self.option_got_starting_state)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_for_option_got_sword_requirement = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_sword_requirement.setObjectName(u"label_for_option_got_sword_requirement")

        self.verticalLayout_4.addWidget(self.label_for_option_got_sword_requirement)

        self.option_got_sword_requirement = QComboBox(self.verticalLayoutWidget)
        self.option_got_sword_requirement.setObjectName(u"option_got_sword_requirement")

        self.verticalLayout_4.addWidget(self.option_got_sword_requirement)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_for_option_got_dungeon_requirement = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_dungeon_requirement.setObjectName(u"label_for_option_got_dungeon_requirement")

        self.verticalLayout_5.addWidget(self.label_for_option_got_dungeon_requirement)

        self.option_got_dungeon_requirement = QComboBox(self.verticalLayoutWidget)
        self.option_got_dungeon_requirement.setObjectName(u"option_got_dungeon_requirement")

        self.verticalLayout_5.addWidget(self.option_got_dungeon_requirement)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_for_option_required_dungeon_count = QLabel(self.verticalLayoutWidget)
        self.label_for_option_required_dungeon_count.setObjectName(u"label_for_option_required_dungeon_count")

        self.horizontalLayout_8.addWidget(self.label_for_option_required_dungeon_count)

        self.option_required_dungeon_count = QSpinBox(self.verticalLayoutWidget)
        self.option_required_dungeon_count.setObjectName(u"option_required_dungeon_count")
        self.option_required_dungeon_count.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.option_required_dungeon_count.sizePolicy().hasHeightForWidth())
        self.option_required_dungeon_count.setSizePolicy(sizePolicy2)
        self.option_required_dungeon_count.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_8.addWidget(self.option_required_dungeon_count)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.option_skip_skykeep = QCheckBox(self.verticalLayoutWidget)
        self.option_skip_skykeep.setObjectName(u"option_skip_skykeep")

        self.verticalLayout.addWidget(self.option_skip_skykeep)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(560, 10, 181, 251))
        self.verticalLayoutWidget_7 = QWidget(self.groupBox_7)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 20, 165, 221))
        self.verticalLayout_10 = QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_for_option_map_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_map_mode.setObjectName(u"label_for_option_map_mode")

        self.verticalLayout_11.addWidget(self.label_for_option_map_mode)

        self.option_map_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_map_mode.setObjectName(u"option_map_mode")

        self.verticalLayout_11.addWidget(self.option_map_mode)


        self.verticalLayout_10.addLayout(self.verticalLayout_11)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_for_option_small_key_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_small_key_mode.setObjectName(u"label_for_option_small_key_mode")

        self.verticalLayout_12.addWidget(self.label_for_option_small_key_mode)

        self.option_small_key_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_small_key_mode.setObjectName(u"option_small_key_mode")

        self.verticalLayout_12.addWidget(self.option_small_key_mode)


        self.verticalLayout_10.addLayout(self.verticalLayout_12)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_for_option_boss_key_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_boss_key_mode.setObjectName(u"label_for_option_boss_key_mode")

        self.verticalLayout_13.addWidget(self.label_for_option_boss_key_mode)

        self.option_boss_key_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_boss_key_mode.setObjectName(u"option_boss_key_mode")

        self.verticalLayout_13.addWidget(self.option_boss_key_mode)


        self.verticalLayout_10.addLayout(self.verticalLayout_13)

        self.option_empty_unrequired_dungeons = QCheckBox(self.verticalLayoutWidget_7)
        self.option_empty_unrequired_dungeons.setObjectName(u"option_empty_unrequired_dungeons")

        self.verticalLayout_10.addWidget(self.option_empty_unrequired_dungeons)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_4)

        self.groupBox_8 = QGroupBox(self.tab_4)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setGeometry(QRect(750, 20, 161, 241))
        self.verticalLayoutWidget_3 = QWidget(self.groupBox_8)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 20, 148, 211))
        self.verticalLayout_14 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.option_imp_2 = QCheckBox(self.verticalLayoutWidget_3)
        self.option_imp_2.setObjectName(u"option_imp_2")

        self.verticalLayout_14.addWidget(self.option_imp_2)

        self.option_horde = QCheckBox(self.verticalLayoutWidget_3)
        self.option_horde.setObjectName(u"option_horde")

        self.verticalLayout_14.addWidget(self.option_horde)

        self.option_g3 = QCheckBox(self.verticalLayoutWidget_3)
        self.option_g3.setObjectName(u"option_g3")

        self.verticalLayout_14.addWidget(self.option_g3)

        self.option_demise = QCheckBox(self.verticalLayoutWidget_3)
        self.option_demise.setObjectName(u"option_demise")

        self.verticalLayout_14.addWidget(self.option_demise)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_5)

        self.groupBox_2 = QGroupBox(self.tab_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(200, 10, 171, 251))
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 151, 221))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_for_option_open_thunderhead = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_open_thunderhead.setObjectName(u"label_for_option_open_thunderhead")

        self.verticalLayout_6.addWidget(self.label_for_option_open_thunderhead)

        self.option_open_thunderhead = QComboBox(self.verticalLayoutWidget_2)
        self.option_open_thunderhead.setObjectName(u"option_open_thunderhead")

        self.verticalLayout_6.addWidget(self.option_open_thunderhead)


        self.verticalLayout_2.addLayout(self.verticalLayout_6)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_for_option_open_lmf = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_open_lmf.setObjectName(u"label_for_option_open_lmf")

        self.verticalLayout_8.addWidget(self.label_for_option_open_lmf)

        self.option_open_lmf = QComboBox(self.verticalLayoutWidget_2)
        self.option_open_lmf.setObjectName(u"option_open_lmf")

        self.verticalLayout_8.addWidget(self.option_open_lmf)


        self.verticalLayout_2.addLayout(self.verticalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_for_option_starting_tablet_count = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_starting_tablet_count.setObjectName(u"label_for_option_starting_tablet_count")

        self.horizontalLayout_10.addWidget(self.label_for_option_starting_tablet_count)

        self.option_starting_tablet_count = QSpinBox(self.verticalLayoutWidget_2)
        self.option_starting_tablet_count.setObjectName(u"option_starting_tablet_count")
        self.option_starting_tablet_count.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_10.addWidget(self.option_starting_tablet_count)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.groupBox_6 = QGroupBox(self.tab_4)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(380, 10, 171, 251))
        self.verticalLayoutWidget_4 = QWidget(self.groupBox_6)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 19, 151, 221))
        self.verticalLayout_7 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_for_option_randomize_entrances = QLabel(self.verticalLayoutWidget_4)
        self.label_for_option_randomize_entrances.setObjectName(u"label_for_option_randomize_entrances")

        self.verticalLayout_9.addWidget(self.label_for_option_randomize_entrances)

        self.option_randomize_entrances = QComboBox(self.verticalLayoutWidget_4)
        self.option_randomize_entrances.setObjectName(u"option_randomize_entrances")

        self.verticalLayout_9.addWidget(self.option_randomize_entrances)


        self.verticalLayout_7.addLayout(self.verticalLayout_9)

        self.option_randomize_trials = QCheckBox(self.verticalLayoutWidget_4)
        self.option_randomize_trials.setObjectName(u"option_randomize_trials")

        self.verticalLayout_7.addWidget(self.option_randomize_trials)

        self.verticalSpacer = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.groupBox_9 = QGroupBox(self.tab_4)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.groupBox_9.setGeometry(QRect(10, 270, 181, 241))
        self.verticalLayoutWidget_5 = QWidget(self.groupBox_9)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 20, 161, 211))
        self.verticalLayout_15 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.label_for_option_starting_sword = QLabel(self.verticalLayoutWidget_5)
        self.label_for_option_starting_sword.setObjectName(u"label_for_option_starting_sword")

        self.verticalLayout_28.addWidget(self.label_for_option_starting_sword)

        self.option_starting_sword = QComboBox(self.verticalLayoutWidget_5)
        self.option_starting_sword.setObjectName(u"option_starting_sword")

        self.verticalLayout_28.addWidget(self.option_starting_sword)


        self.verticalLayout_15.addLayout(self.verticalLayout_28)

        self.option_start_pouch = QCheckBox(self.verticalLayoutWidget_5)
        self.option_start_pouch.setObjectName(u"option_start_pouch")

        self.verticalLayout_15.addWidget(self.option_start_pouch)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_for_option_rupoor = QLabel(self.verticalLayoutWidget_5)
        self.label_for_option_rupoor.setObjectName(u"label_for_option_rupoor")

        self.verticalLayout_16.addWidget(self.label_for_option_rupoor)

        self.option_rupoor_mode = QComboBox(self.verticalLayoutWidget_5)
        self.option_rupoor_mode.setObjectName(u"option_rupoor_mode")

        self.verticalLayout_16.addWidget(self.option_rupoor_mode)


        self.verticalLayout_15.addLayout(self.verticalLayout_16)

        self.option_fix_bit_crashes = QCheckBox(self.verticalLayoutWidget_5)
        self.option_fix_bit_crashes.setObjectName(u"option_fix_bit_crashes")

        self.verticalLayout_15.addWidget(self.option_fix_bit_crashes)

        self.option_hero_mode = QCheckBox(self.verticalLayoutWidget_5)
        self.option_hero_mode.setObjectName(u"option_hero_mode")

        self.verticalLayout_15.addWidget(self.option_hero_mode)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer_6)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.layoutWidget = QWidget(self.tab_5)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 909, 499))
        self.verticalLayout_18 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.label_for_option_logic_mode = QLabel(self.layoutWidget)
        self.label_for_option_logic_mode.setObjectName(u"label_for_option_logic_mode")

        self.verticalLayout_18.addWidget(self.label_for_option_logic_mode)

        self.option_logic_mode = QComboBox(self.layoutWidget)
        self.option_logic_mode.setObjectName(u"option_logic_mode")

        self.verticalLayout_18.addWidget(self.option_logic_mode)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_19.addWidget(self.label)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.enabled_locations = QListView(self.layoutWidget)
        self.enabled_locations.setObjectName(u"enabled_locations")

        self.horizontalLayout_17.addWidget(self.enabled_locations)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.enable_location = QPushButton(self.layoutWidget)
        self.enable_location.setObjectName(u"enable_location")

        self.verticalLayout_20.addWidget(self.enable_location)

        self.disable_location = QPushButton(self.layoutWidget)
        self.disable_location.setObjectName(u"disable_location")

        self.verticalLayout_20.addWidget(self.disable_location)


        self.horizontalLayout_17.addLayout(self.verticalLayout_20)

        self.disabled_locations = QListWidget(self.layoutWidget)
        self.disabled_locations.setObjectName(u"disabled_locations")

        self.horizontalLayout_17.addWidget(self.disabled_locations)


        self.verticalLayout_19.addLayout(self.horizontalLayout_17)


        self.horizontalLayout_2.addLayout(self.verticalLayout_19)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_25.addWidget(self.label_5)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.enabled_tricks = QListView(self.layoutWidget)
        self.enabled_tricks.setObjectName(u"enabled_tricks")

        self.horizontalLayout_18.addWidget(self.enabled_tricks)

        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.enable_trick = QPushButton(self.layoutWidget)
        self.enable_trick.setObjectName(u"enable_trick")

        self.verticalLayout_21.addWidget(self.enable_trick)

        self.disable_trick = QPushButton(self.layoutWidget)
        self.disable_trick.setObjectName(u"disable_trick")

        self.verticalLayout_21.addWidget(self.disable_trick)


        self.horizontalLayout_18.addLayout(self.verticalLayout_21)

        self.disabled_tricks = QListView(self.layoutWidget)
        self.disabled_tricks.setObjectName(u"disabled_tricks")

        self.horizontalLayout_18.addWidget(self.disabled_tricks)


        self.verticalLayout_25.addLayout(self.horizontalLayout_18)


        self.horizontalLayout_2.addLayout(self.verticalLayout_25)


        self.verticalLayout_18.addLayout(self.horizontalLayout_2)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.groupBox_10 = QGroupBox(self.tab_7)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(10, 10, 181, 221))
        self.verticalLayoutWidget_12 = QWidget(self.groupBox_10)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(10, 20, 161, 191))
        self.verticalLayout_22 = QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.label_for_option_hint_distribution = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_hint_distribution.setObjectName(u"label_for_option_hint_distribution")

        self.verticalLayout_24.addWidget(self.label_for_option_hint_distribution)

        self.option_hint_distribution = QComboBox(self.verticalLayoutWidget_12)
        self.option_hint_distribution.setObjectName(u"option_hint_distribution")

        self.verticalLayout_24.addWidget(self.option_hint_distribution)


        self.verticalLayout_22.addLayout(self.verticalLayout_24)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_for_option_woth_hints = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_woth_hints.setObjectName(u"label_for_option_woth_hints")

        self.horizontalLayout_9.addWidget(self.label_for_option_woth_hints)

        self.option_woth_hints = QSpinBox(self.verticalLayoutWidget_12)
        self.option_woth_hints.setObjectName(u"option_woth_hints")

        self.horizontalLayout_9.addWidget(self.option_woth_hints)


        self.verticalLayout_22.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_for_option_barren_hints = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_barren_hints.setObjectName(u"label_for_option_barren_hints")

        self.horizontalLayout_12.addWidget(self.label_for_option_barren_hints)

        self.option_barren_hints = QSpinBox(self.verticalLayoutWidget_12)
        self.option_barren_hints.setObjectName(u"option_barren_hints")

        self.horizontalLayout_12.addWidget(self.option_barren_hints)


        self.verticalLayout_22.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_for_option_sometimes_hints = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_sometimes_hints.setObjectName(u"label_for_option_sometimes_hints")

        self.horizontalLayout_13.addWidget(self.label_for_option_sometimes_hints)

        self.option_sometimes_hints = QSpinBox(self.verticalLayoutWidget_12)
        self.option_sometimes_hints.setObjectName(u"option_sometimes_hints")

        self.horizontalLayout_13.addWidget(self.option_sometimes_hints)


        self.verticalLayout_22.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_for_option_location_hints = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_location_hints.setObjectName(u"label_for_option_location_hints")

        self.horizontalLayout_14.addWidget(self.label_for_option_location_hints)

        self.option_location_hints = QSpinBox(self.verticalLayoutWidget_12)
        self.option_location_hints.setObjectName(u"option_location_hints")

        self.horizontalLayout_14.addWidget(self.option_location_hints)


        self.verticalLayout_22.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_for_option_item_hints = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_item_hints.setObjectName(u"label_for_option_item_hints")

        self.horizontalLayout_15.addWidget(self.label_for_option_item_hints)

        self.option_item_hints = QSpinBox(self.verticalLayoutWidget_12)
        self.option_item_hints.setObjectName(u"option_item_hints")

        self.horizontalLayout_15.addWidget(self.option_item_hints)


        self.verticalLayout_22.addLayout(self.horizontalLayout_15)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_11)

        self.groupBox_11 = QGroupBox(self.tab_7)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(200, 10, 181, 221))
        self.verticalLayoutWidget_6 = QWidget(self.groupBox_11)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 20, 161, 171))
        self.verticalLayout_26 = QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.label_6 = QLabel(self.verticalLayoutWidget_6)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_27.addWidget(self.label_6)

        self.option_song_hints = QComboBox(self.verticalLayoutWidget_6)
        self.option_song_hints.setObjectName(u"option_song_hints")

        self.verticalLayout_27.addWidget(self.option_song_hints)


        self.verticalLayout_26.addLayout(self.verticalLayout_27)

        self.option_impa_sot_hint = QCheckBox(self.verticalLayoutWidget_6)
        self.option_impa_sot_hint.setObjectName(u"option_impa_sot_hint")

        self.verticalLayout_26.addWidget(self.option_impa_sot_hint)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_26.addItem(self.verticalSpacer_10)

        self.tabWidget.addTab(self.tab_7, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.horizontalLayoutWidget_5 = QWidget(self.tab_6)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(10, 10, 911, 451))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.randomized_items = QListView(self.horizontalLayoutWidget_5)
        self.randomized_items.setObjectName(u"randomized_items")

        self.horizontalLayout_5.addWidget(self.randomized_items)

        self.verticalLayout_23 = QVBoxLayout()
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_23.addItem(self.verticalSpacer_9)

        self.randomize_item = QPushButton(self.horizontalLayoutWidget_5)
        self.randomize_item.setObjectName(u"randomize_item")

        self.verticalLayout_23.addWidget(self.randomize_item)

        self.start_with_item = QPushButton(self.horizontalLayoutWidget_5)
        self.start_with_item.setObjectName(u"start_with_item")

        self.verticalLayout_23.addWidget(self.start_with_item)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_23.addItem(self.verticalSpacer_8)


        self.horizontalLayout_5.addLayout(self.verticalLayout_23)

        self.starting_items = QListView(self.horizontalLayoutWidget_5)
        self.starting_items.setObjectName(u"starting_items")

        self.horizontalLayout_5.addWidget(self.starting_items)

        self.tabWidget.addTab(self.tab_6, "")
        self.verticalLayoutWidget_10 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_10.setObjectName(u"verticalLayoutWidget_10")
        self.verticalLayoutWidget_10.setGeometry(QRect(10, 615, 931, 86))
        self.verticalLayout_30 = QVBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.permalink_label = QLabel(self.verticalLayoutWidget_10)
        self.permalink_label.setObjectName(u"permalink_label")

        self.horizontalLayout_3.addWidget(self.permalink_label)

        self.permalink = QLineEdit(self.verticalLayoutWidget_10)
        self.permalink.setObjectName(u"permalink")

        self.horizontalLayout_3.addWidget(self.permalink)


        self.verticalLayout_30.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_3 = QLabel(self.verticalLayoutWidget_10)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setToolTipDuration(-1)
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.label_3)

        self.seed = QLineEdit(self.verticalLayoutWidget_10)
        self.seed.setObjectName(u"seed")

        self.horizontalLayout_16.addWidget(self.seed)

        self.seed_button = QPushButton(self.verticalLayoutWidget_10)
        self.seed_button.setObjectName(u"seed_button")

        self.horizontalLayout_16.addWidget(self.seed_button)


        self.verticalLayout_30.addLayout(self.horizontalLayout_16)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.randomize_button = QPushButton(self.verticalLayoutWidget_10)
        self.randomize_button.setObjectName(u"randomize_button")

        self.horizontalLayout.addWidget(self.randomize_button)


        self.verticalLayout_30.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(4)
        self.option_randomize_entrances.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Skyward Sword Randomizer", None))
        self.option_description.setText("")
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Output Folder", None))
        self.ouput_folder_browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.option_plando.setText(QCoreApplication.translate("MainWindow", u"Enable Plandomizer", None))
        self.plando_file_browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Additional File Generation", None))
        self.option_no_spoiler_log.setText(QCoreApplication.translate("MainWindow", u"No Spoiler Log", None))
        self.option_json_spoiler.setText(QCoreApplication.translate("MainWindow", u"Generate JSON Spoiler Log", None))
        self.option_out_placement_file.setText(QCoreApplication.translate("MainWindow", u"Generate Placement File", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Advanced Options", None))
        self.option_dry_run.setText(QCoreApplication.translate("MainWindow", u"Dry Run", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Cosmetics", None))
        self.option_tunic_swap.setText(QCoreApplication.translate("MainWindow", u"Tunic Swap", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Setup", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"What areas of the world should progress items appear?", None))
        self.progression_skyloft.setText(QCoreApplication.translate("MainWindow", u"Skyloft", None))
        self.progression_sky.setText(QCoreApplication.translate("MainWindow", u"The Sky", None))
        self.progression_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Thunderhead", None))
        self.progression_faron.setText(QCoreApplication.translate("MainWindow", u"Faron", None))
        self.progression_eldin.setText(QCoreApplication.translate("MainWindow", u"Eldin", None))
        self.progression_lanayru.setText(QCoreApplication.translate("MainWindow", u"Lanayru", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Where should progress items appear?", None))
        self.progression_miscellaneous.setText(QCoreApplication.translate("MainWindow", u"Miscellaneous", None))
        self.progression_long.setText(QCoreApplication.translate("MainWindow", u"Long Quests", None))
        self.progression_short.setText(QCoreApplication.translate("MainWindow", u"Short Quests", None))
        self.progression_free_gift.setText(QCoreApplication.translate("MainWindow", u"Free Gifts", None))
        self.progression_digging.setText(QCoreApplication.translate("MainWindow", u"Digging Spots", None))
        self.progression_dungeon.setText(QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.progression_spiral_charge.setText(QCoreApplication.translate("MainWindow", u"Spiral Charge Chests", None))
        self.progression_crystal.setText(QCoreApplication.translate("MainWindow", u"Loose Crystals", None))
        self.progression_bombable.setText(QCoreApplication.translate("MainWindow", u"Bombable Walls", None))
        self.progression_minigame.setText(QCoreApplication.translate("MainWindow", u"Minigames", None))
        self.label_for_option_max_batreaux_reward.setText(QCoreApplication.translate("MainWindow", u"Batreaux", None))
        self.progression_combat.setText(QCoreApplication.translate("MainWindow", u"Combat Rewards", None))
        self.progression_mini_dungeon.setText(QCoreApplication.translate("MainWindow", u"Mini Dungeons", None))
        self.progression_freestanding.setText(QCoreApplication.translate("MainWindow", u"Freestanding Items", None))
        self.progression_crystal_quest.setText(QCoreApplication.translate("MainWindow", u"Crystal Quests", None))
        self.progression_song.setText(QCoreApplication.translate("MainWindow", u"Songs", None))
        self.progression_scrapper.setText(QCoreApplication.translate("MainWindow", u"Scrapper Quests", None))
        self.progression_silent_realm.setText(QCoreApplication.translate("MainWindow", u"Silent Realms", None))
        self.progression_peatrice.setText(QCoreApplication.translate("MainWindow", u"Peatrice", None))
        self.progression_fetch.setText(QCoreApplication.translate("MainWindow", u"Fetch Quests", None))
        self.progression_beedle.setText(QCoreApplication.translate("MainWindow", u"Beedle's Shop", None))
        self.progression_cheap.setText(QCoreApplication.translate("MainWindow", u"Cheap Purchases", None))
        self.progression_medium.setText(QCoreApplication.translate("MainWindow", u"Medium Cost Purchases", None))
        self.progression_expensive.setText(QCoreApplication.translate("MainWindow", u"Expensive Purchases", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Shop Mode", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Goddess Cube Options", None))
        self.progression_eldin_goddess.setText(QCoreApplication.translate("MainWindow", u"Eldin Volcano", None))
        self.progression_goddess.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.progression_faron_goddess.setText(QCoreApplication.translate("MainWindow", u"Faron Woods", None))
        self.progression_lanayru_goddess.setText(QCoreApplication.translate("MainWindow", u"Lanayru Desert", None))
        self.progression_summit_goddess.setText(QCoreApplication.translate("MainWindow", u"Volcano Summit", None))
        self.progression_floria_goddess.setText(QCoreApplication.translate("MainWindow", u"Lake Floria", None))
        self.progression_sand_sea_goddess.setText(QCoreApplication.translate("MainWindow", u"Sand Sea", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Progress Locations", None))
#if QT_CONFIG(tooltip)
        self.tab_4.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Gate of Time and Horde Door", None))
        self.label_for_option_got_starting_state.setText(QCoreApplication.translate("MainWindow", u"Starting State", None))
        self.label_for_option_got_sword_requirement.setText(QCoreApplication.translate("MainWindow", u"Sword Requirement", None))
        self.label_for_option_got_dungeon_requirement.setText(QCoreApplication.translate("MainWindow", u"Dungeon Requirement", None))
        self.label_for_option_required_dungeon_count.setText(QCoreApplication.translate("MainWindow", u"Required Dungeons", None))
        self.option_skip_skykeep.setText(QCoreApplication.translate("MainWindow", u"Skip Sky Keep", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.label_for_option_map_mode.setText(QCoreApplication.translate("MainWindow", u"Map Mode", None))
        self.label_for_option_small_key_mode.setText(QCoreApplication.translate("MainWindow", u"Small Keys", None))
        self.label_for_option_boss_key_mode.setText(QCoreApplication.translate("MainWindow", u"Boss Keys", None))
        self.option_empty_unrequired_dungeons.setText(QCoreApplication.translate("MainWindow", u"Empty Unrequired Dungeons", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Endgame Bosses", None))
        self.option_imp_2.setText(QCoreApplication.translate("MainWindow", u"Skip Imprisoned 2", None))
        self.option_horde.setText(QCoreApplication.translate("MainWindow", u"Horde", None))
        self.option_g3.setText(QCoreApplication.translate("MainWindow", u"Ghirahim 3", None))
        self.option_demise.setText(QCoreApplication.translate("MainWindow", u"Demise", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Open Settings", None))
        self.label_for_option_open_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Open Thunderhead", None))
        self.label_for_option_open_lmf.setText(QCoreApplication.translate("MainWindow", u"Open Lanayru Mining Facility", None))
        self.label_for_option_starting_tablet_count.setText(QCoreApplication.translate("MainWindow", u"Starting Tablets", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Overworld", None))
        self.label_for_option_randomize_entrances.setText(QCoreApplication.translate("MainWindow", u"Randomize Entrances", None))
        self.option_randomize_entrances.setCurrentText("")
        self.option_randomize_trials.setText(QCoreApplication.translate("MainWindow", u"Randomize Silent Realms", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Additional Options", None))
        self.label_for_option_starting_sword.setText(QCoreApplication.translate("MainWindow", u"Starting Sword", None))
        self.option_start_pouch.setText(QCoreApplication.translate("MainWindow", u"Start with Adventure Pouch", None))
        self.label_for_option_rupoor.setText(QCoreApplication.translate("MainWindow", u"Rupoor Mode", None))
        self.option_fix_bit_crashes.setText(QCoreApplication.translate("MainWindow", u"Fix BiT crashes", None))
        self.option_hero_mode.setText(QCoreApplication.translate("MainWindow", u"Hero Mode", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Additional Settings", None))
        self.label_for_option_logic_mode.setText(QCoreApplication.translate("MainWindow", u"Logic Mode", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Exclude Locations", None))
        self.enable_location.setText(QCoreApplication.translate("MainWindow", u"<---", None))
        self.disable_location.setText(QCoreApplication.translate("MainWindow", u"--->", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Enable Tricks", None))
        self.enable_trick.setText(QCoreApplication.translate("MainWindow", u"<---", None))
        self.disable_trick.setText(QCoreApplication.translate("MainWindow", u"--->", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Logic Settings", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Gossip Stone Hints", None))
        self.label_for_option_hint_distribution.setText(QCoreApplication.translate("MainWindow", u"Hint Distribution", None))
        self.label_for_option_woth_hints.setText(QCoreApplication.translate("MainWindow", u"Way of the Hero Hints", None))
        self.label_for_option_barren_hints.setText(QCoreApplication.translate("MainWindow", u"Barren Hints", None))
        self.label_for_option_sometimes_hints.setText(QCoreApplication.translate("MainWindow", u"Sometimes Hints", None))
        self.label_for_option_location_hints.setText(QCoreApplication.translate("MainWindow", u"Location Hints", None))
        self.label_for_option_item_hints.setText(QCoreApplication.translate("MainWindow", u"Item Hints", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Other Hints", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Song Hints", None))
        self.option_impa_sot_hint.setText(QCoreApplication.translate("MainWindow", u"Impa Stone of Trials Hint", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"Hints", None))
        self.randomize_item.setText(QCoreApplication.translate("MainWindow", u"<--", None))
        self.start_with_item.setText(QCoreApplication.translate("MainWindow", u"-->", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Starting Inventory", None))
        self.permalink_label.setText(QCoreApplication.translate("MainWindow", u"Permalink (copy paste to share your settings)", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_3.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Seed", None))
        self.seed_button.setText(QCoreApplication.translate("MainWindow", u"New Seed", None))
        self.randomize_button.setText(QCoreApplication.translate("MainWindow", u"Randomize", None))
    # retranslateUi

