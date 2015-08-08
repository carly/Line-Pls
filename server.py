"""Rap Genius for Shakespeare"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Still need to figure out API keys..

app.secret_key = """Need to figure out"""

#Prevents undefined variables in Jinja2 from failing silently.
# The line below makes jinja raise an error if undefined.

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
	"""Homepage."""
	pass

@app.route('/plays')
def show_plays():
	"""List of Shakespeare Plays"""
	pass

@app.route('/monologue')
def show_monologue():
	"""Shows the chosen monologue + ability to make annotations view"""
	pass
	


#Connecting server to db

if __name__ == "__main__":
	#debug=True for DebugToolbarExtension to work
	app.debug = True
	
	connect_to_db(app)
	
	#Use the DebugToolbar
	DebugToolbarExtension(app)
	print "\n\n\n\nYO\n\n\n"
	app.run()
	