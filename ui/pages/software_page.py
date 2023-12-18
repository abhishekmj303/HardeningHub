from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.components.software.processes import Processes
from ui.components.software.apparmor import AppArmor
from PyQt6.QtCore import Qt


class Software(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.process_hardening = Processes(self.config)
        self.apparmor = AppArmor(self.config)

        self.layout.addWidget(self.process_hardening)
        self.layout.addWidget(self.apparmor)
    
    def refresh_config(self, config):
        self.config = config
        self.process_hardening.refresh_config(config)
        self.apparmor.refresh_config(config)