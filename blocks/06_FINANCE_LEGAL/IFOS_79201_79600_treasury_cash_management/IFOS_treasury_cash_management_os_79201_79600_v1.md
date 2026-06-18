
# IFOS 79201–79600: Treasury & Cash Management OS

## Purpose
Centralize cash visibility and control across bank accounts, payment rails, wallets and reserves.
This block closes the loop between:
- Payments/Settlement (cash movements),
- AR/AP (what should happen),
- Ledger (what is booked),
by adding **bank statement ingestion, reconciliation and cash forecasting**.

## Core Capabilities
1) **Accounts & Instruments**
   - Bank accounts, wallets, virtual accounts
   - Account metadata (IBAN, BIC, bank, currency, country)
   - Authorized signers, limits, approval rules (ties into Identity/Access)

2) **Bank Statement Ingestion**
   - Import formats: CAMT.053/054, MT940, CSV, API pulls
   - Statement normalization: posting date/value date, references, counterparty
   - Statement integrity checks (duplicates, gaps, checksums)

3) **Cash Ledger / Cash Events**
   - Normalize all movements into `cash_event`
   - Track pending vs cleared vs reversed
   - Link cash events to payment intents and ledger postings

4) **Reconciliation (Bank ↔ Payments ↔ Ledger)**
   - Matching rules: exact, fuzzy, multi-leg, partial
   - Exception queue: unmatched, ambiguous, split/merge
   - Evidence + audit trail for each match decision
   - Reconciliation KPIs: match rate, time-to-match, exception backlog

5) **Cash Position & Forecasting**
   - Daily cash position by currency, entity, bank
   - Short-term forecast (7/14/30/90 days) using:
     - scheduled AP/AR
     - recurring expenses/revenue patterns
     - upcoming subscriptions
   - Scenario knobs: pessimistic/expected/optimistic

6) **Controls & Risk**
   - Limits and approvals for transfers
   - Large payment alerts, unusual patterns
   - Segregation of duties (SoD)
   - Integration with Fraud / Trust-Safety

## Inputs
- Payment events (Payments/Settlement)
- Invoices/Bills/Allocations (AR/AP)
- Journal entries (Ledger)
- Bank statements (file import / API)

## Outputs
- Cash position snapshots
- Reconciliation results + exception cases
- Forecast reports and alerts
- Bank fee analytics
- Evidence packs for audit

## APIs (High-level)
- POST /treasury/accounts
- POST /treasury/statements/import
- POST /treasury/reconcile/run
- GET  /treasury/cash-position
- GET  /treasury/forecast
- POST /treasury/transfers (optional; policy-gated)

## Data Model (Minimal)
- treasury_account
- bank_statement
- bank_txn (normalized)
- cash_event
- reconcile_match
- reconcile_exception
- cash_snapshot
- cash_forecast

## KPIs
- Cash coverage days
- Match rate (%)
- Exceptions aging
- Forecast accuracy
- Bank fees per volume

## Security & Compliance
- Audit log for imports, matching decisions, overrides
- PII minimization (masking IBAN where appropriate)
- Strong access controls for treasury operations

## Dependencies
- 77601–78000 Audit & Compliance
- 78401–78800 Accounting Ledger
- 78801–79200 AR/AP, Collections & Dunning
- Payments/Settlement block (earlier)

## Version
v1 (2026-01-11)
