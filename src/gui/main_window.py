from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools

from database import db
from loader import Loader

from .main_window_template import Ui_MainWindow
from .worker import Worker
from . import tables
from .delegate_button import ButtonDelegate
from .delegate_checkbox import CheckBoxDelegate
from .table_chat import TableRowChat, TableModelChat
from .table_participant import TableRowParticipant, TableModelParticipant
from .table_chat_detail import TableRowChatDetail, TableModelChatDetail
from .table_participant_detail import TableRowParticipantDetail, TableModelParticipantDetail

def print_time(msg=''):
    from datetime import datetime
    print(datetime.now().time(), msg)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Chateen')
        self.chats_array = []
        self.statusbar.showMessage('Ahoj, začni otevřením souboru JSON.')
        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.init_table_chats()
        self.init_table_participants()
        self.init_table_chat_detail()
        self.init_table_participant_detail()

    def init_table_chats(self):
        self.model_chats = TableModelChat()
        self.table_chats.setModel(self.model_chats)

        self.deledate_checkbox = CheckBoxDelegate(self.table_chats)
        self.table_chats.setItemDelegateForColumn(0, self.deledate_checkbox)

        self.deledate_button = ButtonDelegate('?', self.table_chats)
        self.table_chats.setItemDelegateForColumn(4, self.deledate_button)

        self.table_chats.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.table_chats.setColumnWidth(4, 40)

    def init_table_participants(self):
        self.model_participants = TableModelParticipant()
        self.table_participants.setModel(self.model_participants)

        self.deledate_button = ButtonDelegate('?', self.table_participants)
        self.table_participants.setItemDelegateForColumn(3, self.deledate_button)

        self.table_participants.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table_participants.setColumnWidth(3, 40)

    def init_table_chat_detail(self):
        self.model_more = TableModelChatDetail()
        self.table_more.setModel(self.model_more)

        self.deledate_button = ButtonDelegate('?', self.table_more)
        self.table_more.setItemDelegateForColumn(3, self.deledate_button)

        self.table_more.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table_more.setColumnWidth(3, 40)

    def init_table_participant_detail(self):
        self.model_more = TableModelParticipantDetail()
        self.table_more.setModel(self.model_more)
        self.table_more.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def update_table(self):
        self.tabwidget.setUpdatesEnabled(False)
        print_time('start update table')
        self.model_chats.update()
        print_time('update table 1')
        self.model_participants.update()
        print_time('update table 2')
        self.model_more.update()
        print_time('update table ok')
        self.tabwidget.setUpdatesEnabled(True)

    def load_new_data(self):
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
        names = [n[0] for n in db.query(db.Participant.name).all()]
        completer = QtWidgets.QCompleter(names)
        self.line_edit_participant.setCompleter(completer)

    def sync_db_chat_selected(self):
        self.table_chats.blockSignals(True)
        for row, id in enumerate(self.chats_array):
            state = bool(self.table_chats.item(row, 0).checkState())
            db.get_chats().filter(db.Chat.id == id).update({db.Chat.selected: state})
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

            if format_is_chat_split:
                with open(path, 'w', encoding='utf-8') as fw:
                    fw.writelines([f'<s>{msg.participant}: {msg.text}</s>\n' for msg in messages])
            else:
                with open(path, 'w', encoding='utf-8') as fw:
                    fw.writelines([f'<s>{msg.text}</s>\n' for msg in messages])

        print_time('Export End')

    def progress(self, percent):
        self.statusbar.showMessage(f'Načítám data: {percent} %')

    def callback_menu_file_open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            filter='JSON (*.json *.JSON)',
            caption='Otevři soubor JSON',
            dir='../data'
        )
        if path != '':
            worker = Worker(Loader, path=path)
            worker.signals.progress.connect(self.progress)
            worker.signals.finished.connect(self.load_new_data)
            self.threadpool.start(worker)

    def callback_menu_tools_reduce(self):
        db.reduce()
        self.load_new_data()

    def callback_menu_tools_clean(self):
        self.chats_array = []
        db.delete_all()
        self.load_new_data()

    def show_html(self, path):
        with open(f'../html/{path}', 'r', encoding='utf-8') as fr:
            html = fr.read()
        self.text_more.setText('')
        self.text_more.insertHtml(html)
        self.table_more.setVisible(False)
        self.text_more.setVisible(True)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def callback_menu_help_help(self):
        self.show_html('help.html')

    def callback_menu_help_about(self):
        self.show_html('about.html')

    def callback_click_table_chat_button(self, chat):
        self.update_table_chat_detail(chat)
        self.table_more.setVisible(True)
        self.text_more.setVisible(False)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def callback_click_table_participant_button(self, participant):
        self.update_table_participant_detail(participant)
        self.table_more.setVisible(True)
        self.text_more.setVisible(False)
        self.tabwidget.setCurrentWidget(self.tab_more)

    def callback_table_chats_cell_clicked(self, row, column):
        self.table_chats.blockSignals(True)
        id = self.chats_array[row]
        item = self.table_chats.item(row, 0)
        state_old = db.query(db.Chat.selected).filter(db.Chat.id == id).scalar()
        state = not bool(item.checkState())
        if state_old == state:
            state = not state
        item.setCheckState(QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)
        tables.checkbox_decorator(item)
        db.get_chats().filter(db.Chat.id == id).update({db.Chat.selected: state})
        db.commit()
        self.callback_check_export_is_ready()
        self.table_chats.blockSignals(False)

    def set_select_all_chat_value(self, state):
        print_time('Update DB')
        self.table_chats.blockSignals(True)
        self.table_chats.setUpdatesEnabled(False)
        db.query(db.Chat).update({db.Chat.selected: state})
        db.commit()
        print_time('Update OK')
        print_time('Update GUI')
        # todo increase power
        for row in range(self.table_chats.rowCount()):
            item = self.table_chats.item(row, 0)
            item.setCheckState(QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)
            tables.checkbox_decorator(item)
        self.table_chats.setUpdatesEnabled(True)
        self.table_chats.blockSignals(False)
        print_time('Update OK')
        self.callback_check_export_is_ready()

    def callback_btn_select_all_clicked(self):
        self.set_select_all_chat_value(True)

    def callback_btn_deselect_all_clicked(self):
        self.set_select_all_chat_value(False)
