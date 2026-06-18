# IFOS — Workspaces & Organizations (Блок 36401–36800)

Версия: v1 · Пакет: `IFOS_36401_36800_workspaces_orgs_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок (идея и роль)

Этот блок вводит **простую модель «рабочего пространства» (workspace)**, чтобы IFOS перестал быть набором разрозненных функций и стал **системой, где всё принадлежит контексту**: пользователю, команде, организации.

Если `Identity & Profiles (35601–36000)` отвечает на вопрос **«кто ты?»**, то Workspaces отвечают на вопросы:
- **«в каком контексте ты работаешь?»** (личный, команда, клиент, проект)
- **«кому принадлежит объект?»** (витрина/макрос/пакет/коннектор/документ)
- **«какие права внутри этой команды?»** (owner/admin/member/viewer)

Без Workspaces невозможен нормальный **B2B**: нельзя безопасно поделиться шаблонами, макросами, коннекторами и витринами между людьми.

## 1) Что появится после внедрения

1) Workspace как контейнер объектов (projects/automations/connectors/knowledge/vitrines).
2) Роли и членство: owner/admin/member/viewer/billing.
3) Приглашения и онбординг команды.
4) Политики доступа «объект принадлежит workspace».
5) Аудит ключевых событий (создание workspace, приглашения, смена ролей).
6) Базовые лимиты/квоты на уровне workspace (опционально).

## 2) Границы блока (что НЕ входит сюда)

- Полноценная федерация/мульти-аренда между дата-центрами/облаками (**39201–39600**).
- Продвинутые enterprise IAM вещи (SSO/SCIM) — это **36001–36400**.
- Платёжная логика биллинга (инвойсы/подписки) — это блоки маркетплейса/settlement.
- Сложная орг-структура (departments, cost centers) — позже, если понадобится.

## 3) MVP (простое → среднее): минимальная модель workspaces

### Шаг 3.1 — Сущности и таблицы (самый простой вариант)

**Сущности:**
- `workspace`
- `workspace_member`
- `workspace_invite`

**workspace** (минимум):
- `id` (uuid)
- `name`
- `slug` (человекочитаемый идентификатор)
- `type` (personal|team|client)
- `owner_user_id`
- `created_at`, `updated_at`, `status`

**workspace_member**:
- `workspace_id`
- `user_id`
- `role` (owner/admin/member/viewer/billing)
- `joined_at`

**workspace_invite**:
- `workspace_id`
- `email`
- `role`
- `token` (one-time)
- `expires_at`
- `status` (pending|accepted|revoked|expired)

### Шаг 3.2 — Правило владения объектами (ключевой принцип)

Любой объект IFOS должен иметь поле `workspace_id` (или ссылку на него через owner).
Примеры:
- `connector.workspace_id`
- `macro.workspace_id`
- `knowledge_pack.workspace_id`
- `vitrine.workspace_id`

Это «скелет» для интеграции тысяч функций: без этого всё превращается в хаос.

### Шаг 3.3 — Минимальные API методы

- `POST /workspaces` создать workspace
- `GET /workspaces` список доступных workspace
- `GET /workspaces/{id}` детали
- `PATCH /workspaces/{id}` обновить (name, avatar, settings)
- `POST /workspaces/{id}/invites` пригласить по email
- `POST /workspaces/invites/{token}/accept` принять приглашение
- `PATCH /workspaces/{id}/members/{user_id}` сменить роль
- `DELETE /workspaces/{id}/members/{user_id}` удалить участника

## 4) Средний уровень: настройки workspace, разделение ролей, политики

### Шаг 4.1 — Настройки и профили workspace

Добавить `workspace_settings` (или JSON-поле):
- `default_visibility` (private|org|public)
- `allowed_domains` (для авто-приглашений)
- `locale`, `timezone`
- `content_policy` (строгость модерации UGC)

### Шаг 4.2 — Модель ролей и разрешений внутри workspace

RBAC в 2 слоя:
1) глобальные роли (admin платформы) — из блока 35601–36000
2) **workspace роли** (owner/admin/member/viewer/billing) — из этого блока

Пример:
- owner: всё + удаление workspace
- admin: управление участниками + настройки
- member: создавать/редактировать объекты внутри workspace
- viewer: только чтение
- billing: доступ к оплате/планам (если включены)

### Шаг 4.3 — Политики доступа (минимальный ABAC)

Правило доступа формулируется так:
- пользователь имеет членство в workspace → доступ к объектам с `workspace_id`.
- дополнительно проверяем роль и действие: read/write/manage.

Минимальная функция-проверка (псевдо):
- `can(user, action, object) = member_of(user, object.workspace_id) AND role_allows(role, action)`.

## 5) Более сложные сценарии (переход к enterprise)

### Шаг 5.1 — Связка с Enterprise IAM (SSO/SCIM)

Когда подключается блок 36001–36400:
- Workspace может иметь `external_org_id` (из IdP)
- SCIM создаёт пользователей и назначает роли/группы
- СSO логин → user → workspace mapping

### Шаг 5.2 — Мульти-проекты внутри workspace

Если нужно больше гранулярности:
- добавить `project` внутри workspace
- объекты принадлежат `project_id` и наследуют `workspace_id`
Но это лучше отдельным блоком позже, чтобы не перегружать MVP.

### Шаг 5.3 — Квоты и лимиты (подготовка к экономике ресурса)

Опционально связать с 39601–40000 (pricing/quotas):
- лимит коннекторов
- лимит запусков макросов/runner
- лимит объёма knowledge vault

## 6) События и аудит

Логировать:
- workspace_created
- member_invited / invite_accepted / invite_revoked
- member_role_changed
- workspace_deleted (soft)
События отправлять в Observability (если подключено).

## 7) Интеграции с другими блоками (карта привязок)

- 35601–36000 `identity_profiles`: пользователь/сессии
- 36001–36400 `enterprise_identity_access`: enterprise SSO/SCIM (опционально)
- 34001–34400 `enterprise_governance`: политики/орг-правила (опционально)
- 44801–45200 `workflow_runner_macro_engine`: запуск макросов внутри workspace
- 45201–45600 `connectors_factory_sdk`: коннекторы принадлежат workspace
- 44001–44400 `searchable_knowledge_vault`: хранилище знаний workspace
- 47601–48000 `comparison_portal_vitrines`: витрины могут быть workspace-scoped

## 8) Чек-лист готовности

- [ ] Workspace создаётся автоматически при регистрации (personal)
- [ ] Пользователь может создать team workspace
- [ ] Приглашения: create → accept → membership
- [ ] Роли: owner/admin/member/viewer/billing
- [ ] Все ключевые объекты имеют workspace_id
- [ ] Политики доступа работают (read/write/manage)
- [ ] Audit событий
