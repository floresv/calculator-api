from __future__ import annotations
from datetime import datetime
from typing import Optional
from mimesis import Person, Text

from project import db, app
from project.models.user import User

data_generator = Person("en")
data_generator_text = Text()


def add_user(
    username: Optional[str] = None,
    password: Optional[str] = None,
    created_at: Optional[datetime] = None,
) -> User:
    """
    Generates a fake user to add in DB
    """
    if username is None:
        username = data_generator.email()
    if password is None:
        password = data_generator.email()
    if created_at is None:
        created_at = datetime.now()

    user = User(username=username, password=password, created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user


def add_user_password(
    username: Optional[str] = None,
    password: Optional[str] = None,
    created_at: Optional[datetime] = None,
) -> tuple[User, str]:
    """
    Generates a fake user to add in DB and return User, password tuple
    """
    if username is None:
        username = data_generator.email()
    if password is None:
        password = data_generator.email()
    if created_at is None:
        created_at = datetime.now()

    user = User(username=username, password=password, created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user, password
