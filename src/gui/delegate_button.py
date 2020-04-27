from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools


class ButtonDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, text='', parent=None):
        super(ButtonDelegate, self).__init__(parent)
        self.text = text

    def createEditor(self, parent, option, index):
        return None

    def paint(self, painter, option, index):
        opts = QtWidgets.QStyleOptionButton()

        opts.state |= QtWidgets.QStyle.State_Active
        opts.state |= QtWidgets.QStyle.State_Enabled

        is_pressed = index.data(QtCore.Qt.DisplayRole)
        opts.state |= (QtWidgets.QStyle.State_Sunken if is_pressed else QtWidgets.QStyle.State_Raised)

        opts.text = self.text
        opts.rect = option.rect

        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_PushButton, opts, painter)

    def editorEvent(self, event, model, option, index):
        if event.button() == QtCore.Qt.LeftButton:
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if option.rect.contains(event.pos()):
                    model.setData(index, True, QtCore.Qt.DisplayRole)
                    return True
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                model.setData(index, False, QtCore.Qt.DisplayRole)
                if option.rect.contains(event.pos()):
                    # Model should handle button click action in its setData() method.
                    model.setData(index, self.text, QtCore.Qt.EditRole)
                    return True
        return False
