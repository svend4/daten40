# IFOS 25201–25600 — Runtime & Execution OS: sandbox/prod запуск, профили окружений, secrets, лимиты, наблюдаемость, receipts, rollback/repair, scheduler, “one-click run” (v1)

Цель этого слоя: превратить “пакет функций” в **управляемое выполнение**:
- одинаково запускается на разных платформах (make/n8n/wp/custom)
- безопасно хранит secrets
- ограничивает side-effects (квоты/PII/домен-листы)
- собирает receipts (доказательства работы)
- умеет rollback/repair
- даёт “one-click run” для пользователя

Дальше — по порядку: от простого к сложному.

---

## 25201–25240 — RuntimeProfile: “где это запускается”

**RuntimeProfile** — конфигурация окружения, независимая от конкретной платформы:
- тип окружения: dev / sandbox / staging / prod
- платформа: make / n8n / wordpress / custom
- регион/tenant (если нужно)
- базовые ограничения: network allowlist, storage, compute time
- политика логирования (PII-safe)

Профиль — ключ к тому, чтобы один и тот же кластер не “разваливался” в разных местах.

---

## 25241–25280 — SecretRef: secrets как ссылочный тип, а не текст

Чтобы не было “ключей в README/скриптах”, вводим **SecretRef**:
- secret_ref: `secret://telegram/bot_token`
- scope: `workspace`, `profile`, `publisher`
- rotate_policy (период ротации)
- redaction_policy (что скрывать в логах)

Секреты подключаются к ExecutionPlan, но **никогда не сериализуются в открытом виде**.

---

## 25281–25320 — QuotaPolicy + SideEffectDeclaration: “что разрешено делать”

### QuotaPolicy
- rate limits (RPS, per-minute)
- daily quotas
- budget caps (по стоимости API)
- retry/backoff параметры

### SideEffectDeclaration
Каждый контракт/адаптер должен объявлять side-effects:
- external_call (HTTP)
- write_db
- send_message
- file_upload
- money_movement (если когда-нибудь появится)
- pii_processing (обработка персональных данных)

Зачем: чтобы sandbox и prod могли по-разному разрешать/блокировать действия.

---

## 25321–25370 — IdempotencyPolicy: “повторный запуск не ломает мир”

**IdempotencyPolicy** задаёт, как повторять безопасно:
- ключ идемпотентности (idempotency_key) вычисляется из inputs
- правила дедупликации
- safe-retry (что можно повторять, а что нельзя)

Это критично для “одной кнопки”: пользователь нажал дважды — мир не должен удвоиться.

---

## 25371–25430 — ExecutionPlan и ExecutionJob

### ExecutionPlan
План выполнения: “что сделать” и “в каком порядке”:
- шаги (steps), каждый шаг — adapter action
- необходимые secrets
- required profile constraints
- test mode (sandbox) vs live (prod)
- expected outputs (по контракту)

### ExecutionJob
Запуск плана:
- статус: queued/running/succeeded/failed/canceled
- timestamps
- логи, метрики, traces (ссылки)
- receipt ref

---

## 25431–25480 — SandboxSession: безопасный прогон

SandboxSession фиксирует:
- изоляцию side-effects (dry-run, stub endpoints)
- ограничения (allowlist доменов)
- test vectors (из Quality OS)
- результаты (receipts + logs)

Идея: любая “установка” сначала проходит sandbox.

---

## 25481–25530 — Receipts: доказательства выполнения

**Receipt** — цифровой чек выполнения:
- какие inputs использовались (в редактированном виде)
- какие outputs получились (в редактированном виде)
- какие шаги прошли/упали
- какие внешние вызовы были сделаны (домен/endpoint без secrets)
- duration, cost_estimate, retries
- hashes для верификации/attestation

Receipts связываются с Trust OS и Quality OS.

---

## 25531–25580 — Observability: logs/metrics/traces + alerts

**ObservabilityConfig** задаёт:
- уровень логирования
- no_log_fields (PII)
- sampling для trace
- метрики (latency, errors, throughput, cost)

События:
- LogEvent (строка/уровень/контекст)
- MetricEvent (метрика/значение)
- TraceSpan (время/родитель/атрибуты)

**AlertRule**:
- “errors > X% за 10 минут”
- “429 rate limit”
- “cost spike”

---

## 25581–25620 — HealthCheck + StateSnapshot

**HealthCheck** описывает, как проверить “живость”:
- ping endpoint
- verify token scopes
- read-only query
- check queue lag

**StateSnapshot** фиксирует состояние до/после:
- что было создано/изменено
- где хранятся артефакты
- чтобы было возможно rollback/repair

---

## 25621–25660 — RollbackPlan и RepairAction

### RollbackPlan
- список обратимых шагов
- стратегия (best-effort / strict)
- ограничения (что не откатить полностью)
- required permissions

### RepairAction
- “повторить шаг 3 с backoff”
- “сменить endpoint на резервный”
- “обновить secret token”
- “перейти в degraded mode”

Это превращает “сломалось” в “ремонтируется”.

---

## 25661–25600 — SchedulerJob и “One-click run”

**SchedulerJob**:
- cron/rrule
- профиль окружения
- execution plan ref
- политика уведомлений
- auto-rollback on fail?

**One-click run** = UI-кнопка, которая:
1) проверяет policy gate (Trust OS)
2) проверяет качество (L3+ для prod)
3) проверяет secrets + scopes
4) запускает sandbox (если нужно)
5) запускает prod job
6) показывает receipt + vitrine trust card

---

## Что в пакете
- JSON Schemas: RuntimeProfile, SecretRef, QuotaPolicy, SideEffectDeclaration, IdempotencyPolicy, ExecutionPlan, ExecutionJob, SandboxSession, Receipt, ExecutionReport, ObservabilityConfig, LogEvent, MetricEvent, TraceSpan, AlertRule, HealthCheck, StateSnapshot, RollbackPlan, RepairAction, SchedulerJob, SchemaRegistry
- Specs: runtime overview, secrets+quotas, receipts+observability, rollback+repair, one-click run
- OpenAPI: Runtime & Execution API (MVP)
- Examples: “News Digest Cluster” — sandbox → prod run → receipts → alerts → rollback
- Python stubs: runner, secret store, receipt emitter, observability, rollback manager, scheduler
