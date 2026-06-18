# IFOS 15241–15600 — Enterprise‑OS: multi‑tenant, RBAC/ACL, usage‑billing, GDPR/retention, audit, SSO, и федерация маркетплейсов (v1)

Этот блок — “сверхслой” над Runtime и Marketplace. Он нужен, чтобы IFOS стал **операционной системой** для компаний/сообществ,
а не просто набором скриптов:

- **Multi‑tenant**: разные организации изолированы (данные, секреты, jobs, evidence).
- **RBAC/ACL**: “вертикаль власти” в терминах доступа, ролей и полномочий.
- **Billing / Metering**: тарификация “по использованию” (runs, steps, requests, storage, verified evidence).
- **GDPR / Retention**: хранение логов и evidence по правилам, PII‑режимы, сроки, право на удаление.
- **Audit / Observability**: кто что делал, когда, с какими данными, с trace‑id, с неизменяемым журналом.
- **SSO / SCIM**: корпоративный вход и управление пользователями.
- **Federation**: несколько узлов маркетплейса/реестра (локальные “гильдии”), синхронизация доверия и артефактов.

Ниже — по порядку: от простого к сложному.

---

## 15241–15280 — Multi‑tenant модель (простое → среднее)

### 15241) Термины
- **Tenant**: организация/проект/сообщество (например “TravelHub GmbH”).
- **Workspace**: пространство внутри tenant (например “Production”, “Sandbox”, “R&D”).
- **Resource**: job/run/recipe/bundle/listing/evidence/secret.
- **Boundary**: граница доступа (tenant_id, workspace_id).

### 15242) Три уровня изоляции
1) **Logical isolation** (MVP): tenant_id в каждой таблице/объекте, строгие проверки в API.
2) **Cryptographic isolation**: ключи/секреты шифруются per‑tenant.
3) **Physical isolation**: отдельные базы/инстансы (enterprise).

### 15243) Встроенная безопасность по умолчанию
- Любой ресурс имеет owner tenant_id.
- Любой запрос несёт subject (user/service) + tenant context.
- Любая операция проверяется policy engine (RBAC/ACL).

---

## 15281–15340 — RBAC/ACL и Policy Engine (среднее)

### 15281) Почему RBAC недостаточно
RBAC отвечает на “кто” (роль), но не на “контекст”.
Например:
- “Verifier может публиковать evidence” — но только **L2/L3** и только **не для money/security_sensitive** без второго подтверждения.

Поэтому:
- RBAC = базовая сетка ролей
- ACL/ABAC = контекст (resource flags, environment, time, approval).

### 15282) Базовые роли (MVP)
- Owner (полный доступ)
- Admin (управление пользователями/политиками)
- Builder (создаёт recipes/jobs/bundles)
- Operator (запускает/мониторит jobs)
- Verifier (подтверждает evidence L2/L3)
- Moderator (policy/security, marketplace)
- Auditor (только чтение, отчёты)

### 15283) Policy Engine (MVP)
Policy принимает:
- subject (user/service)
- action (create_job, run_job, publish_evidence…)
- resource (job/listing/evidence…)
- context (tenant_id, flags pii/money, mode sandbox/production)
и выдаёт: ALLOW / DENY / ALLOW_WITH_CONDITIONS (например “нужна 2FA”).

---

## 15341–15410 — Billing/Metering (от среднего к сложному)

### 15341) Зачем billing
Чтобы “миллионы функций” могли быть:
- бесплатными,
- по подписке,
- “по запуску”,
- “по шагам/запросам/хранилищу”.

### 15342) Что считаем (метрики)
- runs_count
- steps_count
- external_requests_count
- artifacts_storage_mb_day
- verified_evidence_count
- marketplace_downloads (сигнал, но не основной)

### 15343) Usage event
Runtime после каждого run пишет usage_event (immutable):
- tenant_id, job_id, run_id
- meters: runs=1, steps=12, requests=5, storage_mb=0.3
- policy flags (pii/money)
- timestamp

### 15344) Invoice
Биллинг агрегирует usage events → invoice:
- период (month)
- план/тариф
- итог и детализация по meters
- налоговые поля (опционально, позже)

---

## 15411–15480 — GDPR/PII и Retention (сложное, критичное)

### 15411) Классы данных
- **Public**: документация, публичные listings
- **Internal**: configs без PII
- **Sensitive**: секреты, токены, доступы
- **PII**: персональные данные (имена, email, идентификаторы клиентов)
- **Financial**: платежи, счета

### 15412) Retention policy
Каждый tenant может задать:
- сколько хранить run logs
- сколько хранить artifacts
- нужно ли “forget” (удаление) или “anonymize”
- требования к шифрованию at-rest
- запрет на публикацию evidence для pii=true

### 15413) “Redaction-first” принцип
Любой run_record и evidence должны:
- вычищать секреты
- опционально вычищать PII (masking/hashed)
- хранить “минимально достаточное”

---

## 15481–15540 — Audit & Observability (сложнее)

### 15481) Audit log ≠ обычный лог
Audit log должен быть:
- структурированный (JSON)
- неизменяемый (append-only)
- подписываемый/хэшируемый (chain) хотя бы в enterprise режиме
- пригодный для проверки “кто сделал”

### 15482) Что записываем
- auth events (login, token issued)
- admin changes (roles, policies, retention)
- sensitive operations (read_secret, publish_evidence, install_bundle)
- execution events (job run triggered, sandbox denied)

### 15483) Traceability
- trace_id связывает: request → job → run → evidence → marketplace публикацию.

---

## 15541–15580 — SSO / SCIM (enterprise уровень)

### 15541) SSO
Поддержка:
- OIDC (Azure AD / Google Workspace / Keycloak)
- SAML (классика enterprise)

### 15542) SCIM (управление пользователями)
- auto‑provisioning пользователей
- синхронизация групп → роли IFOS

### 15543) Least privilege по умолчанию
Новый пользователь получает роль Viewer/Operator минимум, пока админ не расширит.

---

## 15581–15600 — Federation (самый высокий уровень)

### 15581) Зачем федерация
Потому что:
- один marketplace не покрывает всё
- компании хотят внутренний “реестр кнопок”
- сообщества хотят свой узел, но с обменом trust/evidence

### 15582) Модель узлов
- Node A (internal) публикует bundles, приватные connectors
- Node B (community) публикует open recipes
- Node C (enterprise) принимает только signed artifacts

### 15583) Что синхронизируем
- listings metadata
- trust scores (с объяснениями)
- evidence summaries (без секретов)
- подписи и хэши артефактов
- blacklist/allowlist издателей (опционально)

---

## Приложения (в этом пакете)
- Schemas: tenant, RBAC policy, audit event, usage event, billing plan, invoice, retention, sso, federation
- Specs: multi‑tenant, RBAC/ACL, billing, GDPR, audit, SSO/SCIM, federation
- OpenAPI: Enterprise API (MVP)
- Examples: один tenant + политики + usage + invoice + federation sync event
- Python skeletons: policy engine + usage billing aggregator
