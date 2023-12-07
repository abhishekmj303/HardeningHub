from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class Hardware(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.hardware_text = QLabel("Hardware page")
        layout.addWidget(self.hardware_text)