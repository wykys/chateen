from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools


class TableRowChat(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.selected = True
        self.messages_count = 0
        self.participants_count = 0
        self.participants = 'Pepíček a Kája'
        self.is_pressed = False


class TableModelChat(QtCore.QAbstractTableModel):
    def __init__(self):
        super(TableModelChat, self).__init__()
        self.headers = ['Zpracovat', 'Počet zpráv', 'Počet účastníků', 'Účastníci', 'Více']
        self.chats = []
        self.index_select = 0
        self.index_mmessages_count = 1
        self.index_participants_count = 2
        self.index_participants = 3
        self.index_button = 4

    def addChat(self, chat):
        self.beginResetModel()
        self.chats.append(chat)
        self.endResetModel()

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.chats)

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self.headers)

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
        col = index.column()
        chat = self.chats[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == self.index_select:
                return chat.selected

            elif col == self.index_mmessages_count:
                return chat.messages_count

            elif col == self.index_participants_count:
                return chat.participants_count

            elif col == self.index_participants:
                return chat.participants

            elif col == self.index_button:
                return chat.is_pressed

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if col == self.index_participants_count or col == self.index_mmessages_count:
                return QtCore.Qt.AlignCenter

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.DisplayRole:
            if index.column() == self.index_select:
                self.chats[index.row()].selected = value
            elif index.column() == self.index_button:
                self.chats[index.row()].is_pressed = value

        if role == QtCore.Qt.EditRole:
            if index.column() == self.index_button:
                id = self.chats[index.row()].id
                print('Click:', id)

        return value

    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if role != QtCore.Qt.ItemDataRole.DisplayRole:
            return

        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        return int(section + 1)
