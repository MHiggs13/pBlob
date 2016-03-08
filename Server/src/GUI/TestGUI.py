from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QApplication, QMainWindow
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


class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self,args)

        tets = Test()

        sys.exit(self.exec_())


if __name__ == '__main__':
    print("Test")
    #test = TestGUIClass()
    app = App(sys.argv)