# IFOS Block 70001–70400: Performance, Capacity & Load Testing
**Slug:** `performance_capacity_load_testing`  
**Category:** Observability & Reliability  
**Priority:** P1  
**Status:** MVP Spec + Seeds (v1)

## 1) Идея блока (зачем он нужен)
Этот блок превращает “быстро/медленно” в **управляемую дисциплину**:

- **Performance**: скорость отклика (latency), пропускная способность (throughput), ошибки.
- **Capacity**: сколько трафика/задач система выдержит при заданных SLO.
- **Load/Stress/Soak/Spike**: разные типы нагрузочных испытаний.
- **Bottleneck discovery**: где узкое место — CPU, DB, сеть, очереди, внешние API.
- **Release safety**: тесты как “ворота” перед релизом (CI/CD + feature flags).

В IFOS это критично, потому что:
- runtime запускает workflow/macro jobs,
- коннекторы ходят во внешние сервисы,
- marketplace и витрины должны быть быстрыми,
- поиск/ранжирование и RAG — часто самые тяжёлые компоненты.

---

## 2) Что блок делает (основные функции)
### 2.1. Каталог тестов и профилей нагрузки (Load Test Catalog)
- тип теста: **baseline / load / stress / spike / soak**
- профиль: виртуальные пользователи, RPS, длительность, ramp-up/down
- сценарии: API, UI-операции, “потоки” (import → normalize → index → search)

### 2.2. Модель мощности (Capacity Model)
- цель: “при SLO X система держит Y RPS при Z стоимости”
- хранение результатов прогонов, трендов и предельных значений
- привязка к “домены IFOS”: runtime, connectors, search, marketplace, KB/RAG

### 2.3. Генерация нагрузки и воспроизведение трафика
- синтетический трафик (скрипты)
- (опционально) **traffic replay** с обезличиванием
- прогон в разных средах: dev/staging/prod-safe window

### 2.4. Интеграция с наблюдаемостью и алертами
- обязательное привязывание теста к метрикам/дашбордам
- авто-сбор артефактов: графики, логи, трейсы, результаты

### 2.5. Автоматическая оценка “PASS/FAIL”
- пороги: p95/p99 latency, error rate, saturation, queue depth
- сравнение с baseline (регрессии после релизов)
- генерация action items (тикеты) при провале

---

## 3) Минимальные сущности данных
### 3.1. LoadTestTemplate
- `id`, `title`, `type` (baseline|load|stress|spike|soak)
- `targets` (services/slugs/endpoints)
- `profile` (RPS/VU, duration, ramp)
- `scenarios` (flows), `datasets` (optional)
- `success_criteria` (thresholds), `slo_refs`
- `environment_policy` (where allowed), `safety_guards`

### 3.2. LoadTestRun
- `id`, `template_id`, `env`, `started_at`, `ended_at`
- `release_ref` (commit/version/feature_flag state)
- `result_summary` (pass/fail), `metrics_snapshot`
- `artifacts` (links), `notes`

### 3.3. CapacitySnapshot
- `domain`, `max_rps_at_slo`, `cost_estimate`, `constraints`
- `date`, `trend`, `confidence`

### 3.4. RegressionFinding
- `run_id`, `baseline_run_id`, `delta`, `suspected_components`
- `ticket_ref`, `status`

---

## 4) Связи с другими блоками (стыковки)
- **Observability & Reliability**: метрики/алерты/дашборды — обязательны
- **Scheduling/Orchestration**: планирование прогонов (ночью/по релизу)
- **Runtime/Workflow Runner**: нагрузка на job-исполнение (очереди/воркеры)
- **Connectors/Test Harness**: имитация внешних API и деградаций
- **Experimentation/Evaluation**: сравнение вариантов конфигурации
- **Feature Flags**: безопасные переключатели при релизах
- **Case/Ticketing**: автосоздание задач при регрессии

---

## 5) API (минимальный набор)
- `POST /perf/tests/templates`
- `GET /perf/tests/templates?type=&target=`
- `POST /perf/tests/runs` (create + schedule)
- `POST /perf/tests/runs/{id}/start`
- `POST /perf/tests/runs/{id}/finish` (pass/fail + summary)
- `GET /perf/capacity/snapshots`
- `GET /perf/regressions?since=`

---

## 6) UI
- **Load Test Catalog**: фильтры, теги, “быстрый запуск”
- **Run Result View**: графики, p95/p99, ошибки, “что изменилось”
- **Capacity Dashboard**: мощность по доменам, тренды, лимиты
- **Release Gate**: статус тестов как “ок”/“красный”

---

## 7) MVP vs позже
### MVP (в этом блоке)
- хранение шаблонов тестов + запуск + фиксация результатов
- привязка к наблюдаемости (ссылки на дашборды/метрики)
- простая проверка порогов + создание тикетов

### Later
- traffic replay с приватностью (policy engine + anonymization)
- автопоиск узких мест (корреляции по метрикам)
- авто-тюнинг профилей (подбор нагрузки до границы SLO)
- публичные бенчмарки пакетов/коннекторов (“быстрее/дешевле/стабильнее”)

---

## 8) Безопасность и ограничения
- запрет нагрузочных тестов в prod без окна/разрешения
- лимиты на внешние API (чтобы не попасть в бан/лимиты)
- обязательный rollback plan и safety guards
- аудит запусков и результатов (enterprise governance)
