# IFOS Block 50 (74401–74800): Access Reviews & Privileged Access Management (PAM)

**Purpose:** Keep access least-privilege over time: periodic reviews, privileged session controls, just-in-time elevation, and auditability.

---

## 1) What this block enables

### 1.1 Periodic access reviews
- Campaigns per org/workspace/system (quarterly, monthly for sensitive).
- Reviewer assignment (manager, system owner, security).
- Decisions: keep, revoke, reduce scope, request justification.

### 1.2 Privileged access (PAM patterns)
- JIT elevation with approval and expiry.
- Break-glass roles with strict logging.
- Privileged session recording (optional, via connector to PAM vendor).

### 1.3 Audit trails & enforcement
- Every privileged grant has: reason, approver, start/end, linked ticket/incident.
- Auto-revoke on expiry; reminders and escalations.

---

## 2) Core entities

### 2.1 AccessReviewCampaign
- `campaign_id`, `scope`, `target_system`, `start`, `due`
- `reviewers`, `items_count`, `status`

### 2.2 AccessReviewItem
- `principal_ref`, `role/permission`, `last_used_at`
- `decision` + `justification`

### 2.3 PrivilegeGrant
- `grant_id`, `principal_ref`, `role`, `start`, `end`
- `approval_ref`, `ticket_ref`, `session_recording_ref`

---

## 3) APIs

- `POST /access-reviews/campaigns`
- `GET /access-reviews/campaigns/{id}`
- `POST /access-reviews/items/{id}/decide`
- `POST /pam/grants` (JIT request)
- `POST /pam/grants/{id}/approve`
- `POST /pam/grants/{id}/revoke`

---

## 4) Integration points

- **Identity & Access** for roles, groups, RBAC.
- **Case Mgmt / Incidents** for approvals and evidence.
- **KMS/Secrets** for break-glass credentials handling.
- **Admin Console** for governance UI.

---

## 5) MVP checklist

- [ ] Quarterly review campaigns for admin roles.
- [ ] JIT elevation requests with expiry + audit.
- [ ] Auto-revoke + escalation reminders.
