# definition of global app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Blueprint

# app reference
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config") # load default config
app.config.from_pyfile("config.py") # load instance config (override)

# instantiate database
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
from . import views
#from . import models
