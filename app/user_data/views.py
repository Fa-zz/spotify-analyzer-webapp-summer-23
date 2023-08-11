import requests
from flask import redirect, request, session, url_for, render_template, current_app
from .forms import DropdownForm, DD_NUMBER_CHOICES, DD_TIME_FRAME_CHOICES
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
    my_form = DropdownForm()
    if my_form.validate_on_submit():
        number_disp = my_form.get_choice_label(DD_NUMBER_CHOICES, my_form.dd_number.data)
        time_frame = my_form.get_choice_label(DD_TIME_FRAME_CHOICES, my_form.dd_time_frame.data)
        print(f'Number to display: {number_disp}')
        print(f'Time frame: {time_frame}')
    else:
        print("Form did not submit")
        number_disp = int(5)
        time_frame = "Four weeks"

    access_token = session.get('access_token')
    if access_token:
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        if 'visits' in session:
            session['visits'] = session.get('visits') + 1  # reading and updating session data
            user_data_response = requests.get('https://api.spotify.com/v1/me', headers=headers)
            user_data = user_data_response.json()
            top_artist_response = requests.get('https://api.spotify.com/v1/me/top/artists?time_range=short_term&limit=15&offset=0', headers=headers)
            top_artist_data = top_artist_response.json()
            artist_names, artist_img_infos = top_artist_data_clean(top_artist_data)
            session['usr_name'] = user_data['display_name']
            session['followers'] = user_data['followers']['total']
            session['artists'] = artist_names
            session['artist_img_infos'] = artist_img_infos
        else:
            session['visits'] = 1  # setting session data

        return render_template('user_data/profile.html',
                               form=my_form,
                               usr=session['usr_name'],
                               followers=session['followers'],
                               artists=session['artists'],
                               img_infos=session['artist_img_infos'])
    else:
        return 'You are not logged in.'