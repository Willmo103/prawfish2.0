import os
from flask import Flask, Request, redirect, render_template, url_for

app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'

# this is the database that will store the users and their passwords



@app.route('/')
def index():



    # check to see if the reddit api_key, client_id, and client_secret are set
    # render a form to get the api_key, client_id, and client_secret before continuing

    # if not all(['api_key', 'client_id', 'client_secret']) in os.environ:
    #     return render_template('form.html')

    # once the environment variables are set, the user needs to be redirected to login page

    # if not 'access_token' in os.environ:
    #     return redirect(url_for('login'))

    # if the user is logged in, then the user will be redirected to the main page
    return render_template('index.html')


app.route('/login')
def login():
    # this is the page that will render the login form 'login.html'
    # there will be a option for a new user to create an account

    render_template('login.html')


# this will be the method that will handle the login form
app.route('/login')
def validate_login(request: Request ):
    ...
    return redirect(url_for('index'))

# need to setup db for flask
# need to reasearch how to use flask with a database

if __name__ == '__main__':
    app.run(debug=True)
