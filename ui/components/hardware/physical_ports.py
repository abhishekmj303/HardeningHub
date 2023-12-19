from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton \
    , QTableWidget, QTableWidgetItem, QHBoxLayout
from harden import config_file
from PyQt6.QtCore import Qt

class PhysicalPorts(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.toml_physical_ports = self.config['physical-ports']
        self.init_ui()
        self.refresh_config(config)
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        hlayout = QHBoxLayout()
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.main_label = QLabel("Physical Ports")
        hlayout.addWidget(self.main_label)
        self.main_label.setObjectName("component-title")

        # refresh button
        self.refresh_button = QPushButton("Refresh")    # no connect function yet
        hlayout.addWidget(self.refresh_button)
        self.refresh_button.setProperty('class', 'btn')

        self.layout.addLayout(hlayout)
        
        # container widget
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_widget.setLayout(self.container_layout)
        self.layout.addWidget(self.container_widget)
        self.container_layout.setSpacing(0)
        self.container_layout.setContentsMargins(30, 20, 30, 30)
        self.container_widget.setObjectName("container-widget")

        # enable checkbox
        self.main_checkbox = QCheckBox("Enable USB Blocking")
        self.container_layout.addWidget(self.main_checkbox)
        self.main_checkbox.stateChanged.connect(self.enable_checkbox_clicked)

        # table to block devices
        self.block_devices_table()

        # table to block ports
        self.block_ports_table()

    def block_devices_table(self):
        self.block_devices_label = QLabel("Block Devices")
        self.container_layout.addWidget(self.block_devices_label)
        self.block_devices_label.setObjectName("sub-component-title")

        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(3)
        self.container_layout.addWidget(self.devices_table)

        self.devices_table.setHorizontalHeaderLabels(["Device Name", "Device ID", "Allow"])

    def add_device_rows(self):
        rows = self.toml_physical_ports['device-rules']
        
        for i in range(len(rows)):
            self.devices_table.insertRow(i)
            self.devices_table.setItem(i, 0, QTableWidgetItem(rows[i]['name']))
            self.devices_table.setItem(i, 1, QTableWidgetItem(rows[i]['id']))

            checkbox = QCheckBox()
            checkbox.setChecked(rows[i]['allow'])
            checkbox.stateChanged.connect(lambda state, i=i: self.save_checkbox_state(state, i, 'device-rules'))

            self.devices_table.setCellWidget(i, 2, checkbox)


    def block_ports_table(self):
        self.block_ports_label = QLabel("Block Ports")
        self.container_layout.addWidget(self.block_ports_label)
        self.block_ports_label.setObjectName("sub-component-title")

        self.ports_table = QTableWidget()
        self.ports_table.setColumnCount(3)
        self.container_layout.addWidget(self.ports_table)

        self.ports_table.setHorizontalHeaderLabels(["Port ID", "Device Name", "Allow"])
    
    def add_port_rows(self):
        rows = self.toml_physical_ports['port-rules']
        
        for i in range(len(rows)):
            self.ports_table.insertRow(i)
            self.ports_table.setItem(i, 0, QTableWidgetItem(rows[i]['id']))

            self.ports_table.setItem(i, 1, QTableWidgetItem(rows[i]['name']))

            checkbox = QCheckBox()
            checkbox.setChecked(rows[i]['allow'])
            checkbox.stateChanged.connect(lambda state, i=i: self.save_checkbox_state(state, i, 'port-rules'))

            self.ports_table.setCellWidget(i, 2, checkbox)

    def refresh_config(self, config):
        self.config = config
        self.toml_physical_ports = self.config['physical-ports']
        self.main_checkbox.setChecked(self.toml_physical_ports['enable'])
        if not self.toml_physical_ports['enable']:
            self.devices_table.setEnabled(False)
            self.ports_table.setEnabled(False)
        self.devices_table.setRowCount(0)
        self.ports_table.setRowCount(0)
        self.add_device_rows()
        self.add_port_rows()

    def enable_checkbox_clicked(self, state):
        self.toml_physical_ports['enable'] = (state == 2)
        self.devices_table.setEnabled((state == 2))
        self.ports_table.setEnabled((state == 2))
        config_file.write(self.config)
    
    def save_checkbox_state(self, state, idx, rule):
        self.toml_physical_ports[rule][idx]['allow'] = (state == 2)
        config_file.write(self.config)