#!/usr/bin/env python3

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QStyleFactory
from database import db


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.create_table()

    def create_table(self):
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['Chat ID', 'Počet zpráv', 'Počet účestníků', 'Účastníci'])

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


            self.table.insertRow(self.table.rowCount())
            for c, item in enumerate([item1, item2, item3, item4]):
                self.table.setItem(r, c, item)

        self.setCentralWidget(self.table)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
