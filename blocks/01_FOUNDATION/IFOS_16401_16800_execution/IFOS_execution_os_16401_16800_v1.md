# IFOS 16401–16800 — Execution‑OS: рантайм, песочница, секреты, воспроизводимые билды, и one‑click install/run (Make/n8n/WP/native) (v1)

Этот блок делает то, чего вам не хватает в реальном мире:
- “миллионы деталей” превращаются в **запускаемую систему**
- появляется **одна кнопка**: установить → настроить секреты → запустить → наблюдать → откатить
- один и тот же bundle/recipe может жить в разных “движках”: Make, n8n, WordPress, native (Docker/CLI)

Ниже — по порядку, от простого к сложному.

---

## 16401–16440 — Термины: что именно мы “исполняем”

### 16401) Listing vs Bundle vs Job
- **Listing**: запись в реестре (маркетплейс/каталог)
- **Bundle**: набор компонентов + recipes + policy presets + install wizard
- **Job**: конкретный экземпляр bundle/recipe, настроенный под пользователя (tenant) и секреты

### 16402) Run (запуск)
Run = единичное выполнение Job, со статусом, логами, метриками, артефактами и audit trail.

### 16403) Target runtime (куда ставим)
- Make runtime (шаблон/сценарий, модули)
- n8n runtime (workflow JSON, nodes)
- WordPress runtime (plugin + settings + hooks)
- Native runtime (Docker compose / CLI + systemd)

---

## 16441–16510 — Sandbox (песочница) и enforcement

### 16441) Зачем песочница
Если вы хотите “B2B‑OS для интернета”, нужен режим:
- ограничить side effects (delete, money, users)
- ограничить сеть (whitelist доменов)
- ограничить файлы/процессы
- гарантировать redaction секретов и PII

### 16442) Sandbox Policy (MVP)
Policy описывает:
- network: allow/deny домены/порты
- filesystem: allow paths (или none)
- secrets: нельзя писать в logs, нельзя в output
- limits: timeout, memory, concurrency
- flags: pii/money/security_sensitive → повышают требования

### 16443) Enforcement points
- pre-run: проверка policy + contracts + license flags
- run-time: sandbox runtime (container / wasm / restricted python)
- post-run: redaction, audit, metrics, evidence update

---

## 16511–16590 — Secrets Manager (секреты как “первоклассный объект”)

### 16511) Проблема
Секреты сейчас “вручную”:
- в Make — в connections
- в n8n — credentials
- в WP — settings/ENV
- в Docker — env vars

Это ломает переносимость: нельзя “одной кнопкой” мигрировать.

### 16512) SecretRef (универсальная ссылка)
Job хранит *не секрет*, а ссылку:
- secret://ten/<tenant>/vault/<name>
- scope: read only, rotate interval
- redaction rules

### 16513) Secret provisioning wizard
Install plan может сказать:
- какие секреты нужны
- где их взять (OAuth, API key)
- как проверить (test connection)

### 16514) Rotation & revocation
Execution OS должен поддерживать:
- rotate secret
- revoke secret
- audit “кто и когда использовал”

---

## 16591–16660 — Reproducible builds (воспроизводимые сборки)

### 16591) Почему это важно
Без воспроизводимых билдов нет доверия:
- нельзя доказать, что пакет не подменён
- нельзя повторить run на другом узле
- нельзя сделать “evidence court” честным

### 16592) Build Manifest (MVP)
Содержит:
- source refs (git commit, registry versions)
- dependency lock (hashes)
- build recipe (steps)
- produced artifacts (hashes)
- signatures

### 16593) Supply chain
- подпись издателя
- подпись узла‑сборщика
- SBOM (опционально в v2)
- policy: unsigned artifacts → sandbox-only

---

## 16661–16740 — One‑click install/run: план установки

### 16661) Install Plan (как “манифест установки”)
План включает:
- target runtime (make/n8n/wp/native)
- steps (install, config, secrets, smoke test, schedule)
- rollback steps
- post‑install checks (evidence L1/L2)

### 16662) “Одна кнопка” на практике
UI показывает:
1) что будет установлено
2) какие секреты нужны
3) где данные будут храниться
4) какие риски (flags)
5) кнопка “Install & Run”

### 16663) Smoke tests
Мини‑тесты сразу после установки:
- доступ к API
- запись/чтение (если store)
- отправка уведомления в тестовый чат
Smoke test создает evidence L1.

---

## 16741–16800 — Multi‑target backend: Make/n8n/WP/native

### 16741) Target Adapter Contract
Каждая цель должна реализовать одинаковые операции:
- install(plan)
- run(job)
- get_run(run_id)
- pause/resume/schedule
- export(job) (переносимость)
- rollback(plan)

### 16742) Важная идея
Execution OS *не заменяет* Make/n8n/WP — он делает “слой стандарта” сверху:
- единая модель job/run
- единые секреты
- единые policies
- единые evidence/ratings hooks

### 16743) Результат
Вы получаете “операционную систему рационализации”:
- не изобретать новые приложения
- собирать кластеры
- ставить витрины
- запускать безопасно
- измерять и улучшать

---

## Приложения (в этом пакете)
- JSON Schemas: job, run record, sandbox policy, secret ref, build manifest, install plan, target adapter contract, rollback plan
- Specs: runtime architecture, sandbox enforcement, secrets manager, reproducible builds, one-click install/run, target backends
- OpenAPI: Execution API (MVP)
- Examples: job + run + policy + secrets + build manifest + install plan + rollback
- Python skeletons: orchestrator, sandbox evaluator, secret resolver, CLI stub
