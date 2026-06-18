# IFOS Block 77201–77600: Data Retention, Legal Hold & eDiscovery

## Зачем этот блок нужен (идея)
Даже если IFOS «операционная система функций», она работает с данными: файлы, сообщения, логи, документы, workflow-артефакты, согласия, доказательства, пакеты поставщиков, метаданные графа знаний.
Чтобы IFOS мог жить в enterprise/регулируемой среде и выдерживать проверки/споры, нужны:

- **Retention**: сколько храним каждый класс данных, где, в каком виде, с каким шифрованием, можно ли удалять.
- **Legal Hold**: при расследовании/суде/инциденте запрещаем удаление выбранных данных (заморозка).
- **eDiscovery**: быстрый сбор и экспорт релевантных материалов в формате, пригодном для юристов/аудита.

Этот блок закрывает «последний юридический контур» вокруг логов/документов/согласий и связывает:
- Privacy/Compliance (DSAR, минимизация),
- Provenance/Attestation (подписи, хэши),
- Case Management (тикеты/дела),
- Export/Packaging (архивы доказательств).

---

## Что делает / не делает

### Делает
1. **Retention Policy Engine**
   - политики хранения по типам сущностей (лог, файл, запись графа, тикет, acceptance evidence),
   - правила по юрисдикциям и планам,
   - lifecycle: hot → warm → cold → delete (или archive).
2. **Legal Hold**
   - создание «дела» (hold case) и критериев отбора,
   - навешивание hold на сущности/коллекции,
   - запрет удаления/перезаписи и фиксация причины.
3. **eDiscovery Export**
   - поиск и сбор данных по делу,
   - формирование экспорт-пакета (zip/manifest),
   - подпись пакета (hooks для sigstore/provenance).
4. **Auditability**
   - журнал действий (кто создал hold, кто снял, кто экспортировал),
   - отчёт по покрытию политик хранения.

### НЕ делает
- Не является полноценной юридической платформой (Relativity/CaseMap и т.п.), но даёт минимально необходимое ядро.
- Не «подменяет» продуктовую privacy-логику; DSAR/удаление данных должны учитывать holds.

---

## Модель данных

### 1) RetentionPolicy
- `policy_id`
- `entity_type` (например: audit_log, file_blob, acceptance_event, message, workflow_run, connector_secret_ref)
- `scope` (workspace/org/product/bundle)
- `jurisdiction` (EU/DE/US/…)
- `retention_days_hot`, `retention_days_warm`, `retention_days_cold`
- `final_action` (delete | archive | anonymize)
- `legal_basis` (опционально: ссылка на норматив/контракт)
- `exceptions` (hold, расследование, безопасность)

### 2) LegalHoldCase
- `case_id`
- `title`, `reason`, `created_by`, `created_at`
- `status` (ACTIVE/SUSPENDED/CLOSED)
- `criteria` (queries/filters)
- `frozen_entity_refs[]` (или ссылка на materialized set)
- `export_history[]`

### 3) HoldBinding
- `binding_id`
- `case_id`
- `entity_ref` (type+id) или `collection_ref`
- `applied_at`, `applied_by`
- `expires_at` (опционально)

### 4) EDiscoveryExport
- `export_id`
- `case_id`
- `created_at`, `created_by`
- `artifact_uri`
- `manifest_hash_sha256`
- `signature_ref` (sigstore/provenance)
- `redaction_profile` (что маскировать)

---

## Потоки

### A) Политика хранения
1. Admin задаёт `RetentionPolicy` (seed-данные дают стартовую матрицу).
2. Job «retention-enforcer» переводит данные по стадиям хранения.
3. При достижении конца срока выполняется `final_action`, если нет hold.

### B) Legal Hold
1. Support/Legal создаёт `LegalHoldCase`.
2. Указывает критерии (по времени, субъекту, сервису, типам данных).
3. Система навешивает hold и блокирует удаление/анонимизацию.
4. Любое действие фиксируется в audit trail.

### C) eDiscovery Export
1. По делу собираются материалы (файлы, логи, сообщения, acceptance, изменения).
2. Формируется manifest + hashes + метаданные.
3. Пакет подписывается и выдаётся по ссылке.

---

## API (минимум)
См. `IFOS_records_hold_ediscovery_api_77201_77600_v1.yaml`.

---

## Definition of Done
- RetentionPolicy CRUD + enforcement job (минимальная реализация)
- LegalHoldCase CRUD + binding + блокировка deletion
- Export для дела (zip + manifest + hashes)
- Seed-матрица политик
