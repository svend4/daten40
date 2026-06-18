# IFOS — Connector↔Capability Mapping & Coverage Matrix (What supports what, with evidence) (Блок 67201–67600)

Версия: v1 · Пакет: `IFOS_67201_67600_connector_capability_mapping_coverage_matrix_os_pack.zip` · Дата: 2026-01-03

## 0) Зачем нужен этот блок

Пока нет таблицы «кто что умеет», интернет остаётся хаосом:
есть тысячи коннекторов/плагинов/SDK, но **не ясно**, какие функции они покрывают.

Этот блок создаёт **матрицу покрытия**:
- `connector` → какие `capabilities` поддерживает,
- с доказательствами (OpenAPI/README/скриншоты/тест),
- с ограничениями (тариф, лимиты, ключи, регионы),
- и со статусом (OK/PARTIAL/BROKEN/UNKNOWN).

Именно эта матрица делает возможными:
- честное сравнение (порталы сравнения),
- one‑click bundles,
- автосборку решений из запроса.

## 1) Что делает (функции)

1) **Mapping layer**: связывает registry items (коннекторы/плагины) с capabilities.
2) **Coverage scoring**: считает покрытие по уровням L0/L1/L2.
3) **Evidence model**:
   - типы доказательств
   - confidence score
   - freshness (актуальность)
4) **Compatibility flags**:
   - auth methods (api_key/oauth)
   - regions
   - rate limits
   - required plans (free/pro/enterprise)
5) **Negative mapping**: что НЕ поддерживается и почему.
6) **Drift detection**: сигнал, когда API изменилось и mapping устарел.
7) **Export**: CSV/JSON для витрин и планировщика.

## 2) Что НЕ делает

- Не пишет сам коннектор (это connectors factory sdk).
- Не выполняет интеграции в проде (это runner).
- Не гарантирует вечную актуальность: требует мониторинга.

## 3) Структуры данных

### 3.1 ConnectorCapabilityMap
- `connector_id`
- `capability_id`
- `coverage` (OK/PARTIAL/BLOCKED/UNKNOWN)
- `confidence` (0..1)
- `evidence[]`
- `constraints` (keys, plan, regions)
- `limitations` (rate limit, quotas)
- `last_verified_at`

### 3.2 CoverageMatrix
- агрегаты по доменам/пакетам
- % покрытия L0/L1/L2
- heatmap/табличный экспорт

## 4) Процесс построения (по шагам)

### 4.1 Простое (ручной seed)
1) выбрать топ‑100 коннекторов (Make, n8n, Zapier, WP, GitHub)
2) вручную сопоставить 5–20 ключевых capabilities
3) указать evidence из документации

### 4.2 Среднее (semi‑auto)
1) парсить OpenAPI/README → кандидаты capabilities
2) человек подтверждает
3) прогон test harness (smoke) → повышает confidence

### 4.3 Сложное (auto + drift)
1) nightly проверка endpoints (read‑only)
2) если mismatch → пометка mapping как stale
3) авто‑создание issue/тикета в curation queue

## 5) Метрики качества

- `coverage_ratio` (покрытие)
- `evidence_strength` (сила доказательств)
- `freshness_days`
- `breakage_rate`
- `time_to_fix`

## 6) Дыры/что ещё нужно

- Нужны стандартизированные тесты для ключевых capabilities (benchmark catalog).
- Нужны источники truth для тарифов/лимитов (часто меняются).
- Нужна UI‑витрина матрицы (heatmap) + фильтры.

## 7) Зависимости

### Hard deps
- 66401–66800 `capability_ontology_function_thesaurus`
- 32001–32400 `knowledge_registry_os`
- 43201–43600 `data_contracts_schema_registry_os` (схемы)
- 57601–58000 `standards_interop_os` (профили)

### Optional deps
- 62401–62800 `connector_test_harness_ci_cd_os` (smoke tests)
- 45601–46000 `marketplace_curation_quality_os`
- 59201–59600 `interop_benchmarks_rankings_os`
