from flask import jsonify, Blueprint
from flask_accept import accept
from flask.views import MethodView

from ..base import BaseAPI
from ....models.user import User
from ...common.utils.exceptions import NotImplementedException

user_blueprint = Blueprint('user', __name__)
