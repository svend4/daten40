# IFOS 34401–34800 — Security & Trust OS (v1)
Цель: сделать “Интернет‑функции” **безопасными** и **доверенными**:
- supply chain security (подписи, происхождение, проверка)
- SBOM и attestations (что внутри и как собрано)
- секреты и доступы (vault, rotation, least privilege)
- sandbox/изоляция (контейнеры, ограничения, dry-run)
- сетевые политики (egress allowlist, запрет “куда попало”)
- сканеры уязвимостей и health checks
- trust score (сводный “уровень доверия”)
- инциденты и отзыв пакетов (revocation)

Порядок: простое → среднее → сложное.

---

## 34401–34440 — База доверия: подписи и ключи
### SigningKey
- key_id, owner, algo, created_at, status
- хранение: HSM/Vault/OS keychain
- rotation и revocation

### Signature
Подпись артефакта:
- artifact_ref + hash
- signer key_id
- signature bytes (base64)
- signed_at + purpose (publish/install)

**Минимум:** нельзя публиковать “в маркетплейс”, если нет подписи.

---

## 34441–34510 — SBOM + Attestation
### SBOM
Software Bill of Materials:
- components (deps, версии, хэши)
- licenses
- build info (builder, env)
- source refs

### Attestation
Заявления “как собрано”:
- build provenance (commit, CI job, runner)
- test results
- policy evaluation results

SBOM+attestation — основа supply-chain безопасности.

---

## 34511–34570 — Vulnerability scanning & reports
VulnerabilityReport:
- найденные CVE/уязвимости по компонентам SBOM
- severity (low/med/high/critical)
- fix_available (да/нет)
- recommendation: block / warn / allow

Правило по умолчанию:
- critical → блок
- high → блок в strict, warn в balanced
- medium → warn

---

## 34571–34630 — Secrets OS: vault и политики секретов
### Secret
- secret_id, type (api_key/oauth/token/password)
- scopes (к чему доступ)
- rotation policy (ttl, rotate_by)
- audit trail (кто использовал)

### SecretPolicy
- запрет хранения секретов в открытом виде
- запрет логирования секретов
- разрешённые провайдеры (Vault/KMS/Keychain)

**Ключевое:** пакеты должны работать с “плейсхолдерами”, а секреты — подтягиваться при запуске.

---

## 34631–34690 — Network Egress Policy: “куда можно ходить”
### NetworkPolicy
- allowlist доменов/подсетей
- denylist
- режимы: deny_all_by_default
- DNS rules
- per-bundle egress profile

Это решает главную проблему “модулей интернета”: они часто “утекают” куда угодно.

---

## 34691–34740 — Sandbox профили и runtime guards
### SandboxProfile
- container isolation (no root)
- cpu/mem limits
- filesystem: read-only + temp dir
- syscalls allowlist (seccomp)
- network restrictions

### RuntimeGuardEvent
- попытка выйти в запрещённый домен
- попытка читать секрет вне scope
- неожиданный exec
- превышение ресурсов

GuardEvent → policy violation → (block + incident).

---

## 34741–34780 — Trust Score: сводная оценка
TrustScore собирается из:
- подпись (есть/нет, кто подписал)
- provenance (официальный источник?)
- SBOM полнота
- vuln status (CVE)
- install/run success_rate
- community feedback

TrustScore влияет на ранжирование и видимость в витринах.

---

## 34781–34800 — Инциденты, отзыв пакетов, revocation
### Incident
- тип: malware, data_leak, phishing, vuln_exploit
- затронутые canonical_id/bundles
- статус: open/mitigated/closed
- действия: disable, revoke keys, notify users, rollback versions

Revocation:
- отзыв подписи/ключа
- блок конкретной версии
- авто‑замена на patched bundle

---

## Что дальше
Следующий блок:
**34801–35200 — Observability & Reliability OS** (логи/метрики/трейсы, SLO/SLA, health checks, автопочинка, rollback, канареечные релизы).  
Скажете “Продолжение” — сделаю.
