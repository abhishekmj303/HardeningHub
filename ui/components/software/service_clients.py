from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit
from harden import config_file

class ServiceClients(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.toml_service_clients = self.config['service_clients']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)


        self.main_label = QLabel("Service Clients")
        self.layout.addWidget(self.main_label)
        self.main_label.setObjectName("component-title")

        self.toml_service_clients_checkboxes = {}
        for name, state in self.toml_service_clients.items():
            checkbox = QCheckBox(f"{name.replace('_',' ').title()}")
            checkbox.stateChanged.connect(lambda state, name = name: self.save_checkbox_state(name, state))
            self.toml_service_clients_checkboxes[name] = checkbox
            self.layout.addWidget(checkbox)

    def refresh_config(self, config):
        self.config = config
        self.toml_service_clients = self.config['service_clients']
        for name, state in self.toml_service_clients.items():
            self.toml_service_clients_checkboxes[name].setChecked(state)

    def save_checkbox_state(self, name, state):
        self.toml_service_clients[name] = (state == 2)
        config_file.write(self.config)