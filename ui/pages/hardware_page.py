from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton \
    , QTableWidget, QTableWidgetItem
from tomlkit import loads, dumps

toml_copy_path = "./config/sampleconfig_copy.toml"

def read_toml_copy():                            # Read toml copy file and return as a dict
    with open(toml_copy_path, "r") as f:
        toml_content = f.read()
        toml_dict = loads(toml_content)
        return toml_dict

def save_toml_copy(toml_copy_dict):             # Save toml copy file
    with open(toml_copy_path, "w") as f:
        toml_content = dumps(toml_copy_dict)
        f.write(toml_content)

class Hardware(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.copytoml_dict = read_toml_copy() 
        self.toml_physical_ports = self.copytoml_dict['physical-ports']

        self.main_label = QLabel("Physical Ports")
        self.layout.addWidget(self.main_label)

        # refresh button
        self.refresh_button = QPushButton("Refresh")    # no connect function yet
        self.layout.addWidget(self.refresh_button)
        
        # enable checkbox
        self.main_checkbox = QCheckBox("Enable")
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
        save_toml_copy(self.copytoml_dict)
        if state == 2:
            self.devices_table.setEnabled(True)
            self.ports_table.setEnabled(True)
        else:
            self.devices_table.setEnabled(False)
            self.ports_table.setEnabled(False)
    
    def save_checkbox_state(self, state, idx, rule):
        self.toml_physical_ports[rule][idx]['allow'] = (state == 2)
        save_toml_copy(self.copytoml_dict)