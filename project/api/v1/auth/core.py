from flask import request, current_app, jsonify, Blueprint
from flask_accept import accept  # type: ignore
from sqlalchemy import exc
from pydantic import ValidationError

from .... import db
from ....api.common.utils.exceptions import InvalidPayloadException, \
    NotFoundException, ServerErrorException, ValidationException
from ....models.user import User
from ....api.common.utils.helpers import session_scope
from ..validations.auth.core import UserRegister, UserLogin
from werkzeug.security import generate_password_hash

bp = Blueprint("auth", __name__)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()  # Validation

    if not user or not user.verify_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate a secure session token (replace with a JWT or similar for more robust authentication)
    session_token = generate_password_hash(f"{username}{password}", method='pbkdf2:sha256', salt_length=8)

    # Return the session token in the response (consider a more secure approach like JWT)
    return jsonify({'session_token': session_token})


@bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'})