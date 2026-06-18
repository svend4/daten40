# IFOS 62401–62800 — Hostability & Deployment Profiles OS (v1)
Цель: чтобы “в проде не работает” перестало быть магией.  
Этот блок описывает **унифицированную систему хостинга**: какие платформы/окружения поддерживают какие возможности, как IFOS выбирает правильный “deployment profile”, и почему на некоторых PaaS (например, при тестовом деплое) часто “не работают кнопки” (CORS, webhooks, фоновые задачи, storage, cookies, очереди).

Порядок: **простое → среднее → сложное**.

---

## 62401–62420 — Простое: почему на PaaS “не работает”
Когда фронт/бек связаны неправильно, симптомы одинаковые:
- кнопка “сохранить/отправить” ничего не делает (POST не дошёл)
- “Failed to fetch / CORS error” в консоли
- login работает локально, но не в облаке (cookies/SameSite/HTTPS)
- webhooks не приходят (нет публичного URL, неправильный path, firewall)
- фоновые задачи не выполняются (на платформе нет worker/cron)
- файлы “пропадают” (нет persistent storage, только ephemeral filesystem)

Вывод: проблема не “в коде”, а в том, что **профиль хостинга не соответствует потребностям приложения**.

---

## 62421–62460 — Hostability Capabilities (словарь возможностей хостинга)
IFOS вводит **capability‑словарь** (как драйверы):
- **INBOUND_HTTP**: публичный HTTP вход (base requirement)
- **TLS_CUSTOM_DOMAIN**: свои домены/HTTPS
- **WEBSOCKETS**: realtime (ws)
- **STREAMING**: SSE/streaming response
- **WEBHOOKS_IN**: приём webhooks извне
- **OUTBOUND_EGRESS**: исходящие запросы в интернет
- **STATIC_EGRESS_IP**: фиксированный исходящий IP (корп. интеграции)
- **BACKGROUND_WORKER**: отдельный worker процесс
- **QUEUE**: очередь задач (redis/rabbit/sqs‑like)
- **CRON_SCHEDULER**: расписание (cron)
- **PERSISTENT_STORAGE**: постоянный диск (uploads, caches)
- **OBJECT_STORAGE**: S3‑подобное хранение
- **DATABASE_MANAGED**: управляемая БД (Postgres/MySQL)
- **SECRETS_MANAGER**: безопасные секреты (см. 61601–62000)
- **OBSERVABILITY**: логи/метрики/трейсы
- **MULTI_SERVICE**: несколько сервисов (frontend+api+worker+db)
- **REGION**: размещение по региону (EU/US)
- **IP_ALLOWLIST**: allowlist входа (корп. сети)
- **VPC/PRIVATE_NET**: приватные сети между сервисами

Дальше IFOS сопоставляет: **что нужно приложению** ↔ **что даёт платформа**.

---

## 62461–62520 — App Hostability Manifest (потребности приложения)
Каждый bundle/app публикует manifest:
- какие capabilities нужны (must / should / optional)
- длительность запросов (timeout needs)
- потребность в websocket/streaming
- нужен ли worker и очередь
- нужен ли cron
- нужен ли persistent storage (или достаточно object storage)
- какие порты/переменные окружения/healthcheck
- требования к CORS/cookies/auth

**Ключевая идея:** разработчик описывает “что нужно”, а IFOS подбирает профиль/платформу.

---

## 62521–62580 — Deployment Profiles (готовые типовые профили)
Профиль = шаблон деплоя + настройки:
- **static_site**: чистый фронт (SPA), без бекенда
- **web_api_basic**: API (FastAPI/Node), без worker/cron
- **web_api_plus_worker**: API + worker (очередь)
- **web_api_plus_cron**: API + cron scheduler
- **full_stack_managed**: frontend + api + worker + db + object storage
- **enterprise_restricted**: фиксированный egress IP, allowlists, audit

Каждый профиль содержит:
- топологию сервисов
- настройки портов/health checks
- env vars + secrets refs
- CORS defaults
- шаблон инфраструктуры (Docker/compose/terraform‑like)

---

## 62581–62640 — Типовые “мины”: CORS, cookies, base URL, reverse proxy
### A) CORS (самая частая причина “кнопки не работают”)
Проверка:
- frontend вызывает `https://api.example.com`?
- бекенд отвечает `Access-Control-Allow-Origin`?
- разрешены методы `POST, PUT, PATCH, DELETE`?
- разрешены заголовки `Authorization, Content-Type`?
- `credentials` (cookies) включены корректно?

### B) Cookies / Auth
- в облаке нужен HTTPS
- cookies часто требуют `SameSite=None; Secure`
- если разные домены (app.example.com и api.example.com) — учитываем CORS + cookie domain

### C) Base URL / Env vars
- фронт должен брать API URL из env/config
- бекенд должен слушать `0.0.0.0` и порт из env (`PORT`), а не только 3000/8000

### D) Reverse proxy и path
- если platform проксирует `/api` → приложение должно знать свой root path

---

## 62641–62710 — Webhooks, background jobs, очереди, cron
**Webhooks**: нужен публичный URL + стабильный endpoint + логирование входящих запросов.
- при деплое IFOS автоматически создаёт “webhook receiver” endpoint
- добавляет replay режим для теста (см. 62001–62400)

**Background jobs**:
- нельзя делать тяжёлую работу в HTTP‑запросе (timeout)
- используем очередь (QUEUE) и worker (BACKGROUND_WORKER)

**Cron**:
- ежедневные сборы новостей/дедуп/ранжирование → cron triggers job → queue → worker

---

## 62711–62760 — Диагностика по шагам (debug playbook)
IFOS хранит “пошаговый чеклист”, который запускается автоматически:
1) Health check API
2) Проверка CORS preflight (OPTIONS)
3) Проверка auth flow (token/cookie)
4) Проверка записи (POST) и чтения (GET)
5) Проверка webhook (send test)
6) Проверка worker (enqueue job → confirm processed)
7) Проверка storage (upload → read back)
8) Проверка времени/часового пояса (cron)
9) Проверка outbound egress (доступ к внешним API)
10) Проверка наблюдаемости (лог/trace id)

---

## 62761–62800 — Сложное: Auto‑select хостинга (планировщик профилей)
IFOS делает “план”:
- читает manifest приложения
- ищет совместимые профили
- оценивает стоимость/сложность/риски (score)
- предлагает 2–3 варианта: minimal / recommended / enterprise
- генерирует конфиги деплоя (Dockerfile, compose, env template, health checks)
- запускает probe‑службу для подтверждения возможностей

---

## Что дальше
Следующий блок:
**62801–63200 — Environment & Network OS**  
(egress allowlists, NAT, VPC/private network, service discovery, DNS, certificates, региональные профили).  
Напишите “Продолжение” — сделаю.
