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
        "user_agent", validators=[InputRequired(), Length(min=4, max=15)]
    )
    client_secret = StringField(
        "client_secret", validators=[InputRequired(), Length(min=4, max=15)]
    )
    client_id = StringField(
        "client_id", validators=[InputRequired(), Length(min=4, max=15)]
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
    query = StringField("Query", validators=[DataRequired()])
    sort = SelectField(
        "Sort",
        choices=[
            ("relevance", "Relevance"),
            ("hot", "Hot"),
            ("top", "Top"),
            ("new", "New"),
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
