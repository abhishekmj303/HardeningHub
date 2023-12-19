from PyQt6.QtWidgets import QApplication, QMainWindow \
    , QHBoxLayout, QWidget, QScrollArea
from PyQt6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.page import Pages
from ui.toolbar import ToolBar
from harden import config_file, tooltip_file
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = config_file.init()
        self.tooltip = tooltip_file.read()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("HardeningHub")
        self.setGeometry(0, 0, 1920, 1000)

        self.toolbar = ToolBar(self.config)
        self.addToolBar(self.toolbar)

        self.pages = Pages(self.config, self.tooltip)
        self.pages.setObjectName("page")
        self.toolbar.import_signal.connect(self.pages.refresh_config)

        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setObjectName("sidebarBg")
        self.sidebar.change_page_signal.connect(self.pages.StackedWidget.setCurrentIndex)

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.pages)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(open("ui/qss/dark.qss", "r").read())
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n> Closing...")
        exit(0)