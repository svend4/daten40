# IFOS 20001–20400 — Knowledge & Ontology‑OS: словарь функций, онтология, нормализация тегов, дедупликация, граф знаний, объяснимый поиск (v1)

Ключевая проблема “дикого интернета” и “сотен тысяч плагинов/сценариев” — не отсутствие решений, а отсутствие **единого языка**:
- один и тот же смысл описан разными словами (plugin/addon/extension),
- теги хаотичны (rss, RSS, news-feed, новости),
- одинаковые ассеты дублируются,
- поиск выдаёт “похожее”, но без объяснений.

Knowledge & Ontology‑OS делает:
1) **Controlled Vocabulary** (словарь терминов и функций),
2) **Taxonomy** (иерархии категорий),
3) **Synonyms & Normalization** (синонимы и приведение к канону),
4) **Entity Resolution + Dedupe** (склейка дублей),
5) **Knowledge Graph** (связи “кто с кем и как”),
6) **Explainable Search** (почему это в топе, что именно совпало).

Ниже — по шагам: от простого к сложному.

---

## 20001–20040 — Словарь (самое простое)

### 20001) Term = “каноническое слово” с определением
Каждый термин имеет:
- canonical (основная форма)
- synonyms (варианты)
- definition (коротко, 1–2 предложения)
- examples (где применяется)
- relations (is_a / related_to / opposite_of)

Пример:
- canonical: `plugin`
- synonyms: addon, extension, module
- definition: расширение приложения, добавляющее функции

### 20020) Capability vocabulary
Capabilites — это “глаголы” IFOS, стандартизированные:
- ingest.rss
- dedupe
- summarize.llm
- deliver.telegram
- compare.offers
- publish.wordpress

Важно: capability = **контракт**, а не “маркетинговое слово”.

---

## 20041–20120 — Taxonomy (простое → среднее)

### 20041) Категории как дерево
Taxonomy = иерархия:
- automation
  - workflow
  - integration
- content
  - publishing
  - news
- commerce
  - affiliate
  - marketplace

Зачем:
- навигация “как в магазине”,
- единая выдача,
- фильтры и витрины-кластеры.

### 20100) Политика тегов
Теги — свободнее, но:
- всё приводится к lower + ascii‑safe
- запрещаем мусорные теги (test1, aaa)
- вводим “recommended tags” на категорию

---

## 20121–20210 — Normalization + Synonymy (среднее)

### 20121) Normalization pipeline
1) lower-case
2) trim/replace punctuation
3) map aliases → canonical tags
4) stemming/lemmatization (опционально)
5) remove stop-tags
6) output: canonical set

### 20170) Synonym sets
Синонимы группируются:
- plugin/addon/extension/module → plugin
- rss/feed/newsfeed → rss
- telegram/tg → telegram

Имеем 2 режима:
- strict: только канон
- expansive: канон + синонимы (для recall в поиске)

---

## 20211–20310 — Entity Resolution + Dedupe (сложно)

### 20211) Entity model
В IFOS сущности:
- listing, bundle, workflow, connector, publisher, plan, policy
Каждая имеет идентификаторы + “фингерпринт” (hash контента/структуры).

### 20240) Dedupe clusters
Дубликаты склеиваются в “кластер”:
- primary entity (главная)
- duplicates (зеркала)
- evidence (почему склеили)
- confidence (0..1)
- merge actions (что переносить: отзывы, качество, инциденты)

### 20290) Entity resolution strategy
- exact: same digest / same repo+tag
- strong: high overlap of steps + same capabilities
- weak: similar title/summary + shared dependencies

---

## 20311–20370 — Knowledge Graph (очень полезно)

### 20311) Graph nodes & edges
Ноды: entities (listing/bundle/connector/publisher) + terms/capabilities  
Рёбра:
- listing HAS_CAPABILITY capability
- bundle CONTAINS workflow
- workflow CALLS connector
- publisher OWNS listing
- listing REQUIRES permission
- listing VERIFIED_BY signature

### 20350) Graph snapshot
Граф хранится как snapshot версии:
- чтобы можно было воспроизводить выдачу,
- чтобы объяснять изменения (“почему поднялся/упал”).

---

## 20371–20400 — Explainable Search (самое сложное)

### 20371) Explainable ranking
Ранжирование обязано возвращать:
- matched_terms: что совпало
- matched_capabilities: какие контракты совпали
- evidence: smoke/slo/trust signals
- penalties: почему понижено (warn/deny, vuln, низкий trust)
- final score breakdown

### 20390) Search UI: “почему это тут”
Каждая карточка в выдаче имеет кнопку:
- “Почему?” → JSON explanation → человекочитаемый текст.
Это резко снижает ощущение “магии” и повышает доверие.

---

## Что лежит в пакете
- JSON Schemas: vocab term, taxonomy, synonym set, tag normalization rules, entity, relation, dedupe cluster, provenance source, KG snapshot, embedding index, search explanation, import job
- Specs: ontology, normalization/synonyms, entity resolution/dedup, knowledge graph, explainable search
- OpenAPI: Knowledge/Ontology API (MVP)
- Examples: “News Digest Cluster” как граф + нормализованные теги + объяснение выдачи
- Python skeletons: normalizer, synonym expander, entity resolver, graph builder, explainable ranker, embedding indexer
