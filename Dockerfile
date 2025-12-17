# Multi-stage build для оптимизации размера образа

# Этап 1: Сборка и тестирование
FROM python:3.11-slim as builder

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY src/ ./src/
COPY tests/ ./tests/

# Запуск тестов на этапе сборки
RUN pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Этап 2: Продуктовый образ
FROM python:3.11-slim

# Метаданные образа
LABEL maintainer="student@example.com"
LABEL version="1.0.0"
LABEL description="CI/CD Demo Application"

# Создание непривилегированного пользователя
RUN useradd -m -u 1000 appuser

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей из builder
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Копирование приложения
COPY --chown=appuser:appuser src/ ./src/

# Переключение на непривилегированного пользователя
USER appuser

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from src.main import Calculator; c=Calculator(); assert c.add(1,1)==2" || exit 1

# Запуск приложения
CMD ["python", "-m", "src.main"]
