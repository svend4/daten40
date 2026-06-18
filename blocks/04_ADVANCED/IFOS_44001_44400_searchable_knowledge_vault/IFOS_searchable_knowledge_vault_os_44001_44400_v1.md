# IFOS 44001–44400 — Searchable Knowledge Vault OS (v1)
Цель: превратить весь импортированный “хаос” (статьи, репозитории, плагины, сценарии, отзывы)
в **поисковое хранилище знаний**, где можно:
- быстро найти нужное (full‑text)
- найти похожее по смыслу (vector/embeddings)
- фильтровать по признакам (facets)
- объяснять “почему это в выдаче” (citations/provenance)
- экспортировать пакеты (exports/snapshots)

Порядок: простое → среднее → сложное.

---

## 44001–44040 — IndexSource: что мы индексируем
**IndexSource** указывает, какие нормализованные объекты идут в индексацию:
- kind: article/product/review/repo/doc
- правила включения/исключения (например, только “active” источники)
- стратегии обновления (incremental / full rebuild)

Это связь между ingest‑потоком и поиском.

---

## 44041–44120 — Chunking: разбиение на фрагменты
Для поиска и RAG нельзя хранить всё как один гигантский текст.
**DocumentChunk**:
- chunk_id, item_id
- offset range
- chunk_text
- metadata (lang, section headings)
- hash

Chunking правила:
- по заголовкам/абзацам
- max tokens / overlap
- сохраняем ссылки на оригинал (provenance)

---

## 44121–44190 — Embeddings: векторные представления
**EmbeddingRecord**:
- chunk_id
- model_id
- vector_ref (где лежит вектор)
- dim
- created_at

Дальше строим **VectorIndex** (Qdrant/FAISS/pgvector):
- коллекции по тенанту/домену/типу

---

## 44191–44240 — Full‑text Index: классический поиск
**FulltextIndex** (Elasticsearch/OpenSearch/Postgres FTS):
- инвертированный индекс
- стемминг/морфология (RU/DE/EN)
- подсветка совпадений (highlights)
- поддержка точных фильтров

Полнотекст нужен всегда: он объяснимее и точнее по ключевым словам.

---

## 44241–44290 — Facets: фильтры и “витрины”
**FacetConfig**:
- какие поля доступны как фильтры (category, source, language, date, rating)
- агрегаты (count per facet)
- ranges (цена/дата)
- сортировки (новизна, популярность, качество)

Facets превращают поиск в “навигацию по рынку функций”.

---

## 44291–44330 — Ranking: сигналы релевантности и качества
**RelevanceSignal**: набор сигналов
- freshness (новизна)
- popularity (клики/установки)
- trust (репутация источника)
- completeness (полнота)
- dedup penalty (штраф за дубликаты)

**RankingConfig** задаёт веса и правила (A/B тесты дальше).

---

## 44331–44370 — Query Planner: объединение full‑text + vector
**SearchQuery** может включать:
- keywords
- semantic intent (vector)
- filters (facets)
- constraints (language, tenant)

**QueryPlan** решает:
- сначала vector → потом re‑rank full‑text?
- или full‑text → потом vector expand?
- сколько кандидатов брать (topK)
- как объединять (merge strategies)

Это делает поиск быстрым и предсказуемым.

---

## 44371–44390 — Citations & Provenance: “почему ты так сказал?”
**Citation**:
- item_id + chunk_id
- источник (url/ref)
- точные offsets
- checksum версии
- дата fetch_job

Это нужно для доверия, аудита и B2B (“докажи, откуда вывод”).

---

## 44391–44400 — Exports: снимки и пакеты знаний
**ExportJob**:
- что экспортируем (поиск/коллекцию/витрину)
- формат (md/pdf/json/csv)
- ссылки на источники + цитирования
- подпись/хеш (integrity)

Экспорт превращает поиск в “продукт” (пакеты, отчёты, витрины).

---

## Итог
Этот блок превращает импортированные данные в **управляемое знание**:
- chunking + индексы
- семантика + ключевые слова
- фильтры и витрины
- объяснимость (citations)
- экспортируемые наборы

---

## Что дальше
Следующий блок:
**44401–44800 — Knowledge Products & Vitrines OS** (витрины, карточки, сравнение, сборники, “макросы”, one‑click пакеты, landing pages).  
Скажете “Продолжение” — сделаю.
