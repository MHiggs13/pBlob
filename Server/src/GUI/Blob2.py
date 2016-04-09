import math
from PyQt5.QtWidgets import QLabel, QGraphicsPixmapItem, QGraphicsItemGroup
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt

class Blob(QGraphicsItemGroup):
    """ Allow for a blob to be drawn on GameBoard """

    def __init__(self, parent, client1, client2, boardWidth, boardHeight):
        super(Blob, self).__init__()

        self.blob = QGraphicsPixmapItem()

        self.width = 200
        self.height = 200

        self.driver = client1
        self.gunner = client2


        self.blob.setPixmap(QPixmap('C:\\Users\\michaelh\\Desktop\\CSC Project\\Server\\src\\resources\\blueBlob.png'))
        self.blob.setPixmap(self.blob.pixmap().scaled(self.width, self.height,
                                               Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.defSpeed = 3
        self.xSpeed = 0
        self.ySpeed = 0

        self.gun = Gun(self, boardWidth, boardHeight)
        self.gun.setPos((self.width - self.gun.width) / 2, (self.height - self.gun.height) / 2)

        self.addToGroup(self.blob)
        self.addToGroup(self.gun)

        self.show()


    def updatePos(self, dim):
        """ update the position using the speed variable, this will be set by the GameBoard class
        dim is a list of the dimensions of the board, [width, height] """
        # Draw blob in it's new position
        print("dim", dim)
        x = self.x() + self.xSpeed
        y = self.y() + self.ySpeed

        # Check x
        if x < 0:
            x = 0
        elif x + self.width > dim[0]:
            x = dim[0] - self.width  # Sets x to be equal to width of the widget minus width of blob

        # Check y
        if y < 0:
            y = 0
        elif y + self.height > dim[1]:
            y = dim[1] - self.height  # Sets y to be equal to height of the widget minus height of blob

        print("X()= ", self.x(), "x= ", x)
        self.setPos(x, y)


    def onDraw(self, dim):
        self.updatePos(dim)
        self.gun.onDraw(self.x(), self.y())

class Gun(QGraphicsPixmapItem):
    """ Contains all information to do with a blobs gun     """

    def __init__(self, parent, boardWidth, boardHeight):
        super(Gun, self).__init__()
        self.fireTally = 0

        self.boardWidth = boardWidth
        self.boardHeight = boardHeight

        self.width = 150
        self.height = 150

        self.setPixmap(QPixmap('C:\\Users\\michaelh\\Desktop\\CSC Project\\Server\\src\\resources\\cannon.png'))
        self.setPixmap(self.pixmap().scaled(self.width, self.height,
                                               Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.actualAngle = 0.0  # Starts off at 0, horizontal, pointing at 3 on a clock, value between 0 and 359, ANTI CLOCKWISE ANGLE
        self.desiredAngle = 0.0  # Angle determined by where the user has moved the thumbstick to, CLOCKWISE ANGLE
        self.angleIncrement = 1.0  # actual angle is icnremented by this value until it reaches the desired angle

        self.rotateClockwise = True

        self.setTransformOriginPoint(self.width/2, self.height/2)

        self.projectiles = set()
        self.pToRemove = set()

        self.show()

    def updateOrientation(self):
        """ Changes the visual orientation of the gun to the actual orientation value

        :return:
        """
        if self.desiredAngle == -1:  # thumbstick is neutral, so stop rotating
            self.desiredAngle = self.rotation()
        elif self.rotateClockwise and (self.desiredAngle - self.rotation()) < 0:
            # if rotating clockwise and quickest path to desired is anti clockwise, switch AND likewise anticlockwise
            self.rotateClockwise = not self.rotateClockwise
        elif not self.rotateClockwise and (self.desiredAngle - self.rotation()) >= 0:
            self.rotateClockwise = not self.rotateClockwise

        if self.rotateClockwise:
            if abs(self.desiredAngle - self.rotation()) > 20:
                self.setRotation(self.rotation() + 2)
            elif self.desiredAngle != self.rotation():
                self.setRotation(self.rotation() + 1)
        else:
            if abs(self.desiredAngle - self.rotation()) > 20:
                self.setRotation(self.rotation() - 2)
            elif self.desiredAngle != self.rotation():
                self.setRotation(self.rotation() - 1)

        # make sure rotation is within the bounds 0 - 360
        if self.rotation() > 360:
            self.setRotation(self.rotation() - 360)
        elif self.rotation() < 0:
            self.setRotation(self.rotation() + 360)

    def updateFiring(self, blobX, blobY):
        """ Check if the gun should fire a Projectile. If the fireTally is greater than 0, fire 1 projectile.

        :return:
        """
        for p in self.projectiles:
            isActive = p.update()
            if not isActive:
                self.pToRemove.add(p)

        print(self.fireTally)
        if self.fireTally > 0:
            self.fireTally -= 1
            self.projectiles.add(Projectile(blobX, blobY, self.width, self.height, self.rotation(), self.boardWidth, self.boardHeight))

    def onDraw(self, blobX, blobY):
        self.updateOrientation()
        self.updateFiring(blobX, blobY)

class Projectile(QGraphicsPixmapItem):
    """ Created by the Gun class appears on the Board's scene. The projectile will only stay active if the projectile is
    not out of the bounds of the scene, if it has not collided with a Blob
    """
    def __init__(self, gunX, gunY, gunWidth, gunHeight, gunAngle, boardWidth, boardHeight):
        super(Projectile, self).__init__()

        self.boardWidth = boardWidth
        self.boardHeight = boardHeight

        self.width = 50
        self.height = 50

        # dX and dY use the current angle to the gun to know what direction to travel in
        self.dX = math.cos(math.radians(gunAngle))
        self.dY = math.sin(math.radians(gunAngle))

        self.setPixmap(QPixmap('C:\\Users\\michaelh\\Desktop\\CSC Project\\Server\\src\\resources\\cannon_ball.png'))
        self.setPixmap(self.pixmap().scaled(self.width, self.height,
                                               Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.setPos(gunX + gunWidth/2 + (gunWidth/2 * self.dX), gunY + gunHeight/2 + (gunHeight/2 * self.dY))
        self.show()

    def cosDeg(self, angle):
        """ finds the cos(angle) in degrees  """
        return

    def sinDeg(self, angle):
        pass

    def update(self):
        self.setPos(self.x() + self.dX, self.y() + self.dY)
        if self.x() < 0 or self.x() > self.boardWidth or self.y() < 0 or self.y() > self.boardHeight:  # todo update to Board from Board2
            return False
        else:
            return True