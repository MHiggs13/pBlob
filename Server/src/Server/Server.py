import socket

from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread
import select

from src.Server.State import State


class Server(QObject, Thread):

    # todo define frame per second so animation speed is constant

    # Signal to update the State
    updateActiveWidget = pyqtSignal(dict)

    # Signals to send data to MAIN_SCREEN
    updateConnectedUsersSig = pyqtSignal(['QString'])
    appendConnectedHistorySig = pyqtSignal(['QString'])
    updateConnectedHistorySig = pyqtSignal(['QString'])
    updateGameInfoSig = pyqtSignal(['QString'])

    # Signals to send data to GAME_SCREEN
    updateGameSig = pyqtSignal([dict, 'QString'])

    state = State()

    def __init__(self):
        super(Server, self).__init__()

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (socket.gethostname(), 8313)
        self.server.bind(addr)

        # lists of sockets which listen for input and output events
        self.ins = [self.server]
        self.outs = []
        # dictionary that maps data to the socket it is to be sent to
        self.data = {}
        # dictionary that maps the address to the correct client socket
        self.adrs = {}

        # start listening for incoming communications, max of 10 queued clients
        self.server.listen(10)

    def run(self):
        """ The server loop, loops repeatedly checking ins for sockets that have received an input event, or outs for
        sockets that have to commit an output event

        :return:
        """
        history = 'Hosted on: ' + socket.gethostbyname('michael')
        self.appendConnectedHistorySig.emit(history)

        try:
            while 1:
                i, o, e = select.select(self.ins, self.outs, [])     # [] means no exceptions, and no timeout (default)
                for s in i:
                    # for all sockets in inputs
                    # some input event is trying to take place on s,
                    # either new client, client receives data or disconnection
                    if s is self.server:
                        # if current socket is server accept a new client connection
                        sock, address = self.server.accept()
                        history = 'Connection from {!s}.'.format(address)
                        self.appendConnectedHistorySig.emit(history)

                        self.ins.append(sock)
                        # self.adrs[sock] = {"address":address, "playerIndex":-1}
                        self.adrs[sock] = {-1:address}
                    else:
                        # curr socket not server so data has been received or a disconnection
                        data = s.recv(4096)
                        if not data:
                            # valid data was not received, client disconnected
                            history = 'Disconnection from {!s}.'.format(self.adrs[s])
                            self.appendConnectedHistorySig.emit(history)

                            # delete socket from appropriate lists
                            del self.adrs[s]
                            self.ins.remove(s)
                            if s in self.outs:
                                self.outs.remove(s)
                            s.close()
                        else:
                            # data is a message fromt he client
                            msg = data.decode()
                            self.manageMessage(s, msg)
                for s in o:
                    # for all sockets in outputs
                    # some output event is trying to take place on s,
                    # either a
                    toSend = self.data.get(s)
                    if toSend:
                        sent = s.send(toSend.encode())
                        toSend = toSend[sent:]
                    if toSend:
                        self.data[s] = toSend
                    else:
                        try:
                            del self.data[s]
                        except KeyError:
                            pass
                        self.outs.remove(s)  # remove s from outputs since data is sent to s

        finally:
            self.server.close()

    def manageMessage(self, sock, msg):
        """ Look at the message received and decide what to do with it.

        :param sock: the socket that sent the message
        :param msg: the string sent by the socket
        :return:
        """
        if (msg in State.states):
            # if message is about the state, update state and tell all other clients to change state
            if (self.state.currState != msg):
                self.state.currState = msg
                print("SOCK: ", sock)
                self.assignPlayerIndex(sock)
                # todo make sure there is a mult of 2 clients, driver+gunner for each blob AND make sure order is correct i.e. driver1, gunner1, driver2, gunner2
                self.updateActiveWidget.emit(self.adrs)

            # add all other sockets to outs, with currState as the param
            for s in self.ins:
                if (s != sock) or (s != self.server):
                    self.outs.append(s)  # during next server loop data[s] will be sent to s
                    self.data[s] = self.state.currState
        elif (self.state.currState == State.MAIN_SCREEN):
            # carry out updates for the MAIN_SCREEN STATE
            self.updateMainScreen(sock, msg)
        elif (self.state.currState == State.GAME_SCREEN):
            # carry out updates for the GAME_SCREEN STATE
            self.updateGameScreen(sock, msg)

    def assignPlayerIndex(self, sock):#
        """ assigns the correct index to each player. Even numbers are drivers and odd numbers are gunners.
        0,1 are a pair - 2,3 are a pair etc

        :param sock: the client that started the game - so they are playerIndex 0
        """
        # todo update so that a check is performed by the server to see who is in each team
        self.adrs[sock][0] = self.adrs[sock].pop(-1)  # replace default -1 key with key 0
        for s in self.adrs.keys():
            if (s != sock):
                self.adrs[s][1] = self.adrs[s].pop(-1)  # todo appropriately assign all values not just 0 and 1
            print(self.adrs[s])

    def updateMainScreen(self, sock, msg):
        """ Client either selects an option on the main screen or writes a message to be displayed

        :param sock:
        :param msg:
        :return:
        """
        # todo allow options to be selected by a client and managed here
        output = '{!s}: {!s}\n'.format(self.adrs[sock], msg)
        self.updateGameInfoSig.emit(output)


    def updateGameScreen(self, sock, msg):
        """ Client has sent controls as a string. Controls may be movement,

        :param sock:
        :param msg:
        :return:
        """
        self.updateGameSig.emit(self.adrs[sock], msg)  # send first value in dict (address)