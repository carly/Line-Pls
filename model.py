"""Models and database functions for Rap Genius for Shakespeare"""

from flask_sqlalchemy import SQLAlchemy
from correlation import pearson

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

scene_id = db.Column(db.Integer(4), autoincrement=True, primary_key=True) 
play_id = db.Column(db.String(50), db.ForeignKey('plays.play_id'), nullable=False) #default = ""? 
act = db.Column(db.Integer(4), nullable=False) #default = 0?
scene = db.Column(db.Integer(255), nullable=False) #default = 0?
description = db.Column(db.String(255), nullable=False) #default = ""?

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

char_id = db.Column(db.String(50), primary_key=True) #default = ""?
char_name = db.Column(db.String(255), nullable=False) #default = ""?
play_id = db.Column(db.String(255), db.ForeignKey('plays.title'), nullable=False) #default = ""?
description = db.Column(db.String(255), nullable=False) #default = ""?
mono_count = db.Column(db.Integer, nullable=True) #default?

#Defines relationship between Play class and Character Class

play = db.relationship("Play",
					   backref = db.backref("characters", order_by=char_id))

class Genre(db.Model):
	"""Genres of Shakespeare plays"""
#genre_ID (primary key) varchar(255) NOT NULL DEFAULT '',
#genre_name varchar(255) NOT NULL DEFAULT '',

__tablename 

class Monologue(db.Model):
	"""Shakespeare monologues"""
#mono_id (primary key) int(255) NOT NULL DEFAULT '0',
#play_id (foreign key - references Plays) varchar(255) NOT NULL DEFAULT '',
#char_id (foreign key - references Characters) varchar(255) NOT NULL DEFAULT '',
#text  text NOT NULL,
#scene_id (foreign key - references Scenes)
#character_count int(11) NOT NULL DEFAULT '0',
#word_cout int(11) NOT NULL DEFAULT '0',

class Play(db.Model):
	"""All the Shakespeare plays"""
#play_id (primary key) varchar(50) NOT NULL DEFAULT '',
#title varchar(255) NOT NULL DEFAULT '',
#long_tile varchar(255) NOT NULL DEFAULT '',
#date  int(11) NOT NULL DEFAULT '0',
#genre_type (foreign key - references Genre) varchar(255) NOT NULL DEFAULT ''

class User(db.Model):
	"""Users"""
#user_id
#youtube_google_login

class Annotations(db.Model):
	"""Comments on individual monologues by user"""
#note_id (primary key)
#mono_id(foreign key - referenes Monologues)
#comment_text
#user_id (foreign key- references Users)
#vote (1-like, 0-dislike)

class YoutubeVideo(db.Model):
	"""Youtube videos connected to Monologues"""
#video_id (primary key)
#mono_id (foreign key - references Monologues)
#user_id (foreign key - references Users)
#url 