---
sidebar_position: 8
slug: /run_health_check
---

# Мониторинг

Дважды проверьте состояние здоровья (health status) зависимостей RAGFlow.

---

Работа RAGFlow зависит от четырёх сервисов:

- **Elasticsearch** (по умолчанию) или [Infinity](https://github.com/infiniflow/infinity) в качестве движка документов
- **MySQL**
- **Redis**
- **MinIO** для объектного хранилища

Если возникает исключение или ошибка, связанная с любым из перечисленных сервисов, например `Exception: Can't connect to ES cluster`, обратитесь к этому документу для проверки их состояния здоровья.

Вы также можете нажать на свой аватар в правом верхнем углу страницы **>** System, чтобы просмотреть визуализированный статус здоровья основных сервисов RAGFlow. На следующем скриншоте показано, что все сервисы имеют статус «зелёный» (работают исправно). Исполнитель задач отображает *накопительное* количество завершённых и неудачных задач парсинга документов за последние 30 минут:

![system_status_page](https://github.com/user-attachments/assets/b0c1a11e-93e3-4947-b17a-1bfb4cdab6e4)

Сервисы с жёлтым или красным индикатором работают некорректно. Ниже представлен скриншот страницы системы после выполнения команды `docker stop ragflow-es-10`:

![es_failed](https://github.com/user-attachments/assets/06056540-49f5-48bf-9cc9-a7086bc75790)

Вы можете кликнуть на конкретный 30-секундный интервал времени, чтобы просмотреть детали завершённых и неудачных задач:

![done_tasks](https://github.com/user-attachments/assets/49b25ec4-03af-48cf-b2e5-c892f6eaa261)

![done_vs_failed](https://github.com/user-attachments/assets/eaa928d0-a31c-4072-adea-046091e04599)

## API Проверка состояния здоровья (Health Check)

Помимо проверки системных зависимостей через страницу **avatar > System** в пользовательском интерфейсе, вы можете напрямую обратиться к endpoint проверки состояния здоровья бэкенда:

```bash
http://IP_OF_YOUR_MACHINE/v1/system/healthz
```

Здесь `<port>` означает фактический порт вашего бэкенд-сервиса (например, `7897`, `9222` и т.д.).

Основные моменты:
- **Авторизация не требуется** (нет декоратора `@login_required`)
- Возвращает результаты в формате JSON
- Если все зависимости работают исправно → HTTP **200 OK**
- Если какая-либо зависимость не работает → HTTP **500 Internal Server Error**

### Пример 1: Все сервисы работают исправно (HTTP 200)

```bash
http://127.0.0.1/v1/system/healthz
```

Ответ:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 120

{
  "db": "ok",
  "redis": "ok",
  "doc_engine": "ok",
  "storage": "ok",
  "status": "ok"
}
```

Пояснение:
- База данных (MySQL/Postgres), Redis, движок документов (Elasticsearch/Infinity) и объектное хранилище (MinIO) все работают исправно.
- Поле `status` возвращает `"ok"`.

### Пример 2: Один сервис не работает (HTTP 500)

Например, если Redis не доступен:

Ответ:

```http
HTTP/1.1 500 INTERNAL SERVER ERROR
Content-Type: application/json
Content-Length: 300

{
  "db": "ok",
  "redis": "nok",
  "doc_engine": "ok",
  "storage": "ok",
  "status": "nok",
  "_meta": {
    "redis": {
      "elapsed": "5.2",
      "error": "Lost connection!"
    }
  }
}
```

Пояснение:
- `redis` отмечен как `"nok"`, с подробной информацией об ошибке в `_meta.redis.error`.
- Общий `status` равен `"nok"`, поэтому endpoint возвращает 500.

---

Этот endpoint позволяет программно мониторить основные зависимости RAGFlow в скриптах или внешних системах мониторинга без необходимости использовать фронтенд UI.