#!/usr/bin/env python3


from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

from template_main_win import Ui_MainWindow
from database import db, Chat, Participant, Message
from loader_fb import FbLoader
from loader_ig import IgLoader

import tables


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chateen')
        self.load_new_data()

    def set_completer_name(self):
        names = list([n.name for n in db.get_participants().all()])
        completer = QtWidgets.QCompleter(names)
        self.line_edit_participant.setCompleter(completer)

    def load_new_data(self):
        self.chats_array = []
        self.update_table()
        self.set_completer_name()
        self.sync_db_chat_selected()
        self.callback_check_export_is_ready()

    def sync_db_chat_selected(self):
        self.table_chats.blockSignals(True)
        for row, id in enumerate(self.chats_array):
            item = self.table_chats.item(row, 0)
            chat = db.get_chats().filter(Chat.id == id).first()
            chat.selected = bool(item.checkState())
            db.commit()
        self.table_chats.blockSignals(False)

    def callback_check_export_is_ready(self):

        date_from_state = self.date_from.isEnabled()
        date_to_state = self.date_from.isEnabled()

        date_from = self.date_from.dateTime()
        date_to = self.date_to.dateTime()

        chats = db.get_chats().filter(Chat.selected == True)



        if chats.count() == 0:
            self.btn_export.setEnabled(False)
            return False

        who=self.radio_button_who_one.isChecked()
        if who:
            name=self.line_edit_participant.text()
            if db.get_participants().filter(Participant.name == name).first() is None:
                self.btn_export.setEnabled(False)
                return False
        else:
            print(chats)

        self.btn_export.setEnabled(True)
        return True

    def callback_btn_export(self):
        print('export')

        date_from = self.date_from.dateTime().toPython()
        date_to = self.date_to.dateTime().toPython()

        messages = db.get_messages()
        if self.date_from.isEnabled():
            messages = messages.filter(Message.datetime > date_from)
        if self.date_to.isEnabled():
            messages = messages.filter(Message.datetime < date_to)
        messages = messages.join(Chat.messages, Chat.selected == True)

        who=self.radio_button_who_one.isChecked()
        if who:
            name=self.line_edit_participant.text()
            messages = messages.join(Participant.messages, Participant.name == name)

        print(messages.all())

    def callback_menu_file_open(self):
        self.load_new_data()

    def callback_menu_file_open_fb(self):
        path, _=QtWidgets.QFileDialog.getOpenFileName(
            self,
            filter='Facebook JSON (*.json *.JSON)',
            caption='Open Facebook JSON',
            dir='../data'
        )
        FbLoader(path)
        self.load_new_data()

    def callback_menu_file_open_ig(self):
        path, _=QtWidgets.QFileDialog.getOpenFileName(
            self,
            filter='Instagram JSON (*.json *.JSON)',
            caption='Open Instagram JSON',
            dir='../data'
        )
        IgLoader(path)
        self.load_new_data()

    def callback_menu_tools_reduce(self):
        db.reduce()
        self.load_new_data()

    def callback_menu_tools_clean(self):
        db.delete_all()
        self.load_new_data()

    def update_table(self):
        self.update_table_chats()
        self.update_table_participants()
        self.update_table_participant_detail(None)

    def callback_click_table_chat_button(self, chat):
        self.update_table_chat_detail(chat)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def callback_click_table_participant_button(self, participant):
        self.update_table_participant_detail(participant)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def update_table_chats(self):
        self.table_chats.blockSignals(True)
        chats=db.get_chats()
        if not chats is None:
            tables.update_table_chats(self, chats)
        self.table_chats.blockSignals(False)

    def update_table_participants(self):
        participants=db.get_participants()
        if not participants is None:
            tables.update_table_participants(self, participants)

    def update_table_chat_detail(self, chat):
        if not chat is None:
            tables.update_table_chat_detail(self, chat)

    def update_table_participant_detail(self, participant):
        if not participant is None:
            tables.update_table_participant_detail(self, participant)

    def callback_table_chats_cell_changed(self, row, column, toggle=False, value=None):
        item=self.table_chats.item(row, column)
        self.table_chats.blockSignals(True)
        if toggle:
            if bool(item.checkState()):
                item.setCheckState(QtCore.Qt.Unchecked)
            else:
                item.setCheckState(QtCore.Qt.Checked)

        if value == True:
            item.setCheckState(QtCore.Qt.Checked)
        elif value == False:
            item.setCheckState(QtCore.Qt.Unchecked)

        tables.checkbox_decorator(item)
        self.sync_db_chat_selected()
        self.callback_check_export_is_ready()
        self.table_chats.blockSignals(False)

    def callback_table_chats_cell_clicked(self, row, column):
        self.callback_table_chats_cell_changed(row, 0, toggle=True)

    def callback_btn_select_all_clicked(self):
        for row in range(self.table_chats.rowCount()):
            self.callback_table_chats_cell_changed(row, 0, value=True)

    def callback_btn_deselect_all_clicked(self):
        for row in range(self.table_chats.rowCount()):
            self.callback_table_chats_cell_changed(row, 0, value=False)


if __name__ == '__main__':
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app=QtWidgets.QApplication(sys.argv)

    win=MainWindow()
    win.show()

    sys.exit(app.exec_())
