# Инфраструктура наблюдаемости для Calculator App (лаб. 7)

Отдельный «репозиторий платформы»: **Prometheus**, **Grafana**, **Grafana Tempo**.
Код приложения — в `calculator-app/`; PostgreSQL — в `telegram-support-infra/`.

## Зачем отдельный каталог

- Те же границы, что в лаб. 6: приложение ≠ платформенный стек мониторинга.
- Команда приложения не дублирует Prometheus/Grafana в своём чарте.
- Политики хранения метрик и секреты Grafana — у владельцев платформы.

## Предпосылки

```bash
docker compose version   # 2.x
helm version             # 3.x (для Kubernetes-части)
kubectl get storageclass # кластер доступен
```

## Docker Compose — локальная проверка стека

```bash
cd calculator-observability
docker compose up -d
```

| Сервис     | URL                      | Логин / пароль |
|------------|--------------------------|----------------|
| Grafana    | http://localhost:13001   | admin / admin  |
| Prometheus | http://localhost:19090   | —              |
| Tempo HTTP | http://localhost:13200   | —              |
| OTLP HTTP  | http://localhost:14318   | —              |
| OTLP gRPC  | http://localhost:14317   | —              |

Проверка готовности (подождите 15–20 с):

```bash
curl http://localhost:19090/-/healthy
curl http://localhost:13200/ready
```

Prometheus scrape-цели:
- **prometheus** — всегда **UP**
- **calculator-backend** — `host.docker.internal:8000/metrics` → **UP** если запущен `src/main.py`

Запуск калькулятора на хосте для проверки scrape:

```bash
cd calculator-app
pip install -r requirements.txt
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:14318 \
  OTEL_SERVICE_NAME=calculator-backend \
  python -m src.main
```

Сгенерируйте нагрузку:

```bash
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'
```

Остановка: `docker compose down`

## Порядок развёртывания в Kubernetes

1. **PostgreSQL** (опционально): `telegram-support-infra/`
2. **Приложение**: `mylab6/calculator-app/`
3. **Namespace и Tempo**:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/tempo-configmap.yaml
kubectl apply -f k8s/tempo-deployment.yaml
kubectl apply -f k8s/tempo-service.yaml
```

4. **kube-prometheus-stack**:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace observability --create-namespace \
  -f helm/kube-prometheus-stack/values-dev.yaml
```

5. **ServiceMonitor** (в namespace приложения):

```bash
kubectl apply -f k8s/servicemonitor-calculator.yaml -n calculator-demo
```

6. Проброс портов:

```bash
kubectl port-forward -n observability svc/prometheus-grafana 3000:80
kubectl port-forward -n observability svc/prometheus-kube-prometheus-prometheus 9090:9090
```

## Контракт OTLP для приложения

Добавьте в Deployment calculator-app (Kustomize patch или Helm values):

| Переменная                      | Значение                                              |
|---------------------------------|-------------------------------------------------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT`   | `http://tempo.observability.svc.cluster.local:4318`   |
| `OTEL_SERVICE_NAME`             | `calculator-backend`                                  |

## Файлы

| Путь                                          | Назначение                            |
|-----------------------------------------------|---------------------------------------|
| `docker-compose.yml`                          | Локальный Prometheus + Grafana + Tempo |
| `compose/prometheus/prometheus.yml`           | Scrape calculator-backend на порту 8000 |
| `compose/grafana/dashboards/lab7-calculator.json` | Дашборд с метриками калькулятора  |
| `k8s/tempo-*.yaml`                            | Tempo в namespace observability       |
| `k8s/servicemonitor-calculator.yaml`          | Scrape /metrics в Kubernetes          |
| `helm/kube-prometheus-stack/values-dev.yaml`  | Prometheus Operator (учебный профиль) |
