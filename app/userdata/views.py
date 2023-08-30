from flask import redirect, request, session, url_for, render_template, jsonify
from .forms import DropdownForm
from . import userdata
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random


def create_colors(genre_list):
    genre_colors = []
    all_colors = [
        "#025669", "#7FB5B5", "#008F39", "#721422", "#F44611", "#606E8C", "#20214F", "#316650",
        "#F5D033", "#D95030", "#5E2129", "#E5BE01", "#84C3BE", "#7D7F7D", "#922B3E", "#A98307",
        "#F4A900", "#AF2B1E", "#00BB2D", "#1E213D", "#9D9101", "#C51D34", "#1E2460", "#308446",
        "#E63244", "#DC9D00", "#13f2d2", "#6C4675", "#FFA420", "#DE4C8A", "#ed4f25", "#EAE6CA",
        "#F3A505", "#8B8C7A", "#FFFF00", "#2A6478", "#3E5F8A", "#C6A664", "#4C9141", "#2E3A23"
    ]
    for genre in genre_list:
        genre_colors.append(random.choice(all_colors))
    genre_colors.append(random.choice(all_colors))
    return genre_colors


def count_genres(full_list):
    genres_counted = {}
    for artist in full_list:
        genres_list = artist['genres']

        for genre in genres_list:
            if genre not in genres_counted:
                genres_counted[genre] = 1
            else:
                genres_counted[genre] += 1

    return genres_counted


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
                           'img_url': item['images'][2]['url'],
                           'genres': item['genres']
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


def string_config(selected_dd_type, selected_dd_time_frame, selected_dd_sort):
    # String configuration
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

    # Prepare string
    string = f"Your Most Streamed {selected_dd_type.capitalize()} of {time_frame}."
    if selected_dd_sort == "unsorted":
        string += " Sorted by Your Listens."
    else:
        string += f" Sorted by {selected_dd_sort.capitalize()}."

    return string


@userdata.route('/profile', methods=['GET', 'POST'])
def profile():
    client_credentials_manager = SpotifyClientCredentials()
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager, client_credentials_manager=client_credentials_manager)

    my_form = DropdownForm()

    # TODO: Once dropdown for recommendations exists, check for this and pass to AJAX call.
    if request.method == 'POST' and \
            ('none' not in request.form.get('dd_type') and 'none' not in request.form.get(
                'dd_time_frame') and 'none' not in request.form.get('dd_sort')):
        # User selections on each dropdown
        selected_dd_type = request.form.get('dd_type')
        selected_dd_time_frame = request.form.get('dd_time_frame')
        selected_dd_sort = request.form.get('dd_sort')

        # Obtain and clean top data
        if selected_dd_type == 'artists':
            results = spotify.current_user_top_artists(time_range=selected_dd_time_frame, limit=50)
        else:
            results = spotify.current_user_top_tracks(time_range=selected_dd_time_frame, limit=50)

        full_list = top_data_clean(results, selected_dd_sort, selected_dd_type)

        # print(full_list)  # Obtains each artist
        item_list, img_list, url_list = split_into_lists(full_list)

        # If artist, obtain and count genres
        if selected_dd_type == 'artists' and not session['display_graph'] or \
                not(session['time'] == selected_dd_time_frame):
            genres_counted = count_genres(full_list)
            # Split genre list, number of each, and colors for each genre into lists
            session['genre_list'] = list(genres_counted.keys())
            session['genre_counts'] = list(genres_counted.values())
            session['genre_colors'] = create_colors(session['genre_list'])
            session['display_graph'] = True
            session['time'] = selected_dd_time_frame
            print(session['genre_list'], session['genre_counts'], session['genre_colors'])

        content = render_template('userdata/profile_top_update.html',
                                  string=string_config(selected_dd_type, selected_dd_time_frame, selected_dd_sort),
                                  item_list=item_list,
                                  img_list=img_list,
                                  url_list=url_list,
                                  )

        if session['display_graph']:
            response_data = {
                'content': content,
                'displayGraph': session['display_graph'],
                'genreList': session['genre_list'],
                'genreCounts': session['genre_counts'],
                'genreColors': session['genre_colors']
            }
        # TODO: Append 'recommend' to dictionary if it exists
        else:
            response_data = {
                'content': content,
                'displayGraph': [],
                'genreList': [],
                'genreCounts': [],
                'genreColors': []
            }

        return jsonify(response_data)

    else:
        print("Form did not submit")
        string_top = 'Customize the data using the dropdown menu.'

        return render_template('userdata/profile.html',
                               string_top=string_top,
                               form=my_form,
                               user=spotify.me()['display_name'],
                               followers=spotify.me()['followers']['total']
                               )
