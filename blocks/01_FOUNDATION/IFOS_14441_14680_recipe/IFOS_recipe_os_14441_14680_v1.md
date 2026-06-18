# IFOS 14441–14680 — Recipe‑OS: формальные рецепты, компиляция в Make/n8n/WP/CLI, evidence и one‑click bundles (v1)

Этот блок делает следующий уровень после “Function Wikipedia”:
- Function = атом (действие)
- Recipe = **готовый микро‑макрос**, который реально запускается
- Bundle = **пакет** (набор recipes + deps + install)
- Evidence = **доверие** (как доказать, что рецепт работает и не вредный)

Цель: **“одна идея → одна кнопка → работает в разных платформах”**.

---

## 14441–14460 — Recipe как объект (самое простое)

### 14441) Что такое Recipe (микро‑макрос)
Recipe — это описанный и переносимый сценарий, который:
- решает одну задачу (“RSS → Telegram дайджест”),
- содержит шаги (3–12),
- перечисляет secrets,
- имеет проверку (evidence plan),
- компилируется в targets (Make/n8n/WP/CLI).

### 14442) Стандартная структура Recipe
- `recipe_id` (stable)
- `title`, `goal`, `tags`
- `inputs` (параметры пользователя)
- `steps[]` (pipeline из actions)
- `secrets[]` (ключи)
- `policy` (PII/Money/Security)
- `evidence_plan` (как проверить)
- `targets[]` (куда компилировать)

### 14443) Почему Recipe важнее “статей”
Потому что:
- статья объясняет,
- recipe **включает кнопку** (install/run),
- recipe **воспроизводима** (evidence).

---

## 14461–14490 — Steps и типы шагов (среднее)

### 14461) Типы шагов (MVP)
- `action` — вызов function_id (из каталога)
- `transform` — преобразование данных (JSON → текст)
- `filter` — условие (если нет новых новостей — не отправлять)
- `foreach` — цикл по элементам
- `rate_limit` — паузы/backoff
- `store` — запись состояния (последний seen id)

### 14462) Контракт шага
Каждый step должен иметь:
- `id`
- `kind`
- `uses` (function_id) или `expr` (transform/filter)
- `in` mapping (куда подставить данные)
- `out` mapping (что сохраняем как переменные)
- `on_error` (retry/skip/fail)

### 14463) Идемпотентность
Рецепт обязан явно сказать:
- безопасно ли повторять шаг (idempotent)
- есть ли “ключ повторов” (например message dedupe key)

---

## 14491–14530 — Компиляция в targets (сложнее)

### 14491) Почему “компилятор”
Make/n8n/WP/CLI — разные форматы.
Но recipe должен быть один.
Компилятор:
- читает recipe JSON,
- строит граф шагов,
- подставляет нужные поля,
- генерирует артефакты под target.

### 14492) Targets (MVP)
- `make_blueprint_json`
- `n8n_workflow_json`
- `wp_bundle_manifest_json`
- `cli_script_bash`
- `cli_script_python`

### 14493) Ограничения компиляции
Не всё можно “один в один”:
- где-то нет foreach,
- где-то нет state store,
- где-то нет безопасного secret store.
Поэтому компилятор должен:
- делать best effort,
- писать “NOTES” в артефакт,
- и требовать ручные шаги при необходимости.

---

## 14531–14580 — Evidence: как доказать, что recipe работает (самое важное)

### 14531) Evidence plan (объект)
Evidence plan описывает:
- какие тесты сделать (schema_validate / dry_run / integration)
- какие условия считаем PASS
- какие артефакты сохранить (лог, скрин, checksum, snapshot)

### 14532) Evidence уровни
- **L0**: schema validate
- **L1**: dry-run (симуляция без внешних вызовов)
- **L2**: integration test (реальный вызов в sandbox)
- **L3**: production proof (подтверждение от пользователя/монитора)

### 14533) Почему evidence = вертикаль власти
Потому что иначе marketplace превращается в:
- мусор,
- фейки,
- вредоносные “кнопки”.

---

## 14581–14630 — Bundles: one‑click пакеты (сложнее)

### 14581) Bundle = набор recipes + deps + install plan
Bundle нужен, когда одной кнопки мало:
- “Travel Hub Starter” (RSS + сравнение + CRM + рассылка)
- “WP Commerce Pack” (плагины + webhook + платежи)

### 14582) Bundle manifest (что в нём)
- bundle_id, version
- recipes[] (включить)
- deps (плагины, env, сервисы)
- install plan (шаги установки)
- default secrets list
- evidence plan (на пакет)

### 14583) Marketplace и bundles
Marketplace показывает:
- Install (bundle)
- Run (recipes)
- Evidence (trust)
- Changelog

---

## 14631–14680 — Итог: от хаоса к кнопкам
Recipe‑OS даёт:
- единый формат рецептов,
- переносимость между платформами,
- честный контроль рисков,
- воспроизводимые доказательства,
- сборку “пакетов” под бизнес‑сценарии.

В приложении к этому блоку — схемы (JSON Schema), примеры recipes, заглушки артефактов targets и скелет компилятора.
