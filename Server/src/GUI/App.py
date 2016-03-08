import sys

from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QApplication, QGridLayout

from src.GUI.MainForm import MainForm
from src.GUI.Board import GameBoard
from src.Server.ServerMain import ServerMain
from src.Server.State import State


class Window(QMainWindow):

    BOARD_HEIGHT = 621
    BOARD_WIDTH = 1000

    def __init__(self):
        super(Window, self).__init__()

        self.widgMain = MainForm()
        self.server = ServerMain()

        # Set up connections between UI and Server, allowing Server to send messages to UI
        self.server.updateConnectedUsersSig.connect(self.widgMain.updateConnectedUsers)
        self.server.appendConnectedHistorySig.connect(self.widgMain.appendConnectedHistory)
        self.server.updateConnectedUsersSig.connect(self.widgMain.updateConnectedHistory)
        self.server.updateGameInfoSig.connect(self.widgMain.updateGameInfo)

        self.server.updateStateSig.connect(self.updateState)

        self.widgBoard = GameBoard()

        self.stack = QStackedWidget(self)
        self.stack.resize(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.stack.addWidget(self.widgMain)
        self.stack.addWidget(self.widgBoard)

        self.resize(self.BOARD_WIDTH, self.BOARD_HEIGHT)

        layout = QGridLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.setWindowTitle("Blobbageddon")

        self.stack.setCurrentIndex(0)

        self.server.setupServer()
        self.server.start()
        self.show()

    def updateState(self, string):
        print("In state changed")
        if (self.server.state.currState == State.GAME_SCREEN):
            self.stack.setCurrentIndex(1)
            self.widgBoard.start()
        elif (self.server.state.currState == State.MAIN_SCREEN):
            self.stack.setCurrentIndex(0)


class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self,args)

        self.window = Window()

        sys.exit(self.exec_())