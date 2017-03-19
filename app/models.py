# database modeling
from . import db

class User(db.Model):
    # COLUMNS

    """ auto-incrementing unique id """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    """ first last """
    name = db.Column(db.String(80), nullable=False)

    """ unique identifer """
    email = db.Column(db.String(80), nullable=False)

    """ hashed password """
    password = db.Column(db.String(80))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = hash(password) # TODO: define hash function

    def __repr__(self):
        return "<id ()>".format(self.id)
