# IFOS 36801–37200 — Data Integration & ETL/ELT OS (v1)
Цель: превратить “миллионы разрозненных источников/таблиц/файлов” в управляемые потоки данных,
которые можно:
- подключать (sources)
- нормализовать (mappings)
- проверять (quality checks)
- доставлять (sinks)
- воспроизводить (runs + lineage)
- описывать контрактами (data contracts)
- запускать как “кнопку” (pipeline orchestration)

Порядок: простое → среднее → сложное.

---

## 36801–36840 — Sources & Sinks: откуда и куда идут данные
### DataSource
Источник данных:
- SaaS (Google Sheets, Notion, HubSpot, Shopify)
- DB (Postgres, MySQL, Mongo)
- Files (S3, Drive, FTP)
- APIs (REST/GraphQL)
- Streams (Kafka, Pub/Sub)

### DataSink
Назначение:
- warehouse (BigQuery/Snowflake)
- analytics DB
- search index
- object store
- operational DB

Важно: source/sink — не “код”, а **описание подключения**, которое проверяется и версионируется.

---

## 36841–36900 — Data Contracts: договор о данных
### DataContract
Контракт описывает:
- схему (fields + types)
- SLA (частота, задержка, freshness)
- допустимые значения (enums, ranges)
- PII labels (для governance)
- владельца данных (owner) и ответственного (steward)

Это решает проблему “данные есть, но никто не знает что это”.

---

## 36901–36950 — Schema Mapping: нормализация и “перевод”
### SchemaMapping
Mapping = правила преобразования:
- rename fields
- type casting
- join/split
- normalization (phone/email formats)
- enrichment (geo, currency, categories)

Идея: маппинг хранится как **данные**, а не как “скрытый код”.

---

## 36951–37010 — Pipelines: спецификация пайплайна
### PipelineSpec
PipelineSpec включает:
- source_ref
- sink_ref
- mapping_ref
- schedule (cron / event)
- retries
- checkpoints
- governance hooks (DLP, retention tagging)
- observability (metrics)

Pipeline — это “скрипт”, но описанный декларативно.

---

## 37011–37050 — Batch Jobs: периодическая обработка
### BatchJob
Batch — если данные приходят пачками:
- nightly exports
- daily reports
- weekly sync

Batch умеет:
- backfill (догрузка истории)
- incremental (по watermark)
- partial reruns (повтор сегмента)

---

## 37051–37100 — CDC: Change Data Capture (изменения из БД)
### CDCSpec
CDC нужен, чтобы “ловить изменения”:
- insert/update/delete
- binlog / WAL / triggers

CDC pipeline:
- capture → decode → map → deliver

Плюсы:
- near‑real‑time
- меньше нагрузки, чем full export

---

## 37101–37150 — Streaming: события и потоки
### StreamSpec
Streaming для событий:
- клики, платежи, статусы заказов
- уведомления и webhooks
- телеметрия

StreamSpec описывает:
- topic/partitioning
- schema (Avro/JSON)
- consumer group semantics
- exactly-once/at-least-once

---

## 37151–37180 — Data Quality: проверки до и после
### QualityCheck
Проверки:
- completeness (не пусто)
- uniqueness (id уникален)
- validity (формат email)
- referential integrity
- drift detection (сдвиг распределения)

Реакции:
- warn
- quarantine batch
- block delivery
- open incident

---

## 37181–37200 — Catalog + Lineage: “карта данных”
### CatalogEntry
Каталог:
- где хранится набор данных
- какая схема
- кто владелец
- когда обновлялось
- какие пайплайны питают

### LineageEvent
Автоматический lineage:
- source dataset → transform → sink dataset
- run_id привязан к audit/metrics

Это превращает ETL в “объяснимую систему”, а не чёрный ящик.

---

## Итог блока
Data Integration OS создаёт “интернет данных”:
- источники и назначения как объекты
- контракты как дисциплина
- пайплайны как декларативные артефакты
- качество и lineage как стандарт

---

## Что дальше
Следующий блок:
**37201–37600 — Knowledge Base & RAG OS** (индексация документов, chunking, embeddings, retrieval, citations, KB bundles, offline KB).  
Скажете “Продолжение” — сделаю.
