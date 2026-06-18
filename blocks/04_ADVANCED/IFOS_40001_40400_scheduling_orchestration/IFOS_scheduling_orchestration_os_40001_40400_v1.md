# IFOS 40001–40400 — Scheduling & Orchestration OS (v1)
Цель: чтобы IFOS мог выполнять тысячи “макросов” (runs) над функциями:
- очереди и воркеры
- DAG (зависимости задач)
- retries и идемпотентность
- приоритеты и fairness (справедливость)
- backpressure и circuit breakers
- offline/edge runs (когда интернет нестабилен)
- “one‑click execution at scale” (нажал кнопку — всё побежало)

Порядок: простое → среднее → сложное.

---

## 40001–40040 — Queue: очереди как “кровеносная система”
**Queue** описывает:
- тип: fifo / priority / delayed
- лимиты: max_inflight, max_rate
- привязку к tenant/SLA
- классы ресурсов (CPU/GPU/LLM)
- правила DLQ (dead-letter queue)

Queue — это место, где runs ждут исполнения.

---

## 40041–40100 — Job & Task: атомы выполнения
**Job** — единица работы (например, “запусти workflow X с input Y”).  
**Task** — шаг внутри job или DAG (например, “download → normalize → dedup”).

Обязательные поля:
- idempotency_key (чтобы повтор не дублировал эффект)
- inputs/outputs refs
- security context (tenant, role)
- cost hints (для квот и планировщика)

---

## 40101–40160 — Schedules/Triggers: запуск по времени и событиям
**ScheduleTrigger**:
- cron / interval
- “on event” (webhook, new file, new email)
- “manual button” (UI‑клик)
- “conditional” (если метрика > порога)

Triggers должны писать audit и metering.

---

## 40161–40210 — DAG Orchestration: зависимости и параллельность
**DAG** описывает:
- вершины (tasks)
- зависимости (edges)
- параллельные ветки
- условия ветвления (if/else)
- “fan‑out / fan‑in” (раскидать на 100 задач и собрать)

Это превращает набор функций в “мини‑конвейер”.

---

## 40211–40260 — Retry Policy + Idempotency: “не страшно падать”
**RetryPolicy**:
- max_attempts
- backoff (exponential + jitter)
- retryable errors (timeouts, 429)
- non-retryable (validation ошибок)

**Idempotency**:
- ключ строится из (tenant, workflow, input_hash, intent)
- повторная задача возвращает прошлый результат

Это защищает от “двойного списания” и “двойного импорта”.

---

## 40261–40320 — Priorities & Fairness: кому дать CPU первым
**PriorityPolicy**:
- веса по SLA (enterprise > pro > free)
- веса по tenant (чтобы один не съел всё)
- приоритет по типу задач (security > billing > analytics)
- aging (чтобы низкий приоритет не голодал)

Fairness нужен, иначе “макросы богатых” блокируют остальных.

---

## 40321–40370 — Backpressure & Circuit Breakers: защита от каскадных аварий
**BackpressurePolicy**:
- если downstream перегружен → замедлить upstream
- ограничить fan-out
- отключить “дорогие” функции при бюджете

**Circuit breaker**:
- если внешний API падает → STOP на N минут
- перевод в degrade mode (кэш/заглушка/упрощённый путь)

Это делает систему устойчивой при хаосе интеграций.

---

## 40371–40390 — Offline/Edge Runs: когда сеть слабая
OfflineRuns:
- локальный журнал задач на устройстве (mobile/edge)
- синхронизация при появлении сети
- конфликт‑политика (см. Federation block)
- политика безопасности (что можно выполнять офлайн)

Пример: “домашний сервер на Android/miniPC” выполняет макросы без облака.

---

## 40391–40400 — One‑Click Macro Execution at Scale: UX слой оркестрации
“One click” — это:
- кнопка в витрине
- подбор готового blueprint
- предпросмотр (что будет сделано)
- оценка стоимости/квоты/времени
- запуск в DAG + очередь
- понятный прогресс и отчёт

---

## Итог
Этот блок делает IFOS “движком исполнения”:
- управляемые очереди
- воспроизводимые DAG
- безопасные повторы
- справедливые приоритеты
- защита от перегрузок
- офлайн‑выполнение
- UX‑кнопка “запусти всё”

---

## Что дальше
Следующий блок:
**40401–40800 — Data Lineage & Provenance OS** (происхождение данных, трансформации, “почему это так”, граф зависимостей, доказуемость).  
Скажете “Продолжение” — сделаю.
