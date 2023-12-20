from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem\
    , QComboBox
from PyQt6.QtGui import QIntValidator
from harden import config_file

class SSH(QWidget):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.toml_ssh = self.config['ssh']
        self.ssh_tooltip = self.tooltip['ssh']
        self.init_ui()
        self.refresh_config(config)

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("SSH")
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

        self.configure_permissions_label = QLabel("Configure Permissions")
        self.container_layout.addWidget(self.configure_permissions_label)
        self.configure_permissions_label.setObjectName("sub-component-title")

        self.configure_permissions_checkboxes = {}
        for name, state in self.toml_ssh['configure_permissions'].items():
            checkbox = QCheckBox(f"{name.replace('_',' ').title()}")
            checkbox.setToolTip(self.ssh_tooltip['configure_permissions'][name])
            checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state_configure(state, 'configure_permissions', name))
            checkbox.setProperty('class', 'in-checkbox')
            self.container_layout.addWidget(checkbox)
            self.configure_permissions_checkboxes[name] = checkbox

        self.allow_users_label = QLabel("Allow Users")
        self.container_layout.addWidget(self.allow_users_label)
        self.allow_users_label.setObjectName("sub-component-title")

        hlayout = QHBoxLayout()
        self.container_layout.addLayout(hlayout)

        self.new_user = QLineEdit()
        self.add_user_button = QPushButton('Add')
        self.add_user_button.clicked.connect(self.add_new_user)
        self.add_user_button.setProperty('class', 'add-btn')

        hlayout.addWidget(self.new_user)
        hlayout.addWidget(self.add_user_button)

        self.user_table()

        self.allow_groups_label = QLabel("Allow Groups")
        self.container_layout.addWidget(self.allow_groups_label)
        self.allow_groups_label.setObjectName("sub-component-title")

        hlayout = QHBoxLayout()

        self.new_group = QLineEdit()
        self.add_group_button = QPushButton('Add')
        self.add_group_button.clicked.connect(self.add_new_group)
        self.add_group_button.setProperty('class', 'add-btn')

        hlayout.addWidget(self.new_group)
        hlayout.addWidget(self.add_group_button)

        self.container_layout.addLayout(hlayout)


        self.group_table()

        hlayout = QHBoxLayout()

        self.log_level_label = QLabel('Log Level:')
        self.log_level_label.setToolTip(self.ssh_tooltip['log_level'])
        self.log_level_label.setProperty('class', 'normal-label-for')

        self.log_level_list = QComboBox()
        self.log_level_list.addItems(['VERBOSE', 'INFO'])
        self.log_level_list.currentTextChanged.connect(self.new_item_selected)

        hlayout.addWidget(self.log_level_label)
        hlayout.addWidget(self.log_level_list)
        self.container_layout.addLayout(hlayout)

        self.ssh_checkboxes = {}
        self.ssh_inputs = {}
        i = 0
        for name, state in self.toml_ssh.items():
            if i < 4:
                i += 1
                continue
            elif i <= 17 and name != 'max_auth_tries':
                checkbox = QCheckBox(f"{name.replace('_',' ').title()}")
                checkbox.setToolTip(self.ssh_tooltip[name])
                checkbox.stateChanged.connect(lambda state, name=name: self.save_checkbox_state(name, state))
                self.ssh_checkboxes[name] = checkbox
                self.container_layout.addWidget(checkbox)
            elif i > 17 or name == 'max_auth_tries':
                hlayout = QHBoxLayout()
                label = QLabel(f"{name.replace('_',' ').title()}")
                label.setToolTip(self.ssh_tooltip[name])
                label.setProperty('class', 'normal-label-for')
                input = QLineEdit()
                input.setText(str(state))
                validator = QIntValidator()
                input.setValidator(validator)
                input.textChanged.connect(lambda text, name=name: self.save_text_input(name, text))
                hlayout.addWidget(label)
                hlayout.addWidget(input)
                self.container_layout.addLayout(hlayout)
                self.ssh_inputs[name] = input
            i += 1

    def user_table(self):
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(2)
        self.container_layout.addWidget(self.users_table)

        for i in range(2):
            self.users_table.setColumnWidth(i, 200)

        self.users_table.setFixedWidth(420)

        self.users_table.setHorizontalHeaderLabels(["User", "Remove"])

    def add_new_user(self):
        user = self.new_user.text()
        rows = self.toml_ssh['allow_users']
        if user == '' or user is None or user in rows:
            return
        self.toml_ssh['allow_users'].append(user)
        config_file.write(self.config)
        self.users_table.insertRow(self.users_table.rowCount())
        self.users_table.setItem(self.users_table.rowCount() - 1, 0, QTableWidgetItem(user))
        remove_button = QPushButton('Remove')
        remove_button.setProperty('class', 'remove-btn')
        remove_button.clicked.connect(lambda state, n=user: self.remove_user(n))

        self.users_table.setCellWidget(self.users_table.rowCount() - 1, 1, remove_button)
        self.new_user.setText('')

    def add_users(self):
        for user in self.toml_ssh['allow_users']:
            self.users_table.insertRow(self.users_table.rowCount())
            self.users_table.setItem(self.users_table.rowCount() - 1, 0, QTableWidgetItem(user))
            remove_button = QPushButton('Remove')
            remove_button.setProperty('class', 'remove-btn')
            remove_button.clicked.connect(lambda state, n=user: self.remove_user(n))

            self.users_table.setCellWidget(self.users_table.rowCount() - 1, 1, remove_button)

    def remove_user(self, user):
        rows = self.toml_ssh['allow_users']
        self.toml_ssh['allow_users'].remove(user)
        config_file.write(self.config)
        for i in range(self.users_table.rowCount()):
            if self.users_table.item(i, 0).text() == user:
                self.users_table.removeRow(i)
                break

    def group_table(self):
        self.groups_table = QTableWidget()
        self.groups_table.setColumnCount(2)
        self.container_layout.addWidget(self.groups_table)

        for i in range(2):
            self.groups_table.setColumnWidth(i, 200)

        self.groups_table.setFixedWidth(420)

        self.groups_table.setHorizontalHeaderLabels(["Group", "Remove"])

    def add_new_group(self):
        group = self.new_group.text()
        rows = self.toml_ssh['allow_groups']
        if group == '' or group is None or group in rows:
            return
        self.toml_ssh['allow_groups'].append(group)
        config_file.write(self.config)
        self.groups_table.insertRow(self.groups_table.rowCount())
        self.groups_table.setItem(self.groups_table.rowCount() - 1, 0, QTableWidgetItem(group))
        remove_button = QPushButton('Remove')
        remove_button.setProperty('class', 'remove-btn')
        remove_button.clicked.connect(lambda state, n=group: self.remove_group(n))

        self.groups_table.setCellWidget(self.groups_table.rowCount() - 1, 1, remove_button)
        self.new_group.setText('')

    def add_groups(self):
        for group in self.toml_ssh['allow_groups']:
            self.groups_table.insertRow(self.groups_table.rowCount())
            self.groups_table.setItem(self.groups_table.rowCount() - 1, 0, QTableWidgetItem(group))
            remove_button = QPushButton('Remove')
            remove_button.setProperty('class', 'remove-btn')
            remove_button.clicked.connect(lambda state, n=group: self.remove_group(n))

            self.groups_table.setCellWidget(self.groups_table.rowCount() - 1, 1, remove_button)

    def remove_group(self, group):
        rows = self.toml_ssh['allow_groups']
        self.toml_ssh['allow_groups'].remove(group)
        config_file.write(self.config)
        for i in range(self.groups_table.rowCount()):
            if self.groups_table.item(i, 0).text() == group:
                self.groups_table.removeRow(i)
                break
    def new_item_selected(self, text):
        self.toml_ssh['log_level'] = text
        config_file.write(self.config)

    def save_checkbox_state(self, name, state):
        self.toml_ssh[name] = (state == 2)
        config_file.write(self.config)

    def save_checkbox_state_configure(self, state, category, name):
        self.toml_ssh[category][name] = (state == 2)
        config_file.write(self.config)

    def save_text_input(self, name, text):
        if text:
            self.toml_ssh[name] = int(text)
        else:
            self.toml_ssh[name] = 0
        config_file.write(self.config)

    def refresh_config(self, config):
        self.config = config
        self.toml_ssh = self.config['ssh']
        for name, state in self.toml_ssh['configure_permissions'].items():
            self.configure_permissions_checkboxes[name].setChecked(state)
        i = 0
        for name, state in self.toml_ssh.items():
            if i < 4:
                i += 1
                continue
            elif i <= 17 and name != 'max_auth_tries':
                self.ssh_checkboxes[name].setChecked(state)
            elif i > 17 or name == 'max_auth_tries':
                self.ssh_inputs[name].setText(str(state))
            i += 1

        self.users_table.setRowCount(0)
        self.groups_table.setRowCount(0)

        self.add_users()
        self.add_groups()
            
        

        



