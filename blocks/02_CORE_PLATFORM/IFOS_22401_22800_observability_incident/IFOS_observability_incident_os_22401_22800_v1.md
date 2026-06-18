# IFOS 22401–22800 — Observability & Incident‑OS: логи/метрики/трейсы, алерты, SLO, инциденты, постмортемы, авто‑деградация и фоллбек (v1)

В предыдущем блоке (22001–22400) мы сделали “установку как макрос”: install plan, sandbox, smoke-tests, rollback.
Но в реальной жизни всё ломается уже **после** установки: API отваливается, лимиты, обновления, ключи, сеть, перегрузки.
Поэтому следующий слой IFOS — **наблюдаемость и инцидент‑контур**, как у “взрослых” SaaS/DevOps, но адаптированный под no‑code и “пакеты функций”.

Ниже — по порядку: от простого (лог) к сложному (SLO/инциденты/авто‑фоллбек).

---

## 22401–22460 — Единый лог‑сигнал: LogEvent (простое)

### 22401) LogEvent = минимальный атом правды
Каждое действие в IFOS (install step, run step, webhook, task, agent) пишет LogEvent:
- кто: `subject_id` (asset/bundle/node)
- где: `platform` (make/n8n/wp/local)
- что: `event_type` (run_started/run_failed/secret_invalid/...)
- когда: `ts`
- контекст: `trace_id`, `request_id`, `job_id`
- безопасная полезная нагрузка: `data` (с редактированием PII)

**Цель:** “всё объяснимо” и “всё воспроизводимо”.

---

## 22461–22520 — Метрики: MetricPoint (среднее)

### 22461) MetricPoint = измерение
Примеры метрик:
- `runs_total`, `runs_failed_total`
- `latency_ms_p95`
- `cost_eur_daily`
- `queue_depth`
- `webhook_success_ratio`

Каждая метрика имеет:
- имя, значение, unit
- labels (platform, asset_id, bundle_id, region)
- timestamp

---

## 22521–22580 — Трейсы: TraceSpan (среднее → сложное)

### 22521) TraceSpan = цепочка причин
В no‑code обычно непонятно “почему не пришло сообщение”.
TraceSpan показывает путь:
RSS fetch → summarize → telegram send.
Даже если это Make/n8n/WP, мы “оборачиваем” шаги в span’ы с:
- span_id, parent_span_id
- duration_ms
- status + error_code
- attributes

---

## 22581–22640 — Дашборды и алерты (сложное)

### 22581) Dashboard
Дашборд — сохранённый набор графиков/таблиц:
- “здоровье кластера”
- “топ инцидентов за неделю”
- “стоимость по провайдерам”

### 22610) AlertRule
Алерт — это правило:
- условие (например, fail_ratio > 5% за 10 минут)
- severity (P1/P2/P3)
- routing (куда сообщить)
- suppression (не спамить)
- runbook link (что делать)

---

## 22641–22710 — SLO (уровень сервиса) и бюджет ошибок (очень важно)

### 22641) SLO
SLO = обещание качества:
- Availability: 99.0% в месяц
- Freshness: дайджест не старше 30 минут
- Delivery: доставка сообщений ≥ 98%

SLO связывается с метриками и алертами.
Если “ошибочный бюджет” исчерпан — IFOS запрещает “рискованные обновления” и включает безопасные профили.

---

## 22711–22770 — Инциденты и таймлайн (максимальная практичность)

### 22711) IncidentRecord
Инцидент = объект управления:
- impact (кого затронуло)
- root cause (позже)
- current status (open/mitigated/resolved)
- owner/oncall (кто отвечает)
- links: logs/traces/alerts

### 22740) Timeline
Каждое действие фиксируется:
- “22:10 алерт P1 сработал”
- “22:12 включили dry-run”
- “22:18 переключили на fallback n8n”

---

## 22771–22800 — Постмортем + авто‑фоллбек/деградация (самый высокий уровень)

### 22771) Postmortem
Постмортем нужен, чтобы интернет стал “не диким”, а обучающимся:
- что произошло
- почему
- что сделали
- что исправим в продукте/пакете/политиках
- какие проверки добавим в install/sandbox

### 22785) FallbackPolicy + DegradationAction
Когда сервис ломается — IFOS делает не “паника”, а “мягкая деградация”:
- перейти на альтернативный вариант (Make → n8n)
- переключиться в offline queue (сохранить и отправить позже)
- включить “dry-run” и только логировать
- уменьшить частоту (каждые 60 минут вместо 10)

**Это и есть “макрос‑уровень операционки”: управляемое качество.**

---

## Что в пакете
- JSON Schemas: LogEvent, MetricPoint, TraceSpan, Dashboard, AlertRule, NotificationChannel, SLO, IncidentRecord, Timeline, Postmortem, Runbook, FallbackPolicy, DegradationAction, RedactionRule
- Specs: signals, alerting+SLO, incident response, postmortem learning, auto-fallback/degradation, privacy redaction
- OpenAPI: Observability & Incident API (MVP)
- Examples: “News Digest Cluster” — метрики, лог‑события, trace, алерт, инцидент, постмортем, фоллбек Make→n8n
- Python stubs: collector, metrics, alert evaluator, incident manager, fallback orchestrator
