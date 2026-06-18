# IFOS 20401–20800 — Developer Experience & Runtime‑OS: SDK, шаблоны, локальная песочница, тест‑харнесс, one‑command publish, версии/миграции, observability, debug‑workflows (v1)

Если IFOS — это “операционка функций”, то без удобной разработки и отладки она утонет в хаосе:
- авторы будут публиковать “как получилось”,
- пользователи будут ставить “и оно не работает”,
- качество и доверие не поднимутся.

DX & Runtime‑OS вводит **стандартный цикл жизни ассета**:
1) создать (template),
2) запустить локально (sandbox),
3) протестировать (test harness + smoke),
4) наблюдать (logs/metrics/traces),
5) задебажить (debug sessions),
6) упаковать и опубликовать (one command publish),
7) мигрировать версии (migrations).

Ниже — по порядку: от простого к сложному.

---

## 20401–20450 — Шаблоны (простое)

### 20401) Template bundle = “заготовка, которая уже работает”
Template включает:
- минимальный workflow
- пример connector config
- permissions manifest
- пример secrets refs
- smoke checks

Цель: человек нажал “Create”, и у него **запускается** demo.

### 20430) Catalog templates by intent
Шаблоны должны быть по намерению (intent):
- “RSS → Digest → Telegram”
- “Compare offers → Score → Notify”
- “WordPress publish → SEO → Schedule”

Это ускоряет обучение сильнее, чем “документация на 200 страниц”.

---

## 20451–20520 — SDK & Contracts (среднее)

### 20451) SDK Manifest
SDK описывает:
- supported capabilities
- connector interfaces
- input/output schemas
- error taxonomy

SDK — это “внутренний стандарт”, чтобы ассеты были совместимы.

### 20490) Contract tests
Каждая capability имеет contract tests:
- schema validation
- idempotency (если важно)
- retry semantics
- timeout rules

---

## 20521–20600 — Runtime execution (среднее → сложное)

### 20521) Runtime job model
Каждый запуск = job:
- job_id
- subject (bundle/workflow)
- inputs
- status
- timestamps
- outputs references
- failure reason (structured)

### 20560) Deterministic execution mode
Для отладки нужен режим:
- фиксированные входы
- фиксированное окружение
- реплей (replay) по логам и trace

---

## 20601–20680 — Test Harness (сложно)

### 20601) Test plan
Test plan включает:
- unit checks (по шагам workflow)
- integration checks (коннекторы)
- end-to-end checks (полный сценарий)
- chaos checks (таймауты/ошибки сети)

### 20640) Smoke checks как паспорт работоспособности
Smoke checks — это минимальные тесты, которые обязаны проходить:
- “пинг” целевых доменов allowlist
- validate config
- dry-run на sample data
- assert output schema

Без smoke PASS — нельзя публиковать в marketplace (policy gate).

---

## 20681–20740 — Observability (самое полезное)

### 20681) Structured logs
Логи должны быть:
- JSON structured (не только текст)
- с correlation_id
- с step_id (какой узел упал)
- без секретов (PII/secrets redaction)

### 20710) Metrics snapshot
Метрики:
- latency per step
- success/fail rate
- retries
- external call counts
- cost estimates (LLM tokens)

### 20725) Traces (spans)
Tracing показывает цепочку:
ingest → parse → dedupe → summarize → deliver
Это “рентген” workflow.

---

## 20741–20800 — Debug sessions + Publish (самое сложное)

### 20741) Debug session
Debug session позволяет:
- остановиться на step
- посмотреть inputs/outputs (без секретов)
- изменить параметр и продолжить
- сделать replay

### 20770) Versioning & migrations
При обновлениях:
- schema evolves
- config keys меняются
- permissions могут ужесточиться
Миграции — это “патч‑скрипты” перехода config/state.

### 20790) One‑command publish
Команда publish делает:
- run tests + smoke
- run scans (из блока 19601–20000)
- build SBOM + sign
- generate listing metadata
- upload + create release
- produce installable artifact

---

## Что лежит в пакете
- JSON Schemas: SDK manifest, template bundle, runtime job, log event, metrics snapshot, trace span, debug session, migrations, test plan, smoke check, publish job
- Specs: SDK/DX, runtime execution, test harness, versioning/migrations, observability/debug, one-command publish
- OpenAPI: DX & Runtime API (MVP)
- Examples: “News Digest Cluster” (template + job + logs/metrics/traces + smoke + publish)
- Python skeletons: runner, logger, metrics, tracer, test harness, migration runner, publisher CLI stub
