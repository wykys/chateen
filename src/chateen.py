#!/usr/bin/env python3


import sys
from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools
from gui import MainWindow

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
