from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

"""
This file handles all forms - login forms and sign up forms for now
"""

confirmPasswordValidators = [DataRequired(),
                             EqualTo("password", message="Passwords must match")]

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Submit")

class SignUpForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    firstName = StringField("First Name", validators=[DataRequired()])
    middleNames = StringField("Middle Names (Optional)", validators=[Optional()])
    surname = StringField("Surname", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField("Confirm Password", validators=confirmPasswordValidators)
    submit = SubmitField("Submit")