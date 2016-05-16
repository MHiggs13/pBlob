import sys

from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QApplication, QGridLayout, QDialog

from src.GUI.Board2 import Board
from src.GUI.MainForm import MainForm
from src.GUI.TeamSelection import TeamSelectionUI
from src.Server.Server import Server

from src.Server.State import State


class Window(QMainWindow):

    BOARD_HEIGHT = 621
    BOARD_WIDTH = 1000

    def __init__(self):
        super(Window, self).__init__()

        self.widgMain = MainForm()
        self.widgTeam = TeamSelectionUI()
        self.widgBoard = Board()
        print("AFTER BOARD CREATED")
        self.server = Server()

        # Set up signal to allow state change
        self.server.updateActiveWidget.connect(self.updateActiveWidget)

        # Set up signal to allow data to be sent to MAIN_SCREEN
        self.server.updateConnectedUsersSig.connect(self.widgMain.updateConnectedUsers)
        self.server.appendConnectedHistorySig.connect(self.widgMain.appendConnectedHistory)
        self.server.updateConnectedUsersSig.connect(self.widgMain.updateConnectedHistory)
        self.server.updateGameInfoSig.connect(self.widgMain.updateGameInfo)

        """ Set up signal to allow data to be received by the TEAM_SCREEN (self.widgTeam), data sent is used to sort
        clients into teams of two
        """
        self.server.setupTeamSig.connect(self.widgTeam.setupTeam)


        # Set up signal to allow data to be sent to GAME_SCREEN
        self.server.updateGameSig.connect(self.widgBoard.updateGame)

        # Set up signal to allow updated teams to be sent to server
        self.widgTeam.updateTeamsSig.connect(self.server.updateTeams)

        self.stack = QStackedWidget(self)
        self.stack.resize(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.stack.addWidget(self.widgMain)
        self.stack.addWidget(self.widgTeam)
        self.stack.addWidget(self.widgBoard)

        self.resize(self.BOARD_WIDTH, self.BOARD_HEIGHT)

        layout = QGridLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.setWindowTitle("Blobbageddon")

        self.stack.setCurrentIndex(0)

        self.server.start()
        self.show()

    def updateActiveWidget(self, adrs):
        if (self.server.state.currState == State.GAME_SCREEN):
            self.stack.setCurrentIndex(2)
            print(len(adrs))
            self.widgBoard.start(adrs)
        elif self.server.state.currState == State.TEAM_SCREEN:
            self.widgTeam.setupUi(adrs)
            self.stack.setCurrentIndex(1)
        elif (self.server.state.currState == State.MAIN_SCREEN):
            self.stack.setCurrentIndex(0)


class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self,args)

        self.window = Window()

        sys.exit(self.exec_())