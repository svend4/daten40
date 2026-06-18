# IFOS 24401–24800 — Trust, Reviews & Governance OS: отзывы, репутация, антиспам, верификация издателей, policy-gates, витрина качества (v1)

Это слой “социального двигателя” и “вертикали доверия”.  
Если Interoperability OS обеспечивает техническую совместимость, то Trust OS обеспечивает **социальную совместимость**:
- кто публикует,
- насколько это проверено,
- можно ли “в один клик” ставить в прод,
- почему это рекомендовано,
- как защищаемся от мусора/накруток/вредных шаблонов.

Дальше — по порядку, от простого к сложному.

---

## 24401–24440 — Базовые сущности: Review, Rating, AbuseReport

### 24401) Review (отзыв)
Отзыв — текстовый сигнал от пользователя:
- что работало/не работало
- в каком окружении (profile + platform)
- какие ограничения (privacy/cost)

### 24415) Rating (оценки)
Оценки дробятся по осям:
- “работает?” (reliability)
- “понятно?” (documentation)
- “совместимо?” (compatibility)
- “безопасно?” (safety)

### 24430) AbuseReport
Отдельный поток: репорт о злоупотреблении:
- спам, фишинг, вредные webhooks
- утечка PII
- скрытая монетизация / трекинг

---

## 24441–24500 — Антиспам и модерация (зачем это в ядре)

### 24441) SpamScore
Каждому отзыву/издателю/кластеру присваивается spam score:
- скорость появления отзывов
- однотипные тексты
- одинаковые окружения
- “фермы аккаунтов”
- несоответствие receipts (говорит “работает”, а receipts fail)

### 24470) ModerationAction
Модерация — это управляемые действия:
- hide review
- quarantine cluster
- downgrade badges
- require verification
- block publisher

Важно: модерация **протоколируется** (AuditEvent).

---

## 24501–24560 — Верификация издателей (PublisherVerification)

Проблема: “плагины и сценарии не прославлены” — потому что нет прозрачной системы, кому доверять.

Варианты верификации:
- domain verification (DNS TXT)
- org verification (документы/реестр)
- code signing (подпись артефактов)
- reproducible builds + lockfile hash
- “verified installs” (receipts из Runtime OS)

PublisherProfile хранит:
- идентификаторы (domain, github org, wp author)
- историю инцидентов
- trust signals

---

## 24561–24620 — TrustSignal: единый язык доверия

TrustSignal — атом доверия (как “атом функции”, но социальный):
- `verified_publisher`
- `signed_artifact`
- `reproducible_install`
- `recent_sandbox_receipt_ok`
- `prod_receipt_ok`
- `low_incident_rate_30d`
- `no_pii_leak_reports`

Эти сигналы используются в:
- TrustScore
- QualityBadge
- PolicyGateEvaluation

---

## 24621–24680 — TrustScore и QualityBadges (витрина качества)

### 24621) TrustScore (0..100)
TrustScore учитывает:
- качество и давность receipts (sandbox/prod)
- репутацию издателя
- отзывы (с антиспамом и весами)
- количество и тяжесть инцидентов
- покрытие docs/tests (из Quality uplift OS)

### 24650) QualityBadges
Бейджи — понятные “иконки доверия”:
- ✅ Verified Publisher
- 🔒 Privacy‑Safe
- 🧪 Sandbox‑Proven
- 🏭 Prod‑Ready
- 🔁 Rollback‑Ready
- 📚 Well‑Documented

Badges должны быть **объяснимыми** (why? → список сигналов).

---

## 24681–24740 — Governance: PolicyRule и PolicyGates

### 24681) PolicyRule
Политика — декларативная:
- что запрещено (например: “PII export”)
- что обязательно (rollback_plan required)
- что требует ручного подтверждения (manual override)

### 24710) PolicyGateEvaluation
Gate — вычисление политики “в контексте профиля”:
- dev: мягко
- sandbox: строго по PII + quotas
- prod: требуем L3+ и signed artifacts

Результат: pass/warn/fail + findings + suggested fixes.

---

## 24741–24800 — Audit, Attestation, Disputes (правовая/инженерная зрелость)

### 24741) AuditEvent
Все изменения фиксируются:
- кто изменил рейтинг/скрыл отзыв
- кто перевёл кластер в карантин
- кто дал override на prod

### 24760) Attestation + Provenance
Attestation — “подпись факта”:
- этот bundle именно такой (hash)
- этот publisher действительно владелец
- этот receipt действительно был

Provenance связывает:
- source → conversion → install → receipt → trust score

### 24785) DisputeCase
Система споров:
- издатель оспаривает блокировку
- пользователь оспаривает скрытие отзыва
- арбитраж правилами + логами + receipts

---

## Что в пакете
- JSON Schemas: Review, Rating, ReputationProfile, PublisherProfile, PublisherVerification, TrustSignal, TrustScore, SpamScore, AbuseReport, ModerationAction, PolicyRule, PolicyGateEvaluation, AuditEvent, Attestation, ProvenanceRecord, DisputeCase, QualityBadge, VitrineTrustCard, SchemaRegistry
- Specs: reviews system, anti-spam+moderation, publisher verification, governance policy gates, trust score+badges, vitrine display
- OpenAPI: Trust & Reviews API (MVP)
- Examples: “News Digest Cluster” — отзывы + receipts → trust score → badges → prod gate
- Python stubs: trust scorer, moderation pipeline, publisher verifier, dispute resolver
