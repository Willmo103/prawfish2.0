from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    RadioField,
    IntegerField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    ValidationError,
    DataRequired,
    Optional,
)

from app.models import User, API_Key


class RegisterForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if not existing_user_username:
            raise ValidationError("That username does not exist. Please try again.")


class API_Form(FlaskForm):
    user_agent = StringField(
        "user_agent", validators=[InputRequired(), Length(min=4, max=50)]
    )
    client_secret = StringField(
        "client_secret", validators=[InputRequired(), Length(min=4, max=50)]
    )
    client_id = StringField(
        "client_id", validators=[InputRequired(), Length(min=4, max=50)]
    )
    submit = SubmitField("Save API Key")

    def validate_api_key(self, api_key):
        existing_api_key = API_Key.query().first()
        if existing_api_key:
            raise ValidationError(
                "That API key already exists. Please choose a different one."
            )


class SearchForm(FlaskForm):
    search_type = SelectField(
        "Search Type",
        choices=[
            ("subreddit", "Subreddit"),
            ("redditor", "Redditor"),
            ("submission", "Submission"),
            ("comments", "Comments"),
        ],
        validators=[DataRequired()],
    )
    query = StringField("Query", validators=[Optional()])
    sort = SelectField(
        "Sort",
        choices=[
            ("relevance", "Relevance"),
            ("hot", "Hot"),
            ("top", "Top"),
            ("new", "New"),
            ("controversial", "Controversial"),
            ("guilded", "Guilded"),
            ("rising", "Rising"),
            ("search_comments", "Search Comments"),
            ("comments", "Comments"),
        ],
        validators=[DataRequired()],
    )
    syntax = SelectField(
        "Syntax",
        choices=[
            ("cloudsearch", "Cloudsearch"),
            ("lucene", "Lucene"),
            ("plain", "Plain"),
        ],
        validators=[Optional()],
    )
    time_filter = SelectField(
        "Time Filter",
        choices=[
            ("all", "All"),
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
            ("year", "Year"),
        ],
        validators=[DataRequired()],
    )
    limit = IntegerField("Limit", validators=[Optional()])
    subreddit = StringField("Subreddit", validators=[Optional()])
    redditor = StringField("Redditor", validators=[Optional()])
    submission_id = StringField("Submission ID", validators=[Optional()])
    submit = SubmitField("Search")

    def validate_search_type(self, search_type):
        if search_type.data == "subreddit":
            if self.subreddit.data == "":
                raise ValidationError("Please enter a subreddit.")
        elif search_type.data == "redditor":
            if self.redditor.data == "":
                raise ValidationError("Please enter a redditor.")
        elif search_type.data == "submission":
            if self.submission_id.data == "":
                raise ValidationError("Please enter a submission ID.")
        elif search_type.data == "comments":
            if self.submission_id.data == "":
                raise ValidationError("Please enter a submission ID.")

        # set some defaults
        # TODO: make this better over time.

        if self.limit.data == "":
            self.limit.data = 20

        if self.syntax.data == "":
            self.syntax.data = "plain"

        if self.time_filter.data == "":
            self.time_filter.data = "all"

        if self.sort.data == "":
            self.sort.data = "relevance"

    def __repr__(self) -> str:
        return (
            f"Search Type: {self.search_type.data}\n"
            f"Search Query: {self.query.data}\n"
            f"Sort: {self.sort.data}\n"
            f"Syntax: {self.syntax.data}\n"
            f"Time Filter: {self.time_filter.data}\n"
            f"Limit: {self.limit.data}\n"
            f"Subreddit: {self.subreddit.data}\n"
            f"Redditor: {self.redditor.data}\n"
            f"Submission ID: {self.submission_id.data}\n"
        )

    def submit_search(self):
        # TODO use the search method to take all the data and return a list of results using the praw api
        pass
