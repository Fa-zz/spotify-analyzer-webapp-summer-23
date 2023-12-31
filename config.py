import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # CLIENT_ID = os.environ.get('CLIENT_ID') or ''
    # CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or ''
    SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI') or 'http://127.0.0.1:5000/'
    SCOPE = 'user-top-read'
    AUTH_URL = os.environ.get('AUTH_URL') or 'https://accounts.spotify.com/authorize'
    TOKEN_URL = os.environ.get('TOKEN_URL') or 'https://accounts.spotify.com/api/token'
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './.flask_session/'


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
