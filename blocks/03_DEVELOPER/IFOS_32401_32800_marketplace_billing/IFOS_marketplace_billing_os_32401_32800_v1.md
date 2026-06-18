# IFOS 32401–32800 — Marketplace & Billing OS (v1)
Цель: превратить “словарь функций интернета” в **работающий рынок**:
- разработчик/автор выкладывает “функцию” (плагин/сценарий/шаблон/API),
- пользователь покупает/подписывается,
- система выдаёт **лицензию/доступ**, запускает “one‑click install/run”,
- биллинг прозрачен (trial, подписка, pay‑as‑you‑go),
- справедливая монетизация (revenue share),
- возвраты/чарджбеки/налоги/аудит — тоже часть системы.

Порядок: простое → среднее → сложное.

---

## 32401–32430 — Marketplace Listing: “витрина для продажи”
**MarketplaceListing** связывает RegistryItem с коммерцией:
- что продаём: `item_id` или `bundle_id`
- кто продаёт: `seller_id`
- как продаём: pricing model (одноразово/подписка/usage)
- условия: trial, SLA, поддержка, политика возвратов
- ограничения лицензии: seats, domain, org, usage limits
- регионы/валюты

Мини‑правило: **контент и “установка” живут в Registry, а деньги и права — в Marketplace OS.**

---

## 32431–32470 — Pricing Model: 3 базовые модели
### 1) One‑time (разовая покупка)
- заплатил → получил perpetual license (или фиксированный срок)
- обновления: отдельно или включены N месяцев

### 2) Subscription (подписка)
- monthly/yearly
- уровни: Free/Pro/Team/Enterprise
- seats (кол‑во пользователей), org‑license

### 3) Usage‑based (pay‑as‑you‑go)
- платишь за фактическое использование: вызовы API, задачи, минуты CPU, GB storage
- нужен **metering** (счётчик) и защита от накруток

Комбинации тоже возможны: подписка + лимиты + сверхлимитная тарификация.

---

## 32471–32510 — Trial Policy: “попробуй без боли”
Trial бывает:
- time‑based (14 дней)
- usage‑based (1000 задач)
- feature‑based (ограниченные функции)

Trial должен:
- включать “one‑click demo”,
- иметь авто‑конвертацию или мягкое завершение,
- давать понятный отчёт “что использовано”.

---

## 32511–32560 — Лицензии и Entitlements: “что именно купили”
**LicenseEntitlement** — это ключевой объект:
- кому выдано (user/org)
- на что выдано (item/bundle)
- тип: trial/subscription/perpetual
- ограничения: seats, domains, usage limits
- срок действия
- подпись/токен (для оффлайн/онлайн проверки)

Это “право запуска”: Installer/Runtime должен проверять entitlement перед запуском.

---

## 32561–32610 — Usage Metering: учёт потребления
Для usage‑based системы нужны:
- **UsageMeter** (что меряем: task_runs, api_calls, minutes)
- **UsageEvent** (событие использования)
- агрегатор: суммирование по периоду

Ключ: **идемпотентность** (одно событие не учитывается дважды) и защита от повторной доставки (webhooks/ретраи).

---

## 32611–32660 — Заказы/счета/платежи
### PurchaseOrder
- что покупают (listing + plan)
- сколько (seats/qty)
- цена + скидки + налоги

### Invoice
- документ для бухгалтерии (особенно B2B)
- line items: подписка/usage/скидки/НДС

### Payment Provider
- Stripe/PayPal/SEPA/банковские переводы (зависит от страны)
- Webhooks: payment_succeeded, payment_failed, subscription_canceled

Правило: **платёж = событие; entitlement выдаётся только после подтверждения.**

---

## 32661–32710 — Revenue Share и выплаты авторам
Marketplace должен уметь:
- доли: платформа/автор/партнёр (referral)
- учёт комиссий, налогов, возвратов
- payout schedule: weekly/monthly
- payout account: банковский счёт/PayPal

RevenueShare может быть:
- фиксированный %
- tiered (чем больше продаж, тем меньше комиссия)
- специальные условия для “витрин”/curation

---

## 32711–32750 — Возвраты и чарджбеки
Потому что B2B и B2C реальность:
- Refund: добровольный возврат
- Chargeback: принудительный спор

Важно:
- entitlement должен быть отозван
- usage может быть “заморожен”
- анти‑фрод сигналы влияют на trust seller/customer

---

## 32751–32790 — Налоги и комплаенс (минимально)
Даже если в v1 делать “минимально”, нужно:
- TaxProfile (страна, VAT ID, B2B reverse charge)
- ставки/правила по региону
- хранение инвойсов и audit trail

---

## 32791–32800 — Безопасность и аудит
Обязательные элементы:
- AuditLog (кто что сделал)
- подпись токенов entitlement
- webhook verification
- минимальная KYC для продавцов (хотя бы verified seller)

---

## Мини‑архитектура Marketplace & Billing OS
Listing → Pricing/Plans → Trial → Purchase → Payment Confirmed → Entitlement Issued → Install/Run Allowed → Usage Metering → Invoice → Revenue Share → Payout → Refund/Chargeback → Audit

---

## Что дальше
Следующий блок:
**32801–33200 — Runtime & Execution OS** (песочницы, исполнение сценариев, секреты, политики безопасности, “запусти где угодно”: сервер/контейнер/Android, мониторинг, логи, откат).  
Скажете “Продолжение” — сделаю.
