import unittest
from flask import Flask

app = Flask(__name__)


class FlaskAPITestCase(unittest.TestCase):

    def test_get_hello(self):
        with app.test_client() as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 404)
