from flask_wtf import FlaskForm
from wtforms import SelectField
DD_TYPE_CHOICES = [('none', '---'), ('artists', 'Artists'), ('tracks', 'Tracks')]
DD_TIME_FRAME_CHOICES = [('none', '---'), ('short_term', 'Four weeks'), ('medium_term', 'Six months'), ('long_term', 'All time')]
DD_SORT_CHOICES = [('none', '---'), ('your listens', 'Listens'), ('popularity', 'Popularity')]

class DropdownForm(FlaskForm):
    dd_type = SelectField('Type', choices=DD_TYPE_CHOICES, default=None)
    dd_time_frame = SelectField('Of the past...', choices=DD_TIME_FRAME_CHOICES, default=None)
    dd_sort = SelectField('Sort by', choices=DD_SORT_CHOICES, default=None)