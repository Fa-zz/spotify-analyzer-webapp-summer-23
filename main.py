import os
# TODO: For artists you can sort by popularity, # albums, and possibly audio features?. For tracks you can sort by popularity, release date, audio features
# TODO: Hover over audio features in string to get an explanation for what they are.
# TODO: Hovering over artists shows a recently played song from them that you like.
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
