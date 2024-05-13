import random
import string
import math
from services.random_service import RandomService
from .api.common.utils.exceptions import (
    NotImplementedException,
    InvalidPayloadException,
)


class Calculator:
    """
    Calculator
    """

    def __init__(self):
        pass

    def operation(self, first_value, second_value, operation):
        """
        Perform operation
        """
        if first_value is not None and not isinstance(first_value, (int, float)):
            first_value = float(first_value)
        if second_value is not None and not isinstance(second_value, (int, float)):
            second_value = float(second_value)
        if operation == "addition":
            return self.addition(first_value, second_value)
        elif operation == "subtraction":
            return self.subtraction(first_value, second_value)
        elif operation == "multiplication":
            return self.multiplication(first_value, second_value)
        elif operation == "division":
            return self.division(first_value, second_value)
        elif operation == "square_root":
            return self.square_root(first_value)
        elif operation == "random_string":
            return self.random_string(first_value)
        else:
            raise NotImplementedException("Operation not implemented")

    def addition(self, first_value, second_value):
        """
        Addition
        """
        return first_value + second_value

    def subtraction(self, first_value, second_value):
        """
        Subtraction
        """
        return first_value - second_value

    def multiplication(self, first_value, second_value):
        """
        Multiplication
        """
        return first_value * second_value

    def division(self, first_value, second_value):
        """
        Division
        """
        try:
            return first_value / second_value
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")
        except TypeError:
            raise TypeError("Inputs must be numbers")

    def square_root(self, first_value):
        """
        Square root
        """
        try:
            return math.sqrt(first_value)
        except ValueError:
            raise InvalidPayloadException("Input must be positive")
        return first_value**0.5

    def random_string(self, first_value):
        """
        Random string
        """
        if not isinstance(first_value, int):
            raise InvalidPayloadException("Length must be an integer")
        if first_value <= 0:
            raise InvalidPayloadException("Length must be positive")
        if first_value > 32:
            raise InvalidPayloadException("Length must be less than 32 characters")
        return "".join(RandomService().generate_random_string({"len": first_value}))
