# definition of routes
from __future__ import print_function # In python 2.7
from flask import request, render_template,request, session, abort, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms import validators, ValidationError
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.ext.login import login_user , logout_user , current_user , login_required
#from model import model as db
from . import app, db, models, forms

#Create a DBAPI connection
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])


@app.route("/")
def index():
	if 'email' not in session:
		return render_template("home/home.html")
		return redirect(url_for('login'))

@app.route("/logout")
def logout():
	logout_user()
	return render_template("home/home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	form = forms.SignupForm(csrf_enabled=False)

	Session = sessionmaker(bind=engine)
	session = Session()

	if request.method == "GET":
		return render_template("form/signup.html", form=form)
	elif request.method == 'POST': # handle form submission
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('form/signup.html', form = form)
		else:
			newuser = models.Teachers(form.name.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			name = form.name.data
			classboxForm = forms.ClassBox(csrf_enabled=False)
			return render_template('dashboard/classbox.html', form=classboxForm, name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
	form = forms.LoginForm(csrf_enabled=False)
	if request.method == "GET":
		return render_template("form/login.html",form =form)
	elif request.method == 'POST':
		# handle form submission
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('form/login.html', form = form)
		else:
			user = models.Teachers(name=form.name.data,email=form.email.data, password=form.password.data)
			login_user(user)
			session['name'] = form.name.data
			flash('Logged in successfully')
			return render_template('dashboard/dashboard.html', name=session['name'])

@app.route("/classbox", methods=["GET", "POST"])
@login_required
def classbox():
	form = forms.ClassBox(csrf_enabled=False)
	if request.method == "GET":
		return render_template("dashboard/classbox.html", form =form)
	elif request.method =="POST":
		newClassbox = models.Classrooms(id=form.classbox.data)
		name = session['name']
		email = session['email']
		newClassroom = models.Sections(id=form.classbox.data,classroom=form.classroom.data,teacher=name)
		db.session.add(newClassbox)
		db.session.commit()
		db.session.add(newClassroom)
		db.session.commit()
		return render_template("dashboard/dashboard.html", form =form, email=email)

@app.route('/dashboard')
@login_required
def dashboard():
	if 'email' not in session:
		return redirect(url_for('login'))
	user = models.Teachers.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('login'))
	else:
		return render_template('dashboard/dashboard.html')
