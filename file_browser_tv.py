import os

from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QMenu, QAction, QHeaderView
from os.path import isdir, exists
from os import makedirs
from stack import Stack
from file_system_functions import get_parent_directory, create_new_folder, delete_item, show_error_message
from PyQt5.QtCore import Qt
from folder_name_dialog import FolderNameDialog

'''
Summary:
    Represents the file browser part of the main window
'''


class FileBrowserTv(QTreeView):
    # region Init
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.item_header = self.header()
        self.item_header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.dir_path = ""
        self.doubleClicked.connect(self.on_folder_click)
        self.clicked.connect(self.on_select)
        self.model = QFileSystemModel(self)
        self.history = Stack()
        self.future = Stack()
        self.selected_item = None

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)
    # endregion
    # region ClassFunctions
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
            Checks if it has any paths in history.
        Returns:
            has_history (bool): If it has any paths in history list
        '''

    def has_history(self):
        return len(self.history) > 0

    '''
    Summary:
        Checks if it has any paths in future list
    Returns:
        has_future (bool): If it has any paths in future list
    '''

    def has_future(self):
        return len(self.future) > 0

    def get_selected_items_paths(self):
        selected_indexes = self.selectionModel().selectedIndexes()
        items = []
        for index in selected_indexes:
            items.append(self.model.fileInfo(index).absoluteFilePath())
        return items

    # endregion
    # region Events
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

    def on_select(self, index):
        click_path = self.model.fileInfo(index).absoluteFilePath()
        if isdir(click_path):
            self.selected_item = click_path
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

    '''
    Summary:
        If we ever previously pressed back button then when we press forward it returns to the previous path
    '''
    def return_to_future(self):
        if len(self.future) > 0:
            old_path = self.future.pop()
            self.history.push(self.dir_path)
            self.dir_path = old_path
            self.setRootIndex(self.model.setRootPath(old_path))

    '''
    Summary:
        Moves the path to the parent directory and loads the contents
    '''
    def get_up(self):
        parent_dir = get_parent_directory(self.dir_path)
        self.history.push(self.dir_path)
        self.dir_path = parent_dir
        self.setRootIndex(self.model.setRootPath(parent_dir))

    '''
    Summary:
        Sets and fires the right click context menu
    Parameters:
        Position: position of the window
    '''
    def contextMenuEvent(self, position):
        menu = QMenu()
        action_new_folder = menu.addAction("New Folder")
        action_quit = menu.addAction("Quit")

        action_new_folder.triggered.connect(self.create_new_folder_event)
        menu.exec_(self.viewport().mapToGlobal(position))

    '''
    Summary:
        Event that creates new window. Fires the FolderName dialog
    '''
    def create_new_folder_event(self):
        name_dialog = FolderNameDialog()
        name_dialog.exec_()
        folder_name = name_dialog.get_folder_name()
        if folder_name is not None:
            create_new_folder(self.dir_path, folder_name)

    def delete_items(self):
        selected_indexes = self.selectionModel().selectedIndexes()
        for index in selected_indexes:
            self.model.remove(index)

    # endregion
