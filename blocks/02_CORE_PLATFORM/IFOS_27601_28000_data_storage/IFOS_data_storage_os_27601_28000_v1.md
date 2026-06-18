# IFOS 27601–28000 — Data & Storage OS (v1)
Этот блок отвечает за то, чтобы IFOS мог **собирать, хранить, нормализовать, версионировать и выдавать данные** — не “в чатике”, а как инженерная система.
Главная идея: **данные — это актив**, их надо уметь повторно использовать, сравнивать, экспортировать и проверять.

Ниже — **по порядку, от простого к сложному**.

---

## 27601–27630 — DataSource: источник данных как объект
Источник — не “просто URL”, а описанная сущность:
- тип: rss / html / api / file / appstore / github / webhook
- конфиг: url, headers, auth (через secrets), пагинация
- ограничения: rate_limit_ref, robots/terms hints
- качество/репутация: trust_score, notes
- правила обновления: etag/last_modified, polling interval

Зачем: если источники не описаны, всё превращается в ручной хаос.

---

## 27631–27670 — Collection: коллекция (папка данных) внутри Workspace
Collection — это “набор записей” с общей темой/логикой:
- “Новости (RSS)”, “Плагины WordPress”, “Сценарии Make.com”, “Отзывы (AppStore/Google Play)”, “Каталог API”
- фильтры/теги
- схема нормализации (какие поля обязательны)
- политика хранения/сроков (retention_policy_ref)

Идея: коллекция = **таблица/индекс** уровня “Excel”, но живёт в IFOS.

---

## 27671–27720 — ItemRecord: единая нормализованная запись
ItemRecord — “атом данных”:
- canonical_id (стабильный идентификатор)
- source_ref + source_item_id
- title, url, published_at, author, content, language
- metadata (tags, category, rating, price, region…)
- hashes (content_hash, url_hash) для дедупа
- provenance (откуда получено, какой парсер, какая версия)

Это помогает:
- сравнивать “яблоки с яблоками”
- делать дедуп
- строить поиск/индексы
- пересобирать витрины и отчёты

---

## 27721–27770 — Dedupe & Versions: дедупликация и версионирование
Дедуп — не “одинаковые строки”, а правила:
- exact dedupe: url_hash / content_hash
- near-dedupe: похожие заголовки + близкие даты
- canonical merge: “этот же объект, но из другого источника”

Версионирование:
- ItemRecord может иметь revisions (v1,v2…)
- хранить diff (что поменялось)
- поддержка “time-travel”: “покажи состояние на дату X”

---

## 27771–27820 — Artifact: результат работы (файлы/отчёты/сводки)
Artifact — всё, что produced by jobs/flows:
- markdown report
- csv export
- json bundle
- html vitrines
- logs
- evidence pack (источники/цитаты/скриншоты)

Артефакт должен иметь:
- тип, размер, checksum, created_by_run_id
- ссылку на коллекцию/запрос
- политику хранения (retention)

---

## 27821–27860 — StorageBackend: где храним
IFOS не обязан хранить всё “в одной базе”:
- local_fs (локально)
- s3_compatible
- gdrive (через коннектор)
- database (Postgres/SQLite)
- vector_db (для embeddings)

StorageBackend описывает:
- endpoint, bucket/path
- encryption at rest (опционально)
- access policy (read/write scopes)

---

## 27861–27910 — Index: индексация и поиск (текст + векторы)
Индексы:
- fulltext (по title/content/metadata)
- facet (категории/теги/регион)
- embeddings index (RAG)
- diff index (“что изменилось за неделю”)

Index хранит:
- на каких коллекциях построен
- режим обновления (incremental/full rebuild)
- статус/метрики

---

## 27911–27940 — CachePolicy: кэш и повторное использование
Кэш нужен для:
- повторных запросов к API
- повторного парсинга страниц
- повторных RAG‑ответов (с осторожностью)
- “прогрева” витрин/дашбордов

CachePolicy:
- ttl_seconds
- invalidation rules (по тегам/по источнику)
- max_size

---

## 27941–27970 — Import/Export: переносимость данных
Экспорт форматы:
- CSV (таблично)
- JSON (структурно)
- Bundle (manifest + artifacts + schemas)
- “Evidence pack” (для проверяемости)

Импорт:
- приём чужих пакетов
- маппинг полей
- проверка schema + checksum
- модерация/санитайзинг (связь с Governance OS)

---

## 27971–28000 — Retention & Backup: хранение, архив, бэкапы
RetentionPolicy:
- сколько хранить raw vs normalized vs artifacts
- “удалять через 30 дней” или “архивировать”
- legal hold (не удалять)

BackupPlan:
- full + incremental
- расписание (связь с Automation OS)
- verify restore (проверка восстановления)
- отчёт о целостности (checksums)

---

## Мини‑архитектура Data & Storage OS
1) Источники → 2) Коллекции → 3) Записи (ItemRecord) → 4) Дедуп/версии  
5) Артефакты → 6) Индексы → 7) Экспорт/импорт → 8) Retention/Backup

---

## Что дальше логически
Следующий блок (если скажете “Продолжение”):
**28001–28400 — “Security & Governance OS”**: секреты, политики, аудит, модерация данных, безопасность пакетов, роли/ACL, compliance, запреты/allow-lists, “доверенные источники”.
