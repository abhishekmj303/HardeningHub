from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton \
    , QTableWidget, QTableWidgetItem
from harden import config_file

class PhysicalPorts(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.temp_toml_dict = config_file.read() 
        self.toml_physical_ports = self.temp_toml_dict['physical-ports']

        self.main_label = QLabel("Physical Ports")
        self.layout.addWidget(self.main_label)

        # refresh button
        self.refresh_button = QPushButton("Refresh")    # no connect function yet
        self.layout.addWidget(self.refresh_button)
        
        # enable checkbox
        self.main_checkbox = QCheckBox("Enable USB Blocking")
        self.layout.addWidget(self.main_checkbox)
        self.main_checkbox.setChecked(self.toml_physical_ports['enable'])
        self.main_checkbox.stateChanged.connect(self.enable_checkbox_clicked)

        # table to block devices
        self.block_devices_table()

        # table to block ports
        self.block_ports_table()

    def block_devices_table(self):
        self.block_devices_label = QLabel("Block Devices")
        self.layout.addWidget(self.block_devices_label)

        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(3)
        self.layout.addWidget(self.devices_table)

        self.devices_table.setHorizontalHeaderLabels(["Device Name", "Device ID", "Allow"])

        def add_device_rows():
            rows = self.toml_physical_ports['device-rules']
            
            for i in range(len(rows)):
                self.devices_table.insertRow(i)
                self.devices_table.setItem(i, 0, QTableWidgetItem(rows[i]['name']))
                self.devices_table.setItem(i, 1, QTableWidgetItem(rows[i]['id']))

                checkbox = QCheckBox()
                checkbox.setChecked(rows[i]['allow'])
                checkbox.stateChanged.connect(lambda state, i=i: self.save_checkbox_state(state, i, 'device-rules'))

                self.devices_table.setCellWidget(i, 2, checkbox)

        add_device_rows()

    def block_ports_table(self):
        self.block_ports_label = QLabel("Block Ports")
        self.layout.addWidget(self.block_ports_label)

        self.ports_table = QTableWidget()
        self.ports_table.setColumnCount(3)
        self.layout.addWidget(self.ports_table)

        self.ports_table.setHorizontalHeaderLabels(["Port ID", "Device Name", "Allow"])
    
        def add_port_rows():
            rows = self.toml_physical_ports['port-rules']
            
            for i in range(len(rows)):
                self.ports_table.insertRow(i)
                self.ports_table.setItem(i, 0, QTableWidgetItem(rows[i]['id']))

                self.ports_table.setItem(i, 1, QTableWidgetItem(rows[i]['name']))

                checkbox = QCheckBox()
                checkbox.setChecked(rows[i]['allow'])
                checkbox.stateChanged.connect(lambda state, i=i: self.save_checkbox_state(state, i, 'port-rules'))

                self.ports_table.setCellWidget(i, 2, checkbox)
        
        add_port_rows()

    def enable_checkbox_clicked(self, state):
        self.toml_physical_ports['enable'] = (state == 2)
        self.devices_table.setEnabled((state == 2))
        self.ports_table.setEnabled((state == 2))
        config_file.write(self.temp_toml_dict)
    
    def save_checkbox_state(self, state, idx, rule):
        self.toml_physical_ports[rule][idx]['allow'] = (state == 2)
        config_file.write(self.temp_toml_dict)