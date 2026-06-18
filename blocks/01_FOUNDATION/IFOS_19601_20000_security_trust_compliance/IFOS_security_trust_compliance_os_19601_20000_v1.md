# IFOS 19601–20000 — Security, Trust & Compliance‑OS: подписи/SBOM, supply‑chain защита, sandbox permissions, secrets, policy‑as‑code, сканеры, trust score, audit trail (v1)

Если IFOS превращает “дикий интернет” в операционку, то **без доверия** всё рушится:
- модуль может быть “удобный”, но воровать токены;
- bundle может “работать”, но быть заражён supply‑chain;
- плагин может “поддерживаться”, но иметь CVE и backdoor;
- автор может “накрутить рейтинг”, но факты против него.

Security, Trust & Compliance‑OS вводит **техническое доверие**, а не “веру в автора”:
- каждому ассету: SBOM + подпись + attestations,
- каждый запуск: sandbox permissions + audit log,
- каждый релиз: сканирование + policy gate,
- trust score как измеримая метрика (0..1), отдельно от рейтинга.

Ниже — от простого к сложному.

---

## 19601–19650 — Минимальная гигиена (простое)

### 19601) 4 обязательных артефакта для публикации
1) **Permissions Manifest**: что модуль хочет делать (сеть, файлы, токены, внешние API)  
2) **SBOM**: из чего собран (зависимости, версии)  
3) **Signature**: кто подписал (publisher key)  
4) **Scan Report**: результаты сканеров (SAST/dep scan/secret scan)

Без этих 4 вещей — нельзя в marketplace (см. блок 19201–19600).

### 19620) Principle of Least Privilege
Права по умолчанию минимальны:
- сетевой доступ — только к allowlist доменам
- секреты — только по именованным secret refs
- файловая система — только sandbox dir
- “опасные” действия требуют explicit permission + user consent

---

## 19651–19730 — SBOM + Signatures (среднее)

### 19651) SBOM как паспорт состава
SBOM — не “для галочки”. Он позволяет:
- обнаруживать CVE в зависимостях,
- контролировать лицензии,
- делать воспроизводимые сборки,
- предотвращать “подмену”.

### 19680) Подписи и верификация
Каждый bundle/asset подписывается:
- ключом издателя (publisher signing key)
- с указанием digest (hash) всех файлов
- с привязкой к версии

При установке/обновлении:
- verify signature
- verify sbom digest match
- verify policy compliance

---

## 19731–19810 — Permissions + Sandbox (среднее+)

### 19731) Permissions Manifest — контролируемый словарь прав
Примеры прав:
- net.http.fetch (с allowlist)
- net.smtp.send
- secrets.read (список secret refs)
- storage.write (sandbox)
- schedule.create
- external.webhook.receive
- llm.invoke (с провайдером)

### 19770) Sandbox profile
Sandbox профиль определяет:
- доступ к сети (deny/allowlist)
- лимиты CPU/RAM/timeout
- доступ к файлам
- доступ к env
- ограничения side-effects (например “no delete”)

Это делает “one‑click install” безопасным.

---

## 19811–19870 — Secrets Management (сложно, но жизненно)

### 19811) Секреты никогда не попадают в bundle
Bundle хранит только **SecretReference**:
- name (telegram.bot_token)
- scope (tenant/user/device)
- rotation policy
- last_used_at

### 19840) Разделяем хранение и использование
- storage: vault/keystore (платформа)
- usage: runtime получает временный доступ по ref
- audit: кто/когда/зачем запрашивал

---

## 19871–19940 — Policy‑as‑Code + Scanning (очень сложно)

### 19871) Policy‑as‑Code
Политики описывают правила:
- разрешённые домены
- запрещённые permissions
- лицензии (GPL vs коммерция)
- запрет hardcoded secrets
- требование SLO/smoke/synthetic

Policy engine выдаёт решение:
- allow / deny / allow_with_warnings
и причины (explainable).

### 19910) Scanning pipeline
Минимум сканеров:
- dependency/CVE scan
- secret scan (ключи в коде/конфиге)
- SAST (на распространённые паттерны уязвимостей)
- license compliance scan

Итог: Scan Report + список Vulnerabilities.

---

## 19941–20000 — Trust Score + Audit Trail (самое сложное)

### 19941) Trust Score (0..1) — отдельный от quality
Факторы trust score:
- signature verified (да/нет)
- sbom present + complete
- vuln severity (count sev-high)
- policy compliance (pass/warn/deny)
- permissions risk (high‑risk perms?)
- incident history (sev1/sev2)
- publisher reputation (KYC/verified?)

Trust score нужен, чтобы:
- фильтровать marketplace,
- блокировать опасные обновления,
- строить “trust‑first” выдачу.

### 19980) Audit Log: кто что делал
Audit logging фиксирует:
- install/update/rollback
- secrets access
- permission grants
- external calls (с метаданными)
- policy decisions
- scan results

Audit = основа расследований, комплаенса и доверия.

---

## Что лежит в пакете
- JSON Schemas: SBOM, signature, attestation, permissions manifest, sandbox profile, secret reference, policy bundle, scan report, vulnerability, compliance checklist, trust score, audit log
- Specs: supply‑chain security, permissions/sandbox, secrets, policy‑as‑code, scanning, trust score, audit logging
- OpenAPI: Security/Trust/Compliance API (MVP)
- Examples: “News Digest Cluster” с permissions+sbom+sig+scan+trust
- Python skeletons: signature verifier, sbom parser, policy engine, secrets adapter, scanner orchestrator, trust scorer, audit logger
