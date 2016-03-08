# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from src.Server.ServerMain import ServerMain


class MainForm(QWidget):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.setupUi(self)


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
        self.connectedUsersTxbrwsr = QtWidgets.QTextBrowser(MainForm)
        self.connectedUsersTxbrwsr.setGeometry(QtCore.QRect(15, 250, 270, 351))
        self.connectedUsersTxbrwsr.setObjectName("connectedUsersTxbrwsr")
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
        self.connectedUsersTxbrwsr.raise_()
        self.gameInfoLbl.raise_()
        self.gameInfoTxbrwsr.raise_()

        self.retranslateUi()

        self.loadDefaultInformation()

        self.show()
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainForm", "Blobageddon"))
        self.connectedUsersLbl.setText(_translate("MainForm", "Connected Users"))
        self.connectionHistoryLbl.setText(_translate("MainForm", "Connection History"))
        self.gameInfoLbl.setText(_translate("MainForm", "Game Information"))

    def loadDefaultInformation(self):
        self.connectedUsersTxbrwsr.insertPlainText("")
        self.connectionHistoryTxbrwsr.insertPlainText("")
        self.gameInfoTxbrwsr.insertPlainText("1.) Wait here until all members have connected.\n2.) Once all members have"
                                             " connected continue to the team selection page.")

    def updateConnectedUsers(self, strUsers):
        # Method to update the text browser when a new user has connected or an old one disconnects
        self.connectedUsersTxbrwsr.insertPlainText(strUsers)

    def updateConnectedHistory(self, strHistory):
        # Method to update the text browser when a new connection event has occurred
        self.connectionHistoryTxbrwsr.insertPlainText(strHistory)

    def appendConnectedHistory(self, strHistory):
        # Appends the string passed in to the text in text browser
        output = "" + strHistory
        self.connectionHistoryTxbrwsr.append(output)

    def updateGameInfo(self, strGameInfo):
        # Method to update the text browser with information relevant tot he current state of the game
        self.connectedUsersTxbrwsr.insertPlainText(strGameInfo)