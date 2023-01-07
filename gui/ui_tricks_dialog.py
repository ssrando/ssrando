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
    QHBoxLayout, QListView, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_TricksDialog(object):
    def setupUi(self, TricksDialog):
        if not TricksDialog.objectName():
            TricksDialog.setObjectName(u"TricksDialog")
        TricksDialog.resize(1005, 309)
        self.bbox_tricks = QDialogButtonBox(TricksDialog)
        self.bbox_tricks.setObjectName(u"bbox_tricks")
        self.bbox_tricks.setGeometry(QRect(660, 270, 341, 32))
        self.bbox_tricks.setOrientation(Qt.Horizontal)
        self.bbox_tricks.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layoutWidget = QWidget(TricksDialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(8, 10, 991, 251))
        self.vlay_tricks = QVBoxLayout(self.layoutWidget)
        self.vlay_tricks.setObjectName(u"vlay_tricks")
        self.vlay_tricks.setContentsMargins(0, 0, 0, 0)
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


        self.retranslateUi(TricksDialog)
        self.bbox_tricks.accepted.connect(TricksDialog.accept)
        self.bbox_tricks.rejected.connect(TricksDialog.reject)

        QMetaObject.connectSlotsByName(TricksDialog)
    # setupUi

    def retranslateUi(self, TricksDialog):
        TricksDialog.setWindowTitle(QCoreApplication.translate("TricksDialog", u"Enable Tricks", None))
#if QT_CONFIG(tooltip)
        self.disabled_tricks.setToolTip(QCoreApplication.translate("TricksDialog", u"test", None))
#endif // QT_CONFIG(tooltip)
        self.disable_trick.setText(QCoreApplication.translate("TricksDialog", u"Disable\n"
"<--", None))
        self.enable_trick.setText(QCoreApplication.translate("TricksDialog", u"Enable\n"
"-->", None))
    # retranslateUi

