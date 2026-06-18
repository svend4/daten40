# IFOS 36001–36400 — Enterprise Identity & Access OS (v1)
Цель: IFOS должен работать как “B2B операционная система интернета”:
- много организаций (tenants)
- орг‑структура (org units)
- пользователи и сервис‑аккаунты
- роли (RBAC) + правила по атрибутам (ABAC)
- ключи API и сессии
- SSO (SAML/OIDC)
- аудит и неизменяемые журналы
- BYOK (ключи шифрования клиента)
- делегированное администрирование (delegated admin)

Порядок: простое → среднее → сложное.

---

## 36001–36040 — Tenant: изоляция организаций
### Tenant
Tenant = “компания/организация” в IFOS.
Содержит:
- tenant_id, billing_profile, security_profile
- default policies (PII logs off, egress allowlist)
- data residency (EU/DE/…)

Изоляция:
- данные, ключи, журналы — строго tenant‑scoped.

---

## 36041–36090 — Org Units: структура “как в реальной компании”
### OrgUnit
Орг‑юниты:
- /HQ/IT
- /HQ/Finance
- /Branch/Berlin

Зачем:
- ограничения доступа (“финансы видят только финансы”)
- раздельные cost centers
- разные политики безопасности

---

## 36091–36130 — Users, Service Accounts, Sessions
### User
Пользователь:
- user_id, email, display_name
- status (active/blocked)
- org_unit_id

### Session
- session_id, user_id
- expires_at, scopes
- device metadata

---

## 36131–36190 — Permissions + Roles (RBAC)
### Permission
Разрешения — атомарные права:
- registry.read
- bundle.install
- bundle.run
- secrets.read
- audit.view
- billing.manage

### Role
Роль — набор permissions:
- Viewer
- Operator
- Admin
- SecurityOfficer
- BillingAdmin

RBAC быстро решает “кто что может”.

---

## 36191–36250 — ABAC: правила по атрибутам (тонкая гранулярность)
### ABACPolicy
ABAC нужен, когда RBAC недостаточно:
- “можно запускать только bundles с tag=‘safe’”
- “запрещены коннекторы вне EU”
- “PII доступен только роли SecurityOfficer и только для incident расследования”

ABAC оценивает:
- user attributes (role, org_unit)
- resource attributes (tags, risk, connector region)
- context attributes (time, ip, device)

---

## 36251–36290 — API Keys: автоматизация и интеграции
### ApiKey
- key_id, name, scopes
- expires_at
- rate limits
- last_used_at
- rotate policy

Нужно для CI/CD, агентов, сервер‑сервер вызовов.

---

## 36291–36340 — SSO: вход через корпоративный IdP
### SSOConfig
Поддержка:
- OIDC (Azure AD / Google Workspace / Okta)
- SAML (enterprise)

SSOConfig хранит:
- issuer, client_id
- allowed domains
- group mapping → roles
- MFA requirement (policy)

---

## 36341–36370 — Audit: кто что сделал и когда
### AuditEvent
События:
- login/logout
- install/uninstall bundle
- secrets read/write
- policy change
- publish job approve

Audit требования:
- append-only
- immutable option (WORM)
- export for compliance

---

## 36371–36390 — BYOK: клиентские ключи шифрования
### BYOK
- key_ref (KMS/HSM)
- envelope encryption
- key rotation schedule
- per-tenant encryption contexts

Важное: IFOS не видит “мастер‑ключ”, только использует KMS вызовы.

---

## 36391–36400 — Delegated Admin
### Delegation
Делегирование:
- tenant admin → org unit admin
- scope (which permissions)
- time-bounded
- audit required

Это помогает масштабировать управление без хаоса.

---

## Итог блока
Enterprise I&A OS делает IFOS пригодным для:
- компаний
- ведомств
- B2B/B2G проектов
- мульти‑тенантных хабов

---

## Что дальше
Следующий блок:
**36401–36800 — Compliance & Data Governance OS** (GDPR, data retention, DLP/PII scanning, export/erasure requests, legal holds).  
Скажете “Продолжение” — сделаю.
