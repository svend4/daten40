# IFOS — Feature Flags, Remote Config & Kill‑Switches (Блок 51201–51600)

Версия: v1 · Пакет: `IFOS_51201_51600_feature_flags_remote_config_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

IFOS — это «операционная система функций», где компоненты (коннекторы, макросы, витрины) включаются/выключаются, выпускаются поэтапно и часто зависят от ролей, стран, тарифов и рисков.

Без feature flags система становится хрупкой:
- новый релиз ломает часть пользователей
- нет безопасного A/B (экспериментов) и gradual rollout
- нет аварийной кнопки отключения опасного коннектора/действия
- сложно включать бета‑функции только для выбранных workspace

Этот блок даёт **удалённое управление поведением** продукта:
флаги, конфиги, таргетинг, аудит, kill‑switch.

## 1) Что делает (функции)

1) **Feature Flags** — включение/выключение функций без деплоя.
2) **Remote Config** — динамические параметры (пороги, лимиты, тексты, выбор алгоритма).
3) **Targeting** — правила: роль/тариф/локаль/workspace/segment.
4) **Kill‑Switches** — аварийное отключение пакета/коннектора/операции.
5) **Release Rings** — каналы: internal → beta → GA.
6) **Audit Trail** — кто/когда/почему поменял флаг.
7) **SDK/Resolver** — быстрый вычислитель значений на сервере и/или клиенте.

## 2) Что НЕ делает (границы)

- Не заменяет биллинг/тарифы: только использует план/квоты как условия.
- Не является системой секретов: параметры не должны хранить ключи.
- Не является полноценной системой экспериментов: A/B логика в 40801–41200 (опционально).

## 3) MVP (простое → среднее)

### 3.1 Модель данных

Сущности:
- `flag_definition`: описание флага
- `flag_rule`: правило таргетинга
- `segment`: список workspace/user (динамический или статический)
- `config_key`: параметр remote config
- `change_log`: журнал изменений

**flag_definition**:
- `flag_id` (slug)
- `type` (boolean|multivariate)
- `default_value`
- `owner_team`
- `risk_level` (low|medium|high)
- `release_ring` (internal|beta|ga)

**flag_rule**:
- `rule_id`
- `flag_id`
- `priority`
- `when` (условия)
- `value` (что вернуть)

### 3.2 Условия (when) — минимальный DSL

MVP условия:
- `user.role in [...]`
- `workspace.id in segment(...)`
- `workspace.plan in [...]`
- `locale in [...]`
- `country in [...]`

Комбинация: AND/OR, без вложенных функций кроме `segment()`.

### 3.3 Оценка флага (evaluation)

Порядок:
1) найти активные правила по `flag_id` (по priority)
2) первое совпавшее правило возвращает значение
3) иначе вернуть `default_value`
4) записать telemetry (опционально)

### 3.4 Kill‑Switch

Kill‑switch — это флаг высокого приоритета, который перекрывает остальные правила.
Применения:
- отключить проблемный коннектор
- запретить публикацию витрин
- временно выключить импорт контента

### 3.5 UI и роли

Минимальная админ‑страница:
- список флагов (по ring/owner/risk)
- деталка флага: правила, сегменты, история изменений
- быстрый переключатель kill‑switch

Роли:
- `platform_admin`: может менять всё
- `owner_team_editor`: может менять только свои флаги
- `viewer`: только читать

## 4) Средний уровень (практика)

1) **Rollout %** (опционально): включать для N% workspace в ring beta.
2) **Scheduled enable**: включить в дату/время.
3) **Safeguards**: запрет включать high‑risk флаги без причины/тикета.
4) **Diff view**: сравнить текущие правила с прошлой версией.

## 5) API (минимум)

- `GET  /flags` (список)
- `GET  /flags/{flag_id}`
- `POST /flags/{flag_id}/rules` (создать правило)
- `POST /flags/{flag_id}/toggle` (быстро включить/выключить)
- `POST /flags/evaluate` (resolver)
- `GET  /flags/{flag_id}/changelog`
- `GET  /config/{key}` (remote config для клиента)

## 6) Зависимости

### Hard deps
- 36401–36800 `workspaces_orgs_os` (workspaces/оргструктура)
- 35601–36000 `identity_profiles_os` (user/roles)
- 34001–34400 `enterprise_governance_os` (аудит/политики управления)

### Optional deps
- 40801–41200 `experiment_evaluation_os` (A/B)
- 56001–56400 `analytics_insights_os` (метрики)
- 34801–35200 `observability_reliability_os` (алерты)
- 59601–60000 `enterprise_rollouts_change_control_os` (change control)

## 7) Чек‑лист

- [ ] CRUD флагов и конфигов
- [ ] Resolver (evaluate)
- [ ] Segments (статические)
- [ ] Changelog + аудит
- [ ] Kill‑switch UI
