from flask import render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user
from app import app, db, bcrypt
from app.models import User, API_Key
from app.forms import RegisterForm, LoginForm, API_Form


@app.route("/")
def index():
    verify_api_key = API_Key.query.first()
    if verify_api_key:
        return redirect(url_for("login"))
    elif not verify_api_key:
        return redirect(url_for("api_key"))
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("dashboard"))
        return render_template("dashboard.html", form=form, invalid=True)
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/api_key", methods=["GET", "POST"])
def api_key():
    form = API_Form()
    if form.validate_on_submit():
        new_api_key = API_Key(
            user_agent=form.user_agent.data,
            client_secret=form.client_secret.data,
            client_id=form.client_id.data,
        )
        db.session.add(new_api_key)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("api-key.html", form=form)
