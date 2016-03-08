from PyQt5.QtCore import QObject, pyqtSignal

class ServerMainUiSignals(QObject):

    appendConnectedHistorySig = pyqtSignal(['QString'])

    def __init__(self, parent=None):
        super(ServerMainUiSignals, self).__init__(parent)