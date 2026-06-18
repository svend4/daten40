# IFOS 39601–40000 — Pricing, Quotas & Resource Economy OS (v1)
Цель: чтобы “Интернет функций” был **управляемым по ресурсам**:
- понятные планы/тарифы
- прозрачный учёт использования (metering)
- квоты и rate limits
- SLA и приоритеты
- unit economics (стоимость выполнения функций)
- chargeback/showback (внутренние счета)
- бюджеты и алерты
- классы ресурсов (CPU/GPU/IO/LLM tokens/3rd-party calls)

Порядок: простое → среднее → сложное.

---

## 39601–39630 — Resource Classes: что именно мы считаем
ResourceClass — “валюта ресурсов”:
- compute_cpu_seconds
- gpu_seconds
- storage_gb_month
- egress_gb
- llm_tokens_in / llm_tokens_out
- third_party_calls (например, внешние API)
- workflow_steps
- human_review_minutes (если есть модерация)

Зачем: разные функции потребляют разные ресурсы. Без этого нет честной экономики.

---

## 39631–39680 — Usage Meter: учёт использования по run’ам
UsageMeter собирает события:
- tenant_id / user_id / project_id
- tool/workflow/bundle id
- run_id
- ресурсы (по ResourceClass)
- время и статус
- “цена” (если есть прайс-лист)

Ключ: metering строится на **runs**, а не на абстрактных “пользователях”.

---

## 39681–39720 — Quota Policy: квоты как ограждения
QuotaPolicy задаёт лимиты:
- на тенант (monthly tokens, daily runs, storage cap)
- на пользователя (per-day)
- на проект/namespace
- на конкретные классы функций (например “дорогие LLM”)

Поведение при превышении:
- block (жёстко)
- throttle (замедлить)
- degrade (перейти на “дешёвую” модель/режим)
- require_approval (попросить подтверждение)

---

## 39721–39760 — Rate Limits: защита от перегрузки
RateLimit — это защита в реальном времени:
- N запросов в минуту по endpoint’у
- N runs в час по workflow
- burst limits
- priority lanes (enterprise vs free)

Это обеспечивает стабильность и защищает от “случайной атаки макросами”.

---

## 39761–39810 — SLA: договор по доступности и скорости
SLA фиксирует:
- uptime (например 99.9%)
- latency SLO (p95 для запуска/ответа)
- RPO/RTO (для данных)
- поддержка (response times)
- excluded events (форс-мажор)
- кредиты/компенсации

SLA связан с приоритетами в scheduler’е и rate-limits.

---

## 39811–39870 — Cost Model: unit economics каждой функции
CostModel описывает себестоимость:
- fixed costs (инфраструктура)
- variable costs (LLM tokens, GPU, egress, внешние API)
- overhead (логирование, аудит, compliance)
- риск‑коэффициенты (например, ручная модерация)

На основе CostModel делается:
- price floor (минимальная цена)
- margin targets
- рекомендации по оптимизации (кэш, дедуп, cheaper path)

---

## 39871–39920 — Chargeback/Showback: внутренняя экономика
ChargebackRecord:
- кто потребил (tenant/project)
- что потребил (bundle/workflow)
- сколько (resource units)
- во что это вылилось (€ или внутренние кредиты)
- период и ссылки на runs

Showback = “отчёт без списания”.  
Chargeback = “реальное списание/счёт внутри компании”.

---

## 39921–39960 — Invoices: счета и платёжные циклы
Invoice:
- период
- агрегированные метрики
- скидки/пакеты/лимиты
- налоги (если нужно)
- подписанные артефакты (PDF/JSON)
- ссылка на детализацию (drill-down)

Важно: B2B обычно требует “прозрачной детализации до run’ов”.

---

## 39961–39990 — Budgets & Alerts: контроль расходов
BudgetAlert:
- бюджет на месяц/квартал
- пороги (50/80/100%)
- каналы уведомлений (email/telegram/webhook)
- действия: уведомить, запросить approval, включить degrade mode

Это “педаль тормоза” для владельца тенанта.

---

## 39991–40000 — Итог: экономика как часть ОС
В итоге IFOS становится управляемым:
- мы знаем, что стоит дорого
- квоты защищают от сюрпризов
- rate limits защищают от перегрузки
- SLA делает ожидания явными
- cost model помогает оптимизировать
- chargeback/showback даёт управленческую прозрачность
- бюджеты дают контроль

---

## Что дальше
Следующий блок:
**40001–40400 — Scheduling & Orchestration OS** (очереди, приоритеты, DAG, retries, backpressure, offline runs, “one-click macro execution at scale”).  
Скажете “Продолжение” — сделаю.
