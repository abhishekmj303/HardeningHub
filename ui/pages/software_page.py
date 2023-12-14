from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.components.software.processes import Processes
from ui.components.software.apparmor import AppArmor


class Software(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.process_hardening = Processes()
        self.apparmor = AppArmor()

        self.layout.addWidget(self.process_hardening)
        self.layout.addWidget(self.apparmor)