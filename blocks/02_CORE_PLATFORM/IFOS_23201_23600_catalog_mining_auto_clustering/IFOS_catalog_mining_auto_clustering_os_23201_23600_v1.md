# IFOS 23201–23600 — Catalog Mining & Auto‑Clustering OS: добыча “атомов функций”, дедупликация, таксономия, кластеры, витрины, авто‑подъём качества L0→L3 (v1)

Цель: превратить “дикое поле” (миллионы репозиториев, шаблонов, плагинов, сценариев) в **понятный каталог функций**:
- каждая функция имеет имя, входы/выходы, зависимости, риск, стоимость,
- функции автоматически группируются в **кластеры** (как “пакеты офисных возможностей”),
- из кластеров строятся **витрины** (“сделай как Excel‑макрос, но для интернета”),
- и система сама поднимает качество (L0→L3) через **автодоки + автотесты + sandbox прогон**.

Дальше — по порядку: от простого (источник/импорт) к сложному (кластеризация/качество).

---

## 23201–23260 — Источники и задания импорта (самое простое)

### 23201) SourceRef: что мы импортируем
Источник может быть:
- GitHub repo / release
- WordPress plugin (официальный каталог)
- Make template / scenario export
- n8n workflow
- npm/pypi package
- “документ” (README, tutorial, gist)

Каждый SourceRef хранит:
- URL/идентификатор
- тип источника
- дату/версию
- лицензии (если известны)
- сигнатуры/хэши (если есть)

### 23230) IngestJob: как мы импортируем
Импорт идёт “job’ами”:
- fetch → normalize → extract atoms → dedupe → embed → cluster → publish
Каждый этап пишет лог/метрики (из Observability OS).

---

## 23261–23330 — Extractor rules: как из хаоса сделать “атом функции”

### 23261) ExtractorRule: правила извлечения
Примеры:
- из Make JSON: вытаскиваем модули и связки (trigger→actions)
- из WP plugin: endpoints, hooks, settings, permissions
- из README: “how to use” и минимальный пример

### 23290) AtomFunction: атом функции (каноническая карточка)
AtomFunction — это минимальный “глагол”:
- `action`: “send_telegram_message”, “fetch_rss”, “compare_prices”
- `inputs/outputs` (типы, обязательность)
- `deps` (коннекторы/плагины/библиотеки)
- `constraints` (rate limits, auth, PII)
- `cost_model` (примерно)
- `evidence` (куда смотреть: исходник, тест, пример)

Это тот самый “технический словарь функций”, который вы описывали.

---

## 23331–23410 — Дедупликация и слияние (очень важно)

### 23331) DedupeRecord
Одна и та же функция может быть реализована 1000 раз.
Нужен механизм:
- вычислить “почти одинаково” (embedding + heuristics)
- выбрать “каноническую” карточку
- хранить алиасы и альтернативы

### 23370) Merge policy
Слияние НЕ должно терять информацию:
- канон + список вариантов
- различия по платформам (Make vs n8n vs WP)
- отличия лицензий и рисков

---

## 23411–23490 — Таксономия + embeddings (от среднего к сложному)

### 23411) TaxonomyNode
Таксономия — это дерево категорий:
- Communication → Messaging → Telegram
- Data → Ingest → RSS
- Commerce → Compare → Price comparison

### 23440) EmbeddingRecord
Векторные представления нужны для:
- похожесть функций
- автокластеризация
- поиск “как сделать X”

Важно: embeddings — только один из сигналов. Дальше включается Trust OS.

---

## 23491–23550 — Кластеры функций (сердце системы)

### 23491) FunctionCluster
Кластер — это “пачка функций”, которая закрывает задачу:
- “News Digest Cluster”
- “Travel Comparison Cluster”
- “WP Lead Capture Cluster”

Кластер хранит:
- список AtomFunction
- “канонический blueprint” (Make/n8n/WP variants)
- зависимость и порядок установки
- витрину (UI карточки)
- SLO пресеты

---

## 23551–23600 — Авто‑подъём качества L0→L3 (встроенная рационализация)

### 23551) QualityUpliftTask
Задача, которая поднимает пакет:
- собрать автодоки (AutodocBundle)
- сгенерировать автотест‑план (AutotestPlan)
- прогнать sandbox install/run
- собрать receipt + signals
- присвоить L2/L3 если прошло критерии

### 23580) ClusterVitrine
Витрина — это то, что видит пользователь:
- “что делает” (1–2 строки)
- “установить” (one-click)
- “проверить” (sandbox run)
- “варианты” (Make/n8n/WP)
- “доказательства” (trust signals, отзывы)
- “риск/стоимость/совместимость”

---

## Что в пакете
- JSON Schemas: SourceRef, IngestJob, ExtractorRule, AtomFunction, DedupeRecord, TaxonomyNode, EmbeddingRecord, FunctionCluster, ClusterVitrine, QualityUpliftTask, AutodocBundle, AutotestPlan, ImportManifest, LabelingDecision, FeedbackLoop
- Specs: mining pipeline, clustering, taxonomy+embeddings, dedupe+merge, quality uplift L0→L3, vitrines generation, governance policy
- OpenAPI: Catalog Mining API (MVP)
- Examples: импорт Make‑сценария → атомы → дедуп → кластер → витрина → uplift до L2
- Python stubs: miner, extractor engine, clusterer, uplift orchestrator, vitrine builder
