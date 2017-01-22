from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, SelectField, SelectMultipleField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired
import sqlite3 as sql

class LoginForm(Form):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ProfileForm(Form):
    email = EmailField('email', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    bio = StringField('bio', validators=[DataRequired()])
    personal_skill = StringField('personal_skill', validators=[DataRequired()])
    # skills = SelectMultipleField(
    #     'Skills',
    #     option_widget=CheckboxInput(),
    #     widget=ListWidget(prefix_label=True))
    # skills = BooleanField('skills', validators=[DataRequired()])

class IdeaForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    # Tagetories
    # Skills
    # ownership

class CommentForm(Form):
    comment = StringField('comment', validators=[DataRequired()])
