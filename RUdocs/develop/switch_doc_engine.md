---
sidebar_position: 3
slug: /switch_doc_engine
---

# Переключение движка документов

Переключите движок документов с Elasticsearch на Infinity.

---

RAGFlow по умолчанию использует Elasticsearch для хранения полного текста и векторов. Чтобы переключиться на [Infinity](https://github.com/infiniflow/infinity/), выполните следующие шаги:

:::caution WARNING
Переключение на Infinity на машине с Linux/arm64 пока официально не поддерживается.
:::

1. Остановите все запущенные контейнеры:

   ```bash
   $ docker compose -f docker/docker-compose.yml down -v
   ```

:::caution WARNING
`-v` удалит тома docker-контейнеров, и существующие данные будут очищены.
:::

2. Установите `DOC_ENGINE` в файле **docker/.env** в значение `infinity`.

3. Запустите контейнеры:

   ```bash
   $ docker compose -f docker-compose.yml up -d
   ```