# IFOS 30801–31200 — Automation Blueprints OS (v1)
Цель: “макросы для интернета” — **шаблоны автоматизаций 1‑кнопка** (Make/n8n/WordPress/скрипты), которые:
- легко импортируются/экспортируются,
- параметризуются (как “переменные”),
- тестируются (как unit/integration),
- превращаются в витрины “Install → Configure → Run”.

Порядок: от простого к сложному.

---

## 30801–30840 — Что такое Blueprint (интернет‑макрос)
Blueprint = **описание готового сценария**:
- что делает (intention)
- входы/выходы (inputs/outputs)
- граф шагов (pipeline graph)
- параметры (params) + значения по умолчанию
- требования (secrets/permissions/capabilities)
- тесты (test suites)
- инструкции (human steps)

Blueprint должен быть “меньше чем продукт”, но “больше чем кусок кода”.

---

## 30841–30890 — Типы blueprint’ов (простые → средние)
1) **Single‑Action**: 1 триггер → 1 действие (например “RSS → Telegram”)
2) **Fan‑out**: 1 триггер → N каналов (Telegram + Email + Sheets)
3) **Aggregation**: сбор → дедуп → суммаризация → выдача
4) **Approval Loop**: человек подтверждает (approve/deny)
5) **Batch & Backfill**: “догрузить историю за 90 дней”

---

## 30891–30930 — Параметризация (как макросы в Excel)
Параметры разделяются:
- **secrets**: токены, ключи (через SecretRef)
- **endpoints**: URL, домены, пути
- **selectors**: CSS/XPath/regex
- **schedules**: cron, daily@08:00
- **thresholds**: лимиты, дедуп‑окна, size limits
- **toggles**: флаги (enable_summarize, enable_translate)

Правило: blueprint без параметров превращается в “жёсткий скрипт” и плохо переиспользуется.

---

## 30931–30980 — Импорт из Make / n8n / WordPress (инвентаризация)
### Make
Импортируем:
- список модулей, connections, webhooks
- mapping полей
- расписания
- используемые приложения

Цель: автоматически построить PipelineGraph + ParamSet.

### n8n
Импортируем:
- nodes, credentials, triggers
- expressions
- error handlers

### WordPress
Не импорт “плагинов как кода”, а **инвентаризация**:
- какие плагины установлены
- какие активны
- какие роли/права
- какие конфиги
Потом делаем blueprint “набор плагинов + настройки”, как “пакет функциональности сайта”.

---

## 30981–31030 — Тесты blueprint’ов (минимально жизненно)
Blueprint tests:
- **schema tests**: параметры валидны
- **dry-run**: все dependencies доступны, secrets присутствуют
- **golden output**: на тестовом входе результат совпадает
- **contract tests**: API сервисов отвечает как ожидается
- **rate-limit tests**: сценарий не превышает лимиты

Почему важно: “1 кнопка” без тестов превращается в “1 кнопка — 1 ошибка”.

---

## 31031–31080 — Конструктор PipelineGraph (от схемы к исполнению)
PipelineGraph:
- узлы: trigger, transform, enrich, route, store, notify
- рёбра: dataflow + controlflow
- обработка ошибок: retry/backoff/fallback
- наблюдаемость: metrics + logs + traces

GraphCompiler превращает граф в:
- Make scenario (если есть совместимость)
- n8n workflow
- IFOS job spec (внутренний runtime)
- dockerized runner (если надо)

---

## 31081–31130 — Экспорт/пакетирование blueprint’ов
ExportBundle:
- blueprint.json
- params.json (без секретов)
- UI form schema (как анкета)
- test suite
- screenshots / docs
- signature + attestation (через Security OS)

Так blueprint становится переносимым и пригодным для Marketplace.

---

## 31131–31180 — UI формы и “интервью-установка”
BlueprintUIForm:
- поля параметров
- подсказки (“где взять токен”)
- проверки
- калькуляция риска (“пакет просит доступ к Drive write”)
- кнопка “Test connection”

Идея: пользователь не читает документацию — он проходит “мастер установки”.

---

## 31181–31200 — “1‑кнопка макросы” как библиотека для офиса/дома
Сборники (collections) blueprint’ов:
- Office Essentials (почта, CRM, документы)
- Home Care (напоминания, медданные, покупки)
- Travel Hub (поиск/сравнение/новости/маршруты)
- WordPress Site Ops (бэкапы, обновления, безопасность)

Это уже **операционная система сценариев**: выбираешь — ставишь — работает.

---

## Мини‑архитектура Blueprints OS
Blueprint → Params → Importers (Make/n8n/WP) → Tests → PipelineGraph → Compiler → ExportBundle → UI Form → Marketplace

---

## Что дальше логически
Следующий блок (если скажете “Продолжение”):
**31201–31600 — Observability & Reliability OS**: метрики, health checks, алерты, SLO/SLA, автопочинка, “красные кнопки”, canary/rollout, журналы инцидентов.
