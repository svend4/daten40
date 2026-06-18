
# IFOS 78801–79200: AR/AP, Collections & Dunning OS

## Purpose
Provide end-to-end Accounts Receivable / Accounts Payable management:
- Invoice lifecycle (issued → delivered → due → paid → closed)
- Partial payments, credits, refunds, write-offs
- Dunning workflows (reminders, escalation, pauses)
- Collections status and aging
- Integration with Ledger (double-entry), Tax/VAT, Audit & Compliance

## Core Capabilities
- AR/AP entities and states
- Aging buckets and policies
- Dunning rules and schedules
- Payment allocation logic
- Dispute and promise-to-pay tracking
- Export to Ledger and Evidence Packs

## Inputs
- Invoices (from 78001–78400)
- Payments (from Payments/Settlement)
- Ledger mappings (78401–78800)
- Policies (reminders, grace periods)

## Outputs
- AR/AP balances
- Aging reports
- Dunning events
- Journal entries
- Compliance evidence

## APIs (High-level)
- POST /ar/invoices
- POST /ap/bills
- POST /payments/allocate
- POST /dunning/run
- GET /aging
- GET /collections/cases

## KPIs
- DSO / DPO
- Aging distribution
- Collection rate
- Write-off rate

## Security & Compliance
- Role-based access
- Audit events for every state change
- EvidencePack export compatible

## Dependencies
- 77601–78000 Audit & Compliance
- 78001–78400 Tax/VAT/Invoicing
- 78401–78800 Accounting Ledger

## Version
v1 (2026-01-11)
