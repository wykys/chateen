#!/usr/bin/env python3

import sys
from tr import tr
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog, QFileDialog)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.button = QPushButton('Load JSON')
        self.edit = QLineEdit('Zadej své jméno')

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.load_json)

    # Greets the user
    def load_json(self):
        print("Hello %s" % self.edit.text())
        file_name = QFileDialog.getOpenFileName(self, filter='JSON (*.json *.JSON)', caption='Open JSON', dir='../data')
        print(file_name)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)




    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
