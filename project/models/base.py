from __future__ import annotations
from datetime import datetime
from flask import jsonify
from .. import db


class Base(db.Model):  # type: ignore
    """
    Base model
    """

    __abstract__ = True
    __tablename__ = "base"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now()
    )
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(
        self,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ):
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def first_by(cls, **kwargs) -> Base:
        """
        Get first entity that matches to criterion
        """
        return cls.query.filter_by(deleted_at=None, **kwargs).first()

    @classmethod
    def first(cls, *criterion) -> Base:
        """
        Get first entity that matches to criterion
        """
        return cls.query.filter(*criterion).first()

    @classmethod
    def exists(cls, *criterion) -> bool:
        """
        Check if entry with criterion exists
        """
        return cls.query.filter(*criterion).scalar()

    @classmethod
    def get(cls, _id: int) -> Base:
        """
        Get the entity that matches the id
        """
        return cls.query.get(_id)

    # This must be overridden by derived classes
    def json(self) -> dict:
        """
        Get model data in JSON format
        """
        return {
            "id": self.id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    def delete(self) -> None:
        """
        Delete the entity
        """
        self.deleted_at = datetime.now()
        db.session.commit()
