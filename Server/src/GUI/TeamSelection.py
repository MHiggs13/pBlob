# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'teamSelection.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from src.Server.Server import Server


class TeamSelectionUI(QWidget):

    updateTeamsSig = pyqtSignal(dict)

    def __init__(self, parent = None):
        super(TeamSelectionUI, self).__init__(parent)

    def setupUi(self, adrs):
        self.resize(1000, 621)

        self.teamFrames = []
        self.teamLbls = []
        self.memberTbxs = []
        self.teams = {}

        self.numTeams = int(len(adrs)/2)

        for i in range(0, self.numTeams):
            self.createNewTeamFrame(i)
            self.teams[i] = {}

        for frame in self.teamFrames:
            frame.raise_()
        for lbl in self.teamLbls:
            lbl.raise_()
        for tbx in self.memberTbxs:
            tbx.raise_()

        self.show()
        # QtCore.QMetaObject.connectSlotsByName(self)

    def createNewTeamFrame(self, iteration):
        self.initialXY = [15, 230]
        self.initialWH = [231, 141]

        x = self.initialXY[0] + (self.initialWH[0] + self.initialXY[0]) * iteration
        y = self.initialXY[1]

        teamFrame = QtWidgets.QFrame(self)
        teamFrame.setGeometry(QtCore.QRect(x, y, 231, 141))  # x = 15+ width + 15
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(86, 240, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(86, 240, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(86, 240, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(86, 240, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        teamFrame.setPalette(palette)
        teamFrame.setAutoFillBackground(True)
        teamFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        teamFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        teamFrame.setObjectName("teamFrame")

        teamLbl = QtWidgets.QLabel(teamFrame)
        teamLbl.setGeometry(QtCore.QRect(10, 10, 221, 31))
        strTeamNum = "Team " + str(iteration)
        teamLbl.setText(strTeamNum)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(86, 240, 148))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        teamLbl.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        teamLbl.setFont(font)
        teamLbl.setObjectName("teamLbl")
        member1Tbx = QtWidgets.QTextEdit(teamFrame)
        member1Tbx.setGeometry(QtCore.QRect(10, 50, 171, 31))
        member1Tbx.setObjectName("member1Tbx")
        member2Tbx = QtWidgets.QTextEdit(teamFrame)
        member2Tbx.setGeometry(QtCore.QRect(10, 90, 171, 31))
        member2Tbx.setObjectName("member2Tbx")

        self.teamFrames.append(teamFrame)
        self.teamLbls.append(teamLbl)
        self.memberTbxs.append(member1Tbx)
        self.memberTbxs.append(member2Tbx)

    def setupTeam(self, addressDict, msg):
        """ Take the message passed from the address, addressDict (dictionary), and check if that involves joining a
        team and what position on that team.

        :param addressDict: the dictionary containing the address of the client that sent the message
        :param msg: a String that signifies team and position, e.g. "team1,driver"
        :return:
        """
        address = None
        for key in addressDict:
            address = addressDict[key]

        # take the first character of msg and convert it to an int, this represents the team number
        team = int(msg[0])
        """if second part of msg is driver add that address to dictionary via team number(0,1,2,3) and then "driver" or
        "gunner"
        """
        if msg[1:] == "driver" and address:
            print(address)
            self.checkAndRemovePrevRole(address)
            self.teams[team]["driver"] = address
            self.memberTbxs[team*2].setText(str(address))
        elif msg[1:] == "gunner" and address:
            self.checkAndRemovePrevRole(address)
            self.teams[team]["gunner"] = address
            self.memberTbxs[team*2+1].setText(str(address))

        # Update servers dictionary of teams
        self.updateTeamsSig.emit(self.teams)


    def checkAndRemovePrevRole(self, address):
        """ Check if the client choosing a role already has chosen a role, if they have remove the previous role from,
        both the interface and the team dictionary

        :param address:
        :return:
        """
        for count in range(0, self.numTeams):
            print("in for count")
            if "driver" in self.teams[count].keys():
                print("inside if 1")
                if self.teams[count]["driver"] == address:
                    print("inside inner if 1")
                    self.teams[count].pop("driver")
                    print("after pop")
                    self.memberTbxs[count * 2].setText("")
            if "gunner" in self.teams[count].keys():
                print("inside if 2")
                if self.teams[count]["gunner"] == address:
                    print("inside inner if 2")
                    self.teams[count].pop("gunner")
                    print("after pop")
                    self.memberTbxs[count * 2 + 1].setText("")




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = TeamSelectionUI()

    adrs = []
    for x in range(0,2):
        adrs.append(x)

    ui.setupUi(adrs)
    sys.exit(app.exec_())

