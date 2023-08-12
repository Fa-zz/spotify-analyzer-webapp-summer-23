from flask_wtf import FlaskForm
from wtforms import SelectField
DD_TYPE_CHOICES = [('artists', 'Artists'), ('tracks', 'Tracks')]
DD_NUMBER_CHOICES = [('disp_5', '5'), ('disp_10', '10'), ('disp_15', '15')]
DD_TIME_FRAME_CHOICES = [('short_term', 'Four weeks'), ('medium_term', 'Six months'), ('long_term', 'All time')]


class DropdownForm(FlaskForm):
    dd_type = SelectField('Type', choices=DD_TYPE_CHOICES)
    dd_number = SelectField('# to Display', choices=DD_NUMBER_CHOICES)
    dd_time_frame = SelectField('Of the past...', choices=DD_TIME_FRAME_CHOICES)

    def get_choice_label(self, choices, value):
        return dict(choices).get(value, 'Unknown')