import unittest
from Calculator import Calculator
#Test cases to test Calulator methods
#You always create  a child class derived from unittest.TestCase
class TestCalculator(unittest.TestCase):
  #setUp method is overridden from the parent class TestCase
  def setUp(self):
    self.calculator = Calculator()
  #Each test method starts with the keyword test_
  def test_add(self):
    self.assertEqual(self.calculator.add(5,5), 10)
  def test_subtract(self):
    self.assertEqual(self.calculator.subtract(8,2), 6)
  def test_multiply(self):
    self.assertEqual(self.calculator.multiply(2,2), 4)
  def test_divide(self):
    self.assertEqual(self.calculator.divide(8,2), 4)
  def test_root(self):
    self.assertEqual(self.calculator.root(36), 6)
  def test_module(self):
    self.assertEqual(self.calculator.module(-7), 7)  
  def test_exponentiation(self):
    self.assertEqual(self.calculator.exponentiation(2,2), 4)
# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()