from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from os.path import isdir

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
            self.dir_path = click_path
            self.setRootIndex(self.model.setRootPath(click_path))
