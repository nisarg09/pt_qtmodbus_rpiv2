# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intropg.ui'
#
# Created: Mon Jul 11 04:28:47 2016
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Intro(object):
    def setupUi(self, Intro):
        Intro.setObjectName(_fromUtf8("Intro"))
        Intro.resize(800, 480)
        Intro.setAutoFillBackground(False)
        Intro.setStyleSheet(_fromUtf8("background-color: rgb(0, 139, 255);"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Intro)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setMargin(3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.widget = QtGui.QWidget(Intro)
        self.widget.setStyleSheet(_fromUtf8("background-color: rgb(0, 139, 255);"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Century Schoolbook"))
        font.setPointSize(50)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2.addWidget(self.widget)

        self.retranslateUi(Intro)
        QtCore.QMetaObject.connectSlotsByName(Intro)

    def retranslateUi(self, Intro):
        Intro.setWindowTitle(QtGui.QApplication.translate("Intro", "Introductory", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Intro", "Welcome", None, QtGui.QApplication.UnicodeUTF8))

