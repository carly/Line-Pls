
## Imports for Python Forms

from model import db, User
from wtforms import Form, BooleanField, SubmitField, TextField, PasswordField, HiddenField, validators, FileField
from wtforms.validators import DataRequired



## Form Classes Defined

class SignupForm(Form):
    """Defines the signup form for new users in python with wtforms."""

    username = TextField("Pick a username:",[validators.Length(min=4, max=25)])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
    validators.Required("Please enter a password."),
    validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
          return False

        user = User.query.filter(User.email==self.email.data.lower()).first()
        username = User.query.filter(User.username==self.username.data.lower()).first()
        if user and username:
            self.email.errors.append("That email is already taken.")
            self.username.errors.append("That username is already taken.")
            return False
        else:
          return True


class SigninForm(Form):
    """Defines the signin form for returning users in python wtfforms."""

    username = TextField("Username",[validators.Required("Please enter your username.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter(User.username==self.username.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.username.errors.append("Invalid username or password")
            return False


class PasswordForm(Form):
    """Defines form to change your password."""

    password = PasswordField('New Password', [
    validators.Required("Please enter a password."),
    validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("CHANGE PASSWORD")


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
