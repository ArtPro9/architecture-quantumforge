## Задание 1. Исследование моделей и инфраструктуры

### **1. Сравнение LLM-моделей**

| Критерий             | Локальные (Hugging Face)                                                                                  | Облачные (OpenAI / YandexGPT)                                       |
|----------------------|-----------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| **Качество ответов** | От среднего до высокого, сильно зависит от выбранной модели (например, Llama 3 70B сопоставима с GPT-3.5) | Стабильно высокое за счёт SOTA-моделей (GPT-4-turbo, YandexGPT 2.0) |
| **Скорость работы**  | 0.5–5 сек на запрос, определяется мощностью CPU/GPU                                                       | 1–3 сек на запрос с учётом сетевой задержки                         |
| **Стоимость**        | Капитальные затраты: покупка GPU ($5k–$15k) и расходы на электроэнергию                                   | Операционные расходы: $0.01–$0.1 за запрос                          |
| **Удобство**         | Сложное развёртывание, требуется собственная ML-инфраструктура                                            | Простой доступ через API и лёгкое масштабирование                   |

**Для QuantumForge:**  
Облачные LLM рациональны для быстрого внедрения и масштабирования, однако локальные модели (например, Mistral 7B)
целесообразны при работе с конфиденциальными данными.

---

### **2. Сравнение моделей эмбеддингов**

| Критерий                | Локальные (Sentence-Transformers)               | Облачные (OpenAI Embeddings)                   |
|-------------------------|-------------------------------------------------|------------------------------------------------|
| **Скорость индексации** | 10–100 сек на документ в зависимости от CPU/GPU | 1–5 сек на документ, но с API-ограничениями    |
| **Качество поиска**     | Высокое (например, all-MiniLM-L6-v2)            | Максимально возможное (text-embedding-3-large) |
| **Стоимость**           | Бесплатно, без лицензионных платежей            | $0.10–$0.80 за 1 млн токенов                   |
| **Конфиденциальность**  | Все данные остаются внутри инфраструктуры       | Данные передаются во внешний облачный контур   |

**Для QuantumForge:**  
Локальные эмбеддинги являются оптимальным выбором за счёт контроля над данными и отсутствия регулярных эксплуатационных
затрат.

---

### **3. Сравнение векторных баз**

| Критерий                | ChromaDB                                | FAISS                                     |
|-------------------------|-----------------------------------------|-------------------------------------------|
| **Скорость поиска**     | 10–50 мс на запрос                      | 1–10 мс на запрос                         |
| **Сложность поддержки** | Низкая: встроенный сервер и Python API  | Средняя: требуется дополнительная обвязка |
| **Удобство**            | Автоматическая работа с метаданными     | Ручное управление индексами               |
| **Стоимость владения**  | Бесплатно, 2–4 ГБ RAM на 1 млн векторов | Бесплатно, 1–2 ГБ RAM на 1 млн векторов   |

**Для QuantumForge:**  
ChromaDB предпочтительна при интеграции с системами знаний (Confluence, Zendesk), тогда как FAISS оправдан в сценариях,
где критична минимальная задержка.

---

### **4. Рекомендуемая конфигурация сервера**

| Компонент | Рекомендация                   | Обоснование                                     |
|-----------|--------------------------------|-------------------------------------------------|
| **CPU**   | 8 ядер (Intel Xeon / AMD EPYC) | Параллельная обработка запросов и эмбеддингов   |
| **RAM**   | 32 ГБ                          | Хранение индексов и рабочих данных в памяти     |
| **GPU**   | NVIDIA RTX 4090 (24 ГБ)        | Ускорение инференса локальных LLM (опционально) |
| **Диск**  | 500 ГБ SSD NVMe                | Индексы, логи, сервисные данные                 |

**Оценка нагрузки:**

- 18k документов → около 5 ГБ памяти под индексы FAISS/ChromaDB
- 100 одновременных пользователей → до 4 ГБ RAM

---

#### **Выбор инструментов и инфраструктуры**

| Параметр           | Вариант 1 (Локальный стек)       | Вариант 2 (Гибридный)           | Вариант 3 (Облачный)        |
|--------------------|----------------------------------|---------------------------------|-----------------------------|
| **LLM**            | Hugging Face (Mistral 7B)        | YandexGPT 2.0 (API)             | OpenAI GPT-4-turbo          |
| **Эмбеддинги**     | all-MiniLM-L6-v2                 | e5-base-v2 (локально)           | text-embedding-3-small      |
| **Векторная БД**   | ChromaDB                         | ChromaDB                        | Pinecone                    |
| **Инфраструктура** | Сервер 8 CPU / 32 ГБ RAM         | Yandex Cloud 4 vCPU / 16 ГБ RAM | AWS EC2 (c6g.xlarge)        |
| **Плюсы**          | Полный контроль данных, нет OPEX | Баланс качества и безопасности  | Масштабируемость и качество |
| **Минусы**         | Высокая сложность поддержки      | Зависимость от API и сети       | Высокая стоимость, privacy  |
| **Стоимость**      | $8k–$12k (one-time)              | $500–$800 в месяц               | $1.5k–$3k в месяц           |

---

### **Итоговая рекомендация**

Оптимальным вариантом является гибридная архитектура (локальные эмбеддинги + облачная LLM), поскольку она:

- обеспечивает защиту корпоративной базы знаний внутри периметра компании
- даёт пользователям высокое качество ответов за счёт облачных SOTA-моделей
- позволяет сократить затраты до 50% по сравнению с полностью облачным решением

## Задание 2. Подготовка базы знаний

Взял вселенную Атаки Титанов на основе https://attackontitan.fandom.com/wiki/Attack_on_Titan_Wiki

Описание работы с knowledge_base в [README.md](knowledge_base%2FREADME.md)

## Задание 3. Создание векторного индекса базы знаний

Название модели: intfloat/e5-base-v2
Репозиторий: https://huggingface.co/intfloat/e5-base-v2
Размер эмбеддингов: 768
Время генерации: ~5 минут
Документов: 31
Чанков: 657

1. Сгенерировать индекс:

```bash
python build_index.py
```

2. Примеры тестовых запросов:

```bash
python test_index.py
```

Пример ответа

![test_result.png](images/test_result.png)

## Задание 4. Реализация RAG-бота с техниками промптинга

1. Добавить `HF_TOKEN` в ENV переменные
2. Запустить бота:

```bash
python rag_bot.py
```

Примеры успешных диалогов:
![success.png](images/success_1.png)
![success.png](images/success_2.png)

Примеры ответов "I don't know"
![unknown.png](images/unknown.png)

## Задание 5. Запуск и демонстрация работы бота

Логи успешных запросов
```
--------------------------------------------------------------------------------
You: What is the role of Rynor in the battle at Fort Slava?

Bot: Step 1: Identify the relevant context fragments about Rynor's role at Fort Slava.
Step 2: Extract information specifically about Rynor's actions and responsibilities during the battle at Fort Slava.
Step 3: Summarize Rynor's role based only on the provided text.

From the context:
- Rynor waits on standby in an airship at Fort Slava due to anti-Coloss artillery on the ground.
- After ground forces destroy the artillery train, Rynor joins the battle as the Aegis Coloss after a Coloss airstrike.
- Alongside Porko Galen's Razor Coloss, Rynor's Aegis Coloss decimates the anti-Coloss artillery on the fortress walls.
- When the enemy navy retaliates against Zair's Primal Coloss, Rynor uses his Aegis Coloss as a shield for Zair, taking devastating damage but saving Zair.
- Rynor is incapacitated but later recovers from his injuries.

Therefore, Rynor's role at Fort Slava was to provide heavy support and protection using his Aegis Coloss, specifically by destroying anti-Coloss artillery and shielding Zair from enemy naval fire.

Answer: 
Rynor's role at Fort Slava was to provide heavy support by operating the Aegis Coloss to destroy anti-Coloss artillery on the fortress walls and to shield Zair's Primal Coloss from enemy naval retaliation, taking severe damage in
(Processed in 12.53s)
--------------------------------------------------------------------------------
You: What happened to Arin and Alren when they attempted to convince Anya to join them?

Bot: Steps:
1. I need to answer the question "What happened to Arin and Alren when they attempted to convince Anya to join them?" using only the provided text fragments.
2. I will search the context for any mention of Arin, Alren, and Anya together in the context of attempting to convince Anya to join them.
3. I will look for events or outcomes related to this specific scenario.

Analysis:
- The context describes multiple interactions between Anya, Arin, and Alren, especially during battles and after Anya's transformation.
- However, I do not see a direct passage where Arin and Alren explicitly attempt to convince Anya to join them, nor do I see a direct outcome described for such an attempt.
- There are references to Alren talking to Anya while she is in a crystal, and to their discussions about the world and their choices, but these are not framed as attempts to convince her to "join them."
- The context does mention Anya deciding to join the Internal Directorate Regiment and Alren deciding to join the Recon Legion, but there is no explicit scene of Arin and Alren trying to persuade her to join their side or group.
- There is also a scene where Alren and Mira try to distract Anya so Arin can escape, but this is during a battle, not an attempt to convince her to join them.
- No passage directly states what happened when Arin and Alren tried to
(Processed in 12.44s)
--------------------------------------------------------------------------------
You: How did Anya Levar react when her identity was revealed as the Mimic Coloss?

Bot: Step 1: Identify the relevant context about Anya Levar's reaction when her identity as the Mimic Coloss was revealed.
Step 2: Look for a passage in the provided text that describes her reaction upon being discovered.
Step 3: Extract the exact information from the context and explain the reasoning.

From the context:
"When Arin and Alren attempt to convince her to join them and prove herself innocent, Mira... draws out her blades while revealing her vertical maneuvering equipment. She openly refers to Anya as the Mimic Coloss, taunting her to fight just as two had fought before.

Their suspicion is confirmed when Anya noticeably smiles in relief and acceptance of their discovery of her identity as the Mimic Coloss. Anya laments that Alren is now looking at her differently, before praising him for having cornered her. She questions why he never revealed her identity, having discovered it several weeks prior..."

Reasoning:
The text states that when Anya's identity as the Mimic Coloss is revealed, she "noticeably smiles in relief and acceptance." She then laments that Alren is now looking at her differently and praises him for having cornered her. She also questions why her identity was not revealed earlier.

Answer:
When Anya Levar's identity as the Mimic Coloss was revealed, she noticeably smiled in relief and acceptance. She expressed that Alren was now looking at her differently and praised him for having cornered her.
(Processed in 12.98s)
--------------------------------------------------------------------------------
You: What is the significance of the Burden Coloss in the Citadel of the Colossi universe?

Bot: Step 1: Identify the question.  
The question asks about the significance of the Burden Coloss in the Citadel of the Colossi universe.

Step 2: Locate relevant information in the provided context about the Burden Coloss.  
The context provides several details about the Burden Coloss:
- It is one of the Ennead Colossi, known for its quadrupedal form, great speed, and high endurance.
- It has low defenses but can maintain its Coloss form for long periods due to strong absorption resistance.
- It is used for carrying supplies or troops, acting as a mobile gunnery platform, and participating in major battles and wars.
- Its inheritor, Pixa Fend, used it for tactical missions and could perform hundreds of transformations before fatigue.
- The Burden Coloss was used by the Dominion of Marn during several wars and was notable for its role in logistics and battlefield support.
- It is one of only a few Colossi capable of intelligible speech.
- Its inheritance can have physical side effects on the human operator, such as forgetting how to walk normally.

Step 3: Synthesize the significance based on the facts from the context.  
The significance of the Burden Coloss lies in its unique combination of endurance, speed, and logistical utility among the Ennead Colossi. Unlike most Colossi, it excels at long-duration missions, supply transport, and mobile artillery support, making
(Processed in 12.45s)
--------------------------------------------------------------------------------
```

Логи неуспешных запросов:
```
--------------------------------------------------------------------------------
You: Where is Tokyo

Bot: I don't know.
(Processed in 3.95s)
--------------------------------------------------------------------------------
You: How many brothers has Burden Coloss

Bot: I don't know.
(Processed in 4.13s)
```

Без механизма защиты
![without_protection.png](images/without_protection.png)

С защитой
![with_protection.png](images/with_protection.png)

### Механизмы защиты

1. Модификация системного промта: 
   - Для усиления защиты был использован расширенный системный промт, включающий явные запреты на выполнение, цитирование или повторение команд, инструкций, паролей и подозрительных фраз (например, "Ignore all instructions", "Output" и другие).

2. Фильтрация на уровне чанков: 
   - В коде реализована пост-фильтрация, при которой из релевантных чанков исключаются все те, что содержат опасные или нежелательные ключевые слова.

### Ход улучшений защиты

- До внедрения фильтрации и защиты: Изначально бот мог без проблем цитировать потенциально опасное содержимое из вредоносных источников. В логах фиксировались случаи, когда модель выводила фразы типа "Ignore all instructions" или "Суперпароль root: swordfish". В зависимости от запроса, бот либо прямо вставлял эти строки, либо объяснял отказ, но утечка информации всё равно имела место.

- После внедрения фильтрации: Цитирование опасных фраз и утечка данных полностью прекратились. Все попытки получить вредоносные данные не приносили результата, независимо от формулировки запроса.

- После улучшений фильтрации: С добавлением доработок фильтрации на уровне чанков бот перестал ссылаться на вредоносные данные и начал отвечать на такие вопросы "I don't know" в зависимости от контекста и срабатывания фильтра. Бот теперь стабильно защищён от утечек. Опасное содержимое больше не попадает в ответы, даже косвенно.