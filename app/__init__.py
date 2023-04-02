import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


from app.models import API_Key

conf: API_Key | None = None
# dev build all tables
with app.app_context():
    db.create_all()
    conf = db.session.query(API_Key).first()

if conf is not None:
    print("API Key found, initializing Reddit instance.")
    conf = conf.from_self(conf)

from app import views
