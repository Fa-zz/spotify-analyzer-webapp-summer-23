from flask import Blueprint

user_data = Blueprint('userdata', __name__)

from . import views