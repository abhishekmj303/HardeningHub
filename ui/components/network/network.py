from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from harden import config_file

class Net(QWidget):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.toml_net = self.config['network']
        self.net_tooltip = self.tooltip['network']
        self.init_ui()
        self.refresh_config(config)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("Network")
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

        self.toml_net_checkboxes = {}
        for name, state in self.toml_net.items():
            if name == "disable_protocols":
                continue
            checkbox = QCheckBox(f"{name.replace('_',' ').title()}")
            checkbox.setToolTip(self.net_tooltip[name])
            checkbox.stateChanged.connect(lambda state, name = name: self.save_checkbox_state(name, state))
            self.toml_net_checkboxes[name] = checkbox
            self.container_layout.addWidget(checkbox)

        self.protocols_label = QLabel("Disable Protocols")
        self.container_layout.addWidget(self.protocols_label)
        self.protocols_label.setObjectName("sub-component-title")

        self.protocols_checkboxes = {}
        for name, state in self.toml_net['disable_protocols'].items():
            checkbox = QCheckBox(f"{name.replace('_',' ').title()}")
            checkbox.setToolTip(self.net_tooltip['disable_protocols'][name])
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state_protocols(state, 'disable_protocols', name))
            checkbox.setProperty('class', 'in-checkbox')
            self.container_layout.addWidget(checkbox)
            self.protocols_checkboxes[name] = checkbox

    def refresh_config(self, config):
        self.config = config
        self.toml_net = self.config['network']
        for name, state in self.toml_net.items():
            if name == "disable_protocols":
                continue
            self.toml_net_checkboxes[name].setChecked(state)

        for name, state in self.toml_net['disable_protocols'].items():
            self.protocols_checkboxes[name].setChecked(state)

    def save_checkbox_state(self, name, state):
        self.toml_net[name] = (state == 2)
        config_file.write(self.config)

    def save_checkbox_state_protocols(self, state, category, name):
        self.toml_net[category][name] = (state == 2)
        config_file.write(self.config)
