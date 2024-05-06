from flask import request, current_app, jsonify, Blueprint
from flask_accept import accept
from sqlalchemy import exc
from pydantic import ValidationError

from .... import db
from ....api.common.utils.exceptions import InvalidPayloadException, \
    NotFoundException, ServerErrorException, ValidationException
from ....models.user import User
from ....api.common.utils.helpers import session_scope
from ..validations.auth.core import UserRegister, UserLogin

bp = Blueprint("auth", __name__)


@bp.route('/login', methods=['POST'])
@accept('application/json')
def register_user():
    return "Hello, World!"
