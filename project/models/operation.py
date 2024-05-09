from __future__ import annotations
from datetime import datetime
from flask import current_app
from .base import Base
from .. import db


class Operation(Base):
    """
    Operation model
    """

    __tablename__ = "operations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128), unique=True, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    records = db.relationship("Record", back_populates="operation")

    def __init__(
        self,
        type: str | None = None,
        cost: float | None = None,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ):
        super().__init__(created_at, updated_at)
        self.type = type
        self.cost = cost

    def json(self) -> dict:
        """
        Get operation data in JSON format
        """
        return {"id": self.id, "type": self.type, "cost": self.cost}


from .record import Record
from .user import User
