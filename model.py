"""Models and database functions for Rap Genius for Shakespeare"""

from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from werkzeug import generate_password_hash, check_password_hash

#This is the connection to the SQlite database that we get through the Flask-SQLAlchemy helper library. On this, we can find the 'session' object where we do most of the interactions (committing etc.)

db = SQLAlchemy()

###########################################################
# Model definitions: Scenes Character, Genre, Monologue, Play, User, Annotations, Youtube]

## Instead of doing this.... write a function that switches out the genre id with the genre type when you load the plays


# Fix me
class Genre(db.Model):
	"""Genres of Shakespeare plays"""

	__tablename__="genres"

	genre_id = db.Column(db.String(255), primary_key=True)
	genre_name = db.Column(db.String(255), default=" ", nullable=False)

	def json(self):
		genre = {}
		if self.genre_id in ['c', 'h', 't']:
			genre["genre_id"] = self.genre_id
		genre["genre_name"] = self.genre_name
		# If I leave in plays, I might be able use this to create the links function...
		genre["plays"] = [play.json() for play in self.plays]
		genre["count"] = len(self.plays)
		return genre


class Play(db.Model):
	"""All the Shakespeare plays"""

	__tablename__="plays"

	play_id = db.Column(db.String(50), primary_key=True)
	title = db.Column(db.String(255), default=" ", nullable=False)
	long_title = db.Column(db.String(255), default=" ", nullable=False)
	date = db.Column(db.Integer, default=0, nullable=False)
	genre_id = db.Column(db.String(255), db.ForeignKey('genres.genre_id'), default=" ", nullable=False)

	#Defines relationship between Play class and Genre class
	genre = db.relationship("Genre",
							backref = db.backref("plays", order_by=play_id))

	def json(self):
		play = {}
		play["play_id"] = self.play_id
		play["title"] = self.title
		play["long_title"] = self.long_title
		play["date"] = self.date
		if self.genre_id in ['c', 'h', 't']:
			play["genre_id"] = self.genre_id
		return play


class Scene(db.Model):
	"""Shakespeare plays divided into Scenes"""

	__tablename__ = "scenes"

	scene_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	play_id = db.Column(db.String(50), db.ForeignKey('plays.play_id'), default=" ", nullable=False)
	act = db.Column(db.Integer, default=0,  nullable=False)
	scene = db.Column(db.Integer,default=0, nullable=False)
	s_description = db.Column(db.String(255), default=" ", nullable=False)

	#Defines relationship between Play class and Scene class
	play = db.relationship("Play",
						   backref = db.backref("scenes", order_by=scene_id))

	# I think I'm done with this but might not be
	def json(self):
		scene = {}
		scene["scene_id"] = self.scene_id
		scene["play_id"] = self.play_id
		scene["act"] = self.act
		scene["scene"] = self.scene
		scene["description"] = self.s_description
		return scene


class Character(db.Model):
	"""Shakespeare characters"""

	__tablename__ = "characters"

	char_id = db.Column(db.String(50), primary_key=True)
	char_name = db.Column(db.String(255),default=" ", nullable=False)
	play_id = db.Column(db.String(255), db.ForeignKey('plays.play_id'), default=" ", nullable=False)
	c_description = db.Column(db.String(255),default=" ", nullable=False)
	mono_count = db.Column(db.Integer, default=0, nullable=True)

	#Defines relationship between Play class and Character Class
	play = db.relationship("Play",
						   backref = db.backref("characters", order_by=char_id))

	def json(self):
		character = {}
		character["char_id"] = self.char_id
		character["name"] = self.char_name
		character["play_id"] = self.play_id
		if len(self.c_description) > 10:
			character["bio"] = self.c_description
		if len(self.monologues) > 0:
			character["mono_count"] = len(self.monologues)
		# I don't know why this isn't working...
		character["monologues"] = [monologue.json() for monologue in self.monologues]
		return character


class Monologue(db.Model):
	"""Shakespeare monologues"""

	__tablename__="monologues"

	mono_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	play_id = db.Column(db.String(255), db.ForeignKey('plays.play_id'), default=" ", nullable=False)
	char_id = db.Column(db.String(255), db.ForeignKey('characters.char_id'), default=" ", nullable=False)
	text = db.Column(db.Text, nullable=False)
	act_id = db.Column(db.Integer, default=0,  nullable=False)
	scene_id = db.Column(db.Integer, default=" ", nullable=False)
	char_count = db.Column(db.Integer, default=0, nullable=False)
	word_count = db.Column(db.Integer, default=0, nullable=False)

	#Defines relationship between Play Class & Monologue Class
	play = db.relationship("Play",
						   backref = db.backref("monologues", order_by=mono_id))

	#Defines relationship between Character Class & Monologue Class
	character = db.relationship("Character",
							   backref = db.backref("monologues", order_by=mono_id))

	def json(self):
		monologue = {}
		monologue["mono_id"] = self.mono_id
		monologue["play_id"] = self.play_id
		monologue["char_id"] = self.char_id
		monologue["act_id"] = self.act_id
		monologue["scene_id"] = self.scene_id
		monologue["word_count"] = self.word_count
		monologue["comments"] = [comment.json() for comment in self.comments]
		monologue["comment_count"] = len(self.comments)
		return monologue

class User(db.Model):
	"""Stores users in the database"""
	__tablename__="users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(255), default=" ", nullable=False)
	username = db.Column(db.String(255), default=" ", nullable=False)
	pwdhash = db.Column(db.String(300))
	picture = db.Column(db.String(500), default=" ", nullable=True)
	name = db.Column(db.String(100), default=" ", nullable="true")
	bio = db.Column(db.String(500), default=" ", nullable="true")
	website = db.Column(db.String(300), default=" ", nullable="true")
	twitter = db.Column(d)

	def __init__(self, username, email, password):
		self.username = username.lower()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def json(self):
		user = {}
		user["user_id"] = self.user_id
		user["username"] = self.username
		user["comments"] = [comment.json() for comment in self.comments]
		user["count"] = len(self.comments)
		return user


class Comment(db.Model):
	"""Stores lines with user commentary/annotations in database."""

	__tablename__="comments"

	comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	line_id = db.Column(db.Integer, nullable="false")
	mono_id = db.Column(db.Integer, db.ForeignKey('monologues.mono_id'), nullable=False)
	comment_text = db.Column(db.Text, default=" ", nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), default=0, nullable=True)

	#Defines relationship between Comments made on Monologues
	monologue = db.relationship("Monologue",
							backref= db.backref("comments", order_by=comment_id))
	#Defines relationship between Comments and Users
	user = db.relationship("User",
							backref= db.backref("comments", order_by=comment_id))

	def json(self):
		comment = {}
		comment["comment_id"] = self.comment_id
		comment["line_id"] = self.line_id
		comment["mono_id"] = self.mono_id
		comment["comment_text"] = self.comment_text
		comment["user_id"] = self.user_id
		return comment



###########################################################################
# Hold off on this until we figure out YoutubeAPI
#class YoutubeVideo(db.Model):
#	"""Youtube videos connected to Monologues"""
#	#video_id (primary key)
#	#mono_id (foreign key - references Monologues)
#	#user_id (foreign key - references Users)
#	#url
#	__tablename__="youtube_videos"

###########################################################################



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/monologues'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
