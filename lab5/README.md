# Лабораторная работа №5: Основы Kubernetes

## Цель работы

- Освоить основы работы с Kubernetes — системой оркестрации контейнеризированных приложений
- Контейнеризировать Python-приложение с помощью многоэтапного Dockerfile
- Описать развёртывание в Kubernetes с помощью YAML-манифестов
- Освоить ключевые концепции: Pod, Deployment, Service, ConfigMap, Secret, HPA, Ingress

---

## Структура проекта

```
lab5/
├── Dockerfile                   # Multi-stage сборка с запуском тестов
├── requirements.txt             # Python зависимости
├── src/
│   ├── __init__.py
│   ├── main.py                  # Flask-приложение (калькулятор)
│   └── utils.py
├── tests/
│   ├── test_main.py
│   └── test_utils.py
├── k8s/
│   ├── namespace.yaml           # Namespace lab5
│   ├── configmap.yaml           # Конфигурация приложения
│   ├── secret.yaml              # Секреты (API_KEY)
│   ├── deployment.yaml          # Deployment с 2 репликами
│   ├── service.yaml             # Service типа LoadBalancer
│   ├── hpa.yaml                 # HorizontalPodAutoscaler
│   └── ingress.yaml             # Ingress (calculator.local)
├── .gitlab-ci.yml               # CI/CD пайплайн GitLab
└── .github/workflows/ci.yaml   # CI/CD пайплайн GitHub Actions
```

---

## Приложение

Flask-приложение реализует REST API калькулятора со следующими эндпоинтами:

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Health check для Kubernetes probes |
| POST | `/api/v1/calculate` | Арифметические операции: add, subtract, multiply, divide, power |
| POST | `/api/v1/sqrt` | Квадратный корень |

Пример запроса:
```bash
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'
# {"result": 15}
```

---

## Dockerfile: Multi-stage сборка

Сборка разделена на два этапа:

**Этап 1 (builder):** устанавливает зависимости, копирует исходники, **запускает тесты** (`pytest`). Если тесты не проходят — сборка образа прерывается.

**Этап 2 (runtime):** минимальный образ `python:3.11-slim`, только production-зависимости, непривилегированный пользователь `appuser` (UID 1000), встроенный `HEALTHCHECK`.

```dockerfile
# Этап 1: сборка и тестирование
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src/
COPY tests ./tests/
RUN pytest tests/ --cov=src --cov-report=term-missing

# Этап 2: продуктовый образ
FROM python:3.11-slim
RUN useradd -m -u 1000 appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser src ./src/
USER appuser
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
EXPOSE 8000
CMD ["python", "-m", "src.main"]
```

Сборка локально:
```bash
docker build -t kat10n/calculator:latest .
docker run -p 8000:8000 kat10n/calculator:latest
```

---

## Kubernetes манифесты

### Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: lab5
  labels:
    name: lab5
```

Все ресурсы лабы размещены в namespace `lab5` — это изолирует их от системных компонентов и других проектов.

### ConfigMap

```yaml
# k8s/configmap.yaml
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  PORT: "8000"
  SERVICE_NAME: "calculator-service"
```

ConfigMap хранит несекретную конфигурацию. В Deployment подключается через `envFrom.configMapRef` — все ключи становятся переменными окружения контейнера.

### Secret

```yaml
# k8s/secret.yaml
type: Opaque
data:
  API_KEY: dG9wLXNlY3JldC1rZXk=   # base64("top-secret-key")
```

Secret хранит чувствительные данные в base64. В Deployment подключается через `envFrom.secretRef`. В продакшене секреты не хранят в Git — используют CI/CD variables, Sealed Secrets или External Secrets Operator.

### Deployment

```yaml
# k8s/deployment.yaml
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: calculator
        image: kat10n/calculator:latest
        envFrom:
        - configMapRef:
            name: calculator-config
        - secretRef:
            name: calculator-secret
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

Ключевые решения:
- **2 реплики** — отказоустойчивость: при падении одного пода трафик идёт на второй
- **livenessProbe** — Kubernetes перезапустит контейнер, если `/health` перестанет отвечать
- **readinessProbe** — Kubernetes не направляет трафик на под, пока тот не готов
- **resources.requests/limits** — гарантирует ресурсы и предотвращает захват ресурсов узла

### Service

```yaml
# k8s/service.yaml
spec:
  type: LoadBalancer
  selector:
    app: calculator
  ports:
  - port: 80
    targetPort: 8000
```

`LoadBalancer` — на Docker Desktop эмулируется как `localhost:80`. Трафик на порт 80 перенаправляется на порт 8000 контейнера. Service находит поды через label `app: calculator`.

### HorizontalPodAutoscaler

```yaml
# k8s/hpa.yaml
spec:
  scaleTargetRef:
    kind: Deployment
    name: calculator-app
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

HPA автоматически масштабирует Deployment от 2 до 5 реплик в зависимости от CPU. Если среднее использование CPU превышает 50% — добавляет поды. Требует установленного `metrics-server`.

### Ingress

```yaml
# k8s/ingress.yaml
spec:
  ingressClassName: nginx
  rules:
  - host: calculator.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: calculator-service
            port:
              number: 80
```

Ingress маршрутизирует HTTP-трафик по имени хоста `calculator.local` на сервис. Требует установленного Nginx Ingress Controller.

---

## Запуск (инструкция воспроизведения)

### Требования

- Docker Desktop с включённым Kubernetes
- `kubectl` (входит в Docker Desktop)
- Образ `kat10n/calculator:latest` собран и доступен

### Шаг 1 — Проверить кластер

```bash
kubectl cluster-info
kubectl get nodes
# Должен быть узел docker-desktop в статусе Ready
```

### Шаг 2 — Применить манифесты

```bash
cd lab5

# Namespace первым
kubectl apply -f k8s/namespace.yaml

# Конфигурация и секреты
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Приложение
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Автомасштабирование и Ingress
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

Или одной командой:
```bash
kubectl apply -f k8s/
```

### Шаг 3 — Проверить статус

```bash
# Все ресурсы в namespace
kubectl get all -n lab5

# Поды должны быть Running
kubectl get pods -n lab5

# Deployment
kubectl get deployment -n lab5

# HPA
kubectl get hpa -n lab5
```

### Шаг 4 — Проверить приложение

```bash
# Health check
curl http://localhost/health

# Запрос к API
curl -X POST http://localhost/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "a": 6, "b": 7}'
# {"result": 42}
```

### Шаг 5 — Масштабирование вручную

```bash
kubectl scale deployment calculator-app --replicas=4 -n lab5
kubectl get pods -n lab5 -w
```

### Шаг 6 — Обновление образа

```bash
# Собрать новую версию
docker build -t kat10n/calculator:v2 .

# Обновить deployment
kubectl set image deployment/calculator-app calculator=kat10n/calculator:v2 -n lab5

# Следить за rolling update
kubectl rollout status deployment/calculator-app -n lab5

# История обновлений
kubectl rollout history deployment/calculator-app -n lab5

# Откат если нужно
kubectl rollout undo deployment/calculator-app -n lab5
```

### Шаг 7 — Удаление

```bash
# Удаляет всё в namespace (включая namespace)
kubectl delete namespace lab5
```

---

## Полезные команды kubectl

```bash
# Просмотр ресурсов
kubectl get pods -n lab5
kubectl get pods -n lab5 -o wide          # с IP и узлом
kubectl describe pod <name> -n lab5       # детальная информация

# Логи
kubectl logs <pod-name> -n lab5
kubectl logs <pod-name> -n lab5 -f        # follow (real-time)

# Отладка
kubectl exec -it <pod-name> -n lab5 -- bash
kubectl port-forward svc/calculator-service 8080:80 -n lab5

# Конфигурация
kubectl get configmap calculator-config -n lab5 -o yaml
kubectl get secret calculator-secret -n lab5 -o yaml
```