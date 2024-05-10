import unittest
import random
import math
import string
from flask import Flask, current_app
from project import db
from project.models.user import User
from tests.base import BaseTestCase
from project.api.common.utils.constants import Constants
from tests.utils import (
    add_user,
    successful_login,
    add_operation,
    finance_generator,
    send_record_creation_request,
    add_record,
)
from project.api.common.utils.exceptions import (
    UnauthorizedException,
    BadRequestException,
)


class TestRecord(BaseTestCase):

    def test_add_record_success_addition(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        second_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="addition")
        response = send_record_creation_request(
            self, first_value, second_value, operation.type
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            float(response.json["record"]["operation_response"]),
            first_value + second_value,
        )

    def test_add_record_success_subtraction(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        second_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="subtraction")
        response = send_record_creation_request(
            self, first_value, second_value, operation.type
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            float(response.json["record"]["operation_response"]),
            first_value - second_value,
        )

    def test_add_record_success_multiplication(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        second_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="multiplication")
        response = send_record_creation_request(
            self, first_value, second_value, operation.type
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            float(response.json["record"]["operation_response"]),
            first_value * second_value,
        )

    def test_add_record_success_division(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        second_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="division")
        response = send_record_creation_request(
            self, first_value, second_value, operation.type
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            float(response.json["record"]["operation_response"]),
            first_value / second_value,
        )

    def test_add_record_success_square_root(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="square_root")
        response = send_record_creation_request(self, first_value, None, operation.type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            float(response.json["record"]["operation_response"]), math.sqrt(first_value)
        )

    def test_add_record_success_random_string(self):
        first_value = random.randint(10, 30)
        operation = add_operation(type="random_string")
        response = send_record_creation_request(self, first_value, None, operation.type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["record"]["operation_response"])

    def test_add_record_failure_invalid_operation(self):
        first_value = random.randint(10, 30)
        operation = add_operation(type="addition")
        response = send_record_creation_request(self, first_value, None, "no_addition")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_no_params(self):
        first_value = random.randint(10, 30)
        operation = add_operation(type="addition")
        response = send_record_creation_request(self, None, None, "addition")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_no_operation(self):
        first_value = random.randint(10, 30)
        operation = add_operation(type="addition")
        response = send_record_creation_request(self, first_value, None, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_both_invalid_data_type(self):
        first_value = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        second_value = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        operation = add_operation(type="addition")
        response = send_record_creation_request(self, first_value, second_value, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_first_invalid_data_type(self):
        first_value = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        second_value = random.randint(10, 30)
        operation = add_operation(type="addition")
        response = send_record_creation_request(self, first_value, second_value, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_second_invalid_data_type(self):
        first_value = random.randint(10, 30)
        second_value = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        operation = add_operation(type="addition")
        response = send_record_creation_request(self, first_value, second_value, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_invalid_zero_division(self):
        first_value = random.randint(10, 30)
        second_value = 0
        operation = add_operation(type="addition")
        response = send_record_creation_request(self, first_value, second_value, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_negative_square_root(self):
        first_value = finance_generator.price(minimum=-100, maximum=-1)
        operation = add_operation(type="square_root")
        response = send_record_creation_request(self, first_value, "", operation.type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["message"])

    def test_add_record_failure_no_data(self):
        operation = add_operation(type="addition")
        user = add_user()
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        response = self.client.post("/v1/records", json={}, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")

    def test_add_record_failure_unauthorized(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        second_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="addition")
        headers = {Constants.HttpHeaders.AUTHORIZATION: "Bearer invalid_token"}
        data = {
            "operation": operation.type,
            "first_value": first_value,
            "second_value": second_value,
        }
        response = self.client.post("/v1/records", json=data, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_failure_invalid_token(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        second_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="addition")
        headers = {Constants.HttpHeaders.AUTHORIZATION: "Bearer invalid_token"}
        data = {
            "operation": operation.type,
            "first_value": first_value,
            "second_value": second_value,
        }
        response = self.client.post("/v1/records", json=data, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_add_record_success_large_numbers(self):
        first_value = finance_generator.price(minimum=1000000, maximum=10000000)
        second_value = finance_generator.price(minimum=1000000, maximum=10000000)
        operation = add_operation(type="addition")
        response = send_record_creation_request(
            self, first_value, second_value, operation.type
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            float(response.json["record"]["operation_response"]),
            first_value + second_value,
        )

    def test_add_record_success_negative_numbers(self):
        first_value = finance_generator.price(minimum=-1000, maximum=-1)
        second_value = finance_generator.price(minimum=-1000, maximum=-1)
        operation = add_operation(type="addition")
        response = send_record_creation_request(
            self, first_value, second_value, operation.type
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(
            float(response.json["record"]["operation_response"]),
            first_value + second_value,
        )

    # GET records

    def test_get_list(self):
        first_value = finance_generator.price(minimum=1, maximum=1000)
        second_value = finance_generator.price(minimum=1, maximum=1000)
        operation = add_operation(type="addition")
        user = add_user()
        response = send_record_creation_request(
            self, first_value, second_value, operation.type, user
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        response = self.client.get("/v1/records", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(len(response.json["records"]), 1)
        self.assertEqual(
            float(response.json["records"][0]["operation_response"]),
            first_value + second_value,
        )

    def test_get_list_unauthorized(self):
        response = self.client.get("/v1/records")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["error"])

    def test_get_list_with_pagination(self):
        page_size = 2
        num_records = 5
        num_pages = num_records // page_size + 1
        user = add_user()
        operation = add_operation()
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        records = []
        for i in range(num_records):
            first_value = finance_generator.price()
            second_value = finance_generator.price()
            response = send_record_creation_request(
                self, first_value, second_value, operation.type, user
            )
            records.append(response.json["record"])
        for i in range(num_pages):
            response = self.client.get(
                f"/v1/records?page={i+1}&per_page={page_size}", headers=headers
            )
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.json["records"]) <= page_size)
            for j in range(page_size):
                if i * page_size + j < num_records:
                    self.assertEqual(
                        response.json["records"][j]["id"],
                        records[i * page_size + j]["id"],
                    )
            self.assertEqual(response.json["total"], num_records)
            self.assertEqual(response.json["pages"], num_pages)
            self.assertEqual(response.json["current_page"], i + 1)

    def test_get_list_order_by_amount(self):
        page_size = 2
        num_records = 5
        num_pages = num_records // page_size + 1
        user = add_user()
        operation = add_operation()
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        for i in range(num_records):
            first_value = finance_generator.price()
            second_value = finance_generator.price()
            response = send_record_creation_request(
                self, first_value, second_value, operation.type, user
            )
        response = self.client.get(
            f"/v1/records?page={i+1}&per_page={page_size}&order_by=amount&order=desc",
            headers=headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json["records"]) <= page_size)
        
    def test_get_list_filter_by_operation_response(self):
        num_records = 2
        user = add_user()
        operation = add_operation()
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        records = []
        for i in range(num_records):
            first_value = finance_generator.price()
            second_value = finance_generator.price()
            response = send_record_creation_request(
                self, first_value, second_value, operation.type, user
            )
            records.append(response.json["record"])
        response = self.client.get(
            f"/v1/records?filter_by_operation_response={records[0]['operation_response']}",
            headers=headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["records"]), 1)
        

    # Delete record tests

    def test_delete_record_success(self):
        user = add_user()
        record = add_record(user=user)
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        response = self.client.delete("/v1/records/" + str(record.id), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["message"])

    def test_delete_record_not_found(self):
        user = add_user()
        response_login = successful_login(self, user)
        headers = {
            Constants.HttpHeaders.AUTHORIZATION: "Bearer "
            + response_login.json["session_token"]
        }
        response = self.client.delete("/v1/records/1", headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(response.json["message"])
