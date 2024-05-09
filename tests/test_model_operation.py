from sqlalchemy.exc import IntegrityError
from mimesis import Finance

from project import db
from project.models.operation import Operation
from tests.base import BaseTestCase
from app.utils import add_operation  # type: ignore


class TestOperationModel(BaseTestCase):
    """
    Test User model
    """

    # Generate fake data with mimesis
    data_generator = Finance()

    def test_model_operation_add(self):
        operation_cost = self.data_generator.price()
        operation = Operation(type="Add", cost=operation_cost)
        db.session.add(operation)
        db.session.commit()
        assert operation.id is not None
        assert operation.type == "Add"
        assert operation.cost == operation_cost

    def test_model_operation_duplicate_type(self):
        operation1 = Operation(type="Multiply", cost=self.data_generator.price())
        db.session.add(operation1)
        db.session.commit()
        operation2 = Operation(type="Multiply", cost=self.data_generator.price())
        db.session.add(operation2)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_model_operation_json(self):
        operation_name = "addition"
        operation = add_operation(type=operation_name)
        record_json = operation.json()
        assert record_json["id"] == operation.id
        assert record_json["type"] == operation_name
        assert record_json["cost"] == operation.cost
