from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox \
    , QHBoxLayout, QComboBox, QLineEdit, QPushButton
from PyQt6.QtGui import QIntValidator
from harden import config_file

class TimeSync(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.toml_time_sync = self.config['time-sync']

        self.main_label = QLabel("Time Synchronization")
        self.layout.addWidget(self.main_label)
        self.main_label.setObjectName("component-title")

        #enable ntp checkbox
        self.enable_ntp = QCheckBox('Enable NTP')
        self.enable_ntp.stateChanged.connect(lambda state, name = 'enable_ntp': self.save_checkbox_state(name, state))

        ntp_server_lable = QLabel('NTP Servers')
        self.layout.addWidget(ntp_server_lable)

        hlayout = QHBoxLayout()

        self.new_server = QLineEdit()
        self.add_button = QPushButton('add')
        self.add_button.clicked.connect(self.add_new_server)

        hlayout.addWidget(self.new_server)
        hlayout.addWidget(self.add_button)

        self.layout.addLayout(hlayout)

        for servers in self.toml_time_sync['ntp_servers']:
            self.add_server(servers)

        self.enable_user = QCheckBox('Enable NTP user')
        self.enable_user.stateChanged.connect(lambda state, name = 'enable_ntp_user': self.save_checkbox_state(name, state))
        self.layout.addWidget(self.enable_user)

    def add_new_server(self):
        server = self.new_server.text()
        self.toml_time_sync['ntp_servers'].append(server)
        config_file.write(self.config)
        self.add_server(server)
        self.new_server.setText('')

    def add_server(self, server):
        if server == '':
            return
        
        hlayout = QHBoxLayout()
        self.layout.addLayout(hlayout)

        server_label = QLabel(server)
        hlayout.addWidget(server_label)

        remove_button = QPushButton('remove')
        remove_button.clicked.connect(lambda : self.remove_server(server, hlayout, server_label, remove_button))
        hlayout.addWidget(remove_button)

    def remove_server(self, server, hlayout: QHBoxLayout, server_label: QLabel, remove_button: QPushButton):
        self.toml_time_sync['ntp_servers'].remove(server)
        config_file.write(self.config)
        server_label.deleteLater()
        remove_button.deleteLater()
        hlayout.deleteLater()

    def save_checkbox_state(self, name, state):
        self.toml_gdm[name] = (state == 2)
        config_file.write(self.config)
