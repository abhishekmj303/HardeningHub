from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QLineEdit
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
from harden import config_file

class FileSystems(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.toml_file_systems = self.config['file-systems']

        self.main_label = QLabel("File Systems")
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
        self.container_widget.setProperty("class", "file-systems")

        # Basic Hardening
        self.label_basic = QLabel("Basic Hardening")
        self.container_layout.addWidget(self.label_basic)
        self.label_basic.setObjectName("sub-component-title")

        # block items
        for name, state in self.toml_file_systems['block'].items():
            checkbox = QCheckBox(f'Block {name}')
            checkbox.setChecked(state)
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(state, 'block', name))
            self.container_layout.addWidget(checkbox)

        # Intermediate Hardening
        self.label_intermediate = QLabel("Intermediate Hardening")
        self.container_layout.addWidget(self.label_intermediate)
        self.label_intermediate.setObjectName("sub-component-title")
        
        # configure_fs items
        for name, state in self.toml_file_systems['configure_fs'].items():
            checkbox = QCheckBox(f"Configure /{name.replace('_', '/')}")
            checkbox.setChecked(state)
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(state, 'configure_fs', name))
            self.container_layout.addWidget(checkbox)
        
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
        self.container_layout.addLayout(hlayout)

        # disable_automount
        self.disable_auto_mount = QCheckBox('Disable Auto-Mount')
        self.disable_auto_mount.setChecked(self.toml_file_systems['disable_automount'])
        self.disable_auto_mount.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'disable_automount', None))
        self.container_layout.addWidget(self.disable_auto_mount)

        # Advanced Hardening
        self.label_advanced = QLabel("Advanced Hardening")
        self.container_layout.addWidget(self.label_advanced)
        self.label_advanced.setObjectName("sub-component-title")


        self.enable_aide = QCheckBox('Enable AIDE (Advanced Intrusion Detection Environment)')
        self.enable_aide.setChecked(self.toml_file_systems['enable_aide'])
        self.enable_aide.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'enable_aide', None))
        self.container_layout.addWidget(self.enable_aide)
        
    def save_checkbox_state(self, state, type, name):
        if name:
            self.toml_file_systems[type][name] = (state == 2)
        else:
            self.toml_file_systems[type] = (state == 2)
        config_file.write(self.config)
    
    def size_changed(self, new_size):
        if new_size:
            self.toml_file_systems['tmp_size'] = int(new_size)
        else:
            self.size_input.setText('0')
        config_file.write(self.config)