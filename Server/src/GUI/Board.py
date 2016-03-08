import sys

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.uic.properties import QtCore

from src.GUI.Blob import Blob

""" Class that creates the game UI and manages player actions """
class GameBoard(QWidget):

    # Default variables
    BOARD_HEIGHT = 621
    BOARD_WIDTH = 1000

    """ Initialize the GameBoard class """
    def __init__(self):
       # super(GameBoard, self).__init__()
        super(GameBoard, self).__init__()
        print("Initiated board")

        # self.setupUI()

    def start(self):
        self.setupUI()

    """ Create initial state for the initial board UI """
    def setupUI(self):

        self.resize(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.setWindowTitle('Blobbageddon!')

        # todo no display elements show on this widget. Something fundamental is wrong,probably basic

        self.lbl = QLabel(self)
        self.lbl.setText("HEY")
        self.lbl.setGeometry(QtCore.QRect(15, 230, 151, 20))
        self.lbl.setObjectName("connectedUsersLnbbl")

        self.blob = Blob(self)

        for i in range (0,10):
            self.blob.setGeometry(self.blob.x() + 10, self.blob.y() + 10, self.blob.width(), self.blob.height())

        print("BLOB DONE")
        self.show()

    """ Update game graphics with respect to the current game state """
    def updateGame(self):
        pass

