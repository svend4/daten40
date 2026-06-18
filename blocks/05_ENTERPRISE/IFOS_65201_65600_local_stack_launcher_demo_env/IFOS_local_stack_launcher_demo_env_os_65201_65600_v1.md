# IFOS — Local Stack Launcher & Demo Environments (One-Command IFOS) (Блок 65201–65600)

Версия: v1 · Пакет: `IFOS_65201_65600_local_stack_launcher_demo_env_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

Ты много раз упирался в практическую проблему: **код есть**, плагины/коннекторы/макросы есть,
но **«запустить и попробовать» сложно**. В результате экосистема выглядит как «дикое поле»:
- тысячи решений на GitHub,
- сотни тысяч плагинов (WordPress),
- тысячи сценариев (Make/n8n),
но мало «витрин» и почти нет режима **one‑click demo**.

Этот блок добавляет в IFOS стандарт: **Local Stack Launcher** — «офисная установка» IFOS
в один шаг (локально на ПК/сервере/частично на Android через Termux/контейнеры),
с демо‑данными, тестовыми ключами, туннелями и примером «первого рабочего сценария».

Цель: чтобы любой мог:
1) поднять минимальную сборку IFOS,
2) открыть UI,
3) импортировать 1–2 бандла,
4) увидеть витрину/макрос,
5) прогнать тестовый webhook,
и понять ценность за 10–20 минут.

## 1) Что делает (функции)

1) **One-command bootstrap**: `ifos up` / `docker compose up` / `make up`.
2) **Reference topology**: минимальный набор сервисов (UI, API, registry, storage, runner).
3) **Demo seeds**: демо‑workspace, 2–3 витрины, 1–2 макроса, 1 курс.
4) **Test keys & sandbox**: подключает каталог тест‑ключей и профили окружений.
5) **Local webhook lab**: связка с webhook‑relay (локальная проверка).
6) **Healthchecks & self-diagnosis**: проверка портов, зависимостей, логов.
7) **Upgrade path**: сценарий обновления стека без «сломать всё».
8) **Export snapshot**: выгрузка demo‑состояния для передачи/поддержки.

## 2) Что НЕ делает

- Не является продакшн‑инсталлятором уровня Kubernetes‑платформы.
- Не решает все вопросы enterprise‑интеграций (это отдельные блоки), но даёт их «сухую симуляцию».
- Не гарантирует работу на любом Android без ограничений (зависит от устройства), но задаёт шаблон.

## 3) MVP (простое → среднее → сложное)

### 3.1 Простое (P1.1)

- docker-compose.yml + .env.example
- UI доступен по `http://localhost:8080`
- API health `/health`
- Импорт одного бандла из локального файла


### 3.2 Среднее (P1.2)

- Демоданные (workspace + витрины + макросы)
- Тестовые ключи/профили окружений
- Webhook lab: публичный URL → tunnel → локальный обработчик
- Команда `ifos doctor` (проверки)


### 3.3 Сложное (P1.3)

- Поддержка профилей установки (minimal / demo / dev / edge)
- Авто‑обновление образов + миграции
- Экспорт/импорт snapshot (для поддержки и переносов)
- Локальный marketplace mirror (кеш пакетов)

## 4) Референс-стек (минимальный набор)

- **ifos-ui** (app shell + офисный UI)
- **ifos-api** (registry, bundles, users)
- **ifos-runner** (workflow/macro engine)
- **ifos-storage** (S3-совместимое хранилище или local fs)
- **ifos-db** (Postgres/SQLite — на выбор)
- **ifos-queue** (Redis/NATS — для задач)
- **ifos-hooks** (webhook ingress/relay, опционально)

Смысл: стартовать с малого, но чтобы “кнопки работали” — есть runner, очередь и хранилище.

## 5) Команды (псевдо-CLI контракт)

- `ifos up [--profile minimal|demo|dev|edge]`
- `ifos down`
- `ifos doctor` (проверка: порты, БД, очередь, подписи)
- `ifos seed demo` (залить демоданные)
- `ifos import bundle <file>`
- `ifos snapshot export` / `import`

## 6) Конфигурация и профили

Профиль — это набор значений для .env и compose overrides:
- `IFOS_PROFILE=minimal|demo|dev|edge`
- `IFOS_STORAGE=local|minio|s3`
- `IFOS_DB=sqlite|postgres`
- `IFOS_ENABLE_HOOKS=true|false`
- `IFOS_ENABLE_OFFLINE_CACHE=true|false`
- `IFOS_ENABLE_TUNNELS=true|false`

## 7) Связь с твоей исходной идеей

Это прямо про «рационализацию вместо изобретательства»:
- мы не пишем заново WordPress/Make/n8n,
- мы делаем **понятный запуск**, каталогизацию и витрины,
- чтобы существующие модули превращались в «офисные кнопки» и макросы.

Local Stack — это мост от «описаний» к «действующим демонстрациям».

## 8) Зависимости

### Hard deps
- 38801–39200 `app_shell_navigation_os` (UI shell)
- 32801–33200 `runtime_execution_os` (runner)
- 44801–45200 `workflow_runner_macro_engine_os` (макросы)
- 62001–62400 `sandbox_test_keys_dev_env_os` (тестовые ключи)

### Optional deps
- 64401–64800 `offline_sync_edge_cache` (кеш пакетов/доков)
- 64801–65200 `webhook_relay_tunnels_local_lab` (webhooks)
- 62401–62800 `connector_test_harness_ci_cd_os` (автотесты)
- 63601–64000 `edge_gateway_private_connectivity_os` (edge профиль)
