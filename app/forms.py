from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
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
    submit = SubmitField("Login")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if not existing_user_username:
            raise ValidationError("That username does not exist. Please try again.")


class API_Form(FlaskForm):
    user_agent = StringField(
        "api_key", validators=[InputRequired(), Length(min=4, max=15)]
    )
    client_secret = StringField(
        "client_secret", validators=[InputRequired(), Length(min=4, max=15)]
    )
    client_id = StringField(
        "client_id", validators=[InputRequired(), Length(min=4, max=15)]
    )

    def validate_api_key(self, api_key):
        existing_api_key = API_Key.query().first()
        if existing_api_key:
            raise ValidationError(
                "That API key already exists. Please choose a different one."
            )
