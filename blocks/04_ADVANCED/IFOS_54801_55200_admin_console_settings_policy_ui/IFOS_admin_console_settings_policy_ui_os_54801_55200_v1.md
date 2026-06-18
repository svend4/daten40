# IFOS — Admin Console: Settings, Roles & Policy UI (Блок 54801–55200)

Версия: v1 · Пакет: `IFOS_54801_55200_admin_console_settings_policy_ui_os_pack.zip` · Дата: 2026-01-02

## 0) Идея блока

IFOS не просто «маркетплейс + раннер». Чтобы реальный бизнес мог этим пользоваться, нужен **единый админ‑контур**, как в Word/Excel есть настройки/права/политики.

Этот блок задаёт **единый UI/UX и API‑контуры** для:
- **Workspace/Org Settings** (общие настройки)
- **Roles & Permissions UI** (назначение ролей, доступов)
- **Policy Management UI** (подключение/настройка policy‑packs и правил)
- **Change approvals** (минимальный контроль изменений)

Важно: блок не делает сам «движок политик» (он в 55201–55600), а делает **панель управления**, которая в дальнейшем подключается к engine.

## 1) Что делает

1) **Admin Navigation**: единые разделы админки и маршруты.
2) **Workspace Settings**: параметры воркспейса (локаль, часовой пояс, лимиты UI, брендинг).
3) **Role Assignment UI**: UI назначения ролей и приглашений пользователей.
4) **Permissions Matrix View**: матрица прав (видимость/доступ к операциям).
5) **Policy Packs UI**: подключить pack, включить правила, выбрать режим (audit/block).
6) **Policy Explanations**: UI показа «почему заблокировано» и ссылок на evidence.
7) **Approval Gates (MVP)**: отдельные типы изменений требуют подтверждения админа.
8) **Admin Audit Views**: быстрые ссылки на audit/events (если включены).

## 2) Что НЕ делает

- Не исполняет политики: это делает compliance policy engine.
- Не хранит секреты: это credential vault.
- Не является ERP/CRM: только управляет IFOS‑платформой.

## 3) MVP — от простого к среднему

### 3.1 Самый простой уровень (P0‑подмножество)

- Страница **Workspace Settings** (название, локаль, time‑zone, базовые лимиты)
- Страница **Users & Roles** (список пользователей, роль, приглашение)
- Страница **Policies** (список policy‑packs, включить/выключить)
- Страница **Audit/Events** (read‑only, если установлен audit block)

### 3.2 Средний уровень (P1)

- **Permissions Matrix**: наглядно, что может Admin/Editor/Viewer.
- **Policy modes**: audit-only vs block.
- **Scoped policies**: политика на workspace / project / connector / bundle.
- **Approval gates**: изменения policy, pricing, credentials требуют подтверждения.
- **Change log**: виджет последних админ‑изменений.

## 4) Модель данных (UI-контуры)

**admin_setting**:
- `workspace_id`
- `key`
- `value`
- `updated_at`
- `updated_by`

**role_binding**:
- `workspace_id`
- `user_id`
- `role` (admin/editor/viewer/billing/security)
- `created_at`

**policy_binding**:
- `workspace_id`
- `policy_pack_id`
- `enabled`
- `mode` (audit|block)
- `scope` (workspace|connector|bundle|vitrine)
- `scope_id` (nullable)
- `updated_by` / `updated_at`

**approval_request** (MVP):
- `request_id`
- `workspace_id`
- `change_type` (policy|pricing|credentials|connector_publish)
- `payload`
- `status` (pending|approved|rejected)
- `requested_by` / `approved_by`

## 5) UI маршруты

- `/admin/workspace/settings`
- `/admin/workspace/users`
- `/admin/workspace/roles`
- `/admin/workspace/permissions`
- `/admin/policies`
- `/admin/audit` (если установлен audit_log_event_bus)
- `/admin/approvals`

## 6) API (минимум)

- `GET/PUT /admin/settings`
- `GET/POST /admin/invitations`
- `GET/PUT /admin/roles`
- `GET       /admin/permissions/matrix`
- `GET/PUT   /admin/policies/bindings`
- `GET/POST  /admin/approvals`
- `POST      /admin/approvals/{id}/approve`
- `POST      /admin/approvals/{id}/reject`

## 7) Интеграции

### Подключение движков
- Policy UI вызывает engine (55201–55600), если установлен.
- Audit views читают из audit block (54401–54800), если установлен.
- Для предупреждений использует notifications (52801–53200).
- Для включения/выключения функций использует feature flags (51201–51600).

## 8) Зависимости

### Hard deps
- 35601–36000 `identity_profiles_os`
- 36401–36800 `workspaces_orgs_os`
- 38801–39200 `app_shell_navigation_os`

### Optional deps
- 54401–54800 `audit_log_event_bus`
- 55201–55600 `compliance_policy_engine_os`
- 52801–53200 `notifications_activity_feed`
- 51201–51600 `feature_flags_remote_config`

## 9) Чек‑лист

- [ ] Admin shell routes
- [ ] Settings CRUD + validation
- [ ] Users/Roles UI + invitations
- [ ] Permissions matrix view
- [ ] Policies bindings UI
- [ ] Approvals queue (MVP)
- [ ] Optional widgets: audit + notifications
