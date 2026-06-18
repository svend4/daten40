# IFOS Block 78401–78800: Accounting Ledger & Financial Reporting OS (v1)

## 1) Назначение блока
Этот блок добавляет **финансовый “источник истины”** поверх остальных модулей IFOS: счета/инвойсы, налоги, платежи, биллинг, маркетплейс, возвраты, споры, подписки и т.п.
Цель — чтобы любая операция в IFOS могла быть:
- отражена в **двойной записи** (double-entry),
- связана с первичными документами (invoice/credit note/tax doc),
- сверена (reconciliation) с платежами/выплатами,
- выведена в **финансовые отчёты** (P&L / Balance Sheet / Cash Flow),
- проверяема (audit-ready) через EvidencePack (см. 77601–78000).

## 2) Что блок делает
### 2.1 Двойная запись (Double-entry)
- Генерация **JournalEntry** из событий:
  - invoice_issued / invoice_paid / refund_issued
  - payout_settled / fee_charged / chargeback
  - vat_reported / vat_paid
- Валидация: сумма дебетов = сумма кредитов; валюта; дата; период.

### 2.2 Главная книга (General Ledger)
- Хранение LedgerEntry / JournalEntry (append-only + корректировки через reversal).
- Срезы по:
  - Company/Workspace
  - Project/Product/Marketplace listing
  - Customer/Vendor
  - Tax jurisdiction
  - Time period (day/month/quarter/year)

### 2.3 План счетов (Chart of Accounts)
- Базовый CoA по типовой SaaS/Marketplace модели.
- Маппинг CoA ↔ “Capabilities/Products” (для аналитики).

### 2.4 Финансовая отчётность
- P&L (доходы/расходы, валовая маржа, EBITDA-черновик)
- Balance Sheet (активы/обязательства/капитал)
- Cash Flow (операц./инвест./фин.)
- Отчёт по НДС/налогам (агрегация по юрисдикциям) — интеграция с 78001–78400.

### 2.5 Сверка и закрытие периода
- Автоматическая сверка:
  - invoices ↔ payments
  - payouts ↔ ledger
  - fees ↔ ledger
- “Close period” workflow:
  - freeze_period
  - produce_reports
  - sign_off (подпись ответственным лицом)
  - attach evidence (в EvidencePack)

## 3) Что блок НЕ делает (границы ответственности)
- Не является банковским процессингом (это 42001–42400/платежи).
- Не заменяет юридические договоры (76801–77200) и налоговые правила (78001–78400), а **подкладывает бухгалтерский слой**.
- Не пытается “угадать” легальную бухгалтерию каждой страны — вместо этого поддерживает **плагины правил** (mapping/rulesets).

## 4) Основные сущности (data model)
- Account (CoA)
- JournalEntry / JournalLine (debit/credit)
- LedgerEntry (материализованный слой)
- FinancialPeriod (month/quarter/year)
- ReconciliationRun (сводка + расхождения)
- FinancialReport (P&L/BS/CF + параметры)
- MappingRule (event→accounts)

## 5) API (эскиз)
- POST /ledger/events/ingest  (event → journal)
- POST /ledger/journals/post
- GET  /ledger/entries?filters…
- POST /ledger/reconcile/run
- POST /ledger/periods/<built-in function id>/close
- GET  /ledger/reports/pnl
- GET  /ledger/reports/balance-sheet
- GET  /ledger/reports/cash-flow

## 6) KPI качества
- Reconciliation match rate ≥ 99.5%
- Report generation latency ≤ 60s (typical workspace)
- Audit completeness: 100% JournalEntry linked to source_event_id

## 7) Мини-MVP (P0/P1)
P0:
- CoA seed + JournalEntry schema
- Ingest событий (invoice/payment/refund/payout/fee)
- P&L за период + basic reconciliation
P1:
- Balance Sheet + Cash Flow
- Period close workflow + EvidencePack attachment
- Rule packs per business model (SaaS, Marketplace, Services)

## 8) Зависимости (логические)
- Платежи/выплаты: 42001–42400, 32401–32800
- Налоги/инвойсы: 78001–78400
- Audit/Evidence: 77601–78000
- Marketplace billing: 32401–32800
