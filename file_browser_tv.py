from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from os.path import isdir
from stack import Stack

'''
Summary:
    Represents the file browser part of the main window
'''


class FileBrowserTv(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dir_path = ""
        self.doubleClicked.connect(self.on_folder_click)
        self.model = QFileSystemModel(self)
        self.history = Stack()
        self.future = Stack()
    '''
    Summary:
        sets the path of the file browser
    Parameters:
        file_path(string): the file path of the file that is entered
    '''
    def set_path(self, file_path):
        self.dir_path = file_path
        file_system_model = QFileSystemModel(self)
        file_system_model.setReadOnly(False)
        self.model = file_system_model
        root = file_system_model.setRootPath(file_path)
        self.setModel(file_system_model)
        self.setRootIndex(root)

    '''
    Summary:
        It executes, when clicking on folder or file. If it is folder it enters the folders, else it executes
        the file with the default app
    Parameters:
        index(int): The index of the clicked item
    '''
    def on_folder_click(self, index):
        click_path = self.model.fileInfo(index).absoluteFilePath()
        if isdir(click_path):
            self.future = Stack()
            self.history.push(self.dir_path)
            self.dir_path = click_path
            self.setRootIndex(self.model.setRootPath(click_path))

    '''
    Summary:
        If it has history it reverts back to previous path
    '''
    def return_back(self):
        if len(self.history) > 0:
            old_path = self.history.pop()
            self.future.push(self.dir_path)
            self.dir_path = old_path
            self.setRootIndex(self.model.setRootPath(old_path))

    def return_to_future(self):
        if len(self.future) > 0:
            old_path = self.future.pop()
            self.history.push(self.dir_path)
            self.dir_path = old_path
            self.setRootIndex(self.model.setRootPath(old_path))

    def has_history(self):
        return len(self.history) > 0

    def has_future(self):
        return len(self.future) > 0
