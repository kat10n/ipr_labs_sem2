"""
Вспомогательные утилиты для работы с данными.
"""
from typing import List, Union


class StringProcessor:
    """Класс для обработки строк."""
    
    @staticmethod
    def reverse_string(s: str) -> str:
        """Переворачивает строку."""
        return s[::-1]
    
    @staticmethod
    def is_palindrome(s: str) -> bool:
        """Проверяет, является ли строка палиндромом."""
        cleaned = ''.join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]
    
    @staticmethod
    def count_words(s: str) -> int:
        """Подсчитывает количество слов в строке."""
        return len(s.split())
    
    @staticmethod
    def capitalize_words(s: str) -> str:
        """Делает первую букву каждого слова заглавной."""
        return ' '.join(word.capitalize() for word in s.split())


class ListProcessor:
    """Класс для обработки списков."""
    
    @staticmethod
    def find_max(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Находит максимальное значение в списке."""
        if not numbers:
            raise ValueError("Список не может быть пустым")
        return max(numbers)
    
    @staticmethod
    def find_min(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Находит минимальное значение в списке."""
        if not numbers:
            raise ValueError("Список не может быть пустым")
        return min(numbers)
    
    @staticmethod
    def calculate_average(numbers: List[Union[int, float]]) -> float:
        """Вычисляет среднее значение списка."""
        if not numbers:
            raise ValueError("Список не может быть пустым")
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def remove_duplicates(items: List) -> List:
        """Удаляет дубликаты из списка, сохраняя порядок."""
        seen = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
