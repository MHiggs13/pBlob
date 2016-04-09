import _thread

from PyQt5.QtGui import QTransform, QPixmap
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import sys

class TestGUIClass(QFrame):

    def __init__(self):
        super(TestGUIClass, self).__init__()
        print("I should print")
        self.show()


class Test(QMainWindow):

    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        print("I worked")

        self.label = QLabel(self)
        self.label.setText("HELLO WORLD!")

        self.gunPxMap = QPixmap('C:\\Users\\michaelh\\Desktop\\CSC Project\\Server\\src\\resources\\cannon.png')
        self.gunPxMap = self.gunPxMap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label.setPixmap(self.gunPxMap)

        self.label.setGeometry(200, 200, 150, 150)

        self.setGeometry(100, 100, 700, 700)
        self.show()
        # _thread.start_new_thread(self.rotate, ())
        for x in range (0, 50):
            self.rotate()

    def rotate(self):
        t = QTransform()

        # for x in range (0, 150):
        t.rotate(-1)
        self.label.setPixmap(self.label.pixmap().transformed(t))


        print("FINISHED")





class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self,args)

        tets = Test()

        sys.exit(self.exec_())


if __name__ == '__main__':
    print("Test")
    #test = TestGUIClass()
    app = App(sys.argv)