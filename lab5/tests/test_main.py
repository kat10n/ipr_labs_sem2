"""
Unit-тесты для модуля main.py
"""
import unittest
import pytest
from lab5.src import Calculator


class TestCalculator(unittest.TestCase):
    """Тесты для класса Calculator."""
    
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.calc = Calculator()
    
    def test_add_positive_numbers(self):
        """Тест сложения положительных чисел."""
        self.assertEqual(self.calc.add(5, 3), 8)
        self.assertEqual(self.calc.add(10, 20), 30)
    
    def test_add_negative_numbers(self):
        """Тест сложения отрицательных чисел."""
        self.assertEqual(self.calc.add(-5, -3), -8)
        self.assertEqual(self.calc.add(-10, 5), -5)
    
    def test_add_zero(self):
        """Тест сложения с нулем."""
        self.assertEqual(self.calc.add(0, 0), 0)
        self.assertEqual(self.calc.add(5, 0), 5)
    
    def test_subtract(self):
        """Тест вычитания."""
        self.assertEqual(self.calc.subtract(10, 5), 5)
        self.assertEqual(self.calc.subtract(5, 10), -5)
        self.assertEqual(self.calc.subtract(-5, -3), -2)
    
    def test_multiply(self):
        """Тест умножения."""
        self.assertEqual(self.calc.multiply(5, 3), 15)
        self.assertEqual(self.calc.multiply(-5, 3), -15)
        self.assertEqual(self.calc.multiply(0, 100), 0)
    
    def test_divide(self):
        """Тест деления."""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(15, 3), 5)
        self.assertAlmostEqual(self.calc.divide(10, 3), 3.333, places=3)
    
    def test_divide_by_zero(self):
        """Тест деления на ноль."""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertIn("Деление на ноль", str(context.exception))
    
    def test_power(self):
        """Тест возведения в степень."""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 2), 25)
        self.assertEqual(self.calc.power(10, 0), 1)
        self.assertEqual(self.calc.power(2, -1), 0.5)
    
    def test_sqrt(self):
        """Тест квадратного корня."""
        self.assertEqual(self.calc.sqrt(16), 4)
        self.assertEqual(self.calc.sqrt(25), 5)
        self.assertEqual(self.calc.sqrt(0), 0)
        self.assertAlmostEqual(self.calc.sqrt(2), 1.414, places=3)
    
    def test_sqrt_negative(self):
        """Тест корня из отрицательного числа."""
        with self.assertRaises(ValueError) as context:
            self.calc.sqrt(-1)
        self.assertIn("отрицательного числа", str(context.exception))


# Pytest тесты для дополнительного покрытия
class TestCalculatorPytest:
    """Дополнительные тесты с использованием pytest."""
    
    @pytest.fixture
    def calc(self):
        """Фикстура для создания калькулятора."""
        return Calculator()
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 1, 2),
        (10, 20, 30),
        (-5, 5, 0),
        (0, 0, 0),
        (100, -50, 50),
    ])
    def test_add_parametrized(self, calc, a, b, expected):
        """Параметризованный тест сложения."""
        assert calc.add(a, b) == expected
    
    @pytest.mark.parametrize("a,b,expected", [
        (6, 2, 3),
        (10, 5, 2),
        (100, 10, 10),
    ])
    def test_divide_parametrized(self, calc, a, b, expected):
        """Параметризованный тест деления."""
        assert calc.divide(a, b) == expected


if __name__ == "__main__":
    unittest.main()
