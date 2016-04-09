import re
from decimal import Decimal

import math
from socket import AddressFamily

from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QScrollBar

from src.GUI.Blob2 import Blob


class Board(QGraphicsView):
    """ Class that creates the game UI and manages player actions """

    # Default variables
    BOARD_HEIGHT = 621
    BOARD_WIDTH = 1000

    """ Initialize the GameBoard class """
    def __init__(self):
        super(Board, self).__init__()
        print("Initiated board")
        self.setHorizontalScrollBarPolicy(1)  # Qt::ScrollBarAlwaysOff = 1
        self.setVerticalScrollBarPolicy(1)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0,0, self.BOARD_WIDTH, self.BOARD_HEIGHT)

    def start(self, adrs):
        self.setupUI(adrs)

    """ Create initial state for the initial board UI """
    def setupUI(self, adrs):

        self.resize(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.setWindowTitle('Blobbageddon!')

        # sort clients into correct teams for each blob, client 1 = driver, client 2 = gunner
        clients = []
        self.listBlobs = []
        pIndices = []
        i = 0
        # for all sockets add their key (player index) to a single list of keys and sort
        for s in adrs.keys():
            pIndices.append(list(adrs[s].keys())[0])  # todo may not be thread safe http://blog.labix.org/2008/06/27/watch-out-for-listdictkeys-in-python-3
        pIndices = sorted(pIndices)  # sort the keys by numerical value (0,1,2,3)
        print("sorted KEYS = ", pIndices)
        # go through each index in order and then add the address of the socket that has that player index
        for index in pIndices:
            for s in adrs.keys():
                if index in list(adrs[s].keys()):  # todo may not be thread safe http://blog.labix.org/2008/06/27/watch-out-for-listdictkeys-in-python-3
                    print("KEY: ", index)
                    print(adrs[s][index])
                    clients.append(adrs[s][index])  # since keys are sorted add in order to ads list
            i += 1
        j = 0
        while j < len(clients):
            print(clients[j])
            self.listBlobs.append((Blob(self.scene, clients[j], clients[j+1], self.BOARD_WIDTH, self.BOARD_HEIGHT)))
            j += 2
        for blob in self.listBlobs:
            self.scene.addItem(blob)

        self.setScene(self.scene)

        self.show()

    def getXY(self, strPos):
        """ Gets x and y from the movement string passed from clients

        :param strPos: Movement string received from clients - e.g. '5.432, -145.623532;'
        :return:
        """
        # regex to distinguish if c is a correct character
        pattern = "-|\d|\."

        x = ''
        y = ''
        isXFinished = False

        # Receive the position from the client and change to x and y
        for c in strPos:
            if c == ';':
                break
            else:
                match = re.match(pattern, c)
            if not isXFinished:
                if c == ',':
                    isXFinished = True
                elif match:
                    x += c
            elif match:
                y += c

        return (x, y)

    def updatePos(self, address, strPos):
        """ If address is a driver for a blob then that blob's position will be recalculated using the string passed in

        :param address: The client that has sent the string, must appear in a blob's driver to change pos
        :param strPos:  The movement string passed by the client
        :return: True if driver, meaning address is not a gunner, allows updateGun call to be skipped
        """
        for blob in self.listBlobs:
            if blob.driver == address:

                x, y = self.getXY(strPos)

                # Divide x and y by 100 and remove decimal points to get speed factor
                x = Decimal(x)
                y = Decimal(y)
                x = int(x/100)
                y = int(y/100)


                # Speed becomes equal to x * defSpeed, y * defSpeed
                blob.xSpeed = blob.defSpeed * x
                blob.ySpeed = blob.defSpeed * y
                return True  # return true, know not to carry out gunner
            else:
                return False  # return fals, so carry out gunner

    def getFireTally(self, strGun):
        """ Get the amount of fires sent by a client, and add to the tally of fires to be made by that gunner

        :param strGun:
        :return: the amount of "fires" to add to the Gun's fire tally, followed by the remainder of strGun
        """

        # regex to distinguish if c is a correct character
        pattern = "\d+\,"
        search = re.findall(pattern, strGun)

        tally = 0

        if not search:
            return -1  # return -1, no valid angle so keep orientation the same
        else:
            for e in search:
                tally += int(e[:len(e)-1])
        return tally

    def getAngle(self, strGun):
        """ Takes a string and retries the angle passed in

        :param strGun: eg. ".532523523;3.151515125l;4.323123;"
        :return: the angle passed in eg. 3
        """
        # regex to distinguish if c is a correct character
        pattern = "-?\d+(\.\d+)\;"
        search = re.search(pattern, strGun)

        if not search:
            return -1  # return -1, no valid angle so keep orientation the same
        else:
            angle = search.group(0)
            return math.trunc(float(angle[:len(angle)-1]))

    def updateGun(self, address, strGun):
        """ Take inputs from user and if the fire button has been pressed fire a projectile

        :param address: The client that sent the update gun request
        :param strGun: Contains information about what direction the gun is facing and if fire button has been pressed
        :return: True if address was a gunner
        """
        for blob in self.listBlobs:
            if blob.gunner == address: # if address passed in is a gunner carry out gunner stuff
                blob.gun.fireTally = self.getFireTally(strGun)
                blob.gun.desiredAngle = self.getAngle(strGun)

    """ Update game graphics with respect to the current game state """
    def updateGame(self, addressDict, input):
        try:
            for key in addressDict.keys():
                address = addressDict[key]
            isDriver = self.updatePos(address, input)
            if not isDriver:
                isGunner = self.updateGun(address, input)

            self.drawGame()
        except ValueError:
            print("address was not assigned a value before being used")

    def manageProjectiles(self, blob):
        """ Manage projectiles - send the call to update position on screen, remove from active projectiles if
        necessary.
        :return:
        """
        for p in blob.gun.projectiles:
            if not p in self.scene.items():
                self.scene.addItem(p)


        tempList = []
        """ Put items that are still in the group and are marked to be removed into a temporary list to allow for their
        removal without causing an error within the for loop
        """
        for item in self.scene.items():
            if item in blob.gun.pToRemove:
                tempList.append(item)  # items in tempList are Projectiles that are marked to be removed


        for p in tempList:
            blob.gun.projectiles.remove(p)  # remove from active projectile set
            self.scene.removeItem(p)  # Remove the item from the group
            blob.gun.pToRemove.remove(p)  # Remove the projectile from the set signifying it should be removed

    """ Draw all graphics in the game """
    def drawGame(self):
        for blob in self.listBlobs:
            blob.onDraw([self.width(), self.height()])
            self.manageProjectiles(blob)
