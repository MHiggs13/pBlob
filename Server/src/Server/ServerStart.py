import sys
from src.GUI.App import App


if __name__=='__main__':
    app = App(sys.argv)
    app.window.loadDefaultInformation()