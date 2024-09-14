# FaceVerificationService

Сервис для векторизации изображения.
Сервис предоставляет api, а также работает как consumer, обрабатывая сообщения из кафки.

Этот сервис является частью группы микросервисов, входной точкой для которых является [ApiGateway](https://github.com/KoTBegemoTT/ApiGateway)

# REST API

`POST /get_vector/`

- Возвращает векторное представление изображения

`GET /healthz/ready/`

- Проверка состояния сервиса. Возвращает статус код 200 в случае успеха

## Развёртывание в kubernetes

### Порядок развёртывания

1. Transaction
2. Auth
3. Face-Verification
4. ApiGateway

### Продакшен

```bash
cd helm/face-verification
helm install my-release-name .
```

### Тестирование

```bash
cd helm/face-verification
helm install my-release-name --values ./values/test.yaml
```