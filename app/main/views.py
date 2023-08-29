import requests
from urllib.parse import urlencode
from flask import render_template, redirect, request, session, url_for, current_app
from . import main
import spotipy


@main.route('/')
def index():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope=current_app.config['SCOPE'],
                                               redirect_uri=current_app.config['SPOTIPY_REDIRECT_URI'],
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect(url_for('main.index'))

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        session.clear()
        auth_url = auth_manager.get_authorize_url()
        return render_template('index.html', auth_url=auth_url)

    # Step 3. Signed in, display data
    session['display_graph'] = False
    return redirect(url_for('userdata.profile'))

# @main.route('/callback', methods=['GET', 'POST'])
# def callback():
#     cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
#     auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
#     if not auth_manager.validate_token(cache_handler.get_cached_token()):
#         return redirect('/')

# auth_code = request.args.get('code')
# token_params = {
#     'client_id': current_app.config['CLIENT_ID'],
#     'client_secret': current_app.config['CLIENT_SECRET'],
#     'grant_type': 'authorization_code',
#     'code': auth_code,
#     'redirect_uri': current_app.config['REDIRECT_URI'],
# }
# response = requests.post(current_app.config['TOKEN_URL'], data=token_params)
# token_data = response.json()
# access_token = token_data.get('access_token')
#
# assert access_token
#
# # Store access_token in session or database
# session['access_token'] = access_token
#
# return redirect(url_for('userdata.profile'))
