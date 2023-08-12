import os
import requests
from urllib.parse import urlencode

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# basedir = os.path.abspath(os.path.dirname(__file__))
#
# # Spotify API credentials
# CLIENT_ID = os.environ.get('CLIENT_ID')
# CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
# REDIRECT_URI = 'http://localhost:8888/callback'  # Replace with your Redirect URI
#
# # Step 1: Obtain Authorization Code
# auth_url = 'https://accounts.spotify.com/authorize'
# auth_params = {
#     'client_id': CLIENT_ID,
#     'response_type': 'code',
#     'redirect_uri': REDIRECT_URI,
#     'scope': 'user-top-read',  # Desired scopes
# }
#
# authorization_url = auth_url + '?' + urlencode(auth_params)
# print("Please visit the following URL to authorize your app:")
# print(authorization_url)
# authorization_code = input("Enter the authorization code: ")
#
# # Step 2: Exchange Authorization Code for Access Token
# token_url = 'https://accounts.spotify.com/api/token'
# token_params = {
#     'client_id': CLIENT_ID,
#     'client_secret': CLIENT_SECRET,
#     'grant_type': 'authorization_code',
#     'code': authorization_code,
#     'redirect_uri': REDIRECT_URI,
# }
#
# response = requests.post(token_url, data=token_params)
# token_data = response.json()
#
# access_token = token_data.get('access_token')
# refresh_token = token_data.get('refresh_token')
#
# # Step 3: Use the Access Token to Make API Requests
# api_url = 'https://api.spotify.com/v1/me'
# headers = {
#     'Authorization': f'Bearer {access_token}'
# }
#
# response = requests.get(api_url, headers=headers)
# userdata = response.json()
#
# print("User's Spotify display name:", userdata.get('display_name'))
