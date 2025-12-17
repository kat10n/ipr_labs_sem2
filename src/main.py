"""
Главный модуль приложения для работы с числовыми операциями.
"""


class Calculator:
    """Класс для выполнения математических операций."""
    
    def add(self, a: float, b: float) -> float:
        """Сложение двух чисел."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Вычитание двух чисел."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Умножение двух чисел."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Деление двух чисел."""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """Возведение в степень."""
        return base ** exponent
    
    def sqrt(self, x: float) -> float:
        """Квадратный корень."""
        if x < 0:
            raise ValueError("Корень из отрицательного числа невозможен")
        return x ** 0.5


def main():
    """Главная функция для демонстрации работы калькулятора."""
    calc = Calculator()
    
    print("=== Демонстрация калькулятора ===")
    print(f"10 + 5 = {calc.add(10, 5)}")
    print(f"10 - 5 = {calc.subtract(10, 5)}")
    print(f"10 * 5 = {calc.multiply(10, 5)}")
    print(f"10 / 5 = {calc.divide(10, 5)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"√16 = {calc.sqrt(16)}")


if __name__ == "__main__":
    main()
