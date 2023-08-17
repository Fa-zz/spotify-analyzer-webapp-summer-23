import requests
from flask import redirect, request, session, url_for, render_template, current_app
from .forms import DropdownForm, DD_TYPE_CHOICES, DD_TIME_FRAME_CHOICES
from . import userdata
import spotipy


def top_tracks_data_clean(data):
    track_names = []
    artist_names = {}
    img_urls = {}
    pops = {}
    for i, item in enumerate(data['items']):
        name = item['name']
        track_names.append(name)
        artist_names[name] = item['artists'][0]['name']
        img_urls[name] = item['album']['images'][2]['url']
        pops[name] = item['popularity']
    return track_names, artist_names, img_urls, pops


def top_artist_data_clean(data, sort_by):
    # Find urls for artists only after sorting
    names = []
    img_urls = []
    pops = {}
    artist_dict = {}
    for i, item in enumerate(data['items']):
        name = item['name']
        artist_dict[name] = [item['popularity']]
        if sort_by == "popularity":
            sorted_artist_dict = dict(sorted(artist_dict.items(), key=lambda item: item[1], reverse=True))
        else:
            sorted_artist_dict = artist_dict

        sorted_artist_dict[name].append(item['images'][2]['url'])
        # result_dict = {key: [value] for key, value in list_of_tuples}

    return sorted_artist_dict


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

#TODO: Hover link to spotify
#TODO: For artists you can sort by popularity, # albums, and possibly audio features?. For tracks you can sort by popularity, release date, audio features
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
        range_to_get = my_form.dd_time_frame.data
        sort_by = my_form.dd_sort.data
        print(type, range_to_get, sort_by)
    else:
        print("Form did not submit")
        type = "Artists"
        range_to_get = "short_term"
        sort_by = "unsorted"

    if range_to_get == 'short_term':
        time_frame = 'Four Weeks'
    elif range_to_get == 'medium_term':
        time_frame = 'Six Months'
    elif range_to_get == 'long_term':
        time_frame = 'All time'
    else:
        time_frame = 'short_term'

    if time_frame != "All time":
        time_frame = " the Past " + time_frame

    string = ""

    artist_results = spotify.current_user_top_artists(time_range=range_to_get, limit=50)
    sorted_artist_dict = top_artist_data_clean(artist_results, sort_by)
    track_results = spotify.current_user_top_tracks(time_range=range_to_get, limit=50)
    track_names, track_artist_names, track_imgs, track_pops = top_tracks_data_clean(track_results)
    string = f"Your Most Streamed {type.capitalize()} of {time_frame}."

    if sort_by == "unsorted":
        string = string + f" Sorted by Listens"
    else:
        string = string + f" Sorted by {sort_by.capitalize()}"

    return render_template('userdata/profile.html',
                           form=my_form,
                           string=string,
                           type=type,
                           user=spotify.me()['display_name'],
                           followers=spotify.me()['followers']['total'],

                           artist_dict=sorted_artist_dict,

                           track_names=track_names,
                           track_artist_names=track_artist_names,
                           track_imgs=track_imgs,
                           track_pops=track_pops,
                        )

