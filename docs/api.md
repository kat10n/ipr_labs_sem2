# API Documentation

## Calculator API

### Class: `Calculator`

Класс для выполнения математических операций.

#### Methods

##### `add(a: float, b: float) -> float`
Сложение двух чисел.

**Parameters:**
- `a` (float): Первое число
- `b` (float): Второе число

**Returns:**
- float: Сумма чисел

**Example:**
```python
calc = Calculator()
result = calc.add(5, 3)  # 8
```

##### `subtract(a: float, b: float) -> float`
Вычитание двух чисел.

**Parameters:**
- `a` (float): Уменьшаемое
- `b` (float): Вычитаемое

**Returns:**
- float: Разность чисел

##### `multiply(a: float, b: float) -> float`
Умножение двух чисел.

##### `divide(a: float, b: float) -> float`
Деление двух чисел.

**Raises:**
- `ValueError`: Если b равно 0

##### `power(base: float, exponent: float) -> float`
Возведение в степень.

##### `sqrt(x: float) -> float`
Квадратный корень.

**Raises:**
- `ValueError`: Если x отрицательное

---

## StringProcessor API

### Class: `StringProcessor`

Класс для обработки строк.

#### Methods

##### `reverse_string(s: str) -> str`
Переворачивает строку.

##### `is_palindrome(s: str) -> bool`
Проверяет, является ли строка палиндромом.

##### `count_words(s: str) -> int`
Подсчитывает количество слов в строке.

##### `capitalize_words(s: str) -> str`
Делает первую букву каждого слова заглавной.

---

## ListProcessor API

### Class: `ListProcessor`

Класс для обработки списков.

#### Methods

##### `find_max(numbers: List[Union[int, float]]) -> Union[int, float]`
Находит максимальное значение в списке.

**Raises:**
- `ValueError`: Если список пуст

##### `find_min(numbers: List[Union[int, float]]) -> Union[int, float]`
Находит минимальное значение в списке.

##### `calculate_average(numbers: List[Union[int, float]]) -> float`
Вычисляет среднее значение списка.

##### `remove_duplicates(items: List) -> List`
Удаляет дубликаты из списка, сохраняя порядок.
