#!/usr/bin/env python3

import sys
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools
from chateen.gui import MainWindow


class App(object):
    def __init__(self):
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
        app = QtWidgets.QApplication(sys.argv)
        win = MainWindow()
        win.show()
        sys.exit(app.exec_())