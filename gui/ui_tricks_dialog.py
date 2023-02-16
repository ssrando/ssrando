# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tricks_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QListView, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_TricksDialog(object):
    def setupUi(self, TricksDialog):
        if not TricksDialog.objectName():
            TricksDialog.setObjectName(u"TricksDialog")
        TricksDialog.resize(1005, 481)
        self.verticalLayout = QVBoxLayout(TricksDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.vlay_tricks = QVBoxLayout()
        self.vlay_tricks.setObjectName(u"vlay_tricks")
        self.hlay_tricks_body = QHBoxLayout()
        self.hlay_tricks_body.setObjectName(u"hlay_tricks_body")
        self.vlay_disabled_tricks = QVBoxLayout()
        self.vlay_disabled_tricks.setObjectName(u"vlay_disabled_tricks")
        self.label_for_disabled_tricks = QLabel(TricksDialog)
        self.label_for_disabled_tricks.setObjectName(u"label_for_disabled_tricks")

        self.vlay_disabled_tricks.addWidget(self.label_for_disabled_tricks)

        self.disabled_tricks = QListView(TricksDialog)
        self.disabled_tricks.setObjectName(u"disabled_tricks")

        self.vlay_disabled_tricks.addWidget(self.disabled_tricks)


        self.hlay_tricks_body.addLayout(self.vlay_disabled_tricks)

        self.vlay_tricks_controls = QVBoxLayout()
        self.vlay_tricks_controls.setObjectName(u"vlay_tricks_controls")
        self.vspace_tricks_controls_upper = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_tricks_controls.addItem(self.vspace_tricks_controls_upper)

        self.disable_trick = QPushButton(TricksDialog)
        self.disable_trick.setObjectName(u"disable_trick")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disable_trick.sizePolicy().hasHeightForWidth())
        self.disable_trick.setSizePolicy(sizePolicy)

        self.vlay_tricks_controls.addWidget(self.disable_trick)

        self.vspace_tricks_controls_middle = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_tricks_controls.addItem(self.vspace_tricks_controls_middle)

        self.enable_trick = QPushButton(TricksDialog)
        self.enable_trick.setObjectName(u"enable_trick")
        sizePolicy.setHeightForWidth(self.enable_trick.sizePolicy().hasHeightForWidth())
        self.enable_trick.setSizePolicy(sizePolicy)

        self.vlay_tricks_controls.addWidget(self.enable_trick)

        self.vspace_tricks_controls_lower = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vlay_tricks_controls.addItem(self.vspace_tricks_controls_lower)


        self.hlay_tricks_body.addLayout(self.vlay_tricks_controls)

        self.vlay_enabled_tricks = QVBoxLayout()
        self.vlay_enabled_tricks.setObjectName(u"vlay_enabled_tricks")
        self.label_for_enabled_tricks = QLabel(TricksDialog)
        self.label_for_enabled_tricks.setObjectName(u"label_for_enabled_tricks")

        self.vlay_enabled_tricks.addWidget(self.label_for_enabled_tricks)

        self.enabled_tricks = QListView(TricksDialog)
        self.enabled_tricks.setObjectName(u"enabled_tricks")

        self.vlay_enabled_tricks.addWidget(self.enabled_tricks)


        self.hlay_tricks_body.addLayout(self.vlay_enabled_tricks)


        self.vlay_tricks.addLayout(self.hlay_tricks_body)


        self.verticalLayout.addLayout(self.vlay_tricks)

        self.bbox_tricks = QDialogButtonBox(TricksDialog)
        self.bbox_tricks.setObjectName(u"bbox_tricks")
        self.bbox_tricks.setOrientation(Qt.Horizontal)
        self.bbox_tricks.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.bbox_tricks)


        self.retranslateUi(TricksDialog)
        self.bbox_tricks.accepted.connect(TricksDialog.accept)
        self.bbox_tricks.rejected.connect(TricksDialog.reject)

        QMetaObject.connectSlotsByName(TricksDialog)
    # setupUi

    def retranslateUi(self, TricksDialog):
        TricksDialog.setWindowTitle(QCoreApplication.translate("TricksDialog", u"Enable Tricks", None))
        self.label_for_disabled_tricks.setText(QCoreApplication.translate("TricksDialog", u"Disabled Tricks", None))
#if QT_CONFIG(tooltip)
        self.disabled_tricks.setToolTip(QCoreApplication.translate("TricksDialog", u"test", None))
#endif // QT_CONFIG(tooltip)
        self.disable_trick.setText(QCoreApplication.translate("TricksDialog", u"Disable\n"
"<--", None))
        self.enable_trick.setText(QCoreApplication.translate("TricksDialog", u"Enable\n"
"-->", None))
        self.label_for_enabled_tricks.setText(QCoreApplication.translate("TricksDialog", u"Enabled Tricks", None))
    # retranslateUi

