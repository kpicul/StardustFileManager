import os.path
from pathlib import Path


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

def get_parent_directory(path):
    full_path = Path(path)
    return str(full_path.parent.absolute())
