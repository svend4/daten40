# IFOS 40801–41200 — Experimentation & Evaluation OS (v1)
Цель: чтобы IFOS **улучшался без хаоса**, а качество было измеримым.
Блок отвечает за:
- A/B и multivariate тесты витрин/ранжирования/blueprints
- метрики и события качества (quality, safety, conversion, latency, cost)
- evaluation pipeline (автоматическая оценка и регрессии)
- benchmark suites (наборы тестов по доменам)
- human-in-the-loop (ручная оценка сложных кейсов)
- feedback loops (обратная связь и обучение продукта)
- release gating (выпуск только при прохождении порогов)

Порядок: простое → среднее → сложное.

---

## 40801–40840 — Experiment: эксперимент как объект ОС
**Experiment** описывает:
- что тестируем (vitrine/search/ranking/workflow/bundle)
- цель (например “увеличить успешные install-run”, “снизить cost/run”)
- варианты A/B (Variant)
- аудитория (targeting) и правила распределения
- метрики успеха (primary/secondary/guardrails)
- срок действия и владелец

Принцип: эксперимент — это “контракт”, а не “поигрались”.

---

## 40841–40910 — Variant & Assignment: варианты и распределение трафика
**Variant**:
- ссылка на артефакт (например: ranking policy v2, витрина v3)
- параметры (weights, flags, model choice)
- версия и changelog

**Assignment**:
- кто попал в какой вариант (tenant/user/session)
- deterministic hashing (стабильность)
- holdout группы
- исключения (VIP, internal)

Важное: assignment должен быть **детерминированным**, иначе метрики ломаются.

---

## 40911–40970 — Metric & Event: как считать “победу”
**MetricDefinition**:
- формула (например: success_rate = success_runs / all_runs)
- окно (minute/day/week)
- сегменты (tenant tier, locale, device)
- guardrails (latency_p95, error_rate, safety flags)

**EvaluationEvent**:
- любые события (run_succeeded, install_failed, user_feedback)
- привязка к variant + tenant + run_id
- хранение сырых событий и агрегаций

---

## 40971–41020 — Scorecards: отчёты качества для decision-making
**Scorecard** собирает:
- метрики по каждому варианту
- доверительные интервалы/стат значимость (если используете)
- cost impact (€/1000 runs)
- safety impact (flags)
- рекомендации (“ship”, “iterate”, “rollback”)

Scorecard — это “страница решения”, а не сырая таблица.

---

## 41021–41070 — Benchmark Suites: регрессии и доменные наборы
**BenchmarkSuite**:
- тестовые кейсы (inputs)
- ожидаемые свойства (constraints), не всегда “точный ответ”
- разные домены (например: WordPress installs, Make workflows, OCR docs)
- baseline и сравнение

Benchmark запускается перед релизом, чтобы не ломать качество.

---

## 41071–41120 — Human-in-the-loop: где нужен человек
**HumanReview**:
- очередь кейсов на проверку (сложные/опасные/спорные)
- инструкции оценщика (rubric)
- шкалы (1–5), флаги (unsafe, hallucination, missing_source)
- inter-rater agreement (согласованность)
- стоимость времени (минуты) → связь с Pricing block

HITL нужен для safety и смысловых задач, где автоматикой не проверить.

---

## 41121–41160 — Feedback Loops: обратная связь как топливо
**FeedbackItem**:
- thumbs up/down, комментарий
- причины (неверно, не полно, дорого, сложно)
- привязка к run/variant
- triage: bug / content / product / data

Фидбек должен попадать в:
- backlog задач
- datasets для обучения (если разрешено)
- правила ранжирования/выбор blueprints

---

## 41161–41200 — Release Gating: “выпускаем только если проходит пороги”
**ReleaseGate**:
- условия релиза (например: error_rate < 1%, latency_p95 < 1s, safety_flags <= baseline)
- источники доказательств (scorecard, benchmark, HITL)
- действия: allow / block / rollback / require_approval

Это “система тормозов”, чтобы продукт не деградировал при росте.

---

## Итог
Этот блок делает IFOS “самоулучшаемой ОС”:
- улучшения измеримы
- регрессии ловятся автоматически
- риск‑кейсы уходят на человека
- обратная связь превращается в работу
- релизы защищены порогами

---

## Что дальше
Следующий блок:
**41201–41600 — Data Privacy & Compliance OS** (GDPR, PII/PHI tagging, consent, anonymization, DSAR workflows, audit evidence packs).  
Скажете “Продолжение” — сделаю.
