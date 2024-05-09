from __future__ import annotations
from datetime import datetime
from typing import Optional
from mimesis import Person, Text, Finance

from project import db, app
from project.models.user import User
from project.models.record import Record
from project.models.operation import Operation

data_generator = Person("en")
data_generator_text = Text()
finance_generator = Finance()


def add_user(
    username: Optional[str] = None,
    password: Optional[str] = None,
    balance: Optional[float] = None,
    created_at: Optional[datetime] = None,
) -> User:
    """
    Generates a fake user to add in DB
    """
    if username is None:
        username = data_generator.username()
    if password is None:
        password = data_generator.password()
    if balance is None:
        balance = finance_generator.price(minimum=100.0, maximum=1000.0)
    if created_at is None:
        created_at = datetime.now()

    user = User(username=username, password=password, created_at=created_at, balance=balance)
    db.session.add(user)
    db.session.commit()
    return user


def successful_login(self, user: Optional[User] = None):
    password = data_generator.password()
    if user is None:
        user = add_user(password=password)
    else:
        user.set_password(password=password)
    data = {"username": user.username, "password": password}
    return self.client.post("/v1/login", json=data)


def add_record(
    operation_cost: Optional[float] = None,
    balance: Optional[float] = None
) -> Record:
    user = add_user()
    operation = add_operation(operation_cost)
    if balance is None:
        balance = finance_generator.price()
    record = Record(
        amount=operation.cost,
        user_id=user.id,
        operation_id=operation.id,
        user_balance=balance,
        operation_response="Success"
    )
    db.session.add(record)
    db.session.commit()
    return record


def add_operation(operation_cost: Optional[float] = None):
    if operation_cost is None:
        operation_cost = finance_generator.price(minimum=1, maximum=100)
    operation = Operation(type="Add", cost=operation_cost)
    db.session.add(operation)
    db.session.commit()
    return operation
