#!/usr/bin/env python3


from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

from template_main_win import Ui_MainWindow
from database import db
from loader_fb import FbLoader
from loader_ig import IgLoader

import tables
from datetime import datetime


def print_time(msg=None):
    if not msg is None:
        print(msg)
    print(datetime.now().time())


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chateen')

        """
        print_time('load JSON')
        IgLoader()
        print_time('load ok')
        """

        self.load_new_data()

    def load_new_data(self):
        self.chats_array = []
        print_time('update table')
        self.update_table()
        print_time('completer')
        self.set_completer_name()
        print_time('sync')
        self.sync_db_chat_selected()
        print_time('check export')
        self.callback_check_export_is_ready()
        print_time('load ok')

    def set_completer_name(self):
        names = list([n.name for n in db.get_participants().all()])
        completer = QtWidgets.QCompleter(names)
        self.line_edit_participant.setCompleter(completer)

    def sync_db_chat_selected(self, row=None):
        self.table_chats.blockSignals(True)
        if row is None:
            for row, id in enumerate(self.chats_array):
                item = self.table_chats.item(row, 0)
                chat = db.get_chats().filter_by(id=id).first()
                chat.selected = bool(item.checkState())
        else:
            id = self.chats_array[row]
            chat = db.get_chats().filter_by(id=id).first()
            item = self.table_chats.item(row, 0)
            chat.selected = bool(item.checkState())
        db.commit()
        self.table_chats.blockSignals(False)

    def callback_check_export_is_ready(self):
        date_from = self.date_from.dateTime().toPython()
        date_to = self.date_to.dateTime().toPython()

        name = self.line_edit_participant.text()

        export = db.get_messages().join(db.Chat).filter(db.Chat.selected == True)

        if self.date_from.isEnabled():
            export = export.filter(db.Message.datetime > date_from)

        if self.date_to.isEnabled():
            export = export.filter(db.Message.datetime < date_to)

        who = self.radio_button_who_one.isChecked()
        if who:
            name = self.line_edit_participant.text()
            export = export.join(db.Participant).filter(db.Participant.name == name)

        if export.count() > 0:
            self.btn_export.setEnabled(True)
        else:
            self.btn_export.setEnabled(False)

    def callback_btn_export(self):
        print_time('Export Start')

        date_from = self.date_from.dateTime().toPython()
        date_to = self.date_to.dateTime().toPython()

        name = self.line_edit_participant.text()
        who = self.radio_button_who_one.isChecked()
        format_is_chat_split = self.checkbox_export_format.isChecked() and self.checkbox_export_format.isEnabled()

        export_msg = db.get_messages().join(db.Chat).filter(db.Chat.selected == True).join(db.Participant)

        if self.date_from.isEnabled():
            export_msg = export_msg.filter(db.Message.datetime > date_from)

        if self.date_to.isEnabled():
            export_msg = export_msg.filter(db.Message.datetime < date_to)

        if who:
            name = self.line_edit_participant.text()
            export_msg = export_msg.filter(db.Participant.name == name)

        if format_is_chat_split:
            owner_list = [id.chat for id in export_msg.group_by(db.Chat)]
        else:
            owner_list = [id.participant for id in export_msg.group_by(db.Participant)]

        for owner in owner_list:
            if format_is_chat_split:
                messages = export_msg.filter(db.Message.chat == owner)
            else:
                messages = export_msg.filter(db.Message.participant == owner)

            name = owner.name
            if name is None:
                name = f'chat_{owner.id:09}'
            path = f'../out/{name}.txt'
            print(name)

            with open(path, 'w') as fw:
                fw.writelines([f'<s>{msg.text}</s>\n' for msg in messages])

        print_time('Export End')

    def callback_menu_file_open_fb(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            filter='Facebook JSON (*.json *.JSON)',
            caption='Open Facebook JSON',
            dir='../data'
        )
        FbLoader(path)
        self.load_new_data()

    def callback_menu_file_open_ig(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
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
        print_time('start update table')
        self.update_table_chats()
        print_time('update table 1')
        self.update_table_participants()
        print_time('update table 2')
        self.update_table_participant_detail()
        print_time('update table ok')

    def callback_click_table_chat_button(self, chat):
        self.update_table_chat_detail(chat)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def callback_click_table_participant_button(self, participant):
        self.update_table_participant_detail(participant)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def update_table_chats(self):
        self.table_chats.blockSignals(True)
        chats = db.get_chats()
        if not chats is None:
            tables.update_table_chats(self, chats)
        self.table_chats.blockSignals(False)

    def update_table_participants(self):
        participants = db.get_participants()
        if not participants is None:
            tables.update_table_participants(self, participants)

    def update_table_chat_detail(self, chat):
        if not chat is None:
            tables.update_table_chat_detail(self, chat)

    def update_table_participant_detail(self, participant=None):
        if not participant is None:
            tables.update_table_participant_detail(self, participant)

    def callback_table_chats_cell_changed(self, row, column, toggle=False, value=None):
        item = self.table_chats.item(row, column)
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
        self.sync_db_chat_selected(row)
        self.callback_check_export_is_ready()
        self.table_chats.blockSignals(False)

    def callback_table_chats_cell_clicked(self, row, column):
        self.callback_table_chats_cell_changed(row, 0, toggle=True)

    def set_select_all_chat(self, state):
        self.table_chats.blockSignals(True)
        for row, id in enumerate(self.chats_array):
            chat = db.get_chats().filter_by(id=id).first()
            chat.selected = state
            item = self.table_chats.item(row, 0)
            item.setCheckState(QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)
            tables.checkbox_decorator(item)
        db.commit()
        self.table_chats.blockSignals(False)

    def callback_btn_select_all_clicked(self):
        print('select all')
        print_time()
        self.set_select_all_chat(True)
        print_time()

    def callback_btn_deselect_all_clicked(self):
        print('select none')
        print_time()
        self.set_select_all_chat(False)
        print_time()


if __name__ == '__main__':
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
