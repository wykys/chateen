from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools


def create_table_button(self, callback, arg):
    layout = QtWidgets.QHBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)
    button = QtWidgets.QPushButton(self)
    button.setText('?')
    button.clicked.connect(lambda y=0, x=arg: callback(x))
    layout.addWidget(button)

    item = QtWidgets.QWidget()
    item.setLayout(layout)
    return item


def insert_row(self, row, items, offset=0):
    self.insertRow(self.rowCount())
    for cell, item in enumerate(items):
        self.setItem(row, cell+offset, item)


def init(self, columns):
    self.setColumnCount(columns)
    self.clearContents()
    self.setRowCount(0)
    self.setSortingEnabled(True)


def set_columns_width(self, columns):
    width_btn_more = 20

    if columns == 5:
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.setColumnWidth(4, width_btn_more)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
    elif columns == 4:
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.setColumnWidth(3, width_btn_more)
    elif columns == 3:
        self.setColumnWidth(0, 100)
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)


def checkbox_decorator(item):
    if bool(item.checkState()):
        item.setText('Ano')
        item.setTextColor(QtGui.QColor(0, 150, 0))
    else:
        item.setText('Ne')
        item.setTextColor(QtGui.QColor(200, 0, 0))


def update_table_chats(self, chats):

    self.chats_array = []

    init(self.table_chats, 5)

    self.table_chats.setHorizontalHeaderLabels(
        ['Zpracovat', 'Počet zpráv', 'Počet účastníků', 'Účastníci', 'Více']
    )

    for r, chat in enumerate(chats):

        self.chats_array.append(chat.id)

        item1 = QtWidgets.QTableWidgetItem()
        item1.setText('Ne')
        item1.setFlags(item1.flags() | QtCore.Qt.ItemIsUserCheckable)
        item1.setCheckState(QtCore.Qt.Unchecked)
        item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        item1.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)
        checkbox_decorator(item1)

        item2 = QtWidgets.QTableWidgetItem(str(chat.get_cnt_messages()))
        item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        item2.setFlags(item2.flags() & ~QtCore.Qt.ItemIsEditable)

        item3 = QtWidgets.QTableWidgetItem(str(chat.get_cnt_participants()))
        item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        item3.setFlags(item2.flags() & ~QtCore.Qt.ItemIsEditable)

        item4 = QtWidgets.QTableWidgetItem(str(chat.participants)[1:-1])
        item4.setFlags(item2.flags() & ~QtCore.Qt.ItemIsEditable)

        insert_row(self.table_chats, r, [item1, item2, item3, item4])

        item5 = create_table_button(self.table_chats, self.callback_click_table_chat_button, chat)
        self.table_chats.setCellWidget(r, 4, item5)

    set_columns_width(self.table_chats, 5)


def update_table_participants(self, participants):

    init(self.table_participants, 4)

    self.table_participants.setHorizontalHeaderLabels(
        ['Jméno', 'Počet zpráv', 'Počet chatů', 'Více']
    )

    for r, participant in enumerate(participants):

        item1 = QtWidgets.QTableWidgetItem(str(participant.name))
        item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        item1.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

        item2 = QtWidgets.QTableWidgetItem(str(participant.get_cnt_messages()))
        item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        item2.setFlags(item2.flags() & ~QtCore.Qt.ItemIsEditable)

        item3 = QtWidgets.QTableWidgetItem(str(participant.get_cnt_chats()))
        item3.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        item3.setFlags(item3.flags() & ~QtCore.Qt.ItemIsEditable)

        insert_row(self.table_participants, r, [item1, item2, item3])

        item4 = create_table_button(self.table_participants, self.callback_click_table_participant_button, participant)
        self.table_participants.setCellWidget(r, 3, item4)

    set_columns_width(self.table_participants, 4)


def update_table_chat_detail(self, chat):

    init(self.table_more, 4)

    self.table_more.setHorizontalHeaderLabels(
        ['Datum', 'Odesilatel', 'Text', 'Více']
    )

    for r, message in enumerate(chat.messages):

        item1 = QtWidgets.QTableWidgetItem(message.datetime.strftime('%H:%M:%S    %Y/%m/%d'))
        item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        item1.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

        item2 = QtWidgets.QTableWidgetItem(str(message.participant))
        item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        item2.setFlags(item2.flags() & ~QtCore.Qt.ItemIsEditable)

        item3 = QtWidgets.QTableWidgetItem(str(message.text))
        item3.setFlags(item3.flags() & ~QtCore.Qt.ItemIsEditable)

        insert_row(self.table_more, r, [item1, item2, item3])

        item4 = create_table_button(self.table_participants,
                                    self.callback_click_table_participant_button, message.participant)
        self.table_more.setCellWidget(r, 3, item4)

    set_columns_width(self.table_more, 4)


def update_table_participant_detail(self, participant) -> bool:

    init(self.table_more, 3)

    self.table_more.setHorizontalHeaderLabels(
        ['Datum', 'Odesilatel', 'Text']
    )

    for r, message in enumerate(participant.messages):

        item1 = QtWidgets.QTableWidgetItem(message.datetime.strftime('%H:%M:%S    %Y/%m/%d'))
        item1.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        item1.setFlags(item1.flags() & ~QtCore.Qt.ItemIsEditable)

        item2 = QtWidgets.QTableWidgetItem(str(message.participant))
        item2.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        item2.setFlags(item2.flags() & ~QtCore.Qt.ItemIsEditable)

        item3 = QtWidgets.QTableWidgetItem(str(message.text))
        item3.setFlags(item3.flags() & ~QtCore.Qt.ItemIsEditable)

        insert_row(self.table_more, r, [item1, item2, item3])

    set_columns_width(self.table_more, 3)
