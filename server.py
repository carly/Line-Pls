"""Rap Genius for Shakespeare"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Play, Scene, Character, Monologue, connect_to_db, db

app = Flask(__name__)

# Still need to figure out API keys..

app.secret_key = """Need to figure out"""

#Prevents undefined variables in Jinja2 from failing silently.
# The line below makes jinja raise an error if undefined.

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
	"""Homepage."""
	return render_template("homepage.html") 

@app.route('/plays')
def play_list():
	"""Show list of all the Shakespeare Plays in the database"""
	
	plays = Play.query.order_by(Play.title).all()
	return render_template("play_list.html", plays=plays)

@app.route('/plays/<string:play_id>')
def play_details(play_id):
	"""Displays information about the play"""
	
	play_object = Play.query.filter(Play.play_id==play_id).first()
	
	title = play_object.title
	long_title = play_object.long_title 
	date = play_object.date
	genre = play_object.genre_id
	
	characters = Character.query.filter(Character.play_id==play_id).all()
	
	return render_template("play_details.html", title=title, long_title=long_title, date=date, genre=genre, characters=characters)
  

@app.route('/characters/<string:char_id>')
def show_character(char_id):	
	"""Lists the Character description and links to Monologues"""
	
	char_object = Character.query.filter(Character.char_id==char_id).first()
	
	name = char_object.char_name
	play = char_object.play_id
	c_description = char_object.c_description
	
	monologues = Monologue.query.filter(Monologue.char_id==char_id).all()

	
	return render_template("character.html", name=name, play=play, c_description=c_description, monologues=monologues)
	

@app.route('/monologue/<int:mono_id>')
def monologue_notes():
	"""Shows the chosen monologue + ability to make annotations view"""
	
	pass
#	mono_object = Monologue.query.filter(Monologue.mono_id == mono_id).first()
#	
#	mono_id = mono_object.mono_id
#	play_id = mono_object.play_id
#	char_id = mono_object.char_id
#	text = 
#	#Connects data from Paragraphs.txt to variables in the monologues table 
#				monologue = Monologue(play_id=play_id, char_id=char_id, text=text, act_id=act_id, scene_id=scene_id, char_count=char_count, word_count=word_count)
#	


#Connecting server to db

if __name__ == "__main__":
	#debug=True for DebugToolbarExtension to work
	app.debug = True
	
	connect_to_db(app)
	
	#Use the DebugToolbar
	DebugToolbarExtension(app)
	print "\n\n\n\nYO\n\n\n"
	app.run()
	