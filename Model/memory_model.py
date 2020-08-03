"""
This program will have methods able to load in a database(.json) file
in which the user can change settings of the board and stuff.
"""
import json
from pathlib import Path

database_path = "/home/cole/.memory_game_settings"

def is_database_initialized():
    #check whether the database has been made. If not, create it.
    file_location = Path(database_path)
    if file_location.is_file():
        #the database exists, resume program.
        print("An existing database has been found")
        return
    else:
        #create database
        print("No data found\nInitialize database")
        setup_database()
        return

def setup_database():
    #in this method a .json file will me made which will serve as a database.
    memory_statistics = {"game_settings":{
        "playfield_size": "4",
        "player_one_name": "Player 1",
        "player_two_name": "Player 2",
        "game_card_names": ["fish","cat","tiger","moon","sun","lion","river","ocean","peanut","elephant","monkey", "dolphin","jaguar",
                            "sand","tundra","hyena","treasure","diamond","ruby","emerald","potasium","camel","horse","leaf","knight",
                            "king","emperor","ocean","sea","boat","pirate","ninja","tree"]
    }, "game_statistics":{
        "started_games": 0,
        "finished_games": 0
    }}
    with open(database_path, "w") as output_file:
        json.dump(memory_statistics, output_file)

def get_database():
    #in this method a .json file will loaded in and it's contents will be returned.
    json_file = open(database_path, "r")
    memory_statistics = json.load(json_file)
    return memory_statistics

def write_away_database(database):
    outputfile = open(database_path, "w")
    json.dump(database, outputfile)

def get_game_statistic(key):
    memory_statistics = get_database()
    try:
        statistic = memory_statistics["game_statistics"][key]
        print("The amount of " + str(key) + " has been retrieved")
        return statistic
    except KeyError:
        print("The key: "+str(key)+" is not available in the game statistics")

def get_game_setting(key):
    memory_statistics = get_database()
    try:
        setting = memory_statistics["game_settings"][key]
        print("The game setting: "+key+" has been retrieved")
        return setting
    except KeyError:
        print("The key: "+str(key)+" is not available in the game settings")

def update_game_statistics(key):
    # Read in the database(.json file), do plus one to a game statistic(started or finished game) and write away the database.
    memory_statistics = get_database()
    try:
        memory_statistics["game_statistics"][str(key)] += 1
        write_away_database(memory_statistics)
    except KeyError:
        print("The key: "+str(key)+" is not available in the game settings")
        return

def update_game_settings(key, updated_value):
    # Read in the database(.json file), change a game setting and write away the database.
    memory_statistics = get_database()
    try:
        memory_statistics["game_settings"][str(key)] = str(updated_value)
        write_away_database(memory_statistics)
    except KeyError:
        print("The key: "+str(key)+" is not available in the game statistics")
        return
