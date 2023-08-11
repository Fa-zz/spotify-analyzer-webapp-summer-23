import requests
from urllib.parse import urlencode
from flask import Flask, redirect, request, session, url_for, current_app
from . import user_data

@user_data.route('/login', methods=['GET', 'POST'])
def login():
    auth_params = {
        'client_id': current_app.config['CLIENT_ID'],
        'response_type': 'code',
        'redirect_uri': current_app.config['REDIRECT_URI'],
        'scope': current_app.config['SCOPE'],
    }
    authorization_url = current_app.config['AUTH_URL'] + '?' + urlencode(auth_params)
    return redirect(authorization_url)


@user_data.route('/callback', methods=['GET', 'POST'])
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

    # Store access_token in session or database
    session['access_token'] = access_token

    return redirect(url_for('user_data.profile'))


@user_data.route('/profile')
def profile():
    access_token = session.get('access_token')
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_data_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        user_data = user_data_response.json()
        return f'Hello, {user_data["display_name"]}!'
    else:
        return 'You are not logged in.'