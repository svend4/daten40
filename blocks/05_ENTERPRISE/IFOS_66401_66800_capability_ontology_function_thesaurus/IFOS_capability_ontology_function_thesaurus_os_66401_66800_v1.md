# IFOS — Capability Ontology & Function Thesaurus (IFOS Lexicon / Grammar) (Блок 66401–66800)

Версия: v1 · Пакет: `IFOS_66401_66800_capability_ontology_function_thesaurus_os_pack.zip` · Дата: 2026-01-03

## 0) Идея (почему этот блок вообще нужен)

Ты сформулировал ключевую мысль: **рационализация и интеграция** — это отдельная
ценность, и ей не хватает «операционной системы функций».

Чтобы каталог Make/WordPress/GitHub стал управляемым, нужна **общая грамматика функций**:
- единый словарь (capabilities),
- синонимы/варианты (thesaurus),
- связи (часть‑целое, зависит‑от, альтернатива‑к),
- минимальная “семантика” для сравнения и поиска.

Этот блок вводит **IFOS Lexicon** — онтологию и тезаурус функций.

## 1) Что делает (функции)

1) **Capability Ontology**: иерархия функций (как в «офисном меню»).
2) **Thesaurus**: синонимы/варианты названий (например webhook ↔ callback).
3) **Relations**:
   - `requires` (требует)
   - `provides` (даёт)
   - `alternative_to` (альтернатива)
   - `part_of` (часть)
   - `compatible_with` (совместимо)
4) **Function Grammar**: простая грамматика “действие + объект + канал + условие”.
5) **Mapping rules**: правила привязки к коннекторам/узлам/каталогам.
6) **Normalization**: единый формат id (`cap:domain.verb_object`).
7) **Evidence model**: как подтверждается capability (README, OpenAPI, deps, отзывы).

## 2) Что НЕ делает

- Не является полной философской онтологией всего мира.
- Не заменяет реальную документацию конкретного продукта.
- Не «магически» определяет смысл: даёт структуру, а качество улучшается фидбеком.

## 3) Базовая модель capability

### Поля (минимум)
- `capability_id`
- `name`
- `description`
- `domain` (news/office/commerce/security/...)
- `inputs` / `outputs`
- `preconditions`
- `evidence_types`
- `risk_level` (L/M/H)
- `examples`

### Уровни (слои)
- L0: примитивы (HTTP request, webhook receiver)
- L1: функции (import RSS, dedup items)
- L2: макро‑функции (news digest pipeline)
- L3: пакеты/продукты (one‑click solution)

## 4) Function Grammar (простое описание)

Шаблон:
`<VERB> <OBJECT> [FROM <SOURCE>] [TO <TARGET>] [WHEN <COND>] [WITH <POLICY>]`

Примеры:
- `Fetch items FROM RSS TO Inbox WHEN new WITH dedup`
- `Normalize offers FROM APIs TO CompareTable WITH schema_v1`
- `Send alert TO Telegram WHEN risk_high WITH rate_limit`

## 5) Как это используется в IFOS

1) **Поиск**: пользователь вводит “хочу дайджест новостей” → система ищет capabilities L2.
2) **Сравнение**: продукты сравниваются по покрытию capabilities.
3) **Сборка решения**: L2 → подбираются L1/L0 блоки и коннекторы.
4) **Документация**: витрина показывает человеческие названия и синонимы.

## 6) Дыры/что ещё нужно

- Нужно расширить словарь доменов (финансы, медицина, юриспруденция и т.д.).
- Нужны мультиязычные labels (ru/de/en).
- Нужны веса/приоритеты и “опыт” применения (кто, где, сколько раз запускал).
- Нужна связка с Knowledge Graph UI (просмотр связей).

## 7) Зависимости

### Hard deps
- 35201–35600 `knowledge_graph_semantic_os` (семантика/граф)
- 32001–32400 `knowledge_registry_os` (реестр)
- 33601–34000 `search_ranking_vitrines_os` (поиск/ранжирование)

### Optional deps
- 54001–54400 `knowledge_graph_ui_navigation_os` (UI графа)
- 47201–47600 `compare_evaluation_truthful_os` (оценка сравнения)
- 41601–42000 `localization_i18n_os` (локализация)
