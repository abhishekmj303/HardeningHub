from PyQt6.QtWidgets import QApplication, QMainWindow \
    , QHBoxLayout, QWidget, QCompleter
from PyQt6.QtCore import Qt, pyqtSignal
from ui.sidebar import Sidebar
from ui.page import Pages
from ui.toolbar import ToolBar
from harden import config_file, tooltip_file
import sys

class MainWindow(QMainWindow):
    theme_signal = pyqtSignal(bool)
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
        self.toolbar.theme_changed_signal.connect(self.change_theme)


        self.sidebar = Sidebar()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setObjectName("sidebarBg")
        self.sidebar.change_page_signal.connect(self.change_page)

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.pages)
        
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.toolbar.search_signal.connect(self.search_items)
    
    def change_page(self, index):
        self.pages.StackedWidget.setCurrentIndex(index)
        self.pages.verticalScrollBar().setValue(0)

    def change_theme(self, theme):
        if theme:
            name = "dark"
        else:
            name = "light"
        self.setStyleSheet(open(f"ui/qss/{name}.qss", "r").read())
        self.sidebar.set_theme(theme)
    
    def search_items(self, text):
        curr_index = self.pages.StackedWidget.currentIndex()
        if curr_index == 1:
            widget_items = self.pages.hardware.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly)
        elif curr_index == 2:
            widget_items = self.pages.software.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly)
        elif curr_index == 3:
            widget_items = self.pages.network.findChildren(QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly)
        else:
            return
        widget_names = [item.objectName() for item in widget_items]
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.toolbar.searchbar.setCompleter(self.completer)

        print(widget_names)
        for i in range(len(widget_names)):
            widget_name = widget_names[i]
            widget = widget_items[i]
            if text.lower() in widget_name.lower():
                widget.show()
            else:
                widget.hide()

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(open("ui/qss/light.qss", "r").read())
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n> Closing...")
        exit(0)