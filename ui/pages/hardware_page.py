from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from ui.components.hardware.physical_ports import PhysicalPorts
from ui.components.hardware.file_systems import FileSystems
from PyQt6.QtCore import Qt

class Hardware(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.physical_ports = PhysicalPorts(self.config)
        self.file_systems = FileSystems(self.config)

        self.layout.addWidget(self.physical_ports)
        self.layout.addWidget(self.file_systems)

        # self.scroll = QScrollArea()
        # self.scroll.setWidgetResizable(True)
        # self.scroll.setWidget(self)
        # self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)