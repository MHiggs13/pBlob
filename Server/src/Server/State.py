


class State():

    # All the available game states
    MAIN_SCREEN = "MAIN_SCREEN"
    GAME_SCREEN = "GAME_SCREEN"
    #
    # currState = ""
    # isStateChanged = False

    def __init__(self):
        self.currState = self.MAIN_SCREEN
        self.isStateChanged = False # todo not used atm