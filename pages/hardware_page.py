from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton \
    , QTableWidget, QTableWidgetItem
from tomlkit import loads, dumps

toml_file_path = "./BackEnd/sampleconfig.toml"
toml_copy_path = "./BackEnd/sampleconfig_copy.toml"

def read_toml():                            # Read toml file and return as a dict
    with open(toml_file_path, "r") as f:
        toml_content = f.read()
        toml_dict = loads(toml_content)
        return toml_dict["physical-ports"]  # return only physical-ports content

class Hardware(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.toml_dict = read_toml()
        self.toml_copy = self.toml_dict.copy()

        self.main_label = QLabel("Physical Ports")
        self.layout.addWidget(self.main_label)

        self.refresh_button = QPushButton("Refresh")    # no connect function yet
        self.layout.addWidget(self.refresh_button)

        self.main_checkbox = QCheckBox("Enable")
        self.layout.addWidget(self.main_checkbox)
        self.main_checkbox.setChecked(self.toml_dict['enable'])
        self.main_checkbox.stateChanged.connect(self.main_checkbox_clicked)

        self.allow_all_checkbox = QCheckBox("Allow All Devices")
        self.layout.addWidget(self.allow_all_checkbox)
        self.allow_all_checkbox.setChecked(self.toml_dict['allow-all'])
        self.allow_all_checkbox.stateChanged.connect(self.allow_all_checkbox_clicked)

        self.block_devices_table()
        self.block_ports_table()

        self.save_changes = QPushButton("Save Changes")
        self.layout.addWidget(self.save_changes)
        self.save_changes.setStyleSheet("background-color: green")
        self.save_changes.clicked.connect(self.save_changes_clicked)

    # Table to block devices
    def block_devices_table(self):
        self.block_devices_label = QLabel("Block Devices")
        self.layout.addWidget(self.block_devices_label)

        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(4)
        self.layout.addWidget(self.devices_table)

        self.devices_table.setHorizontalHeaderLabels(["Device Name", "Device ID", "Port ID", "Allow"])

        self.add_device_rows()

    def add_device_rows(self):
        rows = self.toml_dict['device-rules']
        
        for i in range(len(rows)):
            self.devices_table.insertRow(i)
            self.devices_table.setItem(i, 0, QTableWidgetItem(rows[i]['name']))
            self.devices_table.setItem(i, 1, QTableWidgetItem(rows[i]['id']))
            try:
                self.devices_table.setItem(i, 2, QTableWidgetItem(rows[i]['port']))
            except Exception as e:
                self.devices_table.setItem(i, 2, QTableWidgetItem('All'))
            
            self.devices_table.setCellWidget(i, 3, QCheckBox())
            self.devices_table.cellWidget(i, 3).setChecked(rows[i]['allow'])\

    # Table to block ports
    def block_ports_table(self):
        self.block_ports_label = QLabel("Block Ports")
        self.layout.addWidget(self.block_ports_label)

        self.ports_table = QTableWidget()
        self.ports_table.setColumnCount(2)
        self.layout.addWidget(self.ports_table)

        self.ports_table.setHorizontalHeaderLabels(["Port ID", "Allow"])

        self.add_port_rows()
    
    def add_port_rows(self):
        rows = self.toml_dict['port-rules']
        
        for i in range(len(rows)):
            self.ports_table.insertRow(i)
            self.ports_table.setItem(i, 0, QTableWidgetItem(rows[i]['port']))

            self.ports_table.setCellWidget(i, 1, QCheckBox())
            self.ports_table.cellWidget(i, 1).setChecked(rows[i]['allow'])

    def main_checkbox_clicked(self):
        if self.main_checkbox.isChecked():
            self.toml_copy['enable'] = True
        else:
            self.toml_copy['enable'] = False
    
    def allow_all_checkbox_clicked(self):
        if self.allow_all_checkbox.isChecked():
            self.toml_copy['allow-all'] = True
        else:
            self.toml_copy['allow-all'] = False
    
    def save_changes_clicked(self):
        # set devices states
        for i in range(len(self.toml_copy['device-rules'])):
            if self.devices_table.cellWidget(i, 3).isChecked():
                self.toml_copy['device-rules'][i]['allow'] = True
            else:
                self.toml_copy['device-rules'][i]['allow'] = False
        
        # set ports states
        for i in range(len(self.toml_copy['port-rules'])):
            if self.ports_table.cellWidget(i, 1).isChecked():
                self.toml_copy['port-rules'][i]['allow'] = True
            else:
                self.toml_copy['port-rules'][i]['allow'] = False
        
        with open(toml_file_path, 'r') as f:
            toml_content = f.read()
            final_toml_dict = loads(toml_content)
            final_toml_dict['physical-ports'] = self.toml_copy
        
        with open(toml_copy_path, 'w') as f:
            final_toml_content = dumps(final_toml_dict)
            f.write(final_toml_content)