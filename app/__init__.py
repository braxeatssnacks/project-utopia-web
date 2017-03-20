# definition of global app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app reference
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config") # load default config
#app.config.from_pyfile("config.py") # load instance config (override)

# instantiate database
db = SQLAlchemy(app)

from . import views
