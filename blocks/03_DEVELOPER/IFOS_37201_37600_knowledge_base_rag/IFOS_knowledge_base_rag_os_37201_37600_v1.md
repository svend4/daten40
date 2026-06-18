# IFOS 37201–37600 — Knowledge Base & RAG OS (v1)
Цель: превратить “миллионы файлов/страниц/плагинов/гайдов” в **объяснимую базу знаний**, где:
- документы можно подключать как источники (GitHub, Drive, сайты, PDF)
- текст извлекается и нормализуется (parse)
- режется на осмысленные части (chunking)
- индексируется (embeddings + vector index)
- ищется и цитируется (retrieval + citations)
- упаковывается для оффлайна (KB snapshot / bundle)
- измеряется качество (eval runs)

Порядок: простое → среднее → сложное.

---

## 37201–37230 — Sources: откуда берём знания
### DocSource
Источник документов — это описанный объект подключения:
- `web`: сайт/домен/карта сайта
- `repo`: GitHub/GitLab репозиторий
- `drive`: папка/файл (Drive/S3)
- `api`: Notion/Confluence/Helpdesk
- `marketplace`: витрина IFOS (bundle docs)

DocSource включает: auth_ref, фильтры, расписание обновления, правила robots/limits.

---

## 37231–37270 — Parsing: сделать текст “единицами смысла”
### DocItem → DocParseResult
Парсинг делает:
- извлечение текста (PDF/HTML/MD/DOCX)
- нормализацию (unicode, пробелы, разметка)
- структуру (заголовки, таблицы, списки)
- метаданные (url, path, commit, author, time)
- “provenance” (откуда взято, какая версия)

Важно: RAG без provenance = недоверие.

---

## 37271–37320 — Chunking: резка текста правильно
### ChunkSpec
Chunking не должен быть “рубить каждые 1000 символов”.
ChunkSpec задаёт:
- целевой размер (tokens/bytes)
- overlap
- границы: заголовки/абзацы/код-блоки
- стратегии: semantic, heading-aware, code-aware
- policy: не смешивать разные разделы/языки

### ChunkItem
Chunk хранит:
- text
- offsets в исходнике
- section path (H1/H2/H3)
- ссылки на таблицы/код
- quality hints (is_code, is_table)

---

## 37321–37360 — Embeddings: превращаем текст в векторы
### EmbeddingModel
В IFOS модель эмбеддингов — объект с параметрами:
- provider (local/cloud)
- dimension
- normalization
- language support
- cost profile
- version pinning

Чтобы “интернет-функции” были воспроизводимыми, эмбеддинги должны быть версионированы.

---

## 37361–37410 — Vector Index: где живут вектора
### VectorIndex
Индекс описывает:
- storage backend (pgvector/qdrant/weaviate/faiss)
- метаданные (tenant, bundle, tags)
- шардирование/репликации
- фильтры (RBAC/ABAC)
- TTL для временных индексов

Это делает KB **многопользовательской** и безопасной.

---

## 37411–37460 — Retrieval: поиск + фильтры
### RetrievalQuery → RetrievalResult
RetrievalQuery содержит:
- query text
- scope (tenant / org / project / bundle)
- filters (tags, time range, doc_type)
- top_k
- “must cite” правило

Результат:
- список ChunkItem refs
- scores
- reasons (optional)
- candidate citations

---

## 37461–37500 — Reranking: умнее сортировка
### RerankSpec
После первичного retrieval часто нужен rerank:
- cross-encoder rerank (дороже, точнее)
- rule-based rerank (например: свежесть +  авторитетность)
- hybrid (BM25 + vectors)

RerankSpec делает это декларативно.

---

## 37501–37550 — Citations: доказуемость ответа
### Citation
Цитата должна быть проверяемой:
- doc_id + chunk_id
- точный диапазон (offsets)
- ссылка (url/path/commit)
- timestamp/version
- “why cited” (обоснование)

Правило IFOS: **ответ без цитат = черновик** (если запрос требует фактов).

---

## 37551–37580 — Offline KB: снимки для автономной работы
### KBSnapshot
Snapshot — это пакет:
- docs (или ссылки)
- chunks
- embeddings
- index metadata
- licenses/attribution
- manifests + hashes

Формат нужен для:
- работы без интернета
- переносимости (USB/архив)
- “частной базы знаний”

---

## 37581–37600 — RAG Eval: измеряем качество
### RAGEvalRun
Оценка (автоматическая + ручная):
- набор вопросов (gold set)
- expected citations
- metrics: recall@k, mrr, faithfulness, citation coverage
- регрессии при обновлении модели/чанкера

Идея: KB — это продукт, его надо измерять как продукт.

---

## Итог блока
Knowledge Base & RAG OS превращает “хаос документации” в систему:
- источники подключаемы
- текст извлекаем
- чанки стабильны
- поиск управляем
- ответы доказуемы
- оффлайн работает
- качество измеримо

---

## Что дальше
Следующий блок:
**37601–38000 — Agents & Workflow Automation OS** (задачи, планы, цепочки, Make/n8n bridge, tool registry, безопасные действия).  
Скажете “Продолжение” — сделаю.
