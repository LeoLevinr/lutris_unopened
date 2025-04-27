import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from urllib.parse import urlparse, unquote
import sys
import os

import modules.ajout_nouveau_jeu as ajout_nouveau_jeu

sys.path.insert(0, "/usr/lib/python3/dist-packages/lutris/util/wine/") #Where Lutris is located, used to get a list of installed wine versions, flatpak Lutris isn't implemented yet.
import wine

#print(wine.get_installed_wine_versions())

Game_Name = "" #Contains the game name chosen by the user after that the confirm button was pressed.
wine_prefix = "" #Contains the wine prefix chosen by the user after that the confirm button was pressed.
wine_version = ""

builder = Gtk.Builder()
builder.add_from_file('interface.glade')

window = builder.get_object('main_window')

game_name_entry = builder.get_object('game_name_entry')
wine_prefix_folder_chooser = builder.get_object('wine_prefix_folder_chooser')


#Function called if the confirm button was pressed.
def confirm_button_has_been_clicked(self):
	#Will get the game name, the wine prefix and the wine version.

	print("confirm_button has been clicked")

		#Get what the user wrote in "Game Name"
	Game_Name = game_name_entry.get_text()
		###


		#Get which wine prefix the user chose.
	wine_prefix = wine_prefix_folder_chooser.get_current_folder_uri()
	wine_prefix = unquote(urlparse(wine_prefix).path) #Convert the URI path in Unix path.
		###

		 #Get which wine version the user chose.
	wine_version =  wine_version_combo_box.get_active_text()
		###

	Gtk.main_quit() #Close the window after the confirm button was pressed.


	ajout_nouveau_jeu.add_new_game(Game_Name, wine_prefix, wine_version)
	print("Nom du Jeu : " + Game_Name)
	print("Prefix Wine : " + wine_prefix)
	print("Version Wine : " + wine_version)
###

	#Get + add the wine versions in "wine_version_combo_box".
wine_version_combo_box = builder.get_object("wine_version_combo_box")
wine_versions = wine.get_installed_wine_versions()
wine_version_combo_box.append_text("Default",) #Add the "Default" option.
wine_version_combo_box.set_active(0)
for i in wine_versions:
	wine_version_combo_box.append_text(i)
	###


	#Confirm button
confirm_button = builder.get_object('confirm_button')
confirm_button.connect("clicked", confirm_button_has_been_clicked)
	###

	#Cancel button
cancel_button = builder.get_object('cancel_button')
cancel_button.connect("clicked", Gtk.main_quit)
	###

def launch_app(): #So it can be launched via an external script.
	window.connect('delete-event', Gtk.main_quit)
	window.show_all()
	Gtk.main()



