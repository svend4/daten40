# IFOS — Webhook Relay & Local Lab (Ingress, Tunnels, Test Webhooks) (Блок 64801–65200)

Версия: v1 · Пакет: `IFOS_64801_65200_webhook_relay_tunnels_local_lab_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

Одна из главных болей, которую ты описывал: **тестовые хостинги и локальные приложения** часто не умеют
принимать входящие запросы (webhooks), особенно если всё за NAT/файрволом.

А без webhook‑ов не работает половина автоматизаций:
- платежи,
- статусы доставки,
- события CRM,
- уведомления от маркетплейсов,
- интеграции Make/n8n,
- события GitHub/CI.

Этот блок даёт IFOS стандарт: **Webhook Relay** (публичная точка входа) + **Tunnels** (доставка в локальную сеть)
и режим **Local Lab** (тестовые события/ключи/генераторы), чтобы можно было:
- разрабатывать интеграции локально,
- проверять сценарии,
- запускать демо без полноценного прод‑хостинга.

## 1) Что делает (функции)

1) **Public Ingress**: выдаёт публичные URL для webhook‑ов (`https://hooks.ifos/...`).
2) **Tunnel Agent**: локальный агент держит исходящее соединение и получает события.
3) **Delivery Guarantees**: повторная доставка, очереди, dead-letter.
4) **Replay**: повторить webhook (для отладки и восстановления).
5) **Capture & Inspect**: просмотр payload, заголовков, подписи.
6) **Secret Verification**: проверка подписей/секретов (Stripe, GitHub, Shopify и т.д.).
7) **Routing Rules**: маршрутизация на endpoint/runner/queue.
8) **Rate Limits**: защита от лавин/злоупотребления.
9) **Test Webhooks**: генератор тестовых событий по каталогам.

## 2) Что НЕ делает

- Не заменяет полноценный API Gateway/WAF, но даёт минимально нужные защиты (rate limit, auth, signature).
- Не является полноценным брокером сообщений уровня Kafka — но имеет очереди и DLQ для webhook‑доставки.

## 3) MVP (простое → среднее → сложное)

### 3.1 Простое (P1.1)

- Создать endpoint webhook, получить публичный URL
- Tunnel-agent принимает события и пишет в лог/forward
- Capture + Replay вручную


### 3.2 Среднее (P1.2)

- Очередь + retry/backoff + DLQ
- Валидация подписи (HMAC)
- Routing rules (по path/headers/event_type)
- Ограничение скорости


### 3.3 Сложное (P1.3)

- Multi-tenant изоляция
- Автоматический mapping события → IFOS entity/event model
- Интеграция с case-management (инциденты доставки)

## 4) Архитектура

### Компоненты
- **Ingress Service**: принимает входящие webhook.
- **Verifier**: проверяет подписи/секреты.
- **Router**: направляет в tunnel/runner/queue.
- **Delivery Queue**: retries + DLQ.
- **Tunnel Gateway**: держит соединения с tunnel‑агентами.
- **Local Lab UI**: инспектор, replay, генератор тестовых событий.

### Потоки
A) Provider → Ingress → Verify → Queue → Tunnel → Local Endpoint
B) Provider → Ingress → Verify → Runner (workflow)
C) Lab Generator → Ingress → Inspect/Replay

## 5) Модель данных

**webhook_endpoint**:
- `endpoint_id`
- `workspace_id`
- `public_url`
- `target` (tunnel|runner|queue)
- `verify_mode` (none|hmac|provider_profile)
- `rate_limit`

**webhook_event**:
- `event_id`
- `endpoint_id`
- `received_at`
- `headers`
- `payload_ref`
- `status` (delivered|failed|queued)
- `attempts`

**tunnel_agent**:
- `agent_id`
- `device_id`
- `status`
- `last_seen`
- `routes` (list)

## 6) API (минимум)

- `POST /hooks/endpoints` (создать endpoint)
- `GET  /hooks/endpoints` (список)
- `GET  /hooks/events?endpoint_id=` (инспектор)
- `POST /hooks/events/{id}:replay`
- `POST /hooks/tunnels/agents:register`
- `GET  /hooks/tunnels/agents`
- `POST /hooks/lab:generate` (тестовое событие)

## 7) Каталог provider profiles (пример)

- `stripe` (signature: Stripe-Signature)
- `github` (X-Hub-Signature-256)
- `shopify` (X-Shopify-Hmac-Sha256)
- `paypal` (webhook verification)
Профили задают: заголовки подписи, алгоритм, sample payloads.

## 8) Зависимости

### Hard deps
- 61601–62000 `enterprise_connectors_credential_vault_os` (секреты/ключи подписи)
- 32801–33200 `runtime_execution_os` (если роутинг в runner)
- 42801–43200 `case_management_ticketing_os` (инциденты доставки)
- 34801–35200 `observability_reliability_os` (метрики/логи)

### Optional deps
- 62001–62400 `sandbox_test_keys_dev_env_os` (тестовые ключи)
- 62401–62800 `connector_test_harness_ci_cd_os` (автотесты для webhook профилей)
- 64001–64400 `device_fleet_remote_ops` (управление tunnel‑агентами)
- 43601–44000 `content_import_normalization_os` (нормализация payload)
