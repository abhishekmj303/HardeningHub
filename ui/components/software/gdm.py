from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit
from PyQt6.QtGui import QIntValidator
from harden import config_file

class GDM(QWidget):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.toml_gdm = self.config['gdm']
        self.gdm_tooltip = self.tooltip['gdm']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)


        self.main_label = QLabel("GDM")
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

        self.toml_gdm_checkboxes = {}
        self.remove_checkbox = QCheckBox('Remove')
        self.remove_checkbox.setToolTip(self.gdm_tooltip['remove'])
        self.remove_checkbox.stateChanged.connect(lambda state, name = 'remove': self.save_checkbox_state(name, state))
        self.toml_gdm_checkboxes['remove'] = self.remove_checkbox
        self.container_layout.addWidget(self.remove_checkbox)

        hlayout = QHBoxLayout()

        # Lock on Idle Label
        self.lockon_lable = QCheckBox('Enable Lock on Idle (seconds): ')
        self.lockon_lable.setToolTip(self.gdm_tooltip['enable_lock_on_idle'])
        self.lockon_lable.stateChanged.connect(self.enable_lock_on_idle_changed)

        self.time_input = QLineEdit()
        self.time_input.setText(str(self.toml_gdm['lock_on_idle']))
        validator = QIntValidator()
        self.time_input.setValidator(validator)
        self.time_input.textChanged.connect(self.time_changed)

        hlayout.addWidget(self.lockon_lable)
        hlayout.addWidget(self.time_input)

        self.container_layout.addLayout(hlayout)
        for name in self.toml_gdm:
            if name == 'lock_on_idle' or name == 'remove':
                continue
            state = self.toml_gdm[name]
            checkbox = QCheckBox(f"{name.replace('_',' ').title()}")
            checkbox.setToolTip(self.gdm_tooltip[name])
            checkbox.stateChanged.connect(lambda state, name = name: self.save_checkbox_state(name, state))
            self.toml_gdm_checkboxes[name] = checkbox
            self.container_layout.addWidget(checkbox)

    def refresh_config(self, config):
        self.config = config
        self.toml_gdm = self.config['gdm']
        self.lockon_lable.setChecked(self.toml_gdm['enable_lock_on_idle'])
        for name, state in self.toml_gdm.items():
            if name == 'lock_on_idle':
                continue
            self.toml_gdm_checkboxes[name].setChecked(state)
        if self.toml_gdm['remove']:
            self.lockon_lable.setEnabled(False)
            self.time_input.setEnabled(False)
            for name, checkbox in self.toml_gdm_checkboxes.items():
                if name == 'remove':
                    continue
                checkbox.setEnabled(False)

    def save_checkbox_state(self, name, state):
        self.toml_gdm[name] = (state == 2)
        if name == 'remove':
            # setEnable(state == 2) for all other checkboxes
            for name, checkbox in self.toml_gdm_checkboxes.items():
                if name == 'remove':
                    continue
                checkbox.setEnabled(state == 0)
            self.lockon_lable.setEnabled(state == 0)
            self.time_input.setEnabled(state == 0)

        config_file.write(self.config)

    def time_changed(self, new_size):
        if new_size:
            self.toml_gdm['lock_on_idle'] = int(new_size)
        else:
            self.time_input.setText('0')
        config_file.write(self.config)
    
    def enable_lock_on_idle_changed(self, state):
        self.toml_gdm['enable_lock_on_idle'] = (state == 2)
        if state == 2:
            self.time_input.setEnabled(True)
        else:
            self.time_input.setEnabled(False)
        config_file.write(self.config)