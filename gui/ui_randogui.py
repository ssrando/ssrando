# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randogui.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListView, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1051, 738)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(9)
        MainWindow.setFont(font)
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
        self.tabWidget.setGeometry(QRect(10, 10, 1031, 541))
        self.tabWidget.setToolTipDuration(-6)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.verticalLayoutWidget_9 = QWidget(self.tab_setup)
        self.verticalLayoutWidget_9.setObjectName(u"verticalLayoutWidget_9")
        self.verticalLayoutWidget_9.setGeometry(QRect(10, 10, 1001, 115))
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

        self.groupBox_12 = QGroupBox(self.tab_setup)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setGeometry(QRect(10, 130, 181, 131))
        self.verticalLayoutWidget_13 = QWidget(self.groupBox_12)
        self.verticalLayoutWidget_13.setObjectName(u"verticalLayoutWidget_13")
        self.verticalLayoutWidget_13.setGeometry(QRect(10, 20, 169, 101))
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

        self.groupBox_13 = QGroupBox(self.tab_setup)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setGeometry(QRect(210, 130, 181, 131))
        self.verticalLayoutWidget_14 = QWidget(self.groupBox_13)
        self.verticalLayoutWidget_14.setObjectName(u"verticalLayoutWidget_14")
        self.verticalLayoutWidget_14.setGeometry(QRect(10, 20, 161, 101))
        self.verticalLayout_34 = QVBoxLayout(self.verticalLayoutWidget_14)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.option_dry_run = QCheckBox(self.verticalLayoutWidget_14)
        self.option_dry_run.setObjectName(u"option_dry_run")

        self.verticalLayout_34.addWidget(self.option_dry_run)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_34.addItem(self.verticalSpacer_14)

        self.groupBox_14 = QGroupBox(self.tab_setup)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.groupBox_14.setGeometry(QRect(410, 130, 181, 131))
        self.verticalLayoutWidget_8 = QWidget(self.groupBox_14)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(10, 20, 161, 101))
        self.verticalLayout_17 = QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.option_tunic_swap = QCheckBox(self.verticalLayoutWidget_8)
        self.option_tunic_swap.setObjectName(u"option_tunic_swap")

        self.verticalLayout_17.addWidget(self.option_tunic_swap)

        self.option_no_enemy_music = QCheckBox(self.verticalLayoutWidget_8)
        self.option_no_enemy_music.setObjectName(u"option_no_enemy_music")

        self.verticalLayout_17.addWidget(self.option_no_enemy_music)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_15)

        self.groupBox_15 = QGroupBox(self.tab_setup)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setGeometry(QRect(610, 130, 181, 131))
        self.verticalLayoutWidget_11 = QWidget(self.groupBox_15)
        self.verticalLayoutWidget_11.setObjectName(u"verticalLayoutWidget_11")
        self.verticalLayoutWidget_11.setGeometry(QRect(10, 20, 161, 106))
        self.verticalLayout_35 = QVBoxLayout(self.verticalLayoutWidget_11)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_36 = QVBoxLayout()
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.label_for_option_music_rando = QLabel(self.verticalLayoutWidget_11)
        self.label_for_option_music_rando.setObjectName(u"label_for_option_music_rando")

        self.verticalLayout_36.addWidget(self.label_for_option_music_rando)

        self.option_music_rando = QComboBox(self.verticalLayoutWidget_11)
        self.option_music_rando.setObjectName(u"option_music_rando")

        self.verticalLayout_36.addWidget(self.option_music_rando)


        self.verticalLayout_35.addLayout(self.verticalLayout_36)

        self.option_cutoff_gameover_music = QCheckBox(self.verticalLayoutWidget_11)
        self.option_cutoff_gameover_music.setObjectName(u"option_cutoff_gameover_music")

        self.verticalLayout_35.addWidget(self.option_cutoff_gameover_music)

        self.option_allow_custom_music = QCheckBox(self.verticalLayoutWidget_11)
        self.option_allow_custom_music.setObjectName(u"option_allow_custom_music")

        self.verticalLayout_35.addWidget(self.option_allow_custom_music)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_35.addItem(self.verticalSpacer_16)

        self.groupBox_17 = QGroupBox(self.tab_setup)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.groupBox_17.setGeometry(QRect(10, 270, 331, 101))
        self.verticalLayoutWidget_16 = QWidget(self.groupBox_17)
        self.verticalLayoutWidget_16.setObjectName(u"verticalLayoutWidget_16")
        self.verticalLayoutWidget_16.setGeometry(QRect(10, 20, 311, 78))
        self.verticalLayout_39 = QVBoxLayout(self.verticalLayoutWidget_16)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.verticalLayoutWidget_16)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_39.addWidget(self.label_7)

        self.presets_list = QComboBox(self.verticalLayoutWidget_16)
        self.presets_list.setObjectName(u"presets_list")

        self.verticalLayout_39.addWidget(self.presets_list)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.load_preset = QPushButton(self.verticalLayoutWidget_16)
        self.load_preset.setObjectName(u"load_preset")

        self.horizontalLayout_12.addWidget(self.load_preset)

        self.save_preset = QPushButton(self.verticalLayoutWidget_16)
        self.save_preset.setObjectName(u"save_preset")

        self.horizontalLayout_12.addWidget(self.save_preset)

        self.delete_preset = QPushButton(self.verticalLayoutWidget_16)
        self.delete_preset.setObjectName(u"delete_preset")

        self.horizontalLayout_12.addWidget(self.delete_preset)


        self.verticalLayout_39.addLayout(self.horizontalLayout_12)

        self.tabWidget.addTab(self.tab_setup, "")
        self.tab_randomization_settings = QWidget()
        self.tab_randomization_settings.setObjectName(u"tab_randomization_settings")
        self.groupBox_5 = QGroupBox(self.tab_randomization_settings)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(210, 0, 191, 501))
        self.verticalLayoutWidget = QWidget(self.groupBox_5)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 19, 171, 471))
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

        self.option_triforce_required = QCheckBox(self.verticalLayoutWidget)
        self.option_triforce_required.setObjectName(u"option_triforce_required")

        self.verticalLayout.addWidget(self.option_triforce_required)

        self.verticalLayout_38 = QVBoxLayout()
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.label_for_option_triforce_shuffle = QLabel(self.verticalLayoutWidget)
        self.label_for_option_triforce_shuffle.setObjectName(u"label_for_option_triforce_shuffle")

        self.verticalLayout_38.addWidget(self.label_for_option_triforce_shuffle)

        self.option_triforce_shuffle = QComboBox(self.verticalLayoutWidget)
        self.option_triforce_shuffle.setObjectName(u"option_triforce_shuffle")

        self.verticalLayout_38.addWidget(self.option_triforce_shuffle)


        self.verticalLayout.addLayout(self.verticalLayout_38)

        self.option_imp_2 = QCheckBox(self.verticalLayoutWidget)
        self.option_imp_2.setObjectName(u"option_imp_2")

        self.verticalLayout.addWidget(self.option_imp_2)

        self.option_horde = QCheckBox(self.verticalLayoutWidget)
        self.option_horde.setObjectName(u"option_horde")

        self.verticalLayout.addWidget(self.option_horde)

        self.option_g3 = QCheckBox(self.verticalLayoutWidget)
        self.option_g3.setObjectName(u"option_g3")

        self.verticalLayout.addWidget(self.option_g3)

        self.option_demise = QCheckBox(self.verticalLayoutWidget)
        self.option_demise.setObjectName(u"option_demise")

        self.verticalLayout.addWidget(self.option_demise)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_for_option_demise_count = QLabel(self.verticalLayoutWidget)
        self.label_for_option_demise_count.setObjectName(u"label_for_option_demise_count")

        self.horizontalLayout_20.addWidget(self.label_for_option_demise_count)

        self.option_demise_count = QSpinBox(self.verticalLayoutWidget)
        self.option_demise_count.setObjectName(u"option_demise_count")
        self.option_demise_count.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_20.addWidget(self.option_demise_count)


        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.groupBox_7 = QGroupBox(self.tab_randomization_settings)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(820, 0, 191, 501))
        self.verticalLayoutWidget_7 = QWidget(self.groupBox_7)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 20, 181, 471))
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

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_for_sword_dungeon_reward = QLabel(self.verticalLayoutWidget_7)
        self.label_for_sword_dungeon_reward.setObjectName(u"label_for_sword_dungeon_reward")

        self.verticalLayout_16.addWidget(self.label_for_sword_dungeon_reward)

        self.option_sword_dungeon_reward = QComboBox(self.verticalLayoutWidget_7)
        self.option_sword_dungeon_reward.setObjectName(u"option_sword_dungeon_reward")

        self.verticalLayout_16.addWidget(self.option_sword_dungeon_reward)


        self.verticalLayout_10.addLayout(self.verticalLayout_16)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_4)

        self.groupBox_2 = QGroupBox(self.tab_randomization_settings)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(410, 0, 191, 501))
        self.verticalLayoutWidget_2 = QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 171, 471))
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

        self.option_open_et = QCheckBox(self.verticalLayoutWidget_2)
        self.option_open_et.setObjectName(u"option_open_et")

        self.verticalLayout_2.addWidget(self.option_open_et)

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

        self.groupBox_6 = QGroupBox(self.tab_randomization_settings)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(610, 0, 201, 501))
        self.verticalLayoutWidget_4 = QWidget(self.groupBox_6)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 19, 186, 471))
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

        self.groupBox_18 = QGroupBox(self.tab_randomization_settings)
        self.groupBox_18.setObjectName(u"groupBox_18")
        self.groupBox_18.setGeometry(QRect(10, 0, 191, 501))
        self.verticalLayoutWidget_17 = QWidget(self.groupBox_18)
        self.verticalLayoutWidget_17.setObjectName(u"verticalLayoutWidget_17")
        self.verticalLayoutWidget_17.setGeometry(QRect(10, 21, 171, 471))
        self.verticalLayout_40 = QVBoxLayout(self.verticalLayoutWidget_17)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.vlay_batreaux = QVBoxLayout()
        self.vlay_batreaux.setObjectName(u"vlay_batreaux")
        self.label_for_option_max_batreaux_reward = QLabel(self.verticalLayoutWidget_17)
        self.label_for_option_max_batreaux_reward.setObjectName(u"label_for_option_max_batreaux_reward")

        self.vlay_batreaux.addWidget(self.label_for_option_max_batreaux_reward)

        self.option_max_batreaux_reward = QComboBox(self.verticalLayoutWidget_17)
        self.option_max_batreaux_reward.setObjectName(u"option_max_batreaux_reward")

        self.vlay_batreaux.addWidget(self.option_max_batreaux_reward)


        self.verticalLayout_40.addLayout(self.vlay_batreaux)

        self.option_peatrice = QCheckBox(self.verticalLayoutWidget_17)
        self.option_peatrice.setObjectName(u"option_peatrice")

        self.verticalLayout_40.addWidget(self.option_peatrice)

        self.option_cubes = QCheckBox(self.verticalLayoutWidget_17)
        self.option_cubes.setObjectName(u"option_cubes")

        self.verticalLayout_40.addWidget(self.option_cubes)

        self.vlay_minigames = QVBoxLayout()
        self.vlay_minigames.setObjectName(u"vlay_minigames")
        self.label_for_option_minigames = QLabel(self.verticalLayoutWidget_17)
        self.label_for_option_minigames.setObjectName(u"label_for_option_minigames")

        self.vlay_minigames.addWidget(self.label_for_option_minigames)

        self.option_minigames = QComboBox(self.verticalLayoutWidget_17)
        self.option_minigames.setObjectName(u"option_minigames")

        self.vlay_minigames.addWidget(self.option_minigames)


        self.verticalLayout_40.addLayout(self.vlay_minigames)

        self.vlay_beedle = QVBoxLayout()
        self.vlay_beedle.setObjectName(u"vlay_beedle")
        self.label_10 = QLabel(self.verticalLayoutWidget_17)
        self.label_10.setObjectName(u"label_10")

        self.vlay_beedle.addWidget(self.label_10)

        self.option_shopsanity = QComboBox(self.verticalLayoutWidget_17)
        self.option_shopsanity.setObjectName(u"option_shopsanity")

        self.vlay_beedle.addWidget(self.option_shopsanity)


        self.verticalLayout_40.addLayout(self.vlay_beedle)

        self.vlay_rupeesanity = QVBoxLayout()
        self.vlay_rupeesanity.setObjectName(u"vlay_rupeesanity")
        self.label_for_option_rupeesanity = QLabel(self.verticalLayoutWidget_17)
        self.label_for_option_rupeesanity.setObjectName(u"label_for_option_rupeesanity")

        self.vlay_rupeesanity.addWidget(self.label_for_option_rupeesanity)

        self.option_rupeesanity = QComboBox(self.verticalLayoutWidget_17)
        self.option_rupeesanity.setObjectName(u"option_rupeesanity")

        self.vlay_rupeesanity.addWidget(self.option_rupeesanity)


        self.verticalLayout_40.addLayout(self.vlay_rupeesanity)

        self.option_soth = QCheckBox(self.verticalLayoutWidget_17)
        self.option_soth.setObjectName(u"option_soth")

        self.verticalLayout_40.addWidget(self.option_soth)

        self.vspace_shuffles = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_40.addItem(self.vspace_shuffles)

        self.tabWidget.addTab(self.tab_randomization_settings, "")
        self.tab_additional_settings = QWidget()
        self.tab_additional_settings.setObjectName(u"tab_additional_settings")
        self.box_convenience_tweaks = QGroupBox(self.tab_additional_settings)
        self.box_convenience_tweaks.setObjectName(u"box_convenience_tweaks")
        self.box_convenience_tweaks.setGeometry(QRect(10, 0, 191, 251))
        self.verticalLayoutWidget_19 = QWidget(self.box_convenience_tweaks)
        self.verticalLayoutWidget_19.setObjectName(u"verticalLayoutWidget_19")
        self.verticalLayoutWidget_19.setGeometry(QRect(10, 20, 176, 221))
        self.vlay_convenience_tweaks = QVBoxLayout(self.verticalLayoutWidget_19)
        self.vlay_convenience_tweaks.setObjectName(u"vlay_convenience_tweaks")
        self.vlay_convenience_tweaks.setContentsMargins(0, 0, 0, 0)
        self.option_fill_dowsing_on_white_sword = QCheckBox(self.verticalLayoutWidget_19)
        self.option_fill_dowsing_on_white_sword.setObjectName(u"option_fill_dowsing_on_white_sword")

        self.vlay_convenience_tweaks.addWidget(self.option_fill_dowsing_on_white_sword)

        self.vspace_convenience_tweaks = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_convenience_tweaks.addItem(self.vspace_convenience_tweaks)

        self.box_vanilla_tweaks = QGroupBox(self.tab_additional_settings)
        self.box_vanilla_tweaks.setObjectName(u"box_vanilla_tweaks")
        self.box_vanilla_tweaks.setGeometry(QRect(210, 0, 191, 251))
        self.verticalLayoutWidget_18 = QWidget(self.box_vanilla_tweaks)
        self.verticalLayoutWidget_18.setObjectName(u"verticalLayoutWidget_18")
        self.verticalLayoutWidget_18.setGeometry(QRect(10, 20, 171, 221))
        self.vlay_vanilla_tweaks = QVBoxLayout(self.verticalLayoutWidget_18)
        self.vlay_vanilla_tweaks.setObjectName(u"vlay_vanilla_tweaks")
        self.vlay_vanilla_tweaks.setContentsMargins(0, 0, 0, 0)
        self.option_fix_bit_crashes = QCheckBox(self.verticalLayoutWidget_18)
        self.option_fix_bit_crashes.setObjectName(u"option_fix_bit_crashes")

        self.vlay_vanilla_tweaks.addWidget(self.option_fix_bit_crashes)

        self.vspace_vanilla_tweaks = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_vanilla_tweaks.addItem(self.vspace_vanilla_tweaks)

        self.box_item_pool = QGroupBox(self.tab_additional_settings)
        self.box_item_pool.setObjectName(u"box_item_pool")
        self.box_item_pool.setGeometry(QRect(410, 0, 191, 251))
        self.verticalLayoutWidget_20 = QWidget(self.box_item_pool)
        self.verticalLayoutWidget_20.setObjectName(u"verticalLayoutWidget_20")
        self.verticalLayoutWidget_20.setGeometry(QRect(10, 20, 171, 221))
        self.vlay_item_pool = QVBoxLayout(self.verticalLayoutWidget_20)
        self.vlay_item_pool.setObjectName(u"vlay_item_pool")
        self.vlay_item_pool.setContentsMargins(0, 0, 0, 0)
        self.vlay_rupoor_mode = QVBoxLayout()
        self.vlay_rupoor_mode.setObjectName(u"vlay_rupoor_mode")
        self.option_gondo_upgrades = QCheckBox(self.verticalLayoutWidget_20)
        self.option_gondo_upgrades.setObjectName(u"option_gondo_upgrades")

        self.vlay_rupoor_mode.addWidget(self.option_gondo_upgrades)

        self.label_for_option_rupoor_mode = QLabel(self.verticalLayoutWidget_20)
        self.label_for_option_rupoor_mode.setObjectName(u"label_for_option_rupoor_mode")

        self.vlay_rupoor_mode.addWidget(self.label_for_option_rupoor_mode)

        self.option_rupoor_mode = QComboBox(self.verticalLayoutWidget_20)
        self.option_rupoor_mode.setObjectName(u"option_rupoor_mode")

        self.vlay_rupoor_mode.addWidget(self.option_rupoor_mode)

        self.vspace_item_pool = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_rupoor_mode.addItem(self.vspace_item_pool)


        self.vlay_item_pool.addLayout(self.vlay_rupoor_mode)

        self.box_silent_realms = QGroupBox(self.tab_additional_settings)
        self.box_silent_realms.setObjectName(u"box_silent_realms")
        self.box_silent_realms.setGeometry(QRect(610, 0, 191, 251))
        self.verticalLayoutWidget_22 = QWidget(self.box_silent_realms)
        self.verticalLayoutWidget_22.setObjectName(u"verticalLayoutWidget_22")
        self.verticalLayoutWidget_22.setGeometry(QRect(9, 19, 171, 221))
        self.vlay_silent_realms = QVBoxLayout(self.verticalLayoutWidget_22)
        self.vlay_silent_realms.setObjectName(u"vlay_silent_realms")
        self.vlay_silent_realms.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_trialshuffle = QVBoxLayout()
        self.verticalLayout_trialshuffle.setObjectName(u"verticalLayout_trialshuffle")
        self.label_4 = QLabel(self.verticalLayoutWidget_22)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_trialshuffle.addWidget(self.label_4)

        self.option_shuffle_trial_objects = QComboBox(self.verticalLayoutWidget_22)
        self.option_shuffle_trial_objects.setObjectName(u"option_shuffle_trial_objects")

        self.verticalLayout_trialshuffle.addWidget(self.option_shuffle_trial_objects)


        self.vlay_silent_realms.addLayout(self.verticalLayout_trialshuffle)

        self.vspace_silent_realms = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_silent_realms.addItem(self.vspace_silent_realms)

        self.tabWidget.addTab(self.tab_additional_settings, "")
        self.tab_logic_settings = QWidget()
        self.tab_logic_settings.setObjectName(u"tab_logic_settings")
        self.layoutWidget = QWidget(self.tab_logic_settings)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 1001, 499))
        self.verticalLayout_18 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_for_option_logic_mode = QLabel(self.layoutWidget)
        self.label_for_option_logic_mode.setObjectName(u"label_for_option_logic_mode")

        self.horizontalLayout_9.addWidget(self.label_for_option_logic_mode)

        self.option_logic_mode = QComboBox(self.layoutWidget)
        self.option_logic_mode.setObjectName(u"option_logic_mode")

        self.horizontalLayout_9.addWidget(self.option_logic_mode)

        self.option_hero_mode = QCheckBox(self.layoutWidget)
        self.option_hero_mode.setObjectName(u"option_hero_mode")

        self.horizontalLayout_9.addWidget(self.option_hero_mode)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)


        self.verticalLayout_18.addLayout(self.horizontalLayout_9)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_19.addWidget(self.label)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.included_locations = QListView(self.layoutWidget)
        self.included_locations.setObjectName(u"included_locations")

        self.horizontalLayout_17.addWidget(self.included_locations)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.include_location = QPushButton(self.layoutWidget)
        self.include_location.setObjectName(u"include_location")

        self.verticalLayout_20.addWidget(self.include_location)

        self.exclude_location = QPushButton(self.layoutWidget)
        self.exclude_location.setObjectName(u"exclude_location")

        self.verticalLayout_20.addWidget(self.exclude_location)


        self.horizontalLayout_17.addLayout(self.verticalLayout_20)

        self.excluded_locations = QListView(self.layoutWidget)
        self.excluded_locations.setObjectName(u"excluded_locations")

        self.horizontalLayout_17.addWidget(self.excluded_locations)


        self.verticalLayout_19.addLayout(self.horizontalLayout_17)


        self.verticalLayout_18.addLayout(self.verticalLayout_19)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_25.addWidget(self.label_5)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.disabled_tricks = QListView(self.layoutWidget)
        self.disabled_tricks.setObjectName(u"disabled_tricks")

        self.horizontalLayout_18.addWidget(self.disabled_tricks)

        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.disable_trick = QPushButton(self.layoutWidget)
        self.disable_trick.setObjectName(u"disable_trick")

        self.verticalLayout_21.addWidget(self.disable_trick)

        self.enable_trick = QPushButton(self.layoutWidget)
        self.enable_trick.setObjectName(u"enable_trick")

        self.verticalLayout_21.addWidget(self.enable_trick)


        self.horizontalLayout_18.addLayout(self.verticalLayout_21)

        self.enabled_tricks = QListView(self.layoutWidget)
        self.enabled_tricks.setObjectName(u"enabled_tricks")

        self.horizontalLayout_18.addWidget(self.enabled_tricks)


        self.verticalLayout_25.addLayout(self.horizontalLayout_18)


        self.verticalLayout_18.addLayout(self.verticalLayout_25)

        self.tabWidget.addTab(self.tab_logic_settings, "")
        self.tab_hints = QWidget()
        self.tab_hints.setObjectName(u"tab_hints")
        self.groupBox_10 = QGroupBox(self.tab_hints)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setGeometry(QRect(10, 10, 191, 231))
        self.verticalLayoutWidget_12 = QWidget(self.groupBox_10)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(10, 20, 175, 207))
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

        self.option_cube_sots = QCheckBox(self.verticalLayoutWidget_12)
        self.option_cube_sots.setObjectName(u"option_cube_sots")

        self.verticalLayout_22.addWidget(self.option_cube_sots)

        self.option_precise_item = QCheckBox(self.verticalLayoutWidget_12)
        self.option_precise_item.setObjectName(u"option_precise_item")

        self.verticalLayout_22.addWidget(self.option_precise_item)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_22.addItem(self.verticalSpacer_11)

        self.groupBox_11 = QGroupBox(self.tab_hints)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.groupBox_11.setGeometry(QRect(210, 10, 191, 231))
        self.verticalLayoutWidget_6 = QWidget(self.groupBox_11)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 20, 174, 201))
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

        self.verticalLayout_42 = QVBoxLayout()
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.label_for_option_chest_dowsing = QLabel(self.verticalLayoutWidget_6)
        self.label_for_option_chest_dowsing.setObjectName(u"label_for_option_chest_dowsing")

        self.verticalLayout_42.addWidget(self.label_for_option_chest_dowsing)

        self.option_chest_dowsing = QComboBox(self.verticalLayoutWidget_6)
        self.option_chest_dowsing.setObjectName(u"option_chest_dowsing")

        self.verticalLayout_42.addWidget(self.option_chest_dowsing)


        self.verticalLayout_26.addLayout(self.verticalLayout_42)

        self.option_dungeon_dowsing = QCheckBox(self.verticalLayoutWidget_6)
        self.option_dungeon_dowsing.setObjectName(u"option_dungeon_dowsing")

        self.verticalLayout_26.addWidget(self.option_dungeon_dowsing)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_26.addItem(self.verticalSpacer_10)

        self.tabWidget.addTab(self.tab_hints, "")
        self.tab_starting_items = QWidget()
        self.tab_starting_items.setObjectName(u"tab_starting_items")
        self.verticalLayoutWidget_201 = QWidget(self.tab_starting_items)
        self.verticalLayoutWidget_201.setObjectName(u"verticalLayoutWidget_201")
        self.verticalLayoutWidget_201.setGeometry(QRect(10, 10, 1001, 501))
        self.verticalLayout_49 = QVBoxLayout(self.verticalLayoutWidget_201)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.verticalLayout_49.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.verticalLayout_50 = QVBoxLayout()
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.label_randomized_items = QLabel(self.verticalLayoutWidget_201)
        self.label_randomized_items.setObjectName(u"label_randomized_items")

        self.verticalLayout_50.addWidget(self.label_randomized_items)

        self.randomized_items = QListView(self.verticalLayoutWidget_201)
        self.randomized_items.setObjectName(u"randomized_items")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.randomized_items.sizePolicy().hasHeightForWidth())
        self.randomized_items.setSizePolicy(sizePolicy3)

        self.verticalLayout_50.addWidget(self.randomized_items)


        self.horizontalLayout_26.addLayout(self.verticalLayout_50)

        self.verticalLayout_51 = QVBoxLayout()
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_51.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_51.addItem(self.verticalSpacer_20)

        self.randomize_item = QPushButton(self.verticalLayoutWidget_201)
        self.randomize_item.setObjectName(u"randomize_item")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.randomize_item.sizePolicy().hasHeightForWidth())
        self.randomize_item.setSizePolicy(sizePolicy4)

        self.verticalLayout_51.addWidget(self.randomize_item)

        self.start_with_item = QPushButton(self.verticalLayoutWidget_201)
        self.start_with_item.setObjectName(u"start_with_item")
        sizePolicy4.setHeightForWidth(self.start_with_item.sizePolicy().hasHeightForWidth())
        self.start_with_item.setSizePolicy(sizePolicy4)

        self.verticalLayout_51.addWidget(self.start_with_item)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_51.addItem(self.verticalSpacer_21)


        self.horizontalLayout_26.addLayout(self.verticalLayout_51)

        self.verticalLayout_52 = QVBoxLayout()
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.label_starting_items = QLabel(self.verticalLayoutWidget_201)
        self.label_starting_items.setObjectName(u"label_starting_items")

        self.verticalLayout_52.addWidget(self.label_starting_items)

        self.starting_items = QListView(self.verticalLayoutWidget_201)
        self.starting_items.setObjectName(u"starting_items")
        sizePolicy3.setHeightForWidth(self.starting_items.sizePolicy().hasHeightForWidth())
        self.starting_items.setSizePolicy(sizePolicy3)

        self.verticalLayout_52.addWidget(self.starting_items)


        self.horizontalLayout_26.addLayout(self.verticalLayout_52)


        self.verticalLayout_49.addLayout(self.horizontalLayout_26)

        self.line = QFrame(self.verticalLayoutWidget_201)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_49.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_49.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_for_option_starting_sword = QLabel(self.verticalLayoutWidget_201)
        self.label_for_option_starting_sword.setObjectName(u"label_for_option_starting_sword")

        self.horizontalLayout_5.addWidget(self.label_for_option_starting_sword)

        self.option_starting_sword = QComboBox(self.verticalLayoutWidget_201)
        self.option_starting_sword.setObjectName(u"option_starting_sword")

        self.horizontalLayout_5.addWidget(self.option_starting_sword)


        self.horizontalLayout_27.addLayout(self.horizontalLayout_5)

        self.option_random_starting_item = QCheckBox(self.verticalLayoutWidget_201)
        self.option_random_starting_item.setObjectName(u"option_random_starting_item")
        sizePolicy2.setHeightForWidth(self.option_random_starting_item.sizePolicy().hasHeightForWidth())
        self.option_random_starting_item.setSizePolicy(sizePolicy2)

        self.horizontalLayout_27.addWidget(self.option_random_starting_item)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_for_option_starting_heart_containers = QLabel(self.verticalLayoutWidget_201)
        self.label_for_option_starting_heart_containers.setObjectName(u"label_for_option_starting_heart_containers")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_for_option_starting_heart_containers.sizePolicy().hasHeightForWidth())
        self.label_for_option_starting_heart_containers.setSizePolicy(sizePolicy5)

        self.horizontalLayout_28.addWidget(self.label_for_option_starting_heart_containers)

        self.option_starting_heart_containers = QSpinBox(self.verticalLayoutWidget_201)
        self.option_starting_heart_containers.setObjectName(u"option_starting_heart_containers")
        sizePolicy2.setHeightForWidth(self.option_starting_heart_containers.sizePolicy().hasHeightForWidth())
        self.option_starting_heart_containers.setSizePolicy(sizePolicy2)
        self.option_starting_heart_containers.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_28.addWidget(self.option_starting_heart_containers)


        self.horizontalLayout_27.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_for_option_starting_heart_pieces = QLabel(self.verticalLayoutWidget_201)
        self.label_for_option_starting_heart_pieces.setObjectName(u"label_for_option_starting_heart_pieces")
        sizePolicy5.setHeightForWidth(self.label_for_option_starting_heart_pieces.sizePolicy().hasHeightForWidth())
        self.label_for_option_starting_heart_pieces.setSizePolicy(sizePolicy5)

        self.horizontalLayout_29.addWidget(self.label_for_option_starting_heart_pieces)

        self.option_starting_heart_pieces = QSpinBox(self.verticalLayoutWidget_201)
        self.option_starting_heart_pieces.setObjectName(u"option_starting_heart_pieces")
        sizePolicy2.setHeightForWidth(self.option_starting_heart_pieces.sizePolicy().hasHeightForWidth())
        self.option_starting_heart_pieces.setSizePolicy(sizePolicy2)
        self.option_starting_heart_pieces.setMaximumSize(QSize(41, 16777215))

        self.horizontalLayout_29.addWidget(self.option_starting_heart_pieces)


        self.horizontalLayout_27.addLayout(self.horizontalLayout_29)

        self.label_current_starting_health = QLabel(self.verticalLayoutWidget_201)
        self.label_current_starting_health.setObjectName(u"label_current_starting_health")

        self.horizontalLayout_27.addWidget(self.label_current_starting_health)

        self.current_starting_health_counter = QLabel(self.verticalLayoutWidget_201)
        self.current_starting_health_counter.setObjectName(u"current_starting_health_counter")

        self.horizontalLayout_27.addWidget(self.current_starting_health_counter)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_3)


        self.verticalLayout_49.addLayout(self.horizontalLayout_27)

        self.tabWidget.addTab(self.tab_starting_items, "")
        self.verticalLayoutWidget_10 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_10.setObjectName(u"verticalLayoutWidget_10")
        self.verticalLayoutWidget_10.setGeometry(QRect(10, 615, 1031, 110))
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

        self.tabWidget.setCurrentIndex(1)
        self.option_triforce_shuffle.setCurrentIndex(-1)
        self.option_randomize_entrances.setCurrentIndex(-1)
        self.option_chest_dowsing.setCurrentIndex(-1)


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
        self.option_no_enemy_music.setText(QCoreApplication.translate("MainWindow", u"Remove Enemy Music", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("MainWindow", u"Randomize Music", None))
        self.label_for_option_music_rando.setText(QCoreApplication.translate("MainWindow", u"Randomize Music", None))
        self.option_cutoff_gameover_music.setText(QCoreApplication.translate("MainWindow", u"Cutoff Game Over Music", None))
        self.option_allow_custom_music.setText(QCoreApplication.translate("MainWindow", u"Allow Custom Music", None))
        self.groupBox_17.setTitle(QCoreApplication.translate("MainWindow", u"Presets", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Presets overwrite ALL game settings", None))
        self.load_preset.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.save_preset.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.delete_preset.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setup), QCoreApplication.translate("MainWindow", u"Setup", None))
#if QT_CONFIG(tooltip)
        self.tab_randomization_settings.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Completion Conditions", None))
        self.label_for_option_got_starting_state.setText(QCoreApplication.translate("MainWindow", u"Starting State", None))
        self.label_for_option_got_sword_requirement.setText(QCoreApplication.translate("MainWindow", u"Sword Requirement", None))
        self.label_for_option_got_dungeon_requirement.setText(QCoreApplication.translate("MainWindow", u"Dungeon Requirement", None))
        self.label_for_option_required_dungeon_count.setText(QCoreApplication.translate("MainWindow", u"Required Dungeons", None))
        self.option_triforce_required.setText(QCoreApplication.translate("MainWindow", u"Triforce Required", None))
        self.label_for_option_triforce_shuffle.setText(QCoreApplication.translate("MainWindow", u"Triforce Shuffle", None))
        self.option_triforce_shuffle.setCurrentText("")
        self.option_imp_2.setText(QCoreApplication.translate("MainWindow", u"Skip Imprisoned 2", None))
        self.option_horde.setText(QCoreApplication.translate("MainWindow", u"Skip Horde", None))
        self.option_g3.setText(QCoreApplication.translate("MainWindow", u"Skip Ghirahim 3", None))
        self.option_demise.setText(QCoreApplication.translate("MainWindow", u"Skip Demise", None))
        self.label_for_option_demise_count.setText(QCoreApplication.translate("MainWindow", u"Demise Count", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.label_for_option_map_mode.setText(QCoreApplication.translate("MainWindow", u"Map Mode", None))
        self.label_for_option_small_key_mode.setText(QCoreApplication.translate("MainWindow", u"Small Keys", None))
        self.label_for_option_boss_key_mode.setText(QCoreApplication.translate("MainWindow", u"Boss Keys", None))
        self.option_empty_unrequired_dungeons.setText(QCoreApplication.translate("MainWindow", u"Empty Unrequired Dungeons", None))
        self.label_for_sword_dungeon_reward.setText(QCoreApplication.translate("MainWindow", u"Sword Dungeon Reward", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Open Settings", None))
        self.label_for_option_open_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Open Thunderhead", None))
        self.option_open_et.setText(QCoreApplication.translate("MainWindow", u"Open Earth Temple", None))
        self.label_for_option_open_lmf.setText(QCoreApplication.translate("MainWindow", u"Open Lanayru Mining Facility", None))
        self.label_for_option_starting_tablet_count.setText(QCoreApplication.translate("MainWindow", u"Starting Tablets", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Entrance Randomization", None))
        self.label_for_option_randomize_entrances.setText(QCoreApplication.translate("MainWindow", u"Randomize Dungeon Entrances", None))
        self.option_randomize_entrances.setCurrentText("")
        self.option_randomize_trials.setText(QCoreApplication.translate("MainWindow", u"Randomize Silent Realm Gates", None))
        self.groupBox_18.setTitle(QCoreApplication.translate("MainWindow", u"Shuffles", None))
        self.label_for_option_max_batreaux_reward.setText(QCoreApplication.translate("MainWindow", u"Batreaux", None))
        self.option_peatrice.setText(QCoreApplication.translate("MainWindow", u"Peatrice", None))
        self.option_cubes.setText(QCoreApplication.translate("MainWindow", u"Goddess Cubes", None))
        self.label_for_option_minigames.setText(QCoreApplication.translate("MainWindow", u"Minigames", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Beedle's Shop", None))
        self.label_for_option_rupeesanity.setText(QCoreApplication.translate("MainWindow", u"Rupeesanity", None))
        self.option_soth.setText(QCoreApplication.translate("MainWindow", u"Song of the Hero Quest", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_randomization_settings), QCoreApplication.translate("MainWindow", u"Randomization Settings", None))
        self.box_convenience_tweaks.setTitle(QCoreApplication.translate("MainWindow", u"Convenience Tweaks", None))
        self.option_fill_dowsing_on_white_sword.setText(QCoreApplication.translate("MainWindow", u"Fill Dowsing on White Sword", None))
        self.box_vanilla_tweaks.setTitle(QCoreApplication.translate("MainWindow", u"Vanilla Tweaks", None))
        self.option_fix_bit_crashes.setText(QCoreApplication.translate("MainWindow", u"Fix BiT crashes", None))
        self.box_item_pool.setTitle(QCoreApplication.translate("MainWindow", u"Item Pool", None))
        self.option_gondo_upgrades.setText(QCoreApplication.translate("MainWindow", u"Place Scrap Shop Upgrades", None))
        self.label_for_option_rupoor_mode.setText(QCoreApplication.translate("MainWindow", u"Rupoor Mode", None))
        self.box_silent_realms.setTitle(QCoreApplication.translate("MainWindow", u"Silent Realms", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Shuffle Trial Objects", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_additional_settings), QCoreApplication.translate("MainWindow", u"Additional Settings", None))
        self.label_for_option_logic_mode.setText(QCoreApplication.translate("MainWindow", u"Logic Mode", None))
        self.option_hero_mode.setText(QCoreApplication.translate("MainWindow", u"Hero Mode", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Exclude Locations", None))
        self.include_location.setText(QCoreApplication.translate("MainWindow", u"Include\n"
"<--", None))
        self.exclude_location.setText(QCoreApplication.translate("MainWindow", u"Exclude\n"
"-->", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Enable Tricks", None))
#if QT_CONFIG(tooltip)
        self.disabled_tricks.setToolTip(QCoreApplication.translate("MainWindow", u"test", None))
#endif // QT_CONFIG(tooltip)
        self.disable_trick.setText(QCoreApplication.translate("MainWindow", u"Disable\n"
"<--", None))
        self.enable_trick.setText(QCoreApplication.translate("MainWindow", u"Enable\n"
"-->", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logic_settings), QCoreApplication.translate("MainWindow", u"Logic Settings", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Gossip Stone Hints", None))
        self.label_for_option_hint_distribution.setText(QCoreApplication.translate("MainWindow", u"Hint Distribution", None))
        self.option_cube_sots.setText(QCoreApplication.translate("MainWindow", u"Separate Cube SotS Hints", None))
        self.option_precise_item.setText(QCoreApplication.translate("MainWindow", u"Precise Item Hints", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Other Hints", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Song Hints", None))
        self.option_impa_sot_hint.setText(QCoreApplication.translate("MainWindow", u"Impa Stone of Trials Hint", None))
        self.label_for_option_chest_dowsing.setText(QCoreApplication.translate("MainWindow", u"Chest Dowsing", None))
        self.option_chest_dowsing.setCurrentText("")
        self.option_dungeon_dowsing.setText(QCoreApplication.translate("MainWindow", u"Allow Dowsing in Dungeons", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_hints), QCoreApplication.translate("MainWindow", u"Hints", None))
        self.label_randomized_items.setText(QCoreApplication.translate("MainWindow", u"Randomized Items", None))
        self.randomize_item.setText(QCoreApplication.translate("MainWindow", u"Remove\n"
"<--", None))
        self.start_with_item.setText(QCoreApplication.translate("MainWindow", u"Add\n"
"-->", None))
        self.label_starting_items.setText(QCoreApplication.translate("MainWindow", u"Starting Items", None))
        self.label_for_option_starting_sword.setText(QCoreApplication.translate("MainWindow", u"Starting Sword", None))
        self.option_random_starting_item.setText(QCoreApplication.translate("MainWindow", u"Start with Random Progress Item", None))
        self.label_for_option_starting_heart_containers.setText(QCoreApplication.translate("MainWindow", u"Heart Containers", None))
        self.label_for_option_starting_heart_pieces.setText(QCoreApplication.translate("MainWindow", u"Heart Pieces", None))
        self.label_current_starting_health.setText(QCoreApplication.translate("MainWindow", u"Current Starting Health:", None))
        self.current_starting_health_counter.setText(QCoreApplication.translate("MainWindow", u"6 hearts", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_starting_items), QCoreApplication.translate("MainWindow", u"Starting Items", None))
        self.permalink_label.setText(QCoreApplication.translate("MainWindow", u"Settings String", None))
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

