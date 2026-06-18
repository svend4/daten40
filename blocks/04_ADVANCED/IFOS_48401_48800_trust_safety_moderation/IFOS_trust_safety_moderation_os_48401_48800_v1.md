# IFOS — Trust & Safety Moderation Layer (Блок 48401–48800)

Версия: v1 · Пакет: `IFOS_48401_48800_trust_safety_moderation_os_pack.zip` · Дата: 2026-01-02

## 0) Зачем нужен этот блок

IFOS аккумулирует «функции интернета»: коннекторы, макросы, шаблоны, витрины, пакеты знаний, отзывы. Если это публиковать без Trust & Safety, система быстро захлебнётся:
- спам и SEO-паразитирование
- вредоносные ссылки/файлы
- фишинг, поддельные витрины, кража ключей
- токсичный контент и преследование
- публикация приватных данных

Этот блок вводит **модерационный слой**, который работает как «фильтр и судья», и позволяет безопасно масштабировать маркетплейс и отзывы.

## 1) Что делает (функции)

1) **Content classification**: риск/категории/тэги.
2) **Policy engine hooks**: применять политики (что разрешено/запрещено).
3) **Queues**: очереди на авто/ручную модерацию.
4) **Decisions**: approve/reject/escalate/limited_visibility.
5) **Appeals**: обжалование решения.
6) **Abuse signals**: репорты пользователей, spam score, reputation.
7) **Redactions**: маскирование персональных данных.

## 2) Что НЕ делает (границы)

- Не заменяет безопасность инфраструктуры (auth/secret vault) — это отдельные security блоки.
- Не является полным юридическим комплаенсом (GDPR/DSA) — но даёт точки интеграции.
- Не делает «курирование качества» (рейтинги и отбор) — это блок curation.

## 3) MVP (простое → среднее)

### Шаг 3.1 — Объекты модерации

Сущность `moderation_subject`:
- `subject_type` (vitrine|review|bundle|template|connector|message|profile|asset)
- `subject_id`
- `workspace_id`
- `created_by`
- `content_ref` (ссылка на текст/файлы)

### Шаг 3.2 — Политики (policy ids)

MVP набор policy ids:
- `POLICY_SPAM`
- `POLICY_MALWARE_LINK`
- `POLICY_PHISHING`
- `POLICY_HARASSMENT`
- `POLICY_PII_LEAK`
- `POLICY_COPYRIGHT`
- `POLICY_ADULT`

Каждая политика имеет:
- описание
- уровень серьёзности
- тип решения по умолчанию

### Шаг 3.3 — Очередь модерации

Сущность `moderation_queue_item`:
- `queue_item_id`
- `subject_type`, `subject_id`
- `risk_score` (0..1)
- `flags` (список policy ids)
- `status` (pending|in_review|decided)
- `assigned_to` (модератор, optional)
- `created_at`, `updated_at`

MVP: одна очередь `global` + фильтры.

### Шаг 3.4 — Решение модерации

Сущность `moderation_decision`:
- `decision_id`
- `queue_item_id`
- `decision` (approve|reject|escalate|limit_visibility|redact)
- `reason` (policy id + комментарий)
- `actor_type` (system|moderator)
- `actor_id`
- `created_at`

После решения объект получает `visibility`:
- public | unlisted | private | blocked

### Шаг 3.5 — Репорты пользователей

Сущность `user_report`:
- `report_id`
- `subject_type`, `subject_id`
- `reporter_user_id`
- `reason` (spam|scam|abuse|pii|other)
- `details`
- `created_at`

Каждый репорт увеличивает risk_score и может авто-ставить в очередь.

## 4) Средний уровень: апелляции и репутация

### Шаг 4.1 — Appeals
Сущность `moderation_appeal`:
- `appeal_id`, `decision_id`
- `appellant_user_id`
- `message`
- `status` (open|review|accepted|denied)

### Шаг 4.2 — Reputation signals
- `creator_reputation_score`
- `workspace_trust_tier`
- история решений и доля отклонений

## 5) Ближе к сложному: автоматическая детекция и PII redaction

1) Авто-классификация: spam/фишинг/PII по правилам + ML.
2) PII redaction: маскировать email/телефон/адреса до публикации.
3) Safe browsing: проверка URL через списки/сканеры.
4) Sandboxing вложений (интеграция с asset pipeline).

## 6) API (минимум)

- `POST /moderation/queue/enqueue` (subject)
- `GET  /moderation/queue?status=pending`
- `POST /moderation/queue/{id}/decide`
- `POST /moderation/reports` (user report)
- `POST /moderation/appeals` (appeal)

## 7) Зависимости

### Hard deps
- 34401–34800 `security_trust` (политики доверия/верификация)
- 41201–41600 `data_privacy_compliance` (PII/GDPR hook)
- 45601–46000 `marketplace_curation_quality` (сигналы качества)
- 48001–48400 `reviews_feedback_os` (репорты/жалобы по отзывам)

### Optional deps
- 42401–42800 `customer_support_disputes` (эскалации)
- 34001–34400 `enterprise_governance` (роли модераторов)
- 34801–35200 `observability_reliability` (метрики злоупотреблений)

## 8) Чек-лист

- [ ] Очередь модерации
- [ ] Решения + visibility
- [ ] Репорты пользователей
- [ ] Policy ids
- [ ] Апелляции (минимум)
- [ ] PII redaction hook
