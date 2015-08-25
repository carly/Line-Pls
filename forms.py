from wtforms import Form, BooleanField, SubmitField, TextField, PasswordField, validators
from wtforms.validators import DataRequired
from model import db, User



class SignupForm(Form):
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
