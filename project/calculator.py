import random
import string
from .api.common.utils.exceptions import NotImplementedException


class Calculator():
    """
    Calculator
    """

    def __init__(self):
        pass

    def operation(self, first_value, second_value, operation):
        """
        Perform operation
        """
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
        return first_value / second_value
    
    def square_root(self, first_value):
        """
        Square root
        """
        return first_value ** 0.5
    
    def random_string(self, first_value):
        """
        Random string
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=first_value))
