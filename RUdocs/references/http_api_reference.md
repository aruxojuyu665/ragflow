---
sidebar_position: 4
slug: /http_api_reference
---

# HTTP API

Полное руководство по RESTful API RAGFlow. Перед началом убедитесь, что у вас [есть ключ API RAGFlow для аутентификации](https://ragflow.io/docs/dev/acquire_ragflow_api_key).

---

## КОДЫ ОШИБОК

---

| Код  | Сообщение             | Описание                   |
| -----|-----------------------|----------------------------|
| 400  | Bad Request           | Неверные параметры запроса |
| 401  | Unauthorized          | Несанкционированный доступ |
| 403  | Forbidden             | Доступ запрещён             |
| 404  | Not Found             | Ресурс не найден           |
| 500  | Internal Server Error | Внутренняя ошибка сервера  |
| 1001 | Invalid Chunk ID      | Неверный Chunk ID          |
| 1002 | Chunk Update Failed   | Ошибка обновления Chunk    |

---

## OpenAI-совместимый API

---

### Создать завершение чата

**POST** `/api/v1/chats_openai/{chat_id}/chat/completions`

Создаёт ответ модели для заданной беседы в чате.

Этот API использует тот же формат запроса и ответа, что и API OpenAI. Позволяет взаимодействовать с моделью аналогично [API OpenAI](https://platform.openai.com/docs/api-reference/chat/create).

#### Запрос

- Метод: POST
- URL: `/api/v1/chats_openai/{chat_id}/chat/completions`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"model"`: `string`
  - `"messages"`: `список объектов`
  - `"stream"`: `boolean`

##### Пример запроса

```bash
curl --request POST \
     --url http://{address}/api/v1/chats_openai/{chat_id}/chat/completions \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '{
        "model": "model",
        "messages": [{"role": "user", "content": "Say this is a test!"}],
        "stream": true
      }'
```

##### Параметры запроса

- `model` (*параметр тела*) `string`, *Обязательно*  
  Модель, используемая для генерации ответа. Сервер распознает это автоматически, поэтому пока можно указать любое значение.

- `messages` (*параметр тела*) `список объектов`, *Обязательно*  
  Список исторических сообщений чата, используемых для генерации ответа. Должен содержать хотя бы одно сообщение с ролью `user`.

- `stream` (*параметр тела*) `boolean`  
  Получать ответ в виде потока. Явно установите в `false`, если хотите получить полный ответ целиком, а не поток.

#### Ответ

Поток:

```json
data:{
    "id": "chatcmpl-3b0397f277f511f0b47f729e3aa55728",
    "choices": [
        {
            "delta": {
                "content": "Hello! It seems like you're just greeting me. If you have a specific",
                "role": "assistant",
                "function_call": null,
                "tool_calls": null,
                "reasoning_content": null
            },
            "finish_reason": null,
            "index": 0,
            "logprobs": null
        }
    ],
    "created": 1755084508,
    "model": "model",
    "object": "chat.completion.chunk",
    "system_fingerprint": "",
    "usage": null
}

data:{"id": "chatcmpl-3b0397f277f511f0b47f729e3aa55728", "choices": [{"delta": {"content": " question or need information, feel free to ask, and I'll do my best", "role": "assistant", "function_call": null, "tool_calls": null, "reasoning_content": null}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1755084508, "model": "model", "object": "chat.completion.chunk", "system_fingerprint": "", "usage": null}

data:{"id": "chatcmpl-3b0397f277f511f0b47f729e3aa55728", "choices": [{"delta": {"content": " to assist you based on the knowledge base provided.", "role": "assistant", "function_call": null, "tool_calls": null, "reasoning_content": null}, "finish_reason": null, "index": 0, "logprobs": null}], "created": 1755084508, "model": "model", "object": "chat.completion.chunk", "system_fingerprint": "", "usage": null}

data:{"id": "chatcmpl-3b0397f277f511f0b47f729e3aa55728", "choices": [{"delta": {"content": null, "role": "assistant", "function_call": null, "tool_calls": null, "reasoning_content": null}, "finish_reason": "stop", "index": 0, "logprobs": null}], "created": 1755084508, "model": "model", "object": "chat.completion.chunk", "system_fingerprint": "", "usage": {"prompt_tokens": 5, "completion_tokens": 188, "total_tokens": 193}}

data:[DONE]
```

Без потока:

```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null,
            "message": {
                "content": "Hello! I'm your smart assistant. What can I do for you?",
                "role": "assistant"
            }
        }
    ],
    "created": 1755084403,
    "id": "chatcmpl-3b0397f277f511f0b47f729e3aa55728",
    "model": "model",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 55,
        "completion_tokens_details": {
            "accepted_prediction_tokens": 55,
            "reasoning_tokens": 5,
            "rejected_prediction_tokens": 0
        },
        "prompt_tokens": 5,
        "total_tokens": 60
    }
}
```

Ошибка:

```json
{
  "code": 102,
  "message": "The last content of this conversation is not from user."
}
```

---

### Создать завершение агента

**POST** `/api/v1/agents_openai/{agent_id}/chat/completions`

Создаёт ответ модели для заданной беседы в чате.

Этот API использует тот же формат запроса и ответа, что и API OpenAI. Позволяет взаимодействовать с моделью аналогично [API OpenAI](https://platform.openai.com/docs/api-reference/chat/create).

#### Запрос

- Метод: POST
- URL: `/api/v1/agents_openai/{agent_id}/chat/completions`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"model"`: `string`
  - `"messages"`: `список объектов`
  - `"stream"`: `boolean`

##### Пример запроса

```bash
curl --request POST \
     --url http://{address}/api/v1/agents_openai/{agent_id}/chat/completions \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '{
        "model": "model",
        "messages": [{"role": "user", "content": "Say this is a test!"}],
        "stream": true
      }'
```

##### Параметры запроса

- `model` (*параметр тела*) `string`, *Обязательно*  
  Модель, используемая для генерации ответа. Сервер распознает это автоматически, поэтому пока можно указать любое значение.

- `messages` (*параметр тела*) `список объектов`, *Обязательно*  
  Список исторических сообщений чата, используемых для генерации ответа. Должен содержать хотя бы одно сообщение с ролью `user`.

- `stream` (*параметр тела*) `boolean`  
  Получать ответ в виде потока. Явно установите в `false`, если хотите получить полный ответ целиком, а не поток.

- `session_id` (*параметр тела*) `string`  
  ID сессии агента.

#### Ответ

Поток:

```json
...

data: {
    "id": "c39f6f9c83d911f0858253708ecb6573",
    "object": "chat.completion.chunk",
    "model": "d1f79142831f11f09cc51795b9eb07c0",
    "choices": [
        {
            "delta": {
                "content": " terminal"
            },
            "finish_reason": null,
            "index": 0
        }
    ]
}

data: {
    "id": "c39f6f9c83d911f0858253708ecb6573",
    "object": "chat.completion.chunk",
    "model": "d1f79142831f11f09cc51795b9eb07c0",
    "choices": [
        {
            "delta": {
                "content": "."
            },
            "finish_reason": null,
            "index": 0
        }
    ]
}

data: {
    "id": "c39f6f9c83d911f0858253708ecb6573",
    "object": "chat.completion.chunk",
    "model": "d1f79142831f11f09cc51795b9eb07c0",
    "choices": [
        {
            "delta": {
                "content": "",
                "reference": {
                    "chunks": {
                        "20": {
                            "id": "4b8935ac0a22deb1",
                            "content": "```cd /usr/ports/editors/neovim/ && make install```## Android[Termux](https://github.com/termux/termux-app) предлагает пакет Neovim.",
                            "document_id": "4bdd2ff65e1511f0907f09f583941b45",
                            "document_name": "INSTALL22.md",
                            "dataset_id": "456ce60c5e1511f0907f09f583941b45",
                            "image_id": "",
                            "positions": [
                                [
                                    12,
                                    11,
                                    11,
                                    11,
                                    11
                                ]
                            ],
                            "url": null,
                            "similarity": 0.5697155305154673,
                            "vector_similarity": 0.7323851005515574,
                            "term_similarity": 0.5000000005,
                            "doc_type": ""
                        }
                    },
                    "doc_aggs": {
                        "INSTALL22.md": {
                            "doc_name": "INSTALL22.md",
                            "doc_id": "4bdd2ff65e1511f0907f09f583941b45",
                            "count": 3
                        },
                        "INSTALL.md": {
                            "doc_name": "INSTALL.md",
                            "doc_id": "4bd7fdd85e1511f0907f09f583941b45",
                            "count": 2
                        },
                        "INSTALL(1).md": {
                            "doc_name": "INSTALL(1).md",
                            "doc_id": "4bdfb42e5e1511f0907f09f583941b45",
                            "count": 2
                        },
                        "INSTALL3.md": {
                            "doc_name": "INSTALL3.md",
                            "doc_id": "4bdab5825e1511f0907f09f583941b45",
                            "count": 1
                        }
                    }
                }
            },
            "finish_reason": null,
            "index": 0
        }
    ]
}

data: [DONE]
```

Без потока:

```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null,
            "message": {
                "content": "\nДля установки Neovim процесс зависит от вашей операционной системы:\n\n### Для Windows:\n1. **Скачать с GitHub**: \n   - Посетите [страницу релизов Neovim](https://github.com/neovim/neovim/releases)\n   - Скачайте последний установщик для Windows (nvim-win64.msi)\n   - Запустите установщик и следуйте инструкциям\n\n2. **Использование winget** (Windows Package Manager):\n...",
                "reference": {
                    "chunks": {
                        "20": {
                            "content": "```cd /usr/ports/editors/neovim/ && make install```## Android[Termux](https://github.com/termux/termux-app) предлагает пакет Neovim.",
                            "dataset_id": "456ce60c5e1511f0907f09f583941b45",
                            "doc_type": "",
                            "document_id": "4bdd2ff65e1511f0907f09f583941b45",
                            "document_name": "INSTALL22.md",
                            "id": "4b8935ac0a22deb1",
                            "image_id": "",
                            "positions": [
                                [
                                    12,
                                    11,
                                    11,
                                    11,
                                    11
                                ]
                            ],
                            "similarity": 0.5697155305154673,
                            "term_similarity": 0.5000000005,
                            "url": null,
                            "vector_similarity": 0.7323851005515574
                        }
                    },
                    "doc_aggs": {
                        "INSTALL(1).md": {
                            "count": 2,
                            "doc_id": "4bdfb42e5e1511f0907f09f583941b45",
                            "doc_name": "INSTALL(1).md"
                        },
                        "INSTALL.md": {
                            "count": 2,
                            "doc_id": "4bd7fdd85e1511f0907f09f583941b45",
                            "doc_name": "INSTALL.md"
                        },
                        "INSTALL22.md": {
                            "count": 3,
                            "doc_id": "4bdd2ff65e1511f0907f09f583941b45",
                            "doc_name": "INSTALL22.md"
                        },
                        "INSTALL3.md": {
                            "count": 1,
                            "doc_id": "4bdab5825e1511f0907f09f583941b45",
                            "doc_name": "INSTALL3.md"
                        }
                    }
                },
                "role": "assistant"
            }
        }
    ],
    "created": null,
    "id": "c39f6f9c83d911f0858253708ecb6573",
    "model": "d1f79142831f11f09cc51795b9eb07c0",
    "object": "chat.completion",
    "param": null,
    "usage": {
        "completion_tokens": 415,
        "completion_tokens_details": {
            "accepted_prediction_tokens": 0,
            "reasoning_tokens": 0,
            "rejected_prediction_tokens": 0
        },
        "prompt_tokens": 6,
        "total_tokens": 421
    }
}
```

Ошибка:

```json
{
  "code": 102,
  "message": "The last content of this conversation is not from user."
}
```

## УПРАВЛЕНИЕ НАБОРАМИ ДАННЫХ

---

### Создать набор данных

**POST** `/api/v1/datasets`

Создаёт набор данных.

#### Запрос

- Метод: POST
- URL: `/api/v1/datasets`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"name"`: `string`
  - `"avatar"`: `string`
  - `"description"`: `string`
  - `"embedding_model"`: `string`
  - `"permission"`: `string`
  - `"chunk_method"`: `string`
  - `"parser_config"`: `object`

##### Пример запроса

```bash
curl --request POST \
     --url http://{address}/api/v1/datasets \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '{
      "name": "test_1"
      }'
```

##### Параметры запроса

- `"name"`: (*параметр тела*), `string`, *Обязательно*  
  Уникальное имя создаваемого набора данных. Должно соответствовать следующим требованиям:  
  - Только символы из Basic Multilingual Plane (BMP)
  - Максимум 128 символов
  - Регистр не учитывается

- `"avatar"`: (*параметр тела*), `string`  
  Base64-кодировка аватара.
  - Максимум 65535 символов

- `"description"`: (*параметр тела*), `string`  
  Краткое описание создаваемого набора данных.
  - Максимум 65535 символов

- `"embedding_model"`: (*параметр тела*), `string`  
  Имя модели эмбеддинга для использования. Например: `"BAAI/bge-large-zh-v1.5@BAAI"`
  - Максимум 255 символов
  - Должно соответствовать формату `model_name@model_factory`

- `"permission"`: (*параметр тела*), `string`  
  Определяет, кто может получить доступ к создаваемому набору данных. Доступные варианты:  
  - `"me"`: (по умолчанию) Только вы можете управлять набором данных.
  - `"team"`: Все члены команды могут управлять набором данных.

- `"chunk_method"`: (*параметр тела*), `enum<string>`  
  Метод разбиения на чанки для создаваемого набора данных. Доступные варианты:  
  - `"naive"`: Общий (по умолчанию)
  - `"book"`: Книга
  - `"email"`: Электронная почта
  - `"laws"`: Законы
  - `"manual"`: Ручной
  - `"one"`: Один
  - `"paper"`: Статья
  - `"picture"`: Изображение
  - `"presentation"`: Презентация
  - `"qa"`: Вопрос-Ответ
  - `"table"`: Таблица
  - `"tag"`: Тег

- `"parser_config"`: (*параметр тела*), `object`  
  Конфигурация парсера набора данных. Атрибуты в этом JSON-объекте зависят от выбранного `"chunk_method"`:  
  - Если `"chunk_method"` равен `"naive"`, объект `"parser_config"` содержит следующие атрибуты:
    - `"auto_keywords"`: `int`
      - По умолчанию `0`
      - Минимум: `0`
      - Максимум: `32`
    - `"auto_questions"`: `int`
      - По умолчанию `0`
      - Минимум: `0`
      - Максимум: `10`
    - `"chunk_token_num"`: `int`
      - По умолчанию `512`
      - Минимум: `1`
      - Максимум: `2048`
    - `"delimiter"`: `string`
      - По умолчанию `"\n"`.
    - `"html4excel"`: `bool` Указывает, следует ли конвертировать документы Excel в HTML.
      - По умолчанию `false`
    - `"layout_recognize"`: `string`
      - По умолчанию `DeepDOC`
    - `"tag_kb_ids"`: `array<string>` см. [Использование набора тегов](https://ragflow.io/docs/dev/use_tag_sets)
      - Должен содержать список ID наборов данных, каждый из которых парсится с использованием метода Tag Chunking
    - `"task_page_size"`: `int` Только для PDF.
      - По умолчанию `12`
      - Минимум: `1`
    - `"raptor"`: `object` Настройки RAPTOR.
      - По умолчанию: `{"use_raptor": false}`
    - `"graphrag"`: `object` Настройки GRAPHRAG.
      - По умолчанию: `{"use_graphrag": false}`
  - Если `"chunk_method"` равен `"qa"`, `"manuel"`, `"paper"`, `"book"`, `"laws"` или `"presentation"`, объект `"parser_config"` содержит следующий атрибут:  
    - `"raptor"`: `object` Настройки RAPTOR.
      - По умолчанию: `{"use_raptor": false}`.
  - Если `"chunk_method"` равен `"table"`, `"picture"`, `"one"` или `"email"`, `"parser_config"` — пустой JSON-объект.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": {
        "avatar": null,
        "chunk_count": 0,
        "chunk_method": "naive",
        "create_date": "Mon, 28 Apr 2025 18:40:41 GMT",
        "create_time": 1745836841611,
        "created_by": "3af81804241d11f0a6a79f24fc270c7f",
        "description": null,
        "document_count": 0,
        "embedding_model": "BAAI/bge-large-zh-v1.5@BAAI",
        "id": "3b4de7d4241d11f0a6a79f24fc270c7f",
        "language": "English",
        "name": "RAGFlow example",
        "pagerank": 0,
        "parser_config": {
            "chunk_token_num": 128, 
            "delimiter": "\\n!?;。；！？", 
            "html4excel": false, 
            "layout_recognize": "DeepDOC", 
            "raptor": {
                "use_raptor": false
                }
            },
        "permission": "me",
        "similarity_threshold": 0.2,
        "status": "1",
        "tenant_id": "3af81804241d11f0a6a79f24fc270c7f",
        "token_num": 0,
        "update_date": "Mon, 28 Apr 2025 18:40:41 GMT",
        "update_time": 1745836841611,
        "vector_similarity_weight": 0.3,
    },
}
```

Ошибка:

```json
{
    "code": 101,
    "message": "Dataset name 'RAGFlow example' already exists"
}
```

---

### Удалить наборы данных

**DELETE** `/api/v1/datasets`

Удаляет наборы данных по ID.

#### Запрос

- Метод: DELETE
- URL: `/api/v1/datasets`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"ids"`: `список[string]` или `null`

##### Пример запроса

```bash
curl --request DELETE \
     --url http://{address}/api/v1/datasets \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '{
     "ids": ["d94a8dc02c9711f0930f7fbc369eab6d", "e94a8dc02c9711f0930f7fbc369eab6e"]
     }'
```

##### Параметры запроса

- `"ids"`: (*параметр тела*), `список[string]` или `null`, *Обязательно*  
  Указывает наборы данных для удаления:
  - Если `null`, будут удалены все наборы данных.
  - Если массив ID, будут удалены только указанные наборы.
  - Если пустой массив, ничего не удаляется.

#### Ответ

Успех:

```json
{
    "code": 0 
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "You don't own the dataset."
}
```

---

### Обновить набор данных

**PUT** `/api/v1/datasets/{dataset_id}`

Обновляет конфигурации указанного набора данных.

#### Запрос

- Метод: PUT
- URL: `/api/v1/datasets/{dataset_id}`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"name"`: `string`
  - `"avatar"`: `string`
  - `"description"`: `string`
  - `"embedding_model"`: `string`
  - `"permission"`: `string`
  - `"chunk_method"`: `string`
  - `"pagerank"`: `int`
  - `"parser_config"`: `object`

##### Пример запроса

```bash
curl --request PUT \
     --url http://{address}/api/v1/datasets/{dataset_id} \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {
          "name": "updated_dataset"
     }'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID набора данных для обновления.
- `"name"`: (*параметр тела*), `string`  
  Новое имя набора данных.
  - Только символы из Basic Multilingual Plane (BMP)
  - Максимум 128 символов
  - Регистр не учитывается
- `"avatar"`: (*параметр тела*), `string`  
  Обновлённая base64-кодировка аватара.
  - Максимум 65535 символов
- `"embedding_model"`: (*параметр тела*), `string`  
  Обновлённое имя модели эмбеддинга.  
  - Перед обновлением `"embedding_model"` убедитесь, что `"chunk_count"` равен `0`.
  - Максимум 255 символов
  - Должно соответствовать формату `model_name@model_factory`
- `"permission"`: (*параметр тела*), `string`  
  Обновлённые права доступа к набору данных. Доступные варианты:  
  - `"me"`: (по умолчанию) Только вы можете управлять набором данных.
  - `"team"`: Все члены команды могут управлять набором данных.
- `"pagerank"`: (*параметр тела*), `int`  
  см. [Установка page rank](https://ragflow.io/docs/dev/set_page_rank)
  - По умолчанию: `0`
  - Минимум: `0`
  - Максимум: `100`
- `"chunk_method"`: (*параметр тела*), `enum<string>`  
  Метод разбиения на чанки для набора данных. Доступные варианты:  
  - `"naive"`: Общий (по умолчанию)
  - `"book"`: Книга
  - `"email"`: Электронная почта
  - `"laws"`: Законы
  - `"manual"`: Ручной
  - `"one"`: Один
  - `"paper"`: Статья
  - `"picture"`: Изображение
  - `"presentation"`: Презентация
  - `"qa"`: Вопрос-Ответ
  - `"table"`: Таблица
  - `"tag"`: Тег
- `"parser_config"`: (*параметр тела*), `object`  
  Конфигурация парсера набора данных. Атрибуты зависят от выбранного `"chunk_method"`:  
  - Если `"chunk_method"` равен `"naive"`, объект `"parser_config"` содержит следующие атрибуты:
    - `"auto_keywords"`: `int`
      - По умолчанию `0`
      - Минимум: `0`
      - Максимум: `32`
    - `"auto_questions"`: `int`
      - По умолчанию `0`
      - Минимум: `0`
      - Максимум: `10`
    - `"chunk_token_num"`: `int`
      - По умолчанию `512`
      - Минимум: `1`
      - Максимум: `2048`
    - `"delimiter"`: `string`
      - По умолчанию `"\n"`.
    - `"html4excel"`: `bool` Указывает, следует ли конвертировать документы Excel в HTML.
      - По умолчанию `false`
    - `"layout_recognize"`: `string`
      - По умолчанию `DeepDOC`
    - `"tag_kb_ids"`: `array<string>` см. [Использование набора тегов](https://ragflow.io/docs/dev/use_tag_sets)
      - Должен содержать список ID наборов данных, каждый из которых парсится методом Tag Chunking
    - `"task_page_size"`: `int` Только для PDF.
      - По умолчанию `12`
      - Минимум: `1`
    - `"raptor"`: `object` Настройки RAPTOR.
      - По умолчанию: `{"use_raptor": false}`
    - `"graphrag"`: `object` Настройки GRAPHRAG.
      - По умолчанию: `{"use_graphrag": false}`
  - Если `"chunk_method"` равен `"qa"`, `"manuel"`, `"paper"`, `"book"`, `"laws"` или `"presentation"`, объект `"parser_config"` содержит следующий атрибут:  
    - `"raptor"`: `object` Настройки RAPTOR.
      - По умолчанию: `{"use_raptor": false}`.
  - Если `"chunk_method"` равен `"table"`, `"picture"`, `"one"` или `"email"`, `"parser_config"` — пустой JSON-объект.

#### Ответ

Успех:

```json
{
    "code": 0 
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "Can't change tenant_id."
}
```

---

### Список наборов данных

**GET** `/api/v1/datasets?page={page}&page_size={page_size}&orderby={orderby}&desc={desc}&name={dataset_name}&id={dataset_id}`

Получение списка наборов данных.

#### Запрос

- Метод: GET
- URL: `/api/v1/datasets?page={page}&page_size={page_size}&orderby={orderby}&desc={desc}&name={dataset_name}&id={dataset_id}`
- Заголовки:
  - `'Authorization: Bearer <YOUR_API_KEY>'`

##### Пример запроса

```bash
curl --request GET \
     --url http://{address}/api/v1/datasets?page={page}&page_size={page_size}&orderby={orderby}&desc={desc}&name={dataset_name}&id={dataset_id} \
     --header 'Authorization: Bearer <YOUR_API_KEY>'
```

##### Параметры запроса

- `page`: (*параметр фильтра*)  
  Номер страницы для отображения наборов данных. По умолчанию `1`.
- `page_size`: (*параметр фильтра*)  
  Количество наборов данных на странице. По умолчанию `30`.
- `orderby`: (*параметр фильтра*)  
  Поле для сортировки наборов данных. Доступные варианты:
  - `create_time` (по умолчанию)
  - `update_time`
- `desc`: (*параметр фильтра*)  
  Сортировать ли в порядке убывания. По умолчанию `true`.
- `name`: (*параметр фильтра*)  
  Имя набора данных для поиска.
- `id`: (*параметр фильтра*)  
  ID набора данных для поиска.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": [
        {
            "avatar": "",
            "chunk_count": 59,
            "create_date": "Sat, 14 Sep 2024 01:12:37 GMT",
            "create_time": 1726276357324,
            "created_by": "69736c5e723611efb51b0242ac120007",
            "description": null,
            "document_count": 1,
            "embedding_model": "BAAI/bge-large-zh-v1.5",
            "id": "6e211ee0723611efa10a0242ac120007",
            "language": "English",
            "name": "mysql",
            "chunk_method": "naive",
            "parser_config": {
                "chunk_token_num": 8192,
                "delimiter": "\\n",
                "entity_types": [
                    "organization",
                    "person",
                    "location",
                    "event",
                    "time"
                ]
            },
            "permission": "me",
            "similarity_threshold": 0.2,
            "status": "1",
            "tenant_id": "69736c5e723611efb51b0242ac120007",
            "token_num": 12744,
            "update_date": "Thu, 10 Oct 2024 04:07:23 GMT",
            "update_time": 1728533243536,
            "vector_similarity_weight": 0.3
        }
    ],
    "total": 1
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "The dataset doesn't exist"
}
```

 ---

### Получить граф знаний

**GET** `/api/v1/datasets/{dataset_id}/knowledge_graph`

Получение графа знаний указанного набора данных.

#### Запрос

- Метод: GET
- URL: `/api/v1/datasets/{dataset_id}/knowledge_graph`
- Заголовки:
  - `'Authorization: Bearer <YOUR_API_KEY>'`

##### Пример запроса

```bash
curl --request GET \
     --url http://{address}/api/v1/datasets/{dataset_id}/knowledge_graph \
     --header 'Authorization: Bearer <YOUR_API_KEY>'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID целевого набора данных.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": {
        "graph": {
            "directed": false,
            "edges": [
                {
                    "description": "Уведомление — это документ, выпускаемый для передачи предупреждений о рисках и операционных оповещений.<SEP>Уведомление является конкретным примером документа уведомления, выпускаемого в рамках системы предупреждения о рисках.",
                    "keywords": ["9", "8"],
                    "source": "notice",
                    "source_id": ["8a46cdfe4b5c11f0a5281a58e595aa1c"],
                    "src_id": "xxx",
                    "target": "xxx",
                    "tgt_id": "xxx",
                    "weight": 17.0
                }
            ],
            "graph": {
                "source_id": ["8a46cdfe4b5c11f0a5281a58e595aa1c", "8a7eb6424b5c11f0a5281a58e595aa1c"]
            },
            "multigraph": false,
            "nodes": [
                {
                    "description": "xxx",
                    "entity_name": "xxx",
                    "entity_type": "ORGANIZATION",
                    "id": "xxx",
                    "pagerank": 0.10804906590624092,
                    "rank": 3,
                    "source_id": ["8a7eb6424b5c11f0a5281a58e595aa1c"]
                }
            ]
        },
        "mind_map": {}
    }
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "The dataset doesn't exist"
}
```

---

### Удалить граф знаний

**DELETE** `/api/v1/datasets/{dataset_id}/knowledge_graph`

Удаляет граф знаний указанного набора данных.

#### Запрос

- Метод: DELETE
- URL: `/api/v1/datasets/{dataset_id}/knowledge_graph`
- Заголовки:
  - `'Authorization: Bearer <YOUR_API_KEY>'`

##### Пример запроса

```bash
curl --request DELETE \
     --url http://{address}/api/v1/datasets/{dataset_id}/knowledge_graph \
     --header 'Authorization: Bearer <YOUR_API_KEY>'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID целевого набора данных.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": true
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "The dataset doesn't exist"
}
```

---

## УПРАВЛЕНИЕ ФАЙЛАМИ ВНУТРИ НАБОРА ДАННЫХ

---

### Загрузить документы

**POST** `/api/v1/datasets/{dataset_id}/documents`

Загружает документы в указанный набор данных.

#### Запрос

- Метод: POST
- URL: `/api/v1/datasets/{dataset_id}/documents`
- Заголовки:
  - `'Content-Type: multipart/form-data'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Форма:
  - `'file=@{FILE_PATH}'`

##### Пример запроса

```bash
curl --request POST \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents \
     --header 'Content-Type: multipart/form-data' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --form 'file=@./test1.txt' \
     --form 'file=@./test2.pdf'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID набора данных, в который будут загружены документы.
- `'file'`: (*параметр тела*)  
  Загружаемый документ.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": [
        {
            "chunk_method": "naive",
            "created_by": "69736c5e723611efb51b0242ac120007",
            "dataset_id": "527fa74891e811ef9c650242ac120006",
            "id": "b330ec2e91ec11efbc510242ac120004",
            "location": "1.txt",
            "name": "1.txt",
            "parser_config": {
                "chunk_token_num": 128,
                "delimiter": "\\n",
                "html4excel": false,
                "layout_recognize": true,
                "raptor": {
                    "use_raptor": false
                }
            },
            "run": "UNSTART",
            "size": 17966,
            "thumbnail": "",
            "type": "doc"
        }
    ]
}
```

Ошибка:

```json
{
    "code": 101,
    "message": "No file part!"
}
```

---

### Обновить документ

**PUT** `/api/v1/datasets/{dataset_id}/documents/{document_id}`

Обновляет конфигурации указанного документа.

#### Запрос

- Метод: PUT
- URL: `/api/v1/datasets/{dataset_id}/documents/{document_id}`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"name"`:`string`
  - `"meta_fields"`:`object`
  - `"chunk_method"`:`string`
  - `"parser_config"`:`object`

##### Пример запроса

```bash
curl --request PUT \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id} \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --header 'Content-Type: application/json' \
     --data '
     {
          "name": "manual.txt", 
          "chunk_method": "manual", 
          "parser_config": {"chunk_token_num": 128}
     }'

```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `document_id`: (*параметр пути*)  
  ID документа для обновления.
- `"name"`: (*параметр тела*), `string`
- `"meta_fields"`: (*параметр тела*), `dict[str, Any]` Метаданные документа.
- `"chunk_method"`: (*параметр тела*), `string`  
  Метод парсинга документа:  
  - `"naive"`: Общий
  - `"manual"`: Ручной
  - `"qa"`: Вопрос-Ответ
  - `"table"`: Таблица
  - `"paper"`: Статья
  - `"book"`: Книга
  - `"laws"`: Законы
  - `"presentation"`: Презентация
  - `"picture"`: Изображение
  - `"one"`: Один
  - `"email"`: Электронная почта
- `"parser_config"`: (*параметр тела*), `object`  
  Конфигурация парсера. Атрибуты зависят от `"chunk_method"`:  
  - Если `"chunk_method"` равен `"naive"`, объект содержит:
    - `"chunk_token_num"`: По умолчанию `256`.
    - `"layout_recognize"`: По умолчанию `true`.
    - `"html4excel"`: Конвертировать Excel в HTML. По умолчанию `false`.
    - `"delimiter"`: По умолчанию `"\n"`.
    - `"task_page_size"`: По умолчанию `12`. Только для PDF.
    - `"raptor"`: Настройки RAPTOR. По умолчанию: `{"use_raptor": false}`.
  - Если `"chunk_method"` равен `"qa"`, `"manuel"`, `"paper"`, `"book"`, `"laws"` или `"presentation"`, содержит:
    - `"raptor"`: Настройки RAPTOR. По умолчанию: `{"use_raptor": false}`.
  - Если `"chunk_method"` равен `"table"`, `"picture"`, `"one"` или `"email"`, `"parser_config"` — пустой JSON.
- `"enabled"`: (*параметр тела*), `integer`  
  Доступность документа в базе знаний.  
  - `1` → доступен  
  - `0` → недоступен  

#### Ответ

Успех:

```json
{
    "code": 0
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "The dataset does not have the document."
}
```

---

### Скачать документ

**GET** `/api/v1/datasets/{dataset_id}/documents/{document_id}`

Скачивает документ из указанного набора данных.

#### Запрос

- Метод: GET
- URL: `/api/v1/datasets/{dataset_id}/documents/{document_id}`
- Заголовки:
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Вывод:
  - `'{PATH_TO_THE_FILE}'`

##### Пример запроса

```bash
curl --request GET \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id} \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --output ./ragflow.txt
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `documents_id`: (*параметр пути*)  
  ID документа для скачивания.

#### Ответ

Успех:

```json
This is a test to verify the file download feature.
```

Ошибка:

```json
{
    "code": 102,
    "message": "You do not own the dataset 7898da028a0511efbf750242ac1220005."
}
```

---

### Список документов

**GET** `/api/v1/datasets/{dataset_id}/documents?page={page}&page_size={page_size}&orderby={orderby}&desc={desc}&keywords={keywords}&id={document_id}&name={document_name}&create_time_from={timestamp}&create_time_to={timestamp}&suffix={file_suffix}&run={run_status}`

Получение списка документов в указанном наборе данных.

#### Запрос

- Метод: GET
- URL: `/api/v1/datasets/{dataset_id}/documents?page={page}&page_size={page_size}&orderby={orderby}&desc={desc}&keywords={keywords}&id={document_id}&name={document_name}&create_time_from={timestamp}&create_time_to={timestamp}&suffix={file_suffix}&run={run_status}`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`

##### Примеры запроса

**Базовый запрос с пагинацией:**
```bash
curl --request GET \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents?page=1&page_size=10 \
     --header 'Authorization: Bearer <YOUR_API_KEY>'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `keywords`: (*параметр фильтра*), `string`  
  Ключевые слова для поиска по названиям документов.
- `page`: (*параметр фильтра*), `integer`
  Номер страницы для отображения документов. По умолчанию `1`.
- `page_size`: (*параметр фильтра*), `integer`  
  Максимальное количество документов на странице. По умолчанию `30`.
- `orderby`: (*параметр фильтра*), `string`  
  Поле для сортировки документов. Доступные варианты:
  - `create_time` (по умолчанию)
  - `update_time`
- `desc`: (*параметр фильтра*), `boolean`  
  Сортировать ли в порядке убывания. По умолчанию `true`.
- `id`: (*параметр фильтра*), `string`  
  ID документа для поиска.
- `create_time_from`: (*параметр фильтра*), `integer`  
  Unix-временная метка для фильтрации документов, созданных после этого времени. 0 — без фильтра. По умолчанию `0`.
- `create_time_to`: (*параметр фильтра*), `integer`  
  Unix-временная метка для фильтрации документов, созданных до этого времени. 0 — без фильтра. По умолчанию `0`.
- `suffix`: (*параметр фильтра*), `array[string]`  
  Фильтр по расширению файлов. Поддерживает несколько значений, например, `pdf`, `txt`, `docx`. По умолчанию все расширения.
- `run`: (*параметр фильтра*), `array[string]`  
  Фильтр по статусу обработки документа. Поддерживает числовой, текстовый и смешанный форматы:  
  - Числовой формат: `["0", "1", "2", "3", "4"]`
  - Текстовый формат: `[UNSTART, RUNNING, CANCEL, DONE, FAIL]`
  - Смешанный формат: `[UNSTART, 1, DONE]` (смешение числового и текстового)
  - Соответствие статусов:
    - `0` / `UNSTART`: Документ не обработан
    - `1` / `RUNNING`: Документ обрабатывается
    - `2` / `CANCEL`: Обработка отменена
    - `3` / `DONE`: Обработка завершена успешно
    - `4` / `FAIL`: Обработка завершилась с ошибкой  
  По умолчанию все статусы.

##### Примеры использования

**Запрос с несколькими фильтрами**

```bash
curl --request GET \
     --url 'http://{address}/api/v1/datasets/{dataset_id}/documents?suffix=pdf&run=DONE&page=1&page_size=10' \
     --header 'Authorization: Bearer <YOUR_API_KEY>'
```

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": {
        "docs": [
            {
                "chunk_count": 0,
                "create_date": "Mon, 14 Oct 2024 09:11:01 GMT",
                "create_time": 1728897061948,
                "created_by": "69736c5e723611efb51b0242ac120007",
                "id": "3bcfbf8a8a0c11ef8aba0242ac120006",
                "knowledgebase_id": "7898da028a0511efbf750242ac120005",
                "location": "Test_2.txt",
                "name": "Test_2.txt",
                "parser_config": {
                    "chunk_token_count": 128,
                    "delimiter": "\n",
                    "layout_recognize": true,
                    "task_page_size": 12
                },
                "chunk_method": "naive",
                "process_begin_at": null,
                "process_duration": 0.0,
                "progress": 0.0,
                "progress_msg": "",
                "run": "UNSTART",
                "size": 7,
                "source_type": "local",
                "status": "1",
                "thumbnail": null,
                "token_count": 0,
                "type": "doc",
                "update_date": "Mon, 14 Oct 2024 09:11:01 GMT",
                "update_time": 1728897061948
            }
        ],
        "total_datasets": 1
    }
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "You don't own the dataset 7898da028a0511efbf750242ac1220005. "
}
```

---

### Удалить документы

**DELETE** `/api/v1/datasets/{dataset_id}/documents`

Удаляет документы по ID.

#### Запрос

- Метод: DELETE
- URL: `/api/v1/datasets/{dataset_id}/documents`
- Заголовки:
  - `'Content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"ids"`: `список[string]`

##### Пример запроса

```bash
curl --request DELETE \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {
          "ids": ["id_1","id_2"]
     }'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `"ids"`: (*параметр тела*), `список[string]`  
  ID документов для удаления. Если не указано, будут удалены все документы в наборе данных.

#### Ответ

Успех:

```json
{
    "code": 0
}.
```

Ошибка:

```json
{
    "code": 102,
    "message": "You do not own the dataset 7898da028a0511efbf750242ac1220005."
}
```

---

### Парсинг документов

**POST** `/api/v1/datasets/{dataset_id}/chunks`

Парсит документы в указанном наборе данных.

#### Запрос

- Метод: POST
- URL: `/api/v1/datasets/{dataset_id}/chunks`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"document_ids"`: `список[string]`

##### Пример запроса

```bash
curl --request POST \
     --url http://{address}/api/v1/datasets/{dataset_id}/chunks \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {
          "document_ids": ["97a5f1c2759811efaa500242ac120004","97ad64b6759811ef9fc30242ac120004"]
     }'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID набора данных.
- `"document_ids"`: (*параметр тела*), `список[string]`, *Обязательно*  
  ID документов для парсинга.

#### Ответ

Успех:

```json
{
    "code": 0
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "`document_ids` is required"
}
```

---

### Остановить парсинг документов

**DELETE** `/api/v1/datasets/{dataset_id}/chunks`

Останавливает парсинг указанных документов.

#### Запрос

- Метод: DELETE
- URL: `/api/v1/datasets/{dataset_id}/chunks`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"document_ids"`: `список[string]`

##### Пример запроса

```bash
curl --request DELETE \
     --url http://{address}/api/v1/datasets/{dataset_id}/chunks \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {
          "document_ids": ["97a5f1c2759811efaa500242ac120004","97ad64b6759811ef9fc30242ac120004"]
     }'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `"document_ids"`: (*параметр тела*), `список[string]`, *Обязательно*  
  ID документов, для которых нужно остановить парсинг.

#### Ответ

Успех:

```json
{
    "code": 0
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "`document_ids` is required"
}
```

---

## УПРАВЛЕНИЕ ЧАНКАМИ ВНУТРИ НАБОРА ДАННЫХ

---

### Добавить чанк

**POST** `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks`

Добавляет чанк в указанный документ указанного набора данных.

#### Запрос

- Метод: POST
- URL: `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"content"`: `string`
  - `"important_keywords"`: `список[string]`

##### Пример запроса

```bash
curl --request POST \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {
          "content": "<CHUNK_CONTENT_HERE>"
     }'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `document_ids`: (*параметр пути*)  
  ID связанного документа.
- `"content"`: (*параметр тела*), `string`, *Обязательно*  
  Текстовое содержимое чанка.
- `"important_keywords"` (*параметр тела*), `список[string]`  
  Ключевые слова или фразы для пометки чанка.
- `"questions"` (*параметр тела*), `список[string]`  
  Если заданы вопросы, встраиваемые чанки будут основаны на них.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": {
        "chunk": {
            "content": "who are you",
            "create_time": "2024-12-30 16:59:55",
            "create_timestamp": 1735549195.969164,
            "dataset_id": "72f36e1ebdf411efb7250242ac120006",
            "document_id": "61d68474be0111ef98dd0242ac120006",
            "id": "12ccdc56e59837e5",
            "important_keywords": [],
            "questions": []
        }
    }
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "`content` is required"
}
```

---

### Список чанков

**GET** `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks?keywords={keywords}&page={page}&page_size={page_size}&id={id}`

Получение списка чанков указанного документа.

#### Запрос

- Метод: GET
- URL: `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks?keywords={keywords}&page={page}&page_size={page_size}&id={chunk_id}`
- Заголовки:
  - `'Authorization: Bearer <YOUR_API_KEY>'`

##### Пример запроса

```bash
curl --request GET \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks?keywords={keywords}&page={page}&page_size={page_size}&id={chunk_id} \
     --header 'Authorization: Bearer <YOUR_API_KEY>' 
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `document_id`: (*параметр пути*)  
  ID связанного документа.
- `keywords` (*параметр фильтра*), `string`  
  Ключевые слова для поиска по содержимому чанков.
- `page` (*параметр фильтра*), `integer`  
  Номер страницы для отображения чанков. По умолчанию `1`.
- `page_size` (*параметр фильтра*), `integer`  
  Максимальное количество чанков на странице. По умолчанию `1024`.
- `id` (*параметр фильтра*), `string`  
  ID чанка для поиска.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": {
        "chunks": [
            {
                "available": true,
                "content": "This is a test content.",
                "docnm_kwd": "1.txt",
                "document_id": "b330ec2e91ec11efbc510242ac120004",
                "id": "b48c170e90f70af998485c1065490726",
                "image_id": "",
                "important_keywords": "",
                "positions": [
                    ""
                ]
            }
        ],
        "doc": {
            "chunk_count": 1,
            "chunk_method": "naive",
            "create_date": "Thu, 24 Oct 2024 09:45:27 GMT",
            "create_time": 1729763127646,
            "created_by": "69736c5e723611efb51b0242ac120007",
            "dataset_id": "527fa74891e811ef9c650242ac120006",
            "id": "b330ec2e91ec11efbc510242ac120004",
            "location": "1.txt",
            "name": "1.txt",
            "parser_config": {
                "chunk_token_num": 128,
                "delimiter": "\\n",
                "html4excel": false,
                "layout_recognize": true,
                "raptor": {
                    "use_raptor": false
                }
            },
            "process_begin_at": "Thu, 24 Oct 2024 09:56:44 GMT",
            "process_duration": 0.54213,
            "progress": 0.0,
            "progress_msg": "Task dispatched...",
            "run": "2",
            "size": 17966,
            "source_type": "local",
            "status": "1",
            "thumbnail": "",
            "token_count": 8,
            "type": "doc",
            "update_date": "Thu, 24 Oct 2024 11:03:15 GMT",
            "update_time": 1729767795721
        },
        "total": 1
    }
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "You don't own the document 5c5999ec7be811ef9cab0242ac12000e5."
}
```

---

### Удалить чанки

**DELETE** `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks`

Удаляет чанки по ID.

#### Запрос

- Метод: DELETE
- URL: `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"chunk_ids"`: `список[string]`

##### Пример запроса

```bash
curl --request DELETE \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {
          "chunk_ids": ["test_1", "test_2"]
     }'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `document_ids`: (*параметр пути*)  
  ID связанного документа.
- `"chunk_ids"`: (*параметр тела*), `список[string]`  
  ID чанков для удаления. Если не указано, будут удалены все чанки указанного документа.

#### Ответ

Успех:

```json
{
    "code": 0
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "`chunk_ids` is required"
}
```

---

### Обновить чанк

**PUT** `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}`

Обновляет содержимое или конфигурации указанного чанка.

#### Запрос

- Метод: PUT
- URL: `/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"content"`: `string`
  - `"important_keywords"`: `список[string]`
  - `"available"`: `boolean`

##### Пример запроса

```bash
curl --request PUT \
     --url http://{address}/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id} \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {   
          "content": "ragflow123",  
          "important_keywords": []  
     }'
```

##### Параметры запроса

- `dataset_id`: (*параметр пути*)  
  ID связанного набора данных.
- `document_ids`: (*параметр пути*)  
  ID связанного документа.
- `chunk_id`: (*параметр пути*)  
  ID чанка для обновления.
- `"content"`: (*параметр тела*), `string`  
  Текстовое содержимое чанка.
- `"important_keywords"`: (*параметр тела*), `список[string]`  
  Список ключевых слов или фраз для пометки чанка.
- `"available"`: (*параметр тела*) `boolean`  
  Статус доступности чанка в наборе данных. Возможные значения:  
  - `true`: Доступен (по умолчанию)
  - `false`: Недоступен

#### Ответ

Успех:

```json
{
    "code": 0
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "Can't find this chunk 29a2d9987e16ba331fb4d7d30d99b71d2"
}
```

---

### Получить чанки

**POST** `/api/v1/retrieval`

Получение чанков из указанных наборов данных.

#### Запрос

- Метод: POST
- URL: `/api/v1/retrieval`
- Заголовки:
  - `'content-Type: application/json'`
  - `'Authorization: Bearer <YOUR_API_KEY>'`
- Тело:
  - `"question"`: `string`  
  - `"dataset_ids"`: `список[string]`  
  - `"document_ids"`: `список[string]`
  - `"page"`: `integer`  
  - `"page_size"`: `integer`  
  - `"similarity_threshold"`: `float`  
  - `"vector_similarity_weight"`: `float`  
  - `"top_k"`: `integer`  
  - `"rerank_id"`: `string`  
  - `"keyword"`: `boolean`  
  - `"highlight"`: `boolean`
  - `"cross_languages"`: `список[string]`
  - `"metadata_condition"`: `object`

##### Пример запроса

```bash
curl --request POST \
     --url http://{address}/api/v1/retrieval \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data '
     {
          "question": "What is advantage of ragflow?",
          "dataset_ids": ["b2a62730759d11ef987d0242ac120004"],
          "document_ids": ["77df9ef4759a11ef8bdd0242ac120004"],
          "metadata_condition": {
            "conditions": [
              {
                "name": "author",
                "comparison_operator": "=",
                "value": "Toby"
              },
              {
                "name": "url",
                "comparison_operator": "not contains",
                "value": "amd"
              }
            ]
          }
     }'
```

##### Параметры запроса

- `"question"`: (*параметр тела*), `string`, *Обязательно*  
  Запрос пользователя или ключевые слова.
- `"dataset_ids"`: (*параметр тела*) `список[string]`  
  ID наборов данных для поиска. Если не указано, необходимо указать `"document_ids"`.
- `"document_ids"`: (*параметр тела*), `список[string]`  
  ID документов для поиска. Все выбранные документы должны использовать одну и ту же модель эмбеддинга, иначе возникнет ошибка. Если не указано, необходимо указать `"dataset_ids"`.
- `"page"`: (*параметр тела*), `integer`  
  Номер страницы для отображения чанков. По умолчанию `1`.
- `"page_size"`: (*параметр тела*)  
  Максимальное количество чанков на странице. По умолчанию `30`.
- `"similarity_threshold"`: (*параметр тела*)  
  Минимальный порог схожести. По умолчанию `0.2`.
- `"vector_similarity_weight"`: (*параметр тела*), `float`  
  Вес косинусной векторной схожести. По умолчанию `0.3`. Если x — вес косинусной схожести, то (1 - x) — вес терминологической схожести.
- `"top_k"`: (*параметр тела*), `integer`  
  Количество чанков, участвующих в вычислении косинусной схожести. По умолчанию `1024`.
- `"rerank_id"`: (*параметр тела*), `integer`  
  ID модели повторного ранжирования.
- `"keyword"`: (*параметр тела*), `boolean`  
  Включить поиск по ключевым словам:  
  - `true`: Включено.
  - `false`: Выключено (по умолчанию).
- `"highlight"`: (*параметр тела*), `boolean`  
  Включить подсветку совпадающих терминов в результатах:  
  - `true`: Включено.
  - `false`: Выключено (по умолчанию).
- `"cross_languages"`: (*параметр тела*) `список[string]`  
  Языки для перевода, чтобы осуществлять поиск ключевых слов на разных языках.
- `"metadata_condition"`: (*параметр тела*), `object`  
  Условия фильтрации по метаданным:  
  - `"conditions"`: (*параметр тела*), `массив`  
    Список условий фильтрации по метаданным.  
    - `"name"`: `string` - Имя поля метаданных для фильтрации, например, `"author"`, `"company"`, `"url"`. Убедитесь в наличии этого параметра. Подробнее см. [Установка метаданных](../guides/dataset/set_metadata.md).
    - `comparison_operator`: `string` - Оператор сравнения. Может быть одним из: 
      - `"contains"`
      - `"not contains"`
      - `"start with"`
      - `"empty"`
      - `"not empty"`
      - `"="`
      - `"≠"`
      - `">"`
      - `"<"`
      - `"≥"`
      - `"≤"`
    - `"value"`: `string` - Значение для сравнения.

#### Ответ

Успех:

```json
{
    "code": 0,
    "data": {
        "chunks": [
            {
                "content": "ragflow content",
                "content_ltks": "ragflow content",
                "document_id": "5c5999ec7be811ef9cab0242ac120005",
                "document_keyword": "1.txt",
                "highlight": "<em>ragflow</em> content",
                "id": "d78435d142bd5cf6704da62c778795c5",
                "image_id": "",
                "important_keywords": [
                    ""
                ],
                "kb_id": "c7ee74067a2c11efb21c0242ac120006",
                "positions": [
                    ""
                ],
                "similarity": 0.9669436601210759,
                "term_similarity": 1.0,
                "vector_similarity": 0.8898122004035864
            }
        ],
        "doc_aggs": [
            {
                "count": 1,
                "doc_id": "5c5999ec7be811ef9cab0242ac120005",
                "doc_name": "1.txt"
            }
        ],
        "total": 1
    }
}
```

Ошибка:

```json
{
    "code": 102,
    "message": "`datasets` is required."
}
```

---

## УПРАВЛЕНИЕ ЧАТ-АССИСТЕНТАМИ

---

### Создать чат-ассистента

**POST** `/api