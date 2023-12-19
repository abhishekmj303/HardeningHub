from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox
from harden import config_file

class AppArmor(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.toml_apparmor = self.config['apparmor']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("AppArmor")
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

        # Enable Checkbox
        self.enable_checkbox = QCheckBox('Enable')
        self.enable_checkbox.stateChanged.connect(self.save_checkbox_state)
        self.container_layout.addWidget(self.enable_checkbox)

        # Mode Dropdown
        hlayout = QHBoxLayout()

        self.mode_label = QLabel('Select mode:')
        self.mode_list = QComboBox()
        self.mode_list.addItems(['enforce', 'complain'])
        self.mode_list.currentTextChanged.connect(self.new_item_selected)

        hlayout.addWidget(self.mode_label)
        hlayout.addWidget(self.mode_list)
        self.container_layout.addLayout(hlayout)
    
    def refresh_config(self, config):
        self.config = config
        self.toml_apparmor = self.config['apparmor']
        self.enable_checkbox.setChecked(self.toml_apparmor['enable'])
        self.mode_list.setCurrentText(self.toml_apparmor['mode'])
        if not self.toml_apparmor['enable']:
            self.mode_list.setEnabled(False)
        
    def save_checkbox_state(self, state):
        self.toml_apparmor['enable'] = (state == 2)
        self.mode_list.setEnabled((state == 2))
        config_file.write(self.config)
    
    def new_item_selected(self, mode):
        self.toml_apparmor['mode'] = mode
        config_file.write(self.config)