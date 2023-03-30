import os
from flask import Flask, Request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField, Form
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm

app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)


# these will get moved to the models.py file whe I refactor the code
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

class RegisterForm(Form):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if not existing_user_username:
            raise ValidationError('That username does not exist. Please try again.')

@app.route('/')
def index():
    form = LoginForm()
    # check to see if the reddit api_key, client_id, and client_secret are set
    # render a form to get the api_key, client_id, and client_secret before continuing

    # if not all(['api_key', 'client_id', 'client_secret']) in os.environ:
    #     return render_template('form.html')



    # this is the main page that will render the index.html
    # get the user auth token the request header and try to verify it
    # if the token is valid, then the user will be redirected to the main page
    # if the token is invalid, then the user will be redirected to the login page





    # once the environment variables are set, the user needs to be redirected to login page

    # if not 'access_token' in os.environ:
    #     return redirect(url_for('login'))

    # if the user is logged in, then the user will be redirected to the main page
    return render_template('index.html' , form=form)


app.route('/login')
def login():
    # this is the page that will render the login form 'login.html'
    # there will be a option for a new user to create an account

    render_template('login.html')


# this will be the method that will handle the login form
app.route('/login')
def validate_login(request: Request ):
    ...
    return redirect(url_for('index'))

# need to setup db for flask
# need to reasearch how to use flask with a database

if __name__ == '__main__':
    app.run(debug=True)
