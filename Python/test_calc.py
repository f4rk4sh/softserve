import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_add__should_return__a_plus_b(self):
        self.assertEqual(self.calculator.add(1, 2), 3)

    def test_subtract__should_return__a_minus_b(self):
        self.assertEqual(self.calculator.subtract(5, 2), 3)

    def test_multiply__should_return__a_times_b(self):
        self.assertEqual(self.calculator.multiply(6, 10), 60)

    def test_divide__should_return__a_divided_by_b(self):
        self.assertEqual(self.calculator.divide(12, 6), 2)


if __name__ == '__main__':
    unittest.main()
