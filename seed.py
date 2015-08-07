"""Utility file to seed monologues database from Open Source Shakespeare data text files."""

import csv
from model import Scene, Character, Monologue, Play, connect_to_db, db
#Genre is so small I'm just going to insert it manually 
#Annotations also needs to be created by hand since there is no data yet
from server import app


#Time to cook a database...
#______________________________________________________

def load_plays(file_name):
	"""Loads plays from Works.txt into database"""
	#play_id (primary key) [0]
	#title [1]
	#long_tile [2]
	#date  [3]
	#genre_type [4]
	
	#Uses python csv.reader function to parse data from txt file
	with open("file_name") as csvfile:
		playreader = csv.reader(csvfile, delimiter=',', quotechar='~')
		for row in playreader: 
			play_id = row[0]
			title = row[1]
			long_title = row[2]
			date = row[3]
			genre_id = row[4]
			
			#Connects data from Works.txt to variables in the plays table 
			play = Play(play_id=play_id, title=title, long_title=long_title, date=date, genre_id=genre_id)
			
			#Adds the play to the play table in the database. 
			db.session.add(play)
		db.session.commit()
	

def load_scenes(file_name):
	"""Loads scenes from Chapters.txt into database"""
	#Scene_ID (primary key) 
	#Play_ID (foreign key - references Plays) [0]
	#Act [2]
	#Scene [3]
	#Description [4]
	
	#Uses python csv.reader function to parse data from txt file
	with open("file_name") as csvfile:
		scenereader = csv.reader(csvfile, delimiter=',', quotechar='~')
		for row in scenereader:
			play_id = row[0]
			act = row[2]
			scene = row[3]
			s_description = row[4]
			
			#Connects data from Chapters.txt to variables in the scenes table 
			scene = Scene(play_id=play_id, act=act, scene=scene, s_description=s_description)
			
			#Adds the scene to the scenes table in the database. 
			db.session.add(scene)
		db.session.commit()
	
def load_characters(file_name):
	"""Loads characters from Characters.txt into database"""
	#char_ID (primary key) [0]
	#Char_name [1]
	#play_ID (foreign key - references Plays) [3]
	#description [4]
	#monologue_count [5]
	
	#Uses python csv.reader function to parse data from txt file
	with open("file_name") as csvfile:
		charreader = csv.reader(csvfile, delimiter=',', quotechar='~')
		for row in charreader:
			char_id = row[0]
			char_name = row[1]
			play_id = row[3]
			c_description = row[4]
			mono_count = row[5]
			
			#Connects data from Chapters.txt to variables in the scenes table 

def load_monologues(file_name):
	##HOLDING OFF ON THIS ONE UNTIL SOMEONE ANSWERS MY QUESTION
	"""Loads monologues from Paragraphs.txt into database"""
	#mono_id (primary key) 
	#play_id (foreign key - references Plays) [0]
	#char_id (foreign key - references Characters)[3]
	#text [4]
	#act_id (foreign key - references Scenes) [8]
	#scene_id (foreign key - references Scenes) [9]
	#character_count [10]
	#word_count [11]
	pass
	
