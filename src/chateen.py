#!/usr/bin/env python3


from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

from template_main_win import Ui_MainWindow
from database import db
from loader_fb import FbLoader
from loader_ig import IgLoader

import tables


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chateen')

    def set_completer_name(self):
        names = list([n.name for n in db.get_participants().all()])
        completer = QtWidgets.QCompleter(names)
        self.line_edit_participant.setCompleter(completer)

    def load_new_data(self):
        self.update_table()
        self.set_completer_name()

    def action_menu_file_open(self):
        self.load_new_data()

    def action_menu_file_open_fb(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            filter='Facebook JSON (*.json *.JSON)',
            caption='Open Facebook JSON',
            dir='../data'
        )
        FbLoader(path)
        self.load_new_data()

    def action_menu_file_open_ig(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            filter='Instagram JSON (*.json *.JSON)',
            caption='Open Instagram JSON',
            dir='../data'
        )
        IgLoader(path)
        self.load_new_data()

    def action_menu_tools_reduce(self):
        db.reduce()
        self.load_new_data()

    def action_menu_tools_clean(self):
        db.delete_all()
        self.load_new_data()

    def update_table(self):
        self.update_table_chats()
        self.update_table_participants()
        self.update_table_participant_detail(None)

    def click_table_chat_button(self, chat):
        print('CHAT')
        self.update_table_chat_detail(chat)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def click_table_participant_button(self, participant):
        print('PARTICIPANT')
        self.update_table_participant_detail(participant)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def update_table_chats(self):
        chats = db.get_chats()
        if not chats is None:
            tables.update_table_chats(self, chats)

    def update_table_participants(self):
        participants = db.get_participants()
        if not participants is None:
            tables.update_table_participants(self, participants)

    def update_table_chat_detail(self, chat):
        if not chat is None:
            tables.update_table_chat_detail(self, chat)

    def update_table_participant_detail(self, participant):
        if not participant is None:
            tables.update_table_participant_detail(self, participant)


if __name__ == '__main__':
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
