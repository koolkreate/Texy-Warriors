from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

"""
This file handles all forms - login forms and sign up forms for now
"""

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Submit")
