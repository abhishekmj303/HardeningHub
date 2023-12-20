from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from harden import config_file

class TimeSync(QWidget):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.toml_time_sync = self.config['time-sync']
        self.time_sync_tooltip = self.tooltip['time-sync']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main_label = QLabel("Time Synchronization")
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

        #enable ntp checkbox
        self.enable_ntp = QCheckBox('Enable NTP')
        self.enable_ntp.setToolTip(self.time_sync_tooltip['enable_ntp'])
        self.enable_ntp.stateChanged.connect(lambda state, name = 'enable_ntp': self.save_checkbox_state(name, state))
        self.container_layout.addWidget(self.enable_ntp)

        self.enable_user = QCheckBox('Enable NTP user')
        self.enable_user.setToolTip(self.time_sync_tooltip['enable_ntp_user'])
        self.enable_user.stateChanged.connect(lambda state, name = 'enable_ntp_user': self.save_checkbox_state(name, state))
        self.container_layout.addWidget(self.enable_user)

        self.ntp_server_checkbox = QCheckBox('Enable NTP Servers')
        self.ntp_server_checkbox.setToolTip(self.time_sync_tooltip['enable_ntp_servers'])
        self.ntp_server_checkbox.stateChanged.connect(self.enable_ntp_servers_changed)
        self.container_layout.addWidget(self.ntp_server_checkbox)

        hlayout = QHBoxLayout()

        self.new_server = QLineEdit()
        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_new_server)
        self.add_button.setProperty('class', 'add-btn')

        hlayout.addWidget(self.new_server)
        hlayout.addWidget(self.add_button)

        self.container_layout.addLayout(hlayout)
    
        self.server_table()

    def server_table(self):
        self.servers_table = QTableWidget()
        self.servers_table.setColumnCount(2)
        self.container_layout.addWidget(self.servers_table)

        for i in range(2):
            self.servers_table.setColumnWidth(i, 200)
        
        self.servers_table.setFixedWidth(420)

        self.servers_table.setHorizontalHeaderLabels(["Server", "Remove"])

        
    def add_new_server(self):
        server = self.new_server.text()
        rows = self.toml_time_sync['ntp_servers']
        if server == '' or server is None or server in rows:
            return
        self.toml_time_sync['ntp_servers'].append(server)
        config_file.write(self.config)
        self.servers_table.insertRow(self.servers_table.rowCount())
        self.servers_table.setItem(self.servers_table.rowCount() - 1, 0, QTableWidgetItem(server))
        remove_button = QPushButton('Remove')
        remove_button.setProperty('class', 'remove-btn')
        remove_button.clicked.connect(lambda state,n = server : self.remove_server(n))

        self.servers_table.setCellWidget(self.servers_table.rowCount() - 1, 1, remove_button)
        self.new_server.setText('')
        self.servers_table.setFixedHeight((len(rows) + 1) * 37)

    def add_servers(self):
        rows = self.toml_time_sync['ntp_servers']
        for i in range(len(rows)):
            self.servers_table.insertRow(i)
            name = rows[i]
            self.servers_table.setItem(i, 0, QTableWidgetItem(rows[i]))
            
            remove_button = QPushButton('Remove')
            remove_button.setProperty('class', 'remove-btn')
            remove_button.clicked.connect(lambda state,n = name : self.remove_server(n))
            self.servers_table.setCellWidget(i, 1, remove_button)
        self.servers_table.setFixedHeight(len(rows) * 39)

            
    def remove_server(self, name):
        rows = self.toml_time_sync['ntp_servers']
        self.toml_time_sync['ntp_servers'].remove(name)
        config_file.write(self.config)
        for i in range(self.servers_table.rowCount()):
            if self.servers_table.item(i, 0).text() == name:
                self.servers_table.removeRow(i)
                break
        self.servers_table.setFixedHeight((len(rows) + 1) * 37)


    def refresh_config(self, config):
        self.config = config
        self.toml_time_sync = self.config['time-sync']
        self.enable_ntp.setChecked(self.toml_time_sync['enable_ntp'])
        self.enable_user.setChecked(self.toml_time_sync['enable_ntp_user'])
        self.ntp_server_checkbox.setChecked(self.toml_time_sync['enable_ntp_servers'])
        if not self.toml_time_sync['enable_ntp']:
            self.enable_user.setEnabled(False)
            self.servers_table.setEnabled(False)
            self.new_server.setEnabled(False)
            self.add_button.setEnabled(False)
            for i in range(self.servers_table.rowCount()):
                self.servers_table.cellWidget(i, 1).setEnabled(False)

        self.servers_table.setRowCount(0)
        self.add_servers()


    def save_checkbox_state(self, name, state):
        self.toml_time_sync[name] = (state == 2)
        if name == 'enable_ntp':
            self.enable_user.setEnabled(state == 2)
            self.servers_table.setEnabled(state == 2)
            self.new_server.setEnabled(state == 2)
            self.add_button.setEnabled(state == 2)
            for i in range(self.servers_table.rowCount()):
                self.servers_table.cellWidget(i, 1).setEnabled(state == 2)
        config_file.write(self.config)
    
    def enable_ntp_servers_changed(self, state):
        self.toml_time_sync['enable_ntp_servers'] = (state == 2)
        if state == 2:
            self.new_server.setEnabled(True)
            self.add_button.setEnabled(True)
            for i in range(self.servers_table.rowCount()):
                self.servers_table.cellWidget(i, 1).setEnabled(True)
        else:
            self.new_server.setEnabled(False)
            self.add_button.setEnabled(False)
            for i in range(self.servers_table.rowCount()):
                self.servers_table.cellWidget(i, 1).setEnabled(False)
        config_file.write(self.config)