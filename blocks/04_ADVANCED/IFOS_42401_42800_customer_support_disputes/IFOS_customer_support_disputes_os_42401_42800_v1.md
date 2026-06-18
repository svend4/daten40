# IFOS 42401–42800 — Customer Support & Dispute Resolution OS (v1)
Цель: чтобы IFOS масштабировался как продукт, нужна “служба поддержки как система”:
- тикеты и очереди
- SLA и эскалации
- база знаний и макросы
- качество поддержки (CSAT)
- споры/возвраты (dispute resolution) с доказательствами (evidence packs)

Порядок: простое → среднее → сложное.

---

## 42401–42440 — Support Tickets: базовая единица поддержки
**SupportTicket**:
- кто пользователь/tenant
- категория (billing, install, run, bug, security)
- severity (low/med/high/critical)
- статус (open → pending → solved/closed)
- ссылки на объекты IFOS (bundle_id, run_id, invoice_id)

Главное: тикет должен быть “привязан к данным”, а не просто текст.

---

## 42441–42500 — Queues & Routing: очереди и маршрутизация
**SupportQueue**:
- очередь по типу (billing/security/marketplace)
- правила маршрутизации (routing rules)
- приоритеты и лимиты

Routing правило:
- security/critical → отдельная очередь + oncall
- billing/chargeback → finance team

---

## 42501–42540 — SLA Policies: сроки реакции и решения
**SLAPolicy** задаёт:
- время до первого ответа (FRT)
- время до решения (TTR)
- рабочие часы (business hours) и праздники
- исключения (например: waiting for customer)

SLA обязательно для B2B и enterprise.

---

## 42541–42590 — Escalations: эскалации и on‑call
**Escalation**:
- триггер (SLA breach, severity increase, security signal)
- куда эскалировать (team, person, webhook)
- действия (создать incident, поставить legal hold, заморозить payout)

Сложный кейс: security тикет может запускать комплаенс‑процедуры.

---

## 42591–42640 — Refund Policies: правила возвратов
**RefundPolicy**:
- условия возврата (например: 14 дней, если не использовано > X runs)
- частичный возврат (pro‑rata)
- исключения (fraud, abuse)
- автоматические триггеры (double charge)

Политика должна быть машинно‑исполняемой (automation).

---

## 42641–42710 — Dispute Cases: споры и арбитраж
**DisputeCase**:
- тип: refund dispute, chargeback, vendor dispute
- стороны (customer ↔ IFOS / vendor)
- сроки, статусы, решения
- evidence refs (лог, invoice, receipt, lineage, access logs)
- outcome: approved/declined/partial

Цель: чтобы решение было объяснимым и проверяемым.

---

## 42711–42750 — Evidence Packs: “папка доказательств” для поддержки
**SupportEvidencePackRef** связывает:
- тикет/диспут
- документы (invoice/receipt)
- технические артефакты (run logs, install logs, audit events)
- хэши и подписи

Это ускоряет поддержку и снижает риск проигранных chargebacks.

---

## 42751–42780 — Knowledge Base & Macros: самопомощь и ускорение
**KBArticle**:
- тема/категория
- версия, язык (i18n)
- ссылки на “как сделать” (blueprints)
**SupportMacro**:
- шаблон ответа + действия (например: запросить логи, запустить redaction)

KB + macros уменьшают нагрузку и повышают качество.

---

## 42781–42800 — CSAT & Quality: качество поддержки
**CSAT**:
- оценка (1–5)
- причины (slow, unclear, solved)
- связь с агентом/очередью
- автоматическое обучение (какие макросы работают)

Система качества нужна для реального роста продукта.

---

## Итог
Этот блок делает IFOS “взрослым продуктом”:
- поддержка привязана к объектам IFOS (runs/bundles/invoices)
- SLA и эскалации управляемы
- споры решаются на доказательствах
- база знаний и макросы уменьшают стоимость поддержки

---

## Что дальше
Следующий блок:
**42801–43200 — Partner Ecosystem & Integrations OS** (партнеры, партнёрские каталоги, ключи API, sandbox/test keys, сертификация интеграций, рейтинги партнёров).  
Скажете “Продолжение” — сделаю.
