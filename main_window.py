from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QPlainTextEdit, QApplication, QTreeView, \
    QFileSystemModel, QPushButton, QVBoxLayout
from PyQt5 import uic
from file_browser_tv import FileBrowserTv
from string_functions import get_item_name
from stack import Stack
from os.path import isdir
import sys
import os

'''
Summary:
    Represents the main window
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('forms/main_window.ui', self)

        home_folder = os.path.expanduser('~')

        self.path_index = dict()
        self.main_tab_widget = self.findChild(QTabWidget, 'mainTabWidget')
        self.first_tab = self.findChild(QWidget, 'firstTab')
        self.pt_file_path = self.findChild(QPlainTextEdit, 'filePath')
        self.file_browser_tv = self.findChild(FileBrowserTv, 'fileBrowserTv')
        self.btn_new_tab = self.findChild(QPushButton, 'btnNewTab')
        self.btn_back = self.findChild(QPushButton, 'btnBack')
        self.btn_forward = self.findChild(QPushButton, 'btnForward')

        self.btn_forward.setEnabled(False)
        self.btn_back.setEnabled(False)
        self.file_browser_tv.set_path(home_folder)
        self.pt_file_path.setPlainText(self.file_browser_tv.dir_path)
        index = self.main_tab_widget.indexOf(self.first_tab)
        self.main_tab_widget.setTabText(index, get_item_name(home_folder))

        self.set_events()

        self.show()

    '''
    Summary:
        Sets the events to the appropriate elements
    '''
    def set_events(self):
        self.file_browser_tv.doubleClicked.connect(self.on_file_browser_click)
        self.btn_new_tab.clicked.connect(self.add_new_tab)
        self.main_tab_widget.currentChanged.connect(self.on_tab_change)
        self.btn_back.clicked.connect(self.return_back)

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
            if isdir(current_path):
                self.btn_back.setEnabled(True)
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

    '''
    Summary:
        Event that executes on tab change
    '''
    def on_tab_change(self):
        current_fb = self.get_current_file_browser()
        self.pt_file_path.setPlainText(current_fb.dir_path)

    '''
    Summary:
        Event that executes when we press button to go back.
        It reverts toi the previous folder in history. If there
        is no previous folder it disables back button
    '''
    def return_back(self):
        current_fb = self.get_current_file_browser()
        current_fb.return_back()
        if len(current_fb.history) > 0:
            self.pt_file_path.setPlainText(current_fb.dir_path)
        else:
            self.btn_back.setEnabled(False)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
