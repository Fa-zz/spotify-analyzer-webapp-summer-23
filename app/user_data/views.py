import requests
from flask import redirect, request, session, url_for, render_template, current_app
from .forms import DropdownForm, DD_NUMBER_CHOICES, DD_TIME_FRAME_CHOICES
from . import user_data


def top_artist_data_clean(data):
    names = []
    image_info = {}
    for item in data['items']:
        names.append(item['name'])
        image_info[item['name']] = (item['images'][2])
    return names, image_info


def get_data(top_artist, number_disp, time_frame):
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

    if top_artist:
        finding = 'artists'
    else:
        finding = 'tracks'

    data_request_url = f'https://api.spotify.com/v1/me/top/{finding}?time_range={time}&limit={number_disp}&offset=0'

    # short_15_top_artist = requests.get(
    # 'https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=15&offset=0', headers=headers).json()

    info = requests.get(
        data_request_url, headers=headers).json()
    user_info = requests.get(
        'https://api.spotify.com/v1/me', headers=headers).json()

    if finding == 'tracks':
        print(info)

    artist_names, artist_img_infos = top_artist_data_clean(info)

    session['user_name'] = user_info['display_name']
    session['followers'] = user_info['followers']['total']

    session['artists'] = artist_names
    session['artist_img_infos'] = artist_img_infos

    return True


@user_data.route('/profile', methods=['GET', 'POST'])
def profile():
    my_form = DropdownForm()
    if my_form.validate_on_submit():
        number_disp = int(my_form.get_choice_label(DD_NUMBER_CHOICES, my_form.dd_number.data))
        time_frame = my_form.get_choice_label(DD_TIME_FRAME_CHOICES, my_form.dd_time_frame.data)
        print(f'Number to display: {number_disp}')
        print(f'Time frame: {time_frame}')
    else:
        print("Form did not submit")
        number_disp = int(5)
        time_frame = "Four weeks"
    top_artist = True

    got_data = get_data(top_artist, number_disp, time_frame)

    if time_frame != "All time":
        time_frame = " the Past " + time_frame

    string = f"Your Top {number_disp} Most Streamed Artists of {time_frame}"

    if got_data:
        return render_template('user_data/profile.html',
                               form=my_form,
                               string=string,
                               usr=session['user_name'],
                               followers=session['followers'],
                               artists=session['artists'][:number_disp],
                               img_infos=session['artist_img_infos'])
    else:
        return 'You are not logged in.'
