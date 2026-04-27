# Лабораторная работа №6: Kustomize и Helm, разделение приложения и инфраструктуры

## Цель работы

- Разделить манифесты приложения и инфраструктуры (базы данных) по аналогии с промышленной практикой
- Описать инфраструктуру (PostgreSQL) через **Kustomize** (база + overlays) и через **Helm** (chart + values-файлы)
- Описать приложение (calculator-app) через **Kustomize** и **Helm** аналогично
- Освоить StatefulSet, Headless Service и PVC на примере PostgreSQL

---

## Структура проекта

```
lab6/
├── calculator-app/
│   └── k8s/
│       ├── kustomization/
│       │   ├── base/
│       │   │   ├── kustomization.yaml
│       │   │   ├── deployment.yaml
│       │   │   ├── service.yaml
│       │   │   └── configmap.yaml
│       │   └── overlays/
│       │       ├── dev/
│       │       │   ├── kustomization.yaml
│       │       │   ├── patch-deployment.yaml
│       │       │   └── secret.yaml
│       │       └── prod/
│       │           ├── kustomization.yaml
│       │           ├── patch-deployment.yaml
│       │           └── secret.yaml
│       └── helm/
│           └── calculator-app/
│               ├── Chart.yaml
│               ├── values.yaml
│               ├── values-dev.yaml
│               ├── values-prod.yaml
│               └── templates/
│                   ├── _helpers.tpl
│                   ├── deployment.yaml
│                   ├── service.yaml
│                   ├── configmap.yaml
│                   └── secret.yaml
└── telegram-support-infra/
    ├── README.md                        # Контракт для приложения
    └── k8s/
        ├── kustomization/
        │   ├── base/
        │   │   ├── kustomization.yaml
        │   │   ├── postgres-statefulset.yaml
        │   │   └── postgres-service.yaml
        │   └── overlays/
        │       ├── dev/
        │       │   ├── kustomization.yaml
        │       │   ├── patch-statefulset.yaml
        │       │   └── secret.yaml
        │       └── prod/
        │           ├── kustomization.yaml
        │           ├── patch-statefulset.yaml
        │           └── secret.yaml
        └── helm/
            └── postgres-infra/
                ├── Chart.yaml
                ├── values.yaml
                ├── values-dev.yaml
                ├── values-prod.yaml
                └── templates/
                    ├── _helpers.tpl
                    ├── statefulset.yaml
                    ├── service.yaml
                    └── secret.yaml
```

> **Принцип разделения:** в `calculator-app/k8s` нет ни одного манифеста PostgreSQL. Приложение получает строку подключения через Secret, согласованный с контрактом инфраструктуры.

---

## Часть A. Инфраструктура (PostgreSQL)

### Контракт для приложения

После развёртывания `telegram-support-infra` в namespace `N` приложение подключается по следующим параметрам:

| Параметр | Значение |
|----------|----------|
| Хост (внутри кластера) | `postgres-0.postgres.<NAMESPACE>.svc.cluster.local` |
| Короткий хост (тот же namespace) | `postgres-0.postgres` |
| Порт | `5432` |
| Пользователь | `postgres` |
| База данных | `support_bot` |
| Пароль | задаётся в `values-dev.yaml` / overlay `secret.yaml` |

Пример `DATABASE_URL`:
```
postgres://postgres:postgres@postgres-0.postgres:5432/support_bot?sslmode=disable
```

### Различия dev и prod окружений

| Параметр | dev | prod |
|----------|-----|------|
| Пароль | `postgres` (явный, только для стенда) | Плейсхолдер, подставляется из CI |
| PVC size | 1 Gi | 10 Gi |
| memory request | 128 Mi | 512 Mi |
| memory limit | 384 Mi | 1536 Mi |
| cpu request | 50m | 250m |
| cpu limit | 500m | 1000m |

### StatefulSet и Headless Service

PostgreSQL развёрнут как **StatefulSet** с одной репликой. Ключевые особенности:

- **Headless Service** (`clusterIP: None`) даёт стабильный DNS-адрес `postgres-0.postgres.<namespace>.svc.cluster.local` — без него Pod не имеет предсказуемого сетевого имени.
- **PVC через `volumeClaimTemplates`** — данные переживают перезапуск пода, но по умолчанию остаются при удалении StatefulSet (нужно удалять вручную).
- **readinessProbe и livenessProbe** — используют `pg_isready`, чтобы Kubernetes не направлял трафик до готовности БД.

### Вариант A.1 — Helm

```bash
cd lab6/telegram-support-infra

# Dev
helm upgrade --install telegram-support-db ./k8s/helm/postgres-infra \
  --namespace telegram-demo --create-namespace \
  -f ./k8s/helm/postgres-infra/values-dev.yaml

# Prod (пароль из CI, не хранится в Git)
helm upgrade --install telegram-support-db ./k8s/helm/postgres-infra \
  --namespace telegram-demo \
  -f ./k8s/helm/postgres-infra/values-prod.yaml \
  --set password="$PG_PASSWORD"
```

Проверка:
```bash
kubectl get statefulset,pvc,pod -n telegram-demo -l app.kubernetes.io/name=postgres
```

Удаление (PVC остаются — удалите вручную при необходимости):
```bash
helm uninstall telegram-support-db -n telegram-demo
kubectl delete pvc -n telegram-demo -l app.kubernetes.io/name=postgres
```

### Вариант A.2 — Kustomize

Просмотр сгенерированных манифестов без применения:
```bash
kubectl kustomize k8s/kustomization/overlays/dev
```

Применение:
```bash
# Dev (namespace: telegram-demo)
kubectl apply -k k8s/kustomization/overlays/dev

# Prod (namespace: telegram-prod)
kubectl apply -k k8s/kustomization/overlays/prod
```

Проверка готовности пода:
```bash
kubectl get pods,pvc -n telegram-demo -l app=postgres
kubectl logs -n telegram-demo postgres-0 --tail=20
```

---

## Часть B. Приложение (calculator-app)

Манифесты приложения полностью отделены от инфраструктуры. `DATABASE_URL` задаётся через Secret в overlay и указывает на адрес, зафиксированный в контракте инфраструктуры.

### Вариант B.1 — Kustomize

Структура overlays:
- `base/` — Deployment, Service, ConfigMap без секретов
- `overlays/dev/` — namespace `telegram-demo`, Secret с `database-url` на короткий хост БД
- `overlays/prod/` — namespace `telegram-prod`, Secret с FQDN БД из namespace `telegram-demo`

Просмотр и применение:
```bash
cd lab6/calculator-app

# Просмотр без применения
kubectl kustomize k8s/kustomization/overlays/dev

# Применение
kubectl apply -k k8s/kustomization/overlays/dev
```

### Вариант B.2 — Helm

Проверка шаблонов без установки:
```bash
helm template calculator-app ./k8s/helm/calculator-app \
  --namespace telegram-demo \
  -f ./k8s/helm/calculator-app/values-dev.yaml
```

Установка:
```bash
helm upgrade --install calculator-app ./k8s/helm/calculator-app \
  --namespace telegram-demo --create-namespace \
  -f ./k8s/helm/calculator-app/values-dev.yaml
```

Откат релиза:
```bash
helm rollback calculator-app 1 -n telegram-demo
```

Удаление:
```bash
helm uninstall calculator-app -n telegram-demo
```

---

## Порядок деплоя (полный сценарий)

1. Убедиться в наличии StorageClass:
```bash
kubectl get storageclass
```

2. Развернуть инфраструктуру (БД):
```bash
cd lab6/telegram-support-infra
helm upgrade --install telegram-support-db ./k8s/helm/postgres-infra \
  --namespace telegram-demo --create-namespace \
  -f ./k8s/helm/postgres-infra/values-dev.yaml
```

3. Дождаться готовности БД:
```bash
kubectl get pods -n telegram-demo -l app=postgres
# Ожидаем STATUS: Running, READY: 1/1
```

4. Развернуть приложение:
```bash
cd lab6/calculator-app
kubectl apply -k k8s/kustomization/overlays/dev
```

5. Проверить работу:
```bash
kubectl get pods,svc -n telegram-demo
```

---

## Сравнение Kustomize и Helm

| | Kustomize | Helm |
|---|-----------|------|
| Подход | Патчи поверх YAML, без шаблонного языка | Go-шаблоны, values, релиз как единица |
| Версионирование | Нет встроенного понятия версии чарта | `Chart.yaml` с `version` и `appVersion` |
| Откат | Через Git (GitOps) | `helm rollback` из истории релизов |
| Зависимости | Только через ресурсы | `helm dependency` — чарты внутри чарта |
| Удобно когда | Несколько окружений как слои над одной базой | Параметризация, публикация, сложная логика |

Оба инструмента применимы одновременно: Kustomize — для overlay-окружений, Helm — для упаковки и versioned-деплоя.

---

## Безопасность и промышленная норма

- Реальные пароли в Git не хранятся. `values-prod.yaml` содержит плейсхолдер, значение передаётся через `--set` в CI или через External Secrets Operator.
- Для учебного стенда допустим явный пароль только в `values-dev.yaml`.
- Приложение не знает о внутреннем устройстве БД — только о контракте (хост, порт, имя БД).

---
