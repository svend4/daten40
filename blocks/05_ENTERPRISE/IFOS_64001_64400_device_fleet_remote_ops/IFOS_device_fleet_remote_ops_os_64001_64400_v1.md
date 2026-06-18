# IFOS — Device Fleet & Remote Operations (Gateways, Agents, Edge Nodes) (Блок 64001–64400)

Версия: v1 · Пакет: `IFOS_64001_64400_device_fleet_remote_ops_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

Если IFOS реально становится «операционной системой функций интернета», то в ней будут работать **агенты и узлы**:
- Edge Gateway в офисах/домах,
- локальные tunnel‑агенты,
- раннеры/workflow‑исполнители,
- приватные коннекторы,
- мобильные узлы (Android/мини‑ПК).

Без управления парком устройств система превращается в «зоопарк»: версии расходятся, ключи протекают, узлы падают, никто не знает где что запущено.

Этот блок — слой **Remote Ops/MDM‑подобного управления**: инвентаризация, удалённые команды, обновления, конфигурации, диагностика, безопасная ротация ключей, политика доступа.

## 1) Что делает (функции)

1) **Device Inventory**: учёт всех узлов (gateway/tunnel/runner/edge node) с метаданными.
2) **Remote Config**: централизованные профили конфигураций и их применение.
3) **Version & Update Management**: контроль версий, каналы обновления (stable/beta), авто‑апдейты.
4) **Remote Actions**: перезапуск, переподключение туннеля, сбор диагностики, тест‑пинг.
5) **Key Rotation & Attestation**: ротация токенов, проверка подписи сборок (supply‑chain).
6) **Health Policies**: SLO/пороговые правила (offline > N минут → алерт/авто‑ремедиация).
7) **Secure Logs & Diagnostics**: выгрузка логов и дампов с маскированием секретов.
8) **Ownership & Delegation**: владелец узла, команды доступа, делегирование.
9) **Quarantine**: изоляция подозрительного узла (отключить задания, закрыть доступ к секретам).

## 2) Что НЕ делает

- Не является полноценным MDM для смартфонов (как Intune), но покрывает управление **IFOS‑агентами**.
- Не заменяет observability‑платформу целиком: метрики/логи — в соседнем блоке, здесь — управление парком.

## 3) MVP (простое → среднее → сложное)

### 3.1 Простое

- Реестр устройств (тип, версия, статус, last_seen)
- Удалённая ротация токена
- Команды: restart, reconnect, ping
- Экспорт списка устройств


### 3.2 Среднее

- Профили конфигурации + rollout по группам
- Каналы обновлений + авто‑апдейт
- Quarantine + политика доступа к vault
- Диагностика (logs bundle)


### 3.3 Сложное

- Attestation (подписанные сборки)
- Remediation playbooks (авто‑перезапуск, failover)
- Взаимодействие с enterprise change control

## 4) Модель данных

**device_node**:
- `device_id`
- `workspace_id`
- `type` (edge_gateway|tunnel_agent|runner|edge_node)
- `name`
- `version`
- `platform` (linux|windows|android|mac)
- `status` (online|offline|degraded|quarantined)
- `last_seen_at`
- `labels` (env=dev, site=office1, role=gateway)
- `owner_user_id`

**config_profile**:
- `profile_id`
- `workspace_id`
- `target_types` (list)
- `config_blob_ref` (storage)
- `rollout_strategy` (all|canary|ring)

**device_action**:
- `action_id`
- `device_id`
- `action` (restart|reconnect|collect_logs|rotate_token)
- `requested_by`
- `status`
- `result_ref`

**update_channel**:
- `channel_id` (stable|beta)
- `artifact_ref`
- `min_version`

## 5) API (минимум)

- `GET  /ops/devices` (инвентаризация)
- `POST /ops/devices/{id}:rotate_token`
- `POST /ops/devices/{id}:action` (restart/reconnect/collect_logs)
- `POST /ops/config-profiles` (создать профиль)
- `POST /ops/config-profiles/{id}:apply` (применить)
- `POST /ops/updates/channels` (каналы обновлений)
- `POST /ops/devices/{id}:quarantine` / `:unquarantine`

## 6) Зависимости

### Hard deps
- 34801–35200 `observability_reliability_os` (метрики/логи)
- 51201–51600 `feature_flags_remote_config_os` (базовый remote config)
- 61601–62000 `enterprise_connectors_credential_vault_os` (секреты/токены)
- 59601–60000 `enterprise_rollouts_change_control_os` (rollout templates)

### Optional deps
- 63601–64000 `edge_gateway_private_connectivity` (управление gateway)
- 62801–63200 `webhook_relay_tunnels_local_lab` (управление tunnel-агентами)
- 62401–62800 `connector_test_harness_ci_cd_os` (проверка версий/регрессии)
- 34001–34400 `enterprise_governance_os` (RBAC/политики оргуровня)
