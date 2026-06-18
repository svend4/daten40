# IFOS — Notifications, Alerts & Activity Feed (Блок 52801–53200)

Версия: v1 · Пакет: `IFOS_52801_53200_notifications_activity_feed_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

Даже если IFOS умеет «установить, связать и запустить» (marketplace + bundles + runtime), пользователь всё равно теряется без понятного канала обратной связи:
- что именно сейчас происходит (импорт, запуск макроса, сбор новостей)
- где ошибка и что с ней делать
- что требует внимания (креды, квоты, политика, деградация)
- какие действия доступны прямо из сообщения

Этот блок вводит единый стандарт уведомлений:
**in‑app notifications**, **activity feed**, **alerts**, **батчи и дедуп**, а также **пользовательские предпочтения** (что/куда/как часто).

## 1) Что делает (функции)

1) **Activity Feed** — лента событий системы (установки, запуск, импорт, публикация, модерация).
2) **Notifications** — уведомления пользователю/ролям (in‑app) с read/unread.
3) **Alerts** — приоритетные сообщения (severity: info/warn/error/critical) + баннеры.
4) **Actionable messages** — кнопки «исправить», «повторить», «открыть лог», «подать апелляцию».
5) **Dedup/Batch** — объединение однотипных событий, защита от спама.
6) **Preferences** — настройки подписок по типам событий (per user/per workspace).
7) **Templates** — шаблоны сообщений + локализация (ru/de/en).
8) **Delivery adapters (опционально)** — email/webhook/telegram/slack (через коннекторы).

## 2) Что НЕ делает (границы)

- Не является тикетингом/поддержкой: эскалация в case-management (42801–43200).
- Не заменяет observability: метрики/алерты инфраструктуры отдельно (34801–35200), тут — пользовательская витрина и маршрутизация.
- Не хранит секреты.

## 3) MVP (простое → среднее)

### 3.1 Модель данных (минимум)

**event** (сырьё):
- `event_id`
- `event_type` (enum)
- `subject_type` (connector|macro|bundle|vitrine|policy|run)
- `subject_id`
- `workspace_id`
- `actor_user_id` (кто инициировал)
- `ts`
- `payload` (json)

**notification** (то, что видит пользователь):
- `notification_id`
- `user_id`
- `workspace_id`
- `severity` (info|warn|error|critical)
- `title`
- `body_md`
- `actions[]` (label + url/command)
- `dedup_key` (опционально)
- `created_at`
- `read_at` (nullable)

**preference**:
- `pref_id`
- `user_id` / `workspace_id`
- `event_type`
- `channels` (in_app,email,webhook,...)
- `frequency` (immediate|hourly|daily)
- `enabled` (bool)

### 3.2 События (event_type) — базовый словарь

- `install.succeeded`, `install.failed`
- `run.started`, `run.succeeded`, `run.failed`
- `import.started`, `import.succeeded`, `import.failed`
- `publish.requested`, `publish.approved`, `publish.rejected`
- `policy.blocked`
- `quota.exceeded`
- `credentials.missing`

### 3.3 Правила маршрутизации: event → notification

Пайплайн:
1) событие попадает в `event_store`
2) `router` ищет подписчиков по preferences и ролям
3) применяет шаблон (templates)
4) применяет дедуп/батч
5) создаёт уведомления и публикует в real-time канал (SSE/WebSocket)

### 3.4 Dedup/Batch

MVP дедуп:
- `dedup_key = event_type + subject_id + user_id`
- окно дедупа: 10 минут
- если повтор — обновить существующее уведомление (счётчик `xN`).

MVP батч:
- ежедневный digest: собрать все info/warn в одну запись.

### 3.5 UI

Минимальные элементы:
- колокольчик (badge unread)
- панель уведомлений (drawer)
- activity feed (табличная лента событий)
- баннеры критических алертов сверху

## 4) Средний уровень (практика)

1) **Escalation**: критические ошибки → автоматически создать тикет (опционально).
2) **Run linking**: уведомление всегда содержит ссылку на run‑лог/trace.
3) **Smart actions**: «исправить креды», «увеличить квоту», «повторить запуск».
4) **Anti‑spam**: лимиты в минуту/час по user/workspace.

## 5) API (минимум)

- `GET  /notifications?unread=true`
- `POST /notifications/{id}/read`
- `GET  /activity?workspace_id=`
- `GET  /preferences` / `PUT /preferences`
- `GET  /templates` (read)
- `POST /events/emit` (внутренний)
- `GET  /stream/notifications` (SSE/WebSocket)

## 6) Зависимости

### Hard deps
- 35601–36000 `identity_profiles_os` (пользователи/роли)
- 36401–36800 `workspaces_orgs_os` (workspace)
- 38801–39200 `app_shell_navigation_os` (UI‑контекст, ссылки)

### Optional deps
- 34801–35200 `observability_reliability_os` (инфра‑алерты)
- 42801–43200 `case_management_ticketing_os` (эскалация в тикеты)
- 61601–62000 `enterprise_connectors_credential_vault_os` (actions «исправить креды»)
- 39601–40000 `pricing_quotas_resource_economy_os` (quota‑actions)
- 41601–42000 `localization_i18n_os` (локализация)

## 7) Чек‑лист

- [ ] Event store + enum event_type
- [ ] Router (preferences + role)
- [ ] Templates
- [ ] Notifications CRUD (read/unread)
- [ ] Activity feed
- [ ] Dedup + daily digest
- [ ] Real‑time stream (SSE)
