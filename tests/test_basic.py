import unittest
from flask import Flask
from tests.base import BaseTestCase


class TestBasicAPI(BaseTestCase):

    def test_get_hello(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
            
    def test_get_status(self):
        response = self.client.get("/status")
        self.assertEqual(response.status_code, 200)
