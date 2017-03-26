from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms import validators, ValidationError
from wtforms.widgets import PasswordInput
from . import models
from . import db

class LoginForm(FlaskForm):
	name = TextField('Username', [validators.Required(), validators.Length(min=4, max=100)])
	email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
	password = StringField('Password', widget=PasswordInput(hide_value=False))
	submit = SubmitField("Sign In")

	def __init__(self, *args, **kwargs):
		FlaskForm.__init__(self, *args, **kwargs)
	

class SignupForm(FlaskForm):
	name = TextField('Username', [validators.Required(), validators.Length(min=4, max=100)])
	email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])
	submit = SubmitField("Sign Up")

	def __init__(self, *args, **kwargs):
		FlaskForm.__init__(self, *args, **kwargs)

class ClassBox(FlaskForm):
	classbox = TextField('classbox', [validators.Required(), validators.Length(min=4, max=120)])
	classroom = TextField('classroom', [validators.Required(), validators.Length(min=4, max=120)])
	submit = SubmitField("Create ClassBox")

	def __init__(self, *args, **kwargs):
		FlaskForm.__init__(self, *args, **kwargs)
