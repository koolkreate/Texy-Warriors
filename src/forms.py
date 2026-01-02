from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired()])
    password = PasswordField("Password")
    submit = SubmitField("Submit")
