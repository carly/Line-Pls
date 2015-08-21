"""Line Pls! Shakespeare Squad's up."""
import os
import json
import pprint
from flask_oauth2_login import GoogleLogin
from flask_login import LoginManager
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from model import Play, Scene, Genre, Character, Monologue, User, Comment, connect_to_db, db


app = Flask(__name__)
printer = pprint.PrettyPrinter()
app.secret_key = """Need to figure out"""
app.jinja_env.undefined = StrictUndefined
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

#Setup for Google Login using flask_oauth2_login
app.config.update(
  SECRET_KEY="GOOGLE_LOGIN_CLIENT_SECRET",
  GOOGLE_LOGIN_REDIRECT_SCHEME="http",
)
for config in (
  "GOOGLE_LOGIN_CLIENT_ID",
  "GOOGLE_LOGIN_CLIENT_SECRET",
):
  app.config[config] = os.environ[config]
google_login = GoogleLogin(app)

# Routes/Views

@app.route('/')
def index():
    """Renders homepage"""
    # this broke and i have no idea why
    return render_template("homepage.html")

#Login w/ Google API
@google_login.login_success
def login_success(token, profile):
    #Everything we want from the gmail JSON thats returned from the server
    user_gmail = profile["email"]
    user_firstname = profile["given_name"]
    user_pic = profile["picture"]

    # Looks for the the users in the db to see if email is registered in the db
    registered_user = User.query.filter(User.email==user_gmail).first()

    if registered_user:
        flash("Thanks %s. Welcome back. You are now logged in!" % (user_firstname))
    else:
        #if not in db, create a new user in the user db
        new_user = User(email=user_gmail, name=user_firstname, picture=user_pic)
        db.session.add(new_user)
        db.session.commit()
        flash("Thanks %s. You are now logged in!" % (user_firstname))

    session["email"] = user_gmail
    session["name"] = user_firstname
    session["pic"] = user_pic
    return redirect('/')

# if it doesn't work..
@google_login.login_failure
def login_failure(e):
    jsonify(error=str(e))
    return redirect('/')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Logs the current user out. Clears the session, redirects to homepage."""
    session.clear()
    return redirect('/')


# Non login related routes
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
	text = text.replace('[p]', '<br>').split('<br>')

	return render_template("monologue.html", mono_id=mono_id, name=name, play_title=play_title, act=act, scene=scene, description=description, text=text)

@app.route('/comments', methods=["POST"])
def store_comments():
    """Stores comments on monologues by line into db"""

    current_user_email = session["email"]

    current_user = User.query.filter(User.email==current_user_email).first()
    current_user_id = current_user.user_id

    comment_text = request.form.get("comment-text")
    mono_id = request.form.get("mono_id")
    line_id = request.form.get("line_id")
    user_id = current_user_id

    new_comment = Comment(line_id=line_id, mono_id=mono_id, comment_text=comment_text, user_id=user_id)
    db.session.add(new_comment)
    db.session.commit()

    return redirect('/monologue/' + str(mono_id))

@app.route('/shakespeare.json')
def create_shakespeare_json():
    """Creating json object that D3 needs to render to create force graph.

     Main function is defined in helper_functions.py"""
    genres = Genre.query.all()
    shakespeare = {}
    shakespeare["genre"] = [genre.json() for genre in genres]
    printer.pprint(shakespeare)
    return jsonify(shakespeare)





#Connecting server to db

if __name__ == "__main__":
	#debug=True for DebugToolbarExtension to work
	app.debug = True

	connect_to_db(app)

	#Use the DebugToolbar
	DebugToolbarExtension(app)
	print "\n\n\n\nYO\n\n\n"
	app.run()
