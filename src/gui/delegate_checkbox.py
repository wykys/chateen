from PySide2 import QtWidgets, QtGui, QtCore, QtUiTools


class CheckBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CheckBoxDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        return None

    def paint(self, painter, option, index):
        checked = index.data(QtCore.Qt.DisplayRole)
        opts = QtWidgets.QStyleOptionButton()
        opts.rect = self.getCheckBoxRect(option)
        if index.flags() & QtCore.Qt.ItemIsEditable:
            opts.state |= QtWidgets.QStyle.State_Enabled
        else:
            opts.state |= QtWidgets.QStyle.State_ReadOnly
        if checked:
            opts.state |= QtWidgets.QStyle.State_On
        else:
            opts.state |= QtWidgets.QStyle.State_Off
        QtWidgets.QApplication.style().drawControl(
            QtWidgets.QStyle.CE_CheckBox, opts, painter
        )

    def getCheckBoxRect(self, option):
        opts = QtWidgets.QStyleOptionButton()
        rect = QtWidgets.QApplication.style().subElementRect(QtWidgets.QStyle.SE_CheckBoxIndicator, opts, None)
        x = option.rect.x()
        y = option.rect.y()
        w = option.rect.width()
        h = option.rect.height()
        checkBoxTopLeftCorner = QtCore.QPoint(x + w / 2 - rect.width() / 2, y + h / 2 - rect.height() / 2)
        return QtCore.QRect(checkBoxTopLeftCorner, rect.size())

    def editorEvent(self, event, model, option, index):
        if not (index.flags() & QtCore.Qt.ItemIsEditable):
            return False
        if event.button() == QtCore.Qt.LeftButton:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if self.getCheckBoxRect(option).contains(event.pos()):
                    self.setModelData(None, model, index)
                    return True
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if self.getCheckBoxRect(option).contains(event.pos()):
                    return True
        return False

    def setModelData(self, editor, model, index):
        model.setData(index, False if index.data() else True, QtCore.Qt.DisplayRole)
