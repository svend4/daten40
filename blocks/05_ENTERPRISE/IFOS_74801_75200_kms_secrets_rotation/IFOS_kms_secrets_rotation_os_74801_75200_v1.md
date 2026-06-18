# IFOS — KMS / Secrets Rotation & Key Hygiene (74801–75200) — v1

## 0) Зачем этот блок (простыми словами)
В современном «интернет‑офисе» у каждого коннектора/сервиса есть **секреты** (API keys, OAuth refresh tokens, пароли, webhook secrets) и **криптоключи** (KMS‑keys, signing keys).
Если их не **инвентаризировать, хранить, ограничивать, ротировать, отзывать и аудитить**, то:
- возникают взломы (утечки, подмена webhook’ов, доступ к данным),
- невозможно соответствовать требованиям enterprise (audit, compliance),
- любой «one‑click bundle» становится опасным.

Этот блок добавляет в IFOS системный слой: **ключи и секреты как управляемый ресурс**.

---

## 1) Что входит в блок (MVP → Enterprise)

### 1.1 MVP (самое простое)
1) **Secret Registry (инвентарь)**: где секрет используется, в каком окружении, у кого владелец.
2) **Secret Store Adapter**: единый интерфейс к хранилищам (Vault/KMS/Cloud secrets).
3) **Rotation Jobs**: расписание ротации (политика + “job runner”).
4) **Audit Trail**: события кто/когда создал/прочитал/изменил/ротировал/отозвал.
5) **Emergency Revoke**: “kill switch” для компрометации.

### 1.2 Средний уровень
6) **Key Hierarchy**: master keys → data keys; envelope encryption.
7) **Scopes & Least Privilege**: ограничение прав по окружениям/workspace’ам/ролям.
8) **Webhook Signing**: управление secrets для подписи входящих событий.
9) **Token Exchange**: преобразование/обновление токенов (refresh→access) с безопасным кешем.

### 1.3 Enterprise (сложное)
10) **HSM / BYOK / HYOK**: корпоративные ключи и требования хранения.
11) **Dual Control**: критические операции требуют 2‑факторного одобрения.
12) **Evidence Packs**: автоматическая сборка доказательств (audit evidence) для проверок.
13) **Secrets Scanning**: проверка репозиториев/артефактов на утечки.
14) **Key Attestation**: доказательство корректной конфигурации ключей/политик.

---

## 2) Границы блока (что он НЕ делает)
- Не реализует конкретный Vault/KMS (мы интегрируемся через адаптеры).
- Не заменяет IAM/SSO — он использует их (см. enterprise_identity_access, identity_profiles).
- Не делает ETL или RAG — только безопасность ключей/секретов.
- Не выполняет бизнес‑логику коннекторов, а обеспечивает их безопасную работу.

---

## 3) Основные сущности (минимальный словарь данных)
### 3.1 Secret
- `secret_id` (IFOS id)
- `kind`: api_key | oauth_refresh | password | webhook_secret | signing_key | encryption_key_ref
- `owner`: team/user/workspace
- `environment`: dev | test | prod
- `connector_slug`
- `scopes`
- `rotation_policy_id`
- `storage_ref` (где лежит фактически)
- `last_rotated_at`, `next_rotation_at`
- `status`: active | pending_rotate | revoked | compromised

### 3.2 RotationPolicy
- период: 30/60/90 дней
- условия: при компрометации, при смене владельца, при изменении прав
- режим: auto (если возможно) или guided (с ручными шагами)
- rollback: что делать при сбое ротации

### 3.3 RotationJob
- `job_id`, `secret_id`
- `planned_at`, `run_at`, `status`
- `steps[]` (пошаговый runbook, может быть “semi‑auto”)
- `result` + ссылки на `evidence_id`

### 3.4 EvidenceEvent
- события: created/read/updated/rotated/revoked/approved
- actor, timestamp, context, request_id, ip/device (если надо)
- ссылки на артефакты (лог, policy decision, approvals)

---

## 4) Потоки (flows) — от простого к сложному

### 4.1 Добавление нового секрета (простое)
1) Пользователь выбирает коннектор и окружение.
2) IFOS показывает форму “что нужно” (см. credential vault requirements).
3) Секрет записывается в Secret Store (через adapter).
4) Создаётся Secret record + audit event.
5) IFOS предлагает policy по умолчанию (например, ротация раз в 90 дней).

### 4.2 Ротация API‑ключа (среднее)
1) Планировщик ставит RotationJob.
2) IFOS вызывает “rotate” capability коннектора (если поддерживается) **или** выдаёт guided‑runbook.
3) Новый ключ сохраняется и тестируется через connector test harness.
4) Старый ключ помечается “revoked/pending revoke” и отзывается после успешного smoke‑test.
5) Записывается evidence pack.

### 4.3 Инцидент: компрометация (сложное)
1) Срабатывает сигнал (SIEM/secret scanning/аномалии).
2) Создаётся incident ticket, присваивается owner.
3) IFOS запускает emergency revoke: отключает коннекторы/flows, отзывает ключи.
4) Ротирует связанные секреты по dependency graph (что зависит от чего).
5) Собирает отчёт: кто имел доступ, какие действия делались, что было затронуто.

---

## 5) Интеграции/зависимости
**Опирается на:**
- `enterprise_connectors_credential_vault` (где и как храним секреты)
- `security_trust` / `policy_engine` (оценка и разрешения)
- `observability_reliability` + `incident_response_postmortems` (события и инциденты)
- `connector_test_harness_ci_cd` (проверка после ротации)
- `service_catalog_topology_ownership` (ownership и blast radius)

---

## 6) Мини‑MVP “готово, чтобы работало”
- секреты не лежат в тексте/коде, только в vault
- есть инвентарь + простая ротация по расписанию
- есть кнопка “Revoke Now” + журнал событий
- есть минимальные policy templates (default / strict)

---

## 7) Что дальше (следующий блок)
Следующий логичный блок: **Certificate Management / PKI & mTLS (75201–75600)** —
управление сертификатами, ACME/PKI, mTLS‑профилями для private connectivity, service mesh и enterprise‑интеграций.
