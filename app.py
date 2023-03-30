import os
from flask import Flask, Request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from wtforms import StringField, PasswordField, SubmitField, Form
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from praw import Reddit
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# these will get moved to the models.py file whe I refactor the code
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class API_Key(db.Model):
    __tablename__ = 'api_key'
    id = db.Column(db.Integer, primary_key=True)
    user_agent = db.Column(db.String(15), unique=True)
    client_secret = db.Column(db.String(15), unique=True)
    client_id = db.Column(db.String(15), unique=True)

    def __init__(self, user_agent, client_secret, client_id):
        self.user_agent = user_agent
        self.client_secret = client_secret
        self.client_id = client_id

    def reddit_api(self):
        reddit = Reddit(client_id=self.client_id,
                     client_secret=self.client_secret,
                     user_agent=self.user_agent)
        return reddit

class RegisterForm(FlaskForm):
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

class API_Form(FlaskForm):
    user_agent = StringField('api_key', validators=[InputRequired(), Length(min=4, max=15)])
    client_secret = StringField('client_secret', validators=[InputRequired(), Length(min=4, max=15)])
    client_id = StringField('client_id', validators=[InputRequired(), Length(min=4, max=15)])

    def validate_api_key(self, api_key):
        existing_api_key = API_Key.query().first()
        if existing_api_key:
            raise ValidationError('That API key already exists. Please choose a different one.')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    verify_api_key = API_Key.query.first()
    if verify_api_key:
        return redirect(url_for('login'))
    elif not verify_api_key:
        return redirect(url_for('api_key'))
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # this is the page that will render the login form 'login.html'
    # there will be a option for a new user to create an account
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if Bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return render_template('login.html', form=form, invalid=True)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# this will be the method that will handle the login form
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # this is the page that will render the register form 'register.html'
    # there will be a option for a new user to create an account
    if form.validate_on_submit():
        hashed_password = Bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/dashboard' , methods=['GET', 'POST'])
@login_required
def dashboard():

    return render_template('dashboard.html')
# need to setup db for flask
# need to reasearch how to use flask with a database

if __name__ == '__main__':
    app.run(debug=True)
