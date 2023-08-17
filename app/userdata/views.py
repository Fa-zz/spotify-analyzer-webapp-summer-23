import requests
from flask import redirect, request, session, url_for, render_template, current_app
from .forms import DropdownForm, DD_TYPE_CHOICES, DD_TIME_FRAME_CHOICES
from . import userdata
import spotipy


def top_tracks_data_clean(data, sort_by):
    track_dict = {}
    sorted_track_dict = {}
    for i, item in enumerate(data['items']):
        track_name = item['name']
        track_dict[track_name] = [item['artists'][0]['name']]
        track_dict[track_name].append(item['popularity'])
        if sort_by == "popularity":
            sorted_track_dict = dict(sorted(track_dict.items(), key=lambda item: item[1][1], reverse=True))
        else:
            sorted_track_dict = track_dict

        sorted_track_dict[track_name].append(item['album']['images'][2]['url'])

    return sorted_track_dict


def top_artist_data_clean(data, sort_by):
    artist_dict = {}
    sorted_artist_dict = {}
    for i, item in enumerate(data['items']):
        name = item['name']
        artist_dict[name] = [item['popularity']]
        if sort_by == "popularity":
            sorted_artist_dict = dict(sorted(artist_dict.items(), key=lambda item: item[1], reverse=True))
        else:
            sorted_artist_dict = artist_dict

        sorted_artist_dict[name].append(item['images'][2]['url'])

    return sorted_artist_dict



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
    sorted_track_dict = top_tracks_data_clean(track_results, sort_by)
    string = f"Your Most Streamed {type.capitalize()} of {time_frame}."

    if sort_by == "unsorted":
        string = string + f" Sorted by Your Listens"
    else:
        string = string + f" Sorted by {sort_by.capitalize()}"

    return render_template('userdata/profile.html',
                           form=my_form,
                           string=string,
                           type=type,
                           user=spotify.me()['display_name'],
                           followers=spotify.me()['followers']['total'],

                           artist_dict=sorted_artist_dict,
                           track_dict=sorted_track_dict
                        )

