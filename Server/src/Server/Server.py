import socket
import time

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

    #Signals to send data involving team creation to TEAM_SCREEN
    setupTeamSig = pyqtSignal([dict, 'QString'])

    # Signals to send data to GAME_SCREEN
    updateGameSig = pyqtSignal([dict, 'QString', int])

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

        self.teams = {}

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
                i, o, e = select.select(self.ins, self.outs, self.ins)     # [] means no exceptions, and no timeout (default)
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
                        self.adrs[sock] = {-1:address}

                        # update list of connected users
                        strConnectedUsers = ''
                        count = 0
                        for sock in self.adrs:
                            if sock != self.server:
                                count += 1
                                strConnectedUsers += " {0}.) {1}".format(count, self.adrs[sock])
                        self.updateGameInfoSig.emit(strConnectedUsers)
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

                            # update list of connected users
                            strConnectedUsers = ''
                            count = 0
                            for sock in self.adrs:
                                if sock != self.server:
                                    count += 1
                                    strConnectedUsers += " {0}.) {1}".format(count, self.adrs[sock])
                            self.updateGameInfoSig.emit(strConnectedUsers)
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

                for s in e:
                    if s != self.server:  # error/disconnection on a client socket
                        # valid data was not received, client disconnected
                        history = 'Disconnection from {!s}.'.format(self.adrs[s])
                        self.appendConnectedHistorySig.emit(history)

                        # delete socket from appropriate lists
                        del self.adrs[s]
                        self.ins.remove(s)
                        if s in self.outs:
                            self.outs.remove(s)
                        s.close()

                        # update list of connected users
                        strConnectedUsers = ''
                        count = 0
                        for sock in self.adrs:
                            if sock != self.server:
                                count += 1
                                strConnectedUsers += " {0}.) {1}".format(count, self.adrs[sock])
                        self.updateGameInfoSig.emit(strConnectedUsers)

        finally:
            self.server.close()

    def manageMessage(self, sock, msg):
        """ Look at the message received and decide what to do with it.

        :param sock: the socket that sent the message
        :param msg: the string sent by the socket
        :return:
        """
        print(msg)
        parts = msg.split(":")
        if (parts[0] == "SC"):
            self.handleStateChange(sock, parts[1])
        elif parts[0] == "AW":
            self.handleAwake(sock, parts[1])
        elif parts[0] == "RL":
            # information to do with the role and team of a client
            self.updateTeamScreen(sock, parts[1])
        elif self.state.currState == State.MAIN_SCREEN:
            # carry out updates for the MAIN_SCREEN STATE
            self.updateMainScreen(sock, parts[1])
        elif  (parts[0] == "DR" or parts[0] == "GU") and self.state.currState == State.GAME_SCREEN:
            print("in game update")
            print("parts[1]: " + parts[1])
            # carry out updates for the GAME_SCREEN STATE todo switch order more efficient?
            self.updateGameScreen(sock, parts[1])

    def handleStateChange(self, sock, part2):
        # if first section of message equals SC (StateChange)
        # print("SC: part2: " + part2)
        if (self.state.currState != part2 and (len(self.ins)-1) % 2 == 0):
            self.state.currState = part2

            # todo make sure there is a mult of 2 clients, driver+gunner for each blob AND make sure order is correct i.e. driver1, gunner1, driver2, gunner2
            allRolesAssigned = True
            # special case for game screen, addresses need to be ordered
            if self.state.currState == State.GAME_SCREEN:
                # check that all clients have chosen a role
                print(self.teams)
                for t in self.teams.keys():
                    # if all roles have not been assigned do not advance to game screen
                    if not "driver" in self.teams[t] or not "gunner" in self.teams[t]:
                        allRolesAssigned = False
                        self.state.currState = State.TEAM_SCREEN
                if allRolesAssigned:
                    self.assignPlayerIndex(sock)
                    self.sendGameScreenRoles()
            else:
                self.sendStateChange()
                self.gameStartTime = time.clock()
            self.updateActiveWidget.emit(self.adrs)


    def sendGameScreenRoles(self):
        """ Special case for sending a state change, game is entering game state so client needs to know whether or not
        to create a movement or gunner view.

        :return:
        """
        for s in self.ins:
            if s != self.server:
                for k in self.adrs[s].keys():
                    self.outs.append(s)  # during next server loop data[s] will be sent to this socket s
                    if k % 2 == 0:  # driver = 0,2,4,6
                        self.data[s] = "SC:" + self.state.currState + ":" + "driver" + ":"
                        print(self.data[s])
                    else:  # gunner = 1,3,5,7
                        self.data[s] = "SC:" + self.state.currState + ":" + "gunner" + ":"




    def sendStateChange(self, sock=None):
        """ Gets the current state and sends it to the client if the socket passed in is a valid one, otherwise if sock
         is None all clients need to receive the state change. The state change is sent in the form "SC:STATE_HERE"

        :param sock: Optional: Socket of client that needs a state change sent to it
        :return:
        """
        if sock:
            if sock in self.ins:
                self.outs.append(sock)  # during next server loop data[s] will be sent to this socket s
                self.data[sock] = "SC:" + self.state.currState + ":"# SC - signifies state change + the current state
        else:
            for s in self.ins:
                if s != self.server:
                    self.outs.append(s)  # during next server loop data[s] will be sent to this socket s
                    self.data[s] = "SC:" + self.state.currState + ":" # SC - signifies state change + the current state

    def handleAwake(self, sock, part2):
        """ Deals with the client if they are connected but have no data to be sent about state changes or the game.
        part 2 contains the current state of the client, and if this is not equal to the current state of the server.
        The state change is resent to the client.
        If the client is in the TEAM_SCREEN state, continuously send them the number of teams, to make sure the client
        receives that info

        :param sock: Socket of the client that sent the Awake message
        :param part2: String containing the current state of the client
        """
        print(part2)
        if part2 != self.state.currState:
            self.sendStateChange(sock)
        elif part2 == State.TEAM_SCREEN:
            # part2 is equal to current state, check if state is TEAM_SCREEN - send numTeams
            if sock in self.ins:
                self.outs.append(sock)  # during next server loop data[s] will be sent to this socket s
                self.data[sock] = "NT:" + str(int( len(list(self.adrs.keys()))/2 )) + ":"

    def updateTeams(self, teams):
        self.teams = teams

    def assignPlayerIndex(self, sock):
        """ assigns the correct index to each player. Even numbers are drivers and odd numbers are gunners.
        0,1 are a pair - 2,3 are a pair etc

        :param sock: the client that started the game - so they are playerIndex 0
        """
        for i in range(0, len(list(self.teams.keys()))):
            for s in self.adrs.keys():
                for k in self.adrs[s].keys():
                    if self.adrs[s][k] == self.teams[i]["driver"]:
                        self.adrs[s][i*2] = self.adrs[s].pop(k)
                    elif self.adrs[s][k] == self.teams[i]["gunner"]:
                        self.adrs[s][i*2+1] = self.adrs[s].pop(k)

    def updateMainScreen(self, sock, msg):
        """ Client either selects an option on the main screen or writes a message to be displayed

        :param sock:
        :param msg:
        :return:
        """
        # todo allow options to be selected by a client and managed here
        output = '{!s}: {!s}\n'.format(self.adrs[sock], msg)
        self.updateGameInfoSig.emit(output)

    def updateTeamScreen(self, sock, msg):
        """ Manage the team selection screen, where players will be able to organise into teams of two. Once teams have
        been organised playerIndices need to be assigned to the players.

        :param sock:
        :param msg:
        :return:
        """
        self.setupTeamSig.emit(self.adrs[sock], msg)


    def updateGameScreen(self, sock, msg):
        """ Client has sent controls as a string. Controls may be movement,

        :param sock:
        :param msg:
        :return:
        """
        print("GAME TIME: " + str(self.gameStartTime) + " clock: " + str(time.clock()))
        currTime = time.clock()
        if self.gameStartTime - currTime <= -120:
            # game has lasted two minutes - game over
            self.state.currState = State.MAIN_SCREEN
            self.updateActiveWidget.emit(self.adrs)
            self.sendStateChange()
        else:
            self.updateGameSig.emit(self.adrs[sock], msg, int(currTime))  # send first value in dict (address)