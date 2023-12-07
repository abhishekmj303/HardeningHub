from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class Software(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.hardware_text = QLabel("Software page")
        layout.addWidget(self.hardware_text)