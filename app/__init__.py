from flask import Flask
from flask_bootstrap import Bootstrap
import config
from flask_session import Session

# App factory


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)
    # config[config_name].init_app(app)

    bootstrap = Bootstrap(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .userdata import userdata as user_data_blueprint
    app.register_blueprint(user_data_blueprint, url_prefix='/userdata')

    return app
