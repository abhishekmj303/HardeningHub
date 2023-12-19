from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit
from harden import config_file

class Services(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.toml_services = self.config['services']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("Services")
        self.layout.addWidget(self.main_label)
        self.main_label.setObjectName("component-title")

        # container widget
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_layout)
        self.layout.addWidget(self.container_widget)
        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(30, 10, 30, 30)
        self.container_widget.setObjectName("container-widget")

        self.toml_services_checkboxes = {}
        for name, state in self.toml_services.items():
            checkbox = QCheckBox(f"{name.replace('_',' ').title()}")
            checkbox.stateChanged.connect(lambda state, name = name: self.save_checkbox_state(name, state))
            self.toml_services_checkboxes[name] = checkbox
            self.container_layout.addWidget(checkbox)

    def refresh_config(self, config):
        self.config = config
        self.toml_services = self.config['services']
        for name, state in self.toml_services.items():
            self.toml_services_checkboxes[name].setChecked(state)

    def save_checkbox_state(self, name, state):
        self.toml_services[name] = (state == 2)
        config_file.write(self.config)