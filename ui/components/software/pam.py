from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit
from harden import config_file
from PyQt6.QtGui import QIntValidator

class PAM(QWidget):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.toml_pam = self.config['pam']
        self.pam_tooltip = self.tooltip['pam']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("PAM")
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

        # Enable Password Checkbox
        self.enable_password_checkbox = QCheckBox('Enable Password Level')
        self.enable_password_checkbox.setToolTip(self.pam_tooltip['enable_password_level'])
        self.enable_password_checkbox.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'enable_password_level'))
        self.container_layout.addWidget(self.enable_password_checkbox)

        # Enable Password Dropdown
        hlayout = QHBoxLayout()

        # Select Mode Label
        self.mode_label = QLabel('Required Password Level:')
        self.mode_label.setToolTip(self.pam_tooltip['enable_password_level'])
        self.mode_label.setProperty('class', 'normal-label-for')

        # Mode Dropdown
        self.mode_list = QComboBox()
        self.mode_list.addItems(['weak', 'medium', 'strong', 'stronger'])
        self.mode_list.currentTextChanged.connect(lambda text: self.new_item_selected(text, 'required_password_level'))

        hlayout.addWidget(self.mode_label)
        hlayout.addWidget(self.mode_list)
        self.container_layout.addLayout(hlayout)

        # Enable Password Length Checkbox
        self.enable_password_len_checkbox = QCheckBox('Enable Password Length')
        self.enable_password_len_checkbox.setToolTip(self.pam_tooltip['enable_password_length'])
        self.enable_password_len_checkbox.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'enable_password_length'))
        self.container_layout.addWidget(self.enable_password_len_checkbox)

        # Enable Password Dropdown
        hlayout = QHBoxLayout()

        self.len_label = QLabel('Minimum Password Length: ')
        self.len_label.setToolTip(self.pam_tooltip['enable_password_length'])
        self.len_label.setProperty('class', 'normal-label-for')

        self.size_input = QLineEdit()
        validator = QIntValidator()
        self.size_input.setValidator(validator)
        self.size_input.textChanged.connect(lambda text: self.size_changed(text, 'minimum_password_length', self.size_input))

        hlayout.addWidget(self.len_label)
        hlayout.addWidget(self.size_input)
        self.container_layout.addLayout(hlayout)

        # Enable Password Length Checkbox
        self.limit_password_reuse_checkbox = QCheckBox('Enable Limit Password Reuse')
        self.limit_password_reuse_checkbox.setToolTip(self.pam_tooltip['limit_password_reuse'])
        self.limit_password_reuse_checkbox.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'limit_password_reuse'))
        self.container_layout.addWidget(self.limit_password_reuse_checkbox)

        # Enable Password Dropdown
        hlayout = QHBoxLayout()

        self.reuse_label = QLabel('Minimum Password Length: ')
        self.reuse_label.setToolTip(self.pam_tooltip['limit_password_reuse'])
        self.reuse_label.setProperty('class', 'normal-label-for')

        self.size_input_2 = QLineEdit()
        validator = QIntValidator()
        self.size_input_2.setValidator(validator)
        self.size_input_2.textChanged.connect(lambda text: self.size_changed(text, 'password_reuse_limit', self.size_input_2))

        hlayout.addWidget(self.reuse_label)
        hlayout.addWidget(self.size_input_2)
        self.container_layout.addLayout(hlayout)

        # Configure Hashing Algorithm
        self.configure_hashing_algorithm = QCheckBox('Configure Hashing Algorithm')
        self.configure_hashing_algorithm.setToolTip(self.pam_tooltip['configure_hashing_algorithm'])
        self.configure_hashing_algorithm.stateChanged.connect(lambda state: self.save_checkbox_state(state, 'configure_hashing_algorithm'))
        self.container_layout.addWidget(self.configure_hashing_algorithm)
    
    def refresh_config(self, config):
        self.config = config
        self.toml_pam = self.config['pam']
        self.enable_password_checkbox.setChecked(self.toml_pam['enable_password_level'])
        self.enable_password_len_checkbox.setChecked(self.toml_pam['enable_password_length'])
        self.limit_password_reuse_checkbox.setChecked(self.toml_pam['limit_password_reuse'])
        self.configure_hashing_algorithm.setChecked(self.toml_pam['configure_hashing_algorithm'])
        self.mode_list.setCurrentText(self.toml_pam['required_password_level'])
        self.size_input.setText(str(self.toml_pam['minimum_password_length']))
        self.size_input_2.setText(str(self.toml_pam['password_reuse_limit']))
        
    def save_checkbox_state(self, state, key):
        self.toml_pam[key] = (state == 2)
        if state == 0:
            if key == 'enable_password_level':
                self.mode_list.setEnabled(False)
            elif key == 'enable_password_length':
                self.size_input.setEnabled(False)
            elif key == 'limit_password_reuse':
                self.size_input_2.setEnabled(False)
        else:
            if key == 'enable_password_level':
                self.mode_list.setEnabled(True)
            elif key == 'enable_password_length':
                self.size_input.setEnabled(True)
            elif key == 'limit_password_reuse':
                self.size_input_2.setEnabled(True)
        config_file.write(self.config)
    
    def new_item_selected(self, text, key):
        self.toml_pam[key] = text
        config_file.write(self.config)
    
    def size_changed(self, new_size, key, input):
        if new_size.startswith('0') and len(new_size) > 1:
            input.setText(new_size[1:])
        if new_size:
            self.toml_pam[key] = int(new_size)
        else:
            input.setText('0')
        config_file.write(self.config)