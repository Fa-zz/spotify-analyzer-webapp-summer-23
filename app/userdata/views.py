from flask import redirect, request, session, url_for, render_template, jsonify
from .forms import DropdownForm
from . import userdata
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def split_into_lists(full_list):
    item_list = []
    img_list = []
    url_list = []
    for artist in full_list:
        name = artist['name']
        spotify_url = artist['spotify_url']
        img_url = artist['img_url']

        item_list.append(name)
        img_list.append(img_url)
        url_list.append(spotify_url)

    return item_list, img_list, url_list


def top_data_clean(data, sort_by, type):
    full_list = []
    if type == 'artists':
        for i, item in enumerate(data['items']):
            name = item['name']
            artist_dict = {'name': name,
                           'popularity': item['popularity'],
                           'spotify_url': item['external_urls']['spotify'],
                           'img_url': item['images'][2]['url']
                           }
            full_list.append(artist_dict)

    elif type == 'tracks':
        for i, item in enumerate(data['items']):
            track_name = item['name']
            track_dict = {'name': track_name,
                          'artist_name': item['artists'][0]['name'],
                          'popularity': item['popularity'],
                          'spotify_url': item['external_urls']['spotify'],
                          'img_url': item['album']['images'][2]['url']
                          }
            full_list.append(track_dict)

    if sort_by == "popularity":
        # Sort the list of dictionaries by 'popularity' in descending order
        full_list = sorted(full_list, key=lambda x: x['popularity'], reverse=True)

    return full_list


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
            ('none' not in request.form.get('dd_type') and 'none' not in request.form.get(
                'dd_time_frame') and 'none' not in request.form.get('dd_sort')):
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
            results = spotify.current_user_top_artists(time_range=selected_dd_time_frame, limit=50)
        else:
            results = spotify.current_user_top_tracks(time_range=selected_dd_time_frame, limit=50)

        full_list = top_data_clean(results, selected_dd_sort, selected_dd_type)

        print(full_list)  # Obtains each artist
        item_list, img_list, url_list = split_into_lists(full_list)

        # Prepare string
        string = f"Your Most Streamed {selected_dd_type.capitalize()} of {time_frame}."
        if selected_dd_sort == "unsorted":
            string += " Sorted by Your Listens."
        else:
            string += f" Sorted by {selected_dd_sort.capitalize()}."
        string += " Hover for a link to Spotify"

        content = render_template('userdata/profile_update.html',
                                  string=string,
                                  item_list=item_list,
                                  img_list=img_list,
                                  url_list=url_list)
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
