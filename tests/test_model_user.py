from sqlalchemy.exc import IntegrityError
from mimesis import Person, Finance

from project import db
from project.models.user import User
from tests.base import BaseTestCase
from tests.utils import add_user, add_operation
from project.api.common.utils.exceptions import (
    UnauthorizedException,
    BadRequestException,
)


class TestUserModel(BaseTestCase):
    """
    Test User model
    """

    # Generate fake data with mimesis
    data_generator = Person("en")
    finance_generator = Finance()

    def test_model_user_add_user(self):
        """Ensure adding user model works"""
        username = self.data_generator.username()
        user = add_user(username=username)
        self.assertTrue(user.id)
        self.assertEqual(user.username, username)
        self.assertTrue(user.password_hash)
        self.assertTrue(user.status)
        self.assertTrue(user.created_at)

    def test_model_user_add_user_duplicate_username(self):
        """Ensure adding user with duplicate username does not work"""
        user = add_user()
        duplicate_user = User(
            username=user.username, password=self.data_generator.password()
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_model_user_passwords_are_random(self):
        """Ensure passwords are randomly hashed"""
        password = self.data_generator.password()
        user_one = add_user(password=password)
        user_two = add_user(password=password)
        self.assertNotEqual(user_one.password_hash, user_two.password_hash)

    def test_get_balance(self):
        balance = self.finance_generator.price(minimum=100, maximum=1000)
        user = add_user(balance=balance)
        get_balance = user.get_balance()
        self.assertEqual(get_balance, balance)

    def test_charge_operation_success(self):
        user = add_user()
        original_balance = user.get_balance()
        operation = add_operation()
        result = user.charge_operation(operation)
        self.assertTrue(result)
        self.assertEqual(user.balance, original_balance - operation.cost)

    def test_charge_operation_failure(self):
        user = add_user()
        original_balance = user.get_balance()
        operation = add_operation(
            operation_cost=self.finance_generator.price(
                minimum=(original_balance + 10_000)
            )
        )
        with self.assertRaises(BadRequestException):
            user.charge_operation(operation)
        self.assertEqual(user.balance, original_balance)

    def test_add_record_success(self):
        user = add_user()
        original_balance = user.get_balance()
        operation = add_operation()
        result = user.add_record(
            operation=operation, result=self.finance_generator.price()
        )
        self.assertTrue(result)
        self.assertEqual(user.records[-1].user_id, user.id)
