# IFOS 68001–68400 — Reproducible Builds & Signing OS (v1)
**Цель блока:** превратить публикацию коннекторов/пакетов в marketplace в **повторяемый, проверяемый и доверенный** процесс.
Это то, что превращает “хаотичный интернет” в “учтённое поле”: любой пакет имеет **манифест, рецепт сборки, SBOM, provenance, подпись и политику проверки**.

Связи:
- продолжает **Developer Onboarding OS** (67601–68000)
- использует **Security & Trust OS** (34401–34800)
- влияет на **Marketplace Curation & Quality** (45601–46000)
- влияет на **Enterprise Governance** (34001–34400)

Порядок: простое → среднее → сложное.

---

## 68001–68060 — Простое: Package Manifest (что именно публикуем)
**PackageManifest** — “паспорт” артефакта:
- package_id, version, vendor, license
- type: connector | workflow_pack | ui_widget | trial_bundle
- inputs/outputs (какие данные трогает)
- required permissions/scopes
- runtime requirements
- hashes (чтобы не подменили)

Минимум: без manifest публикация запрещена.

---

## 68061–68120 — База: Build Recipe (как собрать одинаково)
**BuildRecipe** описывает сборку:
- source_ref (git commit/tag)
- build environment (container image / toolchain)
- dependency lock (lockfile / pinned versions)
- build steps (команды)
- outputs (что получится)
- deterministic flags

Цель: любая команда/сервер может повторить сборку и получить тот же hash.

---

## 68121–68180 — Среднее: SBOM (из чего состоит пакет)
**SBOM** (Software Bill of Materials) фиксирует:
- зависимости (direct/transitive)
- версии
- лицензии
- уязвимости (по базе)
- “входные артефакты” (контейнер/бинарники)

Зачем:
- marketplace может показывать “состав”
- enterprise может запретить лицензии/пакеты
- trust score учитывает риск

---

## 68181–68240 — Среднее+: Provenance + Attestation (кто и как собрал)
**Provenance**:
- кто запускал сборку (actor, org)
- где (runner id, CI system)
- когда
- из какого источника
- какие шаги

**Attestation**:
- утверждение: “SBOM соответствует”, “build reproducible”, “tests passed”, “sandbox smoke ok”
- привязка к hash артефакта

---

## 68241–68300 — Сложное: Signing Keys + Verification Policy (доверие)
**SigningKey** — описание ключа подписи (не сам ключ):
- key_id, owner, purpose
- storage: hsm | vault | offline
- rotation policy
- revocation

**VerificationPolicy** — правила, которые определяют “можно ли ставить”:
- требуется подпись org key
- SBOM обязателен
- provenance обязателен
- запрет определённых лицензий
- запрет зависимостей из denylist
- минимальный trust score

Идея: как “политика запуска макросов” в офисе.

---

## 68301–68360 — Сложное+: Publish Receipt + Channel Policy
**PublishReceipt** — чек публикации:
- что опубликовано
- куда (channel: private/public/partner)
- какие проверки прошли
- какие подписи и кем
- hash артефакта
- ссылки на docs/vitrines

**ChannelPolicy** — различия каналов:
- private: можно без полного SBOM (опционально), но с подписью
- public: SBOM+provenance обязательны, строгий denylist
- partner: дополнительные enterprise требования

---

## 68361–68400 — Trust Score (сколько доверять пакету)
**TrustScore** агрегирует:
- результаты validation (из 67601–68000)
- наличие SBOM / provenance / подписи
- историю инцидентов
- репутацию издателя (vendor)
- популярность/стабильность (crash rate, rollback rate)
- тестовое покрытие/смоук в sandbox

UI: простая шкала 0–100 + объяснение “почему такой балл”.

---

## MVP (самое важное)
1) PackageManifest + BuildRecipe
2) SBOM (минимальная) + подпись
3) VerificationPolicy (public-min)
4) PublishReceipt
5) TrustScore (простая формула)

Следующий блок по порядку:
**68401–68800 — “SBOM/Vuln Scanning & Supply-chain Monitoring OS”**
(мониторинг уязвимостей, автопереиздание, оповещения, CVE policies).
