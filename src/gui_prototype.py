#!/usr/bin/env python3

import sys
from PySide2 import QtWidgets, QtGui, QtCore


class AppPrototype(object):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.set_theme()

    def set_theme(self):
        self.app.setStyle(QtWidgets.QStyleFactory.create("fusion"))

        darktheme = QtGui.QPalette()
        darktheme.setColor(QtGui.QPalette.Window, QtGui.QColor(45, 45, 45))
        darktheme.setColor(QtGui.QPalette.WindowText, QtGui.QColor(222, 222, 222))
        darktheme.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 45))
        darktheme.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(222, 222, 222))
        darktheme.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(222, 222, 222))
        darktheme.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(222, 222, 222))
        darktheme.setColor(QtGui.QPalette.Highlight, QtGui.QColor(45, 45, 45))

        self.app.setPalette(darktheme)

    def run(self):
        sys.exit(self.app.exec_())
