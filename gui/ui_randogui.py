# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'randogui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFontComboBox, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QListView,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1202, 759)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setSizeIncrement(QSize(0, 0))
        self.tabWidget.setToolTipDuration(-6)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tab_setup = QWidget()
        self.tab_setup.setObjectName(u"tab_setup")
        self.verticalLayout_27 = QVBoxLayout(self.tab_setup)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.vlay_files = QVBoxLayout()
        self.vlay_files.setObjectName(u"vlay_files")
        self.hlay_output = QHBoxLayout()
        self.hlay_output.setObjectName(u"hlay_output")
        self.label_output = QLabel(self.tab_setup)
        self.label_output.setObjectName(u"label_output")
        self.label_output.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.hlay_output.addWidget(self.label_output)

        self.output_folder = QLineEdit(self.tab_setup)
        self.output_folder.setObjectName(u"output_folder")

        self.hlay_output.addWidget(self.output_folder)

        self.ouput_folder_browse_button = QPushButton(self.tab_setup)
        self.ouput_folder_browse_button.setObjectName(u"ouput_folder_browse_button")

        self.hlay_output.addWidget(self.ouput_folder_browse_button)


        self.vlay_files.addLayout(self.hlay_output)

        self.vlay_plando = QVBoxLayout()
        self.vlay_plando.setObjectName(u"vlay_plando")
        self.hlay_plando_file = QHBoxLayout()
        self.hlay_plando_file.setObjectName(u"hlay_plando_file")
        self.option_plando = QCheckBox(self.tab_setup)
        self.option_plando.setObjectName(u"option_plando")

        self.hlay_plando_file.addWidget(self.option_plando)

        self.plando_file = QLineEdit(self.tab_setup)
        self.plando_file.setObjectName(u"plando_file")

        self.hlay_plando_file.addWidget(self.plando_file)

        self.plando_file_browse = QPushButton(self.tab_setup)
        self.plando_file_browse.setObjectName(u"plando_file_browse")

        self.hlay_plando_file.addWidget(self.plando_file_browse)


        self.vlay_plando.addLayout(self.hlay_plando_file)


        self.vlay_files.addLayout(self.vlay_plando)


        self.verticalLayout_27.addLayout(self.vlay_files)

        self.hlay_setup_options = QHBoxLayout()
        self.hlay_setup_options.setObjectName(u"hlay_setup_options")
        self.box_additional_files = QGroupBox(self.tab_setup)
        self.box_additional_files.setObjectName(u"box_additional_files")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.box_additional_files.sizePolicy().hasHeightForWidth())
        self.box_additional_files.setSizePolicy(sizePolicy2)
        self.box_additional_files.setFlat(False)
        self.verticalLayout_22 = QVBoxLayout(self.box_additional_files)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.vlay_additional_files = QVBoxLayout()
        self.vlay_additional_files.setObjectName(u"vlay_additional_files")
        self.option_no_spoiler_log = QCheckBox(self.box_additional_files)
        self.option_no_spoiler_log.setObjectName(u"option_no_spoiler_log")

        self.vlay_additional_files.addWidget(self.option_no_spoiler_log)

        self.option_json_spoiler = QCheckBox(self.box_additional_files)
        self.option_json_spoiler.setObjectName(u"option_json_spoiler")

        self.vlay_additional_files.addWidget(self.option_json_spoiler)

        self.option_out_placement_file = QCheckBox(self.box_additional_files)
        self.option_out_placement_file.setObjectName(u"option_out_placement_file")

        self.vlay_additional_files.addWidget(self.option_out_placement_file)

        self.vspace_additional_files = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_additional_files.addItem(self.vspace_additional_files)


        self.verticalLayout_22.addLayout(self.vlay_additional_files)


        self.hlay_setup_options.addWidget(self.box_additional_files)

        self.box_advanced = QGroupBox(self.tab_setup)
        self.box_advanced.setObjectName(u"box_advanced")
        sizePolicy2.setHeightForWidth(self.box_advanced.sizePolicy().hasHeightForWidth())
        self.box_advanced.setSizePolicy(sizePolicy2)
        self.verticalLayout_23 = QVBoxLayout(self.box_advanced)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.vlay_advanced = QVBoxLayout()
        self.vlay_advanced.setObjectName(u"vlay_advanced")
        self.option_dry_run = QCheckBox(self.box_advanced)
        self.option_dry_run.setObjectName(u"option_dry_run")

        self.vlay_advanced.addWidget(self.option_dry_run)

        self.vspace_advanced = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_advanced.addItem(self.vspace_advanced)


        self.verticalLayout_23.addLayout(self.vlay_advanced)


        self.hlay_setup_options.addWidget(self.box_advanced)

        self.box_cosmetics = QGroupBox(self.tab_setup)
        self.box_cosmetics.setObjectName(u"box_cosmetics")
        sizePolicy2.setHeightForWidth(self.box_cosmetics.sizePolicy().hasHeightForWidth())
        self.box_cosmetics.setSizePolicy(sizePolicy2)
        self.verticalLayout_24 = QVBoxLayout(self.box_cosmetics)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.vlay_cosmetics = QVBoxLayout()
        self.vlay_cosmetics.setObjectName(u"vlay_cosmetics")
        self.option_tunic_swap = QCheckBox(self.box_cosmetics)
        self.option_tunic_swap.setObjectName(u"option_tunic_swap")

        self.vlay_cosmetics.addWidget(self.option_tunic_swap)

        self.option_lightning_skyward_strike = QCheckBox(self.box_cosmetics)
        self.option_lightning_skyward_strike.setObjectName(u"option_lightning_skyward_strike")

        self.vlay_cosmetics.addWidget(self.option_lightning_skyward_strike)

        self.option_starry_skies = QCheckBox(self.box_cosmetics)
        self.option_starry_skies.setObjectName(u"option_starry_skies")

        self.vlay_cosmetics.addWidget(self.option_starry_skies)

        self.hlay_star_count = QHBoxLayout()
        self.hlay_star_count.setObjectName(u"hlay_star_count")
        self.label_for_option_star_count = QLabel(self.box_cosmetics)
        self.label_for_option_star_count.setObjectName(u"label_for_option_star_count")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_for_option_star_count.sizePolicy().hasHeightForWidth())
        self.label_for_option_star_count.setSizePolicy(sizePolicy3)

        self.hlay_star_count.addWidget(self.label_for_option_star_count)

        self.option_star_count = QSpinBox(self.box_cosmetics)
        self.option_star_count.setObjectName(u"option_star_count")
        self.option_star_count.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.option_star_count.sizePolicy().hasHeightForWidth())
        self.option_star_count.setSizePolicy(sizePolicy4)
        self.option_star_count.setMaximum(32767)
        self.option_star_count.setSingleStep(100)

        self.hlay_star_count.addWidget(self.option_star_count)


        self.vlay_cosmetics.addLayout(self.hlay_star_count)

        self.label_for_option_interface = QLabel(self.box_cosmetics)
        self.label_for_option_interface.setObjectName(u"label_for_option_interface")

        self.vlay_cosmetics.addWidget(self.label_for_option_interface)

        self.option_interface = QComboBox(self.box_cosmetics)
        self.option_interface.setObjectName(u"option_interface")

        self.vlay_cosmetics.addWidget(self.option_interface)

        self.vspace_cosmetics = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_cosmetics.addItem(self.vspace_cosmetics)


        self.verticalLayout_24.addLayout(self.vlay_cosmetics)


        self.hlay_setup_options.addWidget(self.box_cosmetics)

        self.box_music_rando = QGroupBox(self.tab_setup)
        self.box_music_rando.setObjectName(u"box_music_rando")
        sizePolicy2.setHeightForWidth(self.box_music_rando.sizePolicy().hasHeightForWidth())
        self.box_music_rando.setSizePolicy(sizePolicy2)
        self.verticalLayout_25 = QVBoxLayout(self.box_music_rando)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.vlay_music_rando = QVBoxLayout()
        self.vlay_music_rando.setObjectName(u"vlay_music_rando")
        self.vlay_music_rando_option = QVBoxLayout()
        self.vlay_music_rando_option.setObjectName(u"vlay_music_rando_option")
        self.label_for_option_music_rando = QLabel(self.box_music_rando)
        self.label_for_option_music_rando.setObjectName(u"label_for_option_music_rando")

        self.vlay_music_rando_option.addWidget(self.label_for_option_music_rando)

        self.option_music_rando = QComboBox(self.box_music_rando)
        self.option_music_rando.setObjectName(u"option_music_rando")

        self.vlay_music_rando_option.addWidget(self.option_music_rando)


        self.vlay_music_rando.addLayout(self.vlay_music_rando_option)

        self.option_cutoff_gameover_music = QCheckBox(self.box_music_rando)
        self.option_cutoff_gameover_music.setObjectName(u"option_cutoff_gameover_music")

        self.vlay_music_rando.addWidget(self.option_cutoff_gameover_music)

        self.option_allow_custom_music = QCheckBox(self.box_music_rando)
        self.option_allow_custom_music.setObjectName(u"option_allow_custom_music")

        self.vlay_music_rando.addWidget(self.option_allow_custom_music)

        self.option_no_enemy_music = QCheckBox(self.box_music_rando)
        self.option_no_enemy_music.setObjectName(u"option_no_enemy_music")

        self.vlay_music_rando.addWidget(self.option_no_enemy_music)

        self.vspace_music_rando = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_music_rando.addItem(self.vspace_music_rando)


        self.verticalLayout_25.addLayout(self.vlay_music_rando)


        self.hlay_setup_options.addWidget(self.box_music_rando)

        self.box = QGroupBox(self.tab_setup)
        self.box.setObjectName(u"box")
        sizePolicy2.setHeightForWidth(self.box.sizePolicy().hasHeightForWidth())
        self.box.setSizePolicy(sizePolicy2)
        self.verticalLayout_28 = QVBoxLayout(self.box)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.vspace_10 = QSpacerItem(20, 342, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_28.addItem(self.vspace_10)


        self.hlay_setup_options.addWidget(self.box)


        self.verticalLayout_27.addLayout(self.hlay_setup_options)

        self.hlay_presets = QHBoxLayout()
        self.hlay_presets.setObjectName(u"hlay_presets")
        self.box_presets = QGroupBox(self.tab_setup)
        self.box_presets.setObjectName(u"box_presets")
        sizePolicy2.setHeightForWidth(self.box_presets.sizePolicy().hasHeightForWidth())
        self.box_presets.setSizePolicy(sizePolicy2)
        self.verticalLayout_26 = QVBoxLayout(self.box_presets)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.vlay_presets = QVBoxLayout()
        self.vlay_presets.setObjectName(u"vlay_presets")
        self.label_presets = QLabel(self.box_presets)
        self.label_presets.setObjectName(u"label_presets")
        self.label_presets.setWordWrap(False)

        self.vlay_presets.addWidget(self.label_presets)

        self.presets_list = QComboBox(self.box_presets)
        self.presets_list.setObjectName(u"presets_list")

        self.vlay_presets.addWidget(self.presets_list)

        self.hlay_presets_controls = QHBoxLayout()
        self.hlay_presets_controls.setObjectName(u"hlay_presets_controls")
        self.load_preset = QPushButton(self.box_presets)
        self.load_preset.setObjectName(u"load_preset")

        self.hlay_presets_controls.addWidget(self.load_preset)

        self.save_preset = QPushButton(self.box_presets)
        self.save_preset.setObjectName(u"save_preset")

        self.hlay_presets_controls.addWidget(self.save_preset)

        self.delete_preset = QPushButton(self.box_presets)
        self.delete_preset.setObjectName(u"delete_preset")

        self.hlay_presets_controls.addWidget(self.delete_preset)


        self.vlay_presets.addLayout(self.hlay_presets_controls)


        self.verticalLayout_26.addLayout(self.vlay_presets)


        self.hlay_presets.addWidget(self.box_presets)

        self.hspace_presets = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlay_presets.addItem(self.hspace_presets)


        self.verticalLayout_27.addLayout(self.hlay_presets)

        self.tabWidget.addTab(self.tab_setup, "")
        self.tab_randomization_settings = QWidget()
        self.tab_randomization_settings.setObjectName(u"tab_randomization_settings")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_randomization_settings)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.box_shuffles = QGroupBox(self.tab_randomization_settings)
        self.box_shuffles.setObjectName(u"box_shuffles")
        sizePolicy2.setHeightForWidth(self.box_shuffles.sizePolicy().hasHeightForWidth())
        self.box_shuffles.setSizePolicy(sizePolicy2)
        self.verticalLayout_17 = QVBoxLayout(self.box_shuffles)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.vlay_shuffles = QVBoxLayout()
        self.vlay_shuffles.setObjectName(u"vlay_shuffles")
        self.vlay_batreaux = QVBoxLayout()
        self.vlay_batreaux.setObjectName(u"vlay_batreaux")
        self.label_for_option_max_batreaux_reward = QLabel(self.box_shuffles)
        self.label_for_option_max_batreaux_reward.setObjectName(u"label_for_option_max_batreaux_reward")

        self.vlay_batreaux.addWidget(self.label_for_option_max_batreaux_reward)

        self.option_max_batreaux_reward = QComboBox(self.box_shuffles)
        self.option_max_batreaux_reward.setObjectName(u"option_max_batreaux_reward")

        self.vlay_batreaux.addWidget(self.option_max_batreaux_reward)


        self.vlay_shuffles.addLayout(self.vlay_batreaux)

        self.vlay_shopsanity = QVBoxLayout()
        self.vlay_shopsanity.setObjectName(u"vlay_shopsanity")
        self.label_for_option_shopsanity = QLabel(self.box_shuffles)
        self.label_for_option_shopsanity.setObjectName(u"label_for_option_shopsanity")

        self.vlay_shopsanity.addWidget(self.label_for_option_shopsanity)

        self.option_shopsanity = QComboBox(self.box_shuffles)
        self.option_shopsanity.setObjectName(u"option_shopsanity")

        self.vlay_shopsanity.addWidget(self.option_shopsanity)


        self.vlay_shuffles.addLayout(self.vlay_shopsanity)

        self.vlay_rupeesanity = QVBoxLayout()
        self.vlay_rupeesanity.setObjectName(u"vlay_rupeesanity")
        self.label_for_option_rupeesanity = QLabel(self.box_shuffles)
        self.label_for_option_rupeesanity.setObjectName(u"label_for_option_rupeesanity")

        self.vlay_rupeesanity.addWidget(self.label_for_option_rupeesanity)

        self.option_rupeesanity = QComboBox(self.box_shuffles)
        self.option_rupeesanity.setObjectName(u"option_rupeesanity")

        self.vlay_rupeesanity.addWidget(self.option_rupeesanity)


        self.vlay_shuffles.addLayout(self.vlay_rupeesanity)

        self.vspace_shuffles = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_shuffles.addItem(self.vspace_shuffles)


        self.verticalLayout_17.addLayout(self.vlay_shuffles)


        self.horizontalLayout_7.addWidget(self.box_shuffles)

        self.box_completion = QGroupBox(self.tab_randomization_settings)
        self.box_completion.setObjectName(u"box_completion")
        sizePolicy2.setHeightForWidth(self.box_completion.sizePolicy().hasHeightForWidth())
        self.box_completion.setSizePolicy(sizePolicy2)
        self.verticalLayout_18 = QVBoxLayout(self.box_completion)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.vlay_completion = QVBoxLayout()
        self.vlay_completion.setObjectName(u"vlay_completion")
        self.vlay_got_start = QVBoxLayout()
        self.vlay_got_start.setObjectName(u"vlay_got_start")
        self.label_for_option_got_starting_state = QLabel(self.box_completion)
        self.label_for_option_got_starting_state.setObjectName(u"label_for_option_got_starting_state")

        self.vlay_got_start.addWidget(self.label_for_option_got_starting_state)

        self.option_got_starting_state = QComboBox(self.box_completion)
        self.option_got_starting_state.setObjectName(u"option_got_starting_state")

        self.vlay_got_start.addWidget(self.option_got_starting_state)


        self.vlay_completion.addLayout(self.vlay_got_start)

        self.vlay_sword_req = QVBoxLayout()
        self.vlay_sword_req.setObjectName(u"vlay_sword_req")
        self.label_for_option_got_sword_requirement = QLabel(self.box_completion)
        self.label_for_option_got_sword_requirement.setObjectName(u"label_for_option_got_sword_requirement")

        self.vlay_sword_req.addWidget(self.label_for_option_got_sword_requirement)

        self.option_got_sword_requirement = QComboBox(self.box_completion)
        self.option_got_sword_requirement.setObjectName(u"option_got_sword_requirement")

        self.vlay_sword_req.addWidget(self.option_got_sword_requirement)


        self.vlay_completion.addLayout(self.vlay_sword_req)

        self.vlay_got_dungeon_req = QVBoxLayout()
        self.vlay_got_dungeon_req.setObjectName(u"vlay_got_dungeon_req")
        self.label_for_option_got_dungeon_requirement = QLabel(self.box_completion)
        self.label_for_option_got_dungeon_requirement.setObjectName(u"label_for_option_got_dungeon_requirement")

        self.vlay_got_dungeon_req.addWidget(self.label_for_option_got_dungeon_requirement)

        self.option_got_dungeon_requirement = QComboBox(self.box_completion)
        self.option_got_dungeon_requirement.setObjectName(u"option_got_dungeon_requirement")

        self.vlay_got_dungeon_req.addWidget(self.option_got_dungeon_requirement)


        self.vlay_completion.addLayout(self.vlay_got_dungeon_req)

        self.hlay_req_dungeons = QHBoxLayout()
        self.hlay_req_dungeons.setObjectName(u"hlay_req_dungeons")
        self.label_for_option_required_dungeon_count = QLabel(self.box_completion)
        self.label_for_option_required_dungeon_count.setObjectName(u"label_for_option_required_dungeon_count")

        self.hlay_req_dungeons.addWidget(self.label_for_option_required_dungeon_count)

        self.option_required_dungeon_count = QSpinBox(self.box_completion)
        self.option_required_dungeon_count.setObjectName(u"option_required_dungeon_count")
        self.option_required_dungeon_count.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.option_required_dungeon_count.sizePolicy().hasHeightForWidth())
        self.option_required_dungeon_count.setSizePolicy(sizePolicy5)
        self.option_required_dungeon_count.setMaximumSize(QSize(41, 16777215))

        self.hlay_req_dungeons.addWidget(self.option_required_dungeon_count)


        self.vlay_completion.addLayout(self.hlay_req_dungeons)

        self.option_triforce_required = QCheckBox(self.box_completion)
        self.option_triforce_required.setObjectName(u"option_triforce_required")

        self.vlay_completion.addWidget(self.option_triforce_required)

        self.vlay_triforce_shuffle = QVBoxLayout()
        self.vlay_triforce_shuffle.setObjectName(u"vlay_triforce_shuffle")
        self.label_for_option_triforce_shuffle = QLabel(self.box_completion)
        self.label_for_option_triforce_shuffle.setObjectName(u"label_for_option_triforce_shuffle")

        self.vlay_triforce_shuffle.addWidget(self.label_for_option_triforce_shuffle)

        self.option_triforce_shuffle = QComboBox(self.box_completion)
        self.option_triforce_shuffle.setObjectName(u"option_triforce_shuffle")

        self.vlay_triforce_shuffle.addWidget(self.option_triforce_shuffle)


        self.vlay_completion.addLayout(self.vlay_triforce_shuffle)

        self.option_imp_2 = QCheckBox(self.box_completion)
        self.option_imp_2.setObjectName(u"option_imp_2")

        self.vlay_completion.addWidget(self.option_imp_2)

        self.option_horde = QCheckBox(self.box_completion)
        self.option_horde.setObjectName(u"option_horde")

        self.vlay_completion.addWidget(self.option_horde)

        self.option_g3 = QCheckBox(self.box_completion)
        self.option_g3.setObjectName(u"option_g3")

        self.vlay_completion.addWidget(self.option_g3)

        self.option_demise = QCheckBox(self.box_completion)
        self.option_demise.setObjectName(u"option_demise")

        self.vlay_completion.addWidget(self.option_demise)

        self.hlay_demise_count = QHBoxLayout()
        self.hlay_demise_count.setObjectName(u"hlay_demise_count")
        self.label_for_option_demise_count = QLabel(self.box_completion)
        self.label_for_option_demise_count.setObjectName(u"label_for_option_demise_count")

        self.hlay_demise_count.addWidget(self.label_for_option_demise_count)

        self.option_demise_count = QSpinBox(self.box_completion)
        self.option_demise_count.setObjectName(u"option_demise_count")
        self.option_demise_count.setMaximumSize(QSize(41, 16777215))

        self.hlay_demise_count.addWidget(self.option_demise_count)


        self.vlay_completion.addLayout(self.hlay_demise_count)

        self.vspace_completion = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_completion.addItem(self.vspace_completion)


        self.verticalLayout_18.addLayout(self.vlay_completion)


        self.horizontalLayout_7.addWidget(self.box_completion)

        self.box_open = QGroupBox(self.tab_randomization_settings)
        self.box_open.setObjectName(u"box_open")
        sizePolicy2.setHeightForWidth(self.box_open.sizePolicy().hasHeightForWidth())
        self.box_open.setSizePolicy(sizePolicy2)
        self.verticalLayout_21 = QVBoxLayout(self.box_open)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.vlay_open = QVBoxLayout()
        self.vlay_open.setObjectName(u"vlay_open")
        self.vlay_open_thunderhead = QVBoxLayout()
        self.vlay_open_thunderhead.setObjectName(u"vlay_open_thunderhead")
        self.label_for_option_open_thunderhead = QLabel(self.box_open)
        self.label_for_option_open_thunderhead.setObjectName(u"label_for_option_open_thunderhead")

        self.vlay_open_thunderhead.addWidget(self.label_for_option_open_thunderhead)

        self.option_open_thunderhead = QComboBox(self.box_open)
        self.option_open_thunderhead.setObjectName(u"option_open_thunderhead")

        self.vlay_open_thunderhead.addWidget(self.option_open_thunderhead)


        self.vlay_open.addLayout(self.vlay_open_thunderhead)

        self.option_open_et = QCheckBox(self.box_open)
        self.option_open_et.setObjectName(u"option_open_et")

        self.vlay_open.addWidget(self.option_open_et)

        self.vlay_open_lmf = QVBoxLayout()
        self.vlay_open_lmf.setObjectName(u"vlay_open_lmf")
        self.label_for_option_open_lmf = QLabel(self.box_open)
        self.label_for_option_open_lmf.setObjectName(u"label_for_option_open_lmf")

        self.vlay_open_lmf.addWidget(self.label_for_option_open_lmf)

        self.option_open_lmf = QComboBox(self.box_open)
        self.option_open_lmf.setObjectName(u"option_open_lmf")

        self.vlay_open_lmf.addWidget(self.option_open_lmf)


        self.vlay_open.addLayout(self.vlay_open_lmf)

        self.hlay_starting_tablets = QHBoxLayout()
        self.hlay_starting_tablets.setObjectName(u"hlay_starting_tablets")
        self.label_for_option_starting_tablet_count = QLabel(self.box_open)
        self.label_for_option_starting_tablet_count.setObjectName(u"label_for_option_starting_tablet_count")

        self.hlay_starting_tablets.addWidget(self.label_for_option_starting_tablet_count)

        self.option_starting_tablet_count = QSpinBox(self.box_open)
        self.option_starting_tablet_count.setObjectName(u"option_starting_tablet_count")
        self.option_starting_tablet_count.setMaximumSize(QSize(41, 16777215))

        self.hlay_starting_tablets.addWidget(self.option_starting_tablet_count)


        self.vlay_open.addLayout(self.hlay_starting_tablets)

        self.label_for_option_open_lake_floria = QLabel(self.box_open)
        self.label_for_option_open_lake_floria.setObjectName(u"label_for_option_open_lake_floria")

        self.vlay_open.addWidget(self.label_for_option_open_lake_floria)

        self.option_open_lake_floria = QComboBox(self.box_open)
        self.option_open_lake_floria.setObjectName(u"option_open_lake_floria")

        self.vlay_open.addWidget(self.option_open_lake_floria)

        self.vspace_open = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_open.addItem(self.vspace_open)


        self.verticalLayout_21.addLayout(self.vlay_open)


        self.horizontalLayout_7.addWidget(self.box_open)

        self.box_entrance_rando = QGroupBox(self.tab_randomization_settings)
        self.box_entrance_rando.setObjectName(u"box_entrance_rando")
        sizePolicy2.setHeightForWidth(self.box_entrance_rando.sizePolicy().hasHeightForWidth())
        self.box_entrance_rando.setSizePolicy(sizePolicy2)
        self.verticalLayout_20 = QVBoxLayout(self.box_entrance_rando)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.vlay_entrance_rando = QVBoxLayout()
        self.vlay_entrance_rando.setObjectName(u"vlay_entrance_rando")
        self.vlay_dungeon_entrance_rando = QVBoxLayout()
        self.vlay_dungeon_entrance_rando.setObjectName(u"vlay_dungeon_entrance_rando")
        self.label_for_option_randomize_entrances = QLabel(self.box_entrance_rando)
        self.label_for_option_randomize_entrances.setObjectName(u"label_for_option_randomize_entrances")

        self.vlay_dungeon_entrance_rando.addWidget(self.label_for_option_randomize_entrances)

        self.option_randomize_entrances = QComboBox(self.box_entrance_rando)
        self.option_randomize_entrances.setObjectName(u"option_randomize_entrances")

        self.vlay_dungeon_entrance_rando.addWidget(self.option_randomize_entrances)


        self.vlay_entrance_rando.addLayout(self.vlay_dungeon_entrance_rando)

        self.option_randomize_trials = QCheckBox(self.box_entrance_rando)
        self.option_randomize_trials.setObjectName(u"option_randomize_trials")

        self.vlay_entrance_rando.addWidget(self.option_randomize_trials)

        self.vspace_entrance_rando = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.vlay_entrance_rando.addItem(self.vspace_entrance_rando)


        self.verticalLayout_20.addLayout(self.vlay_entrance_rando)


        self.horizontalLayout_7.addWidget(self.box_entrance_rando)

        self.box_dungeons = QGroupBox(self.tab_randomization_settings)
        self.box_dungeons.setObjectName(u"box_dungeons")
        sizePolicy2.setHeightForWidth(self.box_dungeons.sizePolicy().hasHeightForWidth())
        self.box_dungeons.setSizePolicy(sizePolicy2)
        self.verticalLayout_19 = QVBoxLayout(self.box_dungeons)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.vlay_dungeons = QVBoxLayout()
        self.vlay_dungeons.setObjectName(u"vlay_dungeons")
        self.vlay_map_shuffle = QVBoxLayout()
        self.vlay_map_shuffle.setObjectName(u"vlay_map_shuffle")
        self.label_for_option_map_mode = QLabel(self.box_dungeons)
        self.label_for_option_map_mode.setObjectName(u"label_for_option_map_mode")

        self.vlay_map_shuffle.addWidget(self.label_for_option_map_mode)

        self.option_map_mode = QComboBox(self.box_dungeons)
        self.option_map_mode.setObjectName(u"option_map_mode")

        self.vlay_map_shuffle.addWidget(self.option_map_mode)


        self.vlay_dungeons.addLayout(self.vlay_map_shuffle)

        self.vlay_small_key_shuffle = QVBoxLayout()
        self.vlay_small_key_shuffle.setObjectName(u"vlay_small_key_shuffle")
        self.label_for_option_small_key_mode = QLabel(self.box_dungeons)
        self.label_for_option_small_key_mode.setObjectName(u"label_for_option_small_key_mode")

        self.vlay_small_key_shuffle.addWidget(self.label_for_option_small_key_mode)

        self.option_small_key_mode = QComboBox(self.box_dungeons)
        self.option_small_key_mode.setObjectName(u"option_small_key_mode")

        self.vlay_small_key_shuffle.addWidget(self.option_small_key_mode)


        self.vlay_dungeons.addLayout(self.vlay_small_key_shuffle)

        self.vlay_boss_key_shuffle = QVBoxLayout()
        self.vlay_boss_key_shuffle.setObjectName(u"vlay_boss_key_shuffle")
        self.label_for_option_boss_key_mode = QLabel(self.box_dungeons)
        self.label_for_option_boss_key_mode.setObjectName(u"label_for_option_boss_key_mode")

        self.vlay_boss_key_shuffle.addWidget(self.label_for_option_boss_key_mode)

        self.option_boss_key_mode = QComboBox(self.box_dungeons)
        self.option_boss_key_mode.setObjectName(u"option_boss_key_mode")

        self.vlay_boss_key_shuffle.addWidget(self.option_boss_key_mode)


        self.vlay_dungeons.addLayout(self.vlay_boss_key_shuffle)

        self.option_empty_unrequired_dungeons = QCheckBox(self.box_dungeons)
        self.option_empty_unrequired_dungeons.setObjectName(u"option_empty_unrequired_dungeons")

        self.vlay_dungeons.addWidget(self.option_empty_unrequired_dungeons)

        self.vlay_sword_reward = QVBoxLayout()
        self.vlay_sword_reward.setObjectName(u"vlay_sword_reward")
        self.label_for_sword_dungeon_reward = QLabel(self.box_dungeons)
        self.label_for_sword_dungeon_reward.setObjectName(u"label_for_sword_dungeon_reward")

        self.vlay_sword_reward.addWidget(self.label_for_sword_dungeon_reward)

        self.option_sword_dungeon_reward = QComboBox(self.box_dungeons)
        self.option_sword_dungeon_reward.setObjectName(u"option_sword_dungeon_reward")

        self.vlay_sword_reward.addWidget(self.option_sword_dungeon_reward)


        self.vlay_dungeons.addLayout(self.vlay_sword_reward)

        self.vspace_dungeons = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_dungeons.addItem(self.vspace_dungeons)


        self.verticalLayout_19.addLayout(self.vlay_dungeons)


        self.horizontalLayout_7.addWidget(self.box_dungeons)

        self.tabWidget.addTab(self.tab_randomization_settings, "")
        self.tab_additional_settings = QWidget()
        self.tab_additional_settings.setObjectName(u"tab_additional_settings")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_additional_settings)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.box_convenience_tweaks = QGroupBox(self.tab_additional_settings)
        self.box_convenience_tweaks.setObjectName(u"box_convenience_tweaks")
        sizePolicy2.setHeightForWidth(self.box_convenience_tweaks.sizePolicy().hasHeightForWidth())
        self.box_convenience_tweaks.setSizePolicy(sizePolicy2)
        self.verticalLayout_4 = QVBoxLayout(self.box_convenience_tweaks)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.vlay_convenience_tweaks = QVBoxLayout()
        self.vlay_convenience_tweaks.setObjectName(u"vlay_convenience_tweaks")
        self.option_fill_dowsing_on_white_sword = QCheckBox(self.box_convenience_tweaks)
        self.option_fill_dowsing_on_white_sword.setObjectName(u"option_fill_dowsing_on_white_sword")

        self.vlay_convenience_tweaks.addWidget(self.option_fill_dowsing_on_white_sword)

        self.vspace_convenience_tweaks = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_convenience_tweaks.addItem(self.vspace_convenience_tweaks)


        self.verticalLayout_4.addLayout(self.vlay_convenience_tweaks)


        self.horizontalLayout_4.addWidget(self.box_convenience_tweaks)

        self.box_vanilla_tweaks = QGroupBox(self.tab_additional_settings)
        self.box_vanilla_tweaks.setObjectName(u"box_vanilla_tweaks")
        sizePolicy2.setHeightForWidth(self.box_vanilla_tweaks.sizePolicy().hasHeightForWidth())
        self.box_vanilla_tweaks.setSizePolicy(sizePolicy2)
        self.verticalLayout_8 = QVBoxLayout(self.box_vanilla_tweaks)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.vlay_vanilla_tweaks = QVBoxLayout()
        self.vlay_vanilla_tweaks.setObjectName(u"vlay_vanilla_tweaks")
        self.label_for_option_bit_patches = QLabel(self.box_vanilla_tweaks)
        self.label_for_option_bit_patches.setObjectName(u"label_for_option_bit_patches")

        self.vlay_vanilla_tweaks.addWidget(self.label_for_option_bit_patches)

        self.option_bit_patches = QComboBox(self.box_vanilla_tweaks)
        self.option_bit_patches.setObjectName(u"option_bit_patches")

        self.vlay_vanilla_tweaks.addWidget(self.option_bit_patches)

        self.vspace_vanilla_tweaks = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_vanilla_tweaks.addItem(self.vspace_vanilla_tweaks)


        self.verticalLayout_8.addLayout(self.vlay_vanilla_tweaks)


        self.horizontalLayout_4.addWidget(self.box_vanilla_tweaks)

        self.box_item_pool = QGroupBox(self.tab_additional_settings)
        self.box_item_pool.setObjectName(u"box_item_pool")
        sizePolicy2.setHeightForWidth(self.box_item_pool.sizePolicy().hasHeightForWidth())
        self.box_item_pool.setSizePolicy(sizePolicy2)
        self.verticalLayout_6 = QVBoxLayout(self.box_item_pool)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.vlay_item_pool = QVBoxLayout()
        self.vlay_item_pool.setObjectName(u"vlay_item_pool")
        self.vlay_rupoor_mode = QVBoxLayout()
        self.vlay_rupoor_mode.setObjectName(u"vlay_rupoor_mode")
        self.option_gondo_upgrades = QCheckBox(self.box_item_pool)
        self.option_gondo_upgrades.setObjectName(u"option_gondo_upgrades")

        self.vlay_rupoor_mode.addWidget(self.option_gondo_upgrades)

        self.label_for_option_rupoor_mode = QLabel(self.box_item_pool)
        self.label_for_option_rupoor_mode.setObjectName(u"label_for_option_rupoor_mode")

        self.vlay_rupoor_mode.addWidget(self.label_for_option_rupoor_mode)

        self.option_rupoor_mode = QComboBox(self.box_item_pool)
        self.option_rupoor_mode.setObjectName(u"option_rupoor_mode")

        self.vlay_rupoor_mode.addWidget(self.option_rupoor_mode)

        self.vspace_item_pool = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_rupoor_mode.addItem(self.vspace_item_pool)


        self.vlay_item_pool.addLayout(self.vlay_rupoor_mode)


        self.verticalLayout_6.addLayout(self.vlay_item_pool)


        self.horizontalLayout_4.addWidget(self.box_item_pool)

        self.box_silent_realms = QGroupBox(self.tab_additional_settings)
        self.box_silent_realms.setObjectName(u"box_silent_realms")
        sizePolicy2.setHeightForWidth(self.box_silent_realms.sizePolicy().hasHeightForWidth())
        self.box_silent_realms.setSizePolicy(sizePolicy2)
        self.verticalLayout_7 = QVBoxLayout(self.box_silent_realms)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.vlay_silent_realms = QVBoxLayout()
        self.vlay_silent_realms.setObjectName(u"vlay_silent_realms")
        self.verticalLayout_trialshuffle = QVBoxLayout()
        self.verticalLayout_trialshuffle.setObjectName(u"verticalLayout_trialshuffle")
        self.label_for_option_shuffle_trial_objects = QLabel(self.box_silent_realms)
        self.label_for_option_shuffle_trial_objects.setObjectName(u"label_for_option_shuffle_trial_objects")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_for_option_shuffle_trial_objects.sizePolicy().hasHeightForWidth())
        self.label_for_option_shuffle_trial_objects.setSizePolicy(sizePolicy6)

        self.verticalLayout_trialshuffle.addWidget(self.label_for_option_shuffle_trial_objects)

        self.option_shuffle_trial_objects = QComboBox(self.box_silent_realms)
        self.option_shuffle_trial_objects.setObjectName(u"option_shuffle_trial_objects")

        self.verticalLayout_trialshuffle.addWidget(self.option_shuffle_trial_objects)


        self.vlay_silent_realms.addLayout(self.verticalLayout_trialshuffle)

        self.vspace_silent_realms = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_silent_realms.addItem(self.vspace_silent_realms)


        self.verticalLayout_7.addLayout(self.vlay_silent_realms)


        self.horizontalLayout_4.addWidget(self.box_silent_realms)

        self.box_heromode_changes = QGroupBox(self.tab_additional_settings)
        self.box_heromode_changes.setObjectName(u"box_heromode_changes")
        sizePolicy2.setHeightForWidth(self.box_heromode_changes.sizePolicy().hasHeightForWidth())
        self.box_heromode_changes.setSizePolicy(sizePolicy2)
        self.verticalLayout_5 = QVBoxLayout(self.box_heromode_changes)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.vlay_heromode_changes = QVBoxLayout()
        self.vlay_heromode_changes.setObjectName(u"vlay_heromode_changes")
        self.option_upgraded_skyward_strike = QCheckBox(self.box_heromode_changes)
        self.option_upgraded_skyward_strike.setObjectName(u"option_upgraded_skyward_strike")

        self.vlay_heromode_changes.addWidget(self.option_upgraded_skyward_strike)

        self.option_fast_air_meter = QCheckBox(self.box_heromode_changes)
        self.option_fast_air_meter.setObjectName(u"option_fast_air_meter")

        self.vlay_heromode_changes.addWidget(self.option_fast_air_meter)

        self.option_enable_heart_drops = QCheckBox(self.box_heromode_changes)
        self.option_enable_heart_drops.setObjectName(u"option_enable_heart_drops")

        self.vlay_heromode_changes.addWidget(self.option_enable_heart_drops)

        self.hlay_damage_multiplier = QHBoxLayout()
        self.hlay_damage_multiplier.setObjectName(u"hlay_damage_multiplier")
        self.label_for_option_damage_multiplier = QLabel(self.box_heromode_changes)
        self.label_for_option_damage_multiplier.setObjectName(u"label_for_option_damage_multiplier")

        self.hlay_damage_multiplier.addWidget(self.label_for_option_damage_multiplier)

        self.option_damage_multiplier = QSpinBox(self.box_heromode_changes)
        self.option_damage_multiplier.setObjectName(u"option_damage_multiplier")
        self.option_damage_multiplier.setMaximumSize(QSize(41, 16777215))
        self.option_damage_multiplier.setMinimum(1)
        self.option_damage_multiplier.setMaximum(255)

        self.hlay_damage_multiplier.addWidget(self.option_damage_multiplier)


        self.vlay_heromode_changes.addLayout(self.hlay_damage_multiplier)

        self.vspace_heromode_changes = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_heromode_changes.addItem(self.vspace_heromode_changes)


        self.verticalLayout_5.addLayout(self.vlay_heromode_changes)


        self.horizontalLayout_4.addWidget(self.box_heromode_changes)

        self.tabWidget.addTab(self.tab_additional_settings, "")
        self.tab_logic_settings = QWidget()
        self.tab_logic_settings.setObjectName(u"tab_logic_settings")
        sizePolicy.setHeightForWidth(self.tab_logic_settings.sizePolicy().hasHeightForWidth())
        self.tab_logic_settings.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.tab_logic_settings)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.vlay_logic_settings = QVBoxLayout()
        self.vlay_logic_settings.setObjectName(u"vlay_logic_settings")
        self.hlay_misc_logic_settings = QHBoxLayout()
        self.hlay_misc_logic_settings.setObjectName(u"hlay_misc_logic_settings")
        self.label_for_option_logic_mode = QLabel(self.tab_logic_settings)
        self.label_for_option_logic_mode.setObjectName(u"label_for_option_logic_mode")

        self.hlay_misc_logic_settings.addWidget(self.label_for_option_logic_mode)

        self.option_logic_mode = QComboBox(self.tab_logic_settings)
        self.option_logic_mode.setObjectName(u"option_logic_mode")

        self.hlay_misc_logic_settings.addWidget(self.option_logic_mode)

        self.edit_tricks = QPushButton(self.tab_logic_settings)
        self.edit_tricks.setObjectName(u"edit_tricks")

        self.hlay_misc_logic_settings.addWidget(self.edit_tricks)

        self.hspace_misc_logic_settings = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlay_misc_logic_settings.addItem(self.hspace_misc_logic_settings)


        self.vlay_logic_settings.addLayout(self.hlay_misc_logic_settings)

        self.vlay_exclude_locations = QVBoxLayout()
        self.vlay_exclude_locations.setSpacing(6)
        self.vlay_exclude_locations.setObjectName(u"vlay_exclude_locations")
        self.hlay_exclude_locations_body = QHBoxLayout()
        self.hlay_exclude_locations_body.setObjectName(u"hlay_exclude_locations_body")
        self.vlay_include_locations = QVBoxLayout()
        self.vlay_include_locations.setObjectName(u"vlay_include_locations")
        self.label_include_locations = QLabel(self.tab_logic_settings)
        self.label_include_locations.setObjectName(u"label_include_locations")

        self.vlay_include_locations.addWidget(self.label_include_locations)

        self.hlay_include_filters = QHBoxLayout()
        self.hlay_include_filters.setObjectName(u"hlay_include_filters")
        self.included_free_search = QLineEdit(self.tab_logic_settings)
        self.included_free_search.setObjectName(u"included_free_search")
        sizePolicy4.setHeightForWidth(self.included_free_search.sizePolicy().hasHeightForWidth())
        self.included_free_search.setSizePolicy(sizePolicy4)
        self.included_free_search.setClearButtonEnabled(True)

        self.hlay_include_filters.addWidget(self.included_free_search)

        self.include_category_filters = QComboBox(self.tab_logic_settings)
        self.include_category_filters.setObjectName(u"include_category_filters")

        self.hlay_include_filters.addWidget(self.include_category_filters)


        self.vlay_include_locations.addLayout(self.hlay_include_filters)

        self.included_locations = QListView(self.tab_logic_settings)
        self.included_locations.setObjectName(u"included_locations")
        self.included_locations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.included_locations.setProperty("showDropIndicator", False)
        self.included_locations.setSelectionMode(QAbstractItemView.MultiSelection)
        self.included_locations.setSelectionRectVisible(False)

        self.vlay_include_locations.addWidget(self.included_locations)


        self.hlay_exclude_locations_body.addLayout(self.vlay_include_locations)

        self.vlay_exclude_locations_controls = QVBoxLayout()
        self.vlay_exclude_locations_controls.setObjectName(u"vlay_exclude_locations_controls")
        self.vspace_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_exclude_locations_controls.addItem(self.vspace_9)

        self.include_location = QPushButton(self.tab_logic_settings)
        self.include_location.setObjectName(u"include_location")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.include_location.sizePolicy().hasHeightForWidth())
        self.include_location.setSizePolicy(sizePolicy7)

        self.vlay_exclude_locations_controls.addWidget(self.include_location)

        self.vspace_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_exclude_locations_controls.addItem(self.vspace_7)

        self.exclude_location = QPushButton(self.tab_logic_settings)
        self.exclude_location.setObjectName(u"exclude_location")
        sizePolicy7.setHeightForWidth(self.exclude_location.sizePolicy().hasHeightForWidth())
        self.exclude_location.setSizePolicy(sizePolicy7)

        self.vlay_exclude_locations_controls.addWidget(self.exclude_location)

        self.vspace_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_exclude_locations_controls.addItem(self.vspace_8)


        self.hlay_exclude_locations_body.addLayout(self.vlay_exclude_locations_controls)

        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.label_exclude_locations = QLabel(self.tab_logic_settings)
        self.label_exclude_locations.setObjectName(u"label_exclude_locations")

        self.verticalLayout_30.addWidget(self.label_exclude_locations)

        self.hlay_exclude_filters = QHBoxLayout()
        self.hlay_exclude_filters.setObjectName(u"hlay_exclude_filters")
        self.excluded_free_search = QLineEdit(self.tab_logic_settings)
        self.excluded_free_search.setObjectName(u"excluded_free_search")
        sizePolicy4.setHeightForWidth(self.excluded_free_search.sizePolicy().hasHeightForWidth())
        self.excluded_free_search.setSizePolicy(sizePolicy4)
        self.excluded_free_search.setClearButtonEnabled(True)

        self.hlay_exclude_filters.addWidget(self.excluded_free_search)

        self.exclude_category_filters = QComboBox(self.tab_logic_settings)
        self.exclude_category_filters.setObjectName(u"exclude_category_filters")

        self.hlay_exclude_filters.addWidget(self.exclude_category_filters)


        self.verticalLayout_30.addLayout(self.hlay_exclude_filters)

        self.excluded_locations = QListView(self.tab_logic_settings)
        self.excluded_locations.setObjectName(u"excluded_locations")
        self.excluded_locations.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.excluded_locations.setProperty("showDropIndicator", False)
        self.excluded_locations.setSelectionMode(QAbstractItemView.MultiSelection)
        self.excluded_locations.setSelectionRectVisible(False)

        self.verticalLayout_30.addWidget(self.excluded_locations)


        self.hlay_exclude_locations_body.addLayout(self.verticalLayout_30)


        self.vlay_exclude_locations.addLayout(self.hlay_exclude_locations_body)


        self.vlay_logic_settings.addLayout(self.vlay_exclude_locations)


        self.horizontalLayout.addLayout(self.vlay_logic_settings)

        self.tabWidget.addTab(self.tab_logic_settings, "")
        self.tab_hints = QWidget()
        self.tab_hints.setObjectName(u"tab_hints")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_hints)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.box_stone_hints = QGroupBox(self.tab_hints)
        self.box_stone_hints.setObjectName(u"box_stone_hints")
        sizePolicy2.setHeightForWidth(self.box_stone_hints.sizePolicy().hasHeightForWidth())
        self.box_stone_hints.setSizePolicy(sizePolicy2)
        self.verticalLayout_12 = QVBoxLayout(self.box_stone_hints)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.vlay_stone_hints = QVBoxLayout()
        self.vlay_stone_hints.setObjectName(u"vlay_stone_hints")
        self.vlay_hint_distro = QVBoxLayout()
        self.vlay_hint_distro.setObjectName(u"vlay_hint_distro")
        self.label_for_option_hint_distribution = QLabel(self.box_stone_hints)
        self.label_for_option_hint_distribution.setObjectName(u"label_for_option_hint_distribution")

        self.vlay_hint_distro.addWidget(self.label_for_option_hint_distribution)

        self.option_hint_distribution = QComboBox(self.box_stone_hints)
        self.option_hint_distribution.setObjectName(u"option_hint_distribution")

        self.vlay_hint_distro.addWidget(self.option_hint_distribution)


        self.vlay_stone_hints.addLayout(self.vlay_hint_distro)

        self.option_cube_sots = QCheckBox(self.box_stone_hints)
        self.option_cube_sots.setObjectName(u"option_cube_sots")

        self.vlay_stone_hints.addWidget(self.option_cube_sots)

        self.option_precise_item = QCheckBox(self.box_stone_hints)
        self.option_precise_item.setObjectName(u"option_precise_item")

        self.vlay_stone_hints.addWidget(self.option_precise_item)

        self.vspace_stone_hints = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_stone_hints.addItem(self.vspace_stone_hints)


        self.verticalLayout_12.addLayout(self.vlay_stone_hints)


        self.horizontalLayout_6.addWidget(self.box_stone_hints)

        self.box_other_hints = QGroupBox(self.tab_hints)
        self.box_other_hints.setObjectName(u"box_other_hints")
        sizePolicy2.setHeightForWidth(self.box_other_hints.sizePolicy().hasHeightForWidth())
        self.box_other_hints.setSizePolicy(sizePolicy2)
        self.verticalLayout_13 = QVBoxLayout(self.box_other_hints)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.vlay_other_hints = QVBoxLayout()
        self.vlay_other_hints.setObjectName(u"vlay_other_hints")
        self.vlay_song_hints = QVBoxLayout()
        self.vlay_song_hints.setObjectName(u"vlay_song_hints")
        self.label_for_option_song_hints = QLabel(self.box_other_hints)
        self.label_for_option_song_hints.setObjectName(u"label_for_option_song_hints")

        self.vlay_song_hints.addWidget(self.label_for_option_song_hints)

        self.option_song_hints = QComboBox(self.box_other_hints)
        self.option_song_hints.setObjectName(u"option_song_hints")

        self.vlay_song_hints.addWidget(self.option_song_hints)


        self.vlay_other_hints.addLayout(self.vlay_song_hints)

        self.option_impa_sot_hint = QCheckBox(self.box_other_hints)
        self.option_impa_sot_hint.setObjectName(u"option_impa_sot_hint")

        self.vlay_other_hints.addWidget(self.option_impa_sot_hint)

        self.vlay_chest_dowsing = QVBoxLayout()
        self.vlay_chest_dowsing.setObjectName(u"vlay_chest_dowsing")
        self.label_for_option_chest_dowsing = QLabel(self.box_other_hints)
        self.label_for_option_chest_dowsing.setObjectName(u"label_for_option_chest_dowsing")

        self.vlay_chest_dowsing.addWidget(self.label_for_option_chest_dowsing)

        self.option_chest_dowsing = QComboBox(self.box_other_hints)
        self.option_chest_dowsing.setObjectName(u"option_chest_dowsing")

        self.vlay_chest_dowsing.addWidget(self.option_chest_dowsing)


        self.vlay_other_hints.addLayout(self.vlay_chest_dowsing)

        self.option_dungeon_dowsing = QCheckBox(self.box_other_hints)
        self.option_dungeon_dowsing.setObjectName(u"option_dungeon_dowsing")

        self.vlay_other_hints.addWidget(self.option_dungeon_dowsing)

        self.vspace_other_hints = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_other_hints.addItem(self.vspace_other_hints)


        self.verticalLayout_13.addLayout(self.vlay_other_hints)


        self.horizontalLayout_6.addWidget(self.box_other_hints)

        self.box_4 = QGroupBox(self.tab_hints)
        self.box_4.setObjectName(u"box_4")
        sizePolicy2.setHeightForWidth(self.box_4.sizePolicy().hasHeightForWidth())
        self.box_4.setSizePolicy(sizePolicy2)
        self.verticalLayout_14 = QVBoxLayout(self.box_4)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.vspace_4 = QSpacerItem(20, 533, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.vspace_4)


        self.horizontalLayout_6.addWidget(self.box_4)

        self.box_5 = QGroupBox(self.tab_hints)
        self.box_5.setObjectName(u"box_5")
        sizePolicy2.setHeightForWidth(self.box_5.sizePolicy().hasHeightForWidth())
        self.box_5.setSizePolicy(sizePolicy2)
        self.verticalLayout_15 = QVBoxLayout(self.box_5)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.vspace_5 = QSpacerItem(20, 533, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.vspace_5)


        self.horizontalLayout_6.addWidget(self.box_5)

        self.box_6 = QGroupBox(self.tab_hints)
        self.box_6.setObjectName(u"box_6")
        sizePolicy2.setHeightForWidth(self.box_6.sizePolicy().hasHeightForWidth())
        self.box_6.setSizePolicy(sizePolicy2)
        self.verticalLayout_16 = QVBoxLayout(self.box_6)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.vspace_6 = QSpacerItem(20, 533, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_16.addItem(self.vspace_6)


        self.horizontalLayout_6.addWidget(self.box_6)

        self.tabWidget.addTab(self.tab_hints, "")
        self.tab_starting_items = QWidget()
        self.tab_starting_items.setObjectName(u"tab_starting_items")
        self.horizontalLayout_8 = QHBoxLayout(self.tab_starting_items)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.vlay_starting_items = QVBoxLayout()
        self.vlay_starting_items.setObjectName(u"vlay_starting_items")
        self.hlay_starting_items_body = QHBoxLayout()
        self.hlay_starting_items_body.setObjectName(u"hlay_starting_items_body")
        self.vlay_randomized_items_section = QVBoxLayout()
        self.vlay_randomized_items_section.setObjectName(u"vlay_randomized_items_section")
        self.label_randomized_items = QLabel(self.tab_starting_items)
        self.label_randomized_items.setObjectName(u"label_randomized_items")

        self.vlay_randomized_items_section.addWidget(self.label_randomized_items)

        self.randomized_items_free_search = QLineEdit(self.tab_starting_items)
        self.randomized_items_free_search.setObjectName(u"randomized_items_free_search")
        self.randomized_items_free_search.setClearButtonEnabled(True)

        self.vlay_randomized_items_section.addWidget(self.randomized_items_free_search)

        self.randomized_items = QListView(self.tab_starting_items)
        self.randomized_items.setObjectName(u"randomized_items")
        sizePolicy1.setHeightForWidth(self.randomized_items.sizePolicy().hasHeightForWidth())
        self.randomized_items.setSizePolicy(sizePolicy1)
        self.randomized_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.randomized_items.setProperty("showDropIndicator", False)
        self.randomized_items.setSelectionMode(QAbstractItemView.MultiSelection)
        self.randomized_items.setSelectionRectVisible(False)

        self.vlay_randomized_items_section.addWidget(self.randomized_items)


        self.hlay_starting_items_body.addLayout(self.vlay_randomized_items_section)

        self.vlay_starting_items_controls = QVBoxLayout()
        self.vlay_starting_items_controls.setObjectName(u"vlay_starting_items_controls")
        self.vlay_starting_items_controls.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.vspace_starting_items_controls_upper = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_starting_items_controls.addItem(self.vspace_starting_items_controls_upper)

        self.randomize_item = QPushButton(self.tab_starting_items)
        self.randomize_item.setObjectName(u"randomize_item")
        sizePolicy7.setHeightForWidth(self.randomize_item.sizePolicy().hasHeightForWidth())
        self.randomize_item.setSizePolicy(sizePolicy7)

        self.vlay_starting_items_controls.addWidget(self.randomize_item)

        self.vspace_starting_items_controls_middle = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_starting_items_controls.addItem(self.vspace_starting_items_controls_middle)

        self.start_with_item = QPushButton(self.tab_starting_items)
        self.start_with_item.setObjectName(u"start_with_item")
        sizePolicy7.setHeightForWidth(self.start_with_item.sizePolicy().hasHeightForWidth())
        self.start_with_item.setSizePolicy(sizePolicy7)

        self.vlay_starting_items_controls.addWidget(self.start_with_item)

        self.vspace_starting_items_controls_lower = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_starting_items_controls.addItem(self.vspace_starting_items_controls_lower)


        self.hlay_starting_items_body.addLayout(self.vlay_starting_items_controls)

        self.vlay_starting_items_section = QVBoxLayout()
        self.vlay_starting_items_section.setObjectName(u"vlay_starting_items_section")
        self.label_starting_items = QLabel(self.tab_starting_items)
        self.label_starting_items.setObjectName(u"label_starting_items")

        self.vlay_starting_items_section.addWidget(self.label_starting_items)

        self.starting_items_free_search = QLineEdit(self.tab_starting_items)
        self.starting_items_free_search.setObjectName(u"starting_items_free_search")
        self.starting_items_free_search.setClearButtonEnabled(True)

        self.vlay_starting_items_section.addWidget(self.starting_items_free_search)

        self.starting_items = QListView(self.tab_starting_items)
        self.starting_items.setObjectName(u"starting_items")
        sizePolicy1.setHeightForWidth(self.starting_items.sizePolicy().hasHeightForWidth())
        self.starting_items.setSizePolicy(sizePolicy1)
        self.starting_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.starting_items.setProperty("showDropIndicator", False)
        self.starting_items.setSelectionMode(QAbstractItemView.MultiSelection)
        self.starting_items.setSelectionRectVisible(False)

        self.vlay_starting_items_section.addWidget(self.starting_items)


        self.hlay_starting_items_body.addLayout(self.vlay_starting_items_section)


        self.vlay_starting_items.addLayout(self.hlay_starting_items_body)

        self.line_starting_items_divider = QFrame(self.tab_starting_items)
        self.line_starting_items_divider.setObjectName(u"line_starting_items_divider")
        self.line_starting_items_divider.setFrameShape(QFrame.HLine)
        self.line_starting_items_divider.setFrameShadow(QFrame.Sunken)

        self.vlay_starting_items.addWidget(self.line_starting_items_divider)

        self.hlay_starting_items_misc_options = QHBoxLayout()
        self.hlay_starting_items_misc_options.setObjectName(u"hlay_starting_items_misc_options")
        self.hlay_starting_items_misc_options.setContentsMargins(-1, -1, -1, 0)
        self.hlay_starting_sword = QHBoxLayout()
        self.hlay_starting_sword.setObjectName(u"hlay_starting_sword")
        self.label_for_option_starting_sword = QLabel(self.tab_starting_items)
        self.label_for_option_starting_sword.setObjectName(u"label_for_option_starting_sword")

        self.hlay_starting_sword.addWidget(self.label_for_option_starting_sword)

        self.option_starting_sword = QComboBox(self.tab_starting_items)
        self.option_starting_sword.setObjectName(u"option_starting_sword")

        self.hlay_starting_sword.addWidget(self.option_starting_sword)


        self.hlay_starting_items_misc_options.addLayout(self.hlay_starting_sword)

        self.option_random_starting_item = QCheckBox(self.tab_starting_items)
        self.option_random_starting_item.setObjectName(u"option_random_starting_item")
        sizePolicy5.setHeightForWidth(self.option_random_starting_item.sizePolicy().hasHeightForWidth())
        self.option_random_starting_item.setSizePolicy(sizePolicy5)

        self.hlay_starting_items_misc_options.addWidget(self.option_random_starting_item)

        self.hlay_heart_containters = QHBoxLayout()
        self.hlay_heart_containters.setObjectName(u"hlay_heart_containters")
        self.label_for_option_starting_heart_containers = QLabel(self.tab_starting_items)
        self.label_for_option_starting_heart_containers.setObjectName(u"label_for_option_starting_heart_containers")
        sizePolicy6.setHeightForWidth(self.label_for_option_starting_heart_containers.sizePolicy().hasHeightForWidth())
        self.label_for_option_starting_heart_containers.setSizePolicy(sizePolicy6)

        self.hlay_heart_containters.addWidget(self.label_for_option_starting_heart_containers)

        self.option_starting_heart_containers = QSpinBox(self.tab_starting_items)
        self.option_starting_heart_containers.setObjectName(u"option_starting_heart_containers")
        sizePolicy5.setHeightForWidth(self.option_starting_heart_containers.sizePolicy().hasHeightForWidth())
        self.option_starting_heart_containers.setSizePolicy(sizePolicy5)
        self.option_starting_heart_containers.setMaximumSize(QSize(41, 16777215))

        self.hlay_heart_containters.addWidget(self.option_starting_heart_containers)


        self.hlay_starting_items_misc_options.addLayout(self.hlay_heart_containters)

        self.hlay_heart_pieces = QHBoxLayout()
        self.hlay_heart_pieces.setObjectName(u"hlay_heart_pieces")
        self.label_for_option_starting_heart_pieces = QLabel(self.tab_starting_items)
        self.label_for_option_starting_heart_pieces.setObjectName(u"label_for_option_starting_heart_pieces")
        sizePolicy6.setHeightForWidth(self.label_for_option_starting_heart_pieces.sizePolicy().hasHeightForWidth())
        self.label_for_option_starting_heart_pieces.setSizePolicy(sizePolicy6)

        self.hlay_heart_pieces.addWidget(self.label_for_option_starting_heart_pieces)

        self.option_starting_heart_pieces = QSpinBox(self.tab_starting_items)
        self.option_starting_heart_pieces.setObjectName(u"option_starting_heart_pieces")
        sizePolicy5.setHeightForWidth(self.option_starting_heart_pieces.sizePolicy().hasHeightForWidth())
        self.option_starting_heart_pieces.setSizePolicy(sizePolicy5)
        self.option_starting_heart_pieces.setMaximumSize(QSize(41, 16777215))

        self.hlay_heart_pieces.addWidget(self.option_starting_heart_pieces)


        self.hlay_starting_items_misc_options.addLayout(self.hlay_heart_pieces)

        self.label_current_starting_health = QLabel(self.tab_starting_items)
        self.label_current_starting_health.setObjectName(u"label_current_starting_health")

        self.hlay_starting_items_misc_options.addWidget(self.label_current_starting_health)

        self.current_starting_health_counter = QLabel(self.tab_starting_items)
        self.current_starting_health_counter.setObjectName(u"current_starting_health_counter")

        self.hlay_starting_items_misc_options.addWidget(self.current_starting_health_counter)

        self.hspace_starting_items_misc = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlay_starting_items_misc_options.addItem(self.hspace_starting_items_misc)


        self.vlay_starting_items.addLayout(self.hlay_starting_items_misc_options)


        self.horizontalLayout_8.addLayout(self.vlay_starting_items)

        self.tabWidget.addTab(self.tab_starting_items, "")
        self.tab_accessibility = QWidget()
        self.tab_accessibility.setObjectName(u"tab_accessibility")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_accessibility)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.box_theme = QGroupBox(self.tab_accessibility)
        self.box_theme.setObjectName(u"box_theme")
        sizePolicy2.setHeightForWidth(self.box_theme.sizePolicy().hasHeightForWidth())
        self.box_theme.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.box_theme)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.vlay_theme = QVBoxLayout()
        self.vlay_theme.setObjectName(u"vlay_theme")
        self.theme_mode_label = QLabel(self.box_theme)
        self.theme_mode_label.setObjectName(u"theme_mode_label")

        self.vlay_theme.addWidget(self.theme_mode_label)

        self.option_theme_mode = QComboBox(self.box_theme)
        self.option_theme_mode.setObjectName(u"option_theme_mode")

        self.vlay_theme.addWidget(self.option_theme_mode)

        self.theme_presets_label = QLabel(self.box_theme)
        self.theme_presets_label.setObjectName(u"theme_presets_label")

        self.vlay_theme.addWidget(self.theme_presets_label)

        self.option_theme_presets = QComboBox(self.box_theme)
        self.option_theme_presets.setObjectName(u"option_theme_presets")

        self.vlay_theme.addWidget(self.option_theme_presets)

        self.option_use_custom_theme = QCheckBox(self.box_theme)
        self.option_use_custom_theme.setObjectName(u"option_use_custom_theme")

        self.vlay_theme.addWidget(self.option_use_custom_theme)

        self.custom_theme_button = QPushButton(self.box_theme)
        self.custom_theme_button.setObjectName(u"custom_theme_button")
        self.custom_theme_button.setEnabled(False)

        self.vlay_theme.addWidget(self.custom_theme_button)

        self.option_use_sharp_corners = QCheckBox(self.box_theme)
        self.option_use_sharp_corners.setObjectName(u"option_use_sharp_corners")

        self.vlay_theme.addWidget(self.option_use_sharp_corners)

        self.vspace_theme = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_theme.addItem(self.vspace_theme)


        self.verticalLayout_3.addLayout(self.vlay_theme)


        self.horizontalLayout_3.addWidget(self.box_theme)

        self.box_font = QGroupBox(self.tab_accessibility)
        self.box_font.setObjectName(u"box_font")
        sizePolicy2.setHeightForWidth(self.box_font.sizePolicy().hasHeightForWidth())
        self.box_font.setSizePolicy(sizePolicy2)
        self.verticalLayout_2 = QVBoxLayout(self.box_font)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.vlay_font = QVBoxLayout()
        self.vlay_font.setObjectName(u"vlay_font")
        self.label_for_option_font_family = QLabel(self.box_font)
        self.label_for_option_font_family.setObjectName(u"label_for_option_font_family")
        self.label_for_option_font_family.setFont(font)

        self.vlay_font.addWidget(self.label_for_option_font_family)

        self.option_font_family = QFontComboBox(self.box_font)
        self.option_font_family.setObjectName(u"option_font_family")
        sizePolicy8 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.option_font_family.sizePolicy().hasHeightForWidth())
        self.option_font_family.setSizePolicy(sizePolicy8)
        self.option_font_family.setEditable(False)
        self.option_font_family.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.option_font_family.setWritingSystem(QFontDatabase.Any)
        self.option_font_family.setFontFilters(QFontComboBox.ScalableFonts)
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        self.option_font_family.setCurrentFont(font1)

        self.vlay_font.addWidget(self.option_font_family)

        self.hlay_font_size = QHBoxLayout()
        self.hlay_font_size.setObjectName(u"hlay_font_size")
        self.label_for_option_font_size = QLabel(self.box_font)
        self.label_for_option_font_size.setObjectName(u"label_for_option_font_size")
        sizePolicy.setHeightForWidth(self.label_for_option_font_size.sizePolicy().hasHeightForWidth())
        self.label_for_option_font_size.setSizePolicy(sizePolicy)

        self.hlay_font_size.addWidget(self.label_for_option_font_size)

        self.option_font_size = QSpinBox(self.box_font)
        self.option_font_size.setObjectName(u"option_font_size")
        sizePolicy5.setHeightForWidth(self.option_font_size.sizePolicy().hasHeightForWidth())
        self.option_font_size.setSizePolicy(sizePolicy5)

        self.hlay_font_size.addWidget(self.option_font_size)


        self.vlay_font.addLayout(self.hlay_font_size)

        self.reset_font_button = QPushButton(self.box_font)
        self.reset_font_button.setObjectName(u"reset_font_button")
        sizePolicy5.setHeightForWidth(self.reset_font_button.sizePolicy().hasHeightForWidth())
        self.reset_font_button.setSizePolicy(sizePolicy5)

        self.vlay_font.addWidget(self.reset_font_button)

        self.vspace_font = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_font.addItem(self.vspace_font)


        self.verticalLayout_2.addLayout(self.vlay_font)


        self.horizontalLayout_3.addWidget(self.box_font)

        self.box_1 = QGroupBox(self.tab_accessibility)
        self.box_1.setObjectName(u"box_1")
        self.box_1.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.box_1.sizePolicy().hasHeightForWidth())
        self.box_1.setSizePolicy(sizePolicy2)
        self.box_1.setFlat(False)
        self.verticalLayout_9 = QVBoxLayout(self.box_1)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.vspace = QSpacerItem(20, 533, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.vspace)


        self.horizontalLayout_3.addWidget(self.box_1)

        self.box_2 = QGroupBox(self.tab_accessibility)
        self.box_2.setObjectName(u"box_2")
        self.box_2.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.box_2.sizePolicy().hasHeightForWidth())
        self.box_2.setSizePolicy(sizePolicy2)
        self.box_2.setFlat(False)
        self.verticalLayout_10 = QVBoxLayout(self.box_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.vspace_2 = QSpacerItem(20, 533, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.vspace_2)


        self.horizontalLayout_3.addWidget(self.box_2)

        self.box_3 = QGroupBox(self.tab_accessibility)
        self.box_3.setObjectName(u"box_3")
        self.box_3.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.box_3.sizePolicy().hasHeightForWidth())
        self.box_3.setSizePolicy(sizePolicy2)
        self.box_3.setFlat(False)
        self.verticalLayout_11 = QVBoxLayout(self.box_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.vspace_3 = QSpacerItem(20, 533, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.vspace_3)


        self.horizontalLayout_3.addWidget(self.box_3)

        self.tabWidget.addTab(self.tab_accessibility, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.option_description = QLabel(self.centralwidget)
        self.option_description.setObjectName(u"option_description")
        self.option_description.setEnabled(True)
        sizePolicy9 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.option_description.sizePolicy().hasHeightForWidth())
        self.option_description.setSizePolicy(sizePolicy9)
        self.option_description.setMinimumSize(QSize(0, 48))
        self.option_description.setStyleSheet(u"")
        self.option_description.setTextFormat(Qt.PlainText)
        self.option_description.setWordWrap(True)

        self.verticalLayout.addWidget(self.option_description)

        self.vlay_bottom_controls = QVBoxLayout()
        self.vlay_bottom_controls.setObjectName(u"vlay_bottom_controls")
        self.hlay_permalink = QHBoxLayout()
        self.hlay_permalink.setObjectName(u"hlay_permalink")
        self.label_permalink = QLabel(self.centralwidget)
        self.label_permalink.setObjectName(u"label_permalink")

        self.hlay_permalink.addWidget(self.label_permalink)

        self.permalink = QLineEdit(self.centralwidget)
        self.permalink.setObjectName(u"permalink")

        self.hlay_permalink.addWidget(self.permalink)

        self.copy_permalink_button = QPushButton(self.centralwidget)
        self.copy_permalink_button.setObjectName(u"copy_permalink_button")

        self.hlay_permalink.addWidget(self.copy_permalink_button)


        self.vlay_bottom_controls.addLayout(self.hlay_permalink)

        self.hlay_seed = QHBoxLayout()
        self.hlay_seed.setObjectName(u"hlay_seed")
        self.label_seed = QLabel(self.centralwidget)
        self.label_seed.setObjectName(u"label_seed")
        self.label_seed.setToolTipDuration(-1)
        self.label_seed.setLayoutDirection(Qt.LeftToRight)
        self.label_seed.setAutoFillBackground(False)
        self.label_seed.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.hlay_seed.addWidget(self.label_seed)

        self.seed = QLineEdit(self.centralwidget)
        self.seed.setObjectName(u"seed")

        self.hlay_seed.addWidget(self.seed)

        self.seed_button = QPushButton(self.centralwidget)
        self.seed_button.setObjectName(u"seed_button")

        self.hlay_seed.addWidget(self.seed_button)


        self.vlay_bottom_controls.addLayout(self.hlay_seed)

        self.hlay_button_row = QHBoxLayout()
        self.hlay_button_row.setObjectName(u"hlay_button_row")
        self.randomize_button = QPushButton(self.centralwidget)
        self.randomize_button.setObjectName(u"randomize_button")

        self.hlay_button_row.addWidget(self.randomize_button)


        self.vlay_bottom_controls.addLayout(self.hlay_button_row)


        self.verticalLayout.addLayout(self.vlay_bottom_controls)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)
        self.option_triforce_shuffle.setCurrentIndex(-1)
        self.option_randomize_entrances.setCurrentIndex(-1)
        self.option_chest_dowsing.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Skyward Sword Randomizer", None))
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
        self.option_lightning_skyward_strike.setText(QCoreApplication.translate("MainWindow", u"Lightning Skyward Strike", None))
        self.option_starry_skies.setText(QCoreApplication.translate("MainWindow", u"Starry Skies", None))
        self.label_for_option_star_count.setText(QCoreApplication.translate("MainWindow", u"Number of stars", None))
        self.label_for_option_interface.setText(QCoreApplication.translate("MainWindow", u"Starting Interface", None))
        self.box_music_rando.setTitle(QCoreApplication.translate("MainWindow", u"Randomize Music", None))
        self.label_for_option_music_rando.setText(QCoreApplication.translate("MainWindow", u"Randomize Music", None))
        self.option_cutoff_gameover_music.setText(QCoreApplication.translate("MainWindow", u"Cutoff Game Over Music", None))
        self.option_allow_custom_music.setText(QCoreApplication.translate("MainWindow", u"Allow Custom Music", None))
        self.option_no_enemy_music.setText(QCoreApplication.translate("MainWindow", u"Remove Enemy Music", None))
        self.box.setTitle("")
        self.box_presets.setTitle(QCoreApplication.translate("MainWindow", u"Presets", None))
        self.label_presets.setText(QCoreApplication.translate("MainWindow", u"Presets overwrite ALL game settings", None))
        self.load_preset.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.save_preset.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.delete_preset.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_setup), QCoreApplication.translate("MainWindow", u"Setup", None))
#if QT_CONFIG(tooltip)
        self.tab_randomization_settings.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.box_shuffles.setTitle(QCoreApplication.translate("MainWindow", u"Shuffles", None))
        self.label_for_option_max_batreaux_reward.setText(QCoreApplication.translate("MainWindow", u"Maximum Batreaux Reward", None))
        self.label_for_option_shopsanity.setText(QCoreApplication.translate("MainWindow", u"Beedle's Shop", None))
        self.label_for_option_rupeesanity.setText(QCoreApplication.translate("MainWindow", u"Rupeesanity", None))
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
        self.box_open.setTitle(QCoreApplication.translate("MainWindow", u"Open Settings", None))
        self.label_for_option_open_thunderhead.setText(QCoreApplication.translate("MainWindow", u"Open Thunderhead", None))
        self.option_open_et.setText(QCoreApplication.translate("MainWindow", u"Open Earth Temple", None))
        self.label_for_option_open_lmf.setText(QCoreApplication.translate("MainWindow", u"Open Lanayru Mining Facility", None))
        self.label_for_option_starting_tablet_count.setText(QCoreApplication.translate("MainWindow", u"Starting Tablets", None))
        self.label_for_option_open_lake_floria.setText(QCoreApplication.translate("MainWindow", u"Open Lake Floria", None))
        self.box_entrance_rando.setTitle(QCoreApplication.translate("MainWindow", u"Entrance Randomization", None))
        self.label_for_option_randomize_entrances.setText(QCoreApplication.translate("MainWindow", u"Randomize Dungeon Entrances", None))
        self.option_randomize_entrances.setCurrentText("")
        self.option_randomize_trials.setText(QCoreApplication.translate("MainWindow", u"Randomize Silent Realm Gates", None))
        self.box_dungeons.setTitle(QCoreApplication.translate("MainWindow", u"Dungeons", None))
        self.label_for_option_map_mode.setText(QCoreApplication.translate("MainWindow", u"Map Mode", None))
        self.label_for_option_small_key_mode.setText(QCoreApplication.translate("MainWindow", u"Small Keys", None))
        self.label_for_option_boss_key_mode.setText(QCoreApplication.translate("MainWindow", u"Boss Keys", None))
        self.option_empty_unrequired_dungeons.setText(QCoreApplication.translate("MainWindow", u"Empty Unrequired Dungeons", None))
        self.label_for_sword_dungeon_reward.setText(QCoreApplication.translate("MainWindow", u"Sword Dungeon Reward", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_randomization_settings), QCoreApplication.translate("MainWindow", u"Randomization Settings", None))
        self.box_convenience_tweaks.setTitle(QCoreApplication.translate("MainWindow", u"Convenience Tweaks", None))
        self.option_fill_dowsing_on_white_sword.setText(QCoreApplication.translate("MainWindow", u"Fill Dowsing on White Sword", None))
        self.box_vanilla_tweaks.setTitle(QCoreApplication.translate("MainWindow", u"Vanilla Tweaks", None))
        self.label_for_option_bit_patches.setText(QCoreApplication.translate("MainWindow", u"BiT Patches", None))
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
        self.edit_tricks.setText(QCoreApplication.translate("MainWindow", u"Tricks", None))
        self.label_include_locations.setText(QCoreApplication.translate("MainWindow", u"Included Locations", None))
        self.included_free_search.setText("")
        self.included_free_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.include_category_filters.setPlaceholderText("")
        self.include_location.setText(QCoreApplication.translate("MainWindow", u"Include\n"
"<--", None))
        self.exclude_location.setText(QCoreApplication.translate("MainWindow", u"Exclude\n"
"-->", None))
        self.label_exclude_locations.setText(QCoreApplication.translate("MainWindow", u"Excluded Locations", None))
        self.excluded_free_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logic_settings), QCoreApplication.translate("MainWindow", u"Logic Settings", None))
        self.box_stone_hints.setTitle(QCoreApplication.translate("MainWindow", u"Gossip Stone Hints", None))
        self.label_for_option_hint_distribution.setText(QCoreApplication.translate("MainWindow", u"Hint Distribution", None))
        self.option_cube_sots.setText(QCoreApplication.translate("MainWindow", u"Separate Cube SotS Hints", None))
        self.option_precise_item.setText(QCoreApplication.translate("MainWindow", u"Precise Item Hints", None))
        self.box_other_hints.setTitle(QCoreApplication.translate("MainWindow", u"Other Hints", None))
        self.label_for_option_song_hints.setText(QCoreApplication.translate("MainWindow", u"Song Hints", None))
        self.option_impa_sot_hint.setText(QCoreApplication.translate("MainWindow", u"Impa Stone of Trials Hint", None))
        self.label_for_option_chest_dowsing.setText(QCoreApplication.translate("MainWindow", u"Chest Dowsing", None))
        self.option_chest_dowsing.setCurrentText("")
        self.option_dungeon_dowsing.setText(QCoreApplication.translate("MainWindow", u"Allow Dowsing in Dungeons", None))
        self.box_4.setTitle("")
        self.box_5.setTitle("")
        self.box_6.setTitle("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_hints), QCoreApplication.translate("MainWindow", u"Hints", None))
        self.label_randomized_items.setText(QCoreApplication.translate("MainWindow", u"Randomized Items", None))
        self.randomized_items_free_search.setText("")
        self.randomized_items_free_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.randomize_item.setText(QCoreApplication.translate("MainWindow", u"Remove\n"
"<--", None))
        self.start_with_item.setText(QCoreApplication.translate("MainWindow", u"Add\n"
"-->", None))
        self.label_starting_items.setText(QCoreApplication.translate("MainWindow", u"Starting Items", None))
        self.starting_items_free_search.setText("")
        self.starting_items_free_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.label_for_option_starting_sword.setText(QCoreApplication.translate("MainWindow", u"Starting Sword", None))
        self.option_random_starting_item.setText(QCoreApplication.translate("MainWindow", u"Start with Random Progress Item", None))
        self.label_for_option_starting_heart_containers.setText(QCoreApplication.translate("MainWindow", u"Heart Containers", None))
        self.label_for_option_starting_heart_pieces.setText(QCoreApplication.translate("MainWindow", u"Heart Pieces", None))
        self.label_current_starting_health.setText(QCoreApplication.translate("MainWindow", u"Current Starting Health:", None))
        self.current_starting_health_counter.setText(QCoreApplication.translate("MainWindow", u"6 hearts", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_starting_items), QCoreApplication.translate("MainWindow", u"Starting Items", None))
        self.box_theme.setTitle(QCoreApplication.translate("MainWindow", u"Theming", None))
        self.theme_mode_label.setText(QCoreApplication.translate("MainWindow", u"Theme Mode", None))
        self.option_theme_mode.setCurrentText("")
        self.theme_presets_label.setText(QCoreApplication.translate("MainWindow", u"Theme Presets", None))
        self.option_theme_presets.setCurrentText("")
        self.option_use_custom_theme.setText(QCoreApplication.translate("MainWindow", u"Use Custom Theme", None))
        self.custom_theme_button.setText(QCoreApplication.translate("MainWindow", u"Customize Theme", None))
        self.option_use_sharp_corners.setText(QCoreApplication.translate("MainWindow", u"Sharp Corners", None))
        self.box_font.setTitle(QCoreApplication.translate("MainWindow", u"Fonts", None))
        self.label_for_option_font_family.setText(QCoreApplication.translate("MainWindow", u"Font Family", None))
        self.option_font_family.setCurrentText(QCoreApplication.translate("MainWindow", u"Arial", None))
        self.option_font_family.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Select Font Family", None))
        self.label_for_option_font_size.setText(QCoreApplication.translate("MainWindow", u"Font Size", None))
        self.reset_font_button.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.box_1.setTitle("")
        self.box_2.setTitle("")
        self.box_3.setTitle("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_accessibility), QCoreApplication.translate("MainWindow", u"Accessibility", None))
        self.option_description.setText("")
        self.label_permalink.setText(QCoreApplication.translate("MainWindow", u"Settings String", None))
        self.copy_permalink_button.setText(QCoreApplication.translate("MainWindow", u"Copy Settings String", None))
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

