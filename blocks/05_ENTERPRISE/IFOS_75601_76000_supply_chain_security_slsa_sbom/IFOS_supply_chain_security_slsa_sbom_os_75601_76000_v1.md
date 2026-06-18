# IFOS · Supply‑Chain Security (SLSA/SBOM/Подписи артефактов)

**Диапазон:** 75601–76000

## 1. Зачем нужен этот блок

Этот блок защищает цепочку поставки (supply chain) для IFOS‑артефактов:
- пакеты коннекторов, blueprint‑пакеты, шаблоны, «one‑click bundles», плагины, runtime‑модули;
- защищает от подмены, вредоносных зависимостей и «заражённых» билдов;
- добавляет **проверяемое происхождение** (provenance) и **описание состава** (SBOM).

Идея: любой артефакт в Marketplace и при установке/запуске должен быть:
1) **подписан**, 2) иметь **прозрачное происхождение**, 3) (по мере зрелости) — иметь **SBOM**.

## 2. Границы ответственности

### 2.1 Делает
- Генерирует и хранит **подписи** для артефактов (bundle/package).
- Хранит **аттестации** (provenance, build info, тесты, сканы).
- Принимает/публикует **SBOM** (список компонентов/зависимостей).
- Проверяет артефакты при:
  - публикации (publisher workflow),
  - установке (installer),
  - запуске (runtime gate).
- Применяет политики (Policy Engine):
  - «без подписи не ставить»,
  - «без SBOM — только в sandbox»,
  - «минимальный уровень доверия для прод».

### 2.2 Не делает
- Не является полноценной CVE‑базой: источник уязвимостей — внешние фиды/сканеры.
- Не делает «идеальный детектор вредоносного кода» — только верификация происхождения и политика допуска.
- Не заменяет CI/CD: он **подключается** к CI/CD и хранит результаты.

## 3. Сущности (Data Model)

### 3.1 Artifact
- `artifact_id`, `type` (connector, bundle, template, runtime-module),
- `digest` (sha256), `version`, `publisher_id`,
- ссылки на `signature`, `sbom`, `attestations`.

### 3.2 Signature
- алгоритм, key_id, подпись для digest, время, issuer/publisher.

### 3.3 SBOM
- формат (CycloneDX/SPDX‑подобный), версия, контент/ссылка на объект‑хранилище.

### 3.4 Attestation (Provenance)
- build pipeline id, commit hash, build environment,
- результаты тестов/сканов,
- уровень доверия (например, «уровни зрелости»).

### 3.5 PolicyRule
- scope: tenant/org/workspace/environment,
- требования: signature_required, sbom_required, min_trust_level,
- allow/deny по издателю и типу артефакта.

## 4. Основной поток (публикация → установка → запуск)

### 4.1 Публикация (Publisher)
1) Publisher собирает артефакт (build).
2) CI генерирует digest.
3) Генерируется signature + provenance attestation.
4) (Опционально) генерируется SBOM.
5) Marketplace принимает артефакт только если проходит policy‑gate.

### 4.2 Установка (Installer)
1) При установке вычисляется digest скачанного пакета.
2) Проверяется подпись (signature → key → publisher).
3) Проверяются policy‑правила среды:
   - sandbox допускает слабее,
   - prod требует больше.
4) Если всё ок — артефакт помещается в локальный cache/registry.

### 4.3 Запуск (Runtime)
1) Перед запуском workflow/коннектора runtime сверяет digest.
2) Проверяет, что policy для workspace разрешает запуск.
3) Логирует решение (почему разрешено/почему запрещено).

## 5. Минимальные интерфейсы (контракт)

- `POST /supply-chain/artifacts/register`
- `POST /supply-chain/signatures/submit`
- `POST /supply-chain/attestations/submit`
- `POST /supply-chain/sbom/submit`
- `POST /supply-chain/verify` — проверить артефакт для install/run
- `GET  /supply-chain/policies` / `POST /supply-chain/policies`

## 6. Интеграции IFOS

- **Publishing / Release Workflow (46001–46400):**
  - точка, где publisher workflow вызывает проверки.
- **Connector Test Harness / CI-CD (62401–62800):**
  - генерирует тесты, сканы, attestation.
- **KMS / Secrets Rotation (74801–75200):**
  - ключи подписи, ротация signing keys.
- **Trust & Safety / Moderation (48401–48800):**
  - контент‑политики и репутация издателей.
- **Compliance / Policy Engine (55201–55600):**
  - правила допуска в разных средах.

## 7. MVP по уровням зрелости

### 7.1 P0 (самое простое)
- Подпись артефактов и проверка подписи при install/run
- Хранение digest + publisher mapping
- Простые policy rules

### 7.2 P1 (средний уровень)
- Присоединение SBOM
- Базовые attestations (build info + тесты)
- Проверка «publisher‑reputation» и allowlist

### 7.3 P2 (advanced / enterprise)
- Полноценные provenance‑аттестации (SLSA‑подобные)
- Гейты в progressive delivery / rollbacks
- Интеграция с внешними vulnerability feeds
- Наблюдаемость: метрики «blocked installs», причины

## 8. Acceptance Criteria
- Любой пакет/бандл имеет digest и подпись.
- Установка запрещается при несовпадении digest/подписи.
- Политика различает sandbox vs prod.
- SBOM хранится и доступен для просмотра (когда включено).
