# IFOS 23601–24000 — Installer & Runtime OS (One‑Click + Sandbox): установка, профили, изоляция, секреты, миграции, rollback, dry‑run, receipts (v1)

Ключевой тезис из вашего запроса:
> “Есть тысячи функций, но они не собраны в кластеры и не запускаются одной кнопкой. Нужна операционная система интернета.”

Этот блок — именно **“одна кнопка”**:
- детерминированная установка кластера (как “макрос”) в среду,
- sandbox прогон для проверки,
- управление секретами и доступами,
- миграции и откаты (rollback),
- receipts: доказательства установки/запуска (для Trust OS и Observability OS).

Дальше — по порядку от простого к сложному.

---

## 23601–23640 — Три режима: Dry‑Run → Sandbox → Prod

### 23601) Dry‑run (безопасная симуляция)
Dry‑run отвечает на вопросы:
- “что будет установлено?”
- “какие разрешения потребуются?”
- “какие секреты нужны?”
- “какие зависимости конфликтуют?”
- “можно ли откатить?”

### 23615) Sandbox (реальный прогон, но изолированный)
Sandbox — это “песочница”:
- отдельные credentials / тестовые токены,
- ограничение ресурсов (quota),
- запрет на экспорт PII,
- “dry delivery” (отправка сообщений в тестовый канал).

### 23630) Prod (боевой контур)
Prod требует прохождения policy gates:
- минимум качества (например L3),
- подпись или верифицированный издатель,
- SLO/алерты готовы,
- rollback план присутствует.

---

## 23641–23710 — InstallRequest → InstallPlan (инсталлер как компилятор)

### 23641) InstallRequest
Заявка на установку:
- что ставим (cluster/bundle/asset)
- куда ставим (profile: dev/staging/prod)
- ограничения (self-hosted/hosted, бюджет, privacy)
- стратегия версий (latest/stable/pinned)

### 23670) InstallPlan (детерминированный план)
План состоит из шагов:
1) resolve dependencies
2) lock versions (lockfile)
3) request permissions
4) request secrets
5) apply migrations (если надо)
6) install artifacts
7) configure runtime
8) health checks
9) write receipt

План должен быть воспроизводимым: сегодня и завтра одинаковый результат при одинаковом lockfile.

---

## 23711–23770 — RuntimeProfile: профили среды (от простого к зрелому)

Пример профилей:
- `dev.local` — минимальные политики, максимум логов
- `sandbox.safe` — изоляция + тестовые каналы + квоты
- `staging.allowlist` — почти прод, но с allowlist доменов/получателей
- `prod.strict` — строгие policy gates, минимум прав, контроль изменений

Каждый профиль задаёт:
- ограничения окружения (EnvironmentConstraint)
- квоты (ResourceQuota)
- правила секретов
- правила логирования (PII redaction из прошлого блока)

---

## 23771–23840 — Секреты и разрешения (самая частая “поломка” интеграций)

### 23771) PermissionRequest
Список прав и доступов:
- какие API вызовы
- какие scopes
- какие external endpoints
- какие webhooks

### 23800) SecretRef и Vault
Секреты никогда не лежат в сценарии.
Сценарий получает только SecretRef:
- `secret://telegram/bot_token`
- `secret://openai/api_key`
- `secret://rss/proxy_key`

Vault хранит:
- версию секретов,
- ротацию,
- кто/что имеет доступ,
- audit trail.

---

## 23841–23910 — Миграции и rollback (уровень “инженерной зрелости”)

### 23841) MigrationPlan
Миграции бывают:
- данные (таблицы, поля)
- конфиги (настройки WP/Make/n8n)
- эндпоинты и webhooks

### 23870) RollbackPlan
Rollback должен быть реальным:
- “что откатываем” (конфиги, версии, маршруты)
- “как возвращаемся” (предыдущая версия + backup)
- “критерии отката” (health check fail / SLO burn rate)

Rollback — это гарантированная кнопка “назад”.

---

## 23911–23960 — Запуск и контроль выполнения (runtime)

### 23911) RunCommand
Команда запуска:
- “run once” (одноразовый прогон)
- “schedule” (по расписанию)
- “webhook mode” (по событию)
- “daemon” (постоянно)

### 23930) HealthCheck
Проверки:
- connectivity (API доступ)
- auth (валидность токена)
- e2e (тестовый payload прошёл)
- performance (латентность в пределах)

---

## 23961–24000 — Receipts и доказательства (связка с Trust + Observability)

### 23961) ExecutionReceipt
Receipt фиксирует:
- plan_id, subject_id, profile_id
- какие шаги выполнены
- версии и lockfile hash
- результаты health checks
- ссылки на logs/trace ids
- итог: success/fail + причина

Receipt — главный “доказательный объект” для:
- Trust signals (Verified install)
- Incident OS (таймлайн)
- Quality uplift L0→L3

---

## Что в пакете
- JSON Schemas: InstallRequest, InstallPlan, RuntimeProfile, SecretRef, SandboxSession, MigrationPlan, RollbackPlan, ExecutionReceipt, DryRunReport, DependencyLockfile, EnvironmentConstraint, PermissionRequest, ResourceQuota, HealthCheck, RunCommand, ArtifactCacheRecord, PolicyGateResult
- Specs: one-click installer, sandbox isolation, secrets management, migrations+rollback, runtime execution, profiles+constraints
- OpenAPI: Installer & Runtime API (MVP)
- Examples: News Digest Cluster: dry-run → sandbox run → prod install with gates + receipt
- Python stubs: planner, executor, sandbox manager, secret vault, rollback executor
