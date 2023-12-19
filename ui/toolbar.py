from PyQt6.QtWidgets import QToolBar, QPushButton, QFileDialog \
    , QMessageBox
from PyQt6.QtCore import pyqtSignal
from tomlkit import TOMLDocument
from harden import config_file
from harden import script

class ToolBar(QToolBar):
    import_signal = pyqtSignal(TOMLDocument)

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
        self.export_button.clicked.connect(self.export_button_clicked)
        self.save_button.clicked.connect(self.save_button_clicked)
        self.script_button.clicked.connect(self.generate_script_button_clicked)
    
    def import_button_clicked(self):
        import_dialog = QFileDialog.getOpenFileName(self, "Select Config File", filter = "Config File (*.toml)")
        if not import_dialog[0]:
            return
        
        selected_file = import_dialog[0]
        print("selected file: ", selected_file)
    
        self.config = config_file.init(selected_file)
        self.import_signal.emit(self.config)

    def export_button_clicked(self):
        export_dialog = QFileDialog.getSaveFileName(self, "Export Config File", filter = "Config File (*.toml)")
        if not export_dialog[0]:
            return

        save_config_path = export_dialog[0]
        if not save_config_path.endswith(".toml"):
            save_config_path += ".toml"
        print("save config path: ", save_config_path)

        config_file.save(save_config_path)
    
    def save_button_clicked(self):
        self.message_box = QMessageBox()
        self.message_box.setWindowTitle("Save Configurations")
        self.message_box.setText("Are you sure you want to save?")
        self.message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.message_box.setDefaultButton(QMessageBox.StandardButton.No)
        self.message_box.setIcon(QMessageBox.Icon.Question)

        if self.message_box.exec() == QMessageBox.StandardButton.Yes:
            config_file.save()
            print("saved")
    
    def generate_script_button_clicked(self):
        generate_dialog = QFileDialog.getSaveFileName(self, "Generate Script File", filter = "Bash Script (*.sh)")
        if not generate_dialog[0]:
            return
        
        selected_file = generate_dialog[0]
        if not selected_file.endswith(".sh"):
            selected_file += ".sh"
        print("selected file: ", selected_file)
        script.save(selected_file)
