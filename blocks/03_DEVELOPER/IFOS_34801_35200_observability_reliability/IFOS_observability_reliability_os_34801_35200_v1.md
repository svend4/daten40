# IFOS 34801–35200 — Observability & Reliability OS (v1)
Цель: сделать IFOS **управляемым в продакшене**:
- наблюдаемость (логи/метрики/трейсы)
- health checks и диагностика
- SLO/SLA
- алерты и инциденты
- устойчивость (retry, circuit breaker, timeouts, rate limiting)
- rollout стратегии (канареечные релизы)
- автопочинка (autofix) + rollback

Порядок: простое → среднее → сложное.

---

## 34801–34850 — Structured Logging
### LogEvent
Единый формат логов:
- ts, level, msg
- tenant/org_unit/project
- run_id, canonical_id
- span_id/trace_id (если есть)
- meta (любой JSON)

Логи делятся на:
- system (ядро IFOS)
- bundle/runtime (выполнение)
- connector (внешние API)
- security (guard events)

---

## 34851–34910 — Metrics: счётчики, гистограммы, бюджеты
### Metric
Базовые метрики:
- run.count, run.success_rate
- latency.p50/p95/p99
- connector.error_rate
- policy.violations
- cost.eur (по cost center)

Метрики должны быть:
- тегируемыми (tenant, canonical_id, connector)
- агрегируемыми по времени

---

## 34911–34960 — Tracing: спаны и причинно‑следственная цепочка
### TraceSpan
Trace показывает:
- какой шаг “пакета” сколько занял
- где случилась ошибка
- какой внешний API тормозил

Это нужно, чтобы чинить не “вслепую”.

---

## 34961–35010 — Health Checks
### HealthCheck
Проверки:
- доступность коннекторов (ping/auth check)
- валидность секретов (не истёк ли токен)
- доступность storage
- readiness/ liveness

HealthCheck результаты пишутся в метрики и алерты.

---

## 35011–35060 — SLO & SLA
### SLO
SLO (цель надежности) — внутренние цели:
- success_rate ≥ 99.0%
- p95 latency ≤ 2s
- error_budget ≤ X

### SLA
SLA — внешние обещания клиенту:
- 99.9% uptime
- max incident response time

SLO → алерты → инциденты → пост‑мортем.

---

## 35061–35110 — Alerts & Incidents
### AlertRule
- условие: metric threshold, anomaly
- severity: warn/high/critical
- routing: oncall group / slack / email / ticket
- suppression (не спамить)

### ReliabilityIncident
- открытие по алерту
- статусы: open/mitigated/closed
- таймлайн событий
- действия и выводы

---

## 35111–35160 — Reliability Patterns
### RetryPolicy
- max_attempts
- backoff (exp/jitter)
- retry_on (код/ошибка)
- idempotency_key

### CircuitBreaker
- open/half-open/closed
- threshold ошибок
- cool-down
- fallback режим

Это критично для интернет‑интеграций (API нестабильны).

---

## 35161–35190 — Rollback & Canary
### CanaryRelease
- rollout_percent по времени
- мониторинг метрик во время релиза
- авто‑откат при деградации

### RollbackPlan
- версия “последняя стабильная”
- миграции данных (если есть)
- шаги “откатить/почистить/вернуть”

---

## 35191–35200 — Autofix (автопочинка)
### AutofixRule
- trigger: alert/guard event
- action: rotate secret, switch connector endpoint, fallback bundle, restart worker, disable risky bundle
- max_frequency (чтобы не зациклиться)

Autofix всегда пишет Audit + Incident note.

---

## Что дальше
Следующий блок:
**35201–35600 — Knowledge Graph & Semantic OS** (онтология функций, связи, эмбеддинги, “похожее”, генерация кластеров, объяснимость, Q/A по каталогу).  
Скажете “Продолжение” — сделаю.
