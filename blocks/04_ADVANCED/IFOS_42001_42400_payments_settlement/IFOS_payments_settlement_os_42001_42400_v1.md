# IFOS 42001–42400 — Payments & Settlement OS (v1)
Цель: IFOS должен уметь **брать деньги и честно распределять их**:
- pricing (цены, планы, лимиты, usage)
- quotes (предложение до оплаты)
- invoices/receipts (счёт/чек)
- payment intents (оплата через провайдера)
- refunds/chargebacks (возвраты/споры)
- vendor ledger (учёт доходов поставщиков)
- payouts (выплаты)
- VAT/tax hooks (НДС/налоги и отчёты)
- reconciliation/audit (сверка и доказательства)

Порядок: простое → среднее → сложное.

---

## 42001–42040 — Product Price: прайс‑модель
**ProductPrice** описывает:
- продукт/план (например: “Marketplace Pro”)
- currency, region, tier
- фиксированная цена / usage‑based (per run, per install, per GB)
- free tier и лимиты
- скидки (coupon, volume)

Важно: цена — это не число, а модель расчёта.

---

## 42041–42100 — Quote: коммерческое предложение
**Quote** фиксирует:
- кто покупатель (tenant)
- что покупает (plan + addons)
- срок действия
- расчёт стоимости (включая taxes)
- условия оплаты
Quote нужен B2B, где без счёта нельзя.

---

## 42101–42160 — Invoice & Receipt: счёт и чек
**Invoice**:
- items, quantity, taxes
- supplier (IFOS) и buyer
- payment terms, due date
- уникальный номер и pdf/ref
**Receipt**:
- подтверждение успешной оплаты (payment reference)
- печать/подпись (если требуется)

---

## 42161–42210 — Payment Intent: интеграция с платёжным провайдером
**PaymentIntent**:
- amount, currency
- status: created → authorized → captured → failed
- processor (stripe/adyen/…)
- idempotency keys (без двойной оплаты)
- webhooks (события платежа)

Эта сущность связывает “финансы” и “техническое выполнение”.

---

## 42211–42250 — Refunds & Chargebacks: возвраты и споры
**Refund**:
- частичный/полный
- причина (service issue, duplicate, policy)
- связь с invoice/payment
**Chargeback**:
- спор от банка
- доказательства (logs, invoice, receipt)
- outcome (won/lost)

Нужны прозрачные правила и автоматизация evidence pack (см. комплаенс).

---

## 42251–42320 — Vendor Ledger: учёт поставщиков (marketplace экономика)
**VendorLedger** ведёт:
- начисления поставщику (revenue share)
- комиссии IFOS
- удержания (refund reserve)
- баланс и доступный payout
- ссылки на транзакции

Леджер — ядро marketplace, иначе “деньги теряются”.

---

## 42321–42360 — Payouts: выплаты
**Payout**:
- vendor_id, amount, currency
- период (weekly/monthly)
- метод (bank transfer, SEPA)
- статусы: queued → sent → settled → failed
- отчёт по транзакциям, включенным в payout

---

## 42361–42390 — VAT/Tax Hooks: налоги и локальные правила
**TaxVAT**:
- ставка НДС по региону
- reverse charge (B2B EU)
- налоговые поля invoice (VAT ID, адрес)
- интеграция с tax provider (hook)

Важно: i18n/locale зона влияет на tax rules.

---

## 42391–42400 — Reconciliation & Audit: сверка и контроль
Сверка:
- суммы invoice vs processor settlements
- payout vs ledger balance
- поиск расхождений
Аудит:
- хэши документов
- трассировка “почему начислено так” (lineage + ledger refs)

---

## Итог
Этот блок превращает IFOS в “платформу, которая умеет монетизироваться”:
- честные цены и счета
- безопасная оплата
- прозрачные выплаты поставщикам
- налоги учитываются по зонам
- все проверяемо (audit/recon)

---

## Что дальше
Следующий блок:
**42401–42800 — Customer Support & Dispute Resolution OS** (tickets, SLAs, escalation, dispute workflows, evidence packs, refund policies).  
Скажете “Продолжение” — сделаю.
