from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from harden import config_file

class Processes(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.toml_processes = self.config['processes']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("Process Hardening")
        self.layout.addWidget(self.main_label)
        self.main_label.setObjectName("component-title")

        # container widget
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_layout)
        self.layout.addWidget(self.container_widget)
        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(30, 30, 30, 30)
        self.container_widget.setObjectName("container-widget")

        self.checkboxes = {}
        for name, state in self.toml_processes.items():
            checkbox = QCheckBox(name.replace('_', ' ').title().replace('Aslr', 'ASLR'))
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(state, name))
            self.container_layout.addWidget(checkbox)
            self.checkboxes[name] = checkbox
    
    def refresh_config(self, config):
        self.config = config
        self.toml_processes = self.config['processes']
        for name, state in self.toml_processes.items():
            self.checkboxes[name].setChecked(state)
        
    def save_checkbox_state(self, state, name):
        self.toml_processes[name] = (state == 2)
        config_file.write(self.config)