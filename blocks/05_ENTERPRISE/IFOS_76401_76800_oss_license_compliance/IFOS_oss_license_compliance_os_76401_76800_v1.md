# IFOS 76401–76800: OSS License Compliance, Attribution & Notices

## 1. Зачем нужен этот блок
Этот блок добавляет в Internet Function OS (IFOS) **контур лицензий Open Source (OSS)** и правовых обязательств:
- автоматическая проверка лицензий зависимостей и артефактов (SCA / license scanning),
- управление **политиками лицензирования** (allow/deny/условно-разрешено),
- формирование **атрибуции** и файлов уведомлений (NOTICE / THIRD_PARTY_NOTICES),
- выпуск **отчётов о соответствии** и *gating* релизов по требованиям лицензий.

Цель: чтобы IFOS мог безопасно и юридически корректно **пакетировать**, **распространять** и **монетизировать** решения/бандлы, не создавая лицензионных рисков и нарушений.

## 2. Что этот блок НЕ делает (границы)
- Не заменяет юридическую экспертизу в спорных кейсах (он готовит доказательства и отчёты).
- Не «определяет» автоматически окончательную лицензию там, где нет данных (фиксирует неопределённость и требует подтверждения).
- Не делает сборку/компиляцию ПО — он проверяет **результаты сборки** (SBOM, артефакты, манифесты).

## 3. Основные понятия
- **SBOM** (Software Bill of Materials): список компонентов/зависимостей (SPDX / CycloneDX).
- **SCA** (Software Composition Analysis): анализ зависимостей (лицензии, уязвимости, provenance).
- **License obligations**: обязательства (атрибуция, копирайты, предоставление исходников, ограничения copyleft и т.д.).
- **Policy**: правила организации/маркетплейса, что допустимо включать в бандлы/витрины.
- **Exception**: оформленное исключение с ответственным лицом, сроком, областью и обоснованием.

## 4. Входы/выходы
### 4.1 Входы
- SBOM: `spdx.json`, `spdx.rdf`, `cyclonedx.json/xml`
- Манифесты: `package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `go.sum`, `Cargo.lock`
- Артефакты: контейнер-образы (digest), релизы, бандлы IFOS
- Результаты сканеров: findings (license matches, copyright)

### 4.2 Выходы
- **Policy Decision**: PASS / WARN / FAIL + причины
- **Attribution Bundle**: NOTICE / THIRD_PARTY_NOTICES + список лицензий
- **Compliance Report**: HTML/Markdown/PDF
- **Audit log**: кто и когда утвердил исключение, какой релиз разрешён

## 5. Модель данных (канонические сущности)
### 5.1 LicensePolicy
- `policy_id`, `name`, `scope` (org/workspace/bundle/registry)
- `allow_list[]`, `deny_list[]`, `review_required[]`
- `copyleft_rules` (например: запрещать AGPL в SaaS, требовать approval для GPL)
- `default_action` (WARN/FAIL)
- `effective_from`, `effective_to`

### 5.2 Component
- `purl`, `name`, `version`, `digest`
- `license_declared`, `license_concluded`, `license_evidence[]`
- `copyrights[]`
- `source_location` (repo url/commit, если известно)

### 5.3 SBOM
- `sbom_id`, `format`, `source` (build/pipeline/registry)
- `artifact_ref` (bundle_id/image_digest)
- `components[]` (refs)
- `generated_at`, `generator`

### 5.4 Finding
- `finding_id`, `type` (license/copyright/notice)
- `component_ref`, `confidence`, `evidence[]`
- `severity` (info/warn/block)
- `recommended_action`

### 5.5 Obligation
- `obligation_id`, `kind` (attribution/source_offer/notice/include_license_text)
- `applies_to` (component/bundle/release)
- `due_by` (release time) / `status`

### 5.6 ExceptionApproval
- `exception_id`, `policy_id`, `scope`
- `approved_by`, `approved_at`, `expires_at`
- `rationale`, `risk_notes`, `mitigations`

### 5.7 PolicyDecision
- `decision_id`, `policy_id`, `target_ref` (bundle/release/build)
- `result` (PASS/WARN/FAIL)
- `reasons[]`, `blocked_components[]`
- `created_at`, `created_by`

## 6. Ключевые функции (Capabilities)
1. **Ingest SBOM**: загрузка/нормализация SBOM и локфайлов.
2. **License detection**: сопоставление лицензий по данным SBOM + эвристика по файлам.
3. **Policy evaluation**: расчёт решения PASS/WARN/FAIL.
4. **Obligation planner**: вычисление обязательств (NOTICE, текст лицензии, source offer).
5. **Attribution generator**: сборка файлов уведомлений и списка компонентов.
6. **Exception workflow**: запрос/утверждение исключений с аудитом.
7. **Release gate**: интеграция с релизами/прогрессивной доставкой (canary/rollback).
8. **Continuous monitoring**: пересканирование при обновлении зависимостей/политик.

## 7. API (минимальный контракт)
### 7.1 Policies
- `GET /license/policies`
- `POST /license/policies`
- `GET /license/policies/{policy_id}`
- `POST /license/policies/{policy_id}:evaluate` (target_ref -> decision)

### 7.2 SBOM & Findings
- `POST /sboms` (upload)
- `GET /sboms/{sbom_id}`
- `GET /sboms/{sbom_id}/findings`

### 7.3 Decisions & Gates
- `GET /decisions/{decision_id}`
- `POST /gates/license` (bundle/release -> PASS/WARN/FAIL)

### 7.4 Attribution / Notices
- `POST /attributions:generate` (sbom_id + policy_id -> bundle)
- `GET /attributions/{attr_id}` (download)

### 7.5 Exceptions
- `POST /exceptions`
- `POST /exceptions/{exception_id}:approve`
- `POST /exceptions/{exception_id}:revoke`

## 8. Основные сценарии (Workflow)
### 8.1 PR / Merge Check (dev)
1) CI строит SBOM и публикует в IFOS.
2) IFOS считает PolicyDecision.
3) Если WARN/FAIL — CI annotates PR (компоненты и причины).
4) При необходимости создаётся ExceptionApproval (в рамках org policy).

### 8.2 Release Gate (prod)
1) Перед релизом IFOS пересчитывает policy на финальном артефакте.
2) Генерирует Attribution Bundle и прикладывает к релизу.
3) Если FAIL — блокирует публикацию/прогрессивную доставку.

### 8.3 Marketplace Publishing
1) При публикации пакета/бандла маркетплейс вызывает `POST /gates/license`.
2) IFOS проверяет лицензии + obligations.
3) Публикация возможна только при PASS (или при WARN + approved exception).

## 9. UI/Отчёты
- Dashboard: top denied licenses, компоненты на review, тренды.
- Drill-down: компонент -> доказательства -> обязательства.
- Экспорт: HTML/MD, интеграция в release notes.

## 10. Интеграции и зависимости
Зависимости (логические):
- **43201–43600 Data Contracts / Schema Registry**: единые контракты SBOM/Findings/Decisions.
- **43601–44000 Import & Normalization**: импорт локфайлов и артефактов.
- **76001–76400 Sigstore Attestation**: привязка SBOM/сканов к provenance и подписи.

## 11. Критерии готовности (Definition of Done)
- Есть как минимум 1 политика по умолчанию (allow/deny/review).
- IFOS принимает SBOM, выдаёт findings и decision.
- Генерируется NOTICE/THIRD_PARTY_NOTICES из SBOM.
- Есть workflow исключений с аудитом.
- Есть интеграция gate в пайплайн публикации пакетов.
