"""
Unit-тесты для модуля utils.py
"""
import unittest
import pytest
from src.utils import StringProcessor, ListProcessor


class TestStringProcessor(unittest.TestCase):
    """Тесты для класса StringProcessor."""
    
    def test_reverse_string(self):
        """Тест переворота строки."""
        self.assertEqual(StringProcessor.reverse_string("hello"), "olleh")
        self.assertEqual(StringProcessor.reverse_string(""), "")
        self.assertEqual(StringProcessor.reverse_string("a"), "a")
        self.assertEqual(StringProcessor.reverse_string("Python"), "nohtyP")
    
    def test_is_palindrome(self):
        """Тест проверки палиндрома."""
        self.assertTrue(StringProcessor.is_palindrome("radar"))
        self.assertTrue(StringProcessor.is_palindrome("А роза упала на лапу Азора"))
        self.assertTrue(StringProcessor.is_palindrome("madam"))
        self.assertFalse(StringProcessor.is_palindrome("hello"))
        self.assertFalse(StringProcessor.is_palindrome("python"))
    
    def test_count_words(self):
        """Тест подсчета слов."""
        self.assertEqual(StringProcessor.count_words("hello world"), 2)
        self.assertEqual(StringProcessor.count_words("one"), 1)
        self.assertEqual(StringProcessor.count_words(""), 0)
        self.assertEqual(StringProcessor.count_words("one two three four"), 4)
    
    def test_capitalize_words(self):
        """Тест капитализации слов."""
        self.assertEqual(StringProcessor.capitalize_words("hello world"), "Hello World")
        self.assertEqual(StringProcessor.capitalize_words("python is great"), "Python Is Great")
        self.assertEqual(StringProcessor.capitalize_words(""), "")


class TestListProcessor(unittest.TestCase):
    """Тесты для класса ListProcessor."""
    
    def test_find_max(self):
        """Тест поиска максимума."""
        self.assertEqual(ListProcessor.find_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(ListProcessor.find_max([10, -5, 20, 15]), 20)
        self.assertEqual(ListProcessor.find_max([1]), 1)
        self.assertEqual(ListProcessor.find_max([-1, -2, -3]), -1)
    
    def test_find_max_empty_list(self):
        """Тест максимума в пустом списке."""
        with self.assertRaises(ValueError):
            ListProcessor.find_max([])
    
    def test_find_min(self):
        """Тест поиска минимума."""
        self.assertEqual(ListProcessor.find_min([1, 2, 3, 4, 5]), 1)
        self.assertEqual(ListProcessor.find_min([10, -5, 20, 15]), -5)
        self.assertEqual(ListProcessor.find_min([1]), 1)
        self.assertEqual(ListProcessor.find_min([-1, -2, -3]), -3)
    
    def test_find_min_empty_list(self):
        """Тест минимума в пустом списке."""
        with self.assertRaises(ValueError):
            ListProcessor.find_min([])
    
    def test_calculate_average(self):
        """Тест вычисления среднего."""
        self.assertEqual(ListProcessor.calculate_average([1, 2, 3, 4, 5]), 3)
        self.assertEqual(ListProcessor.calculate_average([10, 20]), 15)
        self.assertAlmostEqual(ListProcessor.calculate_average([1, 2, 3]), 2.0)
    
    def test_calculate_average_empty_list(self):
        """Тест среднего для пустого списка."""
        with self.assertRaises(ValueError):
            ListProcessor.calculate_average([])
    
    def test_remove_duplicates(self):
        """Тест удаления дубликатов."""
        self.assertEqual(ListProcessor.remove_duplicates([1, 2, 2, 3, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(ListProcessor.remove_duplicates([1, 1, 1, 1]), [1])
        self.assertEqual(ListProcessor.remove_duplicates([]), [])
        self.assertEqual(ListProcessor.remove_duplicates([1, 2, 3]), [1, 2, 3])
        self.assertEqual(ListProcessor.remove_duplicates(["a", "b", "a", "c"]), ["a", "b", "c"])


# Pytest тесты
class TestListProcessorPytest:
    """Дополнительные тесты с использованием pytest."""
    
    @pytest.mark.parametrize("numbers,expected", [
        ([1, 2, 3, 4, 5], 5),
        ([100, 50, 75], 100),
        ([-10, -20, -5], -5),
    ])
    def test_find_max_parametrized(self, numbers, expected):
        """Параметризованный тест поиска максимума."""
        assert ListProcessor.find_max(numbers) == expected
    
    @pytest.mark.parametrize("numbers,expected", [
        ([1, 2, 3, 4, 5], 3.0),
        ([10, 20, 30], 20.0),
        ([5], 5.0),
    ])
    def test_calculate_average_parametrized(self, numbers, expected):
        """Параметризованный тест вычисления среднего."""
        assert ListProcessor.calculate_average(numbers) == expected


if __name__ == "__main__":
    unittest.main()
