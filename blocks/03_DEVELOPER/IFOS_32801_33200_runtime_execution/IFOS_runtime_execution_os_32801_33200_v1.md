# IFOS 32801–33200 — Runtime & Execution OS (v1)
Цель: сделать так, чтобы “функции интернета” из Registry/Marketplace **реально запускались**:
- безопасно (sandbox/policies),
- повторяемо (детерминированные рецепты, pinned versions),
- наблюдаемо (логи/метрики/health),
- переносимо (“run anywhere”: сервер/контейнер/K8s/Android),
- с секретами (ключи API) и правами (entitlements),
- с откатом (rollback) и обновлениями (update channels).

Порядок: простое → среднее → сложное.

---

## 32801–32830 — Базовая модель запуска: RunRequest → RunResult
Минимальная схема:
1) пользователь выбирает item/bundle/vitrine;
2) Runtime поднимает окружение (RuntimeEnvironment);
3) связывает секреты (SecretBinding);
4) применяет политики (ExecutionPolicy);
5) запускает (RunRequest) → выдаёт статус (RunResult) + логи + health.

Ключевой принцип: **Installer устанавливает, Runtime запускает.**

---

## 32831–32870 — RuntimeEnvironment: “где именно это крутится”
RuntimeEnvironment описывает, *в каком типе среды* исполняем:
- local (на машине пользователя),
- docker-compose,
- kubernetes,
- vm micro (в будущем: firecracker),
- wasm (безопасная песочница),
- android-termux (локальный запуск на Android),
- managed (облачный раннер платформы).

Сюда входят:
- ограничения ресурсов (CPU/RAM/Disk/Net),
- требования к рантайму (node/python/php/java),
- “capabilities” (что разрешено: сеть, файловая система, внешние процессы).

---

## 32871–32920 — Секреты: SecretRef и SecretBinding
Проблема: любая интеграция живёт на ключах.
Нужно:
- SecretRef: “ссылка на секрет” (а не сам секрет),
- SecretBinding: как секрет “впрыскивается” (env var, file, vault mount),
- политика хранения: локально (encrypted), серверно (vault), device keystore (Android).

Обязательные требования:
- секреты **не попадают в логи**,
- секреты можно “ротировать” (сменить ключ без пересборки),
- минимальные права (scope).

---

## 32921–32960 — SandboxProfile: как изолировать выполнение
SandboxProfile задаёт “клетку”:
- network: allow/deny + allowlist доменов
- filesystem: read-only, tmp, mounts
- processes: запрет shell или ограничение
- timeouts: max runtime
- syscalls: (для VM/WASM) ограничения уровня ОС

Режимы:
- permissive (dev),
- balanced (default),
- strict (production/marketplace).

---

## 32961–33010 — ExecutionPolicy: политика безопасности и комплаенса
ExecutionPolicy — набор правил:
- что можно вызывать (domains, ports, api scopes),
- какие коннекторы разрешены,
- ограничения по данным (PII, финансы),
- запрет “dangerous ops” (сканирование сети, массовые рассылки без подтверждения),
- лимиты расходов (usage caps).

Важно: политика может быть:
- платформенная (общая),
- организационная (company policy),
- пользовательская (мой профиль безопасности).

---

## 33011–33060 — Оркестрация: Scheduler + Queue + Job Events
Чтобы “кнопка” работала на практике:
- JobQueue: очередь задач (install/run/update),
- Scheduler: cron, event-based, webhook triggers,
- JobEvent: статусы (queued/running/succeeded/failed/canceled),
- Retries: с backoff,
- Idempotency: повтор не создаёт дубль выполнения.

Это делает IFOS похожим на “Make/n8n”, но на уровне **универсального рантайма**.

---

## 33061–33110 — Connector Drivers: “драйверы интернета”
Нужен единый слой “драйверов” для сервисов:
- Gmail/SMTP, Telegram, Slack
- Google Drive, Dropbox
- RSS, Web scraping
- Stripe/PayPal (если разрешено)
- WordPress, CRM, ERP
- LLM providers (опционально)

Driver содержит:
- auth схемы,
- I/O форматы,
- rate limits,
- тестовый режим (sandbox keys),
- “capabilities mapping” (чтобы Registry знал, что это умеет).

---

## 33111–33140 — Наблюдаемость: логи, метрики, health
Минимум:
- LogEntry: уровни, кореляция (trace_id), masking секретов
- HealthStatus: жив ли сервис/коннектор, latency, error rate
- RunResult: ссылку на “run report” (артефакты запуска)

Бонус:
- cost telemetry (стоимость вызовов),
- “why failed” (структурированная причина).

---

## 33141–33170 — Откат и обновления
RollbackPlan описывает:
- как откатить установку,
- как вернуть конфигурацию,
- как откатить миграции данных,
- как “заморозить” версию (pin).

Update channels:
- stable / beta / nightly,
- staged rollout (10% → 50% → 100%),
- auto-update только при прохождении health checks.

---

## 33171–33190 — Run Anywhere: сервер / контейнер / Android
Ключевой продуктовый ход: “работает даже без сервера”.
Варианты:
- Docker/Compose (самый простой для self-hosted)
- K8s (для крупных)
- Android Termux (для прототипов и лёгких раннеров)
- WASM sandbox (для безопасного исполнения небольших функций)

Android‑вариант:
- локальный раннер + “тонкий UI”,
- секреты в Android keystore,
- ограничения фоновых задач (WorkManager).

---

## 33191–33200 — Provenance & Supply‑Chain
Чтобы Marketplace не превратился в “зоопарк вредоносного”:
- ArtifactProvenance: откуда артефакт, кто собрал, хеши, подпись
- SBOM (в будущем): список зависимостей
- policy: запрещать неизвестные источники
- quarantine: подозрительные сборки не запускаются

---

## Что дальше
Следующий блок:
**33201–33600 — Data Quality & Dedup OS** (дедупликация, нормализация карточек, “одно и то же” под разными названиями, канонические IDs, merge/conflict, источники правды, импорт из GitHub/Make/WP/Store).  
Скажете “Продолжение” — сделаю.
