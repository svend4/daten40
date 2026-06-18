
-- Freshness statuses (materialized)
CREATE TABLE IF NOT EXISTS evidence_freshness_status (
  id BIGSERIAL PRIMARY KEY,
  environment TEXT NOT NULL,
  policy_pack TEXT NOT NULL,
  control TEXT NOT NULL,
  evidence_id TEXT NOT NULL,
  scope_tags JSONB NOT NULL DEFAULT '{}'::jsonb,
  status TEXT NOT NULL, -- fresh|stale|missing|expired|unknown
  cadence TEXT NOT NULL,
  last_collected_at TIMESTAMPTZ,
  age_seconds BIGINT,
  expires_at TIMESTAMPTZ,
  artifact_sha256 TEXT,
  artifact_uri TEXT,
  registry_event_id TEXT,
  verification JSONB,
  computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  details JSONB
);

CREATE INDEX IF NOT EXISTS idx_freshness_env_pack ON evidence_freshness_status(environment, policy_pack);
CREATE INDEX IF NOT EXISTS idx_freshness_status ON evidence_freshness_status(status);
CREATE INDEX IF NOT EXISTS idx_freshness_evidence_id ON evidence_freshness_status(evidence_id);

-- Compliance snapshots
CREATE TABLE IF NOT EXISTS compliance_snapshots (
  snapshot_id TEXT PRIMARY KEY,
  environment TEXT NOT NULL,
  policy_packs JSONB NOT NULL,
  computed_at TIMESTAMPTZ NOT NULL,
  coverage_percent NUMERIC NOT NULL,
  counts JSONB NOT NULL,
  payload JSONB NOT NULL
);

-- Dashboard datasets cache
CREATE TABLE IF NOT EXISTS dashboard_datasets (
  dataset_id TEXT PRIMARY KEY,
  widget TEXT NOT NULL,
  environment TEXT NOT NULL,
  generated_at TIMESTAMPTZ NOT NULL,
  cache_ttl_seconds INT NOT NULL,
  payload JSONB NOT NULL
);
