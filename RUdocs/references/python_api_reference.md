---
sidebar_position: 5
slug: /python_api_reference
---

# Python API

Полное руководство по Python API RAGFlow. Перед началом убедитесь, что [у вас есть ключ API RAGFlow для аутентификации](https://ragflow.io/docs/dev/acquire_ragflow_api_key).

:::tip NOTE
Выполните следующую команду для загрузки Python SDK:

```bash
pip install ragflow-sdk
```

:::

---

## КОДЫ ОШИБОК

---

| Код  | Сообщение            | Описание                    |
|-------|----------------------|-----------------------------|
| 400   | Bad Request          | Неверные параметры запроса  |
| 401   | Unauthorized         | Несанкционированный доступ  |
| 403   | Forbidden            | Доступ запрещён             |
| 404   | Not Found            | Ресурс не найден            |
| 500   | Internal Server Error| Внутренняя ошибка сервера   |
| 1001  | Invalid Chunk ID     | Неверный Chunk ID           |
| 1002  | Chunk Update Failed  | Ошибка обновления Chunk     |

---

## OpenAI-совместимый API

---

### Создать чат-комплит

Создаёт ответ модели для заданной истории чата через OpenAI API.

#### Параметры

##### model: `str`, *Обязательно*

Модель, используемая для генерации ответа. Сервер будет обрабатывать это автоматически, поэтому пока можно указать любое значение.

##### messages: `list[object]`, *Обязательно*

Список исторических сообщений чата, используемых для генерации ответа. Должно содержать хотя бы одно сообщение с ролью `user`.

##### stream: `boolean`

Получать ответ в виде потока. Явно установите в `false`, если хотите получить весь ответ целиком, а не поток.

#### Возвращает

- Успех: Ответ [message](https://platform.openai.com/docs/api-reference/chat/create), аналогичный OpenAI
- Ошибка: `Exception`

#### Примеры

```python
from openai import OpenAI

model = "model"
client = OpenAI(api_key="ragflow-api-key", base_url=f"http://ragflow_address/api/v1/chats_openai/<chat_id>")

stream = True
reference = True

completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who are you?"},
        {"role": "assistant", "content": "I am an AI assistant named..."},
        {"role": "user", "content": "Can you tell me how to install neovim"},
    ],
    stream=stream,
    extra_body={"reference": reference}
)

if stream:
    for chunk in completion:
        print(chunk)
        if reference and chunk.choices[0].finish_reason == "stop":
            print(f"Reference:\n{chunk.choices[0].delta.reference}")
            print(f"Final content:\n{chunk.choices[0].delta.final_content}")
else:
    print(completion.choices[0].message.content)
    if reference:
        print(completion.choices[0].message.reference)
```

## УПРАВЛЕНИЕ НАБОРАМИ ДАННЫХ

---

### Создать набор данных

```python
RAGFlow.create_dataset(
    name: str,
    avatar: Optional[str] = None,
    description: Optional[str] = None,
    embedding_model: Optional[str] = "BAAI/bge-large-zh-v1.5@BAAI",
    permission: str = "me", 
    chunk_method: str = "naive",
    parser_config: DataSet.ParserConfig = None
) -> DataSet
```

Создаёт набор данных.

#### Параметры

##### name: `str`, *Обязательно*

Уникальное имя создаваемого набора данных. Должно соответствовать следующим требованиям:

- Максимум 128 символов.
- Регистр не учитывается.

##### avatar: `str`

Base64-кодирование аватара. По умолчанию `None`.

##### description: `str`

Краткое описание создаваемого набора данных. По умолчанию `None`.

##### permission

Определяет, кто может получить доступ к создаваемому набору данных. Доступные варианты:

- `"me"`: (По умолчанию) Управлять набором данных можете только вы.
- `"team"`: Все члены команды могут управлять набором данных.

##### chunk_method, `str`

Метод разбиения набора данных на чанки. Доступные варианты:

- `"naive"`: Общий (по умолчанию)
- `"manual"`: Ручной
- `"qa"`: Вопрос-ответ
- `"table"`: Таблица
- `"paper"`: Статья
- `"book"`: Книга
- `"laws"`: Законы
- `"presentation"`: Презентация
- `"picture"`: Изображение
- `"one"`: Один
- `"email"`: Электронная почта

##### parser_config

Конфигурация парсера набора данных. Атрибуты объекта `ParserConfig` зависят от выбранного `chunk_method`:

- `chunk_method`=`"naive"`:  
  `{"chunk_token_num":512,"delimiter":"\\n","html4excel":False,"layout_recognize":True,"raptor":{"use_raptor":False}}`.
- `chunk_method`=`"qa"`:  
  `{"raptor": {"use_raptor": False}}`
- `chunk_method`=`"manuel"`:  
  `{"raptor": {"use_raptor": False}}`
- `chunk_method`=`"table"`:  
  `None`
- `chunk_method`=`"paper"`:  
  `{"raptor": {"use_raptor": False}}`
- `chunk_method`=`"book"`:  
  `{"raptor": {"use_raptor": False}}`
- `chunk_method`=`"laws"`:  
  `{"raptor": {"use_raptor": False}}`
- `chunk_method`=`"picture"`:  
  `None`
- `chunk_method`=`"presentation"`:  
  `{"raptor": {"use_raptor": False}}`
- `chunk_method`=`"one"`:  
  `None`
- `chunk_method`=`"knowledge-graph"`:  
  `{"chunk_token_num":128,"delimiter":"\\n","entity_types":["organization","person","location","event","time"]}`
- `chunk_method`=`"email"`:  
  `None`

#### Возвращает

- Успех: Объект `dataset`.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.create_dataset(name="kb_1")
```

---

### Удалить наборы данных

```python
RAGFlow.delete_datasets(ids: list[str] | None = None)
```

Удаляет наборы данных по ID.

#### Параметры

##### ids: `list[str]` или `None`, *Обязательно*

ID наборов данных для удаления. По умолчанию `None`.
  - Если `None`, будут удалены все наборы данных.
  - Если массив ID, будут удалены только указанные наборы.
  - Если пустой массив, наборы данных не будут удалены.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
rag_object.delete_datasets(ids=["d94a8dc02c9711f0930f7fbc369eab6d","e94a8dc02c9711f0930f7fbc369eab6e"])
```

---

### Список наборов данных

```python
RAGFlow.list_datasets(
    page: int = 1, 
    page_size: int = 30, 
    orderby: str = "create_time", 
    desc: bool = True,
    id: str = None,
    name: str = None
) -> list[DataSet]
```

Выводит список наборов данных.

#### Параметры

##### page: `int`

Страница, на которой будут отображаться наборы данных. По умолчанию `1`.

##### page_size: `int`

Количество наборов данных на странице. По умолчанию `30`.

##### orderby: `str`

Поле для сортировки наборов данных. Доступные варианты:

- `"create_time"` (по умолчанию)
- `"update_time"`

##### desc: `bool`

Сортировать ли наборы данных в порядке убывания. По умолчанию `True`.

##### id: `str`

ID набора данных для получения. По умолчанию `None`.

##### name: `str`

Имя набора данных для получения. По умолчанию `None`.

#### Возвращает

- Успех: Список объектов `DataSet`.
- Ошибка: `Exception`.

#### Примеры

##### Вывести все наборы данных

```python
for dataset in rag_object.list_datasets():
    print(dataset)
```

##### Получить набор данных по ID

```python
dataset = rag_object.list_datasets(id = "id_1")
print(dataset[0])
```

---

### Обновить набор данных

```python
DataSet.update(update_message: dict)
```

Обновляет конфигурации текущего набора данных.

#### Параметры

##### update_message: `dict[str, str|int]`, *Обязательно*

Словарь с атрибутами для обновления, содержащий следующие ключи:

- `"name"`: `str` Новое имя набора данных.
  - Только Basic Multilingual Plane (BMP)
  - Максимум 128 символов
  - Регистр не учитывается
- `"avatar"`: (*Параметр тела*), `string`  
  Обновлённое base64-кодирование аватара.
  - Максимум 65535 символов
- `"embedding_model"`: (*Параметр тела*), `string`  
  Обновлённое имя embedding модели.  
  - Убедитесь, что `"chunk_count"` равен `0` перед обновлением `"embedding_model"`.
  - Максимум 255 символов
  - Должно соответствовать формату `model_name@model_factory`
- `"permission"`: (*Параметр тела*), `string`  
  Обновлённые права доступа к набору данных. Доступные варианты:  
  - `"me"`: (По умолчанию) Управлять набором данных можете только вы.
  - `"team"`: Все члены команды могут управлять набором данных.
- `"pagerank"`: (*Параметр тела*), `int`  
  См. [Установить page rank](https://ragflow.io/docs/dev/set_page_rank)
  - По умолчанию: `0`
  - Минимум: `0`
  - Максимум: `100`
- `"chunk_method"`: (*Параметр тела*), `enum<string>`  
  Метод разбиения набора данных. Доступные варианты:  
  - `"naive"`: Общий (по умолчанию)
  - `"book"`: Книга
  - `"email"`: Электронная почта
  - `"laws"`: Законы
  - `"manual"`: Ручной
  - `"one"`: Один
  - `"paper"`: Статья
  - `"picture"`: Изображение
  - `"presentation"`: Презентация
  - `"qa"`: Вопрос-ответ
  - `"table"`: Таблица
  - `"tag"`: Тег

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets(name="kb_name")
dataset = dataset[0]
dataset.update({"embedding_model":"BAAI/bge-zh-v1.5", "chunk_method":"manual"})
```

---

## УПРАВЛЕНИЕ ФАЙЛАМИ В НАБОРЕ ДАННЫХ

---

### Загрузить документы

```python
DataSet.upload_documents(document_list: list[dict])
```

Загружает документы в текущий набор данных.

#### Параметры

##### document_list: `list[dict]`, *Обязательно*

Список словарей, представляющих загружаемые документы, каждый из которых содержит следующие ключи:

- `"display_name"`: (Опционально) Имя файла для отображения в наборе данных.  
- `"blob"`: (Опционально) Двоичное содержимое файла для загрузки.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
dataset = rag_object.create_dataset(name="kb_name")
dataset.upload_documents([{"display_name": "1.txt", "blob": "<BINARY_CONTENT_OF_THE_DOC>"}, {"display_name": "2.pdf", "blob": "<BINARY_CONTENT_OF_THE_DOC>"}])
```

---

### Обновить документ

```python
Document.update(update_message:dict)
```

Обновляет конфигурации текущего документа.

#### Параметры

##### update_message: `dict[str, str|dict[]]`, *Обязательно*

Словарь с атрибутами для обновления, содержащий следующие ключи:

- `"display_name"`: `str` Имя документа для обновления.
- `"meta_fields"`: `dict[str, Any]` Метаданные документа.
- `"chunk_method"`: `str` Метод парсинга документа.
  - `"naive"`: Общий
  - `"manual"`: Ручной
  - `"qa"`: Вопрос-ответ
  - `"table"`: Таблица
  - `"paper"`: Статья
  - `"book"`: Книга
  - `"laws"`: Законы
  - `"presentation"`: Презентация
  - `"picture"`: Изображение
  - `"one"`: Один
  - `"email"`: Электронная почта
- `"parser_config"`: `dict[str, Any]` Конфигурация парсера документа. Атрибуты зависят от выбранного `"chunk_method"`:
  - `"chunk_method"`=`"naive"`:  
    `{"chunk_token_num":128,"delimiter":"\\n","html4excel":False,"layout_recognize":True,"raptor":{"use_raptor":False}}`.
  - `chunk_method`=`"qa"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"manuel"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"table"`:  
    `None`
  - `chunk_method`=`"paper"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"book"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"laws"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"presentation"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"picture"`:  
    `None`
  - `chunk_method`=`"one"`:  
    `None`
  - `chunk_method`=`"knowledge-graph"`:  
    `{"chunk_token_num":128,"delimiter":"\\n","entity_types":["organization","person","location","event","time"]}`
  - `chunk_method`=`"email"`:  
    `None`

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets(id='id')
dataset = dataset[0]
doc = dataset.list_documents(id="wdfxb5t547d")
doc = doc[0]
doc.update([{"parser_config": {"chunk_token_num": 256}}, {"chunk_method": "manual"}])
```

---

### Скачать документ

```python
Document.download() -> bytes
```

Скачивает текущий документ.

#### Возвращает

Скачанный документ в виде байтов.

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets(id="id")
dataset = dataset[0]
doc = dataset.list_documents(id="wdfxb5t547d")
doc = doc[0]
open("~/ragflow.txt", "wb+").write(doc.download())
print(doc)
```

---

### Список документов

```python
Dataset.list_documents(
    id: str = None,
    keywords: str = None,
    page: int = 1,
    page_size: int = 30,
    order_by: str = "create_time",
    desc: bool = True,
    create_time_from: int = 0,
    create_time_to: int = 0
) -> list[Document]
```

Выводит список документов в текущем наборе данных.

#### Параметры

##### id: `str`

ID документа для получения. По умолчанию `None`.

##### keywords: `str`

Ключевые слова для поиска по названиям документов. По умолчанию `None`.

##### page: `int`

Страница, на которой будут отображаться документы. По умолчанию `1`.

##### page_size: `int`

Максимальное количество документов на странице. По умолчанию `30`.

##### orderby: `str`

Поле для сортировки документов. Доступные варианты:

- `"create_time"` (по умолчанию)
- `"update_time"`

##### desc: `bool`

Сортировать ли документы в порядке убывания. По умолчанию `True`.

##### create_time_from: `int`
Unix-временная метка для фильтрации документов, созданных после этого времени. 0 — без фильтра. По умолчанию 0.

##### create_time_to: `int`
Unix-временная метка для фильтрации документов, созданных до этого времени. 0 — без фильтра. По умолчанию 0.

#### Возвращает

- Успех: Список объектов `Document`.
- Ошибка: `Exception`.

Объект `Document` содержит следующие атрибуты:

- `id`: ID документа. По умолчанию `""`.
- `name`: Имя документа. По умолчанию `""`.
- `thumbnail`: Миниатюра документа. По умолчанию `None`.
- `dataset_id`: ID набора данных, связанного с документом. По умолчанию `None`.
- `chunk_method`: Метод разбиения на чанки. По умолчанию `"naive"`.
- `source_type`: Тип источника документа. По умолчанию `"local"`.
- `type`: Тип или категория документа. По умолчанию `""`. Зарезервировано для будущего использования.
- `created_by`: `str` Автор документа. По умолчанию `""`.
- `size`: `int` Размер документа в байтах. По умолчанию `0`.
- `token_count`: `int` Количество токенов в документе. По умолчанию `0`.
- `chunk_count`: `int` Количество чанков в документе. По умолчанию `0`.
- `progress`: `float` Текущий прогресс обработки в процентах. По умолчанию `0.0`.
- `progress_msg`: `str` Сообщение о текущем статусе прогресса. По умолчанию `""`.
- `process_begin_at`: `datetime` Время начала обработки документа. По умолчанию `None`.
- `process_duration`: `float` Продолжительность обработки в секундах. По умолчанию `0.0`.
- `run`: `str` Статус обработки документа:
  - `"UNSTART"`  (по умолчанию)
  - `"RUNNING"`
  - `"CANCEL"`
  - `"DONE"`
  - `"FAIL"`
- `status`: `str` Зарезервировано для будущего использования.
- `parser_config`: `ParserConfig` Конфигурация парсера. Атрибуты зависят от выбранного `chunk_method`:
  - `chunk_method`=`"naive"`:  
    `{"chunk_token_num":128,"delimiter":"\\n","html4excel":False,"layout_recognize":True,"raptor":{"use_raptor":False}}`.
  - `chunk_method`=`"qa"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"manuel"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"table"`:  
    `None`
  - `chunk_method`=`"paper"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"book"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"laws"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"presentation"`:  
    `{"raptor": {"use_raptor": False}}`
  - `chunk_method`=`"picure"`:  
    `None`
  - `chunk_method`=`"one"`:  
    `None`
  - `chunk_method`=`"email"`:  
    `None`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.create_dataset(name="kb_1")

filename1 = "~/ragflow.txt"
blob = open(filename1 , "rb").read()
dataset.upload_documents([{"name":filename1,"blob":blob}])
for doc in dataset.list_documents(keywords="rag", page=0, page_size=12):
    print(doc)
```

---

### Удалить документы

```python
DataSet.delete_documents(ids: list[str] = None)
```

Удаляет документы по ID.

#### Параметры

##### ids: `list[list]`

ID документов для удаления. По умолчанию `None`. Если не указано, будут удалены все документы в наборе данных.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets(name="kb_1")
dataset = dataset[0]
dataset.delete_documents(ids=["id_1","id_2"])
```

---

### Парсинг документов

```python
DataSet.async_parse_documents(document_ids:list[str]) -> None
```

Парсит документы в текущем наборе данных.

#### Параметры

##### document_ids: `list[str]`, *Обязательно*

ID документов для парсинга.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.create_dataset(name="dataset_name")
documents = [
    {'display_name': 'test1.txt', 'blob': open('./test_data/test1.txt',"rb").read()},
    {'display_name': 'test2.txt', 'blob': open('./test_data/test2.txt',"rb").read()},
    {'display_name': 'test3.txt', 'blob': open('./test_data/test3.txt',"rb").read()}
]
dataset.upload_documents(documents)
documents = dataset.list_documents(keywords="test")
ids = []
for document in documents:
    ids.append(document.id)
dataset.async_parse_documents(ids)
print("Запущен асинхронный пакетный парсинг.")
```

---

### Парсинг документов (с состоянием документа)

```python
DataSet.parse_documents(document_ids: list[str]) -> list[tuple[str, str, int, int]]
```

*Асинхронно* парсит документы в текущем наборе данных.

Этот метод инкапсулирует `async_parse_documents()`. Он ожидает завершения всех задач парсинга и возвращает подробные результаты, включая статус парсинга и статистику для каждого документа. Если происходит прерывание с клавиатуры (например, `Ctrl+C`), все ожидающие задачи парсинга будут корректно отменены.

#### Параметры

##### document_ids: `list[str]`, *Обязательно*

ID документов для парсинга.

#### Возвращает

Список кортежей с подробными результатами парсинга:

```python
[
  (document_id: str, status: str, chunk_count: int, token_count: int),
  ...
]
```
- `status`: Финальное состояние парсинга (например, `success`, `failed`, `cancelled`).  
- `chunk_count`: Количество созданных чанков из документа.  
- `token_count`: Общее количество обработанных токенов.  

---

#### Пример

```python
rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.create_dataset(name="dataset_name")
documents = dataset.list_documents(keywords="test")
ids = [doc.id for doc in documents]

try:
    finished = dataset.parse_documents(ids)
    for doc_id, status, chunk_count, token_count in finished:
        print(f"Парсинг документа {doc_id} завершён со статусом: {status}, чанков: {chunk_count}, токенов: {token_count}")
except KeyboardInterrupt:
    print("\nПарсинг прерван пользователем. Все ожидающие задачи отменены.")
except Exception as e:
    print(f"Ошибка парсинга: {e}")
```

---

### Остановить парсинг документов

```python
DataSet.async_cancel_parse_documents(document_ids:list[str])-> None
```

Останавливает парсинг указанных документов.

#### Параметры

##### document_ids: `list[str]`, *Обязательно*

ID документов, для которых нужно остановить парсинг.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.create_dataset(name="dataset_name")
documents = [
    {'display_name': 'test1.txt', 'blob': open('./test_data/test1.txt',"rb").read()},
    {'display_name': 'test2.txt', 'blob': open('./test_data/test2.txt',"rb").read()},
    {'display_name': 'test3.txt', 'blob': open('./test_data/test3.txt',"rb").read()}
]
dataset.upload_documents(documents)
documents = dataset.list_documents(keywords="test")
ids = []
for document in documents:
    ids.append(document.id)
dataset.async_parse_documents(ids)
print("Запущен асинхронный пакетный парсинг.")
dataset.async_cancel_parse_documents(ids)
print("Асинхронный пакетный парсинг отменён.")
```

---

## УПРАВЛЕНИЕ ЧАНКАМИ В НАБОРЕ ДАННЫХ

---

### Добавить чанк

```python
Document.add_chunk(content:str, important_keywords:list[str] = []) -> Chunk
```

Добавляет чанк в текущий документ.

#### Параметры

##### content: `str`, *Обязательно*

Текстовое содержимое чанка.

##### important_keywords: `list[str]`

Ключевые термины или фразы для тегирования чанка.

#### Возвращает

- Успех: Объект `Chunk`.
- Ошибка: `Exception`.

Объект `Chunk` содержит следующие атрибуты:

- `id`: `str`: ID чанка.
- `content`: `str` Текстовое содержимое чанка.
- `important_keywords`: `list[str]` Список ключевых терминов или фраз, связанных с чанком.
- `create_time`: `str` Время создания чанка (добавления в документ).
- `create_timestamp`: `float` Временная метка создания чанка в секундах с 1 января 1970 года.
- `dataset_id`: `str` ID связанного набора данных.
- `document_name`: `str` Имя связанного документа.
- `document_id`: `str` ID связанного документа.
- `available`: `bool` Статус доступности чанка в наборе данных. Варианты значений:
  - `False`: Недоступен
  - `True`: Доступен (по умолчанию)

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
datasets = rag_object.list_datasets(id="123")
dataset = datasets[0]
doc = dataset.list_documents(id="wdfxb5t547d")
doc = doc[0]
chunk = doc.add_chunk(content="xxxxxxx")
```

---

### Список чанков

```python
Document.list_chunks(keywords: str = None, page: int = 1, page_size: int = 30, id : str = None) -> list[Chunk]
```

Выводит список чанков в текущем документе.

#### Параметры

##### keywords: `str`

Ключевые слова для поиска по содержимому чанков. По умолчанию `None`

##### page: `int`

Страница, на которой будут отображаться чанки. По умолчанию `1`.

##### page_size: `int`

Максимальное количество чанков на странице. По умолчанию `30`.

##### id: `str`

ID чанка для получения. По умолчанию `None`.

#### Возвращает

- Успех: Список объектов `Chunk`.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets("123")
dataset = dataset[0]
docs = dataset.list_documents(keywords="test", page=1, page_size=12)
for chunk in docs[0].list_chunks(keywords="rag", page=0, page_size=12):
    print(chunk)
```

---

### Удалить чанки

```python
Document.delete_chunks(chunk_ids: list[str])
```

Удаляет чанки по ID.

#### Параметры

##### chunk_ids: `list[str]`

ID чанков для удаления. По умолчанию `None`. Если не указано, будут удалены все чанки текущего документа.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets(id="123")
dataset = dataset[0]
doc = dataset.list_documents(id="wdfxb5t547d")
doc = doc[0]
chunk = doc.add_chunk(content="xxxxxxx")
doc.delete_chunks(["id_1","id_2"])
```

---

### Обновить чанк

```python
Chunk.update(update_message: dict)
```

Обновляет содержимое или конфигурации текущего чанка.

#### Параметры

##### update_message: `dict[str, str|list[str]|int]` *Обязательно*

Словарь с атрибутами для обновления, содержащий следующие ключи:

- `"content"`: `str` Текстовое содержимое чанка.
- `"important_keywords"`: `list[str]` Список ключевых терминов или фраз для тегирования чанка.
- `"available"`: `bool` Статус доступности чанка в наборе данных. Варианты значений:
  - `False`: Недоступен
  - `True`: Доступен (по умолчанию)

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets(id="123")
dataset = dataset[0]
doc = dataset.list_documents(id="wdfxb5t547d")
doc = doc[0]
chunk = doc.add_chunk(content="xxxxxxx")
chunk.update({"content":"sdfx..."})
```

---

### Получить чанки

```python
RAGFlow.retrieve(question:str="", dataset_ids:list[str]=None, document_ids=list[str]=None, page:int=1, page_size:int=30, similarity_threshold:float=0.2, vector_similarity_weight:float=0.3, top_k:int=1024,rerank_id:str=None,keyword:bool=False,cross_languages:list[str]=None,metadata_condition: dict=None) -> list[Chunk]
```

Получает чанки из указанных наборов данных.

#### Параметры

##### question: `str`, *Обязательно*

Запрос пользователя или ключевые слова запроса. По умолчанию `""`.

##### dataset_ids: `list[str]`, *Обязательно*

ID наборов данных для поиска. По умолчанию `None`. 

##### document_ids: `list[str]`

ID документов для поиска. По умолчанию `None`. Убедитесь, что все выбранные документы используют одну и ту же embedding модель. Иначе возникнет ошибка. 

##### page: `int`

Начальный индекс для получения документов. По умолчанию `1`.

##### page_size: `int`

Максимальное количество чанков для получения. По умолчанию `30`.

##### Similarity_threshold: `float`

Минимальный порог сходства. По умолчанию `0.2`.

##### vector_similarity_weight: `float`

Вес косинусного сходства векторов. По умолчанию `0.3`. Если x — косинусное сходство векторов, то (1 - x) — вес сходства по терминам.

##### top_k: `int`

Количество чанков, участвующих в вычислении косинусного сходства векторов. По умолчанию `1024`.

##### rerank_id: `str`

ID модели для повторного ранжирования. По умолчанию `None`.

##### keyword: `bool`

Включить ли поиск по ключевым словам:

- `True`: Включить поиск по ключевым словам.
- `False`: Отключить поиск по ключевым словам (по умолчанию).

##### cross_languages:  `list[string]`  

Языки, на которые следует переводить для поиска по ключевым словам на разных языках.

##### metadata_condition: `dict`

Условие фильтрации по `meta_fields`.

#### Возвращает

- Успех: Список объектов `Chunk`, представляющих чанки документов.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
dataset = rag_object.list_datasets(name="ragflow")
dataset = dataset[0]
name = 'ragflow_test.txt'
path = './test_data/ragflow_test.txt'
documents =[{"display_name":"test_retrieve_chunks.txt","blob":open(path, "rb").read()}]
docs = dataset.upload_documents(documents)
doc = docs[0]
doc.add_chunk(content="This is a chunk addition test")
for c in rag_object.retrieve(dataset_ids=[dataset.id],document_ids=[doc.id]):
  print(c)
```

---

## УПРАВЛЕНИЕ ЧАТ-АССИСТЕНТАМИ

---

### Создать чат-ассистента

```python
RAGFlow.create_chat(
    name: str, 
    avatar: str = "", 
    dataset_ids: list[str] = [], 
    llm: Chat.LLM = None, 
    prompt: Chat.Prompt = None
) -> Chat
```

Создаёт чат-ассистента.

#### Параметры

##### name: `str`, *Обязательно*

Имя чат-ассистента.

##### avatar: `str`

Base64-кодирование аватара. По умолчанию `""`.

##### dataset_ids: `list[str]`

ID связанных наборов данных. По умолчанию `[""]`.

##### llm: `Chat.LLM`

Настройки LLM для создаваемого чат-ассистента. По умолчанию `None`. Если значение `None`, будет создан словарь со следующими значениями по умолчанию. Объект `LLM` содержит следующие атрибуты:

- `model_name`: `str`  
  Имя модели чата. Если `None`, будет использована модель по умолчанию пользователя.  
- `temperature`: `float`  
  Контролирует случайность предсказаний модели. Меньшее значение даёт более консервативные ответы, большее — более креативные и разнообразные. По умолчанию `0.1`.  
- `top_p`: `float`  
  Известен как «nucleus sampling», этот параметр задаёт порог для выбора меньшего набора слов для сэмплинга. Фокусируется на наиболее вероятных словах, отсекая менее вероятные. По умолчанию `0.3`.  
- `presence_penalty`: `float`  
  Снижает повторение модели, штрафуя слова, уже появившиеся в разговоре. По умолчанию `0.2`.
- `frequency penalty`: `float`  
  Аналогично presence penalty, уменьшает склонность модели часто повторять одни и те же слова. По умолчанию `0.7`.

##### prompt: `Chat.Prompt`

Инструкции для LLM. Объект `Prompt` содержит следующие атрибуты:

- `similarity_threshold`: `float` RAGFlow использует либо комбинацию взвешенного сходства по ключевым словам и косинусного сходства векторов, либо комбинацию взвешенного сходства по ключевым словам и оценки повторного ранжирования при поиске. Если оценка сходства ниже этого порога, соответствующий чанк исключается из результатов. Значение по умолчанию `0.2`.
- `keywords_similarity_weight`: `float` Вес сходства по ключевым словам в гибридной оценке сходства с косинусным сходством векторов или моделью повторного ранжирования. Позволяет регулировать влияние сходства по ключевым словам относительно других мер сходства. Значение по умолчанию `0.7`.
- `top_n`: `int` Количество лучших чанков с оценками сходства выше `similarity_threshold`, передаваемых LLM. LLM будет иметь доступ *только* к этим 'top N' чанкам. Значение по умолчанию `8`.
- `variables`: `list[dict[]]` Список переменных для использования в поле 'System' **Конфигураций чата**. Обратите внимание:
  - `knowledge` — зарезервированная переменная, представляющая полученные чанки.
  - Все переменные в 'System' должны быть в фигурных скобках.
  - Значение по умолчанию `[{"key": "knowledge", "optional": True}]`.
- `rerank_model`: `str` Если не указано, используется косинусное сходство векторов; иначе — оценка модели повторного ранжирования. По умолчанию `""`.
- `top_k`: `int` Процесс переупорядочивания или выбора топ-k элементов на основе определённого критерия ранжирования. По умолчанию `1024`.
- `empty_response`: `str` Если в наборе данных не найдено ничего по вопросу пользователя, используется этот ответ. Чтобы позволить LLM импровизировать при отсутствии данных, оставьте пустым. По умолчанию `None`.
- `opener`: `str` Приветствие пользователя. По умолчанию `"Hi! I am your assistant, can I help you?"`.
- `show_quote`: `bool` Показывать ли источник текста. По умолчанию `True`.
- `prompt`: `str` Содержимое промпта.

#### Возвращает

- Успех: Объект `Chat`, представляющий чат-ассистента.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
datasets = rag_object.list_datasets(name="kb_1")
dataset_ids = []
for dataset in datasets:
    dataset_ids.append(dataset.id)
assistant = rag_object.create_chat("Miss R", dataset_ids=dataset_ids)
```

---

### Обновить чат-ассистента

```python
Chat.update(update_message: dict)
```

Обновляет конфигурации текущего чат-ассистента.

#### Параметры

##### update_message: `dict[str, str|list[str]|dict[]]`, *Обязательно*

Словарь с атрибутами для обновления, содержащий следующие ключи:

- `"name"`: `str` Новое имя чат-ассистента.
- `"avatar"`: `str` Base64-кодирование аватара. По умолчанию `""`
- `"dataset_ids"`: `list[str]` Наборы данных для обновления.
- `"llm"`: `dict` Настройки LLM:
  - `"model_name"`, `str` Имя модели чата.
  - `"temperature"`, `float` Контролирует случайность предсказаний модели. Меньшее значение даёт более консервативные ответы, большее — более креативные и разнообразные.  
  - `"top_p"`, `float` Известен как «nucleus sampling», задаёт порог для выбора меньшего набора слов для сэмплинга.  
  - `"presence_penalty"`, `float` Снижает повторение модели, штрафуя слова, появившиеся в разговоре.
  - `"frequency penalty"`, `float` Аналогично presence penalty, уменьшает склонность модели повторять одни и те же слова.
- `"prompt"` : Инструкции для LLM.
  - `"similarity_threshold"`: `float` RAGFlow использует либо комбинацию взвешенного сходства по ключевым словам и косинусного сходства векторов, либо комбинацию взвешенного сходства по ключевым словам и оценки повторного ранжирования при поиске. Этот параметр задаёт порог для сходств между запросом пользователя и чанками. Если оценка ниже порога, чанк исключается из результатов. Значение по умолчанию `0.2`.
  - `"keywords_similarity_weight"`: `float` Вес сходства по ключевым словам в гибридной оценке сходства с косинусным сходством векторов или моделью повторного ранжирования. Позволяет регулировать влияние сходства по ключевым словам относительно других мер сходства. Значение по умолчанию `0.7`.
  - `"top_n"`: `int` Количество лучших чанков с оценками сходства выше `similarity_threshold`, передаваемых LLM. LLM будет иметь доступ *только* к этим 'top N' чанкам. Значение по умолчанию `8`.
  - `"variables"`: `list[dict[]]`  Список переменных для использования в поле 'System' **Конфигураций чата**. Обратите внимание:
    - `knowledge` — зарезервированная переменная, представляющая полученные чанки.
    - Все переменные в 'System' должны быть в фигурных скобках.
    - Значение по умолчанию `[{"key": "knowledge", "optional": True}]`.
  - `"rerank_model"`: `str` Если не указано, используется косинусное сходство векторов; иначе — оценка модели повторного ранжирования. По умолчанию `""`.
  - `"empty_response"`: `str` Если в наборе данных не найдено ничего по вопросу пользователя, используется этот ответ. Чтобы позволить LLM импровизировать при отсутствии данных, оставьте пустым. По умолчанию `None`.
  - `"opener"`: `str` Приветствие пользователя. По умолчанию `"Hi! I am your assistant, can I help you?"`.
  - `"show_quote`: `bool` Показывать ли источник текста. По умолчанию `True`.
  - `"prompt"`: `str` Содержимое промпта.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
datasets = rag_object.list_datasets(name="kb_1")
dataset_id = datasets[0].id
assistant = rag_object.create_chat("Miss R", dataset_ids=[dataset_id])
assistant.update({"name": "Stefan", "llm": {"temperature": 0.8}, "prompt": {"top_n": 8}})
```

---

### Удалить чат-ассистентов

```python
RAGFlow.delete_chats(ids: list[str] = None)
```

Удаляет чат-ассистентов по ID.

#### Параметры

##### ids: `list[str]`

ID чат-ассистентов для удаления. По умолчанию `None`. Если пустой или не указан, будут удалены все чат-ассистенты в системе.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
rag_object.delete_chats(ids=["id_1","id_2"])
```

---

### Список чат-ассистентов

```python
RAGFlow.list_chats(
    page: int = 1, 
    page_size: int = 30, 
    orderby: str = "create_time", 
    desc: bool = True,
    id: str = None,
    name: str = None
) -> list[Chat]
```

Выводит список чат-ассистентов.

#### Параметры

##### page: `int`

Страница, на которой будут отображаться чат-ассистенты. По умолчанию `1`.

##### page_size: `int`

Количество чат-ассистентов на странице. По умолчанию `30`.

##### orderby: `str`

Атрибут для сортировки результатов. Доступные варианты:

- `"create_time"` (по умолчанию)
- `"update_time"`

##### desc: `bool`

Сортировать ли чат-ассистентов в порядке убывания. По умолчанию `True`.

##### id: `str`  

ID чат-ассистента для получения. По умолчанию `None`.

##### name: `str`  

Имя чат-ассистента для получения. По умолчанию `None`.

#### Возвращает

- Успех: Список объектов `Chat`.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
for assistant in rag_object.list_chats():
    print(assistant)
```

---

## УПРАВЛЕНИЕ СЕАНСАМИ

---

### Создать сеанс с чат-ассистентом

```python
Chat.create_session(name: str = "New session") -> Session
```

Создаёт сеанс с текущим чат-ассистентом.

#### Параметры

##### name: `str`

Имя создаваемого сеанса чата.

#### Возвращает

- Успех: Объект `Session`, содержащий следующие атрибуты:
  - `id`: `str` Автоматически сгенерированный уникальный идентификатор созданного сеанса.
  - `name`: `str` Имя созданного сеанса.
  - `message`: `list[Message]` Открывающее сообщение созданного сеанса. По умолчанию `[{"role": "assistant", "content": "Hi! I am your assistant, can I help you?"}]`
  - `chat_id`: `str` ID связанного чат-ассистента.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
assistant = rag_object.list_chats(name="Miss R")
assistant = assistant[0]
session = assistant.create_session()
```

---

### Обновить сеанс чат-ассистента

```python
Session.update(update_message: dict)
```

Обновляет текущий сеанс текущего чат-ассистента.

#### Параметры

##### update_message: `dict[str, Any]`, *Обязательно*

Словарь с атрибутами для обновления, содержащий только один ключ:

- `"name"`: `str` Новое имя сеанса.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
assistant = rag_object.list_chats(name="Miss R")
assistant = assistant[0]
session = assistant.create_session("session_name")
session.update({"name": "updated_name"})
```

---

### Список сеансов чат-ассистента

```python
Chat.list_sessions(
    page: int = 1, 
    page_size: int = 30, 
    orderby: str = "create_time", 
    desc: bool = True,
    id: str = None,
    name: str = None
) -> list[Session]
```

Выводит список сеансов, связанных с текущим чат-ассистентом.

#### Параметры

##### page: `int`

Страница, на которой будут отображаться сеансы. По умолчанию `1`.

##### page_size: `int`

Количество сеансов на странице. По умолчанию `30`.

##### orderby: `str`

Поле для сортировки сеансов. Доступные варианты:

- `"create_time"` (по умолчанию)
- `"update_time"`

##### desc: `bool`

Сортировать ли сеансы в порядке убывания. По умолчанию `True`.

##### id: `str`

ID сеанса чата для получения. По умолчанию `None`.

##### name: `str`

Имя сеанса чата для получения. По умолчанию `None`.

#### Возвращает

- Успех: Список объектов `Session`, связанных с текущим чат-ассистентом.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
assistant = rag_object.list_chats(name="Miss R")
assistant = assistant[0]
for session in assistant.list_sessions():
    print(session)
```

---

### Удалить сеансы чат-ассистента

```python
Chat.delete_sessions(ids:list[str] = None)
```

Удаляет сеансы текущего чат-ассистента по ID.

#### Параметры

##### ids: `list[str]`

ID сеансов для удаления. По умолчанию `None`. Если не указано, будут удалены все сеансы, связанные с текущим чат-ассистентом.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
assistant = rag_object.list_chats(name="Miss R")
assistant = assistant[0]
assistant.delete_sessions(ids=["id_1","id_2"])
```

---

### Общение с чат-ассистентом

```python
Session.ask(question: str = "", stream: bool = False, **kwargs) -> Optional[Message, iter[Message]]
```

Задаёт вопрос указанному чат-ассистенту для начала AI-диалога.

:::tip NOTE
В режиме потоковой передачи не все ответы содержат ссылку, это зависит от решения системы.
:::

#### Параметры

##### question: `str`, *Обязательно*

Вопрос для начала AI-диалога. По умолчанию `""`

##### stream: `bool`

Выводить ли ответы в потоковом режиме:

- `True`: Включить потоковую передачу (по умолчанию).
- `False`: Отключить потоковую передачу.

##### **kwargs

Параметры из prompt(system).

#### Возвращает

- Объект `Message` с ответом на вопрос, если `stream` установлен в `False`.
- Итератор с несколькими объектами `message` (`iter[Message]`), если `stream` установлен в `True`.

Ниже перечислены атрибуты объекта `Message`:

##### id: `str`

Автоматически сгенерированный ID сообщения.

##### content: `str`

Содержимое сообщения. По умолчанию `"Hi! I am your assistant, can I help you?"`.

##### reference: `list[Chunk]`

Список объектов `Chunk`, представляющих ссылки на сообщение, каждый из которых содержит следующие атрибуты:

- `id` `str`  
  ID чанка.
- `content` `str`  
  Содержимое чанка.
- `img_id` `str`  
  ID снимка чанка. Применимо только если источник чанка — изображение, PPT, PPTX или PDF.
- `document_id` `str`  
  ID документа, на который ссылаются.
- `document_name` `str`  
  Имя документа, на который ссылаются.
- `position` `list[str]`  
  Информация о расположении чанка в документе.
- `dataset_id` `str`  
  ID набора данных, к которому принадлежит документ.
- `similarity` `float`  
  Композитный коэффициент сходства чанка от 0 до 1, где большее значение означает большее сходство. Это взвешенная сумма `vector_similarity` и `term_similarity`.
- `vector_similarity` `float`  
  Оценка векторного сходства чанка от 0 до 1, где большее значение означает большее сходство векторных эмбеддингов.
- `term_similarity` `float`  
  Оценка сходства по ключевым словам чанка от 0 до 1, где большее значение означает большее сходство по ключевым словам.

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
assistant = rag_object.list_chats(name="Miss R")
assistant = assistant[0]
session = assistant.create_session()    

print("\n==================== Miss R =====================\n")
print("Hello. What can I do for you?")

while True:
    question = input("\n==================== User =====================\n> ")
    print("\n==================== Miss R =====================\n")
    
    cont = ""
    for ans in session.ask(question, stream=True):
        print(ans.content[len(cont):], end='', flush=True)
        cont = ans.content
```

---

### Создать сеанс с агентом

```python
Agent.create_session(**kwargs) -> Session
```

Создаёт сеанс с текущим агентом.

#### Параметры

##### **kwargs

Параметры компонента `begin`.

#### Возвращает

- Успех: Объект `Session`, содержащий следующие атрибуты:
  - `id`: `str` Автоматически сгенерированный уникальный идентификатор созданного сеанса.
  - `message`: `list[Message]` Сообщения созданного сеанса ассистента. По умолчанию `[{"role": "assistant", "content": "Hi! I am your assistant, can I help you?"}]`
  - `agent_id`: `str` ID связанного агента.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow, Agent

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
agent_id = "AGENT_ID"
agent = rag_object.list_agents(id = agent_id)[0]
session = agent.create_session()
```

---

### Общение с агентом

```python
Session.ask(question: str="", stream: bool = False) -> Optional[Message, iter[Message]]
```

Задаёт вопрос указанному агенту для начала AI-диалога.

:::tip NOTE
В режиме потоковой передачи не все ответы содержат ссылку, это зависит от решения системы.
:::

#### Параметры

##### question: `str`

Вопрос для начала AI-диалога. Если компонент **Begin** принимает параметры, вопрос не обязателен.

##### stream: `bool`

Выводить ли ответы в потоковом режиме:

- `True`: Включить потоковую передачу (по умолчанию).
- `False`: Отключить потоковую передачу.

#### Возвращает

- Объект `Message` с ответом на вопрос, если `stream` установлен в `False`
- Итератор с несколькими объектами `message` (`iter[Message]`), если `stream` установлен в `True`

Ниже перечислены атрибуты объекта `Message`:

##### id: `str`

Автоматически сгенерированный ID сообщения.

##### content: `str`

Содержимое сообщения. По умолчанию `"Hi! I am your assistant, can I help you?"`.

##### reference: `list[Chunk]`

Список объектов `Chunk`, представляющих ссылки на сообщение, каждый из которых содержит следующие атрибуты:

- `id` `str`  
  ID чанка.
- `content` `str`  
  Содержимое чанка.
- `image_id` `str`  
  ID снимка чанка. Применимо только если источник чанка — изображение, PPT, PPTX или PDF.
- `document_id` `str`  
  ID документа, на который ссылаются.
- `document_name` `str`  
  Имя документа, на который ссылаются.
- `position` `list[str]`  
  Информация о расположении чанка в документе.
- `dataset_id` `str`  
  ID набора данных, к которому принадлежит документ.
- `similarity` `float`  
  Композитный коэффициент сходства чанка от 0 до 1, где большее значение означает большее сходство. Это взвешенная сумма `vector_similarity` и `term_similarity`.
- `vector_similarity` `float`  
  Оценка векторного сходства чанка от 0 до 1, где большее значение означает большее сходство векторных эмбеддингов.
- `term_similarity` `float`  
  Оценка сходства по ключевым словам чанка от 0 до 1, где большее значение означает большее сходство по ключевым словам.

#### Примеры

```python
from ragflow_sdk import RAGFlow, Agent

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
AGENT_id = "AGENT_ID"
agent = rag_object.list_agents(id = AGENT_id)[0]
session = agent.create_session()    

print("\n===== Miss R ====\n")
print("Hello. What can I do for you?")

while True:
    question = input("\n===== User ====\n> ")
    print("\n==== Miss R ====\n")
    
    cont = ""
    for ans in session.ask(question, stream=True):
        print(ans.content[len(cont):], end='', flush=True)
        cont = ans.content
```

---

### Список сеансов агента

```python
Agent.list_sessions(
    page: int = 1, 
    page_size: int = 30, 
    orderby: str = "update_time", 
    desc: bool = True,
    id: str = None
) -> List[Session]
```

Выводит список сеансов, связанных с текущим агентом.

#### Параметры

##### page: `int`

Страница, на которой будут отображаться сеансы. По умолчанию `1`.

##### page_size: `int`

Количество сеансов на странице. По умолчанию `30`.

##### orderby: `str`

Поле для сортировки сеансов. Доступные варианты:

- `"create_time"`
- `"update_time"`(по умолчанию)

##### desc: `bool`

Сортировать ли сеансы в порядке убывания. По умолчанию `True`.

##### id: `str`

ID сеанса агента для получения. По умолчанию `None`.

#### Возвращает

- Успех: Список объектов `Session`, связанных с текущим агентом.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
AGENT_id = "AGENT_ID"
agent = rag_object.list_agents(id = AGENT_id)[0]
sessons = agent.list_sessions()
for session in sessions:
    print(session)
```
---
### Удалить сеансы агента

```python
Agent.delete_sessions(ids: list[str] = None)
```

Удаляет сеансы агента по ID.

#### Параметры

##### ids: `list[str]`

ID сеансов для удаления. По умолчанию `None`. Если не указано, будут удалены все сеансы, связанные с агентом.

#### Возвращает

- Успех: Значение не возвращается.
- Ошибка: `Exception`

#### Примеры

```python
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
AGENT_id = "AGENT_ID"
agent = rag_object.list_agents(id = AGENT_id)[0]
agent.delete_sessions(ids=["id_1","id_2"])
```

---

## УПРАВЛЕНИЕ АГЕНТАМИ

---

### Список агентов

```python
RAGFlow.list_agents(
    page: int = 1, 
    page_size: int = 30, 
    orderby: str = "create_time", 
    desc: bool = True,
    id: str = None,
    title: str = None
) -> List[Agent]
```

Выводит список агентов.

#### Параметры

##### page: `int`

Страница, на которой будут отображаться агенты. По умолчанию `1`.

##### page_size: `int`

Количество агентов на странице. По умолчанию `30`.

##### orderby: `str`

Атрибут для сортировки результатов. Доступные варианты:

- `"create_time"` (по умолчанию)
- `"update_time"`

##### desc: `bool`

Сортировать ли агентов в порядке убывания. По умолчанию `True`.

##### id: `str`  

ID агента для получения. По умолчанию `None`.

##### name: `str`  

Имя агента для получения. По умолчанию `None`.

#### Возвращает

- Успех: Список объектов `Agent`.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow
rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
for agent in rag_object.list_agents():
    print(agent)
```

---

### Создать агента

```python
RAGFlow.create_agent(
    title: str,
    dsl: dict,
    description: str | None = None
) -> None
```

Создаёт агента.

#### Параметры

##### title: `str`

Заголовок агента.

##### dsl: `dict`

DSL (Domain Specific Language) канваса агента.

##### description: `str`

Описание агента. По умолчанию `None`.

#### Возвращает

- Успех: Нет.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow
rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
rag_object.create_agent(
  title="Test Agent",
  description="A test agent",
  dsl={
    # ... canvas DSL here ...
  }
)
```

---

### Обновить агента

```python
RAGFlow.update_agent(
    agent_id: str,
    title: str | None = None,
    description: str | None = None,
    dsl: dict | None = None
) -> None
```

Обновляет агента.

#### Параметры

##### agent_id: `str`

ID агента для обновления.

##### title: `str`

Новое название агента. `None`, если не нужно обновлять.

##### dsl: `dict`

Новый DSL канваса агента. `None`, если не нужно обновлять.

##### description: `str`

Новое описание агента. `None`, если не нужно обновлять.

#### Возвращает

- Успех: Нет.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow
rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
rag_object.update_agent(
  agent_id="58af890a2a8911f0a71a11b922ed82d6",
  title="Test Agent",
  description="A test agent",
  dsl={
    # ... canvas DSL here ...
  }
)
```

---

### Удалить агента

```python
RAGFlow.delete_agent(
    agent_id: str
) -> None
```

Удаляет агента.

#### Параметры

##### agent_id: `str`

ID агента для удаления.

#### Возвращает

- Успех: Нет.
- Ошибка: `Exception`.

#### Примеры

```python
from ragflow_sdk import RAGFlow
rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
rag_object.delete_agent("58af890a2a8911f0a71a11b922ed82d6")
```

---