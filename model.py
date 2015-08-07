"""Models and database functions for Rap Genius for Shakespeare"""

from flask_sqlalchemy import SQLAlchemy

#This is the connection to the SQlite database that we get through thte Flask-SQLAlchemy helper library. On this, we can find the 'session' object where we do most of the interactions (committing etc.)

db = SQLAlchemy()

###########################################################
# Model definitions: Scenes Character, Genre, Monologue, Play, User, Annotations, Youtube]


class Scene(db.Model):
	"""Shakespeare plays divided into Scenes"""
	#Scene_ID (primary key)
	#Play_ID (foreign key - references Plays)
	#Act
	#Scene
	#Description

	__tablename__ = "scenes"

	scene_id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
	play_id = db.Column(db.String(50), db.ForeignKey('plays.play_id'), default=" ", nullable=False)
	act = db.Column(db.Integer, default=0,  nullable=False)
	scene = db.Column(db.Integer,default=0, nullable=False)
	description = db.Column(db.String(255), default=" ", nullable=False)
	
	#Defines relationship between Play class and Scene class
	play = db.relationship("Play",
						   backref = db.backref("scenes", order_by=scene_id))


class Character(db.Model):
	"""Shakespeare characters"""
	#char_ID (primary key) varchar(50) NOT NULL DEFAULT '',
	#Char_name varchar(255) NOT NULL DEFAULT '',
	#play_ID(foreign key - references Plays) varchar(255) NOT NULL DEFAULT '',
	#description varchar(255) NOT NULL DEFAULT ''
	#monologue_count mediumint(9) DEFAULT NULL

	__tablename__ = "characters"

	char_id = db.Column(db.String(50), primary_key=True) 
	char_name = db.Column(db.String(255),default=" ", nullable=False) 
	play_id = db.Column(db.String(255), db.ForeignKey('plays.play_id'), default=" ", nullable=False) 
	description = db.Column(db.String(255),default=" ", nullable=False) 
	mono_count = db.Column(db.Integer, default=0, nullable=True) 

	#Defines relationship between Play class and Character Class
	play = db.relationship("Play",
						   backref = db.backref("characters", order_by=char_id))

class Genre(db.Model):
	"""Genres of Shakespeare plays"""
	#genre_ID (primary key) varchar(255) NOT NULL DEFAULT '',
	#genre_name varchar(255) NOT NULL DEFAULT '',

	__tablename__="genres"

	genre_id = db.Column(db.String(255), primary_key=True) 
	genre_name = db.Column(db.String(255), default=" ", nullable=False)


class Monologue(db.Model):
	"""Shakespeare monologues"""
	#mono_id (primary key) int(255) NOT NULL DEFAULT '0',
	#play_id (foreign key - references Plays) varchar(255) NOT NULL DEFAULT '',
	#char_id (foreign key - references Characters) varchar(255) NOT NULL DEFAULT '',
	#text  text NOT NULL,
	#scene_id (foreign key - references Scenes)
	#character_count int(11) NOT NULL DEFAULT '0',
	#word_cout int(11) NOT NULL DEFAULT '0',

	__tablename__="monologues"

	mono_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	play_id = db.Column(db.String(255), db.ForeignKey('plays.play_id'), default=" ", nullable=False) 
	char_id = db.Column(db.String(255), db.ForeignKey('characters.char_id'), default=" ", nullable=False) 
	text = db.Column(db.Text, nullable=False)
	scene_id = db.Column(db.Integer, db.ForeignKey('scenes.scene_id'), default=" ", nullable=False)
	char_count = db.Column(db.Integer, default=" ", nullable=False)
	word_count = db.Column(db.Integer, default=" ", nullable=False)
	
	#Defines relationship between Play Class & Monologue Class
	play = db.relationship("Play",
						   backref = db.backref("monologues", order_by=mono_id))
	
	#Defines relationship between Character Class & Monologue Class
	character = db.relationship("Character",
							   backref = db.backref("monologues", order_by=mono_id))
	
	#Defines relationship between Scene Class & Monologue Class
	scene = db.relationship("Scene",
						   backref = db.backref("monologues", order_by=mono_id))
	
	

class Play(db.Model):
	"""All the Shakespeare plays"""
	#play_id (primary key) varchar(50) NOT NULL DEFAULT '',
	#title varchar(255) NOT NULL DEFAULT '',
	#long_tile varchar(255) NOT NULL DEFAULT '',
	#date  int(11) NOT NULL DEFAULT '0',
	#genre_type (foreign key - references Genre) varchar(255) NOT NULL DEFAULT ''

	__tablename__="plays"

	play_id = db.Column(db.String(50), primary_key=True) 
	title = db.Column(db.String(255), default=" ", nullable=False) 
	long_title = db.Column(db.String(255), default=" ", nullable=False) 
	date = db.Column(db.Integer, default=0, nullable=False)
	genre_type = db.Column(db.String(255), db.ForeignKey('genres.genre_id'), default=" ", nullable=False)
	
	genre = db.relationship("Genre",
						   backref = db.backref("plays", order_by=play_id))

##########################################################################
# Hold off on this until we figure out Google Login
#class User(db.Model):
#	"""Users"""
#	#user_id
#	#youtube_google_login
#	__tablename__="users"
#
#	## Until I figure out the api I can't really do this
#	#user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#	#username = db.Column(db.)
###########################################################################


class Annotation(db.Model):
	"""Annotations on individual monologues by user"""
	#note_id (primary key)
	#mono_id(foreign key - referenes Monologues)
	#note_text
	#user_id (foreign key- references Users)
	#vote (1-like, 0-dislike)
	__tablename__="annotations"

	note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	mono_id = db.Column(db.Integer, db.ForeignKey('monologues.mono_id'), default=" ", nullable=False) 
	note_text = db.Column(db.String(500), default=" ", nullable=False) 
#	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False) #default?
	vote = db.Column(db.Integer, default=0, nullable=True) 

	#Define relationship between Annotation Class & Monologues Class
	monologue = db.relationship("Monologue",
							   backref = db.backref("monologues", order_by=mono_id))


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