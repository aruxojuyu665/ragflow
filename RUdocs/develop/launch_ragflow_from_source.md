---
sidebar_position: 2
slug: /launch_ragflow_from_source
---

# Запуск сервиса из исходного кода

Руководство, объясняющее, как настроить сервис RAGFlow из исходного кода. Следуя этому руководству, вы сможете отлаживать сервис, используя исходный код.

## Целевая аудитория

Разработчики, которые добавили новые функции или изменили существующий код и хотят отлаживать сервис с использованием исходного кода, *при условии*, что на их машине настроена целевая среда развертывания.

## Требования

- CPU &ge; 4 ядра
- ОЗУ &ge; 16 ГБ
- Диск &ge; 50 ГБ
- Docker &ge; 24.0.0 & Docker Compose &ge; v2.26.1

:::tip ПРИМЕЧАНИЕ
Если Docker не установлен на вашей локальной машине (Windows, Mac или Linux), смотрите руководство [Install Docker Engine](https://docs.docker.com/engine/install/).
:::

## Запуск сервиса из исходного кода

Для запуска сервиса RAGFlow из исходного кода:

### Клонирование репозитория RAGFlow

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/
```

### Установка зависимостей Python

1. Установите uv:
   
   ```bash
   pipx install uv
   ```

2. Установите зависимости Python:
   - slim:
   ```bash
   uv sync --python 3.10 # install RAGFlow dependent python modules
   ```
   - full:
   ```bash
   uv sync --python 3.10 # install RAGFlow dependent python modules
   ```
   *Создаётся виртуальное окружение с именем `.venv`, и все зависимости Python устанавливаются в новое окружение.*

### Запуск сторонних сервисов

Следующая команда запускает базовые сервисы (MinIO, Elasticsearch, Redis и MySQL) с помощью Docker Compose:

```bash
docker compose -f docker/docker-compose-base.yml up -d
```

### Обновление настроек `host` и `port` для сторонних сервисов

1. Добавьте следующую строку в `/etc/hosts`, чтобы разрешить все хосты, указанные в **docker/service_conf.yaml.template**, на `127.0.0.1`:

   ```
   127.0.0.1       es01 infinity mysql minio redis
   ```

2. В файле **docker/service_conf.yaml.template** обновите порт mysql на `5455` и порт es на `1200`, как указано в **docker/.env**.

### Запуск backend-сервиса RAGFlow

1. Закомментируйте строку с `nginx` в **docker/entrypoint.sh**.

   ```
   # /usr/sbin/nginx
   ```

2. Активируйте виртуальное окружение Python:

   ```bash
   source .venv/bin/activate
   export PYTHONPATH=$(pwd)
   ```

3. **Опционально:** Если у вас нет доступа к HuggingFace, установите переменную окружения HF_ENDPOINT для использования зеркального сайта:
 
   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   ```

4. Проверьте конфигурацию в **conf/service_conf.yaml**, убедившись, что все хосты и порты настроены корректно.
   
5. Запустите скрипт **entrypoint.sh** для запуска backend-сервиса:

   ```shell
   JEMALLOC_PATH=$(pkg-config --variable=libdir jemalloc)/libjemalloc.so;
   LD_PRELOAD=$JEMALLOC_PATH python rag/svr/task_executor.py 1;
   ```
   ```shell
   python api/ragflow_server.py;
   ```

### Запуск frontend-сервиса RAGFlow

1. Перейдите в директорию `web` и установите зависимости frontend:

   ```bash
   cd web
   npm install
   ```

2. Обновите `proxy.target` в файле **.umirc.ts** на `http://127.0.0.1:9380`:

   ```bash
   vim .umirc.ts
   ```

3. Запустите frontend-сервис RAGFlow:

   ```bash
   npm run dev 
   ```

   *Появится следующее сообщение с IP-адресом и номером порта вашего frontend-сервиса:*  

   ![](https://github.com/user-attachments/assets/0daf462c-a24d-4496-a66f-92533534e187)

### Доступ к сервису RAGFlow

В вашем веб-браузере введите `http://127.0.0.1:<PORT>/`, убедившись, что номер порта совпадает с показанным на скриншоте выше.

### Остановка сервиса RAGFlow после завершения разработки

1. Остановите frontend-сервис RAGFlow:
   ```bash
   pkill npm
   ```

2. Остановите backend-сервис RAGFlow:
   ```bash
   pkill -f "docker/entrypoint.sh"
   ```