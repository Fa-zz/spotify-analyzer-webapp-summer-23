import os
# TODO: For artists you can sort by popularity, # albums, and possibly audio features?. For tracks you can sort by popularity, release date, audio features
# TODO: Tooltip customization for hovering over what user is sorting by.
# TODO: Tooltip customization for hovering over each artist(shows recently played songs).
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
