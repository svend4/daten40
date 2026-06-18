# IFOS 17601–18000 — Trust & Compliance‑OS: доверие, лицензии, provenance/SBOM, подписи, разрешения, audit‑log и “что можно ставить одной кнопкой” (v1)

Вы описали “вертикаль качества” и “почему интернет — дикое поле”.  
**Trust & Compliance‑OS** делает интернет **учтённым**: кто сделал, что именно, с какой лицензией, что внутри, можно ли это запускать в данном режиме (личный/команда/B2B/гос), и как это доказать пост‑фактум.

Связи:
- Registry‑OS: что это за объект
- Governance‑OS: правила и санкции
- Execution‑OS: факты запусков (runs)
- Knowledge‑OS: как пользоваться/чинить
- Economy‑OS: рейтинг/отзывы/биллинг
- **Trust & Compliance‑OS: почему этому можно доверять**

Ниже — по порядку, от простого к сложному.

---

## 17601–17660 — LicenseRef и “право на использование” (простое)

### 17601) LicenseRef (нормализованная ссылка на лицензию)
Вместо хаоса “где-то в README” — единый объект:
- SPDX id (если есть)
- ссылка на текст
- ограничения (commercial? redistribution? copyleft?)
- обязательства (notice, attribution, source offer)

### 17602) License compatibility (совместимость)
Для bundle/кластера нужно уметь автоматически ответить:
- можно ли коммерчески
- можно ли распространять бинарник/образ
- нужно ли раскрывать исходники (copyleft)
- конфликтует ли один компонент с другим

**Итог:** “Install one‑click” возможен только если license gate PASS.

---

## 17661–17730 — Provenance: “кто собрал и из чего” (среднее)

### 17661) Provenance Record
Запись происхождения для артефакта:
- publisher id
- source refs (git commit, registry id, build id)
- build environment (toolchain)
- inputs hashes
- output hashes
- timestamps

### 17662) Supply‑chain минимализм (MVP)
Даже без сложных систем:
- хеши
- подпись
- SBOM
- audit trail
уже резко повышают доверие.

---

## 17731–17810 — SBOM (Software Bill of Materials) + Signature envelope

### 17731) SBOM
SBOM — список того, что внутри:
- зависимости (libs, plugins, adapters)
- версии
- хеши
- источники
- лицензии на уровне компонентов

### 17732) Signature Envelope
Подпись “конвертом”:
- что подписано (hash)
- кем (public key ref)
- когда
- в каком контексте (tenant, environment)
- как проверять (verification method)
Это позволяет:
- проверить “не подменили ли пакет”
- проверить “это действительно от этого издателя”

---

## 17811–17900 — Permissions: RBAC/ABAC, тенанты и режимы (B2B)

### 17811) Role (RBAC)
Роли по умолчанию:
- Owner (всё)
- Admin (управляет политиками, но не ключами владельца)
- Operator (запускает, смотрит логи)
- Reviewer (видит docs/trace, не запускает)
- Auditor (читает audit‑log, без изменений)

### 17812) ABAC (атрибуты)
Пример:
- “можно устанавливать bundles с network access только если evidence >= L2 и есть SBOM+подпись”
- “в гос режиме запретить внешние webhooks”
- “в sandbox разрешить только mock adapters”

---

## 17901–17960 — Audit‑log и доказательство действий

### 17901) Audit Event
Каждое важное действие пишется:
- кто (actor)
- что (action)
- над чем (subject)
- результат (PASS/FAIL)
- ссылки на доказательства (run id, signature id, policy decision id)

### 17902) Неподделываемость (MVP)
Даже простой append‑only журнал + периодические подписи
уже создаёт “след” для B2B и спорных ситуаций.

---

## 17961–18000 — Compliance Attestations + Vulnerability advisories + Consent

### 17961) Compliance Attestation
Публичное/внутреннее заявление:
- “пакет прошёл проверку лицензий”
- “есть SBOM и подпись”
- “выполнены policy checks (no secrets in logs, PII redaction)”
- “поддерживается режим sandbox/production”

### 17962) Vulnerability Advisory
Если нашли проблему:
- affected versions
- severity
- workaround
- fixed version
- disclosure timeline

### 17963) Consent record (принятие условий)
Для risky действий:
- пользователь принял условия (TOS/политику)
- дата и версия политики
- scope (tenant/job/cluster)

---

## Приложения (в этом пакете)
- JSON Schemas: license ref, provenance record, SBOM, signature envelope, RBAC role, policy profile, audit event, compliance attestation, vulnerability advisory, consent record
- Specs: trust levels, provenance+signing, RBAC/ABAC, audit logging, publishing gates, license compliance, vuln disclosure
- OpenAPI: Trust & Compliance API (MVP)
- Examples: bundle package with SBOM + signature + policy profile + audit event + attestation + advisory + consent
- Python skeletons: SBOM generator, signature verify, policy engine, audit logger, publishing gatekeeper
