from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QWidget, QVBoxLayout


class FileBrowserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tree_view = QTreeView()
        self.setGeometry(10, 10, 640, 480)
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.tree_view)

    def set_path(self, file_path):
        file_system_model = QFileSystemModel(self)
        file_system_model.setReadOnly(False)
        root = file_system_model.setRootPath(file_path)
        self.tree_view.setModel(file_system_model)
        self.tree_view.setRootIndex(root)
