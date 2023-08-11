from flask import Blueprint

user_data = Blueprint('user_data', __name__)

from . import views