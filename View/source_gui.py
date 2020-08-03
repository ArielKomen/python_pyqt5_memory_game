"""
het idee is om 3 gui's te hebben. Een startpagina gui, een gui om parameters aan te passen
en een derde gui om memorie op te spelen.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget

from View.settings_gui import SettingGui
from View.playfield_gui import MemoryGui
from View.setup_gui import SetupGui
from Model.memory_model import is_database_initialized

class SourceGui(QMainWindow):
    def __init__(self, parent=None):
        super(SourceGui, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        #initialize the different GUI's
        self.setup_gui = SetupGui(self)
        self.settings_gui = SettingGui(self)
        self.playfield_gui = MemoryGui(self)
        #add the different GUI's to the central_widget and set the currentwidget as the setup gui.
        self.central_widget.addWidget(self.setup_gui)
        self.central_widget.addWidget(self.settings_gui)
        self.central_widget.addWidget(self.playfield_gui)
        #for the first time initialize the setup gui User Interface as the interface.
        self.set_setup_gui_ui()
        #Check if the database has been initialized, if not, create one
        is_database_initialized()
        #go from setup gui to the settings gui or the memory game gui.
        self.setup_gui.settings_button.clicked.connect(lambda: self.set_settings_gui_ui())
        self.setup_gui.start_game_button.clicked.connect(lambda: self.set_playfield_gui_ui())
        # go from the settings gui to the setup gui
        self.settings_gui.go_back_to_setup_button.clicked.connect(lambda: self.set_setup_gui_ui())
        #go from the memory game gui to the setup gui
        self.playfield_gui.go_back_to_setup_button.clicked.connect(lambda: self.set_setup_gui_ui())
    def set_setup_gui_ui(self):
        title = "Source Gui"
        left = 200
        top = 100
        width = 300
        height = 200
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)
        self.central_widget.setCurrentWidget(self.setup_gui)
    def set_settings_gui_ui(self):
        title = "Settings Gui"
        left = 200
        top = 100
        width = 500
        height = 200
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)
        self.central_widget.setCurrentWidget(self.settings_gui)
    def set_playfield_gui_ui(self):
        title = "Memory Game Gui"
        left = 200
        top = 100
        width = 500
        height = 300
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)
        self.playfield_gui.initialize_match_settings()
        self.playfield_gui.update_grid()
        self.central_widget.setCurrentWidget(self.playfield_gui)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    execute = SourceGui()
    execute.show()
    sys.exit(app.exec_())