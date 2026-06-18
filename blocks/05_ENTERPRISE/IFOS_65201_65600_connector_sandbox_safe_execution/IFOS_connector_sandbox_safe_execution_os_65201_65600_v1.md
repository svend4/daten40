# IFOS 65201–65600 — Connector Sandbox & Safe Execution OS (v1)
Цель: запускать **коннекторы/агенты/импортёры** так, чтобы они:
- не “сливали” секреты и данные,
- не делали неожиданный сетевой трафик,
- не съедали ресурсы,
- были **воспроизводимы** и управляемы,
- давали понятные логи/аттестации.

Порядок: **простое → среднее → сложное**.

---

## 65201–65220 — Простое: что такое Sandbox в IFOS
Sandbox — это **контейнер/песочница исполнения**, где коннектор получает:
- минимальные права (scopes/permissions)
- секреты только через **Vault lease** (короткие TTL)
- сетевой доступ по egress policy (allowlist)
- лимиты CPU/RAM/диска/времени
- журнал аудита

Ключевая мысль: *коннектор — потенциально недоверенный код*.

---

## 65221–65270 — Уровни изоляции (от простого к прод)
### Level 0: “Dev local”
- один контейнер, общий интернет
- только базовые лимиты
- подходит для прототипов

### Level 1: “Restricted network”
- выход в сеть только на домены/IPv4/IPv6 allowlist
- запрет прямого доступа в локальную сеть
- DNS policy: только разрешённые резолвы

### Level 2: “Policy-enforced”
- egress policy + rate limits + request signing
- обязательная маскировка логов
- запрет записи секретов на диск

### Level 3: “High assurance”
- отдельные namespaces / gVisor / Firecracker (в зависимости от платформы)
- attestation (что именно запущено)
- out-of-band auditing + tamper-evident logs

---

## 65271–65335 — Egress policies: “куда можно ходить”
**EgressPolicy** описывает:
- allowlist доменов и портов (например api.stripe.com:443)
- ограничения по протоколам (https only)
- запрет на IP literal, запрет на SSRF паттерны
- лимиты на объём трафика (MB/day) и скорость

Практика:
- каждый connector имеет baseline egress policy
- каждое окружение (dev/test/prod) может ужесточать правила
- любые изменения — через change control

---

## 65336–65395 — Resource limits: “сколько можно съесть”
**ResourceLimits**:
- cpu (cores / millicores)
- memory (MB/GB)
- disk (MB)
- wall_time (seconds)
- max_concurrency

Защита:
- OOM → restart with backoff
- runaway → kill by wall_time
- fork bomb → deny by policy (no fork/exec), если поддерживается

---

## 65396–65455 — Rate limiting и квоты (анти-спам, анти-дос)
**RateLimitPolicy**:
- max requests/minute к домену
- max errors/minute (circuit breaker)
- budget для API calls (например 1000/day)
- exponential backoff + jitter

Цель:
- не “убить” внешние API
- не получить бан
- защититься от ошибок коннектора

---

## 65456–65505 — Replay protection и подпись запросов
Если коннектор отправляет webhooks / events:
- добавлять nonce + timestamp
- подписывать payload (HMAC) секретом, который не экспортируется
- проверять replay window (например 5 минут)
- хранить nonce cache (LRU) на TTL

---

## 65506–65550 — Permission model: что коннектор “умеет”
**ConnectorPermissionModel**:
- разрешённые действия: read/write/delete/create
- разрешённые типы данных (entity types)
- разрешённые операции: ingest/run/install/upgrade
- PII flags: запрещать доступ к PII без особой политики

Важно:
- permission model используется UI/Marketplace (показывать риски)
- runtime применяет enforcement

---

## 65551–65585 — Attestation: доказательство того, что запущено
**ExecutionAttestation**:
- hash образа/пакета (bundle)
- digest зависимостей
- sandbox_profile_id
- policy versions (egress/limits)
- timestamp + runtime node id
- подпись (runtime signing key)

Это нужно для:
- расследований
- enterprise compliance
- воспроизводимости

---

## 65586–65600 — Практический “one-click safe run”
Алгоритм:
1) Marketplace выбирает коннектор + версию
2) Dependency resolver собирает bundle
3) Vault выдаёт leases на секреты (TTL 10 мин)
4) Sandbox запускает контейнер с egress/limits/rate policies
5) Runtime пишет audit + attestation
6) Результат складывается в Data OS + provenance/lineage

---

## Что дальше
Следующий блок по порядку:
**65601–66000 — API Gateway & Egress Control OS**  
(центральный шлюз для всего внешнего трафика, WAF-подобные правила, DLP, data exfiltration detection).
