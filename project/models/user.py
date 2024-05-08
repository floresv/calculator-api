from __future__ import annotations
from datetime import datetime
from flask import current_app
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash
from .base import Base
from .. import db
from ..api.common.utils.exceptions import UnauthorizedException, BadRequestException


class User(Base):
    """
    User model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, default=True, nullable=False)
    token_hash = db.Column(db.String(255), nullable=True)

    def __init__(
        self,
        username: str,
        password: str | None = None,
        status: int = 1,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ):
        super().__init__(created_at, updated_at)
        self.username = username
        self.set_password(password)
        self.status = status

    def json(self) -> dict:
        """
        Get user data in JSON format
        """
        return {
            "id": self.id,
            "username": self.username,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "balance": self.get_balance()
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_balance(self):
        return 0
