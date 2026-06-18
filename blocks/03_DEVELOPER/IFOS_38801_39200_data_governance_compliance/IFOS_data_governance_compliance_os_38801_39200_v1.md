# IFOS 38801–39200 — Data Governance & Compliance OS (v1)
Цель: чтобы IFOS мог работать в реальном мире (B2B, гос, медицина, финансы), где важны:
- персональные данные (PII)
- согласия (consent)
- сроки хранения (retention) и удаление
- лицензии и авторские права
- экспорт/портируемость
- аудит и юридический след
- legal hold (заморозка удаления при спорах)

Порядок: простое → среднее → сложное.

---

## 38801–38830 — Data Classification: что за данные и насколько они чувствительны
DataClassification = объектная маркировка данных:
- PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED
- PII: имена, адреса, телефоны
- Special categories (GDPR Art. 9): здоровье, биометрия, убеждения и т.д.
- FIN: платежи, IBAN, карты
- CRED: логины/токены/секреты

Маркировка используется в UI (баннеры), в политике доступа, в DLP, в экспортах.

---

## 38831–38870 — Consent Record: согласие на обработку/передачу
ConsentRecord фиксирует:
- кто дал согласие (subject_id)
- на что (purpose: support, billing, analytics)
- кому (processors/subprocessors)
- срок действия
- каналы отзыва
- доказательства (timestamp, form snapshot, hash)

Без consent’ов автоматизация превращается в юридический риск.

---

## 38871–38920 — Retention Policy: сроки хранения
RetentionPolicy описывает:
- какие данные (по классам/тегам/таблицам)
- сколько хранить (days/months)
- что делать после срока (delete/anonymize/archive)
- исключения (legal_hold)
- минимальный лог аудита

Это “таймеры жизни данных”.

---

## 38921–38960 — Deletion Job: управляемое удаление
DeletionJob — это не “rm -rf”, а процесс:
- подготовка (precheck: legal hold? зависимости?)
- удаление по каскаду (attachments, derived artifacts)
- подтверждение (approvals для RESTRICTED)
- отчёт (сколько удалено, что нельзя удалить)
- доказательство удаления (audit trail)

---

## 38961–39010 — DLP Policy: защита от утечек
DLPPolicy задаёт:
- сигнатуры (email/IBAN/паспорт/медицинские коды)
- правила блокировки (например, запрет отправки PII во внешние webhooks)
- маскирование (redact)
- режимы: warn / block / quarantine
- исключения по ролям и согласиям

DLP = “предохранитель” в экосистеме плагинов.

---

## 39011–39050 — License Record: лицензии и авторские права
LicenseRecord фиксирует:
- источник (repo/marketplace/import)
- тип лицензии (MIT/Apache/GPL/Commercial)
- ограничения (redistribution, attribution)
- совместимость (license compatibility)
- обязательства (NOTICE файлы)

Это решает “хаос WordPress”: кто что может использовать и продавать.

---

## 39051–39100 — Export & Portability: выгрузка данных
ExportRequest поддерживает:
- формат (JSON/CSV/Parquet/Bundle)
- фильтры (по проекту, по датам)
- включение/исключение PII (mask/anonymize)
- подпись архива и контроль целостности
- журнал: кто запросил и зачем

Плюс: “удаляемость” должна сопровождаться “портируемостью”.

---

## 39101–39150 — Audit Event: юридический след
AuditEvent фиксирует:
- кто (actor)
- что сделал (action)
- над чем (resource)
- когда (ts)
- откуда (ip/device)
- результат (success/fail)
- ссылки на run/workflow/tool

Audit — это “черный ящик”, но для закона и расследований.

---

## 39151–39180 — Legal Hold: запрет удаления при споре
LegalHold:
- основания (дело, жалоба, проверка)
- список объектов/датасетов
- сроки и ответственные
- влияние: блокирует deletion jobs, меняет retention

---

## 39181–39200 — Compliance Policy Pack: сборка политики под отрасль
PolicyPack = набор:
- классификация + DLP + retention + export defaults
- шаблоны consent форм
- отраслевые профили (healthcare/finance/public sector)
- checklists и “что должно быть включено”

Это позволяет “включить режим GDPR” или “режим медданных” одной настройкой.

---

## Итог блока
Data Governance & Compliance OS превращает IFOS в “enterprise‑ready”:
- данные размечены
- согласия учитываются
- сроки хранения управляются
- утечки предотвращаются
- лицензии не теряются
- экспорт и аудит работают
- legal hold защищает от ошибок

---

## Что дальше
Следующий блок:
**39201–39600 — Federation & Multi‑Tenant OS** (мультиорганизации, шардирование, синхронизация, trust boundaries, cross‑tenant sharing).  
Скажете “Продолжение” — сделаю.
