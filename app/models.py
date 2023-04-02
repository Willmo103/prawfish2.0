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

    @property
    def reddit(self):
        return self._praw_client()


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


class Redditor(db.Model):
    fullname = db.Column(db.String, primary_key=True)
    submissions = db.relationship("Submission", back_populates="author")


class Subreddit(db.Model):
    id = db.Column(db.String, primary_key=True)
    display_name = db.Column(db.String)
    public_description = db.Column(db.String)
    owner_id = db.Column(db.String, db.ForeignKey("redditor.fullname"))
    subscribers = db.Column(db.Integer)
    submissions = db.relationship("Submission", back_populates="subreddit")


class Submission(db.Model):
    id = db.Column(db.String, primary_key=True)
    author_fullname = db.Column(db.String, db.ForeignKey("redditor.fullname"))
    subreddit_id = db.Column(db.String, db.ForeignKey("subreddit.id"))
    title = db.Column(db.String)
    url = db.Column(db.String)
    score = db.Column(db.Integer)
    ups = db.Column(db.Integer)
    downs = db.Column(db.Integer)
    upvote_ratio = db.Column(db.Float)
    permalink = db.Column(db.String)
    thumbnail = db.Column(db.String)
    author = db.relationship("Redditor", back_populates="submissions")
    subreddit = db.relationship("Subreddit", back_populates="submissions")


class Image(db.Model):
    id = db.Column(db.String, primary_key=True)
    small = db.Column(db.String)
    medium = db.Column(db.String)
    large = db.Column(db.String)
    src = db.Column(db.String)
    owner_id = db.Column(db.String, db.ForeignKey("redditor.fullname"))
    subreddit_id = db.Column(db.String, db.ForeignKey("subreddit.id"))
    submission_id = db.Column(db.String, db.ForeignKey("submission.id"))


def parse_json_to_models(json_object):
    # Create Redditor
    redditor_name = json_object["author"][18:-2]
    redditor = Redditor(fullname=json_object["author_fullname"])

    # Create Subreddit
    subreddit = Subreddit(
        id=json_object["Subreddit"]["subreddit_id"],
        display_name=json_object["Subreddit"]["subreddit_name_prefixed"][2:],
        public_description="",
        owner_id=json_object["author_fullname"],
        subscribers=json_object["Subreddit"]["subreddit_subscribers"],
    )

    # Create Submission
    submission = Submission(
        id=json_object["id"],
        author_fullname=json_object["author_fullname"],
        subreddit_id=json_object["Subreddit"]["subreddit_id"],
        title=json_object["title"],
        url=json_object["url"],
        score=json_object["score"],
        ups=json_object["ups"],
        downs=json_object["downs"],
        upvote_ratio=json_object["upvote_ratio"],
        permalink=json_object["permalink"],
        thumbnail=json_object["thumbnail"],
    )

    # Create Images
    images = []
    for image_data in json_object["preview"]["images"]:
        image = Image(
            id=image_data["id"],
            small=image_data["resolutions"][1]["url"],
            medium=image_data["resolutions"][2]["url"],
            large=image_data["resolutions"][5]["url"],
            src=image_data["source"]["url"],
            owner_id=json_object["author_fullname"],
            subreddit_id=json_object["Subreddit"]["subreddit_id"],
        )
        images.append(image)

    return redditor, subreddit, submission, images


def save_if_not_exists(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
    return instance


def save_models_to_database(submission, redditor, subreddit, images):
    # Save redditor
    saved_redditor = save_if_not_exists(db.session, Redditor, id=redditor.id)

    # Save subreddit
    saved_subreddit = save_if_not_exists(db.session, Subreddit, id=subreddit.id)

    # Save submission
    saved_submission = save_if_not_exists(
        db.session,
        Submission,
        id=submission.id,
        author_id=saved_redditor.id,
        subreddit_id=saved_subreddit.id,
    )

    # Save images
    saved_images = []
    for image in images:
        saved_image = save_if_not_exists(
            db.session,
            Image,
            id=image.id,
            owner_id=saved_redditor.id,
            subreddit_id=saved_subreddit.id,
        )
        saved_images.append(saved_image)

    return saved_submission, saved_redditor, saved_subreddit, saved_images


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
