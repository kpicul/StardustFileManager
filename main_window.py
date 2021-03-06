from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QPlainTextEdit, QApplication, QTreeView, \
    QFileSystemModel, QPushButton, QVBoxLayout, QAction
from PyQt5 import uic
from file_browser_tv import FileBrowserTv
from folder_name_dialog import FolderNameDialog
from file_system_functions import get_item_name, get_posix_path, copy_item, move_item
from stack import Stack
from os.path import isdir
from enum import Enum
import sys
import os

class Mode(Enum):
    COPY = 1,
    MOVE = 2

'''
Summary:
    Represents the main window
'''


class MainWindow(QMainWindow):
    # region Init
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('forms/main_window.ui', self)

        home_folder = get_posix_path(os.path.expanduser('~'))

        self.path_index = dict()
        self.main_tab_widget = self.findChild(QTabWidget, 'mainTabWidget')
        self.first_tab = self.findChild(QWidget, 'firstTab')
        self.pt_file_path = self.findChild(QPlainTextEdit, 'filePath')
        self.file_browser_tv = self.findChild(FileBrowserTv, 'fileBrowserTv')
        self.btn_new_tab = self.findChild(QPushButton, 'btnNewTab')
        self.btn_back = self.findChild(QPushButton, 'btnBack')
        self.btn_forward = self.findChild(QPushButton, 'btnForward')
        self.btn_up = self.findChild(QPushButton, 'btnUp')

        self.action_exit = self.findChild(QAction, 'actionExit')
        self.action_new_tab = self.findChild(QAction, 'actionNew_Tab')
        self.action_new_folder = self.findChild(QAction, 'actionNew_Folder')
        self.action_delete = self.findChild(QAction, 'actionDelete')
        self.action_copy = self.findChild(QAction, 'actionCopy')
        self.action_paste = self.findChild(QAction, 'actionPaste')

        self.clipboard_mode = None
        self.copy_clipboard = []

        self.btn_forward.setEnabled(False)
        self.btn_back.setEnabled(False)
        self.file_browser_tv.set_path(home_folder)
        self.pt_file_path.setPlainText(self.file_browser_tv.dir_path)
        index = self.main_tab_widget.indexOf(self.first_tab)
        self.main_tab_widget.setTabText(index, get_item_name(home_folder))
        self.main_tab_widget.setTabsClosable(True)
        self.setWindowTitle(self.file_browser_tv.dir_path)

        self.set_events()

        self.show()
    # endregion

    '''
    Summary:
        Sets the events to the appropriate elements
    '''

    # region ClassFunctions
    def set_events(self):
        self.file_browser_tv.doubleClicked.connect(self.on_file_browser_click)
        self.btn_new_tab.clicked.connect(self.add_new_tab)
        self.main_tab_widget.currentChanged.connect(self.on_tab_change)
        self.main_tab_widget.tabCloseRequested.connect(self.close_tab_event)
        self.btn_back.clicked.connect(self.return_back)
        self.btn_forward.clicked.connect(self.return_to_future)
        self.btn_up.clicked.connect(self.get_up)

        self.action_exit.triggered.connect(self.quit)
        self.action_new_tab.triggered.connect(self.add_new_tab)
        self.action_new_folder.triggered.connect(self.new_folder_event)
        self.action_delete.triggered.connect(self.delete_event)
        self.action_copy.triggered.connect(self.copy_file_event)
        self.action_paste.triggered.connect(self.paste_event)

    '''
    Summary:
        Gets the file browser instance on currently selected tab
    Returns:
        current_fb: The instance of fileBrowser on currently selected tab
    '''
    def get_current_file_browser(self):
        current_tab = self.main_tab_widget.currentWidget()
        layout = current_tab.layout()
        current_fb = layout.itemAt(0).widget()
        return current_fb
    # endregion
    # region Events
    '''
    Summary:
        Executes when clicking on an folder in main window. Sets the path in the path view
    '''
    def on_file_browser_click(self):
        current_tab = self.main_tab_widget.currentWidget()
        index = self.main_tab_widget.currentIndex()
        layout = current_tab.layout()
        current_fb = layout.itemAt(0).widget()
        if isinstance(current_fb, FileBrowserTv):
            current_path = current_fb.dir_path
            self.path_index[current_tab] = current_path
            self.pt_file_path.setPlainText(current_path)
            self.main_tab_widget.setTabText(int(index), get_item_name(current_path))
            self.setWindowTitle(current_fb.dir_path)
            if isdir(current_path):
                self.btn_back.setEnabled(True)
                self.btn_forward.setEnabled(False)
            if len(current_fb.history) == 0:
                self.btn_back.setEnabled(False)
    '''
    Summary:
        Adds new tab and sets the path to the home folder of the user
    '''
    def add_new_tab(self):
        default_path = os.path.expanduser('~')
        tab = QWidget()
        new_layout = QVBoxLayout()
        new_file_browser = FileBrowserTv()
        new_file_browser.doubleClicked.connect(self.on_file_browser_click)
        new_file_browser.set_path(default_path)
        new_layout.addWidget(new_file_browser)
        tab.setLayout(new_layout)
        tab_name = get_item_name(default_path)
        self.path_index[tab_name] = default_path
        self.main_tab_widget.addTab(tab, tab_name)
        self.main_tab_widget.setCurrentWidget(tab)
        self.setWindowTitle(new_file_browser.dir_path)

    '''
    Summary:
        Event that executes on tab change
    '''
    def on_tab_change(self):
        if self.main_tab_widget.count() > 0:
            current_fb = self.get_current_file_browser()
            self.pt_file_path.setPlainText(current_fb.dir_path)
            self.setWindowTitle(current_fb.dir_path)
            if current_fb.has_history():
                self.btn_back.setEnabled(True)
            else:
                self.btn_back.setEnabled(False)
            if current_fb.has_future():
                self.btn_forward.setEnabled(True)
            else:
                self.btn_forward.setEnabled(False)

    '''
    Summary:
        Event that executes when we press button to go back.
        It reverts toi the previous folder in history. If there
        is no previous folder it disables back button
    '''
    def return_back(self):
        current_fb = self.get_current_file_browser()
        current_fb.return_back()
        if current_fb.has_history():
            self.pt_file_path.setPlainText(current_fb.dir_path)
        else:
            self.btn_back.setEnabled(False)
        self.btn_forward.setEnabled(True)

    '''
    Summary:
        Event that executes when we press forward button
    '''
    def return_to_future(self):
        current_fb = self.get_current_file_browser()
        current_fb.return_to_future()
        if current_fb.has_future():
            self.pt_file_path.setPlainText(current_fb.dir_path)
        else:
            self.btn_forward.setEnabled(False)
        self.btn_back.setEnabled(True)

    '''
    Summary:
        Event that executes when we press "Up" button
    '''
    def get_up(self):
        current_fb = self.get_current_file_browser()
        current_fb.get_up()
        self.pt_file_path.setPlainText(current_fb.dir_path)
        self.setWindowTitle(current_fb.dir_path)

    '''
    Summary:
        Event that executes when we press new folder action
    '''
    def new_folder_event(self):
        current_fb = self.get_current_file_browser()
        current_fb.create_new_folder_event()

    def close_tab_event(self, index):
        active_tab = self.main_tab_widget.widget(index)
        active_tab.deleteLater()
        self.main_tab_widget.removeTab(index)
        if self.main_tab_widget.count() == 0:
            self.quit()

    def delete_event(self):
        current_file_browser = self.get_current_file_browser()
        current_file_browser.delete_items()

    def copy_file_event(self):
        current_file_browser = self.get_current_file_browser()
        self.copy_clipboard = current_file_browser.get_selected_items_paths()
        self.clipboard_mode = Mode.COPY

    def move_event(self):
        current_file_browser = self.get_current_file_browser()
        self.copy_clipboard = current_file_browser.get_selected_items_paths()
        self.clipboard_mode = Mode.MOVE

    def paste_event(self):
        if self.clipboard_mode is not None and len(self.copy_clipboard) > 0:
            current_file_browser = self.get_current_file_browser()
            current_directory_path = current_file_browser.dir_path
            for clipboard_item_path in self.copy_clipboard:
                if self.clipboard_mode == Mode.COPY:
                    copy_item(clipboard_item_path, current_directory_path)
                elif self.clipboard_mode == Mode.MOVE:
                    move_item(clipboard_item_path, current_directory_path)
            if self.clipboard_mode == Mode.MOVE:
                self.clipboard_mode = None
                self.copy_clipboard = []


    def quit(self):
        sys.exit(0)

    # endregion


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
