from flask import redirect, request, session, url_for, render_template, jsonify
from .forms import DropdownForm
from . import userdata
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def split_into_lists(sortedDict):
    item_list = []
    img_list = []
    url_list = []
    for key, values in sortedDict.items():
        item_list.append(key)
        img_list.append(values[-1])
        url_list.append(values[-2])

    return item_list, img_list, url_list

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

        sorted_track_dict[track_name].append(item['external_urls']['spotify'])
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

        sorted_artist_dict[name].append(item['external_urls']['spotify'])
        sorted_artist_dict[name].append(item['images'][2]['url'])

    return sorted_artist_dict


# TODO: Hover link to spotify
# TODO: For artists you can sort by popularity, # albums, and possibly audio features?. For tracks you can sort by popularity, release date, audio features
@userdata.route('/profile', methods=['GET', 'POST'])
def profile():
    client_credentials_manager = SpotifyClientCredentials()
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager, client_credentials_manager=client_credentials_manager)

    my_form = DropdownForm()

    if request.method == 'POST' and \
            ('none' not in request.form.get('dd_type') and 'none' not in request.form.get('dd_time_frame') and 'none' not in request.form.get('dd_sort')):
        selected_dd_type = request.form.get('dd_type')
        selected_dd_time_frame = request.form.get('dd_time_frame')
        selected_dd_sort = request.form.get('dd_sort')

        if selected_dd_time_frame == 'short_term':
            time_frame = 'Four Weeks'
        elif selected_dd_time_frame == 'medium_term':
            time_frame = 'Six Months'
        elif selected_dd_time_frame == 'long_term':
            time_frame = 'All time'
        else:
            time_frame = 'short_term'

        if time_frame != "All time":
            time_frame = " the Past " + time_frame

        if selected_dd_type == 'artists':
            artist_results = spotify.current_user_top_artists(time_range=selected_dd_time_frame, limit=50)
            sortedDict = top_artist_data_clean(artist_results, selected_dd_sort)
        else:
            track_results = spotify.current_user_top_tracks(time_range=selected_dd_time_frame, limit=50)
            sortedDict = top_tracks_data_clean(track_results, selected_dd_sort)

        itemList, imgList, urlList = split_into_lists(sortedDict)

        # Prepare string
        string = f"Your Most Streamed {selected_dd_type.capitalize()} of {time_frame}."
        if selected_dd_sort == "unsorted":
            string += " Sorted by Your Listens."
        else:
            string += f" Sorted by {selected_dd_sort.capitalize()}."
        string += " Hover for a link to Spotify"

        content = render_template('userdata/profile_update.html',
                               string=string,
                               itemList=itemList,
                               imgList=imgList,
                               urlList=urlList)
        return jsonify({'content': content})
    else:
        print("Form did not submit")
        string_top = 'Customize the data using the dropdown menu.'

        return render_template('userdata/profile.html',
                               string_top=string_top,
                               form=my_form,
                               user=spotify.me()['display_name'],
                               followers=spotify.me()['followers']['total'],
                               )
