---
sidebar_position: 3
slug: /mcp_client

---

# Примеры клиента RAGFlow MCP

Примеры клиента MCP на Python и curl.

------

## Пример клиента MCP на Python

Мы предоставляем *прототип* клиента MCP для тестирования [здесь](https://github.com/infiniflow/ragflow/blob/main/mcp/client/client.py).

:::info IMPORTANT
Если ваш MCP сервер работает в режиме хоста, включите полученный API ключ в `headers` вашего клиента при асинхронном подключении:

```python
async with sse_client("http://localhost:9382/sse", headers={"api_key": "YOUR_KEY_HERE"}) as streams:
    # Остальная часть вашего кода...
```

Альтернативно, для соответствия [OAuth 2.1 Раздел 5](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-12#section-5), вы можете использовать следующий код *вместо* для подключения к вашему MCP серверу:

```python
async with sse_client("http://localhost:9382/sse", headers={"Authorization": "YOUR_KEY_HERE"}) as streams:
    # Остальная часть вашего кода...
```
:::

## Использование curl для взаимодействия с сервером RAGFlow MCP

При взаимодействии с сервером MCP через HTTP-запросы следуйте следующей последовательности инициализации:

1. **Клиент отправляет запрос `initialize`** с версией протокола и возможностями.
2. **Сервер отвечает ответом `initialize`**, включая поддерживаемую версию протокола и возможности.
3. **Клиент подтверждает готовность уведомлением `initialized`**.  
   _Устанавливается соединение между клиентом и сервером, и могут выполняться дальнейшие операции (например, получение списка инструментов)._

:::tip NOTE
Для получения дополнительной информации об этом процессе инициализации смотрите [здесь](https://modelcontextprotocol.io/docs/concepts/architecture#1-initialization). 
:::

В следующих разделах мы подробно рассмотрим полный процесс вызова инструмента.

### 1. Получение session ID

Каждый curl-запрос к серверу MCP должен содержать session ID:

```bash
$ curl -N -H "api_key: YOUR_API_KEY" http://127.0.0.1:9382/sse
```

:::tip NOTE
Информация о получении API ключа доступна [здесь](../acquire_ragflow_api_key.md).
:::

#### Транспорт

Транспорт будет передавать сообщения, такие как результаты инструментов, ответы сервера и пинги для поддержания соединения.

_Сервер возвращает session ID:_

```bash
event: endpoint
data: /messages/?session_id=5c6600ef61b845a788ddf30dceb25c54
```

### 2. Отправка запроса `Initialize`

Клиент отправляет запрос `initialize` с версией протокола и возможностями:

```bash
session_id="5c6600ef61b845a788ddf30dceb25c54" && \

curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "1.0",
      "capabilities": {},
      "clientInfo": {
        "name": "ragflow-mcp-client",
        "version": "0.1"
      }
    }
  }' && \
```

#### Транспорт

_Сервер отвечает ответом `initialize`, включая поддерживаемую версию протокола и возможности:_

```bash
event: message
data: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-03-26","capabilities":{"experimental":{"headers":{"host":"127.0.0.1:9382","user-agent":"curl/8.7.1","accept":"*/*","api_key":"ragflow-xxxxxxxxxxxx","accept-encoding":"gzip"}},"tools":{"listChanged":false}},"serverInfo":{"name":"docker-ragflow-cpu-1","version":"1.9.4"}}}
```

### 3. Подтверждение готовности

Клиент подтверждает готовность уведомлением `initialized`:

```bash
curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
  }' && \
```

 _Устанавливается соединение между клиентом и сервером, и могут выполняться дальнейшие операции (например, получение списка инструментов)._

### 4. Получение списка инструментов

```bash
curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/list",
    "params": {}
  }' && \
```

#### Транспорт

```bash
event: message
data: {"jsonrpc":"2.0","id":3,"result":{"tools":[{"name":"ragflow_retrieval","description":"Извлекает релевантные фрагменты из интерфейса RAGFlow retrieve на основе вопроса, используя указанные dataset_ids и опционально document_ids. Ниже приведён список всех доступных наборов данных с их описаниями и идентификаторами. Если вы не уверены, какие наборы данных релевантны вопросу, просто передайте все идентификаторы наборов данных в функцию.","inputSchema":{"type":"object","properties":{"dataset_ids":{"type":"array","items":{"type":"string"}},"document_ids":{"type":"array","items":{"type":"string"}},"question":{"type":"string"}},"required":["dataset_ids","question"]}}]}}

```

### 5. Вызов инструмента

```bash
curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "ragflow_retrieval",
      "arguments": {
        "question": "How to install neovim?",
        "dataset_ids": ["DATASET_ID_HERE"],
        "document_ids": []
      }
    }
  }'
```

#### Транспорт

```bash
event: message
data: {"jsonrpc":"2.0","id":4,"result":{...}}

```

### Полный пример curl

```bash
session_id="YOUR_SESSION_ID" && \

# Шаг 1: Запрос инициализации
curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "1.0",
      "capabilities": {},
      "clientInfo": {
        "name": "ragflow-mcp-client",
        "version": "0.1"
      }
    }
  }' && \

sleep 2 && \

# Шаг 2: Уведомление о готовности
curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
  }' && \

sleep 2 && \

# Шаг 3: Получение списка инструментов
curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/list",
    "params": {}
  }' && \

sleep 2 && \

# Шаг 4: Вызов инструмента
curl -X POST "http://127.0.0.1:9382/messages/?session_id=$session_id" \
  -H "api_key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "ragflow_retrieval",
      "arguments": {
        "question": "How to install neovim?",
        "dataset_ids": ["DATASET_ID_HERE"],
        "document_ids": []
      }
    }
  }'

```