from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, text):
        super().__init__(text)
        self.setFixedHeight(45)

    def mousePressEvent(self, event):
        self.clicked.emit()

class Sidebar(QWidget):
    change_page_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.bg = "#E6C7A9"
        self.active = "#382F27"
        self.index = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        self.hardware_label = ClickableLabel("Hardware")
        self.hardware_label.clicked.connect(lambda: self.set_active(1))
        self.layout.addWidget(self.hardware_label)

        self.software_label = ClickableLabel("Software")
        self.software_label.clicked.connect(lambda: self.set_active(2))
        self.layout.addWidget(self.software_label)

        self.networking_label = ClickableLabel("Network")
        self.networking_label.clicked.connect(lambda: self.set_active(3))
        self.layout.addWidget(self.networking_label)
    
    def set_active(self, index):
        self.index = index
        self.change_page_signal.emit(index)
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().setStyleSheet("")
        print(f'bg: {self.bg}, active: {self.active}')
        self.layout.itemAt(index - 1).widget().setStyleSheet(f"background-color: {self.bg}; border-left: 4px solid {self.active};")