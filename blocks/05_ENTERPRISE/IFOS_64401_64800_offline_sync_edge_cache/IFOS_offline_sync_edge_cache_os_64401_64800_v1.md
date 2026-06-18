# IFOS — Offline Sync & Edge Cache (Bundles, Registry, Knowledge Vault) (Блок 64401–64800)

Версия: v1 · Пакет: `IFOS_64401_64800_offline_sync_edge_cache_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

В твоей исходной идее IFOS должен работать **как офисный пакет**, но для интернета: кнопки, макросы, витрины, сценарии — и всё это должно работать **не только в идеальном облаке**, а в реальности:
- слабый интернет/обрыв связи,
- мобильные устройства (Android),
- офисные сети с ограничениями,
- приватные узлы (gateway) и локальные хранилища.

Если нет offline‑слоя, любой «one‑click bundle» ломается: пользователь нажал, но пакет не скачался, документация не открылась, сценарий не установился.

Этот блок вводит стандарт IFOS: **локальный кеш + синхронизация** (offline-first) для:
- реестра функций (registry),
- бандлов (packages/bundles),
- знаний/документов (knowledge vault),
- настроек/профилей и макросов.

## 1) Что делает (функции)

1) **Edge Cache Store**: локальное хранилище артефактов (registry snapshots, bundle zips, docs, assets).
2) **Delta Sync**: синхронизация по изменениям (manifest-based), а не «качать всё заново».
3) **Profiles & Scopes**: что синхронизировать (workspace, коллекции, избранное, курсы, витрины).
4) **Conflict Resolution**: правила конфликтов для настроек/заметок/макросов.
5) **Integrity & Signatures**: проверка целостности (hash) и подписи (для пакетов/релизов).
6) **Retry & Backoff**: устойчивость к сетевым проблемам.
7) **Partial Offline Mode**: режим «просмотр/поиск по кешу» без сети.
8) **Background Prefetch**: предзагрузка нужного (например, пакет курса/демо).
9) **Cache Policy**: LRU/TTL/квоты по диску, приоритеты хранения.

## 2) Что НЕ делает (границы)

- Не заменяет полноценную систему резервного копирования предприятия.
- Не делает тяжелую репликацию БД «как Postgres streaming replication» — это offline слой для артефактов IFOS.
- Не решает правовые вопросы хранения (это в compliance/политиках), но уважает политики (что можно кешировать).

## 3) MVP (простое → среднее → сложное)

### 3.1 Простое (P1.1)

- Локальный каталог кеша + индекс (SQLite/JSON)
- Скачивание bundle по ID и хранение версии
- Проверка hash (sha256)
- Offline просмотр документации пакета


### 3.2 Среднее (P1.2)

- Delta sync по manifest (скачать только отличия)
- Prefetch избранного/курсов/витрин
- Очередь задач синхронизации + ретраи
- Политики квот (max_cache_mb)


### 3.3 Сложное (P1.3)

- Конфликты и merge для user‑контента (макросы/настройки)
- Подписи пакетов (signed bundles)
- Мульти‑девайс синк (несколько устройств одного пользователя)
- Edge pinning: «закрепить этот пакет всегда доступным»

## 4) Архитектура

### 4.1 Компоненты
- **Sync Orchestrator**: планирует задачи синхронизации.
- **Cache Store**: хранит blobs + индекс.
- **Manifest Resolver**: сравнивает версии/хэши и строит план delta.
- **Policy Gate**: проверяет, что разрешено кешировать.

### 4.2 Потоки
A) Online: UI → request bundle → cache hit? → если нет → download → verify → store → open
B) Offline: UI → open from cache → search local index
C) Sync: scheduler → compute delta → fetch chunks → verify → commit

## 5) Модель данных

**cache_object**:
- `object_id`
- `type` (bundle|doc|asset|registry_snapshot)
- `source_ref` (market://pkg/…, registry://snapshot/…)
- `version`
- `sha256`
- `size_bytes`
- `stored_path`
- `pinned` (bool)
- `last_accessed_at`
- `ttl_expires_at`

**sync_job**:
- `job_id`
- `workspace_id`
- `profile_id`
- `status` (queued|running|done|failed)
- `attempts`
- `bytes_downloaded`
- `started_at` / `ended_at`

**sync_profile**:
- `profile_id`
- `name`
- `scopes` (registry, bundles, docs, favorites, courses)
- `max_cache_mb`
- `prefetch_rules`
- `conflict_policy`

## 6) API (минимум)

- `POST /offline/cache:put` (поместить объект)
- `GET  /offline/cache:fetch?ref=` (получить по ref)
- `POST /offline/cache:pin` / `:unpin`
- `GET  /offline/cache:stats`
- `POST /offline/sync-jobs` (создать sync job)
- `GET  /offline/sync-jobs` (статус)
- `POST /offline/sync-profiles` (профили)

## 7) Интеграция с «one‑click bundles»

Ключевое: install/run не должен зависеть от «сегодня хороший интернет».
- UI показывает: **доступно офлайн** / **требует сети**.
- Wizard может предложить: «предзагрузить пакет курса на 200 МБ».
- Runner может брать артефакты из локального кеша, если политика разрешает.

## 8) Зависимости

### Hard deps
- 55601–56000 `distribution_sync_os` (базовая синхронизация и профили)
- 44001–44400 `searchable_knowledge_vault_os` (объекты знаний)
- 48801–49200 `one_click_bundles_templates_os` (потребитель кеша)
- 40401–40800 `data_lineage_provenance_os` (пометки версий/источников)

### Optional deps
- 61601–62000 `enterprise_connectors_credential_vault_os` (если кеш требует авторизации)
- 64001–64400 `device_fleet_remote_ops` (управление кеш‑профилями на устройствах)
- 34801–35200 `observability_reliability_os` (метрики синхронизации)
- 41201–41600 `data_privacy_compliance_os` (политики что можно кешировать)
