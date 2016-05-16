# from PyQt5.QtGui import QDialog, QPushButton, QApplication
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
from threading import Thread

from PyQt5.QtGui import QPixmap

from src.GUI.Board2 import Board
from src.Server.Items import Wall


class ServerClass(QObject, Thread):

    mySignal = pyqtSignal()

    def __init__(self, parent=None):
        super(ServerClass, self).__init__(parent)

    def run(self):
        self.myEmitterMethod()

    def myEmitterMethod(self):
        time.sleep(3)
        self.mySignal.emit()
        time.sleep(2)
        print('done')

    def testSignal(self):
        receiversCount = self.receivers(QtCore.SIGNAL("mySignal"))
        print('Receivers = ', receiversCount)
        if receiversCount > 0:
            self.sigChanged.disconnect()


class UiClass(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(UiClass, self).__init__(parent)

        self.connectedUsersTxbrwsr = QtWidgets.QTextBrowser(self)

    def startUi(self):
        self.c.show()

    def connectedMethod(self):
        print('The connected method received the custom emit')

class App(QtWidgets.QApplication):
    def __init__(self, args):
        QtWidgets.QApplication.__init__(self,args)
        self.window = Board()
        self.window.show()

        sys.exit(self.exec_())


if __name__ == '__main__':
    app = App(sys.argv)
    app.exec()
    sys.exit(app.exec_())