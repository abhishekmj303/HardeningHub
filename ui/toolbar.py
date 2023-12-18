from PyQt6.QtWidgets import QToolBar, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal
from harden import config_file

class ToolBar(QToolBar):
    import_signal = pyqtSignal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        self.setMovable(False)  
        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        self.save_button = QPushButton("Save")
        self.script_button = QPushButton("Generate Script")

        self.addWidget(self.import_button)
        self.addWidget(self.export_button)
        self.addWidget(self.save_button)
        self.addWidget(self.script_button)

        self.import_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.export_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.save_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.script_button.setProperty('class', ['btn', 'toolbar-btn'])

        self.import_button.clicked.connect(self.import_button_clicked)
    
    def import_button_clicked(self):
        import_dialog = QFileDialog.getOpenFileName(self, "Select Config File", filter = "Config File (*.toml)")

        if not import_dialog[0]:
            return
        
        selected_file = import_dialog[0]
        print("selected file: ", selected_file)
        config_file.set_config_file(selected_file)
        self.config.update(config_file.read())

        self.import_signal.emit()