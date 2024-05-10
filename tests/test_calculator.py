import unittest
from project.calculator import Calculator
from project.api.common.utils.exceptions import InvalidPayloadException


class TestCalculator(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(Calculator().addition(2, 3), 5)
        self.assertEqual(Calculator().addition(-1, 1), 0)
        self.assertEqual(Calculator().addition(0, 0), 0)

    def test_subtraction(self):
        self.assertEqual(Calculator().subtraction(5, 3), 2)
        self.assertEqual(Calculator().subtraction(1, 1), 0)
        self.assertEqual(Calculator().subtraction(-2, -4), 2)

    def test_multiplication(self):
        self.assertEqual(Calculator().multiplication(2, 3), 6)
        self.assertEqual(Calculator().multiplication(0, 5), 0)
        self.assertEqual(Calculator().multiplication(-2, 4), -8)

    def test_division(self):
        self.assertEqual(Calculator().division(6, 3), 2)
        self.assertEqual(Calculator().division(1, 1), 1)
        with self.assertRaises(ValueError):
            Calculator().division(1, 0)
        with self.assertRaises(TypeError):
            Calculator().division(1, "a")

    def test_square_root(self):
        self.assertEqual(round(Calculator().square_root(4), 2), 2.00)
        self.assertEqual(Calculator().square_root(9), 3)
        self.assertEqual(Calculator().square_root(0), 0)
        with self.assertRaises(InvalidPayloadException):
            Calculator().square_root(-1)

    def test_random_string(self):
        result = Calculator().random_string(5)
        self.assertEqual(len(result), 5)
        result = Calculator().random_string(10)
        self.assertEqual(len(result), 10)

    def test_random_string_invalid_length(self):
        with self.assertRaises(InvalidPayloadException):
            Calculator().random_string(-5)

    def test_random_string_zero_length(self):
        with self.assertRaises(InvalidPayloadException):
            Calculator().random_string(0)

    def test_random_string_non_integer_length(self):
        with self.assertRaises(InvalidPayloadException):
            Calculator().random_string("a")
