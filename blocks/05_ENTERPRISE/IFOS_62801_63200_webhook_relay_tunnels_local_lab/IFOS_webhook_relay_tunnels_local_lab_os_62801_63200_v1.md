# IFOS — Webhook Relay, Tunnels & Local Integration Lab (Блок 62801–63200)

Версия: v1 · Пакет: `IFOS_62801_63200_webhook_relay_tunnels_local_lab_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

Одна из твоих исходных болей: **в облачных тест-хостингах часть функций «не работает»** (webhooks, обратные вызовы, входящие запросы, интеграции с внешними API, локальная отладка).

Чтобы «не изобретать новое», а **собирать из готового** (плагины, Make/n8n, коннекторы), нужно сделать стандартный мост:
- как быстро принять входящий webhook/HTTP callback
- как пробросить его в локальную среду разработчика
- как записать/повторить запросы для отладки
- как безопасно проверять подписи и секреты

Этот блок — как «USB‑хаб и логгер» для интернета: единая инфраструктура туннелей, релеев и локальной лаборатории интеграций.

## 1) Что делает (функции)

1) **Webhook Relay**: публичный URL для входящих вебхуков → доставка в workspace/runner.
2) **Local Tunnels**: проброс входящих запросов в локальный порт (dev laptop/phone).
3) **Request Inspector**: просмотр заголовков/тела/таймингов, маскирование секретов.
4) **Replay**: повторить webhook (однократно/серией), управлять задержкой.
5) **Signature Verification**: проверка HMAC/подписей (Stripe, GitHub, Slack и др.).
6) **Rate & Burst Control**: защита от «шторма» вебхуков (очередь/лимиты).
7) **Environment Routing**: маршрутизация dev/stage/prod по профилям.
8) **Firewall Rules**: allowlist/denylist по IP/ASN/UA.
9) **Event-to-Workflow Binding**: привязка endpoint → workflow/macro.

## 2) Что НЕ делает (границы)

- Не заменяет полноценный reverse proxy для продакшена (но может работать как managed компонент).
- Не является WAF уровня enterprise (это security/trust блоки), но даёт базовые правила.
- Не хранит секреты в явном виде — берёт их из credential vault.

## 3) MVP — от простого к среднему

### 3.1 Уровень 1 (простое)

- Создать endpoint вида `https://ifos.io/w/{workspace}/hooks/{id}`
- Принять запрос, сохранить метаданные, передать в runner
- Страница инспектора: список входящих событий + raw payload
- Replay одной кнопкой

### 3.2 Уровень 2 (среднее)

- Туннель локально: CLI/agent `ifos tunnel --port 3000 --hook <id>`
- Проверка подписи (HMAC)
- Маскирование секретов в логах
- Очередь и rate limits
- Routing по sandbox profiles (dev/stage)

### 3.3 Уровень 3 (продвинуто)

- Multi-tunnel (несколько устройств)
- Перехват и трансформация (rewrite headers/body)
- Canary routing (часть вебхуков в новую версию workflow)
- Replay-сценарии (серии) для CI регрессий

## 4) Модель данных

**webhook_endpoint**:
- `endpoint_id`
- `workspace_id`
- `public_url`
- `target` (workflow_id / macro_id / local_tunnel)
- `signature_policy_id` (optional)
- `routing_profile` (dev|stage|prod)
- `security_ruleset_id` (optional)
- `status` (active|paused)

**webhook_event**:
- `event_id`
- `endpoint_id`
- `received_at`
- `headers` (masked)
- `body_hash`
- `body_ref` (storage pointer)
- `verified` (bool)
- `delivery_status` (queued|delivered|failed)
- `attempts`

**tunnel_session**:
- `session_id`
- `endpoint_id`
- `device_id`
- `local_port`
- `connected_at`
- `last_seen_at`

## 5) API (минимум)

- `POST /webhooks/endpoints` (создать endpoint)
- `GET  /webhooks/endpoints` (листинг)
- `POST /webhooks/endpoints/{id}:pause` / `:resume`
- `GET  /webhooks/events?endpoint_id=` (инспектор)
- `POST /webhooks/events/{event_id}:replay` (повтор)
- `POST /tunnels/sessions` (зарегистрировать туннель)
- `GET  /tunnels/sessions` (активные туннели)
- `POST /tunnels/sessions/{id}:close`

## 6) CLI/Agent (локальная лаборатория)

Минимальный набор команд:
- `ifos tunnel --endpoint <id> --port 3000` (проброс вебхуков на localhost:3000)
- `ifos inspect --endpoint <id>` (последние события)
- `ifos replay --event <event_id>` (повтор события)
- `ifos endpoints` (список)

## 7) Зависимости

### Hard deps
- 32801–33200 `runtime_execution_os` (доставка события в workflow runner)
- 44801–45200 `workflow_runner_macro_engine_os` (исполнение связанного workflow)
- 61601–62000 `enterprise_connectors_credential_vault_os` (секреты подписи)
- 62001–62400 `sandbox_test_keys_dev_env` (routing profiles dev/stage)

### Optional deps
- 34801–35200 `observability_reliability_os` (метрики туннелей/доставки)
- 34401–34800 `security_trust_os` (усиленные правила доверия)
- 42401–42800 `customer_support_disputes_os` (разбор инцидентов)
- 52801–53200 `notifications_activity_feed_os` (нотификации о провалах доставок)
- 63201–63600 `multicloud_hybrid_connectivity_os` (расширение на hybrid сетевую связность)

## 8) Чек‑лист

- [ ] Endpoint create/list/pause
- [ ] Event capture + storage + inspector
- [ ] Replay
- [ ] Local tunnel agent
- [ ] Signature verification
- [ ] Routing profiles dev/stage
- [ ] Rate/burst control
