"""
De settings gui hoor je te kunnen openen vanuit de source gui.
In deze gui kan je settings aanpassen. Of de settings opgeslagen kunnen worden
is nog maar de vraag, dat is een extra stap, moet ik even nadenken over hoe ik dat zou kunnen doen.
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, \
    QHBoxLayout, QSizePolicy, QLabel, QVBoxLayout, QLineEdit, QPushButton
#import the model
from Model.memory_model import *


class SettingGui(QWidget):
    def __init__(self, parent=None):
        super(SettingGui, self).__init__(parent)
        self.title = "Settings Gui"
        self.left = 200
        self.top = 100
        self.width = 500
        self.height = 300
        self.initUI()

    def initUI(self):
        self.card_amount_label = QLabel("With how many cards will you play: ")
        self.player_one_label = QLabel("What's the first players name: ")
        self.player_two_label = QLabel("What's the second players name: ")
        self.statistics_label = QLabel("Some game statistics:")
        self.games_started_label = QLabel("The amount of games started: "+str(get_game_statistic("started_games")))
        self.games_finished_label = QLabel("The amount of games finished: "+str(get_game_statistic("finished_games")))

        self.go_back_to_setup_button = QPushButton("Go to Setup")

        self.card_amount_options = QComboBox()
        self.card_amount_options.addItems(["4","8","10","16","36"])
        self.card_amount_options.setCurrentText(get_game_setting("playfield_size"))
        self.card_amount_options.currentIndexChanged.connect(self.card_selection_change)

        self.player_one_name_line_edit = QLineEdit()
        self.player_one_name_line_edit.setText(get_game_setting("player_one_name"))
        self.player_one_name_line_edit.setMaxLength(30)
        self.player_one_name_line_edit.setAlignment(Qt.AlignLeft)
        self.player_one_name_line_edit.textChanged.connect(self.player_one_name_changed)

        self.player_two_name_line_edit =QLineEdit()
        self.player_two_name_line_edit.setText(get_game_setting("player_two_name"))
        self.player_two_name_line_edit.setMaxLength(30)
        self.player_two_name_line_edit.setAlignment(Qt.AlignLeft)
        self.player_two_name_line_edit.textChanged.connect(self.player_two_name_changed)

        horizontal_go_back_to_setup_gui_box = QHBoxLayout()
        horizontal_go_back_to_setup_gui_box.addWidget(self.go_back_to_setup_button)
        horizontal_go_back_to_setup_gui_box.addStretch()

        horizontal_player_one_name_box = QHBoxLayout()
        horizontal_player_one_name_box.addWidget(self.player_one_label)
        horizontal_player_one_name_box.addWidget(self.player_one_name_line_edit)

        horizontal_player_two_name_box = QHBoxLayout()
        horizontal_player_two_name_box.addWidget(self.player_two_label)
        horizontal_player_two_name_box.addWidget(self.player_two_name_line_edit)

        horizontal_card_amount_box = QHBoxLayout()
        horizontal_card_amount_box.addWidget(self.card_amount_label)
        horizontal_card_amount_box.addWidget(self.card_amount_options)
        horizontal_card_amount_box.addStretch()

        horizontal_game_statistics_box = QHBoxLayout()
        horizontal_game_statistics_box.addWidget(self.statistics_label)
        horizontal_game_statistics_box.addStretch()

        horizontal_games_started_box = QHBoxLayout()
        horizontal_games_started_box.addWidget(self.games_started_label)
        horizontal_games_started_box.addStretch()

        horizontal_games_finished_box = QHBoxLayout()
        horizontal_games_finished_box.addWidget(self.games_finished_label)
        horizontal_games_finished_box.addStretch()

        vertical_box = QVBoxLayout()
        vertical_box.insertLayout(1, horizontal_go_back_to_setup_gui_box)
        vertical_box.insertLayout(2, horizontal_card_amount_box)
        vertical_box.insertLayout(3, horizontal_player_one_name_box)
        vertical_box.insertLayout(4, horizontal_player_two_name_box)
        vertical_box.addSpacing(20)
        vertical_box.insertLayout(5, horizontal_game_statistics_box)
        vertical_box.insertLayout(6, horizontal_games_started_box)
        vertical_box.insertLayout(7, horizontal_games_finished_box)
        vertical_box.addStretch()

        self.setLayout(vertical_box)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    def card_selection_change(self):
        #when the card selection is changed, change the playfield_size variable to the new amount of cards.
        print("new card amount selected: "+str(self.card_amount_options.currentText()))
        update_game_settings("playfield_size", str(self.card_amount_options.currentText()))
    def player_one_name_changed(self):
        #when the first player name is changed, change ??? variable to the new first player name.
        print("First player name: " + str(self.player_one_name_line_edit.text()))
        update_game_settings("player_one_name", str(self.player_one_name_line_edit.text()))
    def player_two_name_changed(self):
        #when the second players name is changed, change ??? variable to the second players name.
        print("Second player name: " + str(self.player_two_name_line_edit.text()))
        update_game_settings("player_two_name", str(self.player_two_name_line_edit.text()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingGui()
    ex.show()
    sys.exit(app.exec_())