from __future__ import annotations
from datetime import datetime
from flask import current_app
from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base
from .. import db
from ..api.common.utils.exceptions import UnauthorizedException, BadRequestException


class User(Base):
    """
    User model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    token_hash = db.Column(db.String(255), nullable=True)

    def __init__(self,
                 username: str,
                 password: str = None,
                 active: bool = True,
                 created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now(),
                 **kwargs):
        super().__init__(created_at, updated_at)
        self.email = email
        self.username = username
        self.name = name
        # if password:
        #     self.password = bcrypt.generate_password_hash(password,
        #                                                   current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.active = active

    def json(self) -> json:
        """
        Get user data in JSON format
        """
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'name': self.name,
            'active': self.active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
