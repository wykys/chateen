#!/usr/bin/env python3

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QStyleFactory
from database import db, Chat


class Window(QtWidgets.QMainWindow, QtGui.QWindow):
    def __init__(self, parent=None, chat=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle('Chateen - konverzace')
        self.setGeometry(300, 300, 300, 300)
        self.center_window()

        self.vbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox)

        self.create_table(chat)
        self.show()

    def center_window(self):
        rectangle = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    def create_table(self, chat):
        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ['Datum', 'Odesilatel', 'Text']
        )

        for r, message in enumerate(chat.messages):

            item1 = QtWidgets.QTableWidgetItem(message.datetime.strftime('%H:%M:%S    %Y/%m/%d'))
            item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            item2 = QtWidgets.QTableWidgetItem(str(message.participant))
            item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            item3 = QtWidgets.QTableWidgetItem(str(message.text))

            self.table.insertRow(self.table.rowCount())
            for c, item in enumerate([item1, item2, item3]):
                self.table.setItem(r, c, item)

        self.setCentralWidget(self.table)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Chateen - skupiny')
        self.setGeometry(300, 300, 600, 600)
        self.create_table()

    def create_table(self):
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ['Chat ID', 'Počet zpráv', 'Počet účestníků', 'Účastníci', 'Podrobnosti']
        )

        for r, chat in enumerate(db.get_chats()):

            item1 = QtWidgets.QTableWidgetItem(str(chat.id))
            item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable)
            item1.setCheckState(QtCore.Qt.Unchecked)
            item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            item2 = QtWidgets.QTableWidgetItem(str(chat.get_cnt_messages()))
            item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            item3 = QtWidgets.QTableWidgetItem(str(chat.get_cnt_participants()))
            item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            item4 = QtWidgets.QTableWidgetItem(str(chat.participants)[1:-1])

            layout = QtWidgets.QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            button = QtWidgets.QPushButton('...')
            button.clicked.connect(lambda y=0, x=chat: self.fce(x))
            layout.addWidget(button)

            item5 = QtWidgets.QWidget()
            item5.setLayout(layout)

            self.table.insertRow(self.table.rowCount())
            for c, item in enumerate([item1, item2, item3, item4]):
                self.table.setItem(r, c, item)

            self.table.setCellWidget(r, 4, item5)

        self.setCentralWidget(self.table)

    def fce(self, chat):
        win = Window(self, chat)
        win.create()
        # win.exec_()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    # app.setFont(QtGui.QFont.family.)
    sys.exit(app.exec_())
