from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.components.hardware.physical_ports import PhysicalPorts
from ui.components.hardware.file_systems import FileSystems

class Hardware(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.physical_ports = PhysicalPorts()
        self.file_systems = FileSystems()

        self.layout.addWidget(self.physical_ports)
        self.layout.addWidget(self.file_systems)