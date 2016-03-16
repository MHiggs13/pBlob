from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

class Blob(QLabel):
    """ Allow for a blob to be drawn on GameBoard """

    # Height and width for a blob, changeable by GameBoard
    BLOB_HEIGHT = 200
    BLOB_WIDTH = 200

    def __init__(self, parent):
        super(Blob, self).__init__(parent)

        #Label and Pixmap to contain iamge of blob
        self.resize(self.BLOB_WIDTH, self.BLOB_HEIGHT)

        self.blobPxMap = QPixmap('C:\\Users\\michaelh\\Desktop\\CSC Project\\Server\\src\\resources\\blueBlob.png')
        self.blobPxMap = self.blobPxMap.scaled(self.BLOB_WIDTH, self.BLOB_HEIGHT, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.setPixmap(self.blobPxMap)

        self.defSpeed = 3
        self.xSpeed = 0
        self.ySpeed = 0

        self.show()