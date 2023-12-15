from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class Welcome(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Welcome to HardeningHub!")

        self.layout.addWidget(self.label)