import unittest
from flask import Flask
from project import db, app


class BaseTestCase(unittest.TestCase):
    """
    Base Test Case
    """

    client = app.test_client()

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()