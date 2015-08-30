"""Models and database functions for Line Pls """

############################################################
##########               IMPORTS                 ###########
############################################################

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

#############################################################
############        DB to SQLAlchemy             ############
#############################################################

db = SQLAlchemy()

##############################################################
##########       DEFINE MODEL CLASSES FOR DB   ###############
##############################################################

##############################################################
#####   MODELS RELATED TO STORAGE OF PLAYS/MONOLOUGES  #######
##############################################################

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


#######################################################################
########## DEFINE MODELS RELATED TO STORING USER INFO   ###############
#######################################################################

class User(db.Model):
	"""Stores users in the database"""
	__tablename__="users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(255), default=" ", nullable=False)
	username = db.Column(db.String(255), default=" ", nullable=False)
	pwdhash = db.Column(db.String(300))
	picture = db.Column(db.String(500), default=" ", nullable=True)
	name = db.Column(db.String(100), default=" ", nullable=True)
	bio = db.Column(db.String(500), default=" ", nullable=True)
	website = db.Column(db.String(300), default=" ", nullable=True)
	twitter = db.Column(db.String(60), default=" ", nullable=True)
	resume = db.Column(db.String(300), default=" ", nullable=True)

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
		user["name"] = self.name
		user['bio'] = self.bio
		user['twitter'] = self.twitter
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

class Youtube(db.Model):
	"""Youtube videos connected to Monologues"""

	__tablename__="youtube"

	youtube_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	mono_id = db.Column(db.Integer, db.ForeignKey('monologues.mono_id'), nullable=False)
	youtube_key = db.Column(db.String(100), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), default=0, nullable=True)
	username = db.Column(db.String(100), default=" ", nullable=True)

	# Define relationship between youtube videos and monologues
	monologue = db.relationship("Monologue",
							backref= db.backref("youtube", order_by=youtube_id))

	# Define relationship between youtube videos and associated Users
	user = db.relationship("User",
							backref=db.backref("youtube", order_by=youtube_id))


class Follower(db.Model):
	"""Displays followers of a particular user"""
	__tablename__="followers"

	f_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	# Followed
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	# Follower
	follower = db.Column(db.String(200), default=" ", nullable=False)

	user = db.relationship("User",
						backref= db.backref("followers", order_by=f_id))


class UserVid(db.Model):
	"""stores videos of user performances to be displayed on profile pages."""
	__tablename__="uservids"

	uv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	uv_key = db.Column(db.String(100), nullable=False)

	#Define relationship between UserVids and Users
	user = db.relationship("User",
						backref=db.backref("uservids", order_by=uv_id))


class Reel(db.Model):
	"""Stores performer reels to be displayed on profile pages."""
	__tablename__="reels"

	r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
	reel_key = db.Column(db.String(100), nullable=False)

	#Define relationship between Reels and Users
	user = db.relationship("User",
						backref=db.backref("reels", order_by=r_id))



#####################################################################
##########         MODEL Helper functions    ########################
#####################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost/monologues'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
