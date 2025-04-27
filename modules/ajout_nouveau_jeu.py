from datetime import datetime
import os
import yaml
import sqlite3


#Prints date in Unix Epoch format (numbers at the end of .yml files)
print(int(datetime.now().timestamp()))

lutris_default_folder = ""  #main.py will give the info.
Game_ID : int #main.py will give the info.

Game_Exe : str #main.py will give the info.

Game_Name = ""

future_game_name = "" #Contains the game name in lowercase snake-case.
game_unix_installation_time = ""  #Will contain game installation date in Epoch
future_game_config_path = "" #Will contain the config_path of the game.

def add_new_game(Game_Name, Wine_Prefix, Wine_Version):

	#Name the .yml file of the new game.
	future_game_file_name = Game_Name.replace(" ", "-")
	future_game_file_name = future_game_file_name.lower()

	future_game_name = future_game_file_name

	game_unix_installation_time = int(datetime.now().timestamp())


	future_game_file_name = future_game_file_name + "-" + str(game_unix_installation_time)

	future_game_config_path = future_game_file_name

	future_game_file_name = future_game_file_name + ".yml"

	print(future_game_file_name)
	###

	game_data = {}

	game_data  = {
		"game": {
			"exe": Game_Exe,
			"prefix": Wine_Prefix

		}
	}

	if Wine_Version != "Default":
		game_data["game"]["wine"] = Wine_Version


	print(game_data)

	with open(lutris_default_folder + "/" + "games" + "/" + future_game_file_name, "w") as file:
		yaml.dump(game_data, file)

	print("The .yml file has been created.") 

	#Insert the new game in the pga.db file.
		#using sqlite to read "pga.db".
	conn = sqlite3.connect(lutris_default_folder + "/" + "pga.db")
			 
	cursor = conn.cursor()
	print(Game_ID)
	cursor.execute("INSERT INTO games (id, name, slug, platform, runner, installed, installed_at, configpath) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (int(Game_ID), str(Game_Name), str(future_game_name), 'Windows', 'wine', '1', float(game_unix_installation_time), str(future_game_config_path)))
			 
	data = cursor.fetchall() #List containing tuple, each tuple contains game info.

	conn.commit()
	cursor.close()
	conn.close()
		#### stop using sqlite to read "pga.db".

	os.system("env LUTRIS_SKIP_INIT=1 lutris lutris:rungameid/" + str(Game_ID)) #Launch the game
