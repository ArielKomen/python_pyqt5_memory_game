"""
This will be the gui in which you can ultimately play memory.
The settings about how to play can be selected in the settings gui.
"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, \
    QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QGridLayout, QMessageBox

from Model.memory_model import get_game_setting
from Model.memory_model import update_game_statistics
from Logic.memory_logic import MemoryMatch
from Logic.memory_logic import RegisterButtons
from Logic.memory_logic import is_turn_over
from Logic.memory_logic import get_row_and_colum
from Logic.memory_logic import analyze_game_outcome

class MemoryGui(QWidget):
    def __init__(self, parent=None):
        super(MemoryGui, self).__init__(parent)
        self.title = "Memory Game"
        self.left = 200
        self.top = 100
        self.width = 500
        self.height = 300
        self.initialize_match_settings()
        self.initUI()

    def initUI(self):
        #create widgets
        self.current_playing_player = QLabel("Current playing player: "+str(get_game_setting("player_one_name")))
        self.player_one_score = QLabel("Player: "+str(get_game_setting("player_one_name"))+", score: "+str(self.memory_match.get_player_one_score()))
        self.player_two_score = QLabel("Player: "+str(get_game_setting("player_two_name"))+", score: "+str(self.memory_match.get_player_two_score()))
        self.next_turn_button = QPushButton("Next turn")
        self.next_turn_button.setEnabled(False)
        self.next_turn_button.clicked.connect(self.next_turn)
        self.go_back_to_setup_button = QPushButton("Go to Setup")

        self.finished_game_message = QMessageBox()
        self.finished_game_message.setWindowTitle("The memory game is finished")
        self.finished_game_message.setText("")
        self.finished_game_message.setStandardButtons(QMessageBox.Ok)

        horizontal_go_back_to_setup_box = QHBoxLayout()
        horizontal_go_back_to_setup_box.addWidget(self.go_back_to_setup_button)
        horizontal_go_back_to_setup_box.addStretch()

        self.grid = self.create_playfield()
        horizontal_playing_player_box = QHBoxLayout()
        horizontal_playing_player_box.addWidget(self.current_playing_player)
        horizontal_playing_player_box.addStretch()
        horizontal_playing_player_box.addWidget(self.next_turn_button)

        horizontal_player_scores_box = QHBoxLayout()
        horizontal_player_scores_box.addWidget(self.player_one_score)
        horizontal_player_scores_box.addStretch()
        horizontal_player_scores_box.addWidget(self.player_two_score)

        self.vertical_box = QVBoxLayout()
        self.vertical_box.insertLayout(1, horizontal_go_back_to_setup_box)
        self.vertical_box.insertLayout(2, self.grid)
        self.vertical_box.insertLayout(3, horizontal_playing_player_box)
        self.vertical_box.insertLayout(4, horizontal_player_scores_box)

        self.setWindowTitle(self.title)
        self.setLayout(self.vertical_box)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def create_playfield(self):
        #create a matrix of buttons which will be the playing field.
        self.grid = QGridLayout()
        columns, rows = get_row_and_colum(int(get_game_setting("playfield_size")))
        positions = [(column, row) for column in range(int(columns)) for row in range(int(rows))]

        self.add_buttons_to_grid(positions)
        return self.grid
    def initialize_match_settings(self):
        #set the memory_match object with the default beginning values and initialize the playfield names
        column_count, row_count = get_row_and_colum(int(get_game_setting("playfield_size")))
        self.memory_match = MemoryMatch("player_one")
        self.registered_buttons = RegisterButtons(column_count, row_count)
        self.registered_buttons.initialize_button_dict()
        #accumulate +1 for started games.
        update_game_statistics("started_games")

    def button_pressed(self, button):
        #display the "hidden" text of the button and disable it.
        #when a button is pressed,(1) check which button it was (2) do some logic rules
        coordinates = button.text()
        hidden_name = self.registered_buttons.get_playfield_name(coordinates)
        button.setText(hidden_name)
        button.setEnabled(False)
        print("Button: "+coordinates+" was pressed")
        #accumulate the turn and save the guess of the player.
        self.memory_match.accumulate_turn()
        self.memory_match.save_clicked_button(coordinates, hidden_name)
        #check if the current player has chosen two cards
        if is_turn_over(self.memory_match.get_turn()) == False:
            #the turn is not over
            return
        else:
            #the turn is over. Disable all buttons and check if the player has guessed correctly.
            self.disable_all_buttons()
            self.process_turn()
            self.has_game_ended()


    def process_turn(self):
        #did the player guess two cards correctly or did he not?
        first_clicked_button = self.memory_match.get_clicked_buttons()[0]
        second_clicked_button = self.memory_match.get_clicked_buttons()[1]
        if first_clicked_button["card_name"] == second_clicked_button["card_name"]:
            #the guess was correct :-)
            print("The current player guessed two cards correctly. ")
            #add a point to the current player
            self.accumulate_point_to_current_player()
            #Make the correctly guessed buttons no longer clickable.
            self.registered_buttons.set_button_status(first_clicked_button["position"], False)
            self.registered_buttons.set_button_status(second_clicked_button["position"], False)
            self.outcome = True
        else:
            #The guess was not correct :-(
            print("The current player did not guess two cards correctly. ")
            self.outcome = False
        self.next_turn_button.setEnabled(True)

    def set_original_button_text(self):
        for index in range(0, 2):
            button_index = self.memory_match.get_clicked_buttons()[index]["position"]
            self.registered_buttons.get_button_instance(button_index)["button_instance"].setText(button_index)

    def accumulate_point_to_current_player(self):
        if self.memory_match.get_current_player() == "player_one":
            self.memory_match.accumulate_player_one_score()
            self.player_one_score.setText("Player: " + str(get_game_setting("player_one_name")) + ", score: " + str(
                self.memory_match.get_player_one_score()))
        else:
            self.memory_match.accumulate_player_two_score()
            self.player_two_score.setText("Player: " + str(get_game_setting("player_two_name")) + ", score: " + str(
                self.memory_match.get_player_two_score()))

    def next_turn(self):
        #keep the correctly guessed buttons disabled and make everything ready for a new turn
        #disable the next_turn_button
        self.next_turn_button.setEnabled(False)
        #set the turn back to zero
        self.memory_match.set_turn_to_zero()
        #set the current player
        self.set_current_player(self.memory_match.get_current_player())
        #If the previous player did not guess correctly, the buttons are reset to there original message.
        if self.outcome == False: self.set_original_button_text()
        #remove the clicked buttons from the previous turn
        self.memory_match.remove_clicked_buttons()
        #enable the buttons for the next turn.
        self.enabled_buttons()

    def enabled_buttons(self):
        #enable the buttons which need to be enabled.
        for button in self.registered_buttons.get_button_dict().values():
            button["button_instance"].setEnabled(button["status"])
    def disable_all_buttons(self):
        for button in self.registered_buttons.get_button_dict().values():
            button["button_instance"].setEnabled(False)

    def set_current_player(self, current_player):
        if current_player == "player_one":
            #time to set the new current player to player_two
            self.memory_match.set_current_player("player_two")
            self.current_playing_player.setText("Current playing player: " + str(get_game_setting("player_two_name")))
        elif current_player == "player_two":
            #time to set the new current player to player_one
            self.memory_match.set_current_player("player_one")
            self.current_playing_player.setText("Current playing player: " + str(get_game_setting("player_one_name")))
    def has_game_ended(self):
        #check if the game has ended.
        status_list = [button["status"] for button in self.registered_buttons.get_button_dict().values()]
        if True in status_list:
            #the game has not ended yet
            return
        else:
            #the game has ended. Show a message with the game outcome.
            game_outcome = analyze_game_outcome(str(get_game_setting("player_one_name")), str(get_game_setting("player_two_name")),
                                                str(self.memory_match.get_player_one_score()),str(self.memory_match.get_player_two_score()))
            self.finished_game_message.setText(game_outcome)
            self.finished_game_message.show()

            # disable the next_turn_button
            self.next_turn_button.setEnabled(False)
            # set the turn back to zero
            self.memory_match.set_turn_to_zero()
            # remove the clicked buttons from the previous turn
            self.memory_match.remove_clicked_buttons()
            #set the scores 0 for both player_one and player_two and update the labels to this new score.
            self.memory_match.set_player_one_score_to_zero()
            self.memory_match.set_player_two_score_to_zero()
            self.player_one_score.setText("Player: "+str(get_game_setting("player_one_name"))+", score: "+str(self.memory_match.get_player_one_score()))
            self.player_two_score.setText("Player: "+str(get_game_setting("player_two_name"))+", score: "+str(self.memory_match.get_player_two_score()))
            #make player_one the first player for coming game
            self.memory_match.set_current_player("player_one")
            #Add plus one to the finished games statistic
            update_game_statistics("finished_games")
            #Refresh the contents of the buttons
            self.update_content_buttons()

    def update_content_buttons(self):
        # All buttons need to be clickable again, have a new hidden_name and have a viewable message.
        names = self.registered_buttons.get_X_different_names(self.grid.columnCount(), self.grid.rowCount())
        index = 0
        for position, button in self.registered_buttons.get_button_dict().items():
            button["status"] = True
            button["hidden_name"] = names[index]
            button["button_instance"].setText(position)
            button["button_instance"].setEnabled(True)
            index += 1

    def update_grid(self):
        current_column_count, current_row_count = get_row_and_colum(int(get_game_setting("playfield_size")))
        current_positions = [(column, row) for column in range(int(current_column_count)) for row in range(int(current_row_count))]

        self.registered_buttons.initialize_button_dict()
        self.remove_grid_buttons()
        self.add_buttons_to_grid(current_positions)

    def remove_grid_buttons(self):
        for i in reversed(range(self.grid.count())):
            widgetToRemove = self.grid.itemAt(i).widget()
            # remove it from the layout list
            self.grid.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

    def add_buttons_to_grid(self, positions):
        for position in positions:
            coordinates = str(position[0])+"_"+str(position[1])
            button = QPushButton(coordinates)
            button.setFixedHeight(50)
            self.registered_buttons.set_button_instance(coordinates, button)
            self.registered_buttons.get_button_instance(coordinates)["button_instance"].clicked.connect(lambda state, button=button: self.button_pressed(button))
            self.grid.addWidget(self.registered_buttons.get_button_instance(coordinates)["button_instance"], position[0], position[1])
        print("There are "+str(self.grid.count())+" buttons/cards in the grid")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MemoryGui()
    ex.show()
    sys.exit(app.exec_())
