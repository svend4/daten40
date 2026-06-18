# IFOS 52801–53200 — Integration OS (Connectors Standard: Auth, Secrets, Webhooks, Retries, Rate Limits) (v1)
Цель: чтобы **все коннекторы были одинаковыми по “правилам поведения”**.
Сегодня: WP‑плагины/Make‑модули/скрипты — каждый со своими ошибками, логами, ретраями, лимитами.
Integration OS задаёт единый стандарт: “как должен вести себя любой коннектор”.

Что входит:
- единая модель коннектора (capabilities)
- auth + secrets (без хранения ключей в коде)
- webhooks и подписи
- retries/backoff + idempotency
- rate limits + quotas
- пагинация/курсор
- field mapping + transforms
- taxonomy ошибок
- тестирование коннекторов
- наблюдаемость (metrics/logs/traces)
- security baseline

Порядок: простое → среднее → сложное.

---

## 52801–52830 — Minimal Connector Contract: “как выглядит коннектор”
Любой коннектор описывается как:
- id, name, provider
- capabilities: read/write/webhook
- auth methods
- resources (что умеет: messages, files, products)
- limits (requests/minute, payload size)
- error taxonomy
Это как “драйвер устройства” для интернета.

---

## 52831–52870 — Auth & Secrets: ключи отдельно, политики отдельно
Проблема: ключи в коде и в логах.
Решение:
- SecretRef: ссылка на секрет (vault/ENV/OS keystore)
- auth config хранит только ссылки
- rotation: перевыпуск ключей без ломки процессов
Поддержка:
- API key
- OAuth2
- Basic (только для legacy)
- JWT/service accounts
И правило: **секрет никогда не пишется в лог**.

---

## 52871–52910 — Requests/Responses: единая обвязка
Стандартный запрос:
- method/url
- headers (без секретов)
- body
- timeout
- idempotency_key (если write)
Ответ:
- status
- body
- pagination hints
- rate limit hints
Так runner может универсально управлять коннекторами.

---

## 52911–52960 — Retries + Backoff + Idempotency: устойчивость
Единая политика ретраев:
- только на retryable ошибки (timeout, 429, 5xx)
- exponential backoff + jitter
- max attempts
- dead-letter queue / manual task
Idempotency:
- write операции обязаны принимать idempotency_key
- повтор не создаёт дубликат
Это лечит главную боль “два раза отправило”.

---

## 52961–53010 — Rate Limits & Quotas: чтобы не банили и не разоряли
Лимиты:
- requests/minute
- tokens/day (LLM)
- payload size
Правила:
- коннектор публикует лимиты
- runner применяет token bucket
- есть “budget cap” на уровень bundle/process
Это превращает стоимость в управляемую величину.

---

## 53011–53040 — Pagination/Cursors: большие списки без боли
Стандарт:
- page + page_size (legacy)
- cursor (preferred)
- has_more + next_cursor
Runner умеет:
- продолжать с последнего курсора
- сохранять checkpoint (для восстановления)
Это критично для “выгрузить 1M товаров/сообщений”.

---

## 53041–53080 — Webhooks & Eventing: события вместо опроса
Webhook стандарт:
- endpoint registration
- signature verification (HMAC/JWT)
- replay protection
- event_id + dedup_key
Плюс: outbox pattern (из Integration OS ↔ Runtime OS).
Иначе: “дубли” и “подмена событий”.

---

## 53081–53120 — Field Mapping & Transforms: унификация данных
Mapping:
- source field → canonical field (Data OS)
- transforms (normalize phone, parse price)
Версия маппинга = контракт, иначе ломаем процессы.
Это делает интеграции повторяемыми.

---

## 53121–53160 — Error Taxonomy: ошибки должны быть понятными
Категории:
- auth_error
- rate_limited
- timeout
- provider_down
- bad_request
- schema_mismatch
- permission_denied
Каждая ошибка включает:
- retryable? (да/нет)
- user_action (что сделать)
- internal_code
Так UI может показывать нормальные подсказки, а не “error 500”.

---

## 53161–53190 — Connector Testing: контрактные тесты
Тесты:
- auth smoke test
- read sample
- write idempotency test
- webhook signature test
- rate limit handling
Если тесты не проходят — коннектор не публикуется в marketplace.
Это “качество как правило”, а не как удача.

---

## 53191–53200 — Observability & Security Baseline
Минимальные метрики:
- success_rate
- retries_count
- latency p95
- 429 rate
Security baseline:
- least privilege scopes
- encrypted secrets
- audit logs
Без этого IFOS не станет “B2B OS”, а останется набором скриптов.

---

## Итог
Integration OS делает коннекторы “как драйверы”:
- одинаковые правила
- предсказуемые ошибки
- управляемые лимиты/стоимость
- тестируемость и безопасность

---

## Что дальше
Следующий блок:
**53201–53600 — UI Console OS: панель управления, статусы, конфликты, approvals, “почему не работает”**  
(чтобы человек видел систему как в “Диспетчере задач + Админке”).  
Скажете “Продолжение” — сделаю.
