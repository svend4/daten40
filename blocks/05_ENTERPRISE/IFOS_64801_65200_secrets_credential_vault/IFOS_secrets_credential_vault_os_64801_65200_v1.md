# IFOS 64801–65200 — Secrets & Credential Vault OS (v1)
Цель: превратить “ключи API/токены/пароли” из хаоса в **управляемый модуль**, который:
- безопасно хранит секреты и “тестовые ключи” (developer-friendly)
- выдаёт доступ **по политике** (least privilege, just-in-time)
- поддерживает ротацию, наследование, аудит
- интегрируется с Connectors Factory, Marketplace, Runtime, Enterprise IAM

Порядок: **простое → среднее → сложное**.

---

## 64801–64825 — Простое: что такое “секрет” в IFOS
**Secret** — это объект, который содержит *значение* (key/token/password/private key) и метаданные:
- `secret_id`, `type`, `owner`, `tenant_id`, `environment`
- `created_at`, `expires_at`, `rotation_policy_id`
- `labels/tags`, `purpose`, `connector_id`, `scopes`
- режим доступа: *read once*, *lease*, *never export*

**SecretRef** — безопасная ссылка на секрет (в workflow, bundle, connector config):
- хранит только `secret_id` + “как получать” (например через runtime lease)
- никогда не содержит сам секрет

---

## 64826–64870 — Среднее: модели хранения (dev → prod)
### 1) Dev vault (простая модель)
- шифрование на диске + master key в env
- audit logs минимально

### 2) Prod vault (правильная модель)
- envelope encryption: data key (DEK) шифруется key-encryption-key (KEK)
- KEK хранится в KMS/HSM (или enterprise KMS)
- журнал аудита неизменяемый (append-only)
- поддержка “dual control” для admin actions

### 3) Enterprise mode
- tenancy: отдельные ключи на тенант
- BYOK (bring your own key) и key escrow policies
- разделение duties: security admin ≠ app admin

---

## 64871–64930 — Политики доступа: least privilege + JIT
IFOS вводит **VaultPolicy**:
- кто может запросить секрет (роль/группа/сервис)
- для чего (action/context) — install/run/export/test
- в какой среде (dev/stage/prod)
- как долго (TTL lease), сколько раз (usage limit)
- требуется ли MFA/step-up (для “опасных секретов”)
- можно ли экспортировать значение или только “подписать/вызвать”

JIT (just-in-time):
- runtime запрашивает “lease” на секрет на 5–15 минут
- выдаётся временный токен доступа к секрету (не сам секрет)
- после TTL — доступ исчезает

---

## 64931–64995 — Ротация: “ключи должны стареть и меняться сами”
**RotationPolicy**:
- периодичность (days)
- способ: manual / semi-auto / auto
- проверка работоспособности (probe)
- “grace window”: старый ключ действует N часов/дней
- alerting: предупреждать заранее

Паттерны ротации:
- API key пары (active + next)
- OAuth refresh token rotation (перевыпуск)
- SSH/private key rotation
- Webhook signing secrets

---

## 64996–65060 — Test Keys & Sandbox Keys: чтобы разработчики не искали “где взять ключ”
IFOS хранит **TestKey** как особый тип секрета:
- `provider` (Stripe, Google, Telegram, OpenAI, …)
- `mode`: sandbox/test
- `rate_limits`, `validity`, `how_to_get`, `scopes`
- может быть *shared demo key* (публичный sandbox) или *personal test key*

Важно:
- тестовые ключи **никогда** не должны работать в prod
- обязательная маркировка `env=test` + политика блокировки

---

## 65061–65120 — Требования коннекторов к кредам (Connectors Factory)
Каждый коннектор описывает “что ему нужно”:
- типы: api_key, oauth_client, service_account_json, webhook_secret
- minimum scopes/permissions
- where used: ingest / run / install
- validation rules (формат, длина, checksum)
- “safe handling”: нельзя экспортировать, нельзя показывать, mask rules

IFOS сопоставляет requirement → secret types → UI wizard → policy checks.

---

## 65121–65175 — Аудит и расследование инцидентов
**SecretAuditEvent**:
- кто запросил, откуда, какой workflow/agent
- разрешено/запрещено, почему (policy decision)
- выдавался ли lease, на сколько, был ли “reuse”
- признаки утечки: массовые запросы, неожиданные регионы, частые deny

Механика реакции:
- revoke all leases, rotate secret, блокировать connector, уведомить владельца
- автоматическое создание тикета support/incident

---

## 65176–65200 — Сложное: “вызов без раскрытия” и безопасные прокси
Для особо чувствительных секретов:
- **signing-as-a-service**: секрет не выдаётся, только подписывает запрос
- **token exchange proxy**: runtime получает временный токен у прокси
- **egress gateway**: коннектор ходит во внешний мир через контролируемый шлюз
- DLP: запрещать утечку в логи/экспорт

---

## Что дальше
Следующий блок:
**65201–65600 — Connector Sandbox & Safe Execution OS**  
(изоляция коннекторов, egress policies, network allowlists, rate limiting, секреты только через lease, replay protection).
