# IFOS Block 48 (73601–74000): Backup, Restore & Retention

**Purpose:** Ensure IFOS data can be recovered (accidental deletion, corruption, ransomware, operator error) with clear policies, automation, and tested restore procedures.

---

## 1) What this block enables

### 1.1 Backup policies (by data class)
- Define backup frequency, retention, encryption, and storage targets per dataset:
  - configuration/state
  - workflow definitions/templates
  - audit logs
  - customer content/assets
  - telemetry

### 1.2 Restore orchestration
- Point-in-time restores and object-level restores (where supported).
- Restore runbooks per service, plus automated “restore drills”.

### 1.3 Retention & legal hold
- Policy-driven retention periods and deletion rules.
- Optional legal hold flags to suspend deletions.

### 1.4 Integrity & tamper evidence
- Checksums for backup sets.
- Immutable storage modes (WORM) where available.

---

## 2) Core entities

### 2.1 BackupPolicy
- `policy_id`, `name`, `dataset_selector`
- `frequency` (hourly|daily|weekly), `retention_days`
- `encryption` (kms_key_ref), `storage_target` (s3|gcs|azure|local)
- `restore_rto_minutes`, `restore_rpo_minutes`

### 2.2 BackupJob / Snapshot
- `job_id`, `dataset`, `started_at`, `ended_at`, `status`
- `artifact_ref`, `size_bytes`, `checksum`

### 2.3 RestorePlan
- `plan_id`, `service`, `steps`, `prechecks`, `postchecks`
- `approval_required` (bool), `blast_radius_notes`

---

## 3) APIs

- `POST /backup/policies`
- `POST /backup/jobs/run` (manual trigger)
- `GET /backup/jobs` / `GET /backup/jobs/{id}`
- `POST /restore/plans`
- `POST /restore/run` (with plan + restore point)
- `GET /restore/runs/{id}`

---

## 4) Integration points

- **DR Plans (63201–63600):** align RTO/RPO, failover, and restore drills.
- **KMS/Secrets (74801–75200):** encryption keys for backups.
- **Incidents (69201–69600):** restore used during incident response.
- **Change Intelligence (73201–73600):** restore blast radius annotations.

---

## 5) MVP checklist

- [ ] Backup policies for 3 core datasets.
- [ ] Daily automated backup jobs with retention enforcement.
- [ ] Restore plan + one quarterly restore drill.
- [ ] Encryption via KMS key reference.
