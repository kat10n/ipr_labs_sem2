# Документация проекта

## Описание проекта

Этот проект представляет собой простое Python-приложение для выполнения математических операций (калькулятор). Проект включает:

- Основной код приложения в `src/`
- Модульные тесты в `tests/`
- Docker-контейнеризацию
- CI/CD пайплайн с использованием GitHub Actions
- Развертывание в Kubernetes

## Структура проекта

```
.
├── Dockerfile              # Docker образ приложения
├── requirements.txt        # Python зависимости
├── src/                    # Исходный код
│   ├── __init__.py
│   ├── main.py            # Основной модуль с классом Calculator
│   └── utils.py           # Вспомогательные функции
├── tests/                  # Тесты
│   ├── __init__.py
│   ├── test_main.py       # Тесты для main.py
│   └── test_utils.py      # Тесты для utils.py
├── docs/                   # Документация
│   └── api.md             # API документация
├── .github/workflows/     # GitHub Actions CI/CD
└── TASK.md                # Описание лабораторных работ
```

## Запуск приложения

### Локально

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск
python -m src.main
```

### В Docker

```bash
# Сборка образа
docker build -t calculator .

# Или скачивание готового образа с Docker Hub
docker pull kat10n/calculator:latest

# Запуск контейнера
docker run -p 8000:8000 kat10n/calculator:latest
```

## Тестирование

```bash
# Запуск тестов
pytest tests/

# С покрытием
pytest tests/ --cov=src --cov-report=html
```

## CI/CD

Проект использует GitHub Actions для автоматического тестирования, проверки качества кода и сборки Docker образов. Образы публикуются в Docker Hub под именем `kat10n/calculator`.

## Развертывание в Kubernetes

См. [От лабораторной №4 к Kubernetes](lab4-to-kubernetes.md) для инструкций по развертыванию приложения в Kubernetes с использованием образа `kat10n/calculator:latest`.