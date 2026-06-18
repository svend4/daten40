
# IFOS 79601–80000: Consolidation & Multi-entity Finance OS

## Purpose
Enable financial consolidation across multiple entities (legal entities, workspaces, subsidiaries):
- Intercompany transactions and eliminations
- Multi-currency consolidation with FX translation
- Period close orchestration
- Group-level financial statements

This block builds on Ledger, AR/AP, Treasury, Tax and Audit to produce **group truth**.

## Core Capabilities
1) **Entity Model**
   - Legal entities, business units, workspaces
   - Ownership structure (parent/child, % ownership)
   - Functional vs reporting currency

2) **Intercompany (IC)**
   - IC invoices and settlements
   - IC balances and mismatches
   - Automated eliminations and reclassifications

3) **FX & Translation**
   - Spot / average / closing rates
   - Translation methods (current rate, temporal)
   - FX differences (realized/unrealized)

4) **Consolidation Engine**
   - Trial balance roll-up
   - Eliminations (IC revenue/expense, IC AR/AP)
   - Minority interest calculation
   - Adjustments and top-side entries

5) **Period Close**
   - Close checklist per entity
   - Dependencies and approvals
   - Locking periods after close

6) **Group Reporting**
   - Consolidated P&L, Balance Sheet, Cash Flow
   - Segment reporting
   - Drill-down to entity and transaction

## Inputs
- Ledger trial balances (per entity)
- AR/AP IC balances
- Treasury FX rates
- Tax adjustments
- Audit evidence

## Outputs
- Consolidated trial balance
- Group financial statements
- Elimination journals
- Close status and evidence packs

## APIs (High-level)
- POST /entities
- POST /ownership
- POST /fx/rates
- POST /consolidation/run
- GET  /consolidation/results
- POST /period/close

## Data Model (Minimal)
- entity
- ownership_link
- fx_rate
- trial_balance
- ic_balance
- elimination_entry
- consolidation_run
- group_report

## KPIs
- Days-to-close
- IC mismatch rate
- FX impact
- Adjustment volume

## Security & Compliance
- Entity-level access control
- Locked periods (read-only)
- Full audit trail of eliminations and overrides

## Dependencies
- 77601–78000 Audit & Compliance
- 78401–78800 Accounting Ledger
- 78801–79200 AR/AP
- 79201–79600 Treasury & Cash Management

## Version
v1 (2026-01-11)
