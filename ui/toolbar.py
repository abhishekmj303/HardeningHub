from PyQt6.QtWidgets import QToolBar, QPushButton, QFileDialog \
    , QMessageBox, QCheckBox, QWidget, QSizePolicy, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal
from tomlkit import TOMLDocument
from harden import config_file
from harden import script

class ToolBar(QToolBar):
    import_signal = pyqtSignal(TOMLDocument)
    theme_changed_signal = pyqtSignal(bool)


    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        self.setMovable(False)  

        self.levels_button = QPushButton("Levels")
        self.levels_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.levels_menu = QMenu(self.levels_button)
        workstation_level1_action = QAction("Level 1 - Workstation", self.levels_menu)
        server_level1_action = QAction("Level 1 - Server", self.levels_menu)
        workstation_level2_action = QAction("Level 2 - Workstation", self.levels_menu)
        server_level2_action = QAction("Level 2 - Server", self.levels_menu)
        self.levels_menu.addAction(workstation_level1_action)
        self.levels_menu.addAction(server_level1_action)
        self.levels_menu.addAction(workstation_level2_action)
        self.levels_menu.addAction(server_level2_action)
        self.levels_button.setMenu(self.levels_menu)
        self.addWidget(self.levels_button)



        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        self.save_button = QPushButton("Save")
        self.script_button = QPushButton("Generate Script")

        self.addWidget(self.import_button)
        self.addWidget(self.export_button)
        self.addWidget(self.save_button)
        self.addWidget(self.script_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)

        self.theme_checkbox = QCheckBox("Dark Mode")
        self.theme_checkbox.setChecked(False)
        self.theme_checkbox.stateChanged.connect(self.theme_checkbox_clicked)
        self.theme_checkbox.setProperty('class', 'theme-btn')
        self.addWidget(self.theme_checkbox)


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

    def theme_checkbox_clicked(self, state):
        if state == 2:
            self.theme_changed_signal.emit(True)
        else:
            self.theme_changed_signal.emit(False)
    
    def generate_script_button_clicked(self):
        generate_dialog = QFileDialog.getSaveFileName(self, "Generate Script File", filter = "Bash Script (*.sh)")
        if not generate_dialog[0]:
            return
        
        selected_file = generate_dialog[0]
        if not selected_file.endswith(".sh"):
            selected_file += ".sh"
        print("selected file: ", selected_file)
        script.save(selected_file)
