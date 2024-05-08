import unittest
from flask import Flask
from project import db
from project.models.user import User
from tests.base import BaseTestCase
from tests.utils import add_user, successful_login
from mimesis import Person


class TestUser(BaseTestCase):
    # Generate fake data with mimesis
    data_generator = Person('en')

    def test_auth_login(self):
        response = successful_login(self)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertTrue(response.json['session_token'])

    def test_auth_login_no_password(self):
        user = add_user()
        data = {
            "username": user.username,
        }
        response = self.client.post("/v1/login", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['error'], 'Missing username or password')

    def test_auth_login_no_username(self):
        password = self.data_generator.password()
        user = add_user(password=password)
        data = {
            "password": password
        }
        response = self.client.post("/v1/login", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['error'], 'Missing username or password')
    
    def test_auth_login_incorrect_password(self):
        password = self.data_generator.password()
        user = add_user(password=password)
        data = {
            "username": user.username,
            "password": self.data_generator.password()
        }
        response = self.client.post("/v1/login", json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['error'], 'Invalid credentials')
    
    def test_auth_login_not_registered(self):
        password = self.data_generator.password()
        user = add_user(password=password)
        data = {
            "username": self.data_generator.username(),
            "password": password
        }
        response = self.client.post("/v1/login", json=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['error'], 'Invalid credentials')
        
    def test_auth_logout(self):
        response_login = successful_login(self)
        response = self.client.post("/v1/logout", json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['message'], 'Logged out successfully')
        
        
        
        

