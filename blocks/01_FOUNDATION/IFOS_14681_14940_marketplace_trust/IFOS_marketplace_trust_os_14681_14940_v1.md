# IFOS 14681–14940 — Marketplace & Trust‑OS: витрины, отзывы как evidence, модерация, подписи и “установить→запустить→отчёт” (v1)

Этот блок отвечает на вашу боль: **“почему нет вертикали качества”** и почему интернет выглядит как “дикое поле”.
Ответ: потому что **без Trust‑OS** любая витрина быстро превращается в мусор, а лучшие решения теряются среди 999 000 копий.

IFOS Marketplace & Trust‑OS — это слой, который делает:
- “каталог функций/рецептов/пакетов” **как магазин**
- но с **доказательствами работоспособности (evidence)**, а не только “отзывами”
- с модерацией, подписью артефактов, рейтингом доверия и отчётом по запуску.

---

## 14681–14710 — Marketplace объектно (самое простое)

### 14681) Что продаём/публикуем
Marketplace item (Listing) бывает трёх типов:
- **function** (атом) — “telegram.send_message”
- **recipe** (кнопка) — “RSS → Telegram дайджест”
- **bundle** (пакет) — “Travel Hub Starter” (несколько recipes + deps + install plan)

### 14682) Почему “listing” должен быть отдельным объектом
Потому что один и тот же recipe может:
- иметь разные версии,
- иметь разные адаптации (targets),
- иметь разные evidence,
- иметь разные цены/лицензии/условия.

### 14683) Минимум полей listing
- id, type, title, summary
- version, authors, license
- tags, domains (travel, crm, wordpress)
- targets_supported
- required_secrets
- policy_flags
- evidence_summary (уровень доказательств)
- trust_score (число + расшифровка)

---

## 14711–14750 — Отзывы ≠ доказательства (среднее)

### 14711) Проблема обычных отзывов
Обычный отзыв:
- субъективен
- легко накрутить
- не доказывает “работает у вас”

### 14712) Как сделать отзывы полезными
Отзывы превращаются в evidence, когда:
- пользователь указывает target (Make/n8n/WP/CLI)
- прикладывает “run report” (лог, скрин, checksum)
- система проверяет, что report правдоподобен (подпись, формат, отсутствие секретов)

### 14713) Два вида отзывов
- **Review (human)**: “понятно/удобно/экономит время”
- **Evidence record (machine)**: “запуск был, PASS/FAIL, artifacts сохранены”

Их нельзя смешивать: рейтинг удобства ≠ рейтинг надёжности.

---

## 14751–14795 — Evidence pipeline (сложнее, но обязательное)

### 14751) Evidence record — стандартная запись
Evidence record хранит:
- item_id + version
- level (L0/L1/L2/L3)
- checks[] (schema/dry-run/integration/security)
- artifacts[] (preview/log/screenshot/checksum)
- environment (target, connector versions)
- result (PASS/WARN/FAIL)

### 14752) Автоматические проверки evidence
MVP:
- schema validate (формат evidence)
- secret scan (нет ли токенов/паролей в логах)
- checksum verify (файлы не подменены)
- policy guard (если pii=true → дополнительные требования)

### 14753) “Ложные” evidence
Ложное evidence распознаётся по:
- отсутствию артефактов,
- одинаковым шаблонным логам,
- несоответствию версии/хэша,
- попыткам вставить секреты в отчёт.

---

## 14796–14835 — Подписи и целостность артефактов (ещё сложнее)

### 14796) Почему подпись нужна
Если вы скачали “кнопку” из интернета:
- кто гарантирует, что её не подменили?
- кто гарантирует, что она соответствует описанию?

### 14797) Минимальный механизм целостности
- каждый артефакт имеет **sha256**
- пакет (bundle) имеет manifest со списком файлов и sha256
- manifest подписывается (ed25519 или PGP) — хотя бы на уровне издателя

### 14798) Что даёт подпись
- доверие к “официальной сборке”
- цепочку ответственности (publisher)
- снижение фейков

---

## 14836–14890 — Модерация и “вертикаль власти” (самое сложное)

### 14836) Почему нужна модерация
Потому что marketplace иначе превращается в:
- спам (“копии”)
- вредоносные действия
- пиратские ключи/инструкции
- скрытые утечки данных

### 14837) Объект ModerationTicket
Всё спорное попадает в ticket:
- кто загрузил
- что загрузил (listing/evidence/review)
- какая причина (spam, security, policy, trademark)
- какие решения (approve/needs_changes/reject/ban)

### 14838) Роли (MVP)
- **Publisher**: публикует
- **Curator**: улучшает описание, теги, витрины
- **Verifier**: подтверждает evidence L2/L3
- **Moderator**: решает по policy/security
- **User**: запускает и оставляет review + evidence

### 14839) Правила “порогов” публикации
- Public listing: нужен минимум L1 evidence
- Featured: нужен L2 evidence + 3 независимых запуска
- Enterprise-ready: нужен L3 evidence + security scan

---

## 14891–14940 — Trust Score: формула доверия и витрины (финальный уровень)

### 14891) Trust Score = не одна цифра, а разложение
Trust Score должен объясняться:
- Evidence score (работоспособность)
- Security score (нет утечек/рисков)
- Popularity score (не главное, но сигнал)
- Freshness score (не устарело ли)
- Support score (как быстро отвечают)

### 14892) Витрины (Vitrines)
Витрина — это “страница отрасли”, например:
- Travel: “сравнение страховок + дайджест новостей + CRM заявки”
- WordPress: “пакеты для WooCommerce/SEO/Analytics”
- Office: “документы → подписать → отправить → архивировать”

Витрины строятся из bundles + лучших recipes, а “лучшие” выбираются Trust‑OS, не рекламой.

### 14893) One‑click flow (install→run→report)
Ключевой UX:
1) Install (bundle/recipe)
2) Configure secrets (wizard)
3) Run (dry-run → real)
4) Generate report (evidence log + preview)
5) Publish evidence (optional)

---

## Приложения к этому блоку
В этом пакете:
- JSON Schemas: listing, review, evidence record, moderation ticket, trust score
- OpenAPI: Marketplace API (MVP)
- Examples: 1 listing + 1 review + 1 evidence + 1 moderation ticket + 1 trust score
- Skeleton: расчёт trust score (Python)
- Spec: подпись и sha256‑manifest
- Template: install/run report (Markdown)
