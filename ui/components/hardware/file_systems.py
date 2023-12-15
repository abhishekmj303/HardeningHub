from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QLineEdit
from PyQt6.QtGui import QIntValidator
from harden import config_file

class FileSystems(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.temp_toml_dict = config_file.read()
        self.toml_file_systems = self.temp_toml_dict['file-systems']

        self.main_label = QLabel("File Systems")
        self.layout.addWidget(self.main_label)

        # Basic Hardening
        self.label_basic = QLabel("# Basic Hardening")
        self.layout.addWidget(self.label_basic)

        # block items
        for name, state in self.toml_file_systems['block'].items():
            checkbox = QCheckBox(f'Block {name}')
            checkbox.setChecked(state)
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(state, 'block', name))
            self.layout.addWidget(checkbox)

        # Intermediate Hardening
        self.label_basic = QLabel("# Intermediate Hardening")
        self.layout.addWidget(self.label_basic)
        
        # configure_fs items
        for name, state in self.toml_file_systems['configure_fs'].items():
            checkbox = QCheckBox(f"Configure /{name.replace('_', '/')}")
            checkbox.setChecked(state)
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(state, 'configure_fs', name))
            self.layout.addWidget(checkbox)
        
        # configure /tmp size
        hlayout = QHBoxLayout()

        self.configure_label = QLabel('Configure /tmp size (in GB):')
        self.size_input = QLineEdit()
        self.size_input.setText(str(self.toml_file_systems['tmp_size']))
        validator = QIntValidator()
        self.size_input.setValidator(validator)
        self.size_input.textChanged.connect(self.size_changed)

        hlayout.addWidget(self.configure_label)
        hlayout.addWidget(self.size_input)
        self.layout.addLayout(hlayout)

        # disable_automount
        self.disable_auto_mount = QCheckBox('Disable Auto-Mount')
        self.disable_auto_mount.setChecked(self.toml_file_systems['disable_automount'])
        self.disable_auto_mount.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'disable_automount', None))
        self.layout.addWidget(self.disable_auto_mount)

        # Advanced Hardening
        self.label_basic = QLabel("# Advanced Hardening")
        self.layout.addWidget(self.label_basic)

        self.enable_aide = QCheckBox('Enable AIDE (Advanced Intrusion Detection Environment)')
        self.enable_aide.setChecked(self.toml_file_systems['enable_aide'])
        self.enable_aide.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'enable_aide', None))
        self.layout.addWidget(self.enable_aide)
        
    def save_checkbox_state(self, state, type, name):
        if name:
            self.toml_file_systems[type][name] = (state == 2)
        else:
            self.toml_file_systems[type] = (state == 2)
        config_file.write(self.temp_toml_dict)
    
    def size_changed(self, new_size):
        if new_size:
            self.toml_file_systems['tmp_size'] = int(new_size)
        else:
            self.size_input.setText('0')
        config_file.write(self.temp_toml_dict)