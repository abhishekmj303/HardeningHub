from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class Networking(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.hardware_text = QLabel("Networking page")
        layout.addWidget(self.hardware_text)
    
    def refresh_config(self):
        pass