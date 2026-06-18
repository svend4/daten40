# IFOS Block 71201–71600: Chaos Engineering & Resilience Testing
**Slug:** `chaos_engineering_resilience_testing`  
**Category:** Delivery & Reliability  
**Priority:** P2  
**Status:** MVP + Later design (spec)

## 1) Идея и место в IFOS
Этот блок превращает “надёжность на словах” в **повторяемую практику**:
- мы **искусственно ломаем** систему в контролируемых условиях,
- измеряем реальную устойчивость,
- фиксируем уроки и улучшения,
- связываем всё с SLO/SLI (error budgets) и постмортемами.

Если блок 70801–71200 отвечает за *безопасный выпуск изменений*, то этот блок отвечает за *доказательство устойчивости* в боевых сценариях.

---

## 2) Базовые определения (простыми словами)
- **Chaos Engineering** — управляемые эксперименты, которые создают сбои и измеряют эффект.
- **Fault injection** — “вставка поломки”: задержки, ошибки, отключения зависимостей.
- **Blast radius** — насколько широко может разойтись ущерб (сегмент, регион, процент трафика).
- **Abort / Kill switch** — мгновенная остановка эксперимента.
- **GameDay** — тренировочный день: сценарии + роли + runbooks + метрики успеха.

---

## 3) MVP: минимальная система экспериментов (от простого к среднему)
### 3.1 Объекты данных (минимум)
**Experiment**
- `experiment_id`, `name`, `owner`, `service_scope`
- `hypothesis` (гипотеза: “если упадёт зависимость X, сервис Y должен…")
- `fault_type` (latency, errors, dependency_outage, cpu_spike, memory_leak, packet_loss)
- `target` (endpoint/service/queue/worker/region)
- `blast_radius` (tenant сегмент, % трафика, регион, время)
- `safety` (max duration, abort conditions, allowlist)
- `observability_links` (дашборды/лог/трейсы)
- `runbook_link` (что делать, если пошло плохо)
- `status` (draft/approved/scheduled/running/stopped/completed)

**ExperimentRun**
- `run_id`, `experiment_id`, `start_at`, `end_at`
- `result`: pass/fail/aborted
- `metrics_snapshot` (ключевые значения до/во время/после)
- `notes`, `followups` (тикеты улучшений)

### 3.2 Safety-first правила (обязательные в MVP)
- эксперименты запускаются **только** на allowlist окружений (dev/stage) или на выделенных “beta tenants”
- **kill switch** обязателен
- ограничение blast radius: например ≤ 1% трафика / ≤ 1 tenant tier / ≤ 1 region
- фиксированный max duration (например 10–20 минут)
- автоматический abort по guardrails (ошибки/latency/burn-rate)

### 3.3 Типы экспериментов MVP (стартовый набор)
1) Latency injection на внешний API (p95/p99)
2) Error injection 5xx на зависимость (simulate outage)
3) Queue backlog (замедлить consumer)
4) CPU spike на воркере (saturation)
5) Random pod restart (для k8s)
6) Rate limit / throttling сценарий

### 3.4 Что считаем успехом (минимальные критерии)
- система деградирует **предсказуемо** (graceful degradation)
- алерты срабатывают правильно (не поздно и не шумно)
- runbook приводит к восстановлению
- время восстановления (TTD/TTM/TTF/MTTR) в пределах ожиданий
- не сгорели SLO бюджеты (или сгорели контролируемо в пределах окна)

---

## 4) MVP API (контуры)
### 4.1 Управление экспериментами
- `POST /chaos/experiments` создать
- `POST /chaos/experiments/{id}/approve` (роль/аудит)
- `POST /chaos/experiments/{id}/schedule`
- `POST /chaos/experiments/{id}/start`
- `POST /chaos/runs/{run_id}/abort`
- `GET /chaos/experiments/{id}`
- `GET /chaos/runs/{run_id}`
- `GET /chaos/runs?service=...&from=...&to=...`

### 4.2 Интеграции (обязательные)
- Observability: метрики/логи/трейсы + ссылки на дашборды
- Incident / Ticketing: auto-ticket по fail/abort
- Policy Engine: запрещённые окна, требуемые approvals
- SLO: burn-rate gate во время эксперимента

---

## 5) Later: расширение до “промышленного” уровня
### 5.1 GameDays как продуктовый формат
- библиотека сценариев (каталог)
- расписание и приглашения (уведомления)
- роли: Incident Commander, SRE, Owner, Observer
- авто-формирование отчёта GameDay

### 5.2 Resilience Scorecards (оценка зрелости)
Скоринг по доменам:
- Coverage: сколько ключевых сервисов покрыто экспериментами
- Frequency: как часто проводятся (неделя/месяц)
- Recovery: средний MTTR, качество runbooks
- Observability: полнота сигналов (RED/USE)
- Change safety: как релизы влияют на устойчивость (связь с progressive delivery)

### 5.3 Авто-генерация улучшений
После fail:
- предложить конкретные улучшения (таймауты, ретраи, circuit breaker, bulkhead)
- связать с backlog и назначить владельца
- повторный эксперимент как “re-test” после фикса

### 5.4 Multi-region / DR drills
- региональные отключения (zone/region evacuation)
- проверка RPO/RTO
- failover runbooks и автоматизация переключений

---

## 6) Минимальный “one-click” сценарий (пример)
**Цель:** доказать, что падение внешнего OAuth провайдера не ломает логин.
1) Experiment: dependency_outage OAuth, blast radius: beta tenants
2) Run: 10 минут, abort если 5xx>threshold или burn-rate>limit
3) Ожидание: показываем “логин временно недоступен”, не падает весь UI
4) Результат: pass/fail, автоматически создаём тикет на улучшение (если fail)

---

## 7) Выходы (deliverables)
- Experiment schema + Run schema
- Каталог шаблонов экспериментов (seed)
- Каталог GameDay сценариев (seed)
- Scorecard rules (seed)
- Чек-листы safety/abort/runbook readiness

---
