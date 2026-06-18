# IFOS 55201–55600 — Compliance & Policy Engine OS (политики и enforcement) (v1)
Цель: встроить “рациональную дисциплину” в IFOS: правила (policies) не лежат в README, а **работают**:
- блокируют опасные действия
- требуют approvals
- автоматически маскируют PII
- запрещают утечки секретов
- проверяют data contracts
- создают audit trail

Порядок: простое → среднее → сложное.

---

## 55201–55230 — Минимальный Policy Pack (Personal/Team)
Сущности:
- **Policy** (набор правил)
- **Rule** (условие + действие)
- **Decision** (allow/deny/require_approval/mask)
- **AuditEvent** (след действия)

Пример простых правил:
1) Запретить экспорт, если в пакете есть `secret_ref`
2) Маскировать email/телефон при шаринге
3) Требовать 2 approvals при риске high

---

## 55231–55280 — Rule Language (простая DSL)
Правило = WHEN + IF + THEN:
- WHEN: событие (export_pack, ingest, publish_release, share_link_create)
- IF: условия (artifact.type, tags, connector.auth, contains_pii, tenant, region)
- THEN: действие (deny, allow, require_approval(policy_id), mask(strategy), redact(secrets))

DSL (пример):
WHEN export_pack
IF contains(secret_ref) OR contains(api_key)
THEN deny("Secrets must not be exported")

WHEN share_link_create
IF contains_pii = true
THEN mask("pii_basic") AND require_approval("appr.pii.strict")

---

## 55281–55320 — Enforcement Points: где правила “врезаются”
Enforcement hooks:
- Vault: ingest/export/share
- Marketplace: publish/list/install
- Runtime: run/start/stop
- Graph: link creation of certain types (e.g. “asserts_compliance”)
- Change OS: RFC approval gate

Каждый hook вызывает Policy Engine:
Input: context + object refs
Output: decision + required actions

---

## 55321–55370 — PII masking & Redaction
Стратегии:
- pii_basic: email/phone/address частично скрыть
- pii_strict: заменить на tokens + vault‑mapping
- pii_none: разрешено (только для локального личного vault)

Важно:
- маскирование применяется к **экспортам, витринам, шарингу**
- оригинал остаётся в Vault под политикой доступа

---

## 55371–55410 — Secrets handling
Секреты не живут в пакетах:
- хранить в Secret Store (KMS/Vault)
- в артефактах только `secret_ref`
Правила:
- deny export если secret_ref раскрывается
- require security approval если меняется auth flow
- auto-scan (regex + entropy) на ingest

---

## 55411–55460 — Data Contracts & Schema Registry enforcement
Data Contract:
- допустимые поля
- типы
- обязательность
- допустимые значения
- PII classification
Проверки:
- при импорте/ETL: validate
- при публикации: validate
- при выполнении процесса: validate вход/выход

Если контракт нарушен:
- deny или quarantine dataset
- создать task на исправление

---

## 55461–55500 — Audit trails: неизменяемый след
AuditEvent содержит:
- who (actor)
- what (action)
- which objects
- decision
- timestamp
- reason
Режимы:
- basic (team)
- immutable (enterprise, append-only)
- export audit pack (для партнёров/суда)

---

## 55501–55540 — Exceptions & Waivers (исключения без хаоса)
Иногда нужно “обойти” правило:
- waiver_id
- scope (какой объект/пакет)
- кто выдал
- срок действия
- причина
- обязательные компенсирующие меры (monitoring, watermark, ограничение аудитории)

Всё waiver‑ится прозрачно и логируется.

---

## 55541–55580 — Risk scoring (для автоматизации approvals и запретов)
Risk score считает:
- домены: payments, auth, PII, security
- blast radius (из Graph)
- change type (schema/API)
- внешние экспорт/шаринг
Выход:
- low/medium/high
- required approvals set

---

## 55581–55600 — Enterprise: политики по регионам и организациям
Поддержка:
- multi-tenant policy overlays
- EU/DE режим: более строгий для PII
- domain owners (data owner / security owner)
- policy bundles per industry

---

## Итог
Policy Engine — это “право и дисциплина” IFOS:
- рационализация без утечек
- безопасные витрины, шаринг и маркетплейс
- проверяемые данные и контракты
- аудит и исключения по правилам

---

## Что дальше
Следующий блок:
**55601–56000 — Distribution & Sync OS: локальный оффлайн‑vault, синхронизация, конфликт‑резолвер, federation sync**  
Скажете “Продолжение” — сделаю.
