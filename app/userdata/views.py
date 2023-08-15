import requests
from flask import redirect, request, session, url_for, render_template, current_app
from .forms import DropdownForm, DD_TYPE_CHOICES, DD_TIME_FRAME_CHOICES
from . import userdata
import spotipy


def top_tracks_data_clean(data):
    track_names = []
    popularities = []
    artist_names = []
    image_info = []

    for item in data['items']:
        track_names.append(item['name'])
        popularities.append(item['popularity'])
        artist_names.append(item['album']['artists'][0]['name'])
        image_info.append(item['album']['images'][2]['url'])
    print(f"IMAGE INFO: {image_info}")

    return track_names, popularities, artist_names, image_info


def top_artist_data_clean(data):
    names = []
    img_urls = {}
    pops = {}
    for i, item in enumerate(data['items']):
        names.append(item['name'])
        img_urls[item['name']] = item['images'][2]['url']
        pops[item['name']] = item['popularity']
    return names, img_urls, pops


# def get_data(type, number_disp, time_frame):
#     access_token = session.get('access_token')
#     if access_token:
#         headers = {'Authorization': f'Bearer {access_token}'}
#     else:
#         return False
#
#     if time_frame == 'Four weeks':
#         time = 'short_term'
#     elif time_frame == 'Six months':
#         time = 'medium_term'
#     elif time_frame == 'All time':
#         time = 'long_term'
#     else:
#         return False
#
#     type = type.lower()
#
#     data_request_url = f'https://api.spotify.com/v1/me/top/{type}?time_range={time}&limit={number_disp}&offset=0'
#
#     info = requests.get(
#         data_request_url, headers=headers)
#     # user_info = requests.get(
#     #     'https://api.spotify.com/v1/me', headers=headers).json()
#
#     print(type, info)

    # session['user_name'] = user_info['display_name']
    # session['followers'] = user_info['followers']['total']
    # if type == 'artists':
    #     session['artists'], \
    #     session['artist_img_infos'] \
    #         = top_artist_data_clean(info)
    #     session['track_names'] = ''
    #     session['track_popularities'] = ''
    #     session['artist_names'] = ''
    #     session['image_info'] = ''
    #
    # elif type == 'tracks':
    #     session['track_names'], \
    #     session['track_popularities'], \
    #     session['artist_names'], \
    #     session['image_info'] \
    #         = top_tracks_data_clean(info)

    # return True


@userdata.route('/profile', methods=['GET', 'POST'])
def profile():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    my_form = DropdownForm()
    if my_form.is_submitted():
        type = my_form.dd_type.data
        range = my_form.dd_time_frame.data
        print(type, range)
    else:
        print("Form did not submit")
        type = "Artists"
        range = "short_term"

    if range == 'short_term':
        time_frame = 'Four Weeks'
    elif range == 'medium_term':
        time_frame = 'Six Months'
    elif range == 'long_term':
        time_frame = 'All time'
    else:
        time_frame = 'short_term'

    if time_frame != "All time":
        time_frame = " the Past " + time_frame

    # got_data = get_data(type, number_disp, time_frame)
    artist_results = spotify.current_user_top_artists(time_range=range, limit=50)
    artist_names, artist_imgs, artist_pops = top_artist_data_clean(artist_results)

    string = f"Your Most Streamed {type.capitalize()} of {time_frame}"
    return render_template('userdata/profile.html',
                           form=my_form,
                           string=string,
                           type=type,
                           user=spotify.me()['display_name'],
                           followers=spotify.me()['followers']['total'],
                           artists=artist_names,
                           artist_imgs=artist_imgs,
                           artist_pops=artist_pops
                           )

    # if got_data:
    #     return "hello"
    #     # return render_template('userdata/profile.html',
    #     #                        form=my_form,
    #     #                        string=string,
    #     #                        type=type,
    #     #                        usr=session['user_name'],
    #     #                        followers=session['followers'],
    #     #
    #     #                        artists=session['artists'][:number_disp],
    #     #                        img_infos=session['artist_img_infos'],
    #     #
    #     #                        track_names=session['track_names'][:number_disp],
    #     #                        popularities=session['track_popularities'][:number_disp],
    #     #                        artist_names=session['artist_names'][:number_disp],
    #     #                        image_info=session['image_info']
    #     #                     )
    # else:
    #     return 'You are not logged in.'
