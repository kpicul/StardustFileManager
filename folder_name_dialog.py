import sys

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPlainTextEdit
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication


class FolderNameDialog(QDialog):
    def __init__(self):
        super(FolderNameDialog, self).__init__()
        uic.loadUi('forms/folder_name_dialog.ui', self)

        self.pteFolderName = self.findChild(QPlainTextEdit, 'pteFolderName')
        self.btn_box_choice = self.findChild(QDialogButtonBox, 'btnBoxChoice')

        self.set_events()

    def get_folder_name(self):
        return self.pteFolderName.toPlainText()

    def set_events(self):
        self.btn_box_choice.accepted.connect(self.close)
        self.btn_box_choice.rejected.connect(self.close)
