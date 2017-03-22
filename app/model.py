from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash  
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, event, Boolean, Table  
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relationship  
import flask


#app = Flask(__name__, instance_relative_config=True)
# where my db is being hosted for now
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/project_utopia'

class Teachers(db.Model):
	__tablename__ = 'Teachers'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(25))
	classroom = db.Column(db.String(20),db.ForeignKey('classrooms.id'))

	def __init__(self, id, name, email, password,classroom):
		self.id = id
		self.name = name
		self.email = email
		self.classroom = classroom
		# TODO: define hash function
		self.password = set_password(password) 

	def __repr__(self):
		return '<Teacher %r>' % self.name

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

class Classrooms(db.Model):
	__tablename__ = 'classrooms'
	id = db.Column(db.String(20), primary_key=True)
	date_created = db.Column(db.Date())
	student = db.Column(db.Integer,db.ForeignKey('students.id'), ondelete='SET NULL')

	def __init__(self,id, date_created, student):
		self.id = id
		self.date_created = date_created
		self.student = student

	def __repr__(self):
		return '<Classroom %r>' % self.id

class Students(db.Model):
	__tablename__ = 'students'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100), unique=True)
	stage_number = db.Column(db.Integer)
	stage_date_started = db.Column(db.Date())
	stage_date_completed = db.Column(db.Date())
	attemps = db.Column(db.Integer)
	code = db.Column(db.String(1000))

	def __init__(self, id, name, email, stage_number,stage_date_started, stage_date_completed,attemps,code):
		self.id = id
		self.name = name 
		self.email = email 
		self.stage_number = stage_number
		self.stage_date_started = stage_date_started
		self.stage_date_completed = stage_date_completed
		self.attemps = attemps
		self.code = code 

	def __repr__(self):
		return '<Student %r>' % self.name

