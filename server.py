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
	
	#Lists all the plays as links right now
	plays = Play.query.order_by(Play.title).all()
	return render_template("play_list.html", plays=plays)


@app.route('/plays/<string:play_id>')
def play_details(play_id):
	"""Shows play details, including a list of characters with links to all their monologues"""
	
	# Gets all the info from the db for the play requested by user
	play_object = Play.query.filter(Play.play_id==play_id).first()
	
	title = play_object.title
	long_title = play_object.long_title 
	date = play_object.date
	genre = play_object.genre_id
	
	# Gets all the info we need from the Characters table to be able to display all their monologues 
	characters = Character.query.filter(Character.play_id==play_id).all()
	
	return render_template("play_details.html", title=title, long_title=long_title, date=date, genre=genre, characters=characters)
  

@app.route('/characters/<string:char_id>')
def show_character(char_id):	
	"""Lists the Character description and links to Monologues"""
	
	#Gets all the info we need from the Characters table
	#Fix me
	char_object = Character.query.filter(Character.char_id==char_id).first()
	
	#Fix me
	#Add act, scene, and scene descriptions for each monologue
	name = char_object.char_name
	play = char_object.play_id
	c_description = char_object.c_description
	
	#Fix me 
	#For some reason the for loop isn't displaying all the monologues..
	monologues = Monologue.query.filter(Monologue.char_id==char_id).all()

	return render_template("character.html", name=name, play=play, c_description=c_description, monologues=monologues)
	

@app.route('/monologue/<int:mono_id>')
def show_monologue(mono_id):
	"""Shows the chosen monologue + ability to make annotations view"""
	
	# Gets all the info we need from the Monologues Table
	mono_object = Monologue.query.filter(Monologue.mono_id==mono_id).first()
	#character, play, text, act, scene, scene description
	#these are only here to access the things we need from the Play/Characters tables
	char_id = mono_object.char_id
	play_id = mono_object.play_id
	scene = mono_object.scene_id
	
	# Gets all the info we need from the Play, Scene, and Character tables using values pulled from the Monologue table
	play_object = Play.query.filter(Play.play_id==play_id).first()
	scene_object = Scene.query.filter(Scene.scene_id==scene).first()
	char_object = Character.query.filter(Character.char_id==char_id).first()
	
	#Everything going into the view.. + scene, which we use up there to get the description
	mono_id = mono_object.mono_id
	text = mono_object.text
	act = mono_object.act_id
	description = scene_object.s_description
	play_title = play_object.title
	name = char_object.char_name
	
	return render_template("monologue.html", mono_id=mono_id, name=name, play_title=play_title, act=act, scene=scene, description=description, text=text)



#Connecting server to db

if __name__ == "__main__":
	#debug=True for DebugToolbarExtension to work
	app.debug = True
	
	connect_to_db(app)
	
	#Use the DebugToolbar
	DebugToolbarExtension(app)
	print "\n\n\n\nYO\n\n\n"
	app.run()
	