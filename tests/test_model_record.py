from sqlalchemy.exc import IntegrityError

from project import db
from project.models.operation import Operation
from tests.base import BaseTestCase
from tests.utils import add_record, finance_generator


class TestOperationModel(BaseTestCase):
    """
    Test User model
    """

    def test_model_operation_add(self):
        operation_cost = finance_generator.price()
        balance = finance_generator.price()
        record = add_record(operation_cost=operation_cost, balance=balance)
        assert record.id is not None
        assert record.amount == operation_cost
        assert record.user_id == 1
        assert record.operation_id == 1
        assert record.user_balance == balance
        assert record.operation_response == "Success"

    def test_json(self):
        record = add_record()
        record_json = record.json()
        assert record_json["amount"] == record.amount
        assert record_json["user_id"] == record.user_id
        assert record_json["operation"] == record.operation.type
        assert record_json["user_balance"] == record.user_balance
        assert record_json["operation_response"] == record.operation_response
