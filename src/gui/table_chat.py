from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools


class TableRowChat(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.selected = True
        self.is_pressed = False


class TableModelChat(QtCore.QAbstractTableModel):
    def __init__(self):
        super(TableModelChat, self).__init__()
        self.headers = ['Zpracovat', 'Jméno', 'Více']
        self.chats = []
        self.index_select = 0
        self.index_name = 1
        self.index_button = 2

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
        flags = (original_flags | QtCore.Qt.ItemIsEnabled) & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)
        if index.column() == self.index_select:
            flags |= QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable
        elif index.column() == self.index_button:
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        col = index.column()
        chat = self.chats[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if col == self.index_select:
                return chat.selected
            elif col == self.index_name:
                return chat.name
            elif col == self.index_button:
                return chat.is_pressed
            return

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
