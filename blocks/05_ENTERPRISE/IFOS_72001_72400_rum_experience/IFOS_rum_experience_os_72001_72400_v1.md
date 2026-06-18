# IFOS Block 44 (72001–72400): Real User Monitoring (RUM) & Experience

**Purpose:** Measure and improve end-user experience across IFOS web/mobile: performance, errors, journeys, and regressions — tied back to releases, feature flags, and incidents.

---

## 1) What this block enables

### 1.1 Client-side telemetry (web + mobile)
- Page load and navigation timing (Core Web Vitals / app startup time).
- Frontend error capture (JS exceptions, unhandled promise rejections, mobile crashes).
- Network tracing (XHR/fetch timing, API failures, retry loops).
- Session context: device, browser/app version, locale, coarse geo, network type.

### 1.2 Journeys & funnels
- Define “critical journeys” (login, create workspace, run workflow, publish release).
- Track funnel conversion and abandonment reasons.
- Correlate experience degradation with feature flags and release rollouts.

### 1.3 Session replay (optional)
- Privacy-safe replay with masking/redaction.
- Sampling controls and per-scope enablement (org/workspace/environment).

### 1.4 Alerting & correlation
- Alerts on regressions (e.g., p95 LCP > threshold, error rate spike).
- Correlate to backend APM/Tracing, logs, and synthetic monitoring.

---

## 2) Scope boundaries

- This is not a full analytics/marketing suite; it focuses on reliability & UX health.
- “User identity” is handled by Identity blocks; RUM stores only safe identifiers.
- Privacy: defaults to minimal; session replay is opt-in and heavily masked.

---

## 3) Core entities

### 3.1 RUMProject
- `project_id`, `name`, `platform` (web|android|ios)
- `org_scope`, `workspace_scope`, `env_scope`
- `sampling`: session %, replay %, error %

### 3.2 RUMEvent (normalized)
- `timestamp`, `type` (nav_timing|web_vitals|error|api_call|custom)
- `session_id`, `anon_user_id`, `route`, `release_version`, `flag_snapshot`
- `metrics`: LCP/INP/CLS, TTFB, paint, memory, battery (mobile)

### 3.3 JourneyDefinition
- `journey_id`, `name`, `steps` (routes/actions), `success_criteria`
- `slo`: availability + latency + error budget at the journey level

### 3.4 ReplayArtifact (optional)
- `replay_id`, `session_id`, `storage_ref`, `masking_profile`

---

## 4) APIs & ingestion

### 4.1 Client SDK ingestion
- `POST /rum/ingest` (batched, compressed)
- `POST /rum/replay/ingest` (optional stream)
- Auth: public key + rate limits; tenant mapping by project token.

### 4.2 Query & dashboards
- `GET /rum/projects/{id}/metrics` (p50/p95/p99, error rates)
- `GET /rum/projects/{id}/journeys/{jid}/funnel`
- `GET /rum/projects/{id}/replays/{rid}` (if enabled)

---

## 5) Integration points (important)

- **Release Progressive Delivery (70801–71200):** tag events by release/rollout.
- **Feature Flags (51201–51600):** attach flag snapshot for each session.
- **Incidents & Postmortems (69201–69600):** auto-create evidence bundles.
- **AIOps Correlation (72401–72800):** client signals enrich root-cause analysis.
- **Synthetic Monitoring (71601–72000):** compare “lab” vs real-user signals.

---

## 6) Privacy & security controls

- Default redaction of input fields, query strings, PII candidates.
- Configurable allow/deny list for routes, event names, headers.
- Per-tenant data retention policies (e.g., 30/90/180 days).
- Sampling and “kill switch” via remote config.

---

## 7) MVP checklist

- [ ] Web SDK ingestion + basic dashboards (web vitals + errors).
- [ ] Release/version tagging.
- [ ] Alert on error spike and p95 regression.
- [ ] Minimal privacy-safe identifiers + retention policies.
- [ ] Optional: journey definitions for 3 core flows.

---

## 8) Next block synergy

RUM becomes most powerful when combined with:
- Synthetic journeys (71601–72000),
- AIOps correlation (72401–72800),
- Change intelligence/blast radius (73201–73600).
