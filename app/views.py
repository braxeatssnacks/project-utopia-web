# definition of routes
from __future__ import print_function # In python 2.7
from flask import request, render_template,request, session, abort, flash, redirect, url_for, jsonify 
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms import validators, ValidationError
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import login_user , logout_user , current_user , login_required
import sys
import json
from pprint import pprint
from flask_cors import cross_origin
#from model import model as db
from . import app, db, models, forms
import string
import re

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
	# clear session data and log user out of app
	session.clear()
	logout_user()
	return render_template("home/home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	form = forms.SignupForm(csrf_enabled=False)

	if request.method == "GET":
		return render_template("form/signup.html", form=form)
	elif request.method == 'POST': 
		if form.validate() == False:
			# if form fields not filled
			flash('All fields are required.')
			return render_template('form/signup.html', form = form)
		elif models.db_session.query(models.Teachers).filter_by(email=form.email.data).first() != None:
			error = 'That email already exists in our records, are you sure dont already have an account?'
			return render_template('form/signup.html', form = form, error=error)
		else:
			# handle form submission
			newuser = models.Teachers(form.name.data, form.email.data, form.password.data)
			models.db_session.add(newuser)
			models.db_session.commit()
			return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
	form = forms.LoginForm(csrf_enabled=False)
	if request.method == "GET":
		return render_template("form/login.html",form =form)
	elif request.method == 'POST':
		# handle form submission
		if form.validate() == False:
			error = 'All fields are required.'
			return render_template('form/login.html', form = form, error=error)
		else:
			session['name'] = form.name.data 
			session['email'] = form.email.data 
			#data to login
			user = models.Teachers(name=form.name.data,email=form.email.data, password=form.password.data)

			if models.db_session.query(models.Teachers).filter_by(email=user.email).first() == None:
				# user data not in db 
				error = ' Account credentials entered do not exist, sign up for a new account.'
				return render_template('form/login.html', form = form, error=error)
			elif models.db_session.query(models.Sections).filter_by(teacher=user.email).first() == None  and models.db_session.query(models.Teachers).filter_by(email=user.email).first() != None:
				classbox = forms.ClassBox(csrf_enabled=False)
				name = form.name.data
				login_user(user)
				return render_template('dashboard/classbox.html', form=classbox, name=name)
			else:
				login_user(user)
				flash('Logged in successfully')
				name = form.name.data
				email = form.email.data
				# info to populate dashboard
				classform = forms.ClassDataForm(csrf_enabled=False) 
				classbox = models.db_session.query(models.Sections).filter_by(teacher=email).first()
				sections = models.db_session.query(models.Sections).filter_by(teacher=email)
				section_numbers = models.db_session.query(models.Sections).filter_by(teacher=email).count()
				totalenrollment = models.db_session.query(models.Enrolled).distinct(models.Enrolled.student, models.Enrolled.classroom).filter_by(classroom=classbox.classroom).count()
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

				email = session['email']
				user = models.db_session.query(models.Teachers).filter_by(email=email).first()
				newClassroom = models.Sections(id=None,name=classroom,classroom=classbox,teacher=user.email)
				models.db_session.add(newClassroom)
				models.db_session.commit()

				name = user.name
				classform = forms.ClassDataForm(csrf_enabled=False) 
				classbox = models.db_session.query(models.Sections).filter_by(teacher=user.email).first()
				sections = models.db_session.query(models.Sections).filter_by(teacher=user.email)
				section_numbers = models.db_session.query(models.Sections).filter_by(teacher=user.email).count()
				totalenrollment = models.db_session.query(models.Enrolled).distinct(models.Enrolled.student, models.Enrolled.classroom).filter_by(classroom=classbox.classroom).count()
				return render_template('dashboard/dashboard.html',classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form = classform, name=name,email=email,registered_on=user.registered_on)

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
	# form to get students
	form = forms.ClassDataForm(csrf_enabled=False)
	# remaining variables
	name =session['name']
	email = session['email']
	user = models.db_session.query(models.Teachers).filter_by(email=email).first()
	classbox = models.db_session.query(models.Sections).filter_by(teacher=user.email).first()
	sections = models.db_session.query(models.Sections).filter_by(teacher=user.email)
	section_numbers = models.db_session.query(models.Sections).filter_by(teacher=user.email).count()
	totalenrollment = models.db_session.query(models.Enrolled).distinct(models.Enrolled.student, models.Enrolled.classroom).filter_by(classroom=classbox.classroom).count()

	# adding new class to teach 
	if form.validate() == False:
		# if class button not filled and button clicked
		return render_template('dashboard/dashboard.html',classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form =form, name=name,email=email,registered_on=user.registered_on)
	elif models.db_session.query(models.Sections).filter_by(name=form.classroom.data).first() != None:
		error = 'you already have a classroom with that name, pick a new classroom name'
		return render_template('dashboard/dashboard.html',classroom=sections, error=error, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form =form, name=name,email=email,registered_on=user.registered_on)
	elif form.validate() == True and models.db_session.query(models.Sections).filter_by(name=form.classroom.data).first() == None:
		newclass = models.Sections(id=None,name=form.classroom.data, classroom=classbox.classroom,teacher=user.email)
		models.db_session.add(newclass)
		models.db_session.commit()
		section_numbers = models.db_session.query(models.Sections).filter_by(teacher=user.email).count()
		return render_template('dashboard/dashboard.html',classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form = form, name=name,email=email,registered_on=user.registered_on)

@app.route('/classdata/<classroom>')
@login_required
def classdata(classroom):
	if classroom == None:
		redirect(url_for('dashboard'))
		return
	else:
		form = forms.ClassDataForm(csrf_enabled=False)
		email = session['email']
		name = session['name']
		user = models.db_session.query(models.Teachers).filter_by(email=email).first()
		classbox = models.db_session.query(models.Sections).filter_by(teacher=user.email).first()
		sections = models.db_session.query(models.Sections).filter_by(teacher=user.email)
		section_numbers = models.db_session.query(models.Sections).filter_by(teacher=user.email).count()
		totalenrollment = models.db_session.query(models.Enrolled).distinct(models.Enrolled.student, models.Enrolled.classroom).filter_by(classroom=classbox.classroom).count()
		section_info = models.db_session.query(models.Sections.id).filter_by(name=classroom).first()
		section_id = section_info.id
		section_count = models.db_session.query(models.Enrolled).filter_by(section=str(section_id)).count()
		# made query in raw SQL
		enrolled = db.engine.execute('select distinct(students.email) ,students.name,students.stage_number,students.stage_date_started,students.stage_date_completed,students.attempts,students.code from students, enrolled,sections where students.email = enrolled.student and enrolled.classroom = sections.classroom and enrolled.section_name =(%s)', classroom)
		return render_template('dashboard/dashboard.html', section_enrollment =section_count, enrolled=enrolled,classname=classroom, classroom=sections, classnumber=section_numbers, totalenrollment=totalenrollment,classbox=classbox.classroom, form=form, name=name,email=email,registered_on=user.registered_on)

@app.route('/update_stage', methods=["POST"])
@cross_origin(["POST"])
def update():
	if request.content_type != 'application/json':
		return jsonify({"error": "format application/json"})
	# is json
	try:
		data = json.loads(request.data.decode('UTF-8'))
	except ValueError:
		return jsonify({"error": "value error"})

	# get POST params
	name = data["name"]
	email = data["email"]
	stage_number= data["stage_number"]
	stage_date_started = data["stage_date_started"]
	stage_date_completed = data["stage_date_completed"]
	attempts = data["attempts"]
	code = data["code"]
	section_id = data["section_id"]

	# PUT STUDETNS IN TABLE 
	# not yet in table
	if models.db_session.query(models.Enrolled).filter_by(student=email, section=section_id).first() == None:
		# add current stage data 
		section = models.db_session.query(models.Sections).filter_by(id=section_id).first()
		section_name = section.name
		classbox = section.classroom
		newStudent = models.Students(name, email, stage_number, stage_date_started, stage_date_completed, attempts, code, section_id)
		models.db_session.add(newStudent)
		models.db_session.commit()

		#add new user in classroom section instance 
		newEnrolled = models.Enrolled(email, section_id, classbox, section_name)
		models.db_session.add(newEnrolled)
		models.db_session.commit()

	# already in table
	else:
		# update stage data 
		models.db_session.query.filter_by(student=='email', section=section_id).update({ attempts:attempts, stage_number:stage_number, stage_date_started:stage_date_started,
			stage_date_completed : stage_date_completed, code:code})
		db.session.commit()

	return jsonify({ "success": True })

	
