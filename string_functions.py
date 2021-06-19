import os.path


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
