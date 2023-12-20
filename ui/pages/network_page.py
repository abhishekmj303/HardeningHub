from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ui.components.network.firewall import Firewall
from ui.components.network.network import Net

class Network(QWidget):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Firewall Widget
        self.firewall = Firewall(self.config, self.tooltip)
        self.firewall.setObjectName("firewall")

        # Network Widget
        self.net = Net(self.config, self.tooltip)
        self.net.setObjectName("net")

        self.layout.addWidget(self.firewall)
        self.layout.addWidget(self.net)
    
    def refresh_config(self, config):
        self.config = config
        self.firewall.refresh_config(config)
        self.net.refresh_config(config)