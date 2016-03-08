# from PyQt5.QtGui import QDialog, QPushButton, QApplication
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
from multiprocessing.context import Process
from threading import Thread

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
        self.window = UiClass()
        self.window.show()
        self.server = ServerClass()
        self.server.mySignal.connect(self.window.connectedMethod)

        self.server.start()

        print('this code should print while thread works in background')

        # p = Process(target=self.server.myEmitterMethod)
        # p = Process(target=self.server.testSignal)
        # p.start()
        # self.server.myEmitterMethod()
        # self.server.run()

        sys.exit(self.exec_())


if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    app = App(sys.argv)
    app.exec()
    # form = ServerClass()
    # # form.c.show()
    # sys.exit(app.exec_())