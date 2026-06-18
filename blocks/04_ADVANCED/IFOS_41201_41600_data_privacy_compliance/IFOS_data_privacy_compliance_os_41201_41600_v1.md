# IFOS 41201–41600 — Data Privacy & Compliance OS (v1)
Цель: чтобы IFOS мог **юридически и технически корректно** работать с данными:
- классифицировать (PII/Confidential/Restricted)
- применять политики обработки и минимизации
- управлять согласиями (consent) и целями (purpose limitation)
- поддерживать DSAR (GDPR запросы субъекта данных)
- обеспечивать удаление/удержание (retention/legal hold)
- выдавать “evidence packs” (доказательства комплаенса)

Порядок: простое → среднее → сложное.

---

## 41201–41240 — Data Classification: маркировка данных
**DataClassification** — единый формат меток для datasets/artifacts/logs:
- PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED / PII
- PII subtypes: email, phone, address, id_number, health (если нужно)
- sensitivity score (0–100)
- “allowed zones” (EU-only, on-device-only, no-third-party)

Маркировка нужна, чтобы политики работали автоматически.

---

## 41241–41310 — PII Policies: правила обработки и минимизации
**PIIPolicy** задаёт:
- что запрещено хранить (например raw ID)
- где можно обрабатывать (edge vs cloud)
- маскирование (redaction) и токенизацию
- encryption requirements (at rest/in transit)
- правила экспорта (no export of PII to public links)

В IFOS это должно быть применимо к любому “run”.

---

## 41311–41370 — Consent & Purpose Limitation: согласие и цель
**ConsentRecord**:
- subject_id (псевдо‑идентификатор)
- кто дал согласие (канал)
- цели (purposes) и сроки
- отзыв согласия (revocation)
- доказательства (timestamp + signature)

**Purpose limitation**:
- если purpose=“support”, нельзя использовать для “marketing” без отдельного согласия

---

## 41371–41430 — RoPA / Processing Activities: реестр обработки
**ProcessingActivity** (аналог RoPA):
- какой процесс (workflow/bundle)
- какие категории данных
- цели обработки
- получатели (processors/subprocessors)
- сроки хранения
- меры защиты
- lawful basis (например consent, contract, legitimate interest)

Это “паспорт процесса” для B2B и контроля.

---

## 41431–41510 — DSAR Workflows: запросы субъекта данных
**DSARRequest**:
- type: access / deletion / rectification / portability
- verify identity (процедура)
- scope (какие datasets/artifacts затронуты)
- исполнение (orchestrated jobs)
- отчёт пользователю (что удалено/что нельзя удалить из-за legal hold)

DSAR должен “пробегать” по lineage и находить связанную информацию.

---

## 41511–41550 — Redaction / Anonymization Jobs: механика
**RedactionJob**:
- маскирование PII в текстах/логах/экспортах
- правила: keep last4, hash-email, replace tokens

**AnonymizationJob**:
- k-anonymity/aggregation (упрощённо)
- удаление идентификаторов + перестройка статистики

Важно: отличать “анонимизацию” от “псевдонимизации”.

---

## 41551–41580 — Retention & Legal Hold: сроки и удержание
**RetentionPolicy**:
- сколько хранить (by class)
- условия удаления (по DSAR, по сроку)
- “архив вместо удаления” (если допустимо)

**LegalHold**:
- запрет удаления (расследование/суд/аудит)
- кто поставил hold и на какой срок

---

## 41581–41600 — Compliance Evidence Packs: доказательства комплаенса
**ComplianceEvidencePack** включает:
- какие политики действовали
- где хранились данные (region)
- кто имел доступ (audit links)
- какие операции были выполнены (transform/execution refs)
- подтверждение удаления/маскирования
- подписи и хэши (целостность)

Это то, что вы отдаёте аудитору или enterprise-клиенту.

---

## Итог
Этот блок делает IFOS “GDPR-ready”:
- данные классифицированы
- согласия/цели формализованы
- DSAR выполняется по графу lineage
- сроки хранения соблюдаются
- есть доказательства комплаенса

---

## Что дальше
Следующий блок:
**41601–42000 — Localization & Internationalization OS** (языки, форматы, валюты, правовые зоны, локальные витрины, multi-locale ranking).  
Скажете “Продолжение” — сделаю.
