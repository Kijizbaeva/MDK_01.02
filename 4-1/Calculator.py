import math

class Calculator:
    # empty constructor
    def __init__(self):
        pass

    # add method - given two numbers, return the addition
    def add(self, x1, x2):
        if x1 is None or x2 is None:
            raise TypeError("Переданные значения не должны быть None.")
        return x1 + x2

    # multiply method - given two numbers, return the multiplication of the two
    def multiply(self, x1, x2):
        if x1 is None or x2 is None:
            raise TypeError("Переданные значения не должны быть None.")
        return x1 * x2

    # subtract method - given two numbers, return the value of first value minus the second
    def subtract(self, x1, x2):
        if x1 is None or x2 is None:
            raise TypeError("Переданные значения не должны быть None.")
        return x1 - x2

    # divide method - given two numbers, return the value of first value divided by the second
    def divide(self, x1, x2):
        if x1 is None or x2 is None:
            raise TypeError("Переданные значения не должны быть None.")
        if x2 == 0:
            raise ZeroDivisionError("Деление на ноль!")
        return x1 / x2

    # root method - return the square root of a number
    def root(self, x1):
        if x1 is None:
            raise TypeError("Переданное значение не должно быть None.")
        if x1 < 0:
            raise ValueError("Корень из отрицательного числа не определен.")
        return math.sqrt(x1)

    # module method - return absolute value
    def module(self, x1):
        if x1 is None:
            raise TypeError("Переданное значение не должно быть None.")
        return abs(x1)

    # exponentiation method - raise x1 to the power of x2
    def exponentiation(self, x1, x2):
        if x1 is None or x2 is None:
            raise TypeError("Переданные значения не должны быть None.")
        return math.pow(x1, x2)

