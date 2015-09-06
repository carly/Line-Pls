"""Utility file to seed monologues database from Open Source Shakespeare data text files."""

## SEED IMPORTS

import csv
from model import Scene, Character, Monologue, Play, Genre, connect_to_db, db
from server import app

##  Defines functions that parse data from Open Source Shakespeare db text files
def load_genres(file_name):
	"""Loads genres into db."""

	file_obj = open(file_name)
	for line in file_obj:
		row = line.split(" ")
		genre_id = row[0]
		genre_name = row[1].rstrip()

		#Connects data from Genres.txt to variables in the genre table
		genre = Genre(genre_id=genre_id, genre_name=genre_name)

		#Adds the Genre to the genres table in the database.
		db.session.add(genre)
	db.session.commit()


def load_plays(file_name):
	"""Loads plays from Works.txt into database"""

	#Uses python csv.reader function to parse data from txt file
	with open(file_name) as csvfile:
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

	#Uses python csv.reader function to parse data from txt file
	with open(file_name) as csvfile:
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

	#Uses python csv.reader function to parse data from txt file
	with open(file_name) as csvfile:
		charreader = csv.reader(csvfile, delimiter=',', quotechar='~')
		for row in charreader:
			char_id = row[0]
			char_name = row[1]
			play_id = row[3]
			c_description = row[4]
			mono_count = row[5]

			#Connects data from Characters.txt to variables in the characters table
			character = Character(char_id=char_id, char_name=char_name, play_id=play_id, c_description=c_description, mono_count=mono_count)

			#Adds the character to the characters table in the database.
			db.session.add(character)
		db.session.commit()


def load_monologues(file_name):
	"""Loads monologues from Paragraphs.txt into database"""

	#Uses python csv.reader function to parse data from txt file
	with open(file_name) as csvfile:
		monoreader = csv.reader(csvfile, delimiter=',', quotechar='~')
		for row in monoreader:
			word_count = int(row[11])
			if word_count >= 100:
				print "greater than 100!"
				print type(row[11])
				print row[11]
				play_id = row[0]
				char_id = row[3]
				text = row[4]
				print text
				act_id = row[8]
				scene_id = row[9]
				char_count = row[10]
				word_count = row[11]


			#Connects data from Paragraphs.txt to variables in the monologues table
				monologue = Monologue(play_id=play_id, char_id=char_id, text=text, act_id=act_id, scene_id=scene_id, char_count=char_count, word_count=word_count)

			#Adds the monologue to the monologues table in the database.
				db.session.add(monologue)
			db.session.commit()



##############     Time to cook a database...        ###############

if __name__=="__main__":
	connect_to_db(app)

	load_genres("oss-textdb/Genres.txt")
	load_plays("oss-textdb/Works.txt")
	load_scenes("oss-textdb/Chapters.txt")
	load_characters("oss-textdb/Characters.txt")
	load_monologues("oss-textdb/Paragraphs.txt")
