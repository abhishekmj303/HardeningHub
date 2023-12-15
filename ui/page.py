from PyQt6.QtWidgets import QStackedWidget
from ui.pages.hardware_page import Hardware
from ui.pages.software_page import Software
from ui.pages.networking_page import Networking
from ui.pages.welcome_page import Welcome

class Pages(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.welcome = Welcome()
        self.hardware = Hardware()
        self.software = Software()
        self.networking = Networking()

        self.addWidget(self.welcome)
        self.addWidget(self.hardware)
        self.addWidget(self.software)
        self.addWidget(self.networking)

        self.setCurrentIndex(0)