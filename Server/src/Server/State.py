


class State():

    # All the available game states
    MAIN_SCREEN = "MAIN_SCREEN"
    TEAM_SCREEN = "TEAM_SCREEN"
    GAME_SCREEN = "GAME_SCREEN"

    states = [MAIN_SCREEN,TEAM_SCREEN, GAME_SCREEN]

    def __init__(self):
        self.currState = self.MAIN_SCREEN