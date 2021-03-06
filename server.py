"""Line Pls! An online community for actors."""

# Imports - standard lib
import boto
import json
import os
import pprint
import time

# Imports - flask + flask ext
from flask import Flask, render_template, redirect, request, flash, session, jsonify, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_oauth2_login import GoogleLogin
from flask_login import LoginManager

# Imports - 3rd party + flask integration
from boto.s3.key import Key
from jinja2 import StrictUndefined
from werkzeug import secure_filename

# Imports - local application based
from forms import SignupForm, SigninForm, PasswordForm
from helper_functions import shakespeare_data
from model import Play, Scene, Genre, Character, Monologue, User, Comment, Youtube, Follower, UserVid, Reel, connect_to_db, db


#s3 connection and bucket creation
# this was not implemented yet on demo day. Continuing to add features - learning about s3 buckets.
#c = boto.connect_s3()
#b = c.get_bucket('linepls')

# This connects to an s3 bucket I made so users can store large pdf files (like their resume)
UPLOAD_FOLDER = 'http://s3.amazonaws.com/linepls'
ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'png', 'pdf'])

PORT = int(os.environ.get("PORT", 5000))


#  App Config

app = Flask(__name__)

# Config adjustments
# used for jSON functions attached to models for future implementation of d3
printer = pprint.PrettyPrinter()

app.secret_key = """supersecret"""
app.jinja_env.undefined = StrictUndefined
Bootstrap(app)
# Flask login manager extension
login_manager = LoginManager()
login_manager.init_app(app)


################################ ROUTES/VIEWS  #################################

## SIGN IN/OUT

@app.route('/')
def index():
    """Renders homepage"""

    return render_template("homepage.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """A form for users to signup and create an account."""
    # Using WTFforms here - see forms.py for breakdown of form code
    form = SignupForm(request.form)

    # Checks to see if username is in session. If they've logged in it redirects them to the profile page.
    if 'username' in session:
        return redirect(url_for('profile'))
    # If they haven't logged in, when they fill out the form, send it to this function. This creates a new user in the db.
    if request.method == 'POST' and form.validate():
            new_user = User(username=form.username.data,email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('profile'))
            # Saves username and email into the session
            session['email'] = new_user.email
            session['username'] = new_user.username
            return redirect(url_for('profile'))

    return render_template('signup.html', form=form)


@app.route('/signin', methods=["GET", "POST"])
def signin():
    """Form for signing into the app, once you have created an account."""

    #Flask WTForms
    form = SigninForm(request.form)

    #Once they are signed in, redirect to profile
    if 'username' in session:
        return redirect(url_for('profile'))

    #If not signed in yet, make sure the form validates. Then save the following into the session.
    if request.method == "POST":
        if form.validate()==False:
            return render_template('signin.html', form=form)
        else:
            session['username']= form.username.data
            user = User.query.filter(User.username==form.username.data.lower()).first()
            session['email']= user.email
            session['id'] = user.user_id
            session['picture'] = user.picture
            return redirect(url_for('profile'))

    elif request.method == "GET":
        return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
    """Form for signing out. Dumps user session info and redirects to homepage."""

    if 'username' not in session:
        return redirect(url_for('signin'))

    session.pop('username', None)
    return redirect(url_for('index'))


# SIGNED IN USER => ACCOUNT RELATED
@app.route('/profile')
def profile():
    """Renders user's profile page when they are logged in."""

    if 'username' not in session:
        return redirect(url_for('signin'))
    #Queries user from db info based on session
    user = User.query.filter(User.username==session['username']).first()
    #if there is no user in the db associated with the username in session, redirect them for the signup page.
    if user is None:
        return redirect(url_for('signup'))
    else:
        # assign the user data to these variables that we will pass to jinja to render the profile page template w/ updated info
        name = user.name
        username = user.username
        picture = user.picture
        bio = user.bio
        website = user.website
        twitter = user.twitter
        user_id = user.user_id
        snapchat = user.snapchat
        instagram = user.instagram

    # Get reel from db - if they have a reel, assign it to a var so we can render it with jinja on their prof page.
        reel = Reel.query.filter(Reel.user_id==user_id).first()
        if reel is not None:
            get_reel = reel.reel_key
        else:
            get_reel= " "

        #If this user has followers, go to the follower table and give back a list of all users who follow the current user
        following = Follower.query.filter(Follower.user_id==user_id).all()
        your_follower_ids = []
        for f in following:
            # Appends your followers user ids to list
            your_follower_ids.append(f.follower)

        your_followers = {}
        for user_id in your_follower_ids:
            user = User.query.filter(User.user_id==user_id).first()
            if user is not None:
                your_followers['user.user_id'] = {"pic": user.picture, "username": user.username}



        return render_template('profile.html', name=name, username=username, picture=picture, bio=bio, website=website, twitter=twitter, snapchat=snapchat, instagram=instagram, user_id=user_id, get_reel=get_reel, your_followers=your_followers)


@app.route('/account')
def account():
    """Renders view for user to view, change, update account information."""
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
        picture = user.picture
        instagram = user.instagram
        snapchat = user.snapchat

    else:
        name = ""
        bio = ""
        web = ""
        twitter = ""
        picture = ""
        instagram = ""
        snapchat = ""

    return render_template('myaccount.html', name=name, bio=bio, web=web, twitter=twitter, picture=picture, instagram=instagram, snapchat=snapchat)


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
    new_pic = request.form.get("picture")
    new_insta = request.form.get("instagram")
    new_snap = request.form.get("snapchat")
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
        user.picture = new_pic
        user.instagram = new_insta
        user.snapchat = new_snap

    db.session.commit()
    return redirect(url_for('account'))


@app.route('/password/<string:username>', methods=["GET","POST"])
def change_password(username):
    """Change/Update password"""
    form = PasswordForm(request.form)

    if request.method =='GET':
        return render_template("password.html")

    if request.method == 'POST' and form.validate():
        current_user = User.query.filter(User.user_id==session['id']).first()
        current_user.password = form.password.data
        picture = current_user.picture
        db.session.commit()


    return render_template('password.html', form=form)


@app.route('/save_resume', methods=['POST'])
def save_file():
    """Name and save resume file to s3."""

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename('%s' %int(time.time()) + '.pdf')

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        user_id = session['id']
        update_user = User.query.filter(User.user_id==user_id).first()
        update_user.resume = file_path
        db.session.commit()

    k = b.new_key(filename)
    k.set_contents_from_file(file)
    k = b.lookup(file)
    db.session.commit()

    return "success"

@app.route('/reel', methods=['POST'])
def add_reel():

    if request.method == "POST":
        user_id = session['id']
        reel_key = request.form.get("reel")

        new_reel = Reel(user_id=user_id, reel_key=reel_key)
        db.session.add(new_reel)
        db.session.commit()

    return redirect(url_for('account'))


# SOCIAL NETWORKING RELATED
@app.route('/actors')
def display_actors():
    """Display a list of all actors on the site with links to their profile pages."""

    actors_db = User.query.all()

    return render_template("actors.html", actors_db=actors_db)


@app.route('/profile/<string:username>')
def view_profile(username):
    """View another users public profile."""

    user = User.query.filter(User.username == username).first()
    user_id = user.user_id
    username = user.username
    name = user.name
    website = user.website
    bio = user.bio
    twitter = user.twitter
    picture = user.picture
    snapchat = user.snapchat
    instagram = user.instagram

    #Show user reel
    reel = Reel.query.filter(Reel.user_id==user_id).first()
    if reel:
        get_reel = reel.reel_key
    else:
        get_reel = " "

    following = Follower.query.filter(Follower.user_id==user_id).all()
    your_follower_ids = []
    for f in following:
        # Appends your followers user ids to list
        your_follower_ids.append(f.follower)

    your_followers = {}
    for user_id in your_follower_ids:
        user_list = User.query.filter(User.user_id==user_id).all()
        for u in user_list:
            your_followers['u.user_id'] = {"pic": u.picture, "username": u.username}

    return render_template("profile.html", user_id=user_id, username=username, name=name, website=website, bio=bio, twitter=twitter, snapchat=snapchat, instagram=instagram, picture=picture, get_reel=get_reel, your_followers=your_followers)


@app.route('/follow', methods=['GET', 'POST'])
def follower():
    """Add followers to a user, display user followers."""

    if request.method == "GET":
        pass

    if request.method == "POST":
        current_user = request.form.get('follower') # (user in current session)
        followed = request.form.get('follow') #user_id (who you want to follow)
        followed_user = request.form.get('followed-user')

        new_follower = Follower(user_id=followed, follower=current_user)

        db.session.add(new_follower)
        db.session.commit()

        return redirect('/profile/' + str(followed_user))


# MONOLOGUE SEARCH RELATED
@app.route('/search', methods=["POST"])
def search():
    """Renders search page."""

    multiselect = request.form.getlist('mymultiselect')

    if "all" in multiselect:
        return render_template("play_list.html", plays=plays)

    elif "c" in multiselect:
        plays = Play.query.filter(Play.genre_id=='c').all()
        return render_template("play_list.html", plays=plays)

    elif "h" in multiselect:
        plays = Play.query.filter(Play.genre_id=='h').all()
        return render_template("play_list.html", plays=plays)

    elif "t" in multiselect:
        plays = Play.query.filter(Play.genre_id=='t').all()
        return render_template("play_list.html", plays=plays)

    return render_template("search.html")


@app.route('/plays')
def play_list():
    """Show list of all the Shakespeare Plays in the database."""
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
    # FIX ME
        mono_list = Monologue.query.filter(Monologue.play_id==play_id).all()

        mono_characters = []
        for mono in mono_list:
            mono_characters.append(mono.char_id)

        characters = Character.query.filter(Character.play_id==play_id).all()

        chars = {}

        for char in characters:
            if char.char_id in mono_characters:
                char= Character.query.filter(Character.char_id==char.char_id).first()
                chars[char.char_id] = char.char_name

	return render_template("play_details.html", title=title, long_title=long_title, date=date, genre=genre, chars=chars)


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

	# Gets info about this monologue from Play Table
	play_object = Play.query.filter(Play.play_id==play_id).first()
        play_title = play_object.title

    # Gets info about this monologue from Scene Table
	scene_object = Scene.query.filter(Scene.scene_id==scene).first()
        description = scene_object.s_description

    # Gets info about this monologue from Character's table
	char_object = Character.query.filter(Character.char_id==char_id).first()
        name = char_object.char_name

    # Gets info about the current user's id

        user = User.query.filter(User.username==session['username']).first()
        user_id = user.user_id
        username = user.username

    # Gets list of all youtube keys associated with mono_id
        youtube_playlist = Youtube.query.filter(Youtube.mono_id==mono_id).all()

    # Gets list of comments associated with this monologue from Comments table
        comments_list = Comment.query.filter(Comment.mono_id==mono_id).all()

        comments_dict = {}

        for comment in comments_list:
            user = User.query.filter(User.user_id==comment.user_id).first()
            username = user.username
            id = comment.comment_id
            comments_dict[id] = [username, comment.comment_text]

	return render_template("monologue.html", mono_id=mono_id, name=name, play_title=play_title, act=act, scene=scene, description=description, text=text, comments_dict=comments_dict, user_id=user_id, username=username, youtube_playlist=youtube_playlist)


# RELATED TO MONOLOGUE ANNOTATIONS AND YOUTUBE VIDS
@app.route('/show_reels')
def reel_list():
    """Show list of all the user Reels in the database."""
    reels = Reel.query.all()

    reel_dict = {}

    for reel in reels:
        user = User.query.filter(User.user_id==reel.user_id).first()
        reel_dict[user.username]=reel.reel_key

    return render_template("reels.html", reel_dict=reel_dict)


@app.route('/mono_vids')
def mono_vids():
    """Show list of all the user posted monologues in the database."""
    youtube = Youtube.query.all()

    yt_dict = {}

    for y in youtube:
        user = User.query.filter(User.user_id==y.user_id).first()
        yt_dict[user.username]= y.youtube_key

    return render_template("monologue_vids.html", yt_dict=yt_dict)


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
    """Stores a new youtube video into the db associated with a particular Monologue and user."""

    youtube_key = request.form.get("youtube")
    mono_id = request.form.get("mono_id")
    user_id = request.form.get("user_id")
    username = request.form.get("username")

    new_video = Youtube(mono_id=mono_id, user_id=user_id, youtube_key=youtube_key, username=username)

    db.session.add(new_video)
    db.session.commit()

    return redirect('/monologue/' + str(mono_id))


@app.route('/shakespeare.json')
def shakespeare_json():
    """Return Shakespeare Force Graph Nodes as JSON."""

    return jsonify(shakespeare_data())


##########  Connecting server to db    ############


if __name__ == "__main__":
	#debug=True for DebugToolbarExtension to work
	connect_to_db(app)

	#Use the DebugToolbar
	DebugToolbarExtension(app)
	print "\n\n\n\nYO\n\n\n"
	app.run(debug=True, host="0.0.0.0", port=PORT)
