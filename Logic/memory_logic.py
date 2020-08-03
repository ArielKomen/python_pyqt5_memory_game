#All the logic in order to play memory are found in this file.
import math
import random
from Model.memory_model import get_game_setting

class MemoryMatch():
    def __init__(self, current_player):
        self.__turn = 0
        self.__clicked_buttons = []
        self.__current_player = current_player
        self.__player_one_score = 0
        self.__player_two_score = 0

    def accumulate_player_one_score(self):
        self.__player_one_score += 1
    def accumulate_player_two_score(self):
        self.__player_two_score += 1
    def get_player_one_score(self):
        return self.__player_one_score
    def get_player_two_score(self):
        return self.__player_two_score
    def set_player_one_score_to_zero(self):
        self.__player_one_score = 0
    def set_player_two_score_to_zero(self):
        self.__player_two_score = 0


    def save_clicked_button(self, position, name):
        player_guess = {"position":position, "card_name":name}
        self.__clicked_buttons.append(player_guess)
    def get_clicked_buttons(self):
        return self.__clicked_buttons
    def remove_clicked_buttons(self):
        self.__clicked_buttons = []

    def accumulate_turn(self):
        self.__turn += 1
    def set_turn_to_zero(self):
        self.__turn = 0
    def get_turn(self):
        return self.__turn

    def set_current_player(self, player_name):
        self.__current_player = player_name
    def get_current_player(self):
        return self.__current_player


class RegisterButtons:
    def __init__(self, column_count, row_count):
        self.__button_dict = {}
        self.__column_count = column_count
        self.__row_count = row_count

    def initialize_button_dict(self):
        #Make sure that the self.__button_dict is empty, else weird previous objects will interrupt the game.
        self.__button_dict.clear()
        index = 0
        names = self.get_X_different_names(self.__column_count, self.__row_count)
        for column in range(self.__column_count):
            for row in range(self.__row_count):
                position = str(column)+"_"+str(row)
                self.__button_dict[position] = {"button_instance":None,
                                                "hidden_name":names[index],
                                                "status":True}
                index += 1
    def get_X_different_names(self, column, row):
        names = get_game_setting("game_card_names")
        #names = ["fish","cat","tiger","moon","sun","lion","river","ocean","peanut","elephant","monkey", "dolphin","jaguar","sand","tundra","hyena","treasure","diamond","ruby","emerald","potasium","camel","horse","leaf","knight","king","emperor","ocean","sea","boat","pirate","ninja","tree"]
        total_names_devided_by_two = (column * row) / 2
        unique_names = []
        used_integers = []

        while len(unique_names) != int(total_names_devided_by_two):
            random_integer = random.randint(0, len(names)-1)
            if not random_integer in used_integers:
                name = names[random_integer]
                unique_names.append(name)
                used_integers.append(random_integer)
        unique_names = unique_names + unique_names

        return sorted(unique_names, key=lambda k: random.random())

    def set_button_instance(self, position, button):
        self.__button_dict[position]["button_instance"] = button
    def get_button_instance(self, position):
        return self.__button_dict[str(position)]

    def get_playfield_name(self, position):
        return self.__button_dict[str(position)]["hidden_name"]
    def set_playfield_name(self, position, name):
        self.__button_dict[str(position)]["hidden_name"] = name

    def set_button_status(self, position, boolean):
        self.__button_dict[position]["status"] = boolean
    def get_button_status(self, position):
        return self.__button_dict[position]["status"]

    def get_button_dict(self):
        return self.__button_dict



def get_row_and_colum(total_card_amount):
    """
    get the dimensions of a squarable number. If a number is not squarable but even,
    divide it by 2 and the columns will be 2 and the rows will be the divided number.
    :param integer total_card_amount: the amount of cards in the playfield
    :return: (columns, rows): the columns and the rows of the playfield
    """
    squared_total_card_amount = math.sqrt(total_card_amount)
    columns = 0
    rows = 0
    #Is the squared total card amount an even number? Yes, return the squared_total_card_amount value
    if squared_total_card_amount % 2 == 0:
        columns, rows = int(squared_total_card_amount), int(squared_total_card_amount)
        return (columns, rows)
    else:
        #When the total card amount is not squarable there will be two rows and the columns are total_card_amount divided by two.
        columns = total_card_amount / 2
        rows = 2
        return(int(columns), int(rows))

def is_turn_over(turn):
    """
    1 is the first turn. 2 is the second turn
    :param turn(int): this integer tells the method which is the current turn.
    :return: boolean. If the turn is not over, False will be returned, if the turn is over, True will be returned.
    """
    if int(turn) == 1:
        #the turn is not over
        return False
    elif int(turn) == 2:
        #this is the second turn. The turn is over!
        return True
    else:
        #something is going wrong
        print("The third turn is reached for the current player.\nThis should not happen...the program will be stopped")

def analyze_game_outcome(player_one_name, player_two_name, player_one_score, player_two_score):
    """
    Analyze the outcome of the game. Was there a tie or a winner/loser? Return a string with this information.
    :param player_one_name: (string) the name of the first player
    :param player_two_name: (string) the name of the second player
    :param player_one_score: (string) the score of the first player
    :param player_two_score: (string) the score of the second player
    :return: game_outcome(string), a message of the outcome of the game.
    """
    if int(player_one_score) == int(player_two_score):
        #There is a tie
        game_outcome = "The result is a tie!\nFor both "+player_one_name+" and "+player_two_name+" the score is equal."
    elif int(player_one_score) > int(player_two_score):
        #Player_one has won this game
        game_outcome = player_one_name+" has won with: "+player_one_score+" points"
    elif int(player_one_score) < int(player_two_score):
        #Player_two has won this game
        game_outcome = player_two_name+" has won with: "+player_two_score+" points"
    else:
        game_outcome = "There is neither a tie nor "+player_one_name+" or "+player_two_name+" has won.\nSomething went wrong here...not sure what"
    return game_outcome
