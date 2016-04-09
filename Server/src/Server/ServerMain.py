import socket
import sys
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread

from src.Server.State import State


class ServerMain(QObject, Thread):

    # Signal to update the State
    updateStateSig = pyqtSignal(list)

    # Signals to send data to MAIN_SCREEN
    updateConnectedUsersSig = pyqtSignal(['QString'])
    appendConnectedHistorySig = pyqtSignal(['QString'])
    updateConnectedHistorySig = pyqtSignal(['QString'])
    updateGameInfoSig = pyqtSignal(['QString'])

    # Signals to send data to GAME_SCREEN
    updatePosSig = pyqtSignal(['QString', 'QString'])

    state = State()



    def __init__(self, parent=None):
        super(ServerMain, self).__init__(parent)

        s = socket.socket()
        self.listOfClientSocks = [s]

        # set up host to accept clients with any host name, and arbitrary non
        # privileged port
        HOST = socket.gethostname()
        PORT = 8313
        ADDR = (HOST,PORT)

        self.BUFFER_SIZE = 1024

        # Create socket with ...
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # attempt to bind socket to host and port
        try:
            self.sock.bind(ADDR)
        except socket.error as e:
            msg = e
            print (msg)
            sys.exit()

        # start listening for a connection, parameter is max number of queued connections
        self.sock.listen(10)

    def setupServer(self):
        history = 'Hosted on: '+ socket.gethostbyname('michael')
        self.appendConnectedHistorySig.emit(history)

    def run(self):
        self.startServer()

    def startServer(self):
        # method to start server and set up connection for client to connect to
        # infinite loop to wait on client connections

        self.appendConnectedHistorySig.emit("Waiting on a connection...")


        listOfClients = []
        self.listOfClientNames = []
        counter = 0
        while True:
            # clientSock = new socket object to allow data to be exchanged
            # address is address of cliSock on client's end of communication

            clientSock, address = self.sock.accept()
            # self.app.window.updateConnectedHistory('Server: Connection established to client {!s}'.format(address))
            history = 'Connection from {!s}.'.format(address)
            self.appendConnectedHistorySig.emit(history)

            listOfClients.append(Thread(target=self.inMainState, args=(clientSock, address)))
            self.listOfClientSocks.append(clientSock)
            self.listOfClientNames.append(address[0])
            listOfClients[counter].start()
            counter += 1

        self.sock.close()

    def waitForClient(self, clientSock, address):
        # Loop to wait on data to be received, exits loop if data isn't received
        while True:
            msg = clientSock.recv(self.BUFFER_SIZE)

            # if what was received was not data i.e. connection closed ('') or similar break loop
            if not msg:
                print("TERMINATED - !MSG")
                history = 'Disconnection from {!s}.'.format(address)
                self.appendConnectedHistorySig.emit(history)

                # since msg is returned have to set to empty string
                msg = ""
                break

            stringData = msg.decode('utf-8')
            stringData = stringData[2:] # todo need to remove 2 chars from start of converted string, dont know why

            # Check if game is required to change state, send message to client saying to change state
            if (stringData != self.state.currState):
                self.state.currState = stringData
                self.updateStateSig.emit(self.listOfClientNames)

                if (self.state.currState == State.MAIN_SCREEN):
                    clientSock.send(State.MAIN_SCREEN.encode())
                    self.inMainState(clientSock, address)
                elif (self.state.currState == State.GAME_SCREEN):
                    clientSock.send(State.GAME_SCREEN.encode())
                    self.inGameState(clientSock, address)

            # todo might not be good with method calls above, needs some thought
            return msg
        # close client sock after receiving data
        clientSock.close()

    def stripMessage(self, msg):
         # b'\x00\x07
        return msg[10:]

    def inMainState(self, clientSock, address):
        while True:
            msg = self.waitForClient(clientSock, address)
            output = '{!s}: {!s}\n'.format(address, msg)
            self.updateGameInfoSig.emit(output)

    def inGameState(self, clientSock, address):
        print("SENT STATE TO CLIENT")
        clientSock.send(State.GAME_SCREEN.encode())
        while True:
            msg = self.waitForClient(clientSock, address).decode('utf-8')
            self.updatePosSig.emit(address[0], msg)


    def manageClientConnections(self):
        # method to manage client connections
        # multi threading begins here
        pass