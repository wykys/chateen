from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools
from database import db


class TableRowChatDetail(object):
    def __init__(self, message):
        self.id = message.id
        self.datetime = message.datetime.strftime('%H:%M:%S - %Y/%m/%d')
        self.participant = message.participant
        self.text = message.text
        self.is_pressed = False


ROW_BATCH_COUNT = 100


class TableModelChatDetail(QtCore.QAbstractTableModel):

    def __init__(self):
        super(TableModelChatDetail, self).__init__()
        self.headers = ['Datum', 'Odesilatel', 'Text', 'Více']
        self.messages = []
        self.index_datetime = 0
        self.index_participant = 1
        self.index_text = 2
        self.index_button = 3
        self.rows_loaded = ROW_BATCH_COUNT

    def update(self, chat_id=None):
        self.beginResetModel()
        self.messages = []
        if not chat_id is None:
            for message in db.get_chats().filter(db.Chat.id == chat_id).first().messages:
                self.messages.append(TableRowChatDetail(message))
        self.endResetModel()

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.messages)

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.headers)

    def canFetchMore(self, index=QtCore.QModelIndex()):
        if len(self.messages) > self.rows_loaded:
            return True
        else:
            return False

    def fetchMore(self, index=QtCore.QModelIndex()):
        reminder = len(self.messages) - self.rows_loaded
        items_to_fetch = min(reminder, ROW_BATCH_COUNT)
        self.beginInsertRows(QtCore.QModelIndex(), self.rows_loaded, self.rows_loaded+items_to_fetch-1)
        self.rows_loaded += items_to_fetch
        self.endInsertRows()

    def flags(self, index):
        original_flags = super(TableModelChatDetail, self).flags(index)
        col = index.column()
        flags = (original_flags | QtCore.Qt.ItemIsEnabled) & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)

        if col == self.index_button:
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        col = index.column()
        message = self.messages[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == self.index_datetime:
                return message.datetime

            elif col == self.index_participant:
                return message.participant

            elif col == self.index_text:
                return message.text

            elif col == self.index_button:
                return message.is_pressed

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if col == self.index_datetime or col == self.index_participant:
                return QtCore.Qt.AlignCenter

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.DisplayRole:
            if index.column() == self.index_button:
                self.messages[index.row()].is_pressed = value

        if role == QtCore.Qt.EditRole:
            if index.column() == self.index_button:
                id = self.messages[index.row()].id
                print('Click:', id)

        return value

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return

        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)
