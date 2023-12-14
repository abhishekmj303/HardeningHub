from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget
from PyQt6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.page import Pages
import sys

toml_file_path = "config/sampleconfig.toml"
toml_copy_path = "config/sampleconfig_copy.toml"

def make_copy_config():
    with open(toml_file_path, "r") as f:
        data = f.read()
    with open(toml_copy_path, "w") as f:
        f.write(data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("HardeningHub")
        self.setGeometry(0, 0, 1920, 1000)

        self.pages = Pages()
        self.setCentralWidget(self.pages)
        
        self.sidebar = QDockWidget("Menu")
        self.sidebar_widget = Sidebar()
        self.sidebar.setWidget(self.sidebar_widget)
        self.sidebar.setFixedWidth(250)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)
        self.sidebar.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.sidebar_widget.change_page_signal.connect(self.change_page)
    
    def change_page(self, index):
        self.pages.setCurrentIndex(index)

def main():
    make_copy_config()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n> Closing...")
        exit(0)