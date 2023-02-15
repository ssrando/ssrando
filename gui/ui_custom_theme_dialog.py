# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'custom_theme_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QDoubleSpinBox, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPlainTextEdit, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QTabWidget, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_CustomThemeDialog(object):
    def setupUi(self, CustomThemeDialog):
        if not CustomThemeDialog.objectName():
            CustomThemeDialog.setObjectName(u"CustomThemeDialog")
        CustomThemeDialog.resize(612, 635)
        self.custom_theme_tabWidget = QTabWidget(CustomThemeDialog)
        self.custom_theme_tabWidget.setObjectName(u"custom_theme_tabWidget")
        self.custom_theme_tabWidget.setGeometry(QRect(6, 9, 601, 531))
        self.custom_colors_tab = QWidget()
        self.custom_colors_tab.setObjectName(u"custom_colors_tab")
        self.verticalLayoutWidget = QWidget(self.custom_colors_tab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 571, 481))
        self.vlay_widget = QVBoxLayout(self.verticalLayoutWidget)
        self.vlay_widget.setObjectName(u"vlay_widget")
        self.vlay_widget.setContentsMargins(0, 0, 0, 0)
        self.hlay_widget_catergory = QHBoxLayout()
        self.hlay_widget_catergory.setObjectName(u"hlay_widget_catergory")
        self.widget_category_label = QLabel(self.verticalLayoutWidget)
        self.widget_category_label.setObjectName(u"widget_category_label")

        self.hlay_widget_catergory.addWidget(self.widget_category_label)

        self.widget_category_choice = QComboBox(self.verticalLayoutWidget)
        self.widget_category_choice.setObjectName(u"widget_category_choice")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_category_choice.sizePolicy().hasHeightForWidth())
        self.widget_category_choice.setSizePolicy(sizePolicy)

        self.hlay_widget_catergory.addWidget(self.widget_category_choice)

        self.hspace = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlay_widget_catergory.addItem(self.hspace)


        self.vlay_widget.addLayout(self.hlay_widget_catergory)

        self.hlay_widgets = QHBoxLayout()
        self.hlay_widgets.setObjectName(u"hlay_widgets")
        self.vlay_widget_name = QVBoxLayout()
        self.vlay_widget_name.setObjectName(u"vlay_widget_name")
        self.vlay_widget_name.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.widget_name_label = QLabel(self.verticalLayoutWidget)
        self.widget_name_label.setObjectName(u"widget_name_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_name_label.sizePolicy().hasHeightForWidth())
        self.widget_name_label.setSizePolicy(sizePolicy1)
        self.widget_name_label.setMinimumSize(QSize(0, 0))
        self.widget_name_label.setTextFormat(Qt.MarkdownText)

        self.vlay_widget_name.addWidget(self.widget_name_label)

        self.vspace_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_widget_name.addItem(self.vspace_5)


        self.hlay_widgets.addLayout(self.vlay_widget_name)

        self.vlay_color_light = QVBoxLayout()
        self.vlay_color_light.setObjectName(u"vlay_color_light")
        self.color_light_label = QLabel(self.verticalLayoutWidget)
        self.color_light_label.setObjectName(u"color_light_label")
        self.color_light_label.setTextFormat(Qt.MarkdownText)

        self.vlay_color_light.addWidget(self.color_light_label)

        self.vspace_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_color_light.addItem(self.vspace_3)


        self.hlay_widgets.addLayout(self.vlay_color_light)

        self.vlay_color_dark = QVBoxLayout()
        self.vlay_color_dark.setObjectName(u"vlay_color_dark")
        self.color_dark_label = QLabel(self.verticalLayoutWidget)
        self.color_dark_label.setObjectName(u"color_dark_label")
        self.color_dark_label.setFrameShadow(QFrame.Plain)
        self.color_dark_label.setTextFormat(Qt.MarkdownText)

        self.vlay_color_dark.addWidget(self.color_dark_label)

        self.vspace_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_color_dark.addItem(self.vspace_2)


        self.hlay_widgets.addLayout(self.vlay_color_dark)


        self.vlay_widget.addLayout(self.hlay_widgets)

        self.custom_theme_tabWidget.addTab(self.custom_colors_tab, "")
        self.demo_widgets_tab = QWidget()
        self.demo_widgets_tab.setObjectName(u"demo_widgets_tab")
        self.horizontalLayoutWidget = QWidget(self.demo_widgets_tab)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 581, 571))
        self.hlay_demo = QHBoxLayout(self.horizontalLayoutWidget)
        self.hlay_demo.setObjectName(u"hlay_demo")
        self.hlay_demo.setContentsMargins(0, 0, 0, 0)
        self.vlay_demo_left = QVBoxLayout()
        self.vlay_demo_left.setObjectName(u"vlay_demo_left")
        self.demo_group_box = QGroupBox(self.horizontalLayoutWidget)
        self.demo_group_box.setObjectName(u"demo_group_box")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.demo_group_box.sizePolicy().hasHeightForWidth())
        self.demo_group_box.setSizePolicy(sizePolicy2)
        self.verticalLayoutWidget_8 = QWidget(self.demo_group_box)
        self.verticalLayoutWidget_8.setObjectName(u"verticalLayoutWidget_8")
        self.verticalLayoutWidget_8.setGeometry(QRect(10, 20, 251, 541))
        self.vlay_demo_group_box = QVBoxLayout(self.verticalLayoutWidget_8)
        self.vlay_demo_group_box.setObjectName(u"vlay_demo_group_box")
        self.vlay_demo_group_box.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.verticalLayoutWidget_8)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)

        self.vlay_demo_group_box.addWidget(self.label_10)

        self.line_12 = QFrame(self.verticalLayoutWidget_8)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShape(QFrame.HLine)
        self.line_12.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_12)

        self.demo_checkBox = QCheckBox(self.verticalLayoutWidget_8)
        self.demo_checkBox.setObjectName(u"demo_checkBox")

        self.vlay_demo_group_box.addWidget(self.demo_checkBox)

        self.line_11 = QFrame(self.verticalLayoutWidget_8)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.HLine)
        self.line_11.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_11)

        self.demo_radioButton = QRadioButton(self.verticalLayoutWidget_8)
        self.demo_radioButton.setObjectName(u"demo_radioButton")

        self.vlay_demo_group_box.addWidget(self.demo_radioButton)

        self.line_10 = QFrame(self.verticalLayoutWidget_8)
        self.line_10.setObjectName(u"line_10")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line_10.sizePolicy().hasHeightForWidth())
        self.line_10.setSizePolicy(sizePolicy3)
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_10)

        self.demo_spinBox = QSpinBox(self.verticalLayoutWidget_8)
        self.demo_spinBox.setObjectName(u"demo_spinBox")

        self.vlay_demo_group_box.addWidget(self.demo_spinBox)

        self.line_9 = QFrame(self.verticalLayoutWidget_8)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.HLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_9)

        self.demo_doubleSpinBox = QDoubleSpinBox(self.verticalLayoutWidget_8)
        self.demo_doubleSpinBox.setObjectName(u"demo_doubleSpinBox")

        self.vlay_demo_group_box.addWidget(self.demo_doubleSpinBox)

        self.line_8 = QFrame(self.verticalLayoutWidget_8)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_8)

        self.demo_pushButton = QPushButton(self.verticalLayoutWidget_8)
        self.demo_pushButton.setObjectName(u"demo_pushButton")

        self.vlay_demo_group_box.addWidget(self.demo_pushButton)

        self.line_7 = QFrame(self.verticalLayoutWidget_8)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_7)

        self.demo_comboBox = QComboBox(self.verticalLayoutWidget_8)
        self.demo_comboBox.setObjectName(u"demo_comboBox")

        self.vlay_demo_group_box.addWidget(self.demo_comboBox)

        self.line_6 = QFrame(self.verticalLayoutWidget_8)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_6)

        self.demo_lineEdit = QLineEdit(self.verticalLayoutWidget_8)
        self.demo_lineEdit.setObjectName(u"demo_lineEdit")

        self.vlay_demo_group_box.addWidget(self.demo_lineEdit)

        self.line_5 = QFrame(self.verticalLayoutWidget_8)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_5)

        self.demo_horizontalSlider = QSlider(self.verticalLayoutWidget_8)
        self.demo_horizontalSlider.setObjectName(u"demo_horizontalSlider")
        self.demo_horizontalSlider.setOrientation(Qt.Horizontal)

        self.vlay_demo_group_box.addWidget(self.demo_horizontalSlider)

        self.line_4 = QFrame(self.verticalLayoutWidget_8)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_4)

        self.demo_progressBar = QProgressBar(self.verticalLayoutWidget_8)
        self.demo_progressBar.setObjectName(u"demo_progressBar")
        self.demo_progressBar.setValue(24)

        self.vlay_demo_group_box.addWidget(self.demo_progressBar)

        self.line_3 = QFrame(self.verticalLayoutWidget_8)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_group_box.addWidget(self.line_3)

        self.demo_dialogButtonBox = QDialogButtonBox(self.verticalLayoutWidget_8)
        self.demo_dialogButtonBox.setObjectName(u"demo_dialogButtonBox")
        self.demo_dialogButtonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.demo_dialogButtonBox.setCenterButtons(True)

        self.vlay_demo_group_box.addWidget(self.demo_dialogButtonBox)

        self.vspace = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_demo_group_box.addItem(self.vspace)


        self.vlay_demo_left.addWidget(self.demo_group_box)


        self.hlay_demo.addLayout(self.vlay_demo_left)

        self.line = QFrame(self.horizontalLayoutWidget)
        self.line.setObjectName(u"line")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy4)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.hlay_demo.addWidget(self.line)

        self.verticalSlider = QSlider(self.horizontalLayoutWidget)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setOrientation(Qt.Vertical)

        self.hlay_demo.addWidget(self.verticalSlider)

        self.line_2 = QFrame(self.horizontalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        sizePolicy4.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy4)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.hlay_demo.addWidget(self.line_2)

        self.vlay_demo_right = QVBoxLayout()
        self.vlay_demo_right.setObjectName(u"vlay_demo_right")
        self.demo_textEdit = QTextEdit(self.horizontalLayoutWidget)
        self.demo_textEdit.setObjectName(u"demo_textEdit")

        self.vlay_demo_right.addWidget(self.demo_textEdit)

        self.line_13 = QFrame(self.horizontalLayoutWidget)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShape(QFrame.HLine)
        self.line_13.setFrameShadow(QFrame.Sunken)

        self.vlay_demo_right.addWidget(self.line_13)

        self.demo_plainTextEdit = QPlainTextEdit(self.horizontalLayoutWidget)
        self.demo_plainTextEdit.setObjectName(u"demo_plainTextEdit")

        self.vlay_demo_right.addWidget(self.demo_plainTextEdit)


        self.hlay_demo.addLayout(self.vlay_demo_right)

        self.custom_theme_tabWidget.addTab(self.demo_widgets_tab, "")
        self.widget_description = QLabel(CustomThemeDialog)
        self.widget_description.setObjectName(u"widget_description")
        self.widget_description.setEnabled(True)
        self.widget_description.setGeometry(QRect(10, 550, 591, 41))
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widget_description.sizePolicy().hasHeightForWidth())
        self.widget_description.setSizePolicy(sizePolicy5)
        self.widget_description.setWordWrap(True)
        self.horizontalLayoutWidget_2 = QWidget(CustomThemeDialog)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 590, 591, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.restore_defaults_button = QPushButton(self.horizontalLayoutWidget_2)
        self.restore_defaults_button.setObjectName(u"restore_defaults_button")

        self.horizontalLayout.addWidget(self.restore_defaults_button)

        self.bbox_theme = QDialogButtonBox(self.horizontalLayoutWidget_2)
        self.bbox_theme.setObjectName(u"bbox_theme")
        self.bbox_theme.setOrientation(Qt.Horizontal)
        self.bbox_theme.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Save)
        self.bbox_theme.setCenterButtons(False)

        self.horizontalLayout.addWidget(self.bbox_theme)


        self.retranslateUi(CustomThemeDialog)
        self.bbox_theme.accepted.connect(CustomThemeDialog.accept)
        self.bbox_theme.rejected.connect(CustomThemeDialog.reject)

        self.custom_theme_tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(CustomThemeDialog)
    # setupUi

    def retranslateUi(self, CustomThemeDialog):
        CustomThemeDialog.setWindowTitle(QCoreApplication.translate("CustomThemeDialog", u"Customize Randomizer Theme", None))
        self.widget_category_label.setText(QCoreApplication.translate("CustomThemeDialog", u"Widget Category", None))
        self.widget_name_label.setText(QCoreApplication.translate("CustomThemeDialog", u"_**Widget Name**_", None))
        self.color_light_label.setText(QCoreApplication.translate("CustomThemeDialog", u"_**Color (Light Theme)**_", None))
        self.color_dark_label.setText(QCoreApplication.translate("CustomThemeDialog", u"_**Color (Dark Theme)**_", None))
        self.custom_theme_tabWidget.setTabText(self.custom_theme_tabWidget.indexOf(self.custom_colors_tab), QCoreApplication.translate("CustomThemeDialog", u"Custom Colors", None))
        self.demo_group_box.setTitle(QCoreApplication.translate("CustomThemeDialog", u"GroupBox", None))
        self.label_10.setText(QCoreApplication.translate("CustomThemeDialog", u"QLabel", None))
        self.demo_checkBox.setText(QCoreApplication.translate("CustomThemeDialog", u"CheckBox", None))
        self.demo_radioButton.setText(QCoreApplication.translate("CustomThemeDialog", u"RadioButton", None))
        self.demo_pushButton.setText(QCoreApplication.translate("CustomThemeDialog", u"PushButton", None))
        self.demo_comboBox.setCurrentText("")
        self.demo_comboBox.setPlaceholderText(QCoreApplication.translate("CustomThemeDialog", u"ComboBox", None))
        self.demo_lineEdit.setText(QCoreApplication.translate("CustomThemeDialog", u"LineEdit", None))
        self.demo_textEdit.setHtml(QCoreApplication.translate("CustomThemeDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TextEdit</p></body></html>", None))
        self.demo_plainTextEdit.setPlainText(QCoreApplication.translate("CustomThemeDialog", u"PlainTextEdit", None))
        self.custom_theme_tabWidget.setTabText(self.custom_theme_tabWidget.indexOf(self.demo_widgets_tab), QCoreApplication.translate("CustomThemeDialog", u"Demo Widgets", None))
        self.widget_description.setText("")
        self.restore_defaults_button.setText(QCoreApplication.translate("CustomThemeDialog", u"Restore Defaults", None))
    # retranslateUi

