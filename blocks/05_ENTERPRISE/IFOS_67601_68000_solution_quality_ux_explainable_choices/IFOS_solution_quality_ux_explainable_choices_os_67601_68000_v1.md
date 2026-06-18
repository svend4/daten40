# IFOS — Solution Quality UX (Explainable Choices, Alternatives, Trade-offs, Gaps) (Блок 67601–68000)

Версия: v1 · Пакет: `IFOS_67601_68000_solution_quality_ux_explainable_choices_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

Даже если Planner собрал решение, пользователю нужна **ясность**:
- почему выбрано именно это,
- что будет, если заменить компонент,
- где риски (ключи, лимиты, приватность),
- что *не* закрыто и как закрыть.

Этот блок превращает сборку решения из «магии» в **объяснимую инженерную покупку** —
как в Excel/Word: пользователь видит структуру, правила, макросы, альтернативы.

## 1) Что делает (функции)

1) **Explainability layer** для SolutionPlan:
   - evidence snippets
   - confidence и причины
2) **Alternatives**:
   - минимум 2–3 заменяемых варианта (connector A/B/C)
   - совместимость и цена
3) **Trade-off cards**:
   - privacy vs convenience
   - cost vs reliability
   - cloud vs offline
4) **Gap cards**:
   - чего не хватает (capability missing)
   - как закрыть: добавить компонент, получить ключ, сменить тариф
5) **Risk scoring**:
   - ключи/доступы
   - rate limits
   - vendor lock-in
   - compliance
6) **Decision log**:
   - сохраняет выбранные варианты и причины (audit)
7) **User confirmation hooks**:
   - когда нужно подтверждение действий (оплата, экспорт PII)

## 2) Что НЕ делает

- Не собирает план (это Planner).
- Не выполняет план (Runner).
- Не заменяет policy engine: использует его результаты.

## 3) UI-форматы (карточки)

### 3.1 Карточка решения (Solution Card)
- цель (human goal)
- краткое описание
- шаги pipeline
- стоимость/риски

### 3.2 Карточка выбора компонента (Choice Card)
- выбран компонент
- почему выбран (3 причины)
- альтернативы (2–5) + сравнение

### 3.3 Карточка риска (Risk Card)
- риск
- вероятность/влияние
- меры снижения

### 3.4 Карточка дыры (Gap Card)
- чего не хватает
- варианты закрытия
- цена/время/сложность

## 4) Данные и схемы

- `DecisionExplanation`
- `AlternativeOption`
- `Tradeoff`
- `Gap`
- `Risk`
- `DecisionLogEntry`

## 5) Алгоритм генерации объяснений

1) взять SolutionPlan
2) для каждого выбранного компонента:
   - собрать evidence
   - собрать constraints
   - найти alternatives из Coverage Matrix
3) сформировать trade-offs
4) сформировать gaps (если coverage missing)
5) рассчитать risk score
6) собрать UI-вывод в набор карточек

## 6) Дыры/что ещё нужно

- Нужен единый стиль карточек (UI OS office style / app shell).
- Нужна модель «стоимости» (цена компонентов/тарифов).
- Нужен benchmark/catalog для «качества» альтернатив.

## 7) Зависимости

### Hard deps
- 66801–67200 `intent_to_solution_planner_compiler`
- 67201–67600 `connector_capability_mapping_coverage_matrix`
- 34401–34800 `security_trust_os`
- 41201–41600 `data_privacy_compliance_os`
- 45601–46000 `marketplace_curation_quality_os`

### Optional deps
- 50001–50400 `ui_os_office_style`
- 38801–39200 `app_shell_navigation_os`
- 59201–59600 `interop_benchmarks_rankings_os`
