# IFOS 54801–55200 — Collaboration & Change Management OS (совместная работа и управление изменениями) (v1)
Цель: превратить IFOS в “производственную организацию”, где изменения:
- **обсуждаются** (RFC/комментарии)
- **проверяются** (review + тесты)
- **согласуются** (approvals по политике)
- **выпускаются** (releases / release trains)
- **катятся безопасно** (canary/rollout)
- **разбираются при сбоях** (incident + postmortem)
…и всё это связано с Vault (артефакты), Graph (зависимости), Runtime (запуски).

Порядок: простое → среднее → сложное.

---

## 54801–54830 — Минимум для одного человека (Personal Mode)
Объекты:
- Task (задача)
- Comment (заметка/обсуждение)
- ChangeSet (набор изменений: bundle/doc/policy)

Workflow (простая доска):
1) idea → 2) doing → 3) review → 4) done

Фичи:
- чек‑лист внутри задачи
- ссылки на артефакты (Vault)
- авто‑создание “impact summary” (из Graph) при изменении bundle

---

## 54831–54870 — Team Mode: задачи, роли, ответственность
Добавляем:
- assignee (ответственный)
- reviewers (2‑глазный контроль)
- labels/tags (ops/security/data)
- due dates + reminders
- “Definition of Done” (шаблон критериев)

Внутри проектов появляется:
- backlog
- sprint/iteration (опционально)
- board views (как в Trello/Jira, но проще)

---

## 54871–54920 — RFC: “пишем изменение как документ”
RFC нужен, когда:
- меняется API коннектора
- меняется схема данных
- появляется новый bundle pack
- меняются политики безопасности

RFC Template (коротко):
- Problem
- Goals / Non‑Goals
- Proposed solution
- Alternatives
- Risks + Impact (автоиз Graph)
- Rollout plan
- Rollback plan
- Test plan

RFC — это Artifact в Vault + Node в Graph.

---

## 54921–54970 — Approvals: политики согласования (простое → сложное)
Политики:
- low risk: 1 reviewer
- medium: 2 reviewers + automated tests
- high: security officer + data owner + legal (если PII)

Триггеры risk:
- затронуты PII данные
- затронуты payments
- изменён connector auth
- изменение влияет на >N процессов (impact depth)

Approvals могут быть:
- manual
- automated (если тесты зелёные и риск низкий)

---

## 54971–55010 — Review & Commenting: как обсуждать изменения
Инструменты:
- inline comments (как в Google Docs)
- diff comments (для bundles/manifests)
- “suggestion mode” (предложить правку)
- threads + resolve/unresolve
- “change summary” автоматически (AI + строго с ссылками)

Важно:
- в Review показывать **impact view** и **dependency tree** рядом.

---

## 55011–55060 — Release Trains: выпуск пакетами
Release object:
- release_id
- list of changesets
- snapshot reference (Vault snapshot)
- signed release pack
- changelog (авто)

Режимы:
- ad‑hoc release (когда готово)
- weekly train (каждую пятницу)
- monthly stable

UI:
- календарь релизов
- “что в поезде” (список изменений)
- “готовность” (все approvals? тесты?)

---

## 55061–55110 — Rollout & Canary: безопасная раскатка
Rollout plan:
- canary group (5% пользователей/тенантов)
- monitoring window
- success criteria
- auto rollback conditions

Поддержка:
- feature flags (включать частями)
- staged rollout per tenant
Связь с Observability OS:
- метрики ошибок
- latency
- saturation

---

## 55111–55160 — Incident & Postmortem: когда всё сломалось
Incident:
- severity (S1..S4)
- affected services/processes (из Graph)
- timeline (из Runtime + human notes)
- mitigation steps (runbook links)

Postmortem:
- What happened
- Root cause (ссылка на root cause path)
- What went well / poorly
- Action items (создаются как tasks)
- Prevent recurrence (policy/test addition)

---

## 55161–55190 — Metrics: DORA‑логика для IFOS
Минимальные метрики:
- change lead time (идея → релиз)
- deployment frequency (сколько релизов)
- change failure rate (релизы, вызвавшие incident)
- MTTR (время восстановления)

Это нужно, чтобы IFOS “учился” и улучшался.

---

## 55191–55200 — Enterprise Add‑ons: аудит, комплаенс, запреты
- mandatory approvals per domain
- immutable audit logs
- legal hold on incident packs
- segregation of duties (SoD)
- approval delegation (замена на отпуск)

---

## Итог
Change Management OS делает “рационализацию” управляемой:
- не изобретать новое, а улучшать существующее **без хаоса**
- изменения видны, проверяемы, воспроизводимы
- релизы и откаты безопасны

---

## Что дальше
Следующий блок:
**55201–55600 — Compliance & Policy Engine OS: политики данных/безопасности/контрактов, rule engine, автоматическое enforcement**  
Скажете “Продолжение” — сделаю.
