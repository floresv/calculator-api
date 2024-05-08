from flask import request, current_app, jsonify
from sqlalchemy import exc, text
from pydantic import BaseModel, ValidationError
from typing import Type
from functools import wraps

from ...models.base import Base
from ...models.user import User
from ... import db
from ..common.utils.exceptions import (
    NotFoundException,
    InvalidPayloadException,
    BadRequestException,
    ValidationException,
)
from ..common.utils.helpers import session_scope
import jwt


class BaseAPI:
    def post(self):
        """Standard POST call"""
        post_data = "X"


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        authorization = request.headers.get('Authorization')
        if not authorization or not authorization.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid token'}), 401

        try:
            token = authorization.split()[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.DecodeError:
            return jsonify({'error': 'Invalid token'}), 403

        current_user = User.query.filter_by(username=data['username']).first()

        if not current_user:
            return jsonify({'error': 'User not found'}), 401

        return func(current_user, *args, **kwargs)

    return decorated
