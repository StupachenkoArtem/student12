import unittest
from django.urls import reverse
from my_sum import sum
from fractions import Fraction
from rest_framework.test import APITestCase


class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of fractions
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

    def test_list_fraction(self):
        """
        Test that it can sum a list of fractions
        """
        data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 4)]
        result = sum(data)
        self.assertEqual(result, 1)

    def test_bad_type(self):
        data = "banana"
        with self.assertRaises(TypeError):
            result = sum(data)

    def test_calculate_average(self):
        numbers = [1, 2, 3, 4, 5]
        result = self.calculate_average(numbers)
        self.assertEqual(result, 3.0)

    def calculate_average(self, numbers):
        if len(numbers) == 0:
            return 0
        return sum(numbers) / len(numbers)


if __name__ == '__main__':
    unittest.main()

