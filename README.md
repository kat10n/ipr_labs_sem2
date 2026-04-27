# Лабораторные работы по ИПР 2 семестр

**Галанова Екатерина Алексеевна**  
Группа М8О-102БВ-25

---

## Состав репозитория

| Лаба | Тема | Папка |
|------|------|-------|
| Лаб. 5 | Основы Kubernetes: Deployment, Service, ConfigMap, Secret, HPA, Ingress | `lab5/` |
| Лаб. 6 | Kustomize и Helm, разделение приложения и инфраструктуры | `lab6/` |
| Лаб. 7 | Observability: Prometheus, Grafana, Grafana Tempo | `lab7/` |

---

## Лаб. 5 - Kubernetes

Папка: `lab5/`

Flask-приложение (калькулятор) упаковано в Docker-образ с помощью multi-stage сборки и развернуто в Kubernetes. Реализованы манифесты для Namespace, Deployment, Service, ConfigMap, Secret, HPA и Ingress.

Подробнее: `lab5/README.md`

---

## Лаб. 6 - Kustomize и Helm

Папка: `lab6/`

Инфраструктура (PostgreSQL) и приложение (calculator-app) разделены по разным каталогам. Для каждого реализованы два варианта деплоя: через Kustomize (base + overlays dev/prod) и через Helm (chart + values-dev/values-prod).

Подробнее: `lab6/README.md`

---

## Лаб. 7 - Observability

Папка: `lab7/`

В calculator-app добавлены метрики Prometheus (`/metrics`), бизнес-метрики и трейсинг через OpenTelemetry с экспортом в Grafana Tempo. Стек наблюдаемости (Prometheus, Grafana, Tempo) поднимается через Docker Compose.

Подробнее: `lab7/README.md`