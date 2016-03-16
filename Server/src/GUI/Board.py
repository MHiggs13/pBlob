import re
from decimal import Decimal

from PyQt5.QtCore import QRect
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

        self.blob = Blob(self)
        self.show()

    def updatePos(self, strPos):

        # regex to distinguish if c is a correct character
        pattern = "-|\d|\."

        x = ''
        y = ''
        isXFinished = False


        # Receive the position from the client and change to x and y
        for c in strPos:
            if c == ';':
                break
            else:
                match = re.match(pattern, c)
            if not isXFinished:
                if c == ',':
                    isXFinished = True
                elif match:
                    x += c
            elif match:
                y += c

        # Divide x and y by 100 and remove decimal points to get speed factor
        x = Decimal(x)
        y = Decimal(y)
        x = int(x/100)
        y = int(y/100)

        # Speed becomes equal to x * defSpeed, y * defSpeed
        self.blob.xSpeed = self.blob.defSpeed * x
        self.blob.ySpeed = self.blob.defSpeed * y


    """ Update game graphics with respect to the current game state """
    def updateGame(self, strPos):
        self.updatePos(strPos)

        self.drawGame()

    """ Draw all graphics in the game """
    def drawGame(self):
        print("BEFORE X AND Y")
        # Draw blob in it's new position
        x = self.blob.x() + self.blob.xSpeed
        y = self.blob.y() + self.blob.ySpeed

        print("AFTER X AND Y")

        self.blob.setGeometry(x, y, self.blob.BLOB_WIDTH, self.blob.BLOB_HEIGHT)

