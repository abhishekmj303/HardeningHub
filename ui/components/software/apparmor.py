from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox
from harden import config_file

class AppArmor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.temp_toml_dict = config_file.read()
        self.toml_apparmor = self.temp_toml_dict['apparmor']

        self.main_label = QLabel("AppArmor")
        self.layout.addWidget(self.main_label)
        self.main_label.setObjectName("component-title")

        # Enable Checkbox
        checkbox = QCheckBox('Enable')
        checkbox.setChecked(self.toml_apparmor['enable'])
        checkbox.stateChanged.connect(self.save_checkbox_state)
        self.layout.addWidget(checkbox)

        # Mode Dropdown
        hlayout = QHBoxLayout()

        self.mode_label = QLabel('Select mode:')
        self.mode_list = QComboBox()
        self.mode_list.addItems(['enforce', 'complain'])
        self.mode_list.setCurrentText(self.toml_apparmor['mode'])
        self.mode_list.currentTextChanged.connect(self.new_item_selected)

        hlayout.addWidget(self.mode_label)
        hlayout.addWidget(self.mode_list)
        self.layout.addLayout(hlayout)
        
    def save_checkbox_state(self, state):
        self.toml_apparmor['enable'] = (state == 2)
        self.mode_list.setEnabled((state == 2))
        config_file.write(self.temp_toml_dict)
    
    def new_item_selected(self, mode):
        self.toml_apparmor['mode'] = mode
        config_file.write(self.temp_toml_dict)