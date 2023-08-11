from flask import Flask
import config

# App factory


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)
    # config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user_data import user_data as user_data_blueprint
    app.register_blueprint(user_data_blueprint, url_prefix='/userdata')

    return app