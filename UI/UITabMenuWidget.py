# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabMenuWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QWidget)

class Ui_TabMenuWidget(object):
    def setupUi(self, TabMenuWidget):
        if not TabMenuWidget.objectName():
            TabMenuWidget.setObjectName(u"TabMenuWidget")
        TabMenuWidget.resize(784, 141)
        self.horizontalLayout_2 = QHBoxLayout(TabMenuWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(TabMenuWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setEnabled(True)
        self.horizontalLayout = QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setCheckable(False)

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.tab)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.tab)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_6 = QPushButton(self.tab_2)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton_6)

        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton_8)

        self.pushButton_5 = QPushButton(self.tab_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton_5)

        self.pushButton_7 = QPushButton(self.tab_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton_7)

        self.pushButton_9 = QPushButton(self.tab_2)
        self.pushButton_9.setObjectName(u"pushButton_9")
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.pushButton_9)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_10 = QPushButton(self.tab_3)
        self.pushButton_10.setObjectName(u"pushButton_10")
        sizePolicy.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.pushButton_10)

        self.pushButton_11 = QPushButton(self.tab_3)
        self.pushButton_11.setObjectName(u"pushButton_11")
        sizePolicy.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.pushButton_11)

        self.pushButton_12 = QPushButton(self.tab_3)
        self.pushButton_12.setObjectName(u"pushButton_12")
        sizePolicy.setHeightForWidth(self.pushButton_12.sizePolicy().hasHeightForWidth())
        self.pushButton_12.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.pushButton_12)

        self.pushButton_13 = QPushButton(self.tab_3)
        self.pushButton_13.setObjectName(u"pushButton_13")
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.pushButton_13)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.horizontalLayout_5 = QHBoxLayout(self.tab_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_14 = QPushButton(self.tab_4)
        self.pushButton_14.setObjectName(u"pushButton_14")
        sizePolicy.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButton_14)

        self.pushButton_15 = QPushButton(self.tab_4)
        self.pushButton_15.setObjectName(u"pushButton_15")
        sizePolicy.setHeightForWidth(self.pushButton_15.sizePolicy().hasHeightForWidth())
        self.pushButton_15.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButton_15)

        self.pushButton_16 = QPushButton(self.tab_4)
        self.pushButton_16.setObjectName(u"pushButton_16")
        sizePolicy.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButton_16)

        self.pushButton_17 = QPushButton(self.tab_4)
        self.pushButton_17.setObjectName(u"pushButton_17")
        sizePolicy.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButton_17)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_18 = QPushButton(self.tab_5)
        self.pushButton_18.setObjectName(u"pushButton_18")
        sizePolicy.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.pushButton_18)

        self.pushButton_19 = QPushButton(self.tab_5)
        self.pushButton_19.setObjectName(u"pushButton_19")
        sizePolicy.setHeightForWidth(self.pushButton_19.sizePolicy().hasHeightForWidth())
        self.pushButton_19.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.pushButton_19)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.tabWidget.addTab(self.tab_5, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(TabMenuWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TabMenuWidget)
    # setupUi

    def retranslateUi(self, TabMenuWidget):
        TabMenuWidget.setWindowTitle(QCoreApplication.translate("TabMenuWidget", u"TabMenuWidget", None))
        self.pushButton.setText(QCoreApplication.translate("TabMenuWidget", u"Passive\n"
"Integrated\n"
"Structure", None))
        self.pushButton_2.setText(QCoreApplication.translate("TabMenuWidget", u"Semiconductor\n"
"Device", None))
        self.pushButton_3.setText(QCoreApplication.translate("TabMenuWidget", u"Packaging\n"
"Structure", None))
        self.pushButton_4.setText(QCoreApplication.translate("TabMenuWidget", u"Transistor\n"
"Structure", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("TabMenuWidget", u"Simulation", None))
        self.pushButton_6.setText(QCoreApplication.translate("TabMenuWidget", u"Electrostatic\n"
"Discharge", None))
        self.pushButton_8.setText(QCoreApplication.translate("TabMenuWidget", u"Thermal\n"
"Noise", None))
        self.pushButton_5.setText(QCoreApplication.translate("TabMenuWidget", u"Electromagnetic\n"
"Interference", None))
        self.pushButton_7.setText(QCoreApplication.translate("TabMenuWidget", u"Crosstalk", None))
        self.pushButton_9.setText(QCoreApplication.translate("TabMenuWidget", u"Shot\n"
"Noise", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("TabMenuWidget", u"Source", None))
        self.pushButton_10.setText(QCoreApplication.translate("TabMenuWidget", u"Bayesian\n"
"Optimization", None))
        self.pushButton_11.setText(QCoreApplication.translate("TabMenuWidget", u"Neural\n"
"Networks", None))
        self.pushButton_12.setText(QCoreApplication.translate("TabMenuWidget", u"Reinforcement\n"
"Learning", None))
        self.pushButton_13.setText(QCoreApplication.translate("TabMenuWidget", u"LSTM", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("TabMenuWidget", u"Optimize", None))
        self.pushButton_14.setText(QCoreApplication.translate("TabMenuWidget", u"Data\n"
"Extraction", None))
        self.pushButton_15.setText(QCoreApplication.translate("TabMenuWidget", u"Visualization", None))
        self.pushButton_16.setText(QCoreApplication.translate("TabMenuWidget", u"Parameter\n"
"Fitting", None))
        self.pushButton_17.setText(QCoreApplication.translate("TabMenuWidget", u"Analysis", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("TabMenuWidget", u"Reprocess", None))
        self.pushButton_18.setText(QCoreApplication.translate("TabMenuWidget", u"Model\n"
"Validation", None))
        self.pushButton_19.setText(QCoreApplication.translate("TabMenuWidget", u"Reliability\n"
"Verification", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("TabMenuWidget", u"Confidence", None))
    # retranslateUi

