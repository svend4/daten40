# IFOS Block 70401–70800: SLO/SLI, Error Budgets & Reliability Gates
**Slug:** `slo_sli_error_budgets`  
**Category:** Observability & Reliability  
**Priority:** P1  
**Status:** MVP Spec + Seeds (v1)

## 1) Идея блока (зачем он нужен)
Этот блок делает надёжность **измеримой и управляемой**:

- **SLI** (Service Level Indicator) — измеряемая метрика качества (например p95 latency, error rate).
- **SLO** (Service Level Objective) — целевое значение SLI за период (например 99.9% успеха за 30 дней).
- **Error Budget** — допустимая “квота на ошибки”: сколько можно “потратить” на сбои/деградации.
- **Reliability Gates** — правила, которые останавливают или ограничивают релизы, если бюджет выгорает или SLO нарушен.

Для IFOS это критично, потому что система — “операционка функций”:
- коннекторы зависят от внешних API,
- ingestion/ETL могут создавать лавины ошибок,
- runtime/workflow должен быть стабильным,
- UI и marketplace должны быть быстрыми,
- поиск/ранжирование и RAG часто тяжёлые и подвержены деградации.

---

## 2) Что блок делает (основные функции)
### 2.1. Каталог SLO по доменам (SLO Catalog)
- шаблоны SLO для доменов IFOS: search, runtime, connectors, marketplace, ingest, KB/RAG, UI
- связывание SLO с владельцем (owner), критичностью и потребителями

### 2.2. Определение SLI (SLI Definitions)
- формулы SLI (из метрик/логов/трейсов)
- стандартизированные окна расчёта: 5m/1h/1d, rolling 7d/30d
- классификация ошибок: user-visible vs internal; retryable vs fatal

### 2.3. Расчёт и ведение Error Budgets
- бюджеты на период (например 30 дней) и на “релизное окно”
- разложение бюджета по типам деградации: availability, latency, correctness
- хранение “burn rate” (скорость сгорания) и прогноз: “через N часов бюджет выгорит”

### 2.4. Reliability Gates (ворота надёжности)
- **release gate**: нельзя катить релиз, если:
  - burn rate > порога,
  - SLO нарушен,
  - есть активные critical incidents,
  - отсутствует зелёный baseline/perf тест
- **progressive delivery**: canary + авто-rollback при нарушении SLO
- интеграция с feature flags и change control

### 2.5. Автоматические действия при выгорании бюджета (Policy Actions)
- freeze релизов / только hotfix
- ограничение нагрузок / деградация функций (graceful degradation)
- принудительный postmortem и action items
- усиление мониторинга/алертинга

---

## 3) Минимальные сущности данных
### 3.1. SLODefinition
- `id`, `domain`, `service_slug`, `owner_team`, `criticality`
- `sli_id`, `objective` (например 99.9%), `window` (7d/30d)
- `filters` (tenant, route, region), `labels/tags`
- `error_budget_policy_id`

### 3.2. SLIDefinition
- `id`, `name`, `kind` (availability|latency|correctness|freshness)
- `query` (PromQL/SQL/OTel), `aggregation` (p95/p99/avg)
- `good_event`, `bad_event` definition
- `data_sources` (metrics/logs/traces)

### 3.3. ErrorBudgetState
- `slo_id`, `window_start`, `window_end`
- `budget_total`, `budget_remaining`, `budget_burn_rate`
- `forecast_exhaustion_at`, `status` (ok|warning|exhausted)

### 3.4. ReliabilityGate
- `id`, `name`, `scope` (release|deployment|feature_flag|tenant)
- `conditions` (burn_rate threshold, active incidents, perf regressions)
- `actions` (block, warn, require_approval, rollback, degrade)

### 3.5. PolicyActionLog
- `id`, `policy_id`, `trigger`, `time`, `action_taken`, `artifact_links`

---

## 4) Практические SLO (примерный набор для IFOS)
### Search / Ranking
- Availability: **99.9%** успешных ответов / 30d
- Latency: p95 < 500ms (UI), p99 < 1.5s (heavy queries)

### Runtime / Workflow Runner
- Job success rate: **>= 99%** / 7d
- Queue backlog clears < 60m (steady state)

### Connectors
- Connector request success: **>= 99%** (учитывая retry policy)
- Rate-limit handling: 429 без “падений”, graceful backoff

### Ingestion / ETL
- No data loss SLO: 0 критических потерь за 30d
- Freshness: 95% объектов доступны в поиске < X минут после ingest

### KB/RAG
- Timeout rate < 1%
- p95 latency < 2s (interactive)

### UI / Marketplace
- p95 page API latency < 800ms, error rate < 1%

---

## 5) MVP API
- `POST /reliability/sli` (define SLI)
- `POST /reliability/slo` (create SLO)
- `GET /reliability/slo?domain=&service=`
- `GET /reliability/budgets?slo_id=`
- `POST /reliability/gates`
- `POST /reliability/gates/evaluate` (input: release_ref → output: PASS/FAIL + reasons)
- `GET /reliability/incidents/active` (integration pointer)

---

## 6) UI
- **SLO Catalog**: список SLO, фильтры, критичность, владельцы
- **Budget View**: remaining, burn rate, прогноз выгорания
- **Gate Status**: “можно релизить?” + причины + ссылки на дашборды
- **Reliability Playbook shortcuts**: быстрые кнопки (freeze, rollback, degrade)

---

## 7) MVP vs позже
### MVP (в этом блоке)
- каталог SLI/SLO + расчёт бюджета + burn rate
- ручное включение gate при релизе (CI/CD step)
- алерт: burn rate > X, budget_remaining < Y%

### Later
- авто-генерация SLO из реального поведения + критичности функций
- multi-tenant budgets (по клиентам/тенантам)
- “функциональные бюджеты” (по макросам/пакетам/коннекторам)
- автоматическая деградация функций (dynamic policies)

---

## 8) Безопасность и гигиена
- единые определения “что считать ошибкой”
- корректная маскировка PII при анализе логов
- аудит решений gate и override
- обязательный postmortem при выгорании бюджета в критичном домене
