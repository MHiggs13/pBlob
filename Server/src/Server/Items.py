from PyQt5.QtWidgets import QGraphicsPixmapItem


class Item(QGraphicsPixmapItem):
    """ Super class to be used as a base for all items within the game.
        # Walls
        # Slows
        # Speed boosts
    """
    def __init__(self, pixmap, x, y):
        super(Item, self).__init__()
        self.setPixmap(pixmap)

        self.setPos(x, y)
        self.show()

class Wall(Item):
    """ Stationary item/object on the game board, blobs or projectiles cannot pass through.

    """
    def __init__(self, pixmap, x , y):
        super(Wall, self).__init__(pixmap, x, y)

        # means a collision onlu occurs with the opaque parts of the pixmap
        self.setShapeMode(QGraphicsPixmapItem.MaskShape)

