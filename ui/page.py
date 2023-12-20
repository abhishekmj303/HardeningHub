from PyQt6.QtWidgets import QStackedWidget, QScrollArea, QWidget
from PyQt6.QtCore import Qt
from ui.pages.hardware_page import Hardware
from ui.pages.software_page import Software
from ui.pages.network_page import Network
from ui.pages.welcome_page import Welcome

class Pages(QScrollArea):
    def __init__(self, config, tooltip):
        super().__init__()
        self.config = config
        self.tooltip = tooltip
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.init_ui()
    
    def init_ui(self):
        self.StackedWidget = QStackedWidget()
        self.setWidget(self.StackedWidget)

        self.welcome = Welcome()
        self.hardware = Hardware(self.config, self.tooltip)
        self.software = Software(self.config, self.tooltip)
        self.network = Network(self.config, self.tooltip)

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
    
    # def search_items(self, text):
    #     print('page')
    #     curr_index = self.StackedWidget.currentIndex()
    #     if curr_index == 1:
    #         widget_items = self.hardware.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly)
    #     elif curr_index == 2:
    #         widget_items = self.software.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly)
    #     elif curr_index == 3:
    #         widget_items = self.network.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly)
    #     else:
    #         return
    #     widget_names = [item.objectName() for item in widget_items]
    #     print(widget_names)
    #     self.completer = QCompleter(widget_names)
    #     self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)