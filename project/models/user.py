from __future__ import annotations
from datetime import datetime
from flask import current_app
from sqlalchemy.ext.associationproxy import association_proxy

from .base import Base
from .. import db, bcrypt
from ..api.common.utils.exceptions import UnauthorizedException, BadRequestException


class User(Base):
    """
    User model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.Integer, default=UserRole.USER.value, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    token_hash = db.Column(db.String(255), nullable=True)
    email_token_hash = db.Column(db.String(255), nullable=True)
    email_validation_date = db.Column(db.DateTime, nullable=True)

    # Social
    social_id = db.Column(db.String(128), unique=True, nullable=True)
    social_type = db.Column(db.String(64), default=None, nullable=True)
    social_access_token = db.Column(db.String, nullable=True)

    # Foreign relationships
    associated_groups = db.relationship("UserGroupAssociation", back_populates="user")
    groups = association_proxy('associated_groups', 'group')

    def __init__(self,
                 email: str,
                 username: str,
                 password: str = None,
                 name: str = None,
                 active: bool = True,
                 email_validation_date: datetime = None,
                 social_id: str = None,
                 social_access_token: str = None,
                 created_at: datetime = datetime.now(),
                 updated_at: datetime = datetime.now(),
                 **kwargs):
        super().__init__(created_at, updated_at)
        self.email = email
        self.username = username
        self.name = name
        if password:
            self.password = bcrypt.generate_password_hash(password,
                                                          current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
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