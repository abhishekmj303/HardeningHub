from PyQt6.QtWidgets import QListWidget, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal

class Sidebar(QWidget):
    change_page_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.sidebar = QListWidget()

        self.sidebar.insertItem(0, "Hardware")
        self.sidebar.insertItem(1, "Software")
        self.sidebar.insertItem(2, "Networking")

        self.layout.addWidget(self.sidebar)
        self.sidebar.currentRowChanged.connect(self.change_page)
    
    def change_page(self, index):
        self.change_page_signal.emit(index)