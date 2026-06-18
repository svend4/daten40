# IFOS — Sandbox, Test Keys & Developer Environments (Блок 62001–62400)

Версия: v1 · Пакет: `IFOS_62001_62400_sandbox_test_keys_dev_env_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок (идея)

Многие интеграции «ломаются» не из‑за кода, а из‑за отсутствия **песочниц**, **тестовых ключей**, **тестовых аккаунтов** и **воспроизводимых dev‑профилей**. В итоге:
- разработчики не могут протестировать коннектор «как у пользователя»
- нет стандартного каталога sandbox‑окружений (что где взять)
- ключи хранятся хаотично, нарушая безопасность
- интеграции нельзя воспроизвести/отладить одной кнопкой

Этот блок делает то, что в офисных пакетах делают «макросы и шаблоны»: даёт **стандартизированные dev‑окружения**, **каталог test keys**, и **моки** для интеграций, чтобы можно было быстро повторять тесты.

## 1) Что делает (функции)

1) **Test Key Catalog**: реестр тестовых ключей/сандбоксов по коннекторам (без хранения секретов).
2) **Sandbox Profiles**: шаблоны окружений (dev/stage/sandbox) с параметрами и ограничениями.
3) **Credential Scoping**: правила, какие ключи можно использовать где (sandbox vs prod).
4) **Mock Providers**: локальные/встроенные моки (fake API) для имитации сервисов.
5) **Replay & Fixtures**: наборы тестовых данных и воспроизводимые ответы.
6) **Rate-limit Simulator**: имитация 429/лимитов для тестирования ретраев.
7) **OAuth Test Flows**: тестовые сценарии OAuth (device code, PKCE, refresh).
8) **One-click Dev Setup**: подготовка dev‑профиля и фикстур одной командой.

## 2) Что НЕ делает (границы)

- Не хранит секреты (это делает credential vault 61601–62000).
- Не заменяет тестовый раннер (run‑движок и макро‑движок в других блоках).
- Не гарантирует наличие sandbox у каждого внешнего сервиса (но фиксирует это в каталоге).

## 3) MVP — от простого к среднему

### 3.1 Уровень 1 (самое простое)

- CSV/таблица **Test Key Catalog** (какой сервис имеет sandbox, ссылки на получение ключей)
- UI/страница «Developer → Sandboxes» с фильтром по коннекторам
- Валидатор: запрет использовать prod‑ключи в sandbox‑workspace (и наоборот)

### 3.2 Уровень 2 (среднее)

- **Sandbox Profiles**: набор преднастроенных профилей (dev/stage)
- **Mock Providers**: встроенный mock server с готовыми эндпоинтами
- **Fixtures**: типовые фикстуры (письмо, заказ, платеж, контакт)
- **Rate-limit simulator**: 429, backoff, jitter

### 3.3 Уровень 3 (продвинутый)

- Record/Replay (запись реальных ответов в sandbox и воспроизведение)
- Генератор данных (синтетические датасеты)
- Тестовые план‑кейсы для marketplace публикации

## 4) Модель данных

**test_key_catalog_item** (без секретов):
- `connector_id`
- `provider`
- `sandbox_available` (bool)
- `how_to_get` (url/text)
- `auth_type` (api_key|oauth|basic|custom)
- `rate_limits_hint`
- `notes`

**sandbox_profile**:
- `profile_id`
- `name` (dev|stage|sandbox)
- `workspace_template_id`
- `allowed_connectors` (list)
- `disallowed_capabilities` (e.g., payments.capture)
- `data_fixtures_pack` (id)

**mock_provider**:
- `mock_id`
- `provider_name`
- `base_url`
- `endpoints` (list)
- `fault_modes` (timeouts|429|500)

## 5) API (минимум)

- `GET  /dev/sandboxes` (каталог)
- `GET  /dev/sandbox-profiles`
- `POST /dev/sandbox-profiles/{id}/apply` (one-click setup)
- `GET  /dev/mocks`
- `POST /dev/mocks/{id}/start`
- `POST /dev/mocks/{id}/stop`
- `POST /dev/replay/record` (optional)
- `POST /dev/replay/play` (optional)

## 6) Зависимости

### Hard deps
- 61601–62000 `enterprise_connectors_credential_vault_os` (секреты и политики ключей)
- 45201–45600 `connectors_factory_sdk_os` (коннекторы должны описывать sandbox)
- 32801–33200 `runtime_execution_os` (выполнение тестовых runs)

### Optional deps
- 58801–59200 `demo_sandbox_one_click_trials_os` (демо‑триалы)
- 40801–41200 `experimentation_evaluation_os` (оценка интеграций)
- 34801–35200 `observability_reliability_os` (метрики/логи моков)
- 54401–54800 `audit_log_event_bus` (аудит выдачи/применения профилей)

## 7) Чек‑лист

- [ ] Каталог sandbox/test keys (без секретов)
- [ ] Валидатор scope (sandbox vs prod)
- [ ] Sandbox profiles + apply
- [ ] Mock server + fault modes
- [ ] Fixtures packs
- [ ] Rate-limit simulator
- [ ] Optional: record/replay
