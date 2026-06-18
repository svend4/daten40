# IFOS Block 68801–69200: Observability & SRE (observability_sre)

## 1. Назначение блока
**Observability & SRE** — это “нервная система” IFOS.  
Если IFOS — операционная система функций интернета, то этот блок отвечает за:
- **видимость** того, что происходит (логи/метрики/трейсы/ивенты),
- **контроль качества и надёжности** (SLO/SLA/SLI, error budget),
- **обнаружение проблем** (алерты, аномалии, деградации),
- **управление инцидентами** (триаж, эскалация, статус‑страницы, постмортемы — интерфейсы),
- **автоматическое восстановление** (runbooks + workflow runner),
- и **прозрачность** для бизнеса: “почему медленно/почему упало/что делаем”.

Ключ: не создавать заново Prometheus/ELK/Grafana/Datadog, а дать IFOS **единый контракт**:
1) как собираем сигналы,  
2) как оцениваем SLO,  
3) как запускаем runbooks,  
4) как объясняем решения и SLA пользователю.

## 2. Почему это отдельный блок (а не “просто мониторинг”)
- Мониторинг часто ≠ наблюдаемость: мониторинг отвечает “упало/не упало”, а observability — “почему”.
- SRE добавляет дисциплину: **error budget**, приоритезацию, изменения через risk‑gate.
- В IFOS это нужно для:
  - marketplace (качество коннекторов/паков),
  - runtime (execution health),
  - витрин (UX без “дикого поля”),
  - доверия (trust/security) и enterprise governance.

## 3. Объекты наблюдаемости (what we observe)
Минимальный каталог “targets”:
- **Connector** (коннектор к SaaS/API)
- **Workflow / Macro** (сценарий, сборка)
- **Job / Run** (запуск, попытки, ретраи)
- **Package / Bundle** (установленный пакет, версия, зависимости)
- **Ingest Pipeline** (импорт/нормализация/модерация)
- **Search/Ranking** (поиск/витрины)
- **Auth/Identity** (логин, права)
- **Payments/Billing** (платежи, квоты)
- **UI/Console** (взаимодействия, ошибки фронта)

## 4. Канонические сигналы (Signals v1)
### 4.1 LogEvent (структурный лог)
```json
{
  "time": "2026-01-03T12:00:00Z",
  "level": "debug|info|warn|error",
  "service": "runtime|ingest|search|auth|billing|ui",
  "component": "connector_runner|macro_engine|dedup|policy_engine",
  "trace_id": "trc_...",
  "span_id": "spn_...",
  "tenant_id": "tnt_...",
  "workspace_id": "ws_...",
  "subject": {
    "type": "connector|workflow|job|bundle|user",
    "id": "..."
  },
  "msg": "human readable",
  "fields": {
    "http_status": 502,
    "latency_ms": 823,
    "retry": 1,
    "error_code": "UPSTREAM_TIMEOUT"
  }
}
```

### 4.2 MetricSample (числовой ряд)
```json
{
  "time": "2026-01-03T12:00:00Z",
  "name": "ifos.job.duration_ms",
  "value": 823,
  "labels": {
    "service": "runtime",
    "workflow": "wf_123",
    "connector": "ifos.connector.dhl",
    "tenant_id": "tnt_..."
  }
}
```

### 4.3 TraceSpan (распределённый трейс)
```json
{
  "trace_id": "trc_...",
  "span_id": "spn_...",
  "parent_span_id": "spn_parent",
  "name": "connector.call",
  "start_time": "2026-01-03T12:00:00Z",
  "end_time": "2026-01-03T12:00:00.823Z",
  "attributes": {
    "connector": "ifos.connector.dhl",
    "endpoint": "/track",
    "http_status": 200
  }
}
```

### 4.4 HealthEvent (событие здоровья)
Единый event‑слой для IFOS:
- `runtime.degraded`, `workflow.failed`, `connector.rate_limited`,
- `search.latency_high`, `auth.spike_failed_logins`, `billing.payment_failed`.

## 5. SLI/SLO/SLA: минимальная методология IFOS
### 5.1 SLI (индикаторы)
- **Availability**: доля успешных runs / API calls.
- **Latency**: p50/p95/p99.
- **Correctness**: % runs без ошибок данных (DQ).
- **Freshness**: задержка доставки событий/данных.
- **Coverage**: покрытие capability (для marketplace).

### 5.2 SLO (цели)
SLO задаются на уровень:
- сервисов (runtime, ingest),
- коннекторов (DHL, SAP),
- сценариев (blueprint pack),
- tenant‑уровня (enterprise).

Пример SLO:
- `runtime_runs_success_rate >= 99.5%` за 28 дней
- `p95_latency_ms <= 1500` для critical workflows
- `freshness_minutes <= 15` для новостей/ивентов

### 5.3 Error Budget
Если бюджет ошибок исчерпан — IFOS:
- ограничивает релизы (feature flags),
- повышает приоритет исправлений,
- предлагает “safe bundles” вместо экспериментальных.

## 6. Алерты (Alerting Policy)
### Типы алертов
- **Page** (ночной/срочный): критический outage.
- **Ticket**: важно, но можно в рабочее время.
- **Info**: наблюдение/тренд.

### Пороговые правила (пример)
- `availability < 99%` за 30 минут → Page
- `p95 latency > 2s` 15 минут → Ticket
- `error_rate spike > 3x baseline` → Ticket
- `rate_limit > threshold` → Info + рекомендация кеширования/ретраев

### Эскалация
- первичный oncall → backup → incident commander → owner сервиса.

## 7. Runbooks (авто-восстановление)
**Runbook** — это связка:
1) диагностика (что проверить),
2) действие (перезапуск, откат, переключение),
3) подтверждение (как понять, что стало лучше),
4) запись (audit trail).

В IFOS runbook выполняется через:
- `workflow_runner_macro_engine`,
- `feature_flags_remote_config`,
- `distribution_sync` (откат версий),
- `case_management_ticketing` (фиксация инцидента).

## 8. Дашборды (минимальный набор витрин)
1) **System Health Overview** (availability/latency/error budget).
2) **Connector Health** (успехи/ошибки/лимиты по каждому коннектору).
3) **Workflow Runs** (топ по ошибкам, ретраям, длительности).
4) **Ingest Health** (DQ errors, dedup conflicts, backlog).
5) **Tenant View** (enterprise‑разрез: кто страдает).

## 9. Интеграция с другими блоками IFOS
- Runtime execution: jobs/runs → метрики и трейсинг.
- Trust/Security: подозрительные события → алерты безопасности.
- Marketplace quality: рейтинг коннекторов учитывает SLO.
- Guided setup: мастер “проверь здоровье после установки”.
- Analytics: бизнес‑инсайты по SLA/стоимости простоя.

## 10. Минимальный план внедрения (от простого к сложному)
1) Структурные логи (LogEvent v1) для runtime + ingest.
2) Базовые метрики: success_rate, latency, retries.
3) Корреляция по trace_id (даже без полного tracing).
4) 5–10 SLO для P0 потоков.
5) Алерты (page/ticket/info) + эскалация.
6) Runbooks: перезапуск, откат, выключение фичи.
7) Дашборды + weekly reliability review.
8) Автоматический gate релизов по error budget.

## 11. Артефакты в пакете
- Seeds: signal types, SLO templates, alert rules, dashboards, runbooks.
- Manifest: зависимости и рекомендуемые связи.
