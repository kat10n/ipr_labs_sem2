# API Documentation

## Calculator API

### Base URL
```
http://localhost:8000
```

### Health Check

#### GET /health
Проверка работоспособности сервиса.

**Response:**
```json
{
  "status": "healthy"
}
```

### Calculator Operations

#### POST /api/v1/calculate
Выполнение математических операций.

**Request Body:**
```json
{
  "operation": "add|subtract|multiply|divide|power",
  "a": number,
  "b": number
}
```

**Response:**
```json
{
  "result": number
}
```

**Examples:**

```bash
# Сложение
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'

# Вычитание
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "subtract", "a": 10, "b": 5}'

# Умножение
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "a": 10, "b": 5}'

# Деление
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "divide", "a": 10, "b": 5}'

# Возведение в степень
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "power", "a": 2, "b": 8}'
```

#### POST /api/v1/sqrt
Вычисление квадратного корня.

**Request Body:**
```json
{
  "x": number
}
```

**Response:**
```json
{
  "result": number
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/sqrt \
  -H "Content-Type: application/json" \
  -d '{"x": 16}'
```

### Error Responses

**400 Bad Request:**
```json
{
  "error": "Error message"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error"
}
```

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
