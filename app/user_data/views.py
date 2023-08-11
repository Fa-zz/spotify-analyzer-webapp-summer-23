import requests
from flask import redirect, request, session, url_for, render_template, current_app
from . import user_data


def top_artist_data_clean(data):
    names = []
    image_info = {}
    for item in data['items']:
        names.append(item['name'])
        image_info[item['name']] = (item['images'][1])
    return names, image_info

@user_data.route('/profile', methods=['GET', 'POST'])
def profile():
    access_token = session.get('access_token')
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_data_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
        user_data = user_data_response.json()
        top_artist_response = requests.get('https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=15&offset=0', headers=headers)
        top_artist_data = top_artist_response.json()
        artist_names, artist_img_infos = top_artist_data_clean(top_artist_data)

        return render_template('user_data/profile.html',
                               usr=user_data['display_name'],
                               followers=user_data['followers']['total'],
                               artists=artist_names,
                               img_infos=artist_img_infos)
    else:
        return 'You are not logged in.'