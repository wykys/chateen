from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools
from ..database import db


class TableRowParticipant(object):
    def __init__(self, participant):
        self.id = participant.id
        self.name = participant.name
        self.messages_count = participant.get_cnt_messages()
        self.chats_count = participant.get_cnt_chats()
        self.is_pressed = False


ROW_BATCH_COUNT = 100


class TableModelParticipant(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(TableModelParticipant, self).__init__()
        self.parent = parent
        self.headers = ['Jméno', 'Počet zpráv', 'Počet chatů', 'Více']
        self.participants = []
        self.index_name = 0
        self.index_messages_count = 1
        self.index_chats_count = 2
        self.index_button = 3
        self.rows_loaded = ROW_BATCH_COUNT

    def endInsertRows(self):
        return

    def update(self):
        self.beginResetModel()
        self.participants = []
        participants = db.get_participants().join(
            db.Message).group_by(db.Participant.id).order_by(db.func.count(db.Message.id).desc())
        for participant in participants:
            self.participants.append(TableRowParticipant(participant))
        self.endResetModel()

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.participants)

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.headers)

    def canFetchMore(self, index=QtCore.QModelIndex()):
        if len(self.participants) > self.rows_loaded:
            return True
        else:
            return False

    def fetchMore(self, index=QtCore.QModelIndex()):
        reminder = len(self.participants) - self.rows_loaded
        items_to_fetch = min(reminder, ROW_BATCH_COUNT)
        self.beginInsertRows(QtCore.QModelIndex(), self.rows_loaded, self.rows_loaded+items_to_fetch-1)
        self.rows_loaded += items_to_fetch
        self.endInsertRows()

    def flags(self, index):
        original_flags = super(TableModelParticipant, self).flags(index)
        col = index.column()
        flags = (original_flags | QtCore.Qt.ItemIsEnabled) & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)

        if col == self.index_button:
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        col = index.column()
        participant = self.participants[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == self.index_name:
                return participant.name

            elif col == self.index_messages_count:
                return participant.messages_count

            elif col == self.index_chats_count:
                return participant.chats_count

            elif col == self.index_button:
                return participant.is_pressed

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if col == self.index_chats_count or col == self.index_messages_count:
                return QtCore.Qt.AlignCenter

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        col = index.column()
        row = index.row()

        if role == QtCore.Qt.DisplayRole:
            if col == self.index_button:
                self.participants[row].is_pressed = value

        if role == QtCore.Qt.EditRole:
            if col == self.index_button:
                id = self.participants[row].id
                self.parent.callback_click_table_participant_button(id)

        return value

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return

        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)
