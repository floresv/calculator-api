from flask import request, current_app, jsonify
from sqlalchemy import exc, text
from pydantic import BaseModel, ValidationError
from typing import Type

from ...models.base import Base
from ... import db
from ..common.utils.exceptions import (
    NotFoundException,
    InvalidPayloadException,
    BadRequestException,
    ValidationException,
)
from ..common.utils.helpers import session_scope


class BaseAPI:
    def post(self):
        """Standard POST call"""
        post_data = "X"
