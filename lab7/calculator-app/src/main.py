"""
Главный модуль приложения для работы с числовыми операциями.
Добавлены: /metrics (Prometheus), OpenTelemetry трейсинг (OTLP).
"""
import os
from flask import Flask, request, jsonify

# --- Prometheus метрики ---
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

http_requests_total = Counter(
    "http_requests_total",
    "Общее количество HTTP-запросов",
    ["method", "endpoint", "status"],
)
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "Длительность HTTP-запросов",
    ["method", "endpoint"],
)
# Бизнес-метрика: счётчик выполненных операций
calculator_operations_total = Counter(
    "calculator_operations_total",
    "Количество выполненных операций калькулятора",
    ["operation"],
)

# --- OpenTelemetry трейсинг ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

OTEL_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "")
SERVICE_NAME = os.environ.get("OTEL_SERVICE_NAME", "calculator-backend")

resource = Resource.create({"service.name": SERVICE_NAME})
provider = TracerProvider(resource=resource)

if OTEL_ENDPOINT:
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    exporter = OTLPSpanExporter(endpoint=f"{OTEL_ENDPOINT}/v1/traces")
    provider.add_span_processor(BatchSpanProcessor(exporter))

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# --- Flask инструментирование ---
from opentelemetry.instrumentation.flask import FlaskInstrumentor


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
FlaskInstrumentor().instrument_app(app)
calc = Calculator()


def _track(method: str, endpoint: str, status: int):
    http_requests_total.labels(method=method, endpoint=endpoint, status=str(status)).inc()


@app.before_request
def _start_timer():
    request._start = __import__("time").monotonic()


@app.after_request
def _record_metrics(response):
    endpoint = request.path
    duration = __import__("time").monotonic() - getattr(request, "_start", 0)
    http_request_duration_seconds.labels(
        method=request.method, endpoint=endpoint
    ).observe(duration)
    _track(request.method, endpoint, response.status_code)
    return response


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/api/v1/calculate", methods=["POST"])
def calculate():
    """API endpoint для выполнения расчетов."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        operation = data.get("operation")
        a = data.get("a")
        b = data.get("b")

        if operation not in ["add", "subtract", "multiply", "divide", "power"]:
            return jsonify({"error": "Invalid operation"}), 400

        if not isinstance(a, (int, float)) or (
            b is not None and not isinstance(b, (int, float))
        ):
            return jsonify({"error": "Invalid operands"}), 400

        if b is None:
            return jsonify({"error": "Second operand required"}), 400

        with tracer.start_as_current_span(f"calc.{operation}"):
            result = getattr(calc, operation)(a, b)

        calculator_operations_total.labels(operation=operation).inc()
        return jsonify({"result": result})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/v1/sqrt", methods=["POST"])
def sqrt():
    """API endpoint для квадратного корня."""
    try:
        data = request.get_json()
        if not data or "x" not in data:
            return jsonify({"error": "Parameter 'x' required"}), 400

        x = data["x"]
        if not isinstance(x, (int, float)):
            return jsonify({"error": "Invalid operand"}), 400

        with tracer.start_as_current_span("calc.sqrt"):
            result = calc.sqrt(x)

        calculator_operations_total.labels(operation="sqrt").inc()
        return jsonify({"result": result})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# Монтируем /metrics как отдельный WSGI-эндпоинт (стандартный способ с prometheus_client)
application = DispatcherMiddleware(app, {"/metrics": make_wsgi_app()})


def main():
    """Главная функция для демонстрации работы калькулятора."""
    c = Calculator()
    print("=== Демонстрация калькулятора ===")
    print(f"10 + 5 = {c.add(10, 5)}")
    print(f"10 - 5 = {c.subtract(10, 5)}")
    print(f"10 * 5 = {c.multiply(10, 5)}")
    print(f"10 / 5 = {c.divide(10, 5)}")
    print(f"2 ^ 8 = {c.power(2, 8)}")
    print(f"√16   = {c.sqrt(16)}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Запуск через werkzeug с поддержкой /metrics
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", port, application, use_reloader=False)
