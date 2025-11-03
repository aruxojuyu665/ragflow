---
sidebar_position: 4
slug: /set_chat_variables
---

# Установка переменных

Устанавливайте переменные для использования вместе с системным промптом для вашего LLM.

---

При настройке системного промпта для чат-модели переменные играют важную роль в повышении гибкости и повторного использования. С помощью переменных вы можете динамически настраивать системный промпт, который будет отправлен вашей модели. В контексте RAGFlow, если вы определили переменные в **Chat setting** (настройках чата), за исключением системной зарезервированной переменной `{knowledge}`, вы должны передавать их значения через [HTTP API](../../references/http_api_reference.md#converse-with-chat-assistant) RAGFlow или через его [Python SDK](../../references/python_api_reference.md#converse-with-chat-assistant).

:::danger ВАЖНО
В RAGFlow переменные тесно связаны с системным промптом. При добавлении переменной в разделе **Variable** включайте её в системный промпт. Аналогично, при удалении переменной убедитесь, что она удалена из системного промпта; в противном случае возникнет ошибка.
:::

## Где задавать переменные

![set_variables](https://raw.githubusercontent.com/infiniflow/ragflow-docs/main/images/chat_variables.jpg)

## 1. Управление переменными

В разделе **Variable** вы можете добавлять, удалять или обновлять переменные.

### `{knowledge}` — зарезервированная переменная

`{knowledge}` — это системная зарезервированная переменная, представляющая чанки (фрагменты), извлечённые из набора(ов) данных, указанных в **Knowledge bases** на вкладке **Assistant settings**. Если ваш чат-ассистент связан с определёнными наборами данных, вы можете оставить её без изменений.

:::info ПРИМЕЧАНИЕ
В настоящее время не имеет значения, установлена ли `{knowledge}` как необязательная или обязательная переменная, однако обратите внимание, что этот механизм будет обновлён в будущем.
:::

Начиная с версии v0.17.0, вы можете запускать AI-чат без указания наборов данных. В этом случае рекомендуется удалить переменную `{knowledge}`, чтобы избежать ненужных ссылок, и оставить поле **Empty response** пустым, чтобы избежать ошибок.

### Пользовательские переменные

Помимо `{knowledge}`, вы можете определить собственные переменные для использования вместе с системным промптом. Для использования этих пользовательских переменных необходимо передавать их значения через официальные API RAGFlow. Переключатель **Optional** определяет, являются ли эти переменные обязательными в соответствующих API:

- **Отключено** (по умолчанию): переменная обязательна и должна быть передана.
- **Включено**: переменная необязательна и может быть опущена при отсутствии необходимости.

## 2. Обновление системного промпта

После добавления или удаления переменных в разделе **Variable** убедитесь, что ваши изменения отражены в системном промпте, чтобы избежать несоответствий или ошибок. Пример:

```
You are an intelligent assistant. Please answer the question by summarizing chunks from the specified dataset(s)...

Your answers should follow a professional and {style} style.

...

Here is the dataset:
{knowledge}
The above is the dataset.
```

:::tip ПРИМЕЧАНИЕ
Если вы удалили `{knowledge}`, обязательно тщательно проверьте и обновите весь системный промпт для достижения оптимальных результатов.
:::

## API

*Единственный* способ передать значения для пользовательских переменных, определённых в диалоге **Chat Configuration**, — вызвать [HTTP API](../../references/http_api_reference.md#converse-with-chat-assistant) RAGFlow или использовать его [Python SDK](../../references/python_api_reference.md#converse-with-chat-assistant).

### HTTP API

Смотрите [Converse with chat assistant](../../references/http_api_reference.md#converse-with-chat-assistant). Пример:

```json {9}
curl --request POST \
     --url http://{address}/api/v1/chats/{chat_id}/completions \
     --header 'Content-Type: application/json' \
     --header 'Authorization: Bearer <YOUR_API_KEY>' \
     --data-binary '
     {
          "question": "xxxxxxxxx",
          "stream": true,
          "style":"hilarious"
     }'
```

### Python API

Смотрите [Converse with chat assistant](../../references/python_api_reference.md#converse-with-chat-assistant). Пример:

```python {18}
from ragflow_sdk import RAGFlow

rag_object = RAGFlow(api_key="<YOUR_API_KEY>", base_url="http://<YOUR_BASE_URL>:9380")
assistant = rag_object.list_chats(name="Miss R")
assistant = assistant[0]
session = assistant.create_session()    

print("\n==================== Miss R =====================\n")
print("Hello. What can I do for you?")

while True:
    question = input("\n==================== User =====================\n> ")
    style = input("Please enter your preferred style (e.g., formal, informal, hilarious): ")
    
    print("\n==================== Miss R =====================\n")
    
    cont = ""
    for ans in session.ask(question, stream=True, style=style):
        print(ans.content[len(cont):], end='', flush=True)
        cont = ans.content
```