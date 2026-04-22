"""
Главный модуль приложения для работы с числовыми операциями.
"""
from flask import Flask, request, jsonify
import os


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


app = Flask(__name__)
calc = Calculator()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route('/api/v1/calculate', methods=['POST'])
def calculate():
    """API endpoint для выполнения расчетов."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        operation = data.get('operation')
        a = data.get('a')
        b = data.get('b')
        
        if operation not in ['add', 'subtract', 'multiply', 'divide', 'power']:
            return jsonify({"error": "Invalid operation"}), 400
        
        if not isinstance(a, (int, float)) or (b is not None and not isinstance(b, (int, float))):
            return jsonify({"error": "Invalid operands"}), 400
        
        if operation in ['add', 'subtract', 'multiply', 'divide', 'power'] and b is None:
            return jsonify({"error": "Second operand required"}), 400
        
        result = getattr(calc, operation)(a, b) if b is not None else getattr(calc, operation)(a)
        return jsonify({"result": result})
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/v1/sqrt', methods=['POST'])
def sqrt():
    """API endpoint для квадратного корня."""
    try:
        data = request.get_json()
        if not data or 'x' not in data:
            return jsonify({"error": "Parameter 'x' required"}), 400
        
        x = data['x']
        if not isinstance(x, (int, float)):
            return jsonify({"error": "Invalid operand"}), 400
        
        result = calc.sqrt(x)
        return jsonify({"result": result})
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


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


if __name__ == '__main__':
    # Если запущено как скрипт, запускаем веб-сервер
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    main()
