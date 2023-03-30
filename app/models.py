from app import db, login_manager
from flask_login import UserMixin
from praw import Reddit


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class API_Key(db.Model):
    __tablename__ = "api_key"
    id = db.Column(db.Integer, primary_key=True)
    user_agent = db.Column(db.String(15), unique=True)
    client_secret = db.Column(db.String(15), unique=True)
    client_id = db.Column(db.String(15), unique=True)

    def __init__(self, user_agent, client_secret, client_id):
        self.user_agent = user_agent
        self.client_secret = client_secret
        self.client_id = client_id

    def praw_client(self):
        reddit = Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )
        return reddit


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
