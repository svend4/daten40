# IFOS — Intent→Solution Planner & Compiler (Query → Capabilities → Bundle/Blueprint) (Блок 66801–67200)

Версия: v1 · Пакет: `IFOS_66801_67200_intent_to_solution_planner_compiler_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

У тебя была цель: **не изобретать велосипед**, а брать готовые решения и **собирать** их
в понятные «макросы» и «кнопки».

Но для этого нужен механизм, который делает переход:
**человеческий запрос → набор функций (capabilities) → план → готовый пакет/шаблон**.

Этот блок вводит **Intent→Solution Planner**:
- понимает формулировку пользователя,
- превращает её в требования/ограничения,
- подбирает подходящие capabilities и компоненты,
- собирает минимальный рабочий Bundle (P0/P1) и Blueprint Pack.

## 1) Что делает (функции)

1) **Intent Parsing**: выделение VERB/OBJECT/SOURCE/TARGET/COND/POLICY из текста.
2) **Constraint extraction**: бюджет/платформа/приватность/офлайн/ключи/API.
3) **Capability retrieval**: поиск кандидатов в IFOS Lexicon + Registry.
4) **Plan synthesis**:
   - строит граф функций L2→L1→L0,
   - добавляет required dependencies,
   - выбирает компоненты по совместимости.
5) **Bundle compilation**: выдаёт Bundle Manifest (как one‑click набор).
6) **Blueprint compilation**: создаёт Blueprint Pack (для IFOS Runner / Make/n8n).
7) **Explainability**: объясняет выбор (почему это, чем заменить, что отсутствует).
8) **Fallback modes**:
   - если нет коннектора → предлагает workaround,
   - если нет ключей → предлагает sandbox/test keys профиль.

## 2) Что НЕ делает

- Не запускает исполнение (это делает workflow runner/macro engine).
- Не гарантирует идеальный план без данных: есть режимы уточнения.
- Не «выдумывает» несуществующие коннекторы: если нет — помечает gap.

## 3) Вход/Выход

### Вход: `IntentQuery`
- `text` (запрос)
- `domain_hint` (news/office/compare/...)
- `constraints` (privacy, budget, platform, keys)
- `context` (что уже подключено, какие аккаунты)

### Выход: `SolutionPlan`
- `capability_graph` (узлы и связи)
- `selected_components` (registry items)
- `bundle_manifest` (one‑click)
- `blueprint_pack` (workflow steps)
- `gaps` (что не закрыто)
- `explanations` (почему так)

## 4) Алгоритм (простое → среднее → сложное)

### 4.1 Простое (P1): rule‑based
1) распарсить по грамматике (VERB/OBJECT/...)
2) найти capability candidates по тезаурусу
3) собрать L2→L1→L0 по relations `part_of`/`requires`
4) выбрать компоненты по tag‑matching + compatibility OK
5) скомпилировать bundle + blueprint

### 4.2 Среднее (P2): hybrid scoring
- BM25/semantic search по registry + signals
- оптимизация по стоимости/риску/ключам

### 4.3 Сложное (P3): constraint solving
- SAT/ILP подбор компонентов
- активное обучение по фидбеку

## 5) Политики и риски

Риски:
- неверное сопоставление терминов (решение: evidence + confidence)
- скрытые требования по ключам/доступам (решение: connector cred requirements)
- комплаенс (GDPR/PII) (решение: policy engine)

Политики:
- `policy:privacy.no_pii_export`
- `policy:rate_limit.standard`
- `policy:retry.backoff`

## 6) Дыры/что ещё не закрыто

- Нужен UI диалог уточнений (когда constraints неполные).
- Нужна библиотека эталонных планов (golden plans) для обучения.
- Нужна интеграция с Marketplace Quality (чтобы избегать плохих пакетов).
- Нужны доменные пакеты intents (news/compare/office) в больших объёмах.

## 7) Зависимости

### Hard deps
- 66401–66800 `capability_ontology_function_thesaurus` (лексикон)
- 32001–32400 `knowledge_registry_os` (реестр)
- 33601–34000 `search_ranking_vitrines_os` (поиск/ранжирование)
- 48801–49200 `one_click_bundles_templates_os` (bundle формат)
- 44801–45200 `workflow_runner_macro_engine_os` (исполнение позже)

### Optional deps
- 62001–62400 `sandbox_test_keys_dev_env_os` (песочница)
- 55201–55600 `compliance_policy_engine_os` (политики)
- 47201–47600 `compare_evaluation_truthful_os` (оценка результатов)
