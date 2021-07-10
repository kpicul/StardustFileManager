from PyQt5.QtWidgets import QErrorMessage
import os.path
from os import mkdir
from os.path import exists
from pathlib import Path
from shutil import copy, rmtree, move


"""
Summary:
    Gets the folder or file name from path
Parameters:
    path: Full path of the folder or file
Returns
    name: The name of the item

"""
def get_item_name(path):
    return os.path.split(path)[-1]


'''
Summary:
    returns the path of the parent directory
Parameters:
    path(str): Path of the directory from which we find the parent
Returns:
    parent_path(str): path of the parent directory
'''
def get_parent_directory(path):
    full_path = Path(path)
    return str(full_path.parent.absolute())


'''
Summary:
    converts the string path to the posix path with / separators. Necesary for non POSIX system (ex. Windows)
Parameters:
    path(str): path of the file/directory
Returns:
    posix_path(str): path with posix structure
'''
def get_posix_path(path):
    return str(Path(path).absolute())


'''
Summary:
    Creates new folder with specified name on specified path
Parameters:
    directory_path(str): path to the directory, where we create folder
    folder_name(str): the name of the folder that we are creating
TODO:
    Check if the folder_name parameter is valid
'''
def create_new_folder(directory_path, folder_name):
    new_path = "{}/{}".format(directory_path, folder_name)
    if not exists(new_path):
        try:
            mkdir(new_path)
        except OSError as ose:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("Error: " + ose.strerror)
            error_dialog.exec_()

def copy_item(original_path, copy_path):
    try:
        copy(original_path, copy_path)
    except OSError as ose:
        show_error_message(ose.strerror)

def delete_item(path):
    try:
        rmtree(path)
    except OSError as ose:
        show_error_message(ose.strerror)

def move_item(original_path, new_path):
    try:
        move(original_path, new_path)
    except OSError as ose:
        show_error_message(ose.strerror)

def show_error_message(error_string):
    error_dialog = QErrorMessage()
    error_dialog.showMessage("Error: " + error_string)
    error_dialog.exec_()
