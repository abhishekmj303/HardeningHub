from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ui.components.software.processes import Processes
from ui.components.software.apparmor import AppArmor
from ui.components.software.gdm import GDM
from ui.components.software.time_sync import TimeSync
from ui.components.software.services import Services
from ui.components.software.service_clients import ServiceClients
from ui.components.software.privilege_escalation import PrivilegeEscalation
from PyQt6.QtCore import Qt


class Software(QWidget):
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

        # Processes Widget
        self.process_hardening = Processes(self.config, self.tooltip)
        self.process_hardening.setObjectName("process_hardening")

        # AppArmor Widget
        self.apparmor = AppArmor(self.config, self.tooltip)
        self.apparmor.setObjectName("apparmor")

        # GDM Widget
        self.gdm = GDM(self.config, self.tooltip)
        self.gdm.setObjectName("gdm")

        # Time Sync Widget
        self.time_sync =TimeSync(self.config, self.tooltip)
        self.time_sync.setObjectName("time_sync")

        # Services Widget
        self.services = Services(self.config, self.tooltip)
        self.services.setObjectName("services")

        # Service Clients Widget
        self.service_clients = ServiceClients(self.config, self.tooltip)
        self.service_clients.setObjectName("service_clients")

        # Privilege Escalation Widget
        self.privilege_escalation = PrivilegeEscalation(self.config, self.tooltip)
        self.privilege_escalation.setObjectName("privilege_escalation")

        self.layout.addWidget(self.process_hardening)
        self.layout.addWidget(self.apparmor)
        self.layout.addWidget(self.gdm)
        self.layout.addWidget(self.time_sync)
        self.layout.addWidget(self.services)
        self.layout.addWidget(self.service_clients)
        self.layout.addWidget(self.privilege_escalation)
    
    def refresh_config(self, config):
        self.config = config
        self.process_hardening.refresh_config(config)
        self.apparmor.refresh_config(config)
        self.gdm.refresh_config(config)
        self.time_sync.refresh_config(config)
        self.services.refresh_config(config)
        self.service_clients.refresh_config(config)
        self.privilege_escalation.refresh_config(config)