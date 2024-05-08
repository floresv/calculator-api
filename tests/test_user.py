import unittest
from flask import Flask, current_app
from project import db
from project.models.user import User
from tests.base import BaseTestCase
from tests.utils import add_user, successful_login, data_generator
from project.api.common.utils.constants import Constants
import jwt


class TestUser(BaseTestCase):

    def test_create_user(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/v1/users", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        self.assertIn("User created successfully", response.json["message"])

    def test_create_user_duplicate_username(self):
        """Ensure duplicate username registration is not allowed"""
        user = add_user()
        data = {"username": user.username, "password": "testpassword"}
        response = self.client.post("/v1/users", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Username already exists")

    def test_auth_register_invalid_json_no_username(self):
        data = {"password": "testpassword"}
        response = self.client.post("/v1/users", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing username or password")

    def test_auth_register_invalid_json_no_password(self):
        data = {
            "username": "testuser",
        }
        response = self.client.post("/v1/users", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing username or password")

    def test_auth_register_empty_json(self):
        data = {}
        response = self.client.post("/v1/users", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Missing username or password")

    def test_get_user(self):
        user = add_user()
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        response = self.client.get("/v1/users/me", json={}, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["username"], user.username)
        self.assertEqual(response.json["status"], user.status)
        self.assertEqual(response.json["balance"], user.get_balance())

    def test_get_user_without_token(self):
        """Ensure invalid token doesn't work for status check"""
        with self.client:
            response = self.client.get(
                "/v1/users/me", headers=[("Accept", "application/json")]
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json["error"], "Missing or invalid token")

    def test_get_user_invalid(self):
        """Ensure invalid token doesn't work for status check"""
        with self.client:
            response = self.client.get(
                "/v1/users/me",
                headers=[
                    ("Accept", "application/json"),
                    (Constants.HttpHeaders.AUTHORIZATION, "Bearer invalid"),
                ],
            )
            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json["error"], "Invalid token")

    def test_get_use_not_found(self):
        payload = {"username": data_generator.username()}
        session_token = jwt.encode(
            payload, current_app.config["SECRET_KEY"], algorithm="HS256"
        )
        headers = {Constants.HttpHeaders.AUTHORIZATION: "Bearer " + session_token}
        response = self.client.get("/v1/users/me", json={}, headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["error"], "User not found")
