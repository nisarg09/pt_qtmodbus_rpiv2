# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_page.ui'
#
# Created: Mon Jul 11 04:29:11 2016
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainPage(object):
    def setupUi(self, MainPage):
        MainPage.setObjectName(_fromUtf8("MainPage"))
        MainPage.resize(800, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainPage.sizePolicy().hasHeightForWidth())
        MainPage.setSizePolicy(sizePolicy)
        MainPage.setStyleSheet(_fromUtf8("background-color: rgb(0, 139, 255);"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainPage)
        self.verticalLayout_2.setMargin(3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_3 = QtGui.QWidget(MainPage)
        self.verticalLayout_3.setStyleSheet(_fromUtf8("background-color: rgb(0, 139, 255);"))
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayout_3)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setMargin(3)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalFrame_6 = QtGui.QFrame(self.verticalLayout_3)
        self.horizontalFrame_6.setStyleSheet(_fromUtf8("background-color: rgb(255,255,255);"))
        self.horizontalFrame_6.setFrameShape(QtGui.QFrame.WinPanel)
        self.horizontalFrame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalFrame_6.setObjectName(_fromUtf8("horizontalFrame_6"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.horizontalFrame_6)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.btn_monitorParams = QtGui.QPushButton(self.horizontalFrame_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_monitorParams.sizePolicy().hasHeightForWidth())
        self.btn_monitorParams.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.btn_monitorParams.setFont(font)
        self.btn_monitorParams.setMouseTracking(False)
        self.btn_monitorParams.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_monitorParams.setStyleSheet(_fromUtf8("color: rgb(0,89,131);"))
        self.btn_monitorParams.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/Picture8.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_monitorParams.setIcon(icon)
        self.btn_monitorParams.setIconSize(QtCore.QSize(205, 108))
        self.btn_monitorParams.setAutoRepeat(True)
        self.btn_monitorParams.setAutoDefault(True)
        self.btn_monitorParams.setDefault(False)
        self.btn_monitorParams.setFlat(True)
        self.btn_monitorParams.setObjectName(_fromUtf8("btn_monitorParams"))
        self.horizontalLayout_7.addWidget(self.btn_monitorParams)
        self.horizontalLayout_3.addWidget(self.horizontalFrame_6)
        self.horizontalFrame_5 = QtGui.QFrame(self.verticalLayout_3)
        self.horizontalFrame_5.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.horizontalFrame_5.setFrameShape(QtGui.QFrame.WinPanel)
        self.horizontalFrame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalFrame_5.setObjectName(_fromUtf8("horizontalFrame_5"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.horizontalFrame_5)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.btn_interlockParams = QtGui.QPushButton(self.horizontalFrame_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_interlockParams.sizePolicy().hasHeightForWidth())
        self.btn_interlockParams.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.btn_interlockParams.setFont(font)
        self.btn_interlockParams.setMouseTracking(False)
        self.btn_interlockParams.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_interlockParams.setStyleSheet(_fromUtf8("color: rgb(0, 89, 131);"))
        self.btn_interlockParams.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/Picture2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_interlockParams.setIcon(icon1)
        self.btn_interlockParams.setIconSize(QtCore.QSize(222, 108))
        self.btn_interlockParams.setAutoDefault(True)
        self.btn_interlockParams.setDefault(False)
        self.btn_interlockParams.setFlat(True)
        self.btn_interlockParams.setObjectName(_fromUtf8("btn_interlockParams"))
        self.horizontalLayout_6.addWidget(self.btn_interlockParams)
        self.horizontalLayout_3.addWidget(self.horizontalFrame_5)
        self.horizontalFrame_4 = QtGui.QFrame(self.verticalLayout_3)
        self.horizontalFrame_4.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.horizontalFrame_4.setFrameShape(QtGui.QFrame.WinPanel)
        self.horizontalFrame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalFrame_4.setObjectName(_fromUtf8("horizontalFrame_4"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.horizontalFrame_4)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.btn_setControls = QtGui.QPushButton(self.horizontalFrame_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_setControls.sizePolicy().hasHeightForWidth())
        self.btn_setControls.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.btn_setControls.setFont(font)
        self.btn_setControls.setMouseTracking(False)
        self.btn_setControls.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_setControls.setStyleSheet(_fromUtf8("color: rgb(0, 89, 131);"))
        self.btn_setControls.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/Picture3.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_setControls.setIcon(icon2)
        self.btn_setControls.setIconSize(QtCore.QSize(205, 108))
        self.btn_setControls.setAutoDefault(True)
        self.btn_setControls.setDefault(False)
        self.btn_setControls.setFlat(True)
        self.btn_setControls.setObjectName(_fromUtf8("btn_setControls"))
        self.horizontalLayout_5.addWidget(self.btn_setControls)
        self.horizontalLayout_3.addWidget(self.horizontalFrame_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 109, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalFrame_9 = QtGui.QFrame(self.verticalLayout_3)
        self.horizontalFrame_9.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.horizontalFrame_9.setFrameShape(QtGui.QFrame.WinPanel)
        self.horizontalFrame_9.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalFrame_9.setObjectName(_fromUtf8("horizontalFrame_9"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.horizontalFrame_9)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.btn_commParams = QtGui.QPushButton(self.horizontalFrame_9)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_commParams.sizePolicy().hasHeightForWidth())
        self.btn_commParams.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.btn_commParams.setFont(font)
        self.btn_commParams.setMouseTracking(False)
        self.btn_commParams.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_commParams.setStyleSheet(_fromUtf8("color: rgb(0, 89, 131);"))
        self.btn_commParams.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/Picture7.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_commParams.setIcon(icon3)
        self.btn_commParams.setIconSize(QtCore.QSize(221, 108))
        self.btn_commParams.setAutoDefault(True)
        self.btn_commParams.setDefault(False)
        self.btn_commParams.setFlat(True)
        self.btn_commParams.setObjectName(_fromUtf8("btn_commParams"))
        self.horizontalLayout_10.addWidget(self.btn_commParams)
        self.horizontalLayout.addWidget(self.horizontalFrame_9)
        self.horizontalFrame_8 = QtGui.QFrame(self.verticalLayout_3)
        self.horizontalFrame_8.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.horizontalFrame_8.setFrameShape(QtGui.QFrame.WinPanel)
        self.horizontalFrame_8.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalFrame_8.setObjectName(_fromUtf8("horizontalFrame_8"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.horizontalFrame_8)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.btn_calibration = QtGui.QPushButton(self.horizontalFrame_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_calibration.sizePolicy().hasHeightForWidth())
        self.btn_calibration.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.btn_calibration.setFont(font)
        self.btn_calibration.setMouseTracking(False)
        self.btn_calibration.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_calibration.setStyleSheet(_fromUtf8("color: rgb(0, 89, 131);"))
        self.btn_calibration.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/Picture5.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_calibration.setIcon(icon4)
        self.btn_calibration.setIconSize(QtCore.QSize(205, 108))
        self.btn_calibration.setAutoDefault(True)
        self.btn_calibration.setDefault(False)
        self.btn_calibration.setFlat(True)
        self.btn_calibration.setObjectName(_fromUtf8("btn_calibration"))
        self.horizontalLayout_9.addWidget(self.btn_calibration)
        self.horizontalLayout.addWidget(self.horizontalFrame_8)
        self.horizontalFrame_7 = QtGui.QFrame(self.verticalLayout_3)
        self.horizontalFrame_7.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.horizontalFrame_7.setFrameShape(QtGui.QFrame.WinPanel)
        self.horizontalFrame_7.setFrameShadow(QtGui.QFrame.Raised)
        self.horizontalFrame_7.setObjectName(_fromUtf8("horizontalFrame_7"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.horizontalFrame_7)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.btn_exit = QtGui.QPushButton(self.horizontalFrame_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.btn_exit.setFont(font)
        self.btn_exit.setMouseTracking(False)
        self.btn_exit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btn_exit.setStyleSheet(_fromUtf8("color: rgb(0, 89, 131);"))
        self.btn_exit.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/Picture6.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_exit.setIcon(icon5)
        self.btn_exit.setIconSize(QtCore.QSize(205, 108))
        self.btn_exit.setAutoDefault(True)
        self.btn_exit.setDefault(False)
        self.btn_exit.setFlat(True)
        self.btn_exit.setObjectName(_fromUtf8("btn_exit"))
        self.horizontalLayout_8.addWidget(self.btn_exit)
        self.horizontalLayout.addWidget(self.horizontalFrame_7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.verticalLayout_3)

        self.retranslateUi(MainPage)
        QtCore.QMetaObject.connectSlotsByName(MainPage)

    def retranslateUi(self, MainPage):
        MainPage.setWindowTitle(QtGui.QApplication.translate("MainPage", "Menu Page", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_setControls.setShortcut(QtGui.QApplication.translate("MainPage", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_exit.setShortcut(QtGui.QApplication.translate("MainPage", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
