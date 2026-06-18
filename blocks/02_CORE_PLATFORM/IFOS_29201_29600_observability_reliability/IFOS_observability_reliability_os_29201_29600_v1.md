# IFOS 29201–29600 — Observability & Reliability OS (v1)
Цель: чтобы пользователь **всегда понимал “почему не работает”**, а система могла:
- измерять качество (метрики),
- объяснять поведение (логи/трейсы),
- проверять здоровье (health checks),
- держать уровень сервиса (SLO),
- предупреждать (alerts),
- оформлять инциденты (incidents),
- делать автодиагностику (autodiag),
- предлагать/выполнять авто‑починку (autofix).

Порядок: от простого к среднему и далее к сложному.

---

## 29201–29240 — Metrics: измеримые факты (самый простой сигнал)
Метрика — число во времени:
- success_rate, failure_rate
- latency_p50/p95
- runs_per_day
- cost_per_run (если есть)
- dedupe_ratio (для новостей)
- install_friction (время установки)

Правило: без метрик нет прогресса, есть только мнения.

---

## 29241–29290 — Logs: события и причины (человекочитаемо)
Логи — структурированные события:
- ts, level, message
- context (job_id, package_id, user_id)
- error codes (E_CONN_TIMEOUT, E_SECRET_MISSING)
- remediation_hint (что делать)

Важно: логи не должны быть “простынёй”.
Они должны быть **по шаблону** и “лечебными”.

---

## 29291–29340 — Traces: трассировка цепочки действий (где именно сломалось)
TraceSpan описывает шаги пайплайна:
- fetch → parse → dedupe → summarize → send
Содержит:
- duration
- input/output sizes
- error location
- link to logs

Трейсы дают ответ: “какой компонент виноват” (connector? parser? policy?).

---

## 29341–29390 — Health Checks: быстрые проверки жизнеспособности
HealthCheck бывает:
- connector check (доступен ли API)
- secret check (есть ли secret_ref)
- quota check (не закончился ли лимит)
- storage/index check
- end-to-end smoke test (“собери 1 новость и отправь себе”)

Результат health check поднимается в UI Card (status ok/degraded/broken).

---

## 29391–29430 — SLO: обещания уровня сервиса (уже средний уровень)
SLO (Service Level Objective) для задач:
- 99% запусков успешны за 7 дней
- p95 latency < 30s
- “дайджест” должен приходить до 08:30

SLO переводит “качество” в числа и правила.

---

## 29431–29480 — Alerts: автоматические предупреждения
AlertRule:
- условие (failure_rate > 10% за 1 час)
- каналы (Telegram/email/UI)
- severity (info/warn/critical)
- runbook link (что делать)

Система не ждёт, пока пользователь заметит проблему.

---

## 29481–29520 — Incidents: оформление проблемы как объекта управления
Incident:
- что сломалось (service/job/package)
- когда началось
- влияние (сколько пользователей/витрин)
- статус (open/mitigating/resolved)
- RCA (root cause analysis) по итогам

Инциденты — это “память” и обучение системы.

---

## 29521–29560 — Autodiagnostics: “почему не работает” в 1 экран
DiagnosticFinding:
- symptom (Telegram не отправляет)
- probable causes (нет secret_ref, quota, network)
- evidence (logs, traces, health check)
- confidence score
- suggested actions

Это “инженерный врач”.

---

## 29561–29600 — Autofix: план авто‑починки (с контролем политики)
AutoFixPlan:
- steps (создать secret_ref, пересоздать индекс, обновить пакет)
- risk level
- requires approval? (Governance OS)
- rollback plan
- post-check (health check после починки)

Ключ: авто‑починка не должна ломать безопасность.
Она должна уважать политики и роли.

---

## Мини‑архитектура Observability & Reliability OS
1) Metrics → 2) Logs → 3) Traces → 4) Health checks  
5) SLO → 6) Alerts → 7) Incidents → 8) Autodiag → 9) Autofix

---

## Что дальше логически
Следующий блок (если скажете “Продолжение”):
**29601–30000 — Data Quality & Knowledge OS**: дедуп, нормализация, онтологии тегов, источники доверия, “почему этот результат”, versioned datasets.
