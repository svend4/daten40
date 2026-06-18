# IFOS — Edge Gateway & Private Connectivity (On‑Prem / LAN / Devices) (Блок 63601–64000)

Версия: v1 · Пакет: `IFOS_63601_64000_edge_gateway_private_connectivity_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

Ты описывал проблему: «в тест‑хостингах кнопки не работают», особенно когда нужно, чтобы приложение **общалось с внешними системами** или принимало входящие события. Даже с вебхуками всё решается только частично. Главная «дыра» остаётся: **доступ к приватным сетям** (офис/дом/сервер за NAT, внутренние базы, NAS, локальные сервисы, IoT).

Этот блок создаёт стандартный компонент IFOS: **Edge Gateway** (агент/шлюз), который запускается внутри приватной сети и даёт IFOS возможность безопасно:
- вызывать локальные API/БД/файловые хранилища,
- публиковать локальные события в IFOS,
- исполнять коннекторы «рядом с данными» (data‑gravity),
- работать с Android/мини‑ПК/домашним сервером как с узлом экосистемы.

## 1) Что делает (функции)

1) **Private Outbound Tunnel**: шлюз сам инициирует защищённое исходящее соединение в IFOS (без входящих портов).
2) **Connector Execution Near Data**: запуск коннектор‑операций внутри приватной сети.
3) **Network Segments**: объявление «сегментов» (LAN, VLAN, NAS, db‑cluster) и их политики доступа.
4) **Service Catalog**: публикация доступных локальных сервисов (эндпоинты, порты, протоколы, схемы).
5) **Secrets Bridging**: получение секретов из credential vault по политике (временные токены, short‑lived).
6) **Job Dispatch**: приём заданий от runner (execute step / pull data / push data).
7) **Local Event Egress**: отправка событий (file changed, new record, sensor) в IFOS.
8) **Health & Heartbeats**: статус шлюза, версии, uptime, телеметрия.
9) **Policy Enforcement**: allow‑rules на уровне workspace/org (что разрешено делать в локальной сети).

## 2) Что НЕ делает (границы)

- Не является полноценным корпоративным VPN (это инфраструктурный слой), но использует туннель по схеме «outbound only».
- Не хранит секреты постоянно: берёт их из vault краткоживущими токенами и маскирует в логах.
- Не заменяет ETL/ELT систему: он даёт доступ/исполнение рядом с данными, а пайплайны — в отдельных блоках.

## 3) MVP (простое → среднее → сложное)

### 3.1 Уровень 1 — «подключить домашний/офисный узел»

- Установить gateway (Docker/desktop/Android‑termux) и привязать к workspace.
- Поднять исходящий туннель.
- Получать задания типа HTTP GET/POST к локальному сервису.
- Базовый health‑endpoint + heartbeats.


### 3.2 Уровень 2 — «частные коннекторы и сегменты сети»

- Network segments + правила (какие адреса/порты доступны).
- Service catalog (описание локальных сервисов + схемы).
- Политика секретов (какие secret_ref можно получать).
- Очередь заданий + ретраи + идемпотентность.


### 3.3 Уровень 3 — «enterprise‑готовность»

- Несколько gateway в одном сегменте (HA, failover).
- Аттестация версии (signed builds), автоподновление.
- Проксирование больших файлов (chunking) и локальный кэш.
- Изоляция коннекторов (sandbox) и ограничение ресурсов.

## 4) Архитектура

### 4.1 Потоки
A) **Control plane**: IFOS → (policy) → dispatch job → gateway
B) **Data plane**: gateway → локальный сервис/БД/файлы → результат → IFOS
C) **Telemetry**: gateway → metrics/logs → observability

### 4.2 Связь с другими блоками
- Runner/Workflow engine отправляет шаги выполнения на gateway.
- Credential vault выдаёт секреты на ограниченное время.
- Multicloud/hybrid connectivity расширяет это на федерации и маршрутизацию между средами.

## 5) Модель данных

**edge_gateway**:
- `gateway_id`
- `workspace_id`
- `name`
- `version`
- `platform` (linux|windows|android|mac)
- `status` (online|offline|degraded)
- `last_seen_at`
- `capabilities` (http_proxy, db_proxy, file_proxy, mqtt, etc.)

**network_segment**:
- `segment_id`
- `workspace_id`
- `label` (LAN, NAS, DB)
- `cidr_ranges`
- `allowed_ports`
- `policy_id`

**gateway_job**:
- `job_id`
- `gateway_id`
- `requested_by` (runner/workflow)
- `action` (http_call, db_query, file_read, file_write)
- `idempotency_key`
- `status` (queued|running|done|failed)
- `attempts`
- `result_ref`

## 6) API (минимум)

- `POST /edge/gateways:register` (регистрация + pairing)
- `GET  /edge/gateways` (листинг)
- `POST /edge/gateways/{id}:rotate_token` (ротация ключа)
- `POST /edge/jobs` (создать job)
- `GET  /edge/jobs?gateway_id=` (инспектор)
- `POST /edge/jobs/{id}:cancel`
- `POST /edge/segments` (создать сегмент)
- `GET  /edge/segments`

## 7) Безопасность

- Только исходящие соединения (без входящих портов).
- Short‑lived tokens для доступа к секретам.
- Подписание сборок gateway (supply‑chain security).
- Маскирование секретов в логах.
- Политика «least privilege» по сегментам и действиям.

## 8) Набор примеров

1) **Домашний NAS**: workflow → gateway → список файлов → индекс в Knowledge Vault.
2) **Офисная CRM в LAN**: workflow → gateway → выгрузка изменений → ETL блок.
3) **Android‑узел**: локальный сканер/сенсор → gateway → события → activity feed.

## 9) Зависимости

### Hard deps
- 32801–33200 `runtime_execution_os`
- 44801–45200 `workflow_runner_macro_engine_os`
- 61601–62000 `enterprise_connectors_credential_vault_os`
- 63201–63600 `multicloud_hybrid_connectivity_os`

### Optional deps
- 34801–35200 `observability_reliability_os`
- 34401–34800 `security_trust_os`
- 62401–62800 `connector_test_harness_ci_cd_os` (тестирование gateway интеграций)
- 62801–63200 `webhook_relay_tunnels_local_lab` (локальные события/туннели)
