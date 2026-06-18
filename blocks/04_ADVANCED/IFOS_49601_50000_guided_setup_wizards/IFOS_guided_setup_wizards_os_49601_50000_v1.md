# IFOS — Guided Setup Wizards & Preflight Checks (Блок 49601–50000)

Версия: v1 · Пакет: `IFOS_49601_50000_guided_setup_wizards_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

IFOS собирает мир из «кирпичиков» (коннекторы/макросы/bundles/витрины). Без «мастеров настройки» (wizards) внедрение выглядит так:
- пользователь скачал bundle, но не понимает, что делать дальше
- не настроены ключи/секреты → всё падает
- не выбран workspace/роль/политики
- не понятно, как проверить, что оно «живое»

Этот блок добавляет **навигацию от цели к работающей системе**:
1) выбрать цель (use-case)
2) выбрать/установить bundle
3) пройти preflight (проверки окружения)
4) настроить коннекторы (ключи/тест-ключи)
5) запустить smoke-test
6) получить отчёт и кнопки «поправить/повторить/откатить».

## 1) Что делает (функции)

1) **Wizards каталога**: набор готовых пошаговых «мастеров» под сценарии.
2) **Preflight checks**: диагностика окружения, прав, секретов, квот.
3) **Connector setup UI**: сбор/валидация cred, поддержка test keys.
4) **Smoke tests**: быстрые тестовые запуски коннекторов/макросов.
5) **Auto-fix hints**: подсказки исправлений и ссылки на документацию.
6) **Rollback/cleanup**: отмена частично выполненной установки.

## 2) Что НЕ делает (границы)

- Не хранит секреты сама по себе: использует credential vault (61601–62000).
- Не является marketplace installer: вызывает install/run API (см. marketplace install).
- Не заменяет обучение/курсы: это отдельные learning блоки.

## 3) MVP (простое → среднее)

### Шаг 3.1 — Wizard Definition (описание мастера)

Сущность `wizard_definition`:
- `wizard_id` (slug)
- `display_name`
- `use_case_tag` (news|compare|crm|office|knowledge|automation)
- `bundle_ref` (какой bundle ставим по умолчанию)
- `steps[]` (массив шагов)

Шаг (`wizard_step`):
- `step_id`, `title`, `type` (select|form|preflight|install|test|summary)
- `inputs_schema` (минимально: список полей)
- `actions` (какие API вызвать)
- `success_criteria`

### Шаг 3.2 — Preflight Checks

MVP набор проверок:
- workspace exists & role ok
- квоты/лимиты (если есть)
- наличие обязательных зависимостей bundle
- наличие cred requirements для коннекторов
- доступность runtime (ping)

Сущность `preflight_result`:
- `check_id`, `status` (pass|warn|fail)
- `message`
- `fix_hint` (что делать)

### Шаг 3.3 — Connector Setup

Wizard шаг `type=form` собирает параметры cred.
Валидация:
- формат
- обязательные поля
- тест-вызов `connector.ping()` (smoke)

Сущность `connector_setup_state`:
- `connector_id`
- `env_profile_id`
- `cred_ref` (ссылка на vault)
- `status` (configured|invalid|missing)

### Шаг 3.4 — Smoke Tests

Smoke-test — быстрый run в sandbox режиме:
- один API вызов
- тестовый payload
- ожидаемый тип ответа

Сущность `smoke_test_run`:
- `run_id`, `target` (connector|macro)
- `status` (ok|fail)
- `duration_ms`
- `error_summary` (если fail)

### Шаг 3.5 — Summary Screen

Показывает:
- что установлено
- что настроено
- какие тесты прошли
- кнопки: `repeat test`, `open console`, `rollback`.

## 4) Средний уровень: шаблоны мастеров и автопочинка

1) **Wizard templates**: генерация мастера из bundle manifest (авто-шаги).
2) **Auto-fix**: предложить создать env_profile, импортировать test key,
   включить нужный policy, установить missing dependency.
3) **Progress checkpoints**: сохранение прогресса и продолжение позже.

## 5) Ближе к сложному: enterprise rollouts и multi-tenant

- Массовый rollout по workspace/организациям (с шаблонами профилей).
- Политики запрета некоторых коннекторов.
- Локализация мастеров (i18n).

## 6) API (минимум)

- `GET  /wizards` (каталог)
- `POST /wizards/{wizard_id}/start` → `session_id`
- `POST /wizards/{session_id}/step/{step_id}` (submit)
- `GET  /wizards/{session_id}/status` (progress)
- `POST /wizards/{session_id}/rollback` (cleanup)
- `POST /preflight/run` (явно)
- `POST /smoketests/run` (явно)

## 7) Зависимости

### Hard deps
- 44801–45200 `workflow_runner_macro_engine` (для smoke runs)
- 45201–45600 `connectors_factory_sdk` (коннекторы и их ping)
- 61601–62000 `enterprise_connectors_credential_vault` (секреты)
- 55601–56000 `distribution_sync_os` (для дистрибуции мастеров/шаблонов)

### Optional deps
- 58801–59200 `demo_sandbox_one_click_trials` (trial/sandbox)
- 59601–60000 `enterprise_rollouts_change_control` (массовые внедрения)
- 41601–42000 `localization_i18n` (локализация)

## 8) Чек-лист

- [ ] Каталог мастеров
- [ ] Сессии мастера + прогресс
- [ ] Preflight
- [ ] Setup коннекторов (валидация)
- [ ] Smoke tests
- [ ] Summary + rollback
