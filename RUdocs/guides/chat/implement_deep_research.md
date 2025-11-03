---
sidebar_position: 3
slug: /implement_deep_research
---

# Реализация глубокого исследования

Реализует глубокое исследование для агентного рассуждения (agentic reasoning).

---

Начиная с версии v0.17.0, RAGFlow поддерживает интеграцию агентного рассуждения в AI-чат. Следующая диаграмма иллюстрирует рабочий процесс глубокого исследования в RAGFlow:

![Изображение](https://github.com/user-attachments/assets/f65d4759-4f09-4d9d-9549-c0e1fe907525)

Для активации этой функции:

1. Включите переключатель **Reasoning** в **Chat setting**.

![chat_reasoning](https://raw.githubusercontent.com/infiniflow/ragflow-docs/main/images/chat_reasoning.jpg)

2. Введите корректный API-ключ Tavily для использования веб-поиска на базе Tavily:

![chat_tavily](https://raw.githubusercontent.com/infiniflow/ragflow-docs/main/images/chat_tavily.jpg)

*Ниже приведён скриншот разговора с интегрированным Deep Research (глубоким исследованием):*

![Изображение](https://github.com/user-attachments/assets/165b88ff-1f5d-4fb8-90e2-c836b25e32e9)