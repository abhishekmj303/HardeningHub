from PyQt6.QtWidgets import QStackedWidget, QScrollArea
from PyQt6.QtCore import Qt
from ui.pages.hardware_page import Hardware
from ui.pages.software_page import Software
from ui.pages.network_page import Network
from ui.pages.welcome_page import Welcome

class Pages(QScrollArea):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setProperty("class", "scroll-area")
        self.init_ui()
    
    def init_ui(self):
        self.StackedWidget = QStackedWidget()
        self.setWidget(self.StackedWidget)

        self.welcome = Welcome()
        self.hardware = Hardware(self.config)
        self.software = Software(self.config)
        self.network = Network(self.config)

        self.StackedWidget.addWidget(self.welcome)
        self.StackedWidget.addWidget(self.hardware)
        self.StackedWidget.addWidget(self.software)
        self.StackedWidget.addWidget(self.network)

        self.StackedWidget.setCurrentIndex(0)
    
    def refresh_config(self, config):
        self.config = config
        self.hardware.refresh_config(config)
        self.software.refresh_config(config)
        self.network.refresh_config(config)