# IFOS 54401–54800 — Document & Artifact Vault OS (хранилище документов и артефактов) (v1)
Цель: сделать “хранилище правды” для IFOS:
- документы (MD/DOCX/PDF/HTML)
- данные (CSV/JSON)
- бинарные артефакты (bundle packs, модели, плагины)
- отчёты запусков, логи‑выжимки
- share packs для партнёров/аудита

Ключевые свойства:
1) **дедупликация** (один файл хранится один раз)
2) **версии и снапшоты** (что было в системе на дату X)
3) **provenance** (откуда взялось и кто менял)
4) **подписи** (доказуемость)
5) **безопасный шаринг** (сроки, права, без секретов)

Порядок: простое → среднее → сложное.

---

## 54401–54430 — Object Model: что хранит Vault
### Blob (сырой байтовый объект)
- content_hash (sha256)
- size
- mime_type
- encryption_ref (если зашифровано)

### Artifact (осмысленный объект)
- artifact_id
- type: document | dataset | bundle_pack | run_report
- metadata: title, tags, owner, project
- blob_refs[]

### BundlePack / SharePack
- manifest.json
- список файлов + хэши
- зависимости и версии

---

## 54431–54480 — Storage & Dedup: как хранить эффективно
Стратегия:
- content-addressed storage: путь = hash
- индекс метаданных отдельно (DB)
- дедуп “по содержимому”, а не по имени
Поддержка:
- multipart upload (для больших файлов)
- chunking (опционально)
- garbage collection (по retention)

Плюс: “квази‑Git LFS” для бинарей.

---

## 54481–54520 — Versioning & Snapshots: “состояние системы на дату”
Snapshot:
- список объектов (bundles, policies, datasets, docs)
- их версии
- подпись снапшота
Сценарии:
- “release snapshot” (перед публикацией)
- “incident snapshot” (когда всё сломалось)
- “audit snapshot” (для проверки)
UI: выбрать дату → увидеть набор артефактов → восстановить.

---

## 54521–54560 — Provenance & Signatures: доказуемость и происхождение
Provenance record:
- source: upload | import | runtime | external
- actor (user/service)
- time
- transformations (normalize, dedup, redact)
- evidence links (run_id, connector, URL)
Signatures:
- подпись артефакта/пакета
- подпись снапшота
Важно для:
- комплаенса
- споров
- “кто изменил и почему”

---

## 54561–54600 — Access & Sharing: “поделиться безопасно”
Share link:
- scope (one artifact / project pack)
- permissions (view/download)
- expiry (TTL)
- watermarking (для PDF опционально)
- audit trail (кто скачал)

Правило:
- share packs автоматически **редактируют секреты**
- PII masking по политике

---

## 54601–54640 — Security: шифрование, ключи, изоляция
- encryption at rest (KMS)
- encryption in transit
- per-tenant isolation
- signed URLs
- malware scanning (на ingest)
- immutable storage для “legal hold”

Уровни:
- personal (локальный vault)
- team (мульти‑тенант)
- enterprise (S3 compatible + HSM/KMS)

---

## 54641–54690 — Imports: как загружать из внешнего мира
Импорт из:
- Google Drive/Dropbox/S3
- GitHub releases
- WordPress media library
- Make.com scenario exports
- email attachments (опционально)
Пайплайн:
- ingest job → virus scan → normalize → classify → link to project
Результат: артефакты появляются в Knowledge Worker OS и Graph.

---

## 54691–54740 — Exports & Packs: как отдавать “как продукт”
Экспорт форматов:
- single artifact download
- project share pack (ZIP)
- release bundle pack
- audit pack (ZIP+manifest+signatures)
Каждый pack:
- manifest.json
- hashes
- dependency list
- policy summary (“что скрыто/замаскировано”)

---

## 54741–54780 — Retention & Legal Hold: хранение по правилам
Retention policy:
- default TTL по типам
- правила удаления (GDPR: право на удаление)
- legal hold (заморозка удаления)
- version pinning (сохранить конкретные версии)
Нужно для:
- аудита
- споров
- безопасности

---

## 54781–54800 — Performance & Scaling: чтобы работало на 50+ ГБ и больше
Оптимизации:
- дедуп уменьшает объём
- “холодные” данные в дешёвом хранилище
- кеш метаданных и превью
- параллельный ingest
Плюс: offline mode (локальный vault) + sync.

---

## Итог
Vault OS превращает IFOS в “производственную систему знаний”:
- хранение без хаоса
- доказуемость
- безопасный обмен
- снапшоты для восстановления

---

## Что дальше
Следующий блок:
**54801–55200 — Collaboration & Change Management OS: совместная работа, задачи, workflow изменений, RFC, approvals, release trains**
Скажете “Продолжение” — сделаю.
