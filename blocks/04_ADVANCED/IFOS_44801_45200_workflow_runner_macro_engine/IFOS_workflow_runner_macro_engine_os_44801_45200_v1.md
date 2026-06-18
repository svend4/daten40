# IFOS 44801–45200 — Workflow Runner & Macro Engine OS (v1)
Цель: выполнить “макрос” или “шаблон” **как продукт**:
- безопасно (secrets, sandbox, approval gates)
- надёжно (retries, idempotency, rollback)
- наблюдаемо (logs, traces, artifacts)
- масштабируемо (quotas, scheduling)
- совместимо с Make/n8n/Node‑RED и собственными коннекторами

Порядок: простое → среднее → сложное.

---

## 44801–44840 — Run: минимальная сущность исполнения
Два типа запуска:
- **MacroRun** — выполнение Macro (из 44401–44800)
- **WorkflowRun** — выполнение WorkflowTemplate (Make/n8n/Node‑RED/custom)

Каждый Run хранит:
- input params
- состояние (queued/running/done/error)
- ссылки на логи, артефакты, цитирования
- бюджет/квоты (время/запросы/стоимость)

---

## 44841–44910 — DAG и Tasks: как устроен макрос внутри
**DAG** (Directed Acyclic Graph) — граф задач:
- узлы: Task
- связи: зависимости
- каждый Task — атомарная операция (fetch, normalize, compare, publish)

Task должен быть:
- идемпотентным (или иметь idempotency key)
- уметь работать в sandbox
- иметь таймауты и лимиты

---

## 44911–44960 — Connectors: “драйверы интернета”
Это ваш ключевой тезис: приложения = “слова словаря”.
**ConnectorContract** определяет:
- какие входы/выходы (schemas)
- auth методы
- rate limits
- поддерживаемые операции
- ошибки и коды

Коннекторы можно:
- оборачивать вокруг REST/GraphQL
- генерировать из OpenAPI
- делать как плагины

---

## 44961–45000 — Secrets: безопасные ключи и OAuth
**Secret**:
- хранится в vault (KMS/HashiCorp Vault/Cloud KMS)
- не попадает в логи
- доступ выдаётся только конкретному Run/Task
- ротация

Sandbox режим:
- test keys
- mock endpoints
- “dry run” (без побочных эффектов)

---

## 45001–45040 — Retry & Idempotency: чтобы не ломалось
**RetryPolicy**:
- backoff (exponential)
- max attempts
- retry only on transient errors

Idempotency:
- idempotency_key per task
- dedup of “already executed”
- safe повторный запуск

Это превращает “интернет-автоматизацию” в инженерную систему.

---

## 45041–45080 — Rollback: откат и компенсации
Не всё можно откатить (email уже ушёл).
**RollbackPlan**:
- компенсационные действия (например, “send correction email”)
- удаление временных файлов
- отключение webhook
- пометка “invalid result”

Rollback — обязательный слой для B2B.

---

## 45081–45120 — Approvals & Risk Controls: контроль риска
**ApprovalGate**:
- правила: если PII, деньги, массовая рассылка → нужен approve
- роли: user/team/admin
- журнал действий (audit)

Это важнейшая часть доверия и compliance.

---

## 45121–45160 — Scheduling & Triggers: расписания и события
**Schedule**:
- cron/rrule
- event triggers (webhook, new item, threshold)

Runner должен поддерживать:
- очередь
- priority
- concurrency limits
- rate limits per connector

---

## 45161–45190 — Logs, Traces, Artifacts: наблюдаемость
**RunLog**:
- события (start/stop/step)
- ошибки (structured)
- метрики (latency, retries)

**RunArtifact**:
- результаты (файлы, ссылки, отчёты)
- промежуточные данные (snapshots)
- подписанные хеши

---

## 45191–45200 — Quotas & Cost Controls: экономика выполнения
**Quota**:
- per user/team/tenant
- per connector
- per time window

Cost controls:
- stop‑loss (ограничение затрат)
- budgets per run
- “preview cost” перед запуском

---

## Итог
Этот блок отвечает на “почему интернет — дикое поле”:
- потому что нет общего **исполнителя** (runner) и стандартных “драйверов” (connectors)
- нет sandbox, retries, approvals, rollback
- нет единых артефактов и логов

Macro Engine делает “миллионы решений” **запускаемыми и надёжными**.

---

## Что дальше
Следующий блок:
**45201–45600 — Connectors Factory & SDK OS** (генерация коннекторов из OpenAPI, тесты, mocks, docs, marketplace publishing).  
Скажете “Продолжение” — сделаю.
