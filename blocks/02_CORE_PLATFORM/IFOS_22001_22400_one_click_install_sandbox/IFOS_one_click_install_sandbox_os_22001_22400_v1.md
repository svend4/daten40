# IFOS 22001–22400 — One‑Click Install & Sandbox‑OS: “макросы” для интернета, план установки, секреты, миграции, smoke‑тесты, rollback, policy‑gates (v1)

Вы хотите, чтобы “миллионы решений” стали:
- **внятными** (словари/граф — сделали в 21601–22000),
- **переносимыми между узлами** (федерация/пакеты — сделали в 21201–21600),
- и наконец **устанавливаемыми** “в один клик” как макрос в Excel.

Этот блок — про **исполнение**: как IFOS берёт bundle/cluster и превращает в работающую систему на вашем узле.

Ниже — по порядку, от простого к сложному.

---

## 22001–22060 — Что значит “One‑Click” (простое)

### 22001) One‑Click = 7 обязательных стадий
1) **Resolve**: понять зависимости (capabilities, пакеты, инфра)
2) **Plan**: построить install plan (шаги + порядок)
3) **Bind secrets**: подтянуть credentials/секреты
4) **Sandbox deploy**: развернуть в песочнице
5) **Smoke tests**: проверить, что “дышит”
6) **Policy gate**: разрешить/запретить прод
7) **Promote**: прод‑включение + мониторинг + rollback plan

### 22020) Два режима установки
- *Sandbox‑first* (по умолчанию): сначала песочница → потом прод
- *Direct‑prod* (только если policy позволяет и риск низкий)

---

## 22061–22140 — Install Plan: детальный сценарий (среднее)

### 22061) InstallPlan как “скрипт макроса”
InstallPlan содержит:
- цель: subject (bundle/asset)
- target platform (wordpress/make/n8n/node‑red/android)
- steps[] (упорядоченные шаги)
- credential bindings
- migrations
- rollback plan
- expected smoke tests

### 22100) Step taxonomy (типы шагов)
Типичные шаги:
- `fetch_payload` (загрузить zip/json)
- `verify_signatures` (подписи)
- `verify_sbom` (SBOM)
- `apply_policy_precheck`
- `import_workflow` / `install_plugin` / `import_flow`
- `configure_credentials`
- `configure_webhooks`
- `run_migrations`
- `run_smoke_tests`
- `promote_to_prod`
- `post_install_monitoring_enable`

---

## 22141–22220 — Секреты и credentials (важно)

### 22141) Credential binding
Одна и та же capability требует разных секретов на разных платформах.
Например `deliver.telegram`:
- Make: token в аккаунте Make
- n8n: credential “Telegram API”
- WP: env var + settings page
IFOS хранит **абстрактную потребность** в секрете, а затем “биндит” её к реальному хранилищу.

### 22180) Secret references
Секреты никогда не кладём в bundle.
Bundle содержит только ссылки:
- `secret://vault/telegram_bot_token`
- `secret://env/MAKE_API_TOKEN`
- `secret://k8s/secret/ifos-telegram`

---

## 22221–22300 — Sandbox execution + smoke tests (сложно)

### 22221) SandboxRun
Песочница должна быть воспроизводимой:
- отдельная среда (docker namespace / vm / wp staging / n8n staging)
- ограничения сети (policy)
- логирование
- артефакты (экспорт конфигов, отчёты)

### 22260) Smoke tests & health checks
Smoke tests — это минимальные проверки:
- “workflow импортирован”
- “webhook отвечает 200”
- “Telegram send проходит на тестовый чат”
- “RSS ingest возвращает items”
Результаты пишем в SmokeTestResult + публикуем в trust signals.

---

## 22301–22360 — Rollback (очень важно)

### 22301) RollbackPlan
Если что-то пошло не так:
- откатить импорт (удалить workflow/flow/plugin)
- откатить миграции (down migrations или snapshot restore)
- отозвать credentials binding (disabled)
- вернуть старую версию (supersedes edge из KG)

### 22330) Два уровня rollback
- *Fast rollback*: переключить трафик на старую версию
- *Full rollback*: откатить данные/конфиги

---

## 22361–22400 — Policy gates и объяснимость (максимальная сложность)

### 22361) PolicyGateDecision
Перед прод‑включением IFOS должен сказать:
- PASS/FAIL
- причины (политика, trust, compat, secrets)
- что можно исправить (remediation)
- какие риски остались

### 22390) Explain install decisions
Каждый запрет должен быть “объясним”:
- “bundle требует внешнюю сеть, а policy offline=true”
- “нет SBOM”
- “нет подписи доверенного издателя”
- “smoke test telegram_send failed”

---

## Что лежит в пакете
- JSON Schemas: install plan/steps, credential binding, secret ref, sandbox run, smoke test result, rollback plan, policy gate decision, migration step, artifact store, runtime environment, install report
- Specs: one‑click install, sandbox execution, secrets/credentials, smoke tests, rollback strategy, policy gates, migrations+compat
- OpenAPI: Install & Sandbox API (MVP)
- Examples: “News Digest Cluster” установка Make+n8n (sandbox-first), отчёт, smoke tests, gate decision, rollback plan
- Python skeletons: install planner, sandbox executor, secrets manager stub, smoke runner stub, rollback executor, policy evaluator
