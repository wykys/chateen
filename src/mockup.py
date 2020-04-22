#!/usr/bin/env python3
# pip3 install pyqt5
# pyuic5 path_to_your_ui_file -o path_to_the_output_python_file

from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

from template_main_win import Ui_MainWindow
from database import db, Chat, Participant


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chateen')
        self.update_table()

    def menu_file_open(self):
        print('Ahoj')
        self.update_table()

    def update_table(self):
        self.update_table_chats()
        self.update_table_participants()

    def update_table_chats(self):

        self.table_chats.setColumnCount(5)
        self.table_chats.clearContents()
        self.table_chats.setRowCount(0)
        self.table_chats.setSortingEnabled(True)

        self.table_chats.setHorizontalHeaderLabels(
            ['Zpracovat', 'Počet zpráv', 'Počet účastníků', 'Účastníci', 'Více']
        )

        for r, chat in enumerate(db.get_chats()):

            item1 = QtWidgets.QTableWidgetItem()
            item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable)
            item1.setCheckState(QtCore.Qt.Unchecked)
            item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            item1.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

            item2 = QtWidgets.QTableWidgetItem(str(chat.get_cnt_messages()))
            item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item2.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

            item3 = QtWidgets.QTableWidgetItem(str(chat.get_cnt_participants()))
            item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item3.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

            item4 = QtWidgets.QTableWidgetItem(str(chat.participants)[1:-1])
            item4.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            button = QtWidgets.QPushButton('...')
            button.clicked.connect(lambda y=0, x=chat: self.button_click(x))
            layout.addWidget(button)

            item5 = QtWidgets.QWidget()
            item5.setLayout(layout)

            self.table_chats.insertRow(self.table_chats.rowCount())
            for c, item in enumerate([item1, item2, item3, item4]):
                self.table_chats.setItem(r, c, item)

            self.table_chats.setCellWidget(r, 4, item5)

        header = self.table_chats.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.table_chats.setColumnWidth(4, 20)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def update_table_participants(self):

        self.table_participants.setColumnCount(4)
        self.table_participants.clearContents()
        self.table_participants.setRowCount(0)
        self.table_chats.setSortingEnabled(True)

        self.table_participants.setHorizontalHeaderLabels(
            ['Jméno', 'Počet zpráv', 'Počet chatů', 'Více']
        )

        for r, participant in enumerate(db.get_participants()):

            item1 = QtWidgets.QTableWidgetItem(str(participant.name))
            item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            item1.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

            item2 = QtWidgets.QTableWidgetItem(str(participant.get_cnt_messages()))
            item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item2.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

            item3 = QtWidgets.QTableWidgetItem(str(participant.get_cnt_chats()))
            item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            item3.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            button = QtWidgets.QPushButton('...')
            button.clicked.connect(lambda y=0, x=participant: self.button_click(x))
            layout.addWidget(button)

            item4 = QtWidgets.QWidget()
            item4.setLayout(layout)

            self.table_participants.insertRow(self.table_participants.rowCount())
            for c, item in enumerate([item1, item2, item3]):
                self.table_participants.setItem(r, c, item)

            self.table_participants.setCellWidget(r, 3, item4)

        header = self.table_participants.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table_participants.setColumnWidth(3, 20)

    def button_click(self, chat):
        WinMessages(self, chat)


class UiWinFactory(object):
    pass


if __name__ == '__main__':
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
