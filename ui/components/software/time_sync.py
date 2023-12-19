from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QIntValidator
from harden import config_file

class TimeSync(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.toml_time_sync = self.config['time-sync']
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

        #enable ntp checkbox
        self.enable_ntp = QCheckBox('Enable NTP')
        self.enable_ntp.stateChanged.connect(lambda state, name = 'enable_ntp': self.save_checkbox_state(name, state))
        self.layout.addWidget(self.enable_ntp)

        

        self.enable_user = QCheckBox('Enable NTP user')
        self.enable_user.stateChanged.connect(lambda state, name = 'enable_ntp_user': self.save_checkbox_state(name, state))
        self.layout.addWidget(self.enable_user)

        ntp_server_lable = QLabel('NTP Servers')
        self.layout.addWidget(ntp_server_lable)

        hlayout = QHBoxLayout()

        self.new_server = QLineEdit()
        self.add_button = QPushButton('add')
        self.add_button.clicked.connect(self.add_new_server)

        hlayout.addWidget(self.new_server)
        hlayout.addWidget(self.add_button)

        self.layout.addLayout(hlayout)
    
        self.server_table()

    def server_table(self):
        self.servers_table = QTableWidget()
        self.servers_table.setColumnCount(2)
        self.layout.addWidget(self.servers_table)

        self.servers_table.setHorizontalHeaderLabels(["Server", "Remove"])

        
    def add_new_server(self):
        server = self.new_server.text()
        self.toml_time_sync['ntp_servers'].append(server)
        config_file.write(self.config)
        self.servers_table.insertRow(self.servers_table.rowCount())
        self.servers_table.setItem(self.servers_table.rowCount() - 1, 0, QTableWidgetItem(server))
        remove_button = QPushButton('remove')
        remove_button.clicked.connect(lambda state,n = server : self.remove_server(n))
        self.servers_table.setCellWidget(self.servers_table.rowCount() - 1, 1, remove_button)

        self.new_server.setText('')

    def add_servers(self):
        rows = self.toml_time_sync['ntp_servers']
        for i in range(len(rows)):
            self.servers_table.insertRow(i)
            name = rows[i]
            self.servers_table.setItem(i, 0, QTableWidgetItem(rows[i]))
            
            remove_button = QPushButton('remove')
            remove_button.clicked.connect(lambda state,n = name : self.remove_server(n))
            self.servers_table.setCellWidget(i, 1, remove_button)

            
    def remove_server(self, name):
        self.toml_time_sync['ntp_servers'].remove(name)
        config_file.write(self.config)
        for i in range(self.servers_table.rowCount()):
            if self.servers_table.item(i, 0).text() == name:
                self.servers_table.removeRow(i)
                break


    def refresh_config(self, config):
        self.config = config
        self.toml_time_sync = self.config['time-sync']
        self.enable_ntp.setChecked(self.toml_time_sync['enable_ntp'])
        self.enable_user.setChecked(self.toml_time_sync['enable_ntp_user'])

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
