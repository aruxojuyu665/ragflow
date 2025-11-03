---
sidebar_position: 1
slug: /configurations
---

# Конфигурация

Конфигурации для развертывания RAGFlow через Docker.

## Руководство

Для настройки системы необходимо управлять следующими файлами:

- [.env](https://github.com/infiniflow/ragflow/blob/main/docker/.env): Содержит важные переменные окружения для Docker.
- [service_conf.yaml.template](https://github.com/infiniflow/ragflow/blob/main/docker/service_conf.yaml.template): Конфигурирует бэкенд-сервисы. Определяет системные настройки для RAGFlow и используется его API-сервером и исполнителем задач. При запуске контейнера файл `service_conf.yaml` будет сгенерирован на основе этого шаблона. В процессе все переменные окружения внутри шаблона будут заменены, что позволяет динамически настраивать конфигурацию под окружение контейнера.
- [docker-compose.yml](https://github.com/infiniflow/ragflow/blob/main/docker/docker-compose.yml): Файл Docker Compose для запуска сервиса RAGFlow.

Чтобы изменить порт HTTP-сервера по умолчанию (80), откройте [docker-compose.yml](https://github.com/infiniflow/ragflow/blob/main/docker/docker-compose.yml) и замените `80:80` на `<YOUR_SERVING_PORT>:80`.

:::tip NOTE
Обновления вышеуказанных конфигураций требуют перезапуска всех контейнеров для вступления изменений в силу:

```bash
docker compose -f docker/docker-compose.yml up -d
```

:::

## Docker Compose

- **docker-compose.yml**  
  Настраивает окружение для RAGFlow и его зависимостей.
- **docker-compose-base.yml**  
  Настраивает окружение для зависимостей RAGFlow: Elasticsearch/[Infinity](https://github.com/infiniflow/infinity), MySQL, MinIO и Redis.

:::danger IMPORTANT
Мы не поддерживаем активно **docker-compose-CN-oc9.yml**, **docker-compose-macos.yml**, используйте их на свой страх и риск. Однако вы можете предложить улучшения через pull request.
:::

## Переменные окружения Docker

Файл [.env](https://github.com/infiniflow/ragflow/blob/main/docker/.env) содержит важные переменные окружения для Docker.

### Elasticsearch

- `STACK_VERSION`  
  Версия Elasticsearch. По умолчанию `8.11.3`.
- `ES_PORT`  
  Порт для экспонирования сервиса Elasticsearch на хост-машину, обеспечивающий **внешний** доступ к сервису внутри Docker-контейнера. По умолчанию `1200`.
- `ELASTIC_PASSWORD`  
  Пароль для Elasticsearch.

### Kibana

- `KIBANA_PORT`  
  Порт для экспонирования сервиса Kibana на хост-машину, обеспечивающий **внешний** доступ к сервису внутри Docker-контейнера. По умолчанию `6601`.
- `KIBANA_USER`  
  Имя пользователя для Kibana. По умолчанию `rag_flow`.
- `KIBANA_PASSWORD`  
  Пароль для Kibana. По умолчанию `infini_rag_flow`.

### Управление ресурсами

- `MEM_LIMIT`  
  Максимальный объем памяти в байтах, который *конкретный* Docker-контейнер может использовать во время работы. По умолчанию `8073741824`.

### MySQL

- `MYSQL_PASSWORD`  
  Пароль для MySQL.
- `MYSQL_PORT`  
  Порт для экспонирования сервиса MySQL на хост-машину, обеспечивающий **внешний** доступ к базе данных MySQL внутри Docker-контейнера. По умолчанию `5455`.

### MinIO

RAGFlow использует MinIO в качестве решения для объектного хранилища, используя его масштабируемость для хранения и управления всеми загруженными файлами.

- `MINIO_CONSOLE_PORT`  
  Порт для экспонирования интерфейса консоли MinIO на хост-машину, обеспечивающий **внешний** доступ к веб-консоли внутри Docker-контейнера. По умолчанию `9001`.
- `MINIO_PORT`  
  Порт для экспонирования API-сервиса MinIO на хост-машину, обеспечивающий **внешний** доступ к объектному хранилищу MinIO внутри Docker-контейнера. По умолчанию `9000`.
- `MINIO_USER`  
  Имя пользователя для MinIO.
- `MINIO_PASSWORD`  
  Пароль для MinIO.

### Redis

- `REDIS_PORT`  
  Порт для экспонирования сервиса Redis на хост-машину, обеспечивающий **внешний** доступ к сервису Redis внутри Docker-контейнера. По умолчанию `6379`.
- `REDIS_PASSWORD`  
  Пароль для Redis.

### RAGFlow

- `SVR_HTTP_PORT`  
  Порт для экспонирования HTTP API сервиса RAGFlow на хост-машину, обеспечивающий **внешний** доступ к сервису внутри Docker-контейнера. По умолчанию `9380`.
- `RAGFLOW-IMAGE`  
  Версия Docker-образа. Доступные версии:  
  
  - `infiniflow/ragflow:v0.21.1-slim` (по умолчанию): Docker-образ RAGFlow без моделей embedding (встраивания).  
  - `infiniflow/ragflow:v0.21.1`: Docker-образ RAGFlow с моделями embedding, включая:
    - Встроенные модели embedding:
      - `BAAI/bge-large-zh-v1.5` 
      - `maidalun1020/bce-embedding-base_v1`


:::tip NOTE  
Если не удаётся скачать Docker-образ RAGFlow, попробуйте следующие зеркала.  

- Для версии `nightly`:  
  - `RAGFLOW_IMAGE=swr.cn-north-4.myhuaweicloud.com/infiniflow/ragflow:nightly` или,
  - `RAGFLOW_IMAGE=registry.cn-hangzhou.aliyuncs.com/infiniflow/ragflow:nightly`.
:::

### Сервис embedding

- `TEI_MODEL`  
  Модель embedding, которую обслуживает text-embeddings-inference. Допустимые значения: `Qwen/Qwen3-Embedding-0.6B` (по умолчанию), `BAAI/bge-m3`, и `BAAI/bge-small-en-v1.5`.

- `TEI_PORT`  
  Порт для экспонирования сервиса text-embeddings-inference на хост-машину, обеспечивающий **внешний** доступ к сервису внутри Docker-контейнера. По умолчанию `6380`.

### Часовой пояс

- `TZ`  
  Локальный часовой пояс. По умолчанию `Asia/Shanghai`.

### Зеркальный сайт Hugging Face

- `HF_ENDPOINT`  
  Зеркальный сайт для huggingface.co. По умолчанию отключён. Вы можете раскомментировать эту строку, если у вас ограничен доступ к основному домену Hugging Face.

### MacOS

- `MACOS`  
  Оптимизации для macOS. По умолчанию отключено. Вы можете раскомментировать эту строку, если ваша ОС — macOS.

### Регистрация пользователей

- `REGISTER_ENABLED`
  - `1`: (По умолчанию) Включить регистрацию пользователей.
  - `0`: Отключить регистрацию пользователей.

## Конфигурация сервиса

[service_conf.yaml.template](https://github.com/infiniflow/ragflow/blob/main/docker/service_conf.yaml.template) задаёт системные настройки для RAGFlow и используется его API-сервером и исполнителем задач.

### `ragflow`

- `host`: IP-адрес API-сервера внутри Docker-контейнера. По умолчанию `0.0.0.0`.
- `port`: Порт API-сервера внутри Docker-контейнера. По умолчанию `9380`.

### `mysql`
  
- `name`: Имя базы данных MySQL. По умолчанию `rag_flow`.
- `user`: Имя пользователя MySQL.
- `password`: Пароль MySQL.
- `port`: Порт MySQL внутри Docker-контейнера. По умолчанию `3306`.
- `max_connections`: Максимальное количество одновременных подключений к базе данных MySQL. По умолчанию `100`.
- `stale_timeout`: Таймаут в секундах.

### `minio`
  
- `user`: Имя пользователя MinIO.
- `password`: Пароль MinIO.
- `host`: IP-адрес *и* порт MinIO внутри Docker-контейнера. По умолчанию `minio:9000`.

### `oauth`  

Конфигурация OAuth для регистрации или входа в RAGFlow через сторонний аккаунт.

- `<channel>`: Пользовательский идентификатор канала.
  - `type`: Тип аутентификации, варианты: `oauth2`, `oidc`, `github`. По умолчанию `oauth2`, при наличии параметра `issuer` по умолчанию `oidc`.
  - `icon`: Идентификатор иконки, варианты: `github`, `sso`, по умолчанию `sso`.
  - `display_name`: Название канала, по умолчанию формат с заглавной буквы от ID канала.
  - `client_id`: Обязательный, уникальный идентификатор клиента.
  - `client_secret`: Обязательный, секретный ключ клиента для взаимодействия с сервером аутентификации.
  - `authorization_url`: Базовый URL для получения авторизации пользователя.
  - `token_url`: URL для обмена кода авторизации на токен доступа.
  - `userinfo_url`: URL для получения информации о пользователе (имя, email и т.д.).
  - `issuer`: Базовый URL провайдера идентификации. Клиенты OIDC могут динамически получать метаданные провайдера (`authorization_url`, `token_url`, `userinfo_url`) через `issuer`.
  - `scope`: Запрашиваемые права доступа, строка с разделением пробелами. Например, `openid profile email`.
  - `redirect_uri`: Обязательный, URI, на который сервер авторизации перенаправляет в процессе аутентификации для возврата результата. Должен совпадать с зарегистрированным callback URI на сервере аутентификации. Формат: `https://your-app.com/v1/user/oauth/callback/<channel>`. Для локальной конфигурации можно использовать `http://127.0.0.1:80/v1/user/oauth/callback/<channel>`.

:::tip NOTE 
Ниже приведены лучшие практики настройки различных сторонних методов аутентификации. Вы можете настроить один или несколько методов для Ragflow:
```yaml
oauth:
  oauth2:
    display_name: "OAuth2"
    client_id: "your_client_id"
    client_secret: "your_client_secret"
    authorization_url: "https://your-oauth-provider.com/oauth/authorize"
    token_url: "https://your-oauth-provider.com/oauth/token"
    userinfo_url: "https://your-oauth-provider.com/oauth/userinfo"
    redirect_uri: "https://your-app.com/v1/user/oauth/callback/oauth2"

  oidc:
    display_name: "OIDC"
    client_id: "your_client_id"
    client_secret: "your_client_secret"
    issuer: "https://your-oauth-provider.com/oidc"
    scope: "openid email profile"
    redirect_uri: "https://your-app.com/v1/user/oauth/callback/oidc"

  github:
    # https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app
    type: "github"
    icon: "github"
    display_name: "Github"
    client_id: "your_client_id"
    client_secret: "your_client_secret"
    redirect_uri: "https://your-app.com/v1/user/oauth/callback/github"
```
:::

### `user_default_llm`  

LLM (Large Language Model, большая языковая модель) по умолчанию для нового пользователя RAGFlow. По умолчанию отключена. Чтобы включить эту функцию, раскомментируйте соответствующие строки в **service_conf.yaml.template**.  

- `factory`: Поставщик LLM. Доступные варианты:
  - `"OpenAI"`
  - `"DeepSeek"`
  - `"Moonshot"`
  - `"Tongyi-Qianwen"`
  - `"VolcEngine"`
  - `"ZHIPU-AI"`
- `api_key`: API-ключ для указанной LLM. Необходимо получить ключ для вашей модели онлайн.

:::tip NOTE  
Если вы не зададите LLM по умолчанию здесь, настройте её на странице **Settings** в интерфейсе RAGFlow.
:::