import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QPushButton

class SetupGui(QWidget):
    def __init__(self, parent=None):
        super(SetupGui, self).__init__(parent)
        self.title = "Source Gui"
        self.left = 200
        self.top = 100
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.start_game_button = QPushButton("Start")
        self.start_game_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.settings_button = QPushButton("Settings")
        self.settings_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        vertical_box = QVBoxLayout()
        vertical_box.addWidget(self.start_game_button)
        vertical_box.addWidget(self.settings_button)

        self.setLayout(vertical_box)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SetupGui()
    ex.show()
    sys.exit(app.exec_())