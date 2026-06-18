# IFOS — Connector Test Harness & CI/CD Quality Gates (Блок 62401–62800)

Версия: v1 · Пакет: `IFOS_62401_62800_connector_test_harness_ci_cd_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок (контекст IFOS)

Ты описывал проблему: интернет и экосистемы (WordPress-плагины, Make/n8n сценарии, GitHub проекты) огромные, но **не интегрированы и не доведены до «одна кнопка — работает»**. Чаще всего причина — отсутствуют:
- стандартизированные тесты коннекторов
- воспроизводимые песочницы/фикстуры
- автоматические quality gates перед публикацией

Этот блок превращает «хаос интеграций» в **конвейер качества**: каждый коннектор/пакет проходит минимальный набор автоматических проверок до того, как его можно устанавливать и использовать.

## 1) Что делает (функции)

1) **Connector Test Harness**: единый фреймворк тестов для всех коннекторов.
2) **Contract Tests**: тесты соответствия data contracts (схемам) и API-спецификации.
3) **Auth Tests**: OAuth/API-key flows в sandbox режиме.
4) **Error & Retry Tests**: 429/timeouts/5xx и поведение ретраев.
5) **Idempotency Tests**: проверка повторных запросов/защита от дублей.
6) **Security Checks**: сканирование на утечки секретов и небезопасные практики.
7) **CI/CD Pipelines**: готовые пайплайны (GitHub Actions/GitLab/Jenkins) как шаблоны.
8) **Quality Gates**: политика «публиковать можно только если…» (минимальный набор тестов).
9) **Evidence Bundle**: артефакты тестов (логи, отчёты) для marketplace и enterprise аудита.

## 2) Что НЕ делает (границы)

- Не заменяет runtime исполнение рабочих процессов (это другие блоки).
- Не хранит секреты; берёт их из credential vault и sandbox профилей.
- Не решает проблемы внешних API (если у провайдера нет sandbox), но фиксирует это.

## 3) MVP — от простого к среднему

### 3.1 Уровень 1 (самое простое)

- Каталог тестов коннектора: `health`, `auth`, `list`, `create`, `error`.
- CI шаблон: запуск тестов на PR/merge.
- Отчёт в формате JUnit/JSON.
- Gate: нельзя публиковать коннектор без `health+auth+contract`.

### 3.2 Уровень 2 (среднее)

- Прогон тестов по **sandbox profiles** и фикстурам.
- Fault-injection: 429/timeouts/500 (через mock providers).
- Idempotency suite: повтор запросов, дедуп ключи.
- Coverage метрика по capability-модели: какие функции покрыты тестами.

### 3.3 Уровень 3 (продвинуто)

- Record/Replay тесты на реальных sandbox ответах.
- Матрица совместимости: версии API/SDK.
- Регрессии: сравнение результатов текущего и предыдущего релиза.

## 4) Структура тестов (пример)

### TestCase schema
- `test_id`
- `connector_id`
- `capability` (например `crm.contact.create`)
- `preconditions` (fixtures/profile)
- `steps` (HTTP calls or connector ops)
- `assertions` (schema, status, fields)
- `fault_mode` (optional)
- `evidence` (logs, payload hashes)

### Suites
- `smoke` (быстро)
- `contract` (схемы)
- `auth` (токены)
- `resilience` (ретраи)
- `idempotency` (дедуп)

## 5) API (минимум)

- `POST /ci/tests/run` (запуск набора тестов)
- `GET  /ci/tests/results/{run_id}` (результаты)
- `POST /ci/gates/evaluate` (оценка quality gates)
- `GET  /ci/templates` (шаблоны пайплайнов)

## 6) Зависимости

### Hard deps
- 62001–62400 `sandbox_test_keys_dev_env` (sandbox профили, моки, фикстуры)
- 61601–62000 `enterprise_connectors_credential_vault_os` (секреты)
- 43201–43600 `data_contracts_schema_registry_os` (контракты)
- 45201–45600 `connectors_factory_sdk_os` (единый SDK/описания)

### Optional deps
- 45601–46000 `marketplace_curation_quality_os` (публикация/курирование)
- 46001–46400 `publishing_release_workflow_os` (релизы)
- 34801–35200 `observability_reliability_os` (метрики)
- 54401–54800 `audit_log_event_bus` (аудит)

## 7) Чек‑лист

- [ ] Унифицированный test harness
- [ ] Набор smoke/contract/auth
- [ ] Resilience + fault modes
- [ ] Idempotency suite
- [ ] CI templates
- [ ] Quality gates
- [ ] Evidence bundle
