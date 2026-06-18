# IFOS — Audit Log, Immutable Events & Event Bus (Блок 54401–54800)

Версия: v1 · Пакет: `IFOS_54401_54800_audit_log_event_bus_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

IFOS строится вокруг «установить/настроить/запустить» и вокруг решений, которые влияют на данные, деньги и безопасность. Чтобы система была пригодна для бизнеса и гос/enterprise, нужно доказуемое и воспроизводимое понимание:
- кто и когда сделал действие
- что именно изменилось (включая конфиги, флаги, политики)
- почему действие было разрешено/запрещено
- как восстановить историю и расследовать инцидент

Этот блок вводит:
**Audit Log** (читабельный журнал), **Immutable Event Store** (неизменяемые события), и **Event Bus** (шина событий для остальных блоков).

## 1) Что делает (функции)

1) **Audit Log**: человеко‑читаемые записи действий (actor → action → target → result).
2) **Immutable Events**: append‑only события с хеш‑цепочкой (tamper‑evident).
3) **Event Bus**: публикация событий для подписчиков (notifications, analytics, security, billing).
4) **Correlation IDs**: связывает цепочку действий (request_id/run_id).
5) **Retention/Export**: хранение по правилам и экспорт (CSV/JSON).
6) **Query**: фильтрация по типу, actor, workspace, target, времени.
7) **Policy Evidence**: фиксирует, какой policy‑pack сработал.

## 2) Что НЕ делает (границы)

- Не является SIEM: интеграция через экспорт/стрим в внешние системы.
- Не является хранением данных домена (это data_os): хранит только события/аудит.
- Не заменяет security controls: только доказательная база.

## 3) MVP (простое → среднее)

### 3.1 Audit Record (читабельный журнал)

Поля:
- `audit_id`
- `ts`
- `workspace_id`
- `actor_user_id` + `actor_role`
- `action` (enum)
- `target_type` + `target_id`
- `result` (allowed|denied|failed|succeeded)
- `reason` (policy_reason/error_summary)
- `correlation_id` (request/run)
- `metadata` (json)

### 3.2 Immutable Event Store (append‑only)

Модель:
- `event_id`
- `ts`
- `event_type`
- `payload`
- `prev_hash`
- `hash`

Хеш‑цепочка делает подмену заметной: если кто-то изменил старое событие, цепочка не сойдётся.

### 3.3 Event Bus (publish/subscribe)

MVP варианты реализации:
1) DB outbox table + polling worker
2) Redis streams
3) Kafka/NATS (enterprise)

Контракт:
- `topic` = `event_type` или `domain.*`
- подписчик подтверждает обработку (ack)

### 3.4 Корреляция и трассировка

Каждый HTTP запрос получает `correlation_id`.
Run‑движок присваивает `run_id` и вкладывает его в события.
Так можно собрать историю: install → policy → run → notify → billing.

## 4) Средний уровень (практика)

1) **Role-based visibility**: кто может видеть чей audit.
2) **Redaction**: маскировать PII/секреты в payload.
3) **Export jobs**: расписание выгрузок и подпись.
4) **Integrity check**: периодическая проверка hash-chain.

## 5) API (минимум)

- `GET  /audit?workspace_id=&from=&to=&action=&target=`
- `GET  /events?from=&to=&type=`
- `POST /events/publish` (internal)
- `GET  /events/stream` (SSE/WebSocket)
- `POST /exports/audit` (job)
- `GET  /exports/{job_id}`

## 6) Зависимости

### Hard deps
- 35601–36000 `identity_profiles_os`
- 36401–36800 `workspaces_orgs_os`
- 55201–55600 `compliance_policy_engine_os` (evidence)

### Optional deps
- 52801–53200 `notifications_activity_feed` (подписчик)
- 56001–56400 `analytics_insights_os` (подписчик)
- 42001–42400 `payments_settlement_os` / 32401–32800 billing (события денег)
- 34801–35200 `observability_reliability_os` (стрим в инфру)

## 7) Чек‑лист

- [ ] Audit log write middleware
- [ ] Event store append + hash chain
- [ ] Event bus (outbox + worker)
- [ ] Query + filters
- [ ] Export job
- [ ] Integrity check
