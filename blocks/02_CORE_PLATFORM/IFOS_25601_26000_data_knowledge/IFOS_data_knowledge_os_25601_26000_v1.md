# IFOS 25601–26000 — Data & Knowledge OS (v1)
Единая модель данных и знаний для “Интернет‑Функций”: импорт → нормализация → сущности/граф → дедупликация → индексы (embedding/RAG) → хранение/кэш/ретеншн.

Ниже — **по порядку: от простого к сложному**, шагами, чтобы это можно было реализовывать как “операционную систему данных” поверх WordPress/Make/n8n/своего backend.

---

## 25601–25640 — Core DataItem: универсальный атом данных
**DataItem** — это “всё, что мы можем сохранить и потом использовать”:
- контент (текст/HTML/JSON/файлы/байты)
- метаданные (автор, время, язык, теги, категория)
- ссылки на источник и provenance (откуда взяли и как обработали)
- статус (raw/normalized/enriched/indexed)
- политика хранения (сколько хранить, можно ли показывать публично)

**Ключевой принцип:** мы не спорим “что важнее” — RSS, PDF или API. Всё превращаем в DataItem, а дальше строим знания.

---

## 25641–25690 — Source + IngestJob: откуда и как импортируем
**Source** описывает вход:
- тип: rss/html/pdf/api/file/webhook
- endpoint/uri, auth (через SecretRef из Runtime OS)
- расписание (SchedulerJob)
- правила фильтрации и парсинга (селекторы, пагинация)
- требования к лицензии/terms (если известны)

**IngestJob** фиксирует запуск:
- source_id
- диапазон времени/страницы
- результаты (сколько items, сколько ошибок)
- ссылки на receipts (Runtime OS)

---

## 25691–25750 — NormalizedRecord: нормализация
Нормализация — перевод “как попало” → “в одном формате”:
- очистка HTML → text + структурные блоки
- выделение языка
- заголовок/аннотация/ключевые фразы
- canonical_url
- “контент‑хеш” для дедупликации

Результат: **NormalizedRecord**, который связан с DataItem (raw) и становится основой для энричмента.

---

## 25751–25820 — VersionRecord + Provenance: версии и трассировка
**VersionRecord**:
- revision_id, parent_revision_id
- diff/patch или full snapshot
- кто/что изменило (agent/user/pipeline)
- причины (normalize, enrich, redact, fix)

**Provenance**:
- цепочка действий: ingest → normalize → entity_extract → dedupe → embed → rag
- параметры шагов и хеши входа/выхода
- ссылки на receipts и артефакты

Это делает знания “проверяемыми”, а не магией.

---

## 25821–25880 — Entity + EntityLink: сущности и связи
**Entity** — нормализованный объект:
- Person / Org / Product / Place / Event / Topic / URL / Doc
- aliases (синонимы)
- identifiers (wikidata, domain, sku и т.п. — если есть)
- evidence_refs (какие DataItem поддерживают сущность)

**EntityLink** — ребро графа:
- тип: mentions / same_as / part_of / related_to / cites / produced_by
- вес/уверенность
- источники доказательства

Так строится **KnowledgeGraph** — не только “тексты”, но и структура.

---

## 25881–25930 — DedupeCluster: дедупликация и “канонизация”
Дедупликация нужна, потому что интернет — это копии/репосты/переводы.
**DedupeCluster**:
- список record_ids
- canonical_record_id
- причины (same_url, near_duplicate, same_hash, same_entity_signature)
- правила мерджа (что брать в canonical: title/body/metadata)

Цель: 1000 одинаковых новостей → 1 канон + ссылки на варианты.

---

## 25931–25970 — EmbeddingIndex: семантические индексы
**EmbeddingVector**:
- model_id
- dims
- vector (или ссылочный формат)
- scope (collection/tenant)

**EmbeddingIndex**:
- стратегия: flat/hnsw/ivf
- политика обновления (batch/stream)
- filters (lang, date, topic, publisher)
- версионирование индекса

Это основа RAG и “умного поиска”.

---

## 25971–26000 — RAGQuery/RAGResult + StoragePolicy/CachePolicy
**RAGQuery**:
- вопрос
- фильтры (язык, даты, источники, доверие)
- топ‑k, rerank, citations_required
- режим: preview/safe/prod

**RAGResult**:
- answer
- citations (record refs)
- extracted entities
- confidence + warnings

**StoragePolicy**:
- retention_days
- tier (hot/warm/cold/archive)
- pii_policy (redact/deny)
- legal_hold (не удалять)

**CachePolicy**:
- ttl
- invalidation triggers (новая версия, новый дедуп-кластер, новый индекс)
- stale‑while‑revalidate

---

## Мини‑архитектура “Data OS”
1) Ingest (RSS/HTML/PDF/API) → DataItem(raw)  
2) Normalize → NormalizedRecord (+Version +Provenance)  
3) Entity Extract → Entity + links  
4) Dedupe → canonical records  
5) Embed → EmbeddingIndex  
6) Query → RAGResult (+citations)  
7) Retention/Cache → контролируем хранение и скорость

---

## Что дальше логически
Следующий блок (если скажете “Продолжение”):
**26001–26400 — “Trust & Governance OS”**: trust score источников, политика лицензий, безопасность данных, модерация знаний, права на контент, аудит, “policy gates” для RAG/выдачи.
