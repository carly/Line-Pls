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
from model import Play, Scene, Genre, Character, Monologue, User, Comment, Youtube, connect_to_db, db
from helper_functions import shakespeare_data
from forms import SignupForm, SigninForm, YoutubeForm



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


# @app.route('/login')
# def index():
#     """Login Page"""
#     return render_template("login.html")
#
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """A form to signup and create an account."""
    form = SignupForm(request.form)

    if 'username' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST' and form.validate():
            new_user = User(username=form.username.data,email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            # flash('Welcome to the ensemble!')
            return redirect(url_for('profile'))

            session['email'] = new_user.email
            session['username'] = new_user.username
            return redirect(url_for('profile'))

    return render_template('signup.html', form=form)

@app.route('/signin', methods=["GET", "POST"])
def signin():
    form = SigninForm(request.form)

    if 'username' in session:
        return redirect(url_for('profile'))

    if request.method == "POST":
        if form.validate()==False:
            return render_template('signin.html', form=form)
        else:
            session['username']= form.username.data
            user = User.query.filter(User.username==form.username.data.lower()).first()
            session['email']= user.email
            session['id'] = user.user_id
            return redirect(url_for('profile'))

    elif request.method == "GET":
        return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

    if 'username' not in session:
        return redirect(url_for('signin'))

    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    """Renders user's profile page."""

    if 'username' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter(User.username==session['username']).first()

    if user is None:
        return redirect(url_for('signup'))
    else:
        return render_template('profile.html')

@app.route('/search')
def search():
    """Renders search page."""

    return render_template('search.html')

@app.route('/account')
def account():
    """renders account form."""
    # Since we already have these values in session, we wont' include in db query.
    email = session['email']
    username = session['username']

    # Query db so we can populate account form with current db values for user
    user = User.query.filter(User.username==username).first()
    if user is not None:
        name = user.name
        bio = user.bio
        web = user.website
        twitter = user.twitter
    else:
        name = ""
        bio = ""
        web = ""
        twitter = ""
    return render_template('myaccount.html', name=name, bio=bio, web=web, twitter=twitter)

@app.route('/update_profile', methods=["POST"])
def update_profile():
    """Change user info in db if the user changes the basic information form."""
    print request.form
    new_name = request.form.get("name")
    new_email = request.form.get("email")
    new_username = request.form.get("username")
    new_bio = request.form.get("bio")
    new_website = request.form.get("web")
    new_twitter = request.form.get("twitter")
    print new_bio

    user_id = session["id"]
    # Updates user info in database
    #
    user = User.query.filter(User.user_id==user_id).first()

    if user is not None:
        user.name = new_name
        user.email= new_email
        user.username = new_username
        user.bio= new_bio
        user.website= new_website
        user.twitter= new_twitter

    db.session.commit()
    return redirect(url_for('account'))


#Login w/ Google API
# @google_login.login_success
# def login_success(token, profile):
    #Everything we want from the gmail JSON thats returned from the server
    # user_gmail = profile["email"]
    # user_firstname = profile["given_name"]
    # user_pic = profile["picture"]

    # Looks for the the users in the db to see if email is registered in the db
    # registered_user = User.query.filter(User.email==user_gmail).first()
    #
    # if registered_user:
    #     flash("Thanks %s. Welcome back. You are now logged in!" % (user_firstname))
    # else:
        #if not in db, create a new user in the user db
    #     new_user = User(email=user_gmail, name=user_firstname, picture=user_pic)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     flash("Thanks %s. You are now logged in!" % (user_firstname))
    #
    # session["email"] = user_gmail
    # session["name"] = user_firstname
    # session["pic"] = user_pic
    # return redirect('/')

# if it doesn't work..
# @google_login.login_failure
# def login_failure(e):
#     jsonify(error=str(e))
#     return redirect('/')

# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     """Logs the current user out. Clears the session, redirects to homepage."""
#     session.clear()
#     return redirect('/')


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
        mono_id = mono_object.mono_id
        char_id = mono_object.char_id
        play_id = mono_object.play_id
        scene = mono_object.scene_id
        act = mono_object.act_id
        text = mono_object.text
        text = text.replace('[p]', '<br>').split('<br>')

	# Gets info about this monologue ffrom Play Table
	play_object = Play.query.filter(Play.play_id==play_id).first()
        play_title = play_object.title

    # Gets info about this monologue from Scene Table
	scene_object = Scene.query.filter(Scene.scene_id==scene).first()
        description = scene_object.s_description

    # Get's info about this monologue from Character's table
	char_object = Character.query.filter(Character.char_id==char_id).first()
        name = char_object.char_name

    # Gets list of comments associated with this monologue from Comments table
        comments_list = Comment.query.filter(Comment.mono_id==mono_id).all()

    comments_dict = {}

    for comment in comments_list:
        user = User.Query.filter(User.user_id==comment.user_id).first()
        comments_dict["user.username"] = comment.comment_text

	return render_template("monologue.html", mono_id=mono_id, name=name, play_title=play_title, act=act, scene=scene, description=description, text=text, comments_dict=comments_dict)

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


@app.route('/add_youtube', methods=["POST"])
def add_new_youtube():
    """Stores a new youtube video into the db associated with a particular monoogue and user."""

    if request.method == 'POST' and form.validate():
        new_youtube = Youtube(youtube_url=form.youtube_url.data,mono_id=form.mono_id.data, user_id=form.user_id.data)
        db.session.add(new_user)
        db.session.commit()
        # flash('Welcome to the ensemble!')
        return redirect('/monologue/' + str(form.mono_id.data))


######## JSON ROUTES ##########

# @app.route('/shakespeare-links.json')
# def shakespeare_links():
#     """Return Shakespeare Force Graph Links as JSON."""
#     genres_lq = Genre.query.all()
#     plays_lq = Plays.query.all()
#
#     for genre in genres_lq:



@app.route('/shakespeare.json')
def shakespeare_json():
    """Return Shakespeare Force Graph Nodes as JSON."""

    return jsonify(shakespeare_data())

#     genres_q = Genre.query.all()
#     plays_q = Play.query.all()
#     characters_q = Character.query.all()
#     monologues_q = Monologue.query.all()
#
#     shakespeare = {}
#     shakespeare["genre"] = [genre.json() for genre in genres_q]
#     shakespeare["play"] = [play.json() for play in plays_q]
#     shakespeare["character"] = [character.json() for character in characters_q]
#     shakespeare["monologue"] = [monologue.json() for monologue in monologues_q]
#     printer.pprint(shakespeare)
#     return jsonify(shakespeare)
#
# @app.route('/comments.json')
# def comments_json():
#     """Return info about a comment as JSON."""
#     comments_q = Comment.query.all()
#     comments = {}
#     comments["comments"] = [comment.json() for comment in comments_q]
#     printer.pprint(comments)
#     return jsonify(comments)
#
# @app.route('/users.json')
# def users_json():
#     """Return info about a user as JSON."""
#     users_q = User.query.all()
#     users = {}
#     users["users"] = [user.json() for user in users_q]
#     printer.pprint(users)
#     return jsonify(users)



#Connecting server to db

if __name__ == "__main__":
	#debug=True for DebugToolbarExtension to work
	app.debug = True

	connect_to_db(app)

	#Use the DebugToolbar
	DebugToolbarExtension(app)
	print "\n\n\n\nYO\n\n\n"
	app.run()
