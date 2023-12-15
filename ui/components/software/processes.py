from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from harden import config_file

class Processes(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.temp_toml_dict = config_file.read()
        self.toml_processes = self.temp_toml_dict['processes']

        self.main_label = QLabel("Process Hardening")
        self.layout.addWidget(self.main_label)

        for name, state in self.toml_processes.items():
            checkbox = QCheckBox(name.replace('_', ' ').title().replace('Aslr', 'ASLR'))
            checkbox.setChecked(state)
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(state, name))
            self.layout.addWidget(checkbox)
        
    def save_checkbox_state(self, state, name):
        self.toml_processes[name] = (state == 2)
        config_file.write(self.temp_toml_dict)