#!/usr/bin/env python3

import sys
from PySide2.QtWidgets import QApplication, QWidget, QDialog, QPushButton, QLineEdit, QVBoxLayout, QFileDialog, QDesktopWidget, QGroupBox, QRadioButton, QCompleter
from loader_fb import FbLoader
from loader_ig import IgLoader


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.corpus = None

        self.setWindowTitle('Chateen')
        self.setGeometry(300, 300, 300, 300)
        self.center_window()

        self.vbox = QVBoxLayout()
        self.create_load_ui()
        self.setLayout(self.vbox)

    def center_window(self):
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    def create_load_ui(self):
        group_box = QGroupBox('Načti data')

        self.radio_ig = QRadioButton('Instagram')
        self.radio_fb = QRadioButton('Facebook')

        self.radio_ig.setChecked(True)

        button = QPushButton('Vyber JSON')
        button.clicked.connect(self.load_json)

        vbox = QVBoxLayout()
        vbox.addWidget(self.radio_ig)
        vbox.addWidget(self.radio_fb)
        vbox.addWidget(button)
        vbox.addStretch(1)

        group_box.setLayout(vbox)
        self.vbox.addWidget(group_box)

    def load_json(self):
        path, _ = QFileDialog.getOpenFileName(self, filter='JSON (*.json *.JSON)', caption='Open JSON', dir='../data')

        if self.radio_ig.isChecked():
            self.corpus = IgLoader(path).corpus
        else:
            self.corpus = FbLoader(path).corpus

        self.corpus.show()
        self.create_participant_ui()

    def create_participant_ui(self):
        group_box = QGroupBox('Najdi se')

        completer = QCompleter(self.corpus.get_participants())
        self.participant = QLineEdit()
        self.participant.setCompleter(completer)

        vbox = QVBoxLayout()
        vbox.addWidget(self.participant)
        vbox.addStretch(1)

        group_box.setLayout(vbox)
        self.vbox.addWidget(group_box)


class GUI(object):
    def __init__(self):
        app = QApplication(sys.argv)
        win = Window()
        win.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    GUI()
