# IFOS 14941–15240 — Compiler‑Runtime OS: реальный рантайм рецептов (state store, scheduler, secret vault, connector adapters), sandbox safe‑run и one‑click bundle builder (v1)

Это **техническое ядро** того, что вы описали как “B2B операционная система для всего интернета”:
- “есть миллионы функций” → нужен **единый реестр**
- “есть recipes” → нужен **исполняемый движок**
- “нужны кластеры/пакеты” → нужен **bundle builder**
- “нужна вертикаль качества” → нужен **evidence + trust**
- “нужна безопасность” → нужен **sandbox + secret vault + policy**

Дальше — всё по шагам: от простого (понятия) к сложному (архитектура и API).

---

## 14941–14970 — Минимальная модель Runtime (самое простое)

### 14941) Что делает Runtime
Runtime берёт:
- **recipe JSON** (формат Recipe‑OS)
- **inputs + secrets**
- **targets** (Make/n8n/WP/CLI) или **native runtime**
и выполняет recipe шаг за шагом, создавая:
- **run record** (лог запуска)
- **evidence artifacts** (preview/log/checksum)
- **state updates** (last_seen и т.п.)

### 14942) Три режима запуска
- **Dry‑run**: без внешних вызовов (или с “mock adapters”)
- **Sandbox**: реальные вызовы, но с ограничениями (rate limit, allowlist)
- **Production**: без ограничений sandbox (но с policy)

### 14943) Run = Job + Attempt
- **Job** = постоянная “задача” (расписание/триггер, secrets refs, inputs)
- **Attempt** = конкретная попытка запуска (с retry/backoff)

---

## 14971–15020 — Состояние (State Store) и идемпотентность (среднее)

### 14971) Почему state store обязателен
Без state:
- RSS будет слать одно и то же
- webhook будет писать дубли
- сравнение цен будет перезапускаться без кеша

### 14972) Минимальные операции state store
- `get(job_id, key)`
- `set(job_id, key, value)`
- `compare_and_set(job_id, key, expected, new)`
- `append_log(job_id, record)` (опционально)

### 14973) Идемпотентность на практике
Каждый step должен иметь “dedupe key” или маркер:
- message_id / item_guid / checksum payload
- хранить в state последние N ключей (ring buffer)

---

## 15021–15080 — Connector Adapters (главный слой интеграции)

### 15021) Что такое adapter
Adapter — это “драйвер” (ваше слово):
- знает API сервиса (Telegram, Google Sheets, WP, Stripe…)
- принимает стандартизованный request
- возвращает стандартизованный response
- умеет redact secrets из логов

### 15022) Два уровня adapters
- **Function‑adapter**: реализует конкретный function_id (например telegram.send_message)
- **Service‑adapter**: общая обвязка сервиса (auth, rate-limit, retries)

### 15023) Обязательные функции adapter API
- `validate(params)`
- `execute(params, ctx)`
- `redact(obj)`
- `capabilities()` (что умеет: markdown/html, attachments, batching)

---

## 15081–15130 — Secret Vault (хранилище секретов) + policy

### 15081) Почему нельзя хранить токены “в рецепте”
Потому что:
- рецепты будут публиковаться
- логи будут храниться
- токены утекут

### 15082) Минимальный Secret Vault
- хранит secrets по `secret_ref`
- выдаёт secret только при выполнении job, а не при чтении recipe
- ведёт audit trail (кто/когда получал)

### 15083) Policy flags
Каждый listing/recipe/job имеет flags:
- pii (персональные данные)
- money (платежи/финансы)
- security_sensitive (доступы/админки)

И policy влияет на sandbox:
- pii=true → строгий redact, короткое хранение логов
- money=true → обязательный L2/L3 evidence + двухфакторная публикация
- security_sensitive=true → allowlist only + manual review

---

## 15131–15180 — Scheduler + Triggers (сложнее)

### 15131) Scheduler нужен для “макросов интернета”
Чтобы всё работало “как Excel макрос”:
- по времени (каждые 10 минут)
- по событию (webhook)
- по очереди (job queue)

### 15132) Триггеры (MVP)
- `cron`: расписание
- `webhook`: входящее событие
- `manual`: ручной запуск
- `queue`: запуск по сообщению из очереди

### 15133) Минимальные гарантии
- at‑least‑once execution (минимум)
- dedupe через state store
- retry/backoff
- dead letter queue (DLQ) для провалов

---

## 15181–15220 — Sandbox Safe‑Run (самый “опасный” слой)

### 15181) Sandbox — это не “симуляция”, а “ограниченная реальность”
Sandbox должен:
- ограничивать домены (allowlist)
- ограничивать частоту (rate limit)
- запрещать опасные действия (delete, transfer_money) без подтверждения
- маскировать PII/секреты в логах
- сохранять evidence без утечек

### 15182) Модель разрешений (MVP)
- allow outbound hosts: ["api.telegram.org", "rss.example.com"]
- deny methods: ["DELETE"] (по умолчанию)
- max requests per run: 50
- max payload size: 1MB
- max runtime: 30s/step, 5min/run

---

## 15221–15240 — One‑click bundle builder (финальный уровень)

### 15221) Bundle builder строит пакеты из витрин
Вы выбираете витрину “Travel Hub Starter”:
- recipes (RSS, сравнение, CRM, рассылка)
- deps (плагины, коннекторы)
- install wizard (secrets + inputs)
Bundle builder собирает:
- bundle manifest
- generated targets (Make/n8n/WP/CLI)
- install/run report template
- evidence checklist

### 15222) “Одна кнопка” в реальности
Кнопка = bundle + runtime:
- install (подтянуть deps, создать jobs)
- configure (wizard secrets)
- run dry‑run (preview)
- run sandbox (integration)
- publish evidence (опционально)

---

## Приложения (в этом пакете)
- JSON Schemas: job, run record
- Interfaces/specs: adapters, state store, vault, scheduler, sandbox, bundle builder
- OpenAPI: Runtime API (MVP)
- Examples: job + run record + sandbox policy snippet
- Python skeleton: runtime engine + adapter stubs
