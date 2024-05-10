import unittest
from services.random_service import RandomService

class TestRandomService(unittest.TestCase):

    def test_generate_random_string_valid_length(self):
        service = RandomService()
        result = service.generate_random_string({"len": 10})
        self.assertEqual(len(result), 10)

    def test_generate_random_string_zero_length(self):
        service = RandomService()
        with self.assertRaises(Exception):
            service.generate_random_string({"len": 0})

