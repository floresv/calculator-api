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
    # token_hash = db.Column(db.String(255), nullable=True)
    records = db.relationship("Record", back_populates="user")
    balance = db.Column(db.Float, default=0, nullable=False)

    def __init__(
        self,
        username: str,
        password: str | None = None,
        status: int = 1,
        balance: float = 100.0,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ):
        super().__init__(created_at, updated_at)
        self.username = username
        self.set_password(password)
        self.status = status
        self.balance = balance

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
            "balance": self.get_balance(),
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_balance(self):
        return self.balance

    def charge_operation(self, operation: Operation):
        if self.get_balance() < operation.cost:
            raise BadRequestException("You can't add a record with a negative amount")
        self.balance = self.get_balance() - operation.cost
        return self.balance

    def add_record(self, operation: Operation, result: float):
        record = Record(
            user_id=self.id,
            operation_id=operation.id,
            amount=operation.cost,
            user_balance=self.get_balance(),
            operation_response=result
        )
        if self.id != record.user_id:
            raise UnauthorizedException("You can only add records for your own user")
        self.records.append(record)
        return record


from .record import Record
from .operation import Operation
