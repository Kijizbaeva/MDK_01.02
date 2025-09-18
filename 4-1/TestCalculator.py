import unittest
from Calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()
    
    # Позитивные тесты
    def test_add(self):
        self.assertEqual(self.calculator.add(5, 5), 10)
    
    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(8, 2), 6)
    
    def test_multiply(self):
        self.assertEqual(self.calculator.multiply(2, 2), 4)
    
    def test_divide(self):
        self.assertEqual(self.calculator.divide(2, 2), 1)
    
    def test_root(self):
        self.assertEqual(self.calculator.root(36), 6)
    
    def test_module(self):
        self.assertEqual(self.calculator.module(-7), 7)
    
    def test_exponentiation(self):
        self.assertEqual(self.calculator.exponentiation(2, 2), 4)

    # Негативные тесты
    def test_add_none(self):
        with self.assertRaises(TypeError):
            self.calculator.add(None, 5)
    
    def test_subtract_none(self):
        with self.assertRaises(TypeError):
            self.calculator.subtract(8, None)
    
    def test_multiply_none(self):
        with self.assertRaises(TypeError):
            self.calculator.multiply(None, 2)
    
    def test_divide_none(self):
        with self.assertRaises(TypeError):
            self.calculator.divide(2, None)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.divide(2, 0)
    
    def test_root_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.root(-36)
    
    def test_module_none(self):
        with self.assertRaises(TypeError):
            self.calculator.module(None)
    
    def test_exponentiation_none(self):
        with self.assertRaises(TypeError):
            self.calculator.exponentiation(None, 2)

# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
