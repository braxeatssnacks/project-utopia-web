# definition of routes
from __future__ import print_function # In python 2.7
from flask import request, render_template,request, session, abort, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms import validators, ValidationError
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import login_user , logout_user , current_user , login_required
import sys
#from model import model as db
from . import app, db, models, forms

#Create a DBAPI connection
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
email = ""

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

	if request.method == "GET":
		return render_template("form/signup.html", form=form)
	elif request.method == 'POST': # handle form submission
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('form/signup.html', form = form)
		else:
			newuser = models.Teachers(form.name.data, form.email.data, form.password.data)
			models.db_session.add(newuser)
			models.db_session.commit()
			name = form.name.data
			form = forms.LoginForm(csrf_enabled=False)
			return render_template('form/login.html',form= form,name=name)

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
			#data to login
			print(form.email.data,sys.stderr)
			user = models.Teachers(name=form.name.data,email=form.email.data, password=form.password.data)
			if models.db_session.query(models.Sections).filter_by(teacher=user.email).first() == None:
				classbox = forms.ClassBox(csrf_enabled=False)
				name = form.name.data
				login_user(user)
				return render_template('dashboard/classbox.html', form=classbox, name=name)
			else:
				login_user(user)
				flash('Logged in successfully')
				name = form.name.data
				email = form.email.data
				print(email,sys.stderr)
				# info to populate dashboard
				classform = forms.ClassDataForm(csrf_enabled=False) 
				classbox = models.db_session.query(models.Sections).filter_by(teacher=email).first()
				sections = models.db_session.query(models.Sections).filter_by(teacher=email)
				section_numbers = models.db_session.query(models.Sections).filter_by(teacher=email).count()
				totalenrollment = models.db_session.query(models.Enrolled).distinct(models.Enrolled.student, models.Enrolled.classroom).count()
				return render_template('dashboard/dashboard.html',classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form = classform, name=name,email=email,registered_on=user.registered_on)

@app.route('/classbox', methods=["GET", "POST"])
@login_required
def classbox():
	form = forms.ClassBox(csrf_enabled=False)
	if request.method == "GET":
		return render_template("dashboard/classbox.html", form =form)
	elif request.method =="POST":
			if form.validate() == False:
				flash('All fields are required.')
				return render_template("dashboard/classbox.html", form = form)
			else:
				classbox = form.classbox.data
				classroom = form.classroom.data

				#make new classbox
				newClassbox = models.Classrooms(classbox)
				models.db_session.add(newClassbox)
				models.db_session.commit()

				email = form.email.data
				user = models.db_session.query(models.Teachers).filter_by(email=email).first()
				newClassroom = models.Sections(id=classroom,classroom=classbox,teacher=user.email)
				models.db_session.add(newClassroom)
				models.db_session.commit()

				name = user.name
				classbox = models.db_session.query(models.Sections).filter_by(teacher=user.email).first()
				sections = models.db_session.query(models.Sections).filter_by(teacher=user.email)
				section_numbers = models.db_session.query(models.Sections).filter_by(teacher=user.email).count()
				totalenrollment = models.db_session.query(models.Enrolled).distinct(models.Enrolled.student, models.Enrolled.classroom).count()
				return render_template('dashboard/dashboard.html',classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form = form, name=name,email=email,registered_on=user.registered_on)

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
	# form to get students
	form = forms.ClassDataForm(csrf_enabled=False)
	# remaining variables
	name =session['name']
	user = models.db_session.query(models.Teachers).filter_by(name=name).first()
	classbox = models.db_session.query(models.Sections).filter_by(teacher=user.email).first()
	sections = models.db_session.query(models.Sections).filter_by(teacher=user.email)
	section_numbers = models.db_session.query(models.Sections).filter_by(teacher=user.email).count()
	totalenrollment = models.db_session.query(models.Enrolled).distinct(models.Enrolled.student, models.Enrolled.classroom).count()
	
	if form.validate() == False:
		return render_template('dashboard/dashboard.html',classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form =form, name=name,email=email,registered_on=user.registered_on)
	elif form.validate() == True:
		newclass = models.Sections(id=form.classroom.data, classroom=classbox.classroom,teacher=user.email)
		models.db_session.add(newclass)
		models.db_session.commit()
		return render_template('dashboard/dashboard.html',classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form = form, name=name,email=email,registered_on=user.registered_on)



