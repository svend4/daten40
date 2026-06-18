# IFOS Block 82 (75601–76000): Certificate Compliance — Linting, Transparency, Trust Distribution, Audits

**Purpose:** Operationalize certificate hygiene and trust correctness at scale: detect weak/invalid certificates, drifted trust stores, improper SAN/EKU usage, and missing audit trails. Provide clear compliance signals for security and reliability teams.

---

## 1) What this block enables

### 1.1 Certificate linting (policy-as-code)
- Validate issued/imported certificates against:
  - maximum validity (e.g., 90d public, 7d workloads)
  - allowed algorithms (no SHA1, no RSA1024)
  - SAN patterns (no wildcard in internal mTLS)
  - EKU correctness (clientAuth/serverAuth/codeSigning, etc.)
  - name constraints and forbidden domains
- Emit violations with severity, owner, and remediation guidance.

### 1.2 Trust store distribution & drift detection
- Define “authoritative trust stores” per scope (org/workspace/env).
- Distribute bundles to gateways, agents, meshes, edge nodes.
- Detect drift: node trust store differs from expected bundle (hash mismatch).

### 1.3 Transparency & provenance (internal CT optional)
- Optional: publish issued cert metadata to a transparency log (internal or public where appropriate).
- Ensure traceability: issuance request → approval → issuance → deployment targets.

### 1.4 Audit dashboards & evidence packs
- Compliance posture dashboard: violations by severity/team/system.
- Evidence export for audits (SOC2/ISO style): policy configs, approval logs, drift reports.

---

## 2) Core entities

### 2.1 ComplianceRule
- `rule_id`, `name`, `severity` (low|med|high|critical)
- `selector`: profile/purpose/scope
- `check`: algorithm/validity/san/eku/chain/trust_drift
- `remediation`: text + links + runbook reference

### 2.2 Violation
- `violation_id`, `cert_id` or `trust_target_id`
- `rule_id`, `detected_at`, `status` (open|ack|mitigated|resolved|false_positive)
- `owner_team`, `due_date`, `case_ref`

### 2.3 TrustTarget
- `target_id`, `type` (gateway|agent|mesh|edge)
- `observed_bundle_hash`, `expected_bundle_hash`, `last_checked_at`

---

## 3) APIs

- `POST /pki/compliance/rules`
- `GET /pki/compliance/violations`
- `POST /pki/compliance/violations/{id}/ack`
- `POST /pki/truststores/{id}/drift-check` (or scheduled checks)
- `GET /pki/compliance/evidence-pack` (exports configs + logs)

---

## 4) Detection loops

- Nightly lint scan over active cert inventory (plus on-issue hook).
- Hourly drift check for Tier0 targets; daily for others.
- Alerts via Notifications + AIOps correlation for spikes or critical drift.

---

## 5) Integration points

- **PKI core (75201–75600):** certificate inventory, issuance logs, trust stores.
- **Service Catalog (72801–73200):** map violations to owners and blast radius.
- **Change Intelligence (73201–73600):** tie drift/violations to recent deployments.
- **Case Mgmt (42801–43200):** open cases for critical violations.

---

## 6) MVP checklist

- [ ] 10–15 lint rules (algorithms, validity, EKU, SAN patterns).
- [ ] Drift detection for at least gateways + k8s agents.
- [ ] Dashboard: violations by severity/team.
- [ ] Evidence export (json/zip) for audits.
