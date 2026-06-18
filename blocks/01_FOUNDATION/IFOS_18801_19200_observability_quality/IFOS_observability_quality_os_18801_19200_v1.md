# IFOS 18801–19200 — Observability & Quality‑OS: метрики, SLI/SLO, тест‑харнес, смоук‑тесты, синтетика, качество‑скоринг, релиз‑гейты, инциденты, “качество как продукт” (v1)

Ваша идея “миллионы модулей — собирать кластеры” ломается в одном месте: **качество**.  
Пользователь не будет “учиться 1000 сценариев”, если:
- половина не запускается,
- непонятно “что сломалось”,
- нет минимальных гарантий,
- нельзя сравнить стабильность.

Observability & Quality‑OS делает **интернет‑операционку измеримой**:
- всё имеет метрики,
- у всего есть SLO,
- у всего есть smoke‑тест,
- качество считается автоматически,
- релизы режутся гейтами,
- инциденты не теряются.

Ниже — от простого к сложному.

---

## 18801–18850 — Метрики как “валюта качества” (простое)

### 18801) Минимальный набор метрик для любого ассета
**Install**
- install_attempts, install_success_rate
- time_to_first_success (TTFS)

**Run**
- run_pass_rate
- p95_latency
- error_rate по кодам (TOKEN_INVALID, TIMEOUT, RATE_LIMIT)

**Stability**
- crash_count / retry_count
- mean_time_between_failures (MTBF) — если есть

**User**
- rating (звёзды) + evidence_score (доказательность)
- doc_coverage (есть ли docs/FAQ/cases/tutorials)

### 18820) Метрика = объект (не просто числа)
Метрика должна знать:
- что измеряем (definition)
- где собираем (source)
- как агрегируем (window)
- норму (target)
- что считать деградацией (thresholds)

---

## 18851–18910 — SLI/SLO (среднее): “гарантии” вместо надежды

### 18851) SLI: что именно измеряем
Примеры SLI:
- run_pass_rate over 24h
- install_success_rate over 30d
- p95_latency per run

### 18870) SLO: какая цель и что считается нарушением
Пример SLO:
- Run pass rate ≥ 95% (24h window)
- Install success rate ≥ 98% (30d window)
- p95_latency ≤ 8s

SLO нужен не ради “корпоративности”, а ради:
- сравнения модулей,
- автоматического рейтинга,
- релиз‑гейтов.

---

## 18911–18980 — Test Harness + Smoke tests (среднее+): “одна кнопка проверить”

### 18911) Тест‑харнес (единый двигатель тестов)
Единый формат теста для:
- Make scenario
- n8n workflow
- WP plugin config
- native yaml

**TestCase** содержит:
- setup (создать тестовые данные)
- act (запуск)
- assert (проверка результата)
- cleanup (не оставить мусор)

### 18940) Smoke‑Test Plan (обязательный минимум)
Smoke тест — самый дешёвый тест, который:
- проверяет токены/доступы
- делает 1–2 запроса к источнику
- отправляет тест‑сообщение (если нужно)
- не делает разрушительных действий

**Принцип:** любой ассет без smoke‑теста = “неpublishable” для marketplace.

---

## 18981–19050 — Synthetic Monitoring (сложнее): мониторинг без пользователей

### 18981) Синтетика = “робот‑пользователь”
Синтетический чек:
- каждые N минут запускает короткий сценарий
- проверяет ключевую цепочку (fetch → transform → deliver)
- пишет результат в evidence run store

Это позволяет:
- заранее ловить падения API
- видеть деградации до жалоб
- строить стабильный рейтинг

### 19020) Canary installs
Новые версии:
- ставим на 1–5% окружений (или sandbox)
- сравниваем SLI с предыдущей версией
- только потом расширяем rollout

---

## 19051–19120 — Quality Score (сложно): “оценка модуля” без ручной магии

### 19051) Quality Score = взвешенная формула
Пример факторов:
- Stability: run_pass_rate, MTBF
- Performance: p95_latency
- Installability: install_success_rate, TTFS
- Docs: doc_coverage (card/page/faq/cases/tutorials)
- Trust: signatures, SBOM, license_ok, policy_ok
- Support: time_to_fix, known_issues_count

Скоринг должен быть:
- объяснимым (почему 0.62, а не 0.90)
- воспроизводимым
- независимым от “маркетинга”

### 19090) Evidence score vs rating
- rating = мнение людей
- evidence_score = факты (runs, SLO, tests)

Они должны быть раздельными, иначе накрутка уничтожит систему.

---

## 19121–19170 — Release Gates (очень сложно): “не сломай рынок”

### 19121) Gate Decision — автоматическое решение
Перед публикацией/обновлением:
- smoke‑тест PASS
- SLO не нарушены
- синтетика PASS N раз подряд
- SBOM + подпись присутствуют
- no critical incident open

Если не проходит — релиз блокируется, и даётся план исправления.

### 19150) Виды гейтов
- publish gate (первый выпуск)
- update gate (обновление)
- hotfix gate (экстренное исправление, но всё равно с минимумом)

---

## 19171–19200 — Incident Management (самое сложное): ошибки как продукт

### 19171) Инцидент = объект + таймлайн
Инцидент должен содержать:
- что сломалось (scope)
- кто затронут (tenants/segments)
- когда началось/закончилось
- root cause (после расследования)
- actions taken
- prevention actions
- связи с troubleshooting cases и релизом

### 19190) Postmortem → Knowledge OS
После инцидента:
- автоматически создаём troubleshooting case
- обновляем FAQ
- обновляем docs
- добавляем регрессионный тест в harness

Это превращает хаос в развитие.

---

## Приложения (в этом пакете)
- JSON Schemas: metric definition, SLI, SLO, test case, smoke test plan, synthetic check, quality score, release gate decision, incident report, dashboard summary
- Specs: observability, quality scoring, test harness, release gates, incident management
- OpenAPI: Observability & Quality API (MVP)
- Examples: комплект на “News Digest Cluster”
- Python skeletons: collector, SLO evaluator, smoke runner, synthetic monitor, quality scorer, gate engine, incident reporter, dashboard aggregator
