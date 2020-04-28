from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools
from database import db


class TableRowParticipantDetail(object):
    def __init__(self, message):
        self.id = message.id
        self.datetime = message.datetime.strftime('%H:%M:%S %Y/%m/%d')
        self.participant = message.participant.name
        self.text = message.text


ROW_BATCH_COUNT = 100


class TableModelParticipantDetail(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(TableModelParticipantDetail, self).__init__()
        self.parent = parent
        self.headers = ['Datum', 'Odesilatel', 'Text']
        self.messages = []
        self.index_datetime = 0
        self.index_participant = 1
        self.index_text = 2
        self.rows_loaded = ROW_BATCH_COUNT

    def endInsertRows(self):
        return

    def update(self, participant_id=None):
        self.beginResetModel()
        self.messages = []
        if not participant_id is None:
            messages = db.get_messages().filter(db.Message.participant_id == participant_id).order_by(db.Message.datetime)
            for message in messages:
                self.messages.append(TableRowParticipantDetail(message))
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
        original_flags = super(TableModelParticipantDetail, self).flags(index)
        flags = (original_flags | QtCore.Qt.ItemIsEnabled) & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)

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

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if col == self.index_datetime or col == self.index_participant:
                return QtCore.Qt.AlignCenter

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        return value

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return

        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)
