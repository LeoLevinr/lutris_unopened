#!/usr/bin/env python3
import sys
import os
import getpass
import sqlite3
from ruamel.yaml import YAML

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from modules import gui, ajout_nouveau_jeu

file_name = ""
app_id = ""
list_of_same_exe = [] # Will contain tuple that contains ID & the .yml file name.

game_yml = ""

# The app doesn't support multi-setups yet, so by priority will take the setup with the lowest ID -> the oldest one.

exe_path = str(sys.argv[1]) # Argument, give the executable path.

ajout_nouveau_jeu.Game_Exe = exe_path
print(ajout_nouveau_jeu.Game_Exe)

	# Lutris default folder path + give it to "ajout_nouveau_jeu"
lutris_default_folder = "/home/" + getpass.getuser() + "/.local/share/lutris"
ajout_nouveau_jeu.lutris_default_folder = lutris_default_folder

	# Folder path containing the games list in .yml - (Wont be the same path for flatpak users.)
lutris_yml_folder_path = lutris_default_folder + "/" + "games"




	 # Var containing every files in "lutris_yml_folder_path" 
games_files_folder = os.listdir(lutris_yml_folder_path)


for i in games_files_folder:
	yaml = YAML(typ='safe')


	with open(str(lutris_yml_folder_path + "/" + i)) as opened_lutris_yml_folder_path:
		game_yml = yaml.load(opened_lutris_yml_folder_path) # game_yml contains the info of the current .yml as a dict.

	the_supposed_same_path : dict = game_yml.get('game', {}).get("exe") # Will get the .exe path of the current .yml.

	if the_supposed_same_path == exe_path: #If the .exe's argument path is the same as one of the .yml, will get the .yml's' file name and put it in "file_name".
		file_name = i

	#using sqlite to read "pga.db".
		conn = sqlite3.connect(lutris_default_folder + "/" + "pga.db")
				 
		cursor = conn.cursor()
				 
		cursor.execute("SELECT * FROM games")
				 
		data = cursor.fetchall()  #List containing tuple, each tuple contains game info.


		conn.commit()
		cursor.close()
		conn.close()
	#### stop using sqlite to read "pga.db".

		for values in data: #Will check every tuples.
			if values[15] == file_name.replace(".yml",""): # Index 15 of the tuple correspond to game's .yml file name. 
				app_id = values[0] # Index 0 of the tuple correspond to the game's ID on Lutris.
				list_of_same_exe.append([app_id, values[15]])
				#print(list_of_same_exe)

if len(list_of_same_exe) == 1:
	os.system("env LUTRIS_SKIP_INIT=1 lutris lutris:rungameid/" + str(app_id))
elif len(list_of_same_exe) >= 1:
	print("Multi-setups aren't implemented yet.") # What happens if multiple setups have the same .exe.
else:

		# Will give an ID to the new game.
	conn = sqlite3.connect(lutris_default_folder + "/" + "pga.db")	 
	cursor = conn.cursor()
	cursor.execute("SELECT id FROM games")
				 
	data = cursor.fetchall() #List containing tuple, each tuple contains game info.

	#Give ID to the new game (in a janky way)
	ajout_nouveau_jeu.Game_ID = str(data[-1]).replace("(", "")
	ajout_nouveau_jeu.Game_ID = int(ajout_nouveau_jeu.Game_ID.replace(",)", "")) + 1
	#print(ajout_nouveau_jeu.Game_ID)

	conn.commit()
	cursor.close()
	conn.close()
		###

	gui.launch_app()
