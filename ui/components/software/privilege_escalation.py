from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit
from harden import config_file
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator

class PrivilegeEscalation(QWidget):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.toml_privilege_escalation = self.config['privilege_escalation']
        self.privilege_escalation_tooltip = self.tooltip['privilege_escalation']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("Privilege Escalation")
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
        for name, state in self.toml_privilege_escalation.items():
            if name == 'authentication_timeout':
                continue
            checkbox = QCheckBox(name)
            self.checkboxes[name] = checkbox
            checkbox.setToolTip(self.privilege_escalation_tooltip[name])
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(state, name))
            self.container_layout.addWidget(checkbox)

        # Authentication Timeout
        hlayout = QHBoxLayout()
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.configure_label = QLabel('Authentication Timeout (minutes): ')
        self.configure_label.setToolTip(self.privilege_escalation_tooltip['authentication_timeout'])
        self.time_input = QLineEdit()
        validator = QIntValidator()
        self.time_input.setValidator(validator)
        self.time_input.textChanged.connect(self.time_changed)
        self.configure_label.setProperty('class', 'normal-label-for')

        hlayout.addWidget(self.configure_label)
        hlayout.addWidget(self.time_input)
        self.container_layout.addLayout(hlayout)

    def refresh_config(self, config):
        self.config = config
        self.toml_privilege_escalation = self.config['privilege_escalation']
        for name, state in self.toml_privilege_escalation.items():
            if name == 'authentication_timeout':
                continue
            checkbox = self.checkboxes[name]
            checkbox.setChecked(state)
        self.time_input.setText(str(self.toml_privilege_escalation['authentication_timeout']))
        
        
    def save_checkbox_state(self, state, name):
        self.toml_privilege_escalation[name] = (state == 2)
        config_file.write(self.config)

    def time_changed(self, new_size):
        if new_size.startswith('0') and len(new_size) > 1:
            self.time_input.setText(new_size[1:])
        if new_size:
            self.toml_privilege_escalation['authentication_timeout'] = int(new_size)
        else:
            self.time_input.setText('0')
        config_file.write(self.config)