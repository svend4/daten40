# IFOS 67601–68000 — Developer Onboarding OS (v1)
**Задача блока:** сделать так, чтобы разработчик (или интегратор) мог:
- создать проект за 2–5 минут (как “File → New” в Office)
- сгенерировать коннектор/интеграцию “Hello World”
- получить автодокументацию, тесты, линтеры, примеры
- пройти проверку качества и опубликовать в marketplace
- не думать о “как хранить секреты”, “как делать sandbox”, “как не слить prod”

Этот блок напрямую закрывает ваш тезис: **не изобретать новое**, а “индустриализировать” интеграцию существующих решений.

Связи:
- использует **Test Keys & Safe Demo Assets OS** (67201–67600)
- использует **Credential Vault** (61601–62000)
- публикуется через **Marketplace & Curation** (45601–46000)
- запускается через **Workflow Runner / Macro Engine** (44801–45200)

Порядок: простое → среднее → сложное.

---

## 67601–67640 — Простое: “File → New” для интеграций
### ProjectTemplate
Шаблон проекта: структура репозитория, зависимости, окружение, минимальная документация.
Цель: единый стандарт, чтобы любой проект выглядел знакомо.

Состав:
- language/runtime (python/node/go)
- scaffold manifest (папки/файлы)
- default CI (lint, tests)
- “getting started”
- hooks: connect to vault, use sandbox keys, run sample pipeline

Результат: команда `ifos init` создаёт repo, который **уже запускается**.

---

## 67641–67720 — База: ConnectorTemplate + генератор коннекторов
### ConnectorTemplate
Шаблон коннектора: как описать API сервиса так, чтобы:
- можно было сделать REST/GraphQL/Webhooks
- можно было автоматически собрать SDK
- можно было автоматически сделать UI-форму настройки
- можно было автоматически сделать тесты по fixtures

### ScaffoldRequest → ScaffoldResult
Генератор получает:
- provider_id (из sandbox registry)
- auth type (api_key/oauth/webhook_secret)
- endpoints (sandbox allowlist)
- операции (list/get/create/update)
и возвращает готовый “скелет” коннектора.

---

## 67721–67800 — Среднее: Документация и примеры как продукт
### DocsTemplate
Шаблон документации:
- Overview (что делает)
- Auth (как получить тест‑ключ)
- Quickstart (5 минут)
- Examples (готовые payloads)
- Troubleshooting (типовые ошибки)
- Security (что нельзя)

### DocsBuildJob
Сборка документации:
- извлекает описание API/операций
- добавляет примеры/fixtures
- генерирует страницы для marketplace (карточка, витрина, “one-click”)

---

## 67801–67880 — Среднее+: Валидация качества (Validation Rules)
Набор “автопроверок”, которые не дают выпускать мусор:
- endpoint_guardrail: запрет prod endpoint
- scopes_guardrail: запрет опасных scopes
- secret_leak_scan: нет секретов в git
- lint/tests: базовые проверки
- docs_minimum: наличие quickstart + examples
- demo_assets_required: если коннектор публичный — должны быть demo assets

Правило: **нельзя публиковать без прохождения validation pack**.

---

## 67881–67960 — Сложное: Pipeline публикации (PublishingPipeline)
PublishingPipeline описывает путь “из repo → в marketplace”:
1) build (package)
2) validate (quality gates)
3) sign (подпись артефакта)
4) publish (канал: private/public)
5) notify (обновить витрины/каталоги)
6) post-publish smoke tests (в sandbox)

Важное: pipeline должен быть воспроизводимым (reproducible build).

---

## 67961–68000 — Сложное+: Onboarding Tracks (обучение как “курсы Office”)
OnboardingTrack — сценарий обучения:
- уровень: beginner/intermediate/advanced
- уроки: 10–20 минут
- практики: собрать trial bundle, написать коннектор, пройти публикацию
- проверка: автотест + “badge”

Цель: не просто “инструмент”, а **массовое внедрение**.

---

## Мини‑MVP (самое важное)
Если делать быстро:
1) 3 ProjectTemplate (Python FastAPI, Node, “No-code pack” для Make/n8n)
2) 5 ConnectorTemplate (REST API key, REST OAuth, Webhooks, Storage, Messaging)
3) 10 Validation Rules (минимум)
4) 1 Publishing pipeline (private channel)
5) 2 Tracks (Beginner + Marketplace Publisher)

Следующий блок по порядку:
**68001–68400 — “Connector Marketplace Publishing OS: Reproducible Builds & Signing”**
(подписи, SBOM, supply-chain security, provenance, trust score).
