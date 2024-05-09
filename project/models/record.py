from __future__ import annotations
from datetime import datetime
from flask import current_app
from sqlalchemy.ext.associationproxy import association_proxy
from .base import Base
from .. import db


class Record(Base):
    """
    User model
    """

    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, default=True, nullable=False)
    user_balance = db.Column(db.Float, nullable=False)
    operation_response = db.Column(db.String(255), nullable=False)

    # Foreign relationships
    operation_id = db.Column(db.Integer, db.ForeignKey('operations.id'), nullable=False)
    operation = db.relationship("Operation", back_populates="records")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="records")
    
    def __init__(
        self, amount, user_id, operation_id,
        user_balance, operation_response,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ):
        super().__init__(created_at, updated_at)
        self.amount = amount
        self.user_id = user_id
        self.operation_id = operation_id
        self.user_balance = user_balance
        self.operation_response = operation_response

    def json(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "user_balance": self.user_balance,
            "operation_response": self.operation_response,
            "operation_id": self.operation_id,
            "user_id": self.user_id
        }


from .operation import Operation
from .user import User
