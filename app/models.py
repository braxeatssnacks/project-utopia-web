from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column,Sequence, Integer, String, DateTime,Date, ForeignKey, event, Boolean, Table, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import flask
from flask_login import LoginManager, UserMixin,login_user, login_required
from . import app

#Declare an instance of the Base class for mapping tables
Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))

Base.query = db_session.query_property()
SECTION_SEQ = Sequence('user_id_seq')  # define sequence explicitly

class Teachers(Base):
	__tablename__ = 'teachers'
	name = Column(String(100),nullable=False)
	email = Column(String(100),primary_key=True, unique=True, nullable=False)
	password = Column(String(100),nullable=False)
	registered_on = Column(Date, default=datetime.datetime.utcnow().strftime("%Y-%m-%d"),nullable=False)


	def __init__(self, name, email, password,registered_on=None):
		self.name = name
		self.email = email
		self.set_password(password)
		self.registered_on = datetime.datetime.utcnow().strftime("%Y-%m-%d")

	def __repr__(self):
		return '<Teacher %r>' % self.name

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def is_authenticated(self):
		users = Teachers.objects(name=self.name, password=self.password)
		return len(users) != 0

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return (self.email)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user_id(email):
    return Teachers.query.filter(Teachers.email==email).first()

class Classrooms(Base):
	__tablename__ = 'classrooms'
	id = Column(String(30),primary_key=True,unique=True)
	date_created = Column(DateTime, default=datetime.datetime.utcnow(),nullable=False)

	def __init__(self,id,date_created=None):
		self.id = id
		self.date_created = datetime.datetime.utcnow()

	def __repr__(self):
		return '<Classroom %r>' % self.id

class Sections(Base):
	__tablename__ = 'sections'
	id = Column(Integer, SECTION_SEQ,primary_key=True,unique=True,server_default=SECTION_SEQ.next_value())
	name = Column(String(100))
	classroom = Column(String(1000), ForeignKey('classrooms.id'),nullable=False)
	teacher = Column(String(100), ForeignKey('teachers.email'), nullable=False)

	def __init__(self,id,name,classroom,teacher):
		self.id = id
		self.name = name
		self.teacher = teacher
		self.classroom = classroom

	def __repr__(self):
		return '<Section %r>' % self.id

class Students(Base):
	__tablename__ = 'students'
	name = Column(String(100),nullable=False)
	email = Column(String(100),primary_key=True, unique=True)
	section = Column(Integer, ForeignKey('sections.id'),primary_key=True, nullable=False)
	stage_number = Column(Integer,nullable=False)
	stage_date_started = Column(Date(),nullable=False)
	stage_date_completed = Column(Date(),nullable=False)
	attempts = Column(Integer)
	code = Column(String(1000))
	#ForeignKeyConstraint(['section'], ['section.id'])

	def __init__(self, name, email, stage_number, stage_date_started, stage_date_completed, attempts, code, section):
		self.name = name
		self.email = email
		self.stage_number = stage_number
		self.stage_date_started = stage_date_started
		self.stage_date_completed = stage_date_completed
		self.attempts = attempts
		self.code = code
		self.section = section 

	def __repr__(self):
		return '<Student %r>' % self.name

class Enrolled(Base):
 	__tablename__ = 'enrolled'
 	student = Column(String(100), ForeignKey('students.email'),primary_key=True,nullable=False)
 	section =  Column(String(100),primary_key=True, nullable=False)
 	classroom = Column(String(100), primary_key=True,nullable=False)
 	section_name = Column(String(100), nullable=False)
 	ForeignKeyConstraint(['section', 'classroom','section_name'], ['section.id', 'section.classroom','section_name'])

 	def __init__(self,student,section,classroom, section_name):
 		self.student = student
 		self.section = section
 		self.classroom = classroom
 		self.section_name = section_name

 	def __repr__(self):
 		return '<Enrolled %r>' % self.student

# Create the table using the metadata attribute of the base class
# Base.metadata.create_all(engine)

# Sessions give you access to Transactions, whereby on success you can commit the transaction or rollback one incase you encounter an error

# Session = sessionmaker(bind=engine)
# session = Session()


# #Insert multiple data in this session, similarly you can delete
# classroom1 = Classrooms(id='comsw4156')
# classroom2 = Classrooms(id='comsw4111')
# teacher1 = Teachers(name='Ewan Lowe',email='elowe@cs.columbia.edu',password='comsw4156')
# teacher2 = Teachers(name='Paul Blaer',email='pblaer@cs.columbia.edu',password='comsw3134')
# student1 = Students(name='Kofi Fredrick Tam', email='fkt2105@columbia.edu', stage_number=9,
# 	stage_date_started='03/03/2017',stage_date_completed='04/03/2017',attemps=2,code='Hello, world')
# student2 = Students(name='Braxton Gunter', email='beg2119@columbia.edu', stage_number=7,
# 	stage_date_started='03/03/2017',stage_date_completed='04/03/2017',attemps=2,code='Hello, world')
# student3 = Students(name='Aditi Hudli', email='aah2183@columbia.edu',stage_number=3,
# 	stage_date_started='03/03/2017',stage_date_completed='04/03/2017',attemps=2,code='Hello, world')

# session.add(classroom1)
# session.add(classroom2)
# session.add(teacher1)
# session.add(teacher2)
# session.add(student1)
# session.add(student2)
# session.add(student3)

# if __name__ == "__main__":


# 	try:
# 		session.commit()
# 	#You can catch exceptions with  SQLAlchemyError base class
# 	except SQLAlchemyError as e:
# 		session.rollback()
# 		print (str(e))
# 	#Get data
# 	for student in session.query(Students).all():
# 		print ("name of the student is" ,student.name)
# 		print ("email id of the student is" ,student.email)
# 	# Close the connection
# engine.dispose()
