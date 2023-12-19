from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit
from PyQt6.QtGui import QIntValidator
from harden import config_file

class GDM(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
        self.refresh_config()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.toml_gdm = self.config['gdm']

        self.main_label = QLabel("GDM")
        self.layout.addWidget(self.main_label)
        self.main_label.setObjectName("component-title")

        # remove Checkbox
        # checkbox = QCheckBox('Remove')
        # checkbox.stateChanged.connect(self.save_checkbox_state)
        # self.layout.addWidget(checkbox)

        # # disable user list checkbox
        # checkbox = QCheckBox('Disable user list')
        # checkbox.setChecked(self.toml_gdm['disable_user_list'])
        # checkbox.stateChanged.connect(self.save_checkbox_state)
        # self.layout.addWidget(checkbox)
        # lockonidle Qlineedit

        hlayout = QHBoxLayout()

        self.lockon_lable = QLabel('Lock on Idle')
        self.time_input = QLineEdit()
        self.time_input.setText(str(self.toml_gdm['lock_on_idle']))
        validator = QIntValidator()
        self.time_input.setValidator(validator)
        self.time_input.textChanged.connect(self.time_changed)

        hlayout.addWidget(self.lockon_lable)
        hlayout.addWidget(self.time_input)

        self.layout.addLayout(hlayout)
        self.toml_gdm_checkboxes = {}
        for name in self.toml_gdm:
            if name == 'lock_on_idle':
                continue
            state = self.toml_gdm[name]
            checkbox = QCheckBox(f"{name.replace('_',' ')}")
            checkbox.stateChanged.connect(lambda state, name = name: self.save_checkbox_state(name, state))
            self.toml_gdm_checkboxes[name] = checkbox
            self.layout.addWidget(checkbox)

    def refresh_config(self):
        for name, state in self.toml_gdm.items():
            if name == 'lock_on_idle':
                continue
            self.toml_gdm_checkboxes[name].setChecked(state)

    def save_checkbox_state(self, name, state):
        self.toml_gdm[name] = (state == 2)
        config_file.write(self.config)

    def time_changed(self, new_size):
        if new_size:
            self.toml_gdm['lock_on_idle'] = int(new_size)
        else:
            self.time_input.setText('0')
        config_file.write(self.config)