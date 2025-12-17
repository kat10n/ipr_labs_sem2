# CI/CD Demo Project

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

## 📋 Описание проекта

Демонстрационное приложение для лабораторной работы по CI/CD. Проект включает в себя:
- Python приложение с модулями для математических операций и обработки данных
- Полное покрытие unit-тестами (>70%)
- Автоматизированный GitLab CI/CD пайплайн
- Контейнеризация с использованием Docker
- Публикация образов в GitLab Container Registry

## 🚀 Возможности

### Основной функционал
- **Calculator**: Класс для выполнения математических операций (сложение, вычитание, умножение, деление, степень, корень)
- **StringProcessor**: Обработка строк (переворот, проверка палиндрома, подсчет слов)
- **ListProcessor**: Работа со списками (поиск min/max, среднее значение, удаление дубликатов)

### CI/CD Pipeline
1. **Test Stage**: Автоматические unit-тесты с отчетами о покрытии кода
2. **Build Stage**: Сборка Docker образа с multi-stage build
3. **Publish Stage**: Публикация образа в GitLab Container Registry
4. **Deploy Stage**: Деплой на staging/production окружения

## 📁 Структура проекта

```
my-application/
├── README.md                   # Документация проекта
├── .gitignore                 # Исключения для Git
├── .gitlab-ci.yml             # Конфигурация CI/CD пайплайна
├── Dockerfile                 # Multi-stage Docker образ
├── requirements.txt           # Python зависимости
├── LICENSE                    # Лицензия MIT
├── src/                       # Исходный код приложения
│   ├── __init__.py
│   ├── main.py               # Основной модуль (Calculator)
│   └── utils.py              # Утилиты (StringProcessor, ListProcessor)
├── tests/                     # Unit-тесты
│   ├── __init__.py
│   ├── test_main.py          # Тесты для main.py
│   └── test_utils.py         # Тесты для utils.py
└── docs/                      # Дополнительная документация
    └── api.md                # API документация
```

## 🛠️ Установка и запуск

### Локальная разработка

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd PythonProject5
```

2. **Создание виртуального окружения**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

4. **Запуск приложения**
```bash
python -m src.main
```

### Запуск тестов

```bash
# Запуск всех тестов
pytest tests/

# Запуск с отчетом о покрытии
pytest tests/ --cov=src --cov-report=html

# Запуск конкретного теста
pytest tests/test_main.py -v
```

### Docker

1. **Сборка образа**
```bash
docker build -t my-app:latest .
```

2. **Запуск контейнера**
```bash
docker run --rm my-app:latest
```

3. **Проверка работоспособности**
```bash
docker run --rm my-app:latest python -m src.main
```

## 🔄 CI/CD Pipeline

### Стадии пайплайна

#### 1. Test (Тестирование)
- Запуск unit-тестов с pytest
- Генерация отчета о покрытии кода
- Проверка качества кода (flake8, pylint)

#### 2. Build (Сборка)
- Сборка Docker образа с multi-stage build
- Оптимизация с использованием кэша
- Проверка безопасности образа

#### 3. Publish (Публикация)
- Публикация образа в GitLab Container Registry
- Тегирование: latest, commit SHA, branch name
- Автоматическое версионирование для релизов

#### 4. Deploy (Деплой)
- Деплой на staging окружение (ручной запуск)
- Деплой на production (только для тегов)

### Переменные окружения

Pipeline использует следующие переменные:
- `CI_REGISTRY_IMAGE`: Адрес GitLab Container Registry
- `CI_REGISTRY_USER`: Пользователь для авторизации
- `CI_REGISTRY_PASSWORD`: Пароль для авторизации
- `PYTHON_VERSION`: Версия Python (по умолчанию 3.11)

## 📊 Покрытие кода

Проект имеет высокое покрытие unit-тестами:
- **src/main.py**: >90% coverage
- **src/utils.py**: >90% coverage
- **Общее покрытие**: >85%

Отчеты о покрытии генерируются автоматически в каждом pipeline run.

## 🐳 Docker

### Multi-stage Build

Dockerfile использует multi-stage build для оптимизации:
1. **Builder stage**: Установка зависимостей и запуск тестов
2. **Production stage**: Минимальный финальный образ

### Особенности образа
- Базовый образ: `python:3.11-slim`
- Непривилегированный пользователь для безопасности
- Health check для контроля работоспособности
- Оптимизированный размер (<200 MB)

## 🔒 Безопасность

- Использование непривилегированного пользователя в Docker
- Регулярное обновление зависимостей
- Проверка безопасности в pipeline (опционально)
- Использование секретов GitLab CI/CD для аутентификации

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 👥 Авторы

- **Student** - Разработчик - [student@example.com](mailto:student@example.com)

## 🤝 Вклад в проект

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменений (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Контакты

- Email: student@example.com
- GitLab: https://gitlab.com/username/project

## 📚 Дополнительная информация

### Требования к окружению
- Python 3.11+
- Docker 24+
- GitLab Runner (для CI/CD)

### Полезные команды

```bash
# Проверка стиля кода
flake8 src/ --max-line-length=100

# Линтинг кода
pylint src/ --max-line-length=100

# Форматирование кода
black src/ tests/

# Сортировка импортов
isort src/ tests/
```

### Troubleshooting

**Проблема**: Тесты не проходят локально  
**Решение**: Убедитесь, что установлены все зависимости из requirements.txt

**Проблема**: Docker образ не собирается  
**Решение**: Проверьте версию Docker и наличие прав на запуск

**Проблема**: Pipeline падает на стадии publish  
**Решение**: Проверьте настройки CI/CD переменных в GitLab

---

⭐ Не забудьте поставить звезду, если проект был полезен!
