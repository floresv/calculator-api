from sqlalchemy.exc import IntegrityError
from mimesis import Person

from project import db
from project.models.user import User
from tests.base import BaseTestCase
from tests.utils import add_user


class TestUserModel(BaseTestCase):
    """
    Test User model
    """
    # Generate fake data with mimesis
    data_generator = Person('en')

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
            username=user.username,
            password=self.data_generator.password()
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_model_user_passwords_are_random(self):
        """Ensure passwords are randomly hashed"""
        password = self.data_generator.password()
        user_one = add_user(password=password)
        user_two = add_user(password=password)
        self.assertNotEqual(user_one.password_hash, user_two.password_hash)