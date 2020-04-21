#!/usr/bin/env python3

import sys
from PySide2 import QtCore, QtGui, QtWidgets
from gui_prototype import AppPrototype

from loader_fb import FbLoader
from loader_ig import IgLoader


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.corpus = None

        self.setWindowTitle('Chateen')
        self.setGeometry(300, 300, 300, 300)
        self.center_window()

        self.vbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox)
        self.create_load_ui()

    def center_window(self):
        rectangle = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    def create_load_ui(self):
        group_box = QtWidgets.QGroupBox('Načti data')

        self.radio_ig = QtWidgets.QRadioButton('Instagram')
        self.radio_fb = QtWidgets.QRadioButton('Facebook')

        self.radio_ig.setChecked(True)

        button = QtWidgets.QPushButton('Vyber JSON')
        button.clicked.connect(self.load_json)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.radio_ig)
        vbox.addWidget(self.radio_fb)
        vbox.addWidget(button)
        vbox.addStretch(1)

        group_box.setLayout(vbox)
        self.vbox.addWidget(group_box)

    def load_json(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, filter='JSON (*.json *.JSON)', caption='Open JSON', dir='../data')

        if self.radio_ig.isChecked():
            self.corpus = IgLoader(path).corpus
        else:
            self.corpus = FbLoader(path).corpus

        self.create_participant_ui()

    def create_participant_ui(self):
        group_box = QGroupBox('Najdi se')

        completer = QCompleter(self.corpus.get_participants())
        self.participant = QLineEdit()
        self.participant.setCompleter(completer)

        button = QtWidgets.QPushButton('Vyber konverzace')
        button.clicked.connect(self.create_chat_ui)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.participant)
        vbox.addWidget(button)
        vbox.addStretch(1)

        group_box.setLayout(vbox)
        self.vbox.addWidget(group_box)

    def create_chat_ui(self):
        if not self.participant.text() in self.corpus.get_participants():
            msg = QMessageBox()
            msg.setText('Zadané jméno není platné.')
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle('Chateen varování')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            return

        group_box = QtWidgets.QGroupBox('Vyber konverzace k exportu')

        completer = QtWidgets.QCompleter(self.corpus.get_participants())
        self.participant = QLineEdit()
        self.participant.setCompleter(completer)

        button = QtWidgets.QPushButton('Vyber konverzace')
        button.clicked.connect(self.create_chat_ui)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.participant)
        vbox.addWidget(button)
        vbox.addStretch(1)

        group_box.setLayout(vbox)
        self.vbox.addWidget(group_box)


class GUI(AppPrototype):
    def __init__(self):
        super(GUI, self).__init__()

        win = Window()
        win.show()

        self.run()


if __name__ == '__main__':
    GUI()
