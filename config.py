# application configurations

DEBUG = False
SQLALCHEMY_ECHO = False
import os
basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
TESTING = False
CSRF_ENABLED = False
SECRET_KEY = 'this-really-needs-to-be-changed'
