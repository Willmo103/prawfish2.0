import os
from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)



app.get('/')
def index():

    # check to see if the reddit api_key, client_id, and client_secret are set
    # render a form to get the api_key, client_id, and client_secret before continuing

    if not all(['api_key', 'client_id', 'client_secret']) in os.environ:
        return render_template('form.html')

    # once the environment variables are set, the user needs to be redirected to login page

    if not 'access_token' in os.environ:
        return redirect(url_for('login'))


    return render_template('index.html')
