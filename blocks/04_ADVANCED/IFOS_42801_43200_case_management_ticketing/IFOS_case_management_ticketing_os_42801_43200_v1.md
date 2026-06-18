# IFOS — Case Management & Ticketing Engine (Блок 42801–43200)

Версия: v1 · Пакет: `IFOS_42801_43200_case_management_ticketing_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

Этот блок закрывает «дыру операционной реальности»: когда в системе появляются **покупки, установки, отзывы, жалобы, споры и вопросы пользователей**, должна быть единая механика:
- **обращение → тикет → диалог → решение → закрытие**
- SLA/эскалации
- привязка к workspace/тенанту
- доказательства (вложения), аудит и итоговый статус

Без тикетов любая платформа (маркетплейс/автоматизация/витрины) превращается в хаотичный чат.
Этот блок делает поддержку и споры **структурируемыми и измеримыми**.

## 1) Что делает (функции)

1) **Case** (дело) как контейнер (например «спор по оплате», «инцидент безопасности», «ошибка коннектора»).
2) **Ticket** (заявка) как поток общения и действий внутри case.
3) Сообщения/комментарии, внутренние заметки, вложения.
4) Статусы и жизненный цикл (state machine).
5) SLA: целевые сроки реакции/решения + эскалации.
6) Связи с объектами IFOS: macro/run, connector, bundle, payment, review.

## 2) Что НЕ делает (границы)

- Полный «customer support процесс» (скрипты, политики, арбитраж) — это блок **42401–42800**.
- Платёжный движок и возвраты — блоки payments/settlement.
- Аналитика и BI по поддержке — блок **56001–56400** (можно интегрировать события).
- Коммуникация по email/SMS/мессенджерам — отдельные коннекторы/уведомления (здесь только события/шаблоны).

## 3) MVP (простое → среднее)

### Шаг 3.1 — Сущности и минимальные поля

**case**:
- `case_id` (uuid)
- `workspace_id`
- `type` (support|dispute|incident|abuse|billing)
- `severity` (low|medium|high|critical)
- `subject`, `description`
- `status` (open|triage|in_progress|waiting_user|resolved|closed)
- `created_by_user_id`
- `assignee_user_id` (может быть null)
- `created_at`, `updated_at`

**ticket** (опционально как отдельная таблица):
- `ticket_id`
- `case_id`
- `channel` (web|api|import)
- `status` (open|pending|solved)
- `created_at`

**message**:
- `message_id`
- `case_id`
- `author_type` (user|agent|staff|system)
- `author_id` (user_id или staff_id)
- `body` (markdown)
- `visibility` (public|internal)
- `created_at`

**attachment**:
- `attachment_id`, `case_id`, `uploader_id`
- `filename`, `mime`, `size`
- `storage_url` (или key)
- `created_at`

### Шаг 3.2 — Привязка к объектам IFOS (links)

Добавить таблицу `case_link`:
- `case_id`
- `object_type` (connector|macro|workflow_run|bundle|payment|review|vitrine)
- `object_id`
- `note`

Цель: оператор поддержки сразу видит контекст.

### Шаг 3.3 — Минимальный API

- `POST /cases` создать дело
- `GET /cases?workspace_id=...` список дел
- `GET /cases/{id}` детали
- `PATCH /cases/{id}` изменить статус/приоритет/назначить исполнителя
- `POST /cases/{id}/messages` добавить сообщение
- `POST /cases/{id}/attachments` загрузить вложение
- `POST /cases/{id}/links` привязать объект IFOS

### Шаг 3.4 — Минимальная автоматика (правила триажа)

Простейшие правила:
- если `type=incident` и `severity=critical` → статус `triage` + уведомить on-call
- если сообщение содержит ключевые слова «refund/chargeback» → `type=billing` + tag `payment`
- если case связан с connector → предложить авто-диагностику (link на observability/logs)

## 4) Средний уровень: SLA, эскалации, шаблоны ответов

### Шаг 4.1 — SLA политики

Сущность `sla_policy`:
- `policy_id`, `name`
- `applies_to` (case_type, severity, plan)
- `first_response_minutes`
- `resolution_minutes`
- `business_hours` (true/false)

Сущность `sla_clock` (на case):
- `case_id`
- `first_response_due_at`
- `resolution_due_at`
- `breach_flags`

### Шаг 4.2 — Эскалации

Сущность `escalation_rule`:
- `when` (before_due|after_breach)
- `target` (group|user|webhook)
- `action` (notify|reassign|priority_up)

MVP: 2 уровня — team lead и on-call.

### Шаг 4.3 — Макросы поддержки (canned responses)

Сущность `support_macro`:
- `macro_id`, `workspace_id`, `title`
- `template_body` (markdown + переменные)
- `tags` (refund, billing, connector, troubleshooting)

Это ускоряет поддержку и делает ответы единообразными.

## 5) Ближе к сложному: агентная помощь и доказуемость

### Шаг 5.1 — AI Copilot для тикетов
- суммаризация переписки
- предложение следующего шага
- авто-черновики ответов

### Шаг 5.2 — Доказуемость (provenance)
- хэш вложений
- запись ключевых событий в audit log
- неизменяемые системные сообщения (system notes)

## 6) События (для наблюдаемости и аналитики)

- case_created
- case_assigned
- case_status_changed
- message_added (public/internal)
- sla_breach_first_response / sla_breach_resolution
- escalation_triggered

## 7) Зависимости

### Hard deps
- 35601–36000 `identity_profiles`
- 36401–36800 `workspaces_orgs`

### Optional deps
- 34801–35200 `observability_reliability` (ссылки на логи/трейсы)
- 41201–41600 `data_privacy_compliance` (GDPR/ретеншн вложений)
- 42401–42800 `customer_support_disputes` (процессы и политики)
- 52401–52800 `ai_copilot` (AI помощь)

## 8) Чек-лист готовности

- [ ] case CRUD
- [ ] сообщения (public/internal)
- [ ] вложения
- [ ] links к объектам IFOS
- [ ] базовые статусы и переходы
- [ ] SLA policy + часы
- [ ] эскалации (хотя бы notify)
- [ ] support macros (шаблоны ответов)
