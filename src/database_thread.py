from PySide2 import QtCore

from loader_ig import IgLoader


class DatabaseSignals(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(int)

class DatabaseThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(DatabaseThread, self).__init__()
        self.signals = DatabaseSignals()

    @QtCore.Slot()
    def run(self):
        #IgLoader(callback_progress=self.signals.progress)
        IgLoader()

