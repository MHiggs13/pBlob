# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1000, 621)
        self.titleGraphic = QtWidgets.QGraphicsView(MainForm)
        self.titleGraphic.setGeometry(QtCore.QRect(15, 20, 970, 192))
        self.titleGraphic.setObjectName("titleGraphic")
        self.connectedUsersLbl = QtWidgets.QLabel(MainForm)
        self.connectedUsersLbl.setGeometry(QtCore.QRect(15, 230, 151, 20))
        self.connectedUsersLbl.setObjectName("connectedUsersLbl")
        self.connectionHistoryLbl = QtWidgets.QLabel(MainForm)
        self.connectionHistoryLbl.setGeometry(QtCore.QRect(365, 230, 231, 16))
        self.connectionHistoryLbl.setObjectName("connectionHistoryLbl")
        self.connectedUsersTable = QtWidgets.QTableView(MainForm)
        self.connectedUsersTable.setGeometry(QtCore.QRect(15, 250, 270, 351))
        self.connectedUsersTable.setObjectName("connectedUsersTable")
        self.connectionHistoryTxbrwsr = QtWidgets.QTextBrowser(MainForm)
        self.connectionHistoryTxbrwsr.setGeometry(QtCore.QRect(365, 250, 270, 351))
        self.connectionHistoryTxbrwsr.setObjectName("connectionHistoryTxbrwsr")
        self.gameInfoLbl = QtWidgets.QLabel(MainForm)
        self.gameInfoLbl.setGeometry(QtCore.QRect(715, 230, 231, 16))
        self.gameInfoLbl.setObjectName("gameInfoLbl")
        self.gameInfoTxbrwsr = QtWidgets.QTextBrowser(MainForm)
        self.gameInfoTxbrwsr.setGeometry(QtCore.QRect(715, 250, 270, 351))
        self.gameInfoTxbrwsr.setObjectName("gameInfoTxbrwsr")
        self.titleGraphic.raise_()
        self.connectedUsersLbl.raise_()
        self.connectionHistoryLbl.raise_()
        self.connectionHistoryTxbrwsr.raise_()
        self.connectedUsersTable.raise_()
        self.gameInfoLbl.raise_()
        self.gameInfoTxbrwsr.raise_()

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Dialog"))
        self.connectedUsersLbl.setText(_translate("MainForm", "Connected Users"))
        self.connectionHistoryLbl.setText(_translate("MainForm", "Connection History"))
        self.gameInfoLbl.setText(_translate("MainForm", "Game Information"))

