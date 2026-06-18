# IFOS 24001–24400 — Interoperability & Compatibility OS: единые контракты I/O, адаптеры Make↔n8n↔WP, конвертация сценариев, матрица совместимости, compat score (v1)

Это слой “грамматики” и “переводчика”.
Если Catalog Mining OS добывает атомы и кластеры, а Installer & Runtime OS ставит “одной кнопкой”,
то Interoperability OS делает так, чтобы:
- один и тот же кластер мог существовать в вариантах (Make / n8n / WP / custom),
- входы/выходы были **совместимы**, типы — **единообразны**,
- конвертация и сборка происходили **автоматически**,
- пользователю всегда показывался лучший вариант “под его профиль” (compat score).

Дальше — по порядку (от простого к сложному).

---

## 24001–24060 — Что такое “контракт” и почему это важнее кода

### 24001) Проблема
Интернет-поле “дикое” потому что:
- у каждого инструмента свой формат сценариев,
- одна и та же функция называется по‑разному,
- типы данных несовместимы (строка vs объект vs массив),
- а ошибки проявляются только “в рантайме”.

### 24015) Решение: IFOS I/O Contract
Контракт — это каноническое описание:
- `action` (глагол)
- `inputs`/`outputs`
- типы и ограничения (TypeSystem)
- семантические теги (“chat_id”, “rss_url”, “pii”)
- поведение при ошибках (retry/backoff/idempotency)
- политика приватности (PII/no-PII)

Контракт становится “грамматикой” для перевода.

---

## 24061–24130 — TypeSystem (единая типовая система)

Типы должны быть одинаковыми для всех платформ:
- primitives: string, number, boolean, datetime, url
- compound: object, array<T>, map<K,V>
- special: secret_ref, file_ref, pii_string, token_count

В TypeSystem также есть:
- nullability
- validation (regex, min/max, enum)
- redaction rules (для логов и receipts)

---

## 24131–24210 — ConnectorCapability: что умеет конкретный коннектор

Коннекторы (Make module / n8n node / WP plugin) имеют ограничения:
- поддерживаемые поля
- лимиты (rate limit)
- методы аутентификации
- поддержка webhooks
- поддержка файлов
- поддержка “dry-run”

ConnectorCapability — это “паспорт” коннектора для compat engine.

---

## 24211–24280 — AdapterSpec и MappingRule (переводчики)

### 24211) AdapterSpec
Адаптер — это:
- “как привести входы контракта к формату платформы”
- “как распаковать выходы платформы в канонический контракт”
- “как обработать ошибки”

### 24240) MappingRule
Правила маппинга:
- field mapping (chat_id → chatId)
- transforms (string → array<string>)
- defaults (timeout=30s)
- guards (если поле отсутствует → fail/warn)

Это позволяет автоматизировать конвертацию.

---

## 24281–24340 — ConversionPlan + ConversionJob (авто-конвертер сценариев)

### 24281) ConversionPlan
План конвертации определяет:
- исходная платформа и целевая
- список узлов/шагов
- какие адаптеры применить
- где неизбежна ручная правка (manual flags)
- как протестировать (TestVector)

### 24310) ConversionJob
Job: запускаем план, генерируем артефакты:
- n8n workflow JSON
- WP plugin config stub
- custom FastAPI wrapper (если нужно)

Далее это идёт в Installer OS.

---

## 24341–24400 — Compatibility Matrix + Compat Score (выбор лучшего варианта)

### 24341) CompatibilityMatrix
Матрица на уровне кластера:
- какие платформы доступны
- какие условия требуют (hosting, secrets, auth)
- какой уровень качества (L0..L5)
- какие риски

### 24370) CompatScore
Алгоритм выбора варианта “по профилю”:
- профиль (dev/sandbox/prod) и ограничения (privacy/cost/hosting)
- наличие адаптеров/контрактов
- результаты sandbox receipts
- trust signals издателя
- оценка совместимости (field coverage, auth coverage, webhook support)
→ итог: score 0..100 + причины.

---

## Что в пакете
- JSON Schemas: IOContract, TypeSystem, ConnectorCapability, AdapterSpec, MappingRule, ConversionPlan, ConversionJob, CompatibilityMatrix, CompatibilityScore, ContractValidationReport, TestVector, SchemaRegistry
- Specs: interoperability overview, contracts+types, adapters+mapping, conversion pipeline, scoring, cookbook Make↔n8n↔WP
- OpenAPI: Interop & Compat API (MVP)
- Examples: “News Digest Cluster” — контракт → адаптеры → план конвертации Make→n8n → compat score для sandbox/prod
- Python stubs: compat scorer, converter planner, adapter registry, contract validator
