from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import LoginForm
from flask_login import LoginManager
from supabase import create_client, Client
from auth import loginRequired
from dotenv import load_dotenv
import os
import jwt
from config import Config

#Must have a .env file with the environment variables mentioned to be able to run this
load_dotenv()

app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SUPERBASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

#Gets superbase urls and keys from .env file
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

"""Handles routing to sites"""

#Routes to homepage
@app.route("/")
def home():
    return render_template("homepage.html")

#Routes to login page
@app.route("/login")
def login():
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        email = loginForm.email.data
        password = loginForm.password.data

        print(email, password)
        #Check logic

    return render_template("login.html", form=loginForm)

#Using REST API endpoints to handle authentication at the moment
@loginRequired
@app.route("/users/<user_id>", methods=["GET"])
def checkUser(user, user_id):

    #For now only users can access their own information
    # TODO: Change this later on for admin access - right now it's not important
    if user["sub"] == user_id:
        return "Valid"
    else:
        return "Invalid"

#Runs flask application
if __name__ == '__main__':
    app.run()