# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randogui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
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
        self.option_description.setGeometry(QRect(10, 570, 1031, 31))
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
        self.vlay_files = QVBoxLayout(self.verticalLayoutWidget_9)
        self.vlay_files.setObjectName(u"vlay_files")
        self.vlay_files.setContentsMargins(0, 0, 0, 0)
        self.hlay_output = QHBoxLayout()
        self.hlay_output.setObjectName(u"hlay_output")
        self.label_output = QLabel(self.verticalLayoutWidget_9)
        self.label_output.setObjectName(u"label_output")
        self.label_output.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.hlay_output.addWidget(self.label_output)

        self.output_folder = QLineEdit(self.verticalLayoutWidget_9)
        self.output_folder.setObjectName(u"output_folder")

        self.hlay_output.addWidget(self.output_folder)

        self.ouput_folder_browse_button = QPushButton(self.verticalLayoutWidget_9)
        self.ouput_folder_browse_button.setObjectName(u"ouput_folder_browse_button")

        self.hlay_output.addWidget(self.ouput_folder_browse_button)


        self.vlay_files.addLayout(self.hlay_output)

        self.vlay_plando = QVBoxLayout()
        self.vlay_plando.setObjectName(u"vlay_plando")
        self.option_plando = QCheckBox(self.verticalLayoutWidget_9)
        self.option_plando.setObjectName(u"option_plando")

        self.vlay_plando.addWidget(self.option_plando)

        self.hlay_plando_file = QHBoxLayout()
        self.hlay_plando_file.setObjectName(u"hlay_plando_file")
        self.plando_file = QLineEdit(self.verticalLayoutWidget_9)
        self.plando_file.setObjectName(u"plando_file")

        self.hlay_plando_file.addWidget(self.plando_file)

        self.plando_file_browse = QPushButton(self.verticalLayoutWidget_9)
        self.plando_file_browse.setObjectName(u"plando_file_browse")

        self.hlay_plando_file.addWidget(self.plando_file_browse)


        self.vlay_plando.addLayout(self.hlay_plando_file)


        self.vlay_files.addLayout(self.vlay_plando)

        self.vspace_files = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_files.addItem(self.vspace_files)

        self.box_additional_files = QGroupBox(self.tab_setup)
        self.box_additional_files.setObjectName(u"box_additional_files")
        self.box_additional_files.setGeometry(QRect(10, 130, 181, 131))
        self.verticalLayoutWidget_13 = QWidget(self.box_additional_files)
        self.verticalLayoutWidget_13.setObjectName(u"verticalLayoutWidget_13")
        self.verticalLayoutWidget_13.setGeometry(QRect(10, 20, 169, 101))
        self.vlay_additional_files = QVBoxLayout(self.verticalLayoutWidget_13)
        self.vlay_additional_files.setObjectName(u"vlay_additional_files")
        self.vlay_additional_files.setContentsMargins(0, 0, 0, 0)
        self.option_no_spoiler_log = QCheckBox(self.verticalLayoutWidget_13)
        self.option_no_spoiler_log.setObjectName(u"option_no_spoiler_log")

        self.vlay_additional_files.addWidget(self.option_no_spoiler_log)

        self.option_json_spoiler = QCheckBox(self.verticalLayoutWidget_13)
        self.option_json_spoiler.setObjectName(u"option_json_spoiler")

        self.vlay_additional_files.addWidget(self.option_json_spoiler)

        self.option_out_placement_file = QCheckBox(self.verticalLayoutWidget_13)
        self.option_out_placement_file.setObjectName(u"option_out_placement_file")

        self.vlay_additional_files.addWidget(self.option_out_placement_file)

        self.vspace_additional_files = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_additional_files.addItem(self.vspace_additional_files)

        self.box_advanced = QGroupBox(self.tab_setup)
        self.box_advanced.setObjectName(u"box_advanced")
        self.box_advanced.setGeometry(QRect(210, 130, 181, 131))
        self.verticalLayoutWidget_14 = QWidget(self.box_advanced)
        self.verticalLayoutWidget_14.setObjectName(u"verticalLayoutWidget_14")
        self.verticalLayoutWidget_14.setGeometry(QRect(10, 20, 161, 101))
        self.vlay_advanced = QVBoxLayout(self.verticalLayoutWidget_14)
        self.vlay_advanced.setObjectName(u"vlay_advanced")
        self.vlay_advanced.setContentsMargins(0, 0, 0, 0)
        self.option_dry_run = QCheckBox(self.verticalLayoutWidget_14)
        self.option_dry_run.setObjectName(u"option_dry_run")

        self.vlay_advanced.addWidget(self.option_dry_run)

        self.vspace_advanced = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_advanced.addItem(self.vspace_advanced)

        self.box_cosmetics = QGroupBox(self.tab_setup)
        self.box_cosmetics.setObjectName(u"box_cosmetics")
        self.box_cosmetics.setGeometry(QRect(410, 130, 181, 131))
        self.verticalLayoutWidget_8 = QWidget(self.box_cosmetics)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(10, 20, 161, 101))
        self.vlay_cosmetics = QVBoxLayout(self.verticalLayoutWidget_8)
        self.vlay_cosmetics.setObjectName(u"vlay_cosmetics")
        self.vlay_cosmetics.setContentsMargins(0, 0, 0, 0)
        self.option_tunic_swap = QCheckBox(self.verticalLayoutWidget_8)
        self.option_tunic_swap.setObjectName(u"option_tunic_swap")

        self.vlay_cosmetics.addWidget(self.option_tunic_swap)

        self.option_no_enemy_music = QCheckBox(self.verticalLayoutWidget_8)
        self.option_no_enemy_music.setObjectName(u"option_no_enemy_music")

        self.vlay_cosmetics.addWidget(self.option_no_enemy_music)

        self.vspace_cosmetics = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_cosmetics.addItem(self.vspace_cosmetics)

        self.box_music_rando = QGroupBox(self.tab_setup)
        self.box_music_rando.setObjectName(u"box_music_rando")
        self.box_music_rando.setGeometry(QRect(610, 130, 181, 131))
        self.verticalLayoutWidget_11 = QWidget(self.box_music_rando)
        self.verticalLayoutWidget_11.setObjectName(u"verticalLayoutWidget_11")
        self.verticalLayoutWidget_11.setGeometry(QRect(10, 20, 161, 106))
        self.vlay_music_rando = QVBoxLayout(self.verticalLayoutWidget_11)
        self.vlay_music_rando.setObjectName(u"vlay_music_rando")
        self.vlay_music_rando.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_36 = QVBoxLayout()
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.label_for_option_music_rando = QLabel(self.verticalLayoutWidget_11)
        self.label_for_option_music_rando.setObjectName(u"label_for_option_music_rando")

        self.verticalLayout_36.addWidget(self.label_for_option_music_rando)

        self.option_music_rando = QComboBox(self.verticalLayoutWidget_11)
        self.option_music_rando.setObjectName(u"option_music_rando")

        self.verticalLayout_36.addWidget(self.option_music_rando)


        self.vlay_music_rando.addLayout(self.verticalLayout_36)

        self.option_cutoff_gameover_music = QCheckBox(self.verticalLayoutWidget_11)
        self.option_cutoff_gameover_music.setObjectName(u"option_cutoff_gameover_music")

        self.vlay_music_rando.addWidget(self.option_cutoff_gameover_music)

        self.option_allow_custom_music = QCheckBox(self.verticalLayoutWidget_11)
        self.option_allow_custom_music.setObjectName(u"option_allow_custom_music")

        self.vlay_music_rando.addWidget(self.option_allow_custom_music)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_music_rando.addItem(self.verticalSpacer_16)

        self.box_presets = QGroupBox(self.tab_setup)
        self.box_presets.setObjectName(u"box_presets")
        self.box_presets.setGeometry(QRect(10, 270, 331, 101))
        self.verticalLayoutWidget_16 = QWidget(self.box_presets)
        self.verticalLayoutWidget_16.setObjectName(u"verticalLayoutWidget_16")
        self.verticalLayoutWidget_16.setGeometry(QRect(10, 20, 311, 78))
        self.vlay_presets = QVBoxLayout(self.verticalLayoutWidget_16)
        self.vlay_presets.setObjectName(u"vlay_presets")
        self.vlay_presets.setContentsMargins(0, 0, 0, 0)
        self.label_presets = QLabel(self.verticalLayoutWidget_16)
        self.label_presets.setObjectName(u"label_presets")

        self.vlay_presets.addWidget(self.label_presets)

        self.presets_list = QComboBox(self.verticalLayoutWidget_16)
        self.presets_list.setObjectName(u"presets_list")

        self.vlay_presets.addWidget(self.presets_list)

        self.hlay_presets_controls = QHBoxLayout()
        self.hlay_presets_controls.setObjectName(u"hlay_presets_controls")
        self.load_preset = QPushButton(self.verticalLayoutWidget_16)
        self.load_preset.setObjectName(u"load_preset")

        self.hlay_presets_controls.addWidget(self.load_preset)

        self.save_preset = QPushButton(self.verticalLayoutWidget_16)
        self.save_preset.setObjectName(u"save_preset")

        self.hlay_presets_controls.addWidget(self.save_preset)

        self.delete_preset = QPushButton(self.verticalLayoutWidget_16)
        self.delete_preset.setObjectName(u"delete_preset")

        self.hlay_presets_controls.addWidget(self.delete_preset)


        self.vlay_presets.addLayout(self.hlay_presets_controls)

        self.tabWidget.addTab(self.tab_setup, "")
        self.tab_randomization_settings = QWidget()
        self.tab_randomization_settings.setObjectName(u"tab_randomization_settings")
        self.box_completion = QGroupBox(self.tab_randomization_settings)
        self.box_completion.setObjectName(u"box_completion")
        self.box_completion.setGeometry(QRect(210, 0, 191, 501))
        self.verticalLayoutWidget = QWidget(self.box_completion)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 19, 171, 471))
        self.vlay_completion = QVBoxLayout(self.verticalLayoutWidget)
        self.vlay_completion.setObjectName(u"vlay_completion")
        self.vlay_completion.setContentsMargins(0, 0, 0, 0)
        self.vlay_got_start = QVBoxLayout()
        self.vlay_got_start.setObjectName(u"vlay_got_start")
        self.label_for_option_got_starting_state = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_starting_state.setObjectName(u"label_for_option_got_starting_state")

        self.vlay_got_start.addWidget(self.label_for_option_got_starting_state)

        self.option_got_starting_state = QComboBox(self.verticalLayoutWidget)
        self.option_got_starting_state.setObjectName(u"option_got_starting_state")

        self.vlay_got_start.addWidget(self.option_got_starting_state)


        self.vlay_completion.addLayout(self.vlay_got_start)

        self.vlay_sword_req = QVBoxLayout()
        self.vlay_sword_req.setObjectName(u"vlay_sword_req")
        self.label_for_option_got_sword_requirement = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_sword_requirement.setObjectName(u"label_for_option_got_sword_requirement")

        self.vlay_sword_req.addWidget(self.label_for_option_got_sword_requirement)

        self.option_got_sword_requirement = QComboBox(self.verticalLayoutWidget)
        self.option_got_sword_requirement.setObjectName(u"option_got_sword_requirement")

        self.vlay_sword_req.addWidget(self.option_got_sword_requirement)


        self.vlay_completion.addLayout(self.vlay_sword_req)

        self.vlay_got_dungeon_req = QVBoxLayout()
        self.vlay_got_dungeon_req.setObjectName(u"vlay_got_dungeon_req")
        self.label_for_option_got_dungeon_requirement = QLabel(self.verticalLayoutWidget)
        self.label_for_option_got_dungeon_requirement.setObjectName(u"label_for_option_got_dungeon_requirement")

        self.vlay_got_dungeon_req.addWidget(self.label_for_option_got_dungeon_requirement)

        self.option_got_dungeon_requirement = QComboBox(self.verticalLayoutWidget)
        self.option_got_dungeon_requirement.setObjectName(u"option_got_dungeon_requirement")

        self.vlay_got_dungeon_req.addWidget(self.option_got_dungeon_requirement)


        self.vlay_completion.addLayout(self.vlay_got_dungeon_req)

        self.hlay_req_dungeons = QHBoxLayout()
        self.hlay_req_dungeons.setObjectName(u"hlay_req_dungeons")
        self.label_for_option_required_dungeon_count = QLabel(self.verticalLayoutWidget)
        self.label_for_option_required_dungeon_count.setObjectName(u"label_for_option_required_dungeon_count")

        self.hlay_req_dungeons.addWidget(self.label_for_option_required_dungeon_count)

        self.option_required_dungeon_count = QSpinBox(self.verticalLayoutWidget)
        self.option_required_dungeon_count.setObjectName(u"option_required_dungeon_count")
        self.option_required_dungeon_count.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.option_required_dungeon_count.sizePolicy().hasHeightForWidth())
        self.option_required_dungeon_count.setSizePolicy(sizePolicy2)
        self.option_required_dungeon_count.setMaximumSize(QSize(41, 16777215))

        self.hlay_req_dungeons.addWidget(self.option_required_dungeon_count)


        self.vlay_completion.addLayout(self.hlay_req_dungeons)

        self.option_triforce_required = QCheckBox(self.verticalLayoutWidget)
        self.option_triforce_required.setObjectName(u"option_triforce_required")

        self.vlay_completion.addWidget(self.option_triforce_required)

        self.vlay_triforce_shuffle = QVBoxLayout()
        self.vlay_triforce_shuffle.setObjectName(u"vlay_triforce_shuffle")
        self.label_for_option_triforce_shuffle = QLabel(self.verticalLayoutWidget)
        self.label_for_option_triforce_shuffle.setObjectName(u"label_for_option_triforce_shuffle")

        self.vlay_triforce_shuffle.addWidget(self.label_for_option_triforce_shuffle)

        self.option_triforce_shuffle = QComboBox(self.verticalLayoutWidget)
        self.option_triforce_shuffle.setObjectName(u"option_triforce_shuffle")

        self.vlay_triforce_shuffle.addWidget(self.option_triforce_shuffle)


        self.vlay_completion.addLayout(self.vlay_triforce_shuffle)

        self.option_imp_2 = QCheckBox(self.verticalLayoutWidget)
        self.option_imp_2.setObjectName(u"option_imp_2")

        self.vlay_completion.addWidget(self.option_imp_2)

        self.option_horde = QCheckBox(self.verticalLayoutWidget)
        self.option_horde.setObjectName(u"option_horde")

        self.vlay_completion.addWidget(self.option_horde)

        self.option_g3 = QCheckBox(self.verticalLayoutWidget)
        self.option_g3.setObjectName(u"option_g3")

        self.vlay_completion.addWidget(self.option_g3)

        self.option_demise = QCheckBox(self.verticalLayoutWidget)
        self.option_demise.setObjectName(u"option_demise")

        self.vlay_completion.addWidget(self.option_demise)

        self.hlay_demise_count = QHBoxLayout()
        self.hlay_demise_count.setObjectName(u"hlay_demise_count")
        self.label_for_option_demise_count = QLabel(self.verticalLayoutWidget)
        self.label_for_option_demise_count.setObjectName(u"label_for_option_demise_count")

        self.hlay_demise_count.addWidget(self.label_for_option_demise_count)

        self.option_demise_count = QSpinBox(self.verticalLayoutWidget)
        self.option_demise_count.setObjectName(u"option_demise_count")
        self.option_demise_count.setMaximumSize(QSize(41, 16777215))

        self.hlay_demise_count.addWidget(self.option_demise_count)


        self.vlay_completion.addLayout(self.hlay_demise_count)

        self.vspace_completion = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_completion.addItem(self.vspace_completion)

        self.box_dungeons = QGroupBox(self.tab_randomization_settings)
        self.box_dungeons.setObjectName(u"box_dungeons")
        self.box_dungeons.setGeometry(QRect(820, 0, 191, 501))
        self.verticalLayoutWidget_7 = QWidget(self.box_dungeons)
        self.verticalLayoutWidget_7.setObjectName(u"verticalLayoutWidget_7")
        self.verticalLayoutWidget_7.setGeometry(QRect(10, 20, 178, 471))
        self.vlay_dungeons = QVBoxLayout(self.verticalLayoutWidget_7)
        self.vlay_dungeons.setObjectName(u"vlay_dungeons")
        self.vlay_dungeons.setContentsMargins(0, 0, 0, 0)
        self.vlay_map_shuffle = QVBoxLayout()
        self.vlay_map_shuffle.setObjectName(u"vlay_map_shuffle")
        self.label_for_option_map_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_map_mode.setObjectName(u"label_for_option_map_mode")

        self.vlay_map_shuffle.addWidget(self.label_for_option_map_mode)

        self.option_map_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_map_mode.setObjectName(u"option_map_mode")

        self.vlay_map_shuffle.addWidget(self.option_map_mode)


        self.vlay_dungeons.addLayout(self.vlay_map_shuffle)

        self.vlay_small_key_shuffle = QVBoxLayout()
        self.vlay_small_key_shuffle.setObjectName(u"vlay_small_key_shuffle")
        self.label_for_option_small_key_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_small_key_mode.setObjectName(u"label_for_option_small_key_mode")

        self.vlay_small_key_shuffle.addWidget(self.label_for_option_small_key_mode)

        self.option_small_key_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_small_key_mode.setObjectName(u"option_small_key_mode")

        self.vlay_small_key_shuffle.addWidget(self.option_small_key_mode)


        self.vlay_dungeons.addLayout(self.vlay_small_key_shuffle)

        self.vlay_boss_key_shuffle = QVBoxLayout()
        self.vlay_boss_key_shuffle.setObjectName(u"vlay_boss_key_shuffle")
        self.label_for_option_boss_key_mode = QLabel(self.verticalLayoutWidget_7)
        self.label_for_option_boss_key_mode.setObjectName(u"label_for_option_boss_key_mode")

        self.vlay_boss_key_shuffle.addWidget(self.label_for_option_boss_key_mode)

        self.option_boss_key_mode = QComboBox(self.verticalLayoutWidget_7)
        self.option_boss_key_mode.setObjectName(u"option_boss_key_mode")

        self.vlay_boss_key_shuffle.addWidget(self.option_boss_key_mode)


        self.vlay_dungeons.addLayout(self.vlay_boss_key_shuffle)

        self.option_empty_unrequired_dungeons = QCheckBox(self.verticalLayoutWidget_7)
        self.option_empty_unrequired_dungeons.setObjectName(u"option_empty_unrequired_dungeons")

        self.vlay_dungeons.addWidget(self.option_empty_unrequired_dungeons)

        self.vlay_sword_reward = QVBoxLayout()
        self.vlay_sword_reward.setObjectName(u"vlay_sword_reward")
        self.label_for_sword_dungeon_reward = QLabel(self.verticalLayoutWidget_7)
        self.label_for_sword_dungeon_reward.setObjectName(u"label_for_sword_dungeon_reward")

        self.vlay_sword_reward.addWidget(self.label_for_sword_dungeon_reward)

        self.option_sword_dungeon_reward = QComboBox(self.verticalLayoutWidget_7)
        self.option_sword_dungeon_reward.setObjectName(u"option_sword_dungeon_reward")

        self.vlay_sword_reward.addWidget(self.option_sword_dungeon_reward)


        self.vlay_dungeons.addLayout(self.vlay_sword_reward)

        self.vspace_dungeons = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_dungeons.addItem(self.vspace_dungeons)

        self.box_open = QGroupBox(self.tab_randomization_settings)
        self.box_open.setObjectName(u"box_open")
        self.box_open.setGeometry(QRect(410, 0, 191, 501))
        self.verticalLayoutWidget_2 = QWidget(self.box_open)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 171, 471))
        self.vlay_open = QVBoxLayout(self.verticalLayoutWidget_2)
        self.vlay_open.setObjectName(u"vlay_open")
        self.vlay_open.setContentsMargins(0, 0, 0, 0)
        self.vlay_open_thunderhead = QVBoxLayout()
        self.vlay_open_thunderhead.setObjectName(u"vlay_open_thunderhead")
        self.label_for_option_open_thunderhead = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_open_thunderhead.setObjectName(u"label_for_option_open_thunderhead")

        self.vlay_open_thunderhead.addWidget(self.label_for_option_open_thunderhead)

        self.option_open_thunderhead = QComboBox(self.verticalLayoutWidget_2)
        self.option_open_thunderhead.setObjectName(u"option_open_thunderhead")

        self.vlay_open_thunderhead.addWidget(self.option_open_thunderhead)


        self.vlay_open.addLayout(self.vlay_open_thunderhead)

        self.option_open_et = QCheckBox(self.verticalLayoutWidget_2)
        self.option_open_et.setObjectName(u"option_open_et")

        self.vlay_open.addWidget(self.option_open_et)

        self.vlay_open_lmf = QVBoxLayout()
        self.vlay_open_lmf.setObjectName(u"vlay_open_lmf")
        self.label_for_option_open_lmf = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_open_lmf.setObjectName(u"label_for_option_open_lmf")

        self.vlay_open_lmf.addWidget(self.label_for_option_open_lmf)

        self.option_open_lmf = QComboBox(self.verticalLayoutWidget_2)
        self.option_open_lmf.setObjectName(u"option_open_lmf")

        self.vlay_open_lmf.addWidget(self.option_open_lmf)


        self.vlay_open.addLayout(self.vlay_open_lmf)

        self.hlay_starting_tablets = QHBoxLayout()
        self.hlay_starting_tablets.setObjectName(u"hlay_starting_tablets")
        self.label_for_option_starting_tablet_count = QLabel(self.verticalLayoutWidget_2)
        self.label_for_option_starting_tablet_count.setObjectName(u"label_for_option_starting_tablet_count")

        self.hlay_starting_tablets.addWidget(self.label_for_option_starting_tablet_count)

        self.option_starting_tablet_count = QSpinBox(self.verticalLayoutWidget_2)
        self.option_starting_tablet_count.setObjectName(u"option_starting_tablet_count")
        self.option_starting_tablet_count.setMaximumSize(QSize(41, 16777215))

        self.hlay_starting_tablets.addWidget(self.option_starting_tablet_count)


        self.vlay_open.addLayout(self.hlay_starting_tablets)

        self.vspace_open = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_open.addItem(self.vspace_open)

        self.box_er = QGroupBox(self.tab_randomization_settings)
        self.box_er.setObjectName(u"box_er")
        self.box_er.setGeometry(QRect(610, 0, 201, 501))
        self.verticalLayoutWidget_4 = QWidget(self.box_er)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 19, 186, 471))
        self.vlay_er = QVBoxLayout(self.verticalLayoutWidget_4)
        self.vlay_er.setObjectName(u"vlay_er")
        self.vlay_er.setContentsMargins(0, 0, 0, 0)
        self.vlay_dungeon_er = QVBoxLayout()
        self.vlay_dungeon_er.setObjectName(u"vlay_dungeon_er")
        self.label_for_option_randomize_entrances = QLabel(self.verticalLayoutWidget_4)
        self.label_for_option_randomize_entrances.setObjectName(u"label_for_option_randomize_entrances")

        self.vlay_dungeon_er.addWidget(self.label_for_option_randomize_entrances)

        self.option_randomize_entrances = QComboBox(self.verticalLayoutWidget_4)
        self.option_randomize_entrances.setObjectName(u"option_randomize_entrances")

        self.vlay_dungeon_er.addWidget(self.option_randomize_entrances)


        self.vlay_er.addLayout(self.vlay_dungeon_er)

        self.option_randomize_trials = QCheckBox(self.verticalLayoutWidget_4)
        self.option_randomize_trials.setObjectName(u"option_randomize_trials")

        self.vlay_er.addWidget(self.option_randomize_trials)

        self.vspace_er = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.vlay_er.addItem(self.vspace_er)

        self.box_shuffles = QGroupBox(self.tab_randomization_settings)
        self.box_shuffles.setObjectName(u"box_shuffles")
        self.box_shuffles.setGeometry(QRect(10, 0, 191, 501))
        self.verticalLayoutWidget_17 = QWidget(self.box_shuffles)
        self.verticalLayoutWidget_17.setObjectName(u"verticalLayoutWidget_17")
        self.verticalLayoutWidget_17.setGeometry(QRect(10, 21, 171, 471))
        self.vlay_shuffles = QVBoxLayout(self.verticalLayoutWidget_17)
        self.vlay_shuffles.setObjectName(u"vlay_shuffles")
        self.vlay_shuffles.setContentsMargins(0, 0, 0, 0)
        self.vlay_batreaux = QVBoxLayout()
        self.vlay_batreaux.setObjectName(u"vlay_batreaux")
        self.label_for_option_max_batreaux_reward = QLabel(self.verticalLayoutWidget_17)
        self.label_for_option_max_batreaux_reward.setObjectName(u"label_for_option_max_batreaux_reward")

        self.vlay_batreaux.addWidget(self.label_for_option_max_batreaux_reward)

        self.option_max_batreaux_reward = QComboBox(self.verticalLayoutWidget_17)
        self.option_max_batreaux_reward.setObjectName(u"option_max_batreaux_reward")

        self.vlay_batreaux.addWidget(self.option_max_batreaux_reward)


        self.vlay_shuffles.addLayout(self.vlay_batreaux)

        self.vlay_beedle = QVBoxLayout()
        self.vlay_beedle.setObjectName(u"vlay_beedle")
        self.label_10 = QLabel(self.verticalLayoutWidget_17)
        self.label_10.setObjectName(u"label_10")

        self.vlay_beedle.addWidget(self.label_10)

        self.option_shopsanity = QComboBox(self.verticalLayoutWidget_17)
        self.option_shopsanity.setObjectName(u"option_shopsanity")

        self.vlay_beedle.addWidget(self.option_shopsanity)


        self.vlay_shuffles.addLayout(self.vlay_beedle)

        self.vlay_rupeesanity = QVBoxLayout()
        self.vlay_rupeesanity.setObjectName(u"vlay_rupeesanity")
        self.label_for_option_rupeesanity = QLabel(self.verticalLayoutWidget_17)
        self.label_for_option_rupeesanity.setObjectName(u"label_for_option_rupeesanity")

        self.vlay_rupeesanity.addWidget(self.label_for_option_rupeesanity)

        self.option_rupeesanity = QComboBox(self.verticalLayoutWidget_17)
        self.option_rupeesanity.setObjectName(u"option_rupeesanity")

        self.vlay_rupeesanity.addWidget(self.option_rupeesanity)


        self.vlay_shuffles.addLayout(self.vlay_rupeesanity)

        self.vspace_shuffles = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_shuffles.addItem(self.vspace_shuffles)

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
        self.label_for_option_shuffle_trial_objects = QLabel(self.verticalLayoutWidget_22)
        self.label_for_option_shuffle_trial_objects.setObjectName(u"label_for_option_shuffle_trial_objects")

        self.verticalLayout_trialshuffle.addWidget(self.label_for_option_shuffle_trial_objects)

        self.option_shuffle_trial_objects = QComboBox(self.verticalLayoutWidget_22)
        self.option_shuffle_trial_objects.setObjectName(u"option_shuffle_trial_objects")

        self.verticalLayout_trialshuffle.addWidget(self.option_shuffle_trial_objects)


        self.vlay_silent_realms.addLayout(self.verticalLayout_trialshuffle)

        self.vspace_silent_realms = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_silent_realms.addItem(self.vspace_silent_realms)

        self.box_heromode_changes = QGroupBox(self.tab_additional_settings)
        self.box_heromode_changes.setObjectName(u"box_heromode_changes")
        self.box_heromode_changes.setGeometry(QRect(810, 0, 191, 251))
        self.verticalLayoutWidget_21 = QWidget(self.box_heromode_changes)
        self.verticalLayoutWidget_21.setObjectName(u"verticalLayoutWidget_21")
        self.verticalLayoutWidget_21.setGeometry(QRect(10, 20, 180, 221))
        self.vlay_heromode_changes = QVBoxLayout(self.verticalLayoutWidget_21)
        self.vlay_heromode_changes.setObjectName(u"vlay_heromode_changes")
        self.vlay_heromode_changes.setContentsMargins(0, 0, 0, 0)
        self.option_upgraded_skyward_strike = QCheckBox(self.verticalLayoutWidget_21)
        self.option_upgraded_skyward_strike.setObjectName(u"option_upgraded_skyward_strike")

        self.vlay_heromode_changes.addWidget(self.option_upgraded_skyward_strike)

        self.option_fast_air_meter = QCheckBox(self.verticalLayoutWidget_21)
        self.option_fast_air_meter.setObjectName(u"option_fast_air_meter")

        self.vlay_heromode_changes.addWidget(self.option_fast_air_meter)

        self.option_enable_heart_drops = QCheckBox(self.verticalLayoutWidget_21)
        self.option_enable_heart_drops.setObjectName(u"option_enable_heart_drops")

        self.vlay_heromode_changes.addWidget(self.option_enable_heart_drops)

        self.hlay_damage_multiplier = QHBoxLayout()
        self.hlay_damage_multiplier.setObjectName(u"hlay_damage_multiplier")
        self.label_for_option_damage_multiplier = QLabel(self.verticalLayoutWidget_21)
        self.label_for_option_damage_multiplier.setObjectName(u"label_for_option_damage_multiplier")

        self.hlay_damage_multiplier.addWidget(self.label_for_option_damage_multiplier)

        self.option_damage_multiplier = QSpinBox(self.verticalLayoutWidget_21)
        self.option_damage_multiplier.setObjectName(u"option_damage_multiplier")
        self.option_damage_multiplier.setMaximumSize(QSize(41, 16777215))
        self.option_damage_multiplier.setMinimum(1)
        self.option_damage_multiplier.setMaximum(255)

        self.hlay_damage_multiplier.addWidget(self.option_damage_multiplier)


        self.vlay_heromode_changes.addLayout(self.hlay_damage_multiplier)

        self.vspace_heromode_changes = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_heromode_changes.addItem(self.vspace_heromode_changes)

        self.tabWidget.addTab(self.tab_additional_settings, "")
        self.tab_logic_settings = QWidget()
        self.tab_logic_settings.setObjectName(u"tab_logic_settings")
        self.layoutWidget = QWidget(self.tab_logic_settings)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 1001, 499))
        self.vlay_logic_settings = QVBoxLayout(self.layoutWidget)
        self.vlay_logic_settings.setObjectName(u"vlay_logic_settings")
        self.vlay_logic_settings.setContentsMargins(0, 0, 0, 0)
        self.hlay_misc_logic_settings = QHBoxLayout()
        self.hlay_misc_logic_settings.setObjectName(u"hlay_misc_logic_settings")
        self.label_for_option_logic_mode = QLabel(self.layoutWidget)
        self.label_for_option_logic_mode.setObjectName(u"label_for_option_logic_mode")

        self.hlay_misc_logic_settings.addWidget(self.label_for_option_logic_mode)

        self.option_logic_mode = QComboBox(self.layoutWidget)
        self.option_logic_mode.setObjectName(u"option_logic_mode")

        self.hlay_misc_logic_settings.addWidget(self.option_logic_mode)

        self.option_hero_mode = QCheckBox(self.layoutWidget)
        self.option_hero_mode.setObjectName(u"option_hero_mode")

        self.hlay_misc_logic_settings.addWidget(self.option_hero_mode)

        self.hspace_misc_logic_settings = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlay_misc_logic_settings.addItem(self.hspace_misc_logic_settings)


        self.vlay_logic_settings.addLayout(self.hlay_misc_logic_settings)

        self.vlay_exclude_locations = QVBoxLayout()
        self.vlay_exclude_locations.setObjectName(u"vlay_exclude_locations")
        self.label_exclude_locations = QLabel(self.layoutWidget)
        self.label_exclude_locations.setObjectName(u"label_exclude_locations")

        self.vlay_exclude_locations.addWidget(self.label_exclude_locations)

        self.hlay_exclude_locations_body = QHBoxLayout()
        self.hlay_exclude_locations_body.setObjectName(u"hlay_exclude_locations_body")
        self.included_locations = QListView(self.layoutWidget)
        self.included_locations.setObjectName(u"included_locations")

        self.hlay_exclude_locations_body.addWidget(self.included_locations)

        self.vlay_exclude_locations_controls = QVBoxLayout()
        self.vlay_exclude_locations_controls.setObjectName(u"vlay_exclude_locations_controls")
        self.include_location = QPushButton(self.layoutWidget)
        self.include_location.setObjectName(u"include_location")

        self.vlay_exclude_locations_controls.addWidget(self.include_location)

        self.exclude_location = QPushButton(self.layoutWidget)
        self.exclude_location.setObjectName(u"exclude_location")

        self.vlay_exclude_locations_controls.addWidget(self.exclude_location)


        self.hlay_exclude_locations_body.addLayout(self.vlay_exclude_locations_controls)

        self.excluded_locations = QListView(self.layoutWidget)
        self.excluded_locations.setObjectName(u"excluded_locations")

        self.hlay_exclude_locations_body.addWidget(self.excluded_locations)


        self.vlay_exclude_locations.addLayout(self.hlay_exclude_locations_body)


        self.vlay_logic_settings.addLayout(self.vlay_exclude_locations)

        self.vlay_tricks = QVBoxLayout()
        self.vlay_tricks.setObjectName(u"vlay_tricks")
        self.label_tricks = QLabel(self.layoutWidget)
        self.label_tricks.setObjectName(u"label_tricks")

        self.vlay_tricks.addWidget(self.label_tricks)

        self.hlay_tricks_body = QHBoxLayout()
        self.hlay_tricks_body.setObjectName(u"hlay_tricks_body")
        self.disabled_tricks = QListView(self.layoutWidget)
        self.disabled_tricks.setObjectName(u"disabled_tricks")

        self.hlay_tricks_body.addWidget(self.disabled_tricks)

        self.vlay_tricks_controls = QVBoxLayout()
        self.vlay_tricks_controls.setObjectName(u"vlay_tricks_controls")
        self.disable_trick = QPushButton(self.layoutWidget)
        self.disable_trick.setObjectName(u"disable_trick")

        self.vlay_tricks_controls.addWidget(self.disable_trick)

        self.enable_trick = QPushButton(self.layoutWidget)
        self.enable_trick.setObjectName(u"enable_trick")

        self.vlay_tricks_controls.addWidget(self.enable_trick)


        self.hlay_tricks_body.addLayout(self.vlay_tricks_controls)

        self.enabled_tricks = QListView(self.layoutWidget)
        self.enabled_tricks.setObjectName(u"enabled_tricks")

        self.hlay_tricks_body.addWidget(self.enabled_tricks)


        self.vlay_tricks.addLayout(self.hlay_tricks_body)


        self.vlay_logic_settings.addLayout(self.vlay_tricks)

        self.tabWidget.addTab(self.tab_logic_settings, "")
        self.tab_hints = QWidget()
        self.tab_hints.setObjectName(u"tab_hints")
        self.box_stone_hints = QGroupBox(self.tab_hints)
        self.box_stone_hints.setObjectName(u"box_stone_hints")
        self.box_stone_hints.setGeometry(QRect(10, 10, 191, 231))
        self.verticalLayoutWidget_12 = QWidget(self.box_stone_hints)
        self.verticalLayoutWidget_12.setObjectName(u"verticalLayoutWidget_12")
        self.verticalLayoutWidget_12.setGeometry(QRect(10, 20, 175, 207))
        self.vlay_stone_hints = QVBoxLayout(self.verticalLayoutWidget_12)
        self.vlay_stone_hints.setObjectName(u"vlay_stone_hints")
        self.vlay_stone_hints.setContentsMargins(0, 0, 0, 0)
        self.vlay_hint_distro = QVBoxLayout()
        self.vlay_hint_distro.setObjectName(u"vlay_hint_distro")
        self.label_for_option_hint_distribution = QLabel(self.verticalLayoutWidget_12)
        self.label_for_option_hint_distribution.setObjectName(u"label_for_option_hint_distribution")

        self.vlay_hint_distro.addWidget(self.label_for_option_hint_distribution)

        self.option_hint_distribution = QComboBox(self.verticalLayoutWidget_12)
        self.option_hint_distribution.setObjectName(u"option_hint_distribution")

        self.vlay_hint_distro.addWidget(self.option_hint_distribution)


        self.vlay_stone_hints.addLayout(self.vlay_hint_distro)

        self.option_cube_sots = QCheckBox(self.verticalLayoutWidget_12)
        self.option_cube_sots.setObjectName(u"option_cube_sots")

        self.vlay_stone_hints.addWidget(self.option_cube_sots)

        self.option_precise_item = QCheckBox(self.verticalLayoutWidget_12)
        self.option_precise_item.setObjectName(u"option_precise_item")

        self.vlay_stone_hints.addWidget(self.option_precise_item)

        self.vspace_stone_hints = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_stone_hints.addItem(self.vspace_stone_hints)

        self.box_other_hints = QGroupBox(self.tab_hints)
        self.box_other_hints.setObjectName(u"box_other_hints")
        self.box_other_hints.setGeometry(QRect(210, 10, 191, 231))
        self.verticalLayoutWidget_6 = QWidget(self.box_other_hints)
        self.verticalLayoutWidget_6.setObjectName(u"verticalLayoutWidget_6")
        self.verticalLayoutWidget_6.setGeometry(QRect(10, 20, 174, 201))
        self.vlay_other_hints = QVBoxLayout(self.verticalLayoutWidget_6)
        self.vlay_other_hints.setObjectName(u"vlay_other_hints")
        self.vlay_other_hints.setContentsMargins(0, 0, 0, 0)
        self.vlay_song_hints = QVBoxLayout()
        self.vlay_song_hints.setObjectName(u"vlay_song_hints")
        self.label_6 = QLabel(self.verticalLayoutWidget_6)
        self.label_6.setObjectName(u"label_6")

        self.vlay_song_hints.addWidget(self.label_6)

        self.option_song_hints = QComboBox(self.verticalLayoutWidget_6)
        self.option_song_hints.setObjectName(u"option_song_hints")

        self.vlay_song_hints.addWidget(self.option_song_hints)


        self.vlay_other_hints.addLayout(self.vlay_song_hints)

        self.option_impa_sot_hint = QCheckBox(self.verticalLayoutWidget_6)
        self.option_impa_sot_hint.setObjectName(u"option_impa_sot_hint")

        self.vlay_other_hints.addWidget(self.option_impa_sot_hint)

        self.vlay_chest_dowsing = QVBoxLayout()
        self.vlay_chest_dowsing.setObjectName(u"vlay_chest_dowsing")
        self.label_for_option_chest_dowsing = QLabel(self.verticalLayoutWidget_6)
        self.label_for_option_chest_dowsing.setObjectName(u"label_for_option_chest_dowsing")

        self.vlay_chest_dowsing.addWidget(self.label_for_option_chest_dowsing)

        self.option_chest_dowsing = QComboBox(self.verticalLayoutWidget_6)
        self.option_chest_dowsing.setObjectName(u"option_chest_dowsing")

        self.vlay_chest_dowsing.addWidget(self.option_chest_dowsing)


        self.vlay_other_hints.addLayout(self.vlay_chest_dowsing)

        self.option_dungeon_dowsing = QCheckBox(self.verticalLayoutWidget_6)
        self.option_dungeon_dowsing.setObjectName(u"option_dungeon_dowsing")

        self.vlay_other_hints.addWidget(self.option_dungeon_dowsing)

        self.vspace_other_hints = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_other_hints.addItem(self.vspace_other_hints)

        self.tabWidget.addTab(self.tab_hints, "")
        self.tab_starting_items = QWidget()
        self.tab_starting_items.setObjectName(u"tab_starting_items")
        self.verticalLayoutWidget_201 = QWidget(self.tab_starting_items)
        self.verticalLayoutWidget_201.setObjectName(u"verticalLayoutWidget_201")
        self.verticalLayoutWidget_201.setGeometry(QRect(10, 10, 1001, 501))
        self.vlay_starting_items = QVBoxLayout(self.verticalLayoutWidget_201)
        self.vlay_starting_items.setObjectName(u"vlay_starting_items")
        self.vlay_starting_items.setContentsMargins(0, 0, 0, 0)
        self.hlay_starting_items_body = QHBoxLayout()
        self.hlay_starting_items_body.setObjectName(u"hlay_starting_items_body")
        self.vlay_randomized_items_section = QVBoxLayout()
        self.vlay_randomized_items_section.setObjectName(u"vlay_randomized_items_section")
        self.label_randomized_items = QLabel(self.verticalLayoutWidget_201)
        self.label_randomized_items.setObjectName(u"label_randomized_items")

        self.vlay_randomized_items_section.addWidget(self.label_randomized_items)

        self.randomized_items = QListView(self.verticalLayoutWidget_201)
        self.randomized_items.setObjectName(u"randomized_items")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.randomized_items.sizePolicy().hasHeightForWidth())
        self.randomized_items.setSizePolicy(sizePolicy3)

        self.vlay_randomized_items_section.addWidget(self.randomized_items)


        self.hlay_starting_items_body.addLayout(self.vlay_randomized_items_section)

        self.vlay_starting_items_controls = QVBoxLayout()
        self.vlay_starting_items_controls.setObjectName(u"vlay_starting_items_controls")
        self.vlay_starting_items_controls.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.vspace_starting_items_controls_upper = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_starting_items_controls.addItem(self.vspace_starting_items_controls_upper)

        self.randomize_item = QPushButton(self.verticalLayoutWidget_201)
        self.randomize_item.setObjectName(u"randomize_item")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.randomize_item.sizePolicy().hasHeightForWidth())
        self.randomize_item.setSizePolicy(sizePolicy4)

        self.vlay_starting_items_controls.addWidget(self.randomize_item)

        self.start_with_item = QPushButton(self.verticalLayoutWidget_201)
        self.start_with_item.setObjectName(u"start_with_item")
        sizePolicy4.setHeightForWidth(self.start_with_item.sizePolicy().hasHeightForWidth())
        self.start_with_item.setSizePolicy(sizePolicy4)

        self.vlay_starting_items_controls.addWidget(self.start_with_item)

        self.vspace_starting_items_controls_lower = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_starting_items_controls.addItem(self.vspace_starting_items_controls_lower)


        self.hlay_starting_items_body.addLayout(self.vlay_starting_items_controls)

        self.vlay_starting_items_section = QVBoxLayout()
        self.vlay_starting_items_section.setObjectName(u"vlay_starting_items_section")
        self.label_starting_items = QLabel(self.verticalLayoutWidget_201)
        self.label_starting_items.setObjectName(u"label_starting_items")

        self.vlay_starting_items_section.addWidget(self.label_starting_items)

        self.starting_items = QListView(self.verticalLayoutWidget_201)
        self.starting_items.setObjectName(u"starting_items")
        sizePolicy3.setHeightForWidth(self.starting_items.sizePolicy().hasHeightForWidth())
        self.starting_items.setSizePolicy(sizePolicy3)

        self.vlay_starting_items_section.addWidget(self.starting_items)


        self.hlay_starting_items_body.addLayout(self.vlay_starting_items_section)


        self.vlay_starting_items.addLayout(self.hlay_starting_items_body)

        self.line_starting_items_divider = QFrame(self.verticalLayoutWidget_201)
        self.line_starting_items_divider.setObjectName(u"line_starting_items_divider")
        self.line_starting_items_divider.setFrameShape(QFrame.HLine)
        self.line_starting_items_divider.setFrameShadow(QFrame.Sunken)

        self.vlay_starting_items.addWidget(self.line_starting_items_divider)

        self.hlay_starting_items_misc_options = QHBoxLayout()
        self.hlay_starting_items_misc_options.setObjectName(u"hlay_starting_items_misc_options")
        self.hlay_starting_items_misc_options.setContentsMargins(-1, -1, -1, 0)
        self.hlay_starting_sword = QHBoxLayout()
        self.hlay_starting_sword.setObjectName(u"hlay_starting_sword")
        self.label_for_option_starting_sword = QLabel(self.verticalLayoutWidget_201)
        self.label_for_option_starting_sword.setObjectName(u"label_for_option_starting_sword")

        self.hlay_starting_sword.addWidget(self.label_for_option_starting_sword)

        self.option_starting_sword = QComboBox(self.verticalLayoutWidget_201)
        self.option_starting_sword.setObjectName(u"option_starting_sword")

        self.hlay_starting_sword.addWidget(self.option_starting_sword)


        self.hlay_starting_items_misc_options.addLayout(self.hlay_starting_sword)

        self.option_random_starting_item = QCheckBox(self.verticalLayoutWidget_201)
        self.option_random_starting_item.setObjectName(u"option_random_starting_item")
        sizePolicy2.setHeightForWidth(self.option_random_starting_item.sizePolicy().hasHeightForWidth())
        self.option_random_starting_item.setSizePolicy(sizePolicy2)

        self.hlay_starting_items_misc_options.addWidget(self.option_random_starting_item)

        self.hlay_heart_containters = QHBoxLayout()
        self.hlay_heart_containters.setObjectName(u"hlay_heart_containters")
        self.label_for_option_starting_heart_containers = QLabel(self.verticalLayoutWidget_201)
        self.label_for_option_starting_heart_containers.setObjectName(u"label_for_option_starting_heart_containers")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_for_option_starting_heart_containers.sizePolicy().hasHeightForWidth())
        self.label_for_option_starting_heart_containers.setSizePolicy(sizePolicy5)

        self.hlay_heart_containters.addWidget(self.label_for_option_starting_heart_containers)

        self.option_starting_heart_containers = QSpinBox(self.verticalLayoutWidget_201)
        self.option_starting_heart_containers.setObjectName(u"option_starting_heart_containers")
        sizePolicy2.setHeightForWidth(self.option_starting_heart_containers.sizePolicy().hasHeightForWidth())
        self.option_starting_heart_containers.setSizePolicy(sizePolicy2)
        self.option_starting_heart_containers.setMaximumSize(QSize(41, 16777215))

        self.hlay_heart_containters.addWidget(self.option_starting_heart_containers)


        self.hlay_starting_items_misc_options.addLayout(self.hlay_heart_containters)

        self.hlay_heart_pieces = QHBoxLayout()
        self.hlay_heart_pieces.setObjectName(u"hlay_heart_pieces")
        self.label_for_option_starting_heart_pieces = QLabel(self.verticalLayoutWidget_201)
        self.label_for_option_starting_heart_pieces.setObjectName(u"label_for_option_starting_heart_pieces")
        sizePolicy5.setHeightForWidth(self.label_for_option_starting_heart_pieces.sizePolicy().hasHeightForWidth())
        self.label_for_option_starting_heart_pieces.setSizePolicy(sizePolicy5)

        self.hlay_heart_pieces.addWidget(self.label_for_option_starting_heart_pieces)

        self.option_starting_heart_pieces = QSpinBox(self.verticalLayoutWidget_201)
        self.option_starting_heart_pieces.setObjectName(u"option_starting_heart_pieces")
        sizePolicy2.setHeightForWidth(self.option_starting_heart_pieces.sizePolicy().hasHeightForWidth())
        self.option_starting_heart_pieces.setSizePolicy(sizePolicy2)
        self.option_starting_heart_pieces.setMaximumSize(QSize(41, 16777215))

        self.hlay_heart_pieces.addWidget(self.option_starting_heart_pieces)


        self.hlay_starting_items_misc_options.addLayout(self.hlay_heart_pieces)

        self.label_current_starting_health = QLabel(self.verticalLayoutWidget_201)
        self.label_current_starting_health.setObjectName(u"label_current_starting_health")

        self.hlay_starting_items_misc_options.addWidget(self.label_current_starting_health)

        self.current_starting_health_counter = QLabel(self.verticalLayoutWidget_201)
        self.current_starting_health_counter.setObjectName(u"current_starting_health_counter")

        self.hlay_starting_items_misc_options.addWidget(self.current_starting_health_counter)

        self.hspace_starting_items_misc = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlay_starting_items_misc_options.addItem(self.hspace_starting_items_misc)


        self.vlay_starting_items.addLayout(self.hlay_starting_items_misc_options)

        self.tabWidget.addTab(self.tab_starting_items, "")
        self.verticalLayoutWidget_10 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_10.setObjectName(u"verticalLayoutWidget_10")
        self.verticalLayoutWidget_10.setGeometry(QRect(10, 615, 1031, 110))
        self.vlay_bottom_controls = QVBoxLayout(self.verticalLayoutWidget_10)
        self.vlay_bottom_controls.setObjectName(u"vlay_bottom_controls")
        self.vlay_bottom_controls.setContentsMargins(0, 0, 0, 0)
        self.hlay_permalink = QHBoxLayout()
        self.hlay_permalink.setObjectName(u"hlay_permalink")
        self.label_permalink = QLabel(self.verticalLayoutWidget_10)
        self.label_permalink.setObjectName(u"label_permalink")

        self.hlay_permalink.addWidget(self.label_permalink)

        self.permalink = QLineEdit(self.verticalLayoutWidget_10)
        self.permalink.setObjectName(u"permalink")

        self.hlay_permalink.addWidget(self.permalink)


        self.vlay_bottom_controls.addLayout(self.hlay_permalink)

        self.hlay_seed = QHBoxLayout()
        self.hlay_seed.setObjectName(u"hlay_seed")
        self.label_seed = QLabel(self.verticalLayoutWidget_10)
        self.label_seed.setObjectName(u"label_seed")
        self.label_seed.setToolTipDuration(-1)
        self.label_seed.setLayoutDirection(Qt.LeftToRight)
        self.label_seed.setAutoFillBackground(False)
        self.label_seed.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.hlay_seed.addWidget(self.label_seed)

        self.seed = QLineEdit(self.verticalLayoutWidget_10)
        self.seed.setObjectName(u"seed")

        self.hlay_seed.addWidget(self.seed)

        self.seed_button = QPushButton(self.verticalLayoutWidget_10)
        self.seed_button.setObjectName(u"seed_button")

        self.hlay_seed.addWidget(self.seed_button)


        self.vlay_bottom_controls.addLayout(self.hlay_seed)

        self.hlay_button_row = QHBoxLayout()
        self.hlay_button_row.setObjectName(u"hlay_button_row")
        self.randomize_button = QPushButton(self.verticalLayoutWidget_10)
        self.randomize_button.setObjectName(u"randomize_button")

        self.hlay_button_row.addWidget(self.randomize_button)


        self.vlay_bottom_controls.addLayout(self.hlay_button_row)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(5)
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
        self.label_output.setText(QCoreApplication.translate("MainWindow", u"Output Folder", None))
        self.ouput_folder_browse_button.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.option_plando.setText(QCoreApplication.translate("MainWindow", u"Enable Plandomizer", None))
        self.plando_file_browse.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.box_additional_files.setTitle(QCoreApplication.translate("MainWindow", u"Additional File Generation", None))
        self.option_no_spoiler_log.setText(QCoreApplication.translate("MainWindow", u"No Spoiler Log", None))
        self.option_json_spoiler.setText(QCoreApplication.translate("MainWindow", u"Generate JSON Spoiler Log", None))
        self.option_out_placement_file.setText(QCoreApplication.translate("MainWindow", u"Generate Placement File", None))
        self.box_advanced.setTitle(QCoreApplication.translate("MainWindow", u"Advanced Options", None))
        self.option_dry_run.setText(QCoreApplication.translate("MainWindow", u"Dry Run", None))
        self.box_cosmetics.setTitle(QCoreApplication.translate("MainWindow", u"Cosmetics", None))
        self.option_tunic_swap.setText(QCoreApplication.translate("MainWindow", u"Tunic Swap", None))
        self.option_no_enemy_music.setText(QCoreApplication.translate("MainWindow", u"Remove Enemy Music", None))
        self.box_music_rando.setTitle(QCoreApplication.translate("MainWindow", u"Randomize Music", None))
        self.label_for_option_music_rando.setText(QCoreApplication.translate("MainWindow", u"Randomize Music", None))
        self.option_cutoff_gameover_music.setText(QCoreApplication.translate("MainWindow", u"Cutoff Game Over Music", None))
        self.option_allow_custom_music.setText(QCoreApplication.translate("MainWindow", u"Allow Custom Music", None))
        self.box_presets.setTitle(QCoreApplication.translate("MainWindow", u"Presets", None))
        self.label_presets.setText(QCoreApplication.translate("MainWindow", u"Presets overwrite ALL game settings", None))
        self.load_preset.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.save_preset.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.delete_preset.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setup), QCoreApplication.translate("MainWindow", u"Setup", None))
#if QT_CONFIG(tooltip)
        self.tab_randomization_settings.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.box_completion.setTitle(QCoreApplication.translate("MainWindow", u"Completion Conditions", None))
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
        self.box_dungeons.setTitle(QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.label_for_option_map_mode.setText(QCoreApplication.translate("MainWindow", u"Map Mode", None))
        self.label_for_option_small_key_mode.setText(QCoreApplication.translate("MainWindow", u"Small Keys", None))
        self.label_for_option_boss_key_mode.setText(QCoreApplication.translate("MainWindow", u"Boss Keys", None))
        self.option_empty_unrequired_dungeons.setText(QCoreApplication.translate("MainWindow", u"Empty Unrequired Dungeons", None))
        self.label_for_sword_dungeon_reward.setText(QCoreApplication.translate("MainWindow", u"Sword Dungeon Reward", None))
        self.box_open.setTitle(QCoreApplication.translate("MainWindow", u"Open Settings", None))
        self.label_for_option_open_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Open Thunderhead", None))
        self.option_open_et.setText(QCoreApplication.translate("MainWindow", u"Open Earth Temple", None))
        self.label_for_option_open_lmf.setText(QCoreApplication.translate("MainWindow", u"Open Lanayru Mining Facility", None))
        self.label_for_option_starting_tablet_count.setText(QCoreApplication.translate("MainWindow", u"Starting Tablets", None))
        self.box_er.setTitle(QCoreApplication.translate("MainWindow", u"Entrance Randomization", None))
        self.label_for_option_randomize_entrances.setText(QCoreApplication.translate("MainWindow", u"Randomize Dungeon Entrances", None))
        self.option_randomize_entrances.setCurrentText("")
        self.option_randomize_trials.setText(QCoreApplication.translate("MainWindow", u"Randomize Silent Realm Gates", None))
        self.box_shuffles.setTitle(QCoreApplication.translate("MainWindow", u"Shuffles", None))
        self.label_for_option_max_batreaux_reward.setText(QCoreApplication.translate("MainWindow", u"Maximum Batreaux Reward", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Beedle's Shop", None))
        self.label_for_option_rupeesanity.setText(QCoreApplication.translate("MainWindow", u"Rupeesanity", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_randomization_settings), QCoreApplication.translate("MainWindow", u"Randomization Settings", None))
        self.box_convenience_tweaks.setTitle(QCoreApplication.translate("MainWindow", u"Convenience Tweaks", None))
        self.option_fill_dowsing_on_white_sword.setText(QCoreApplication.translate("MainWindow", u"Fill Dowsing on White Sword", None))
        self.box_vanilla_tweaks.setTitle(QCoreApplication.translate("MainWindow", u"Vanilla Tweaks", None))
        self.option_fix_bit_crashes.setText(QCoreApplication.translate("MainWindow", u"Fix BiT crashes", None))
        self.box_item_pool.setTitle(QCoreApplication.translate("MainWindow", u"Item Pool", None))
        self.option_gondo_upgrades.setText(QCoreApplication.translate("MainWindow", u"Place Scrap Shop Upgrades", None))
        self.label_for_option_rupoor_mode.setText(QCoreApplication.translate("MainWindow", u"Rupoor Mode", None))
        self.box_silent_realms.setTitle(QCoreApplication.translate("MainWindow", u"Silent Realms", None))
        self.label_for_option_shuffle_trial_objects.setText(QCoreApplication.translate("MainWindow", u"Shuffle Trial Objects", None))
        self.box_heromode_changes.setTitle(QCoreApplication.translate("MainWindow", u"Hero Mode Changes", None))
        self.option_upgraded_skyward_strike.setText(QCoreApplication.translate("MainWindow", u"Upgraded Skyward Strike", None))
        self.option_fast_air_meter.setText(QCoreApplication.translate("MainWindow", u"Faster Air Meter Depletion", None))
        self.option_enable_heart_drops.setText(QCoreApplication.translate("MainWindow", u"Spawn Heart Flowers", None))
        self.label_for_option_damage_multiplier.setText(QCoreApplication.translate("MainWindow", u"Damage Taken Multiplier", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_additional_settings), QCoreApplication.translate("MainWindow", u"Additional Settings", None))
        self.label_for_option_logic_mode.setText(QCoreApplication.translate("MainWindow", u"Logic Mode", None))
        self.option_hero_mode.setText(QCoreApplication.translate("MainWindow", u"Hero Mode", None))
        self.label_exclude_locations.setText(QCoreApplication.translate("MainWindow", u"Exclude Locations", None))
        self.include_location.setText(QCoreApplication.translate("MainWindow", u"Include\n"
"<--", None))
        self.exclude_location.setText(QCoreApplication.translate("MainWindow", u"Exclude\n"
"-->", None))
        self.label_tricks.setText(QCoreApplication.translate("MainWindow", u"Enable Tricks", None))
#if QT_CONFIG(tooltip)
        self.disabled_tricks.setToolTip(QCoreApplication.translate("MainWindow", u"test", None))
#endif // QT_CONFIG(tooltip)
        self.disable_trick.setText(QCoreApplication.translate("MainWindow", u"Disable\n"
"<--", None))
        self.enable_trick.setText(QCoreApplication.translate("MainWindow", u"Enable\n"
"-->", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logic_settings), QCoreApplication.translate("MainWindow", u"Logic Settings", None))
        self.box_stone_hints.setTitle(QCoreApplication.translate("MainWindow", u"Gossip Stone Hints", None))
        self.label_for_option_hint_distribution.setText(QCoreApplication.translate("MainWindow", u"Hint Distribution", None))
        self.option_cube_sots.setText(QCoreApplication.translate("MainWindow", u"Separate Cube SotS Hints", None))
        self.option_precise_item.setText(QCoreApplication.translate("MainWindow", u"Precise Item Hints", None))
        self.box_other_hints.setTitle(QCoreApplication.translate("MainWindow", u"Other Hints", None))
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
        self.label_permalink.setText(QCoreApplication.translate("MainWindow", u"Settings String", None))
#if QT_CONFIG(tooltip)
        self.label_seed.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.label_seed.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.label_seed.setText(QCoreApplication.translate("MainWindow", u"Seed", None))
        self.seed_button.setText(QCoreApplication.translate("MainWindow", u"New Seed", None))
        self.randomize_button.setText(QCoreApplication.translate("MainWindow", u"Randomize", None))
    # retranslateUi

