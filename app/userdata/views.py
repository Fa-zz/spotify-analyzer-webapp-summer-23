import requests
from flask import redirect, request, session, url_for, render_template, current_app
from .forms import DropdownForm, DD_TYPE_CHOICES, DD_NUMBER_CHOICES, DD_TIME_FRAME_CHOICES
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
    image_info = {}
    for item in data['items']:
        names.append(item['name'])
        image_info[item['name']] = (item['images'][2])
    return names, image_info


def get_data(type, number_disp, time_frame):
    access_token = session.get('access_token')
    if access_token:
        headers = {'Authorization': f'Bearer {access_token}'}
    else:
        return False

    if time_frame == 'Four weeks':
        time = 'short_term'
    elif time_frame == 'Six months':
        time = 'medium_term'
    elif time_frame == 'All time':
        time = 'long_term'
    else:
        return False

    type = type.lower()

    data_request_url = f'https://api.spotify.com/v1/me/top/{type}?time_range={time}&limit={number_disp}&offset=0'

    info = requests.get(
        data_request_url, headers=headers)
    # user_info = requests.get(
    #     'https://api.spotify.com/v1/me', headers=headers).json()

    print(type, info)

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

    return True


@userdata.route('/profile', methods=['GET', 'POST'])
def profile():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    return spotify.current_user_top_artists()

    my_form = DropdownForm()
    if my_form.validate_on_submit():
        type = my_form.get_choice_label(DD_TYPE_CHOICES, my_form.dd_type.data)
        number_disp = int(my_form.get_choice_label(DD_NUMBER_CHOICES, my_form.dd_number.data))
        time_frame = my_form.get_choice_label(DD_TIME_FRAME_CHOICES, my_form.dd_time_frame.data)
        print(f'Number to display: {number_disp}')
        print(f'Time frame: {time_frame}')
    else:
        print("Form did not submit")
        type = "Artists"
        number_disp = int(5)
        time_frame = "Four weeks"

    got_data = get_data(type, number_disp, time_frame)

    if time_frame != "All time":
        time_frame = " the Past " + time_frame

    string = f"Your Top {number_disp} Most Streamed {type} of {time_frame}"

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
