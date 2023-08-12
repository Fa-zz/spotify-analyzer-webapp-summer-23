import requests
from urllib.parse import urlencode
from flask import render_template, redirect, request, session, url_for, current_app
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    auth_params = {
        'client_id': current_app.config['CLIENT_ID'],
        'response_type': 'code',
        'redirect_uri': current_app.config['REDIRECT_URI'],
        'scope': current_app.config['SCOPE'],
    }
    authorization_url = current_app.config['AUTH_URL'] + '?' + urlencode(auth_params)
    return redirect(authorization_url)


@main.route('/callback', methods=['GET', 'POST'])
def callback():
    auth_code = request.args.get('code')
    token_params = {
        'client_id': current_app.config['CLIENT_ID'],
        'client_secret': current_app.config['CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': current_app.config['REDIRECT_URI'],
    }
    response = requests.post(current_app.config['TOKEN_URL'], data=token_params)
    token_data = response.json()
    access_token = token_data.get('access_token')

    assert access_token

    # Store access_token in session or database
    session['access_token'] = access_token

    return redirect(url_for('userdata.profile'))