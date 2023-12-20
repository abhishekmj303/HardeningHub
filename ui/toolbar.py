from PyQt6.QtWidgets import QToolBar, QPushButton, QFileDialog \
    , QMessageBox, QCheckBox, QWidget, QSizePolicy, QMenu, QLineEdit, QDialog, QVBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal
from tomlkit import TOMLDocument
from harden import config_file
from harden import script


class ConfirmationDialog(QMessageBox):
    def __init__(self, title: str, message: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.No)
        self.setIcon(QMessageBox.Icon.Question)


class ToolBar(QToolBar):
    import_signal = pyqtSignal(TOMLDocument)
    theme_changed_signal = pyqtSignal(bool)
    search_signal = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        self.setMovable(False)

        self.profiles_button = QPushButton("Default Profile")
        self.profiles_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.profiles_menu = QMenu(self.profiles_button)
        self.profiles_menu.addAction("Default", lambda: self.switch_profile("default"))
        self.profiles = config_file.get_profiles()
        for profile in self.profiles:
            self.profiles_menu.addAction(profile.title(), lambda p = profile: self.switch_profile(p))
        self.profiles_menu.addAction("Add New Profile", lambda: self.add_new_profile())
        self.profiles_button.setMenu(self.profiles_menu)
        self.addWidget(self.profiles_button)




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

        workstation_level1_action.triggered.connect(lambda: self.import_level("w1"))
        server_level1_action.triggered.connect(lambda: self.import_level("s1"))
        workstation_level2_action.triggered.connect(lambda: self.import_level("w2"))
        server_level2_action.triggered.connect(lambda: self.import_level("s2"))


        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        self.save_button = QPushButton("Save")
        self.script_button = QPushButton("Generate Script")
        self.run_button = QPushButton("Run Script")

        self.addWidget(self.import_button)
        self.addWidget(self.export_button)
        self.addWidget(self.save_button)
        self.addWidget(self.script_button)
        self.addWidget(self.run_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)

        # Search Bar
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search")
        self.searchbar.setProperty('class', 'searchbar')
        self.searchbar.textChanged.connect(self.searchbar_text_changed)
        self.addWidget(self.searchbar)

        # Toggle Theme
        self.theme_checkbox = QCheckBox("Dark Mode")
        self.theme_checkbox.setChecked(False)
        self.theme_checkbox.stateChanged.connect(self.theme_checkbox_clicked)
        self.theme_checkbox.setProperty('class', 'theme-btn')
        self.addWidget(self.theme_checkbox)


        self.import_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.export_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.save_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.script_button.setProperty('class', ['btn', 'toolbar-btn'])
        self.run_button.setProperty('class', ['btn', 'toolbar-btn'])

        self.import_button.clicked.connect(self.import_button_clicked)
        self.export_button.clicked.connect(self.export_button_clicked)
        self.save_button.clicked.connect(self.save_button_clicked)
        self.script_button.clicked.connect(self.script_button_clicked)
        self.run_button.clicked.connect(self.run_button_clicked)

    def switch_profile(self, profile: str):
        if profile == "default":
            self.config = config_file.init()
            self.import_signal.emit(self.config)
            self.profiles_button.setText("Default Profile")
            return
        profile_file = config_file.get_profile_path(profile)
        self.config = config_file.init(profile_file)
        self.import_signal.emit(self.config)
        self.profiles_button.setText(f"Profile: {profile.title()}")

    def add_new_profile(self):
        # take input from user using a dialog
        add_new_profile_dialog = QDialog()
        add_new_profile_dialog.setWindowTitle("Add New Profile")
        add_new_profile_dialog.setModal(True)
        add_new_profile_dialog.resize(300, 100)
        add_new_profile_dialog.setFixedSize(add_new_profile_dialog.size())

        profile_name_input = QLineEdit()
        profile_name_input.setPlaceholderText("Profile Name")
        profile_name_input.setProperty('class', 'searchbar')

        add_button = QPushButton("Add")
        add_button.setProperty('class', ['btn', 'toolbar-btn'])
        add_button.clicked.connect(add_new_profile_dialog.accept)

        # add input and button to dialog
        layout = QVBoxLayout()
        add_new_profile_dialog.setLayout(layout)
        layout.addWidget(profile_name_input)
        layout.addWidget(add_button)

        if add_new_profile_dialog.exec():
            profile_name = profile_name_input.text()
            self.config = config_file.init_profile(profile_name)
            self.import_signal.emit(self.config)
            #add action at last but before add new profile
            self.profiles_menu.insertAction(self.profiles_menu.actions()[-1], QAction(profile_name.title(), self.profiles_menu, triggered = lambda p = profile_name: self.switch_profile(p)))
            self.profiles_button.setText(f"Profile: {profile_name.title()}")

    
    def import_level(self, level: str = "w1"):
        self.config = config_file.import_level(level)
        self.import_signal.emit(self.config)
    
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
        message_box = ConfirmationDialog("Save Configurations", "Are you sure you want to save?")
        if message_box.exec() == QMessageBox.StandardButton.Yes:
            config_file.save()
            print("saved")
    
    def script_button_clicked(self):
        message_box = ConfirmationDialog("Create Backup", "Do you want to create a system backup before running the script?")
        if message_box.exec() == QMessageBox.StandardButton.Yes:
            backup = True
        else:
            backup = False

        generate_dialog = QFileDialog.getSaveFileName(self, "Generate Script File", filter = "Bash Script (*.sh)")
        if not generate_dialog[0]:
            return
        
        selected_file = generate_dialog[0]
        if not selected_file.endswith(".sh"):
            selected_file += ".sh"
        print("selected file: ", selected_file)
        script.save(selected_file, backup)

    def theme_checkbox_clicked(self, state):
        if state == 2:
            self.theme_changed_signal.emit(True)
        else:
            self.theme_changed_signal.emit(False)
    
    def searchbar_text_changed(self, text):
        self.search_signal.emit(text)
    
    def run_button_clicked(self):
        message_box = ConfirmationDialog("Create Backup", "Do you want to create a backup before running the script?")
        if message_box.exec() == QMessageBox.StandardButton.Yes:
            backup = True
        else:
            backup = False
        
        script.run(backup)
