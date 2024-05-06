from __future__ import annotations
from datetime import datetime
from mimesis import Person, Text

from project import db, app
from project.models.user import User

data_generator = Person('en')
data_generator_text = Text()


def add_user(email: str = None,
             username: str = None,
             password: str = None,
             created_at: datetime = None,
             name: str = None) -> User:
    """
    Generates a fake user to add in DB
    """
    if email is None:
        email = data_generator.email()
    if username is None:
        username = data_generator.email()
    if password is None:
        password = data_generator.email()
    if created_at is None:
        created_at = datetime.now()
    if name is None:
        name = data_generator.full_name()

    user = User(email=email,
                username=username,
                password=password,
                name=name,
                created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user


def add_user_password(email: str = None,
                      username: str = None,
                      password: str = None,
                      created_at: datetime = None,
                      name: str = None) -> tuple(User, str):
    """
    Generates a fake user to add in DB and return User, password tuple
    """
    if email is None:
        email = data_generator.email()
    if username is None:
        username = data_generator.email()
    if password is None:
        password = data_generator.email()
    if created_at is None:
        created_at = datetime.now()
    if name is None:
        name = data_generator.full_name()

    user = User(email=email,
                username=username,
                password=password,
                name=name,
                created_at=created_at)
    db.session.add(user)
    db.session.commit()
    return user, password
