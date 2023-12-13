from PyQt6.QtWidgets import QStackedWidget
from ui.pages.hardware_page import Hardware
from ui.pages.software_page import Software
from ui.pages.networking_page import Networking

class Pages(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.hardware = Hardware()
        self.software = Software()
        self.networking = Networking()

        self.addWidget(self.hardware)
        self.addWidget(self.software)
        self.addWidget(self.networking)