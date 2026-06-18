# IFOS 38001–38400 — Developer Platform & SDK OS (v1)
Цель: чтобы “интернет функций” рос как экосистема, а не как хаотичный набор скриптов.
Здесь появляются:
- плагины как стандартный формат расширений
- шаблоны/скелеты (scaffolding) под типовые интеграции
- генерация SDK (Python/JS/Go) из OpenAPI/JSON Schema
- песочницы (sandbox) для тестов и дебага
- контрактное тестирование (чтобы не ломать совместимость)
- публикация в marketplace (release pipeline)

Порядок: простое → среднее → сложное.

---

## 38001–38030 — PluginManifest: плагин как продукт
PluginManifest описывает плагин:
- имя, автор, лицензия
- capabilities (tools, workflows, UI cards)
- dependencies (минимальная версия IFOS, сторонние пакеты)
- security (что трогает, какие секреты нужны)
- docs (readme, примеры, витрина)

Смысл: “плагин можно установить и понять” без личного общения с автором.

---

## 38031–38070 — Template Packs: “скелеты” для типовых задач
TemplatePack = набор шаблонов:
- коннектор к API (auth + pagination + retries)
- webhook intake → normalize → store
- импорт CSV/Drive → dedup → registry
- Make/n8n bridge template

Плюс: одна кнопка “создать проект интеграции”, как `create-react-app` для IFOS.

---

## 38071–38110 — Scaffolding: генерация проекта под задачу
ScaffoldRequest задаёт:
- тип (connector / tool-pack / workflow-pack / UI-pack)
- целевые языки (py/js)
- сервисы (qdrant, postgres)
- стиль (sync/async)
- тестовый стенд (docker compose)

ScaffoldResult возвращает:
- структуру файлов
- конфиги
- примерные тесты
- README

---

## 38111–38160 — SDK Profiles: где и как генерировать SDK
SDKProfile описывает:
- язык и версию (python 3.12, node 20)
- стиль клиента (sync/async)
- auth adapters (api key, oauth)
- retries/backoff defaults
- logging hooks

Так разные команды получают одинаковый “фирменный” SDK.

---

## 38161–38210 — SDK Packages: результат генерации
SDKPackage включает:
- код клиента
- модели данных (types)
- примеры запросов
- mock server / fixtures
- changelog

Это снижает порог входа: интеграции делаются быстрее и качественнее.

---

## 38211–38260 — Sandbox: песочница для тестов и дебага
SandboxEnv:
- изолированное окружение (docker/k8s namespace)
- фейковые секреты
- тестовые данные
- локальный “mock external services”

Принцип: “интеграцию можно обкатать без риска испортить прод”.

---

## 38261–38310 — Contract Tests: не ломаем совместимость
ContractTest проверяет:
- схемы входов/выходов
- обязательные поля
- backward compatibility (semver)
- rate limit поведение
- error shapes (как выглядят ошибки)

Смысл: marketplace масштабируется только при стабильных контрактах.

---

## 38311–38360 — Publishing Job: публикация в marketplace
PublishingJob:
- сборка (build)
- проверка (lint/tests/contract tests)
- security scan (secrets, deps)
- подписывание артефактов
- публикация (draft → review → release)

Идея: “плагин проходит pipeline как любой enterprise продукт”.

---

## 38361–38400 — Compatibility Matrix: экосистема без ада версий
CompatibilityMatrix описывает:
- plugin version ↔ IFOS version
- plugin ↔ plugin dependencies
- breaking changes
- migration hints

Это то, чего не хватает WordPress/Make: понятная совместимость и миграции.

---

## Итог блока
Developer Platform & SDK OS делает “рационализацию интернет‑функций” масштабируемой:
- авторы создают плагины быстрее
- пользователи устанавливают без боли
- совместимость контролируется
- качество проверяется автоматически

---

## Что дальше
Следующий блок:
**38401–38800 — UI Builder & Interaction OS** (карточки функций, конструктор витрин, формы, ручной/авто режимы, explainability).  
Скажете “Продолжение” — сделаю.
