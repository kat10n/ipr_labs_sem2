# От лабораторной №4 к Kubernetes

## Введение

В лабораторной работе №4 вы настроили CI/CD пайплайн для автоматической сборки и публикации Docker-образа вашего приложения. В этой работе мы используем этот образ для развертывания приложения в Kubernetes.

## Предварительные требования

1. **Docker Desktop с Kubernetes** - см. основную инструкцию в [TASK.md](../TASK.md)
2. **kubectl** - установлен и настроен
3. **Docker образ** - собран и опубликован в GitHub Container Registry

## Шаг 1: Проверка доступа к образу

Убедитесь, что ваш Docker образ доступен на Docker Hub:

```bash
# Проверка образа
docker pull kat10n/calculator:latest
```

## Шаг 2: Настройка Kubernetes манифестов

Kubernetes манифесты уже созданы в директории `k8s/`. Вам нужно заменить плейсхолдеры на реальные значения.

### Обновление deployment.yaml

В файле `k8s/deployment.yaml` образ уже настроен правильно:
```yaml
image: kat10n/calculator:latest
```

## Шаг 3: Развертывание в Kubernetes

```bash
# Переход в директорию с манифестами
cd k8s

# Применение deployment
kubectl apply -f deployment.yaml

# Применение service
kubectl apply -f service.yaml

# Проверка статуса подов
kubectl get pods

# Проверка сервиса
kubectl get services

# Просмотр логов
kubectl logs -l app=calculator
```

## Шаг 4: Доступ к приложению

```bash
# Получение информации о сервисе
kubectl get service calculator-service

# В Docker Desktop найдите EXTERNAL-IP или PORT
# Например: localhost:8080

# Тестирование API
curl http://localhost:8080/health

# Выполнение расчетов
curl -X POST http://localhost:8080/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 10, "b": 5}'
```

## Шаг 5: Масштабирование и обновление

### Масштабирование

```bash
# Изменение количества реплик
kubectl scale deployment calculator-app --replicas=3

# Проверка
kubectl get pods
```

### Обновление образа

```bash
# Обновление образа в deployment
kubectl set image deployment/calculator-app calculator=kat10n/calculator:new-tag

# Проверка rollout
kubectl rollout status deployment/calculator-app
```

## Шаг 6: Мониторинг и отладка

### Просмотр событий

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Описание подов

```bash
kubectl describe pod <pod-name>
```

### Просмотр логов

```bash
# Логи всех подов приложения
kubectl logs -l app=calculator

# Логи конкретного пода
kubectl logs <pod-name>
```

## Очистка

```bash
# Удаление всех ресурсов
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml

# Или удаление по лейблу
kubectl delete all -l app=calculator
```

## Структура манифестов

### Deployment
- **Реплики**: 2 пода для высокой доступности
- **Ресурсы**: Ограничения памяти и CPU
- **Health Checks**: Liveness и Readiness probes для `/health` endpoint
- **Образ**: Из GitHub Container Registry

### Service
- **Тип**: LoadBalancer (в Docker Desktop создает порт-форвардинг)
- **Порт**: 80 -> 8000
- **Селектор**: По лейблу `app=calculator`

## Дополнительные задания

1. **ConfigMap**: Создайте ConfigMap для конфигурации (например, уровень логирования)

2. **Secret**: Добавьте Secret для API ключей или других чувствительных данных

3. **PersistentVolume**: Если нужно хранение данных между перезапусками

4. **Ingress**: Настройте Ingress для внешнего доступа с доменным именем

5. **HorizontalPodAutoscaler**: Автоматическое масштабирование на основе CPU/памяти

6. **NetworkPolicy**: Ограничение сетевого трафика между подами

## Полезные команды

```bash
# Просмотр всех ресурсов
kubectl get all

# Просмотр namespaces
kubectl get namespaces

# Переключение контекста
kubectl config use-context docker-desktop

# Просмотр конфигурации
kubectl config view

# Отладка образов
kubectl run debug --image=busybox --rm -it -- sh
```