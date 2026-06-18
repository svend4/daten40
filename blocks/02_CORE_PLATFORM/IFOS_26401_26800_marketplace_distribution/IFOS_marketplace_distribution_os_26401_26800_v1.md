# IFOS 26401–26800 — Marketplace & Distribution OS (v1)
Цель блока: превратить “хаос плагинов/сценариев/скриптов” в **управляемый рынок функций**, которые можно:
- найти (по смыслу, рейтингу, совместимости),
- установить (в один клик),
- безопасно запустить (sandbox),
- обновлять (каналы release, миграции),
- измерять качество (телеметрия, отзывы),
- собирать в “витрины” (готовые наборы под задачи).

Ниже — **по порядку, от простого к сложному**.

---

## 26401–26440 — MarketplaceItem: карточка “что это”
**MarketplaceItem** — базовое описание единицы в каталоге:
- id, name, short_description
- category/tags
- publisher
- pricing (free/paid/subscription) — даже если вы пока не продаёте
- links (docs/demo/repo)
- trust_badges (из Trust & Governance OS)
- supported_runtimes (wordpress/make/n8n/fastapi/local)

Смысл: чтобы один и тот же “компонент” имел стандартную карточку и мог ранжироваться.

---

## 26441–26490 — FunctionPackage: “упаковка” функции
**FunctionPackage** — то, что реально устанавливается:
- package_id, version (semver)
- entrypoints (install/run/uninstall/healthcheck)
- assets (файлы, шаблоны, схемы)
- config_schema (что надо спросить у пользователя)
- permissions (доступ к сети/файлам/секретам)
- integrity (хеши) и подпись

Это как “плагин WordPress” + “Make blueprint” + “Docker‑образ” в одной модели.

---

## 26491–26530 — Dependency + CompatibilityMatrix: зависимости и совместимость
**Dependency** описывает, от чего пакет зависит:
- другой пакет
- версия (>=1.2 <2.0)
- capabilities (например: “needs: vector_store”, “needs: telegram_bot”)

**CompatibilityMatrix** говорит, где пакет работает:
- runtime: wordpress 6.x, make, n8n, node-red, fastapi
- OS: linux/windows/android
- resources: RAM/CPU/disk
- conflicts: несовместимые пакеты

Зачем: “не ставить то, что заведомо не взлетит”.

---

## 26531–26580 — VitrineCard: витрины и “сборки под задачи”
**VitrineCard** — это кураторская/автоматическая витрина:
- цель (“Авто‑новости”, “Портал сравнения”, “CRM‑мини”)
- список пакетов (bundle)
- порядок установки
- демо‑данные и быстрый старт
- ожидаемый результат (скрин/описание)

Витрина — мост между “тысячи компонентов” и “одна кнопка: сделай мне систему”.

---

## 26581–26620 — RatingReview + TelemetryEvent: качество и обратная связь
**RatingReview**:
- звёзды, текст, pros/cons
- контекст: на каком runtime ставили, какие данные, какой тариф
- верификация: “реально установлено” (proof)

**TelemetryEvent** (опционально):
- install_success/fail
- run_duration
- error_codes
- usage counters

Важно: телеметрия должна уважать privacy и политики (Governance OS).

---

## 26621–26680 — InstallPlan: установка “в один клик”
InstallPlan — детальный план действий:
- что скачать
- какие зависимости поставить
- какие секреты запросить (SecretRef)
- какие миграции выполнить (если обновление)
- проверка подписи и целостности
- rollback план

InstallPlan — это “скрипт установки”, но описан декларативно и проверяемо.

---

## 26681–26730 — SandboxProfile + RuntimeRequirements: безопасный запуск
**SandboxProfile**:
- ограничения (no_shell/no_fs_write/no_external_network)
- allowlist доменов (если надо)
- лимиты времени/памяти
- режимы: preview/safe/prod

**RuntimeRequirements**:
- какие сервисы нужны (db/vectorstore/queue)
- какие permissions нужны
- какие порты/эндпоинты откроет

Так вы можете запускать чужие пакеты безопасно.

---

## 26731–26780 — Release + UpdatePolicy: релизы, каналы, миграции
**Release**:
- версия, дата
- changelog
- breaking changes
- migration scripts/steps

**UpdatePolicy**:
- канал: stable/beta/nightly
- автообновления: off/on
- ограничения: “не обновлять при active_jobs”
- backout policy

---

## 26781–26800 — Signatures: подписи, цепочка доверия, supply-chain
**PackageSignature**:
- signer_id, key_id
- signature (detached)
- signed_hashes
- timestamp

Проверка подписи + хешей — база B2B‑доверия: “мы ставим только то, что не подменили”.

---

## Мини‑архитектура “Marketplace OS”
1) Индексируем пакеты → MarketplaceIndex  
2) Пользователь выбирает витрину/пакет  
3) Строим InstallPlan (dependencies + compatibility + policy gates)  
4) Проверяем подпись/целостность  
5) Устанавливаем и запускаем в sandbox  
6) Пишем telemetry + reviews  
7) Обновления через каналы + миграции

---

## Что дальше логически
Следующий блок (если скажете “Продолжение”):
**26801–27200 — “Workspace & UI OS”**: рабочие пространства, карточки “как в офисных приложениях”, визуальный конструктор потоков, IDE‑режим, one‑click demo, библиотека макросов, шаблоны интерфейсов.
