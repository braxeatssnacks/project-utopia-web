# definition of routes
from flask import request, render_template
from . import app

@app.route("/")
def index():
    return render_template("home/default.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET": return render_template("form/signup.html")
    else: # handle submission attempt
        pass

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET": return render_template("form/login.html")
    else: # handle submission attempt
        pass
