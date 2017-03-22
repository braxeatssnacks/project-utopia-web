# definition of routes
from flask import request, render_template,request, session, abort, flash
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms import validators, ValidationError
#from model import model as db
from . import app
import os 

app.secret_key = os.urandom(50)

@app.route("/")
def index():
    return render_template("home/home.html")

class LoginForm(Form):
	username = TextField('Username', [validators.Required(), validators.Length(min=4, max=25)])
	email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required(), validators.Length(min=6, max=200)])
	submit = SubmitField("Sign In")

class SignupForm(Form):
	username = TextField('Username', [validators.Required(), validators.Length(min=4, max=25)])
	email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required(), validators.Length(min=6, max=200)])
	submit = SubmitField("Sign Up")

@app.route("/")
def logout():
	return render_template("home/home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	form = SignupForm(csrf_enabled=False)
	session['name'] = form.username.data
	if request.method == "GET": 
		return render_template("form/signup.html", form=form)
	elif request.method == 'POST': # handle form submission 
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('form/signup.html', form = form)
		else:
			return render_template('dashboard/dashboard.html', name=session.get('name'))

@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm(csrf_enabled=False)
	session['name'] = form.username.data
	name = form.username.data
	if request.method == "GET":
		return render_template("form/login.html",form =form)
	elif request.method == 'POST':
		# handle form submission 
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('form/login.html', form = form)
		else:
			return render_template('dashboard/dashboard.html', name=name)

