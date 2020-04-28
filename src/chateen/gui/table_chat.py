from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools
from ..database import db


class TableRowChat(object):
    def __init__(self, chat):
        self.id = chat.id
        self.name = chat.name
        self.selected = chat.selected
        self.messages_count = chat.get_cnt_messages()
        self.participants_count = chat.get_cnt_participants()
        self.participants = str(chat.participants)[1:-1]
        self.is_pressed = False


ROW_BATCH_COUNT = 100


class TableModelChat(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(TableModelChat, self).__init__()
        self.parent = parent
        self.headers = ['Zpracovat', 'Počet zpráv', 'Počet účastníků', 'Účastníci', 'Více']
        self.chats = []
        self.index_select = 0
        self.index_messages_count = 1
        self.index_participants_count = 2
        self.index_participants = 3
        self.index_button = 4
        self.rows_loaded = ROW_BATCH_COUNT

    def endInsertRows(self):
        return

    def update(self):
        self.beginResetModel()
        self.chats = []
        chats = db.get_chats().join(db.Message).group_by(
            db.Chat.id).order_by(db.func.count(db.Message.id).desc()).all()
        for chat in chats:
            self.chats.append(TableRowChat(chat))
        self.endResetModel()
        self.index

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.chats)

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.headers)

    def canFetchMore(self, index=QtCore.QModelIndex()):
        if len(self.chats) > self.rows_loaded:
            return True
        else:
            return False

    def fetchMore(self, index=QtCore.QModelIndex()):
        reminder = len(self.chats) - self.rows_loaded
        items_to_fetch = min(reminder, ROW_BATCH_COUNT)
        self.beginInsertRows(QtCore.QModelIndex(), self.rows_loaded, self.rows_loaded+items_to_fetch-1)
        self.rows_loaded += items_to_fetch
        self.endInsertRows()

    def flags(self, index):
        original_flags = super(TableModelChat, self).flags(index)
        col = index.column()
        flags = (original_flags | QtCore.Qt.ItemIsEnabled) & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)

        if col == self.index_select:
            flags |= QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable
        elif col == self.index_button:
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        row = index.row()
        col = index.column()
        chat = self.chats[row]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == self.index_select:
                return chat.selected

            elif col == self.index_messages_count:
                return chat.messages_count

            elif col == self.index_participants_count:
                return chat.participants_count

            elif col == self.index_participants:
                return chat.participants

            elif col == self.index_button:
                return chat.is_pressed

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if col == self.index_participants_count or col == self.index_messages_count:
                return QtCore.Qt.AlignCenter

        elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
            if self.chats[row].selected:
                return QtGui.QColor('green')
            else:
                return QtGui.QColor('red')

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):

        col = index.column()
        row = index.row()

        if role == QtCore.Qt.DisplayRole:
            if col == self.index_select:
                self.beginResetModel()
                self.chats[row].selected = value
                self.endResetModel()
                id = self.chats[row].id
                chat = db.get_chats().filter(db.Chat.id == id).scalar()
                chat.selected = not chat.selected
                db.commit()
                self.parent.callback_check_export_is_ready()

            elif col == self.index_button:
                self.chats[row].is_pressed = value

        if role == QtCore.Qt.EditRole:
            if col == self.index_button:
                id = self.chats[row].id
                self.parent.callback_click_table_chat_button(id)

        return value

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return

        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)
