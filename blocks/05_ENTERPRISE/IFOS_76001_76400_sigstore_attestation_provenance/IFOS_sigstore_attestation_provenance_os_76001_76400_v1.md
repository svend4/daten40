# IFOS Block 82 (76001–76400): Sigstore Attestation + Provenance

**Purpose:** Add supply-chain trust primitives to IFOS: artifact signing, provenance attestations, and SBOM linkage with policy-driven verification. This block makes “what you run” verifiable: **who built it**, **how**, **from what sources**, and **whether it meets org policy**.

---

## 1) What this block enables

### 1.1 Artifact signing (containers, bundles, templates, connectors)
- Sign build outputs (OCI images, bundles, connector packages) using **keyless** or key-based identities.
- Maintain verifiable signatures and immutable references (digest-first discipline).

### 1.2 Attestations (provenance, SBOM, test results)
- Attach **provenance** attestations (SLSA/in-toto-style predicates) to artifacts.
- Attach **SBOM** attestations (SPDX/CycloneDX payloads or references) to artifacts.
- Optionally attach attestations for:
  - CI test results (unit/integration), lint, policy checks
  - vulnerability scan summaries (links to existing vulnerability mgmt blocks)
  - license compliance reports (future block)

### 1.3 Transparency log & auditability (Sigstore-like)
- Record signature/attestation events into an append-only log abstraction (rekor-like).
- Provide a normalized audit trail usable by:
  - Marketplace curation & quality gates
  - Enterprise governance approvals
  - Incident response investigations

### 1.4 Policy verification at install / run
- Verify signatures and attestations:
  - at **publish** time (Marketplace),
  - at **install** time (Package Manager),
  - at **run** time (Runtime Execution / Workflow Runner),
  - at **sync** time (Edge + Offline sync).
- Enforce “deny by default” policies for sensitive environments.

---

## 2) Scope boundaries (what this block does NOT try to be)

- Not a full CI/CD system. It integrates with pipelines and stores/verifies outcomes.
- Not a full SBOM generator. It can **ingest** SBOMs, store references, and validate presence/format.
- Not a full PKI. It builds on **Certificate & PKI** and **KMS/Secrets** blocks for identities/keys.

---

## 3) Core entities (data model)

### 3.1 ArtifactRef
- `artifact_type`: (oci_image|bundle|connector|template|doc_pack)
- `artifact_digest`: immutable digest (e.g., sha256)
- `artifact_uri`: optional registry URI
- `producer`: service/team/workspace reference

### 3.2 SignatureRecord
- `signature_id`, `artifact_ref`
- `issuer`: identity (keyless subject, cert chain, or key id)
- `signature_bytes` (opaque) + `signature_format` (cosign-like)
- `timestamp`, `transparency_log_entry` (optional)
- `verification_status`: (verified|failed|unknown) + reason

### 3.3 AttestationRecord
- `attestation_id`, `artifact_ref`
- `predicate_type`: (provenance|sbom|test_results|vuln_scan|license_report|custom)
- `payload_ref`: stored blob or external reference (object store / registry)
- `subject_identity`: signer identity
- `timestamp`, `transparency_log_entry` (optional)
- `verification_status` + reason

### 3.4 PolicyGate
- `policy_id`, `name`, `scope` (org|workspace|env|service|artifact_type)
- `requirements`:
  - signature required (yes/no)
  - keyless identities allowed (yes/no) + allowed issuers/domains
  - provenance required (predicate type + minimum fields)
  - sbom required (format + freshness)
  - vulnerability gate (max severity, allowlists)
  - license gate (future block)
- `enforcement_point`: publish|install|run|sync

---

## 4) APIs (minimal surface)

### 4.1 Publish / attach
- `POST /supplychain/signatures` (register signature for an artifact digest)
- `POST /supplychain/attestations` (register attestation for artifact digest)
- `GET /supplychain/artifacts/{digest}/trust` (summary: signatures + attestations + policy status)

### 4.2 Verify / enforce
- `POST /supplychain/verify` (input: artifact digest + requested policy scope; output: pass/fail + reasons)
- `POST /supplychain/policies` (create/update policy gates)
- `GET /supplychain/policies` / `GET /supplychain/policies/{id}`

### 4.3 Transparency log adapter (optional MVP)
- `POST /supplychain/log/append` (internal) → returns log index/hash
- `GET /supplychain/log/entries/{id}`

---

## 5) Workflows (end-to-end)

### 5.1 Marketplace publish (happy path)
1. Producer builds connector/bundle → computes digest.
2. Producer signs digest and uploads signature record.
3. CI emits provenance + SBOM attestations and uploads them.
4. Marketplace runs policy verify (publish gate).
5. If pass → artifact becomes “trusted” for allowed scopes.

### 5.2 Install-time enforcement (enterprise)
1. Admin selects bundle → Package Manager fetches artifacts by digest.
2. Verify signature + required attestations for target env.
3. If fail → block install, open a Case (Case Mgmt) with evidence.

### 5.3 Runtime enforcement (high-security)
- Runtime Execution / Workflow Runner re-verifies trust on each run:
  - allow cached trust decisions with TTL for performance
  - re-check when policy changes or new vulnerabilities emerge

---

## 6) Security & compliance notes

- Prefer **digest pinning** everywhere; treat tags as pointers only.
- Maintain an immutable audit trail for signature/attestation events.
- Keyless identities must be constrained by strict issuer + subject rules.
- Provide break-glass paths (time-limited policy exceptions) with mandatory case/audit records.

---

## 7) Dependencies

Hard dependencies:
- **Certificate & PKI + mTLS** (75201–75600) for trust roots and identity binding.
- **KMS & Secrets Rotation** (74801–75200) for key refs, signer identities, and rotation.
- **Marketplace Curation & Quality** (45601–46000) + **Publishing/Release Workflow** (46001–46400) for publish-time gates.
- **Runtime Execution** (32801–33200) + **Workflow Runner** (44801–45200) for install/run enforcement points.

Nice-to-have:
- **Vulnerability & Patch Management** (74001–74400) to enrich policy checks with CVE gates.
- **Compliance Policy Engine** (55201–55600) for unified policy authoring and audits.

---

## 8) MVP checklist (to call this block “usable”)

- [ ] Register signatures and attestations for artifacts (by digest).
- [ ] Policy gates with at least: “signature required” + “provenance required”.
- [ ] Verification API returning pass/fail + reasons + evidence bundle.
- [ ] Publish-time enforcement in Marketplace (soft fail allowed for P0; hard fail for P1+).
- [ ] Install-time enforcement for enterprise environments (hard fail).
- [ ] Audit log of trust decisions (who verified, which policy, when).

---

## 9) Next block suggestion (planned)

After provenance is in place, the next practical extension is **open-source license compliance**:
policy gates for SPDX licenses, attribution bundle generation, and exportable compliance artifacts.
