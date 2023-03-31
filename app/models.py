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
    user_agent = db.Column(db.String(15), unique=True, primary_key=True)
    client_secret = db.Column(db.String(15), unique=True)
    client_id = db.Column(db.String(15), unique=True)

    def __init__(self, user_agent, client_secret, client_id):
        self.user_agent = user_agent
        self.client_secret = client_secret
        self.client_id = client_id
        self.reddit = self._praw_client()

    @classmethod
    def from_self(cls, self):
        return cls(
            user_agent=self.user_agent,
            client_secret=self.client_secret,
            client_id=self.client_id,
        )

    def _praw_client(self):
        reddit = Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )
        return reddit


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_type = db.Column(db.String(50), nullable=False)
    query = db.Column(db.String(250), nullable=False)
    sort = db.Column(db.String(50), nullable=False)
    syntax = db.Column(db.String(50), nullable=True)
    time_filter = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Integer, nullable=True)
    subreddit = db.Column(db.String(250), nullable=True)
    redditor = db.Column(db.String(250), nullable=True)
    submission_id = db.Column(db.String(50), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
