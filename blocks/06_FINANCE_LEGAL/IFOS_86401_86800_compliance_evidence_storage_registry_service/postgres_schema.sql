
-- Evidence Registry (append-only)
CREATE TABLE IF NOT EXISTS evidence_events (
  event_id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL, -- APPEND, SUPERSEDE, HOLD, RELEASE_HOLD, TAG
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  actor TEXT NOT NULL,
  reason TEXT,
  supersedes_event_id TEXT,
  evidence_id TEXT,
  artifact_sha256 TEXT,
  artifact_uri TEXT,
  payload JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_evidence_events_evidence_id ON evidence_events(evidence_id);
CREATE INDEX IF NOT EXISTS idx_evidence_events_artifact_sha256 ON evidence_events(artifact_sha256);
CREATE INDEX IF NOT EXISTS idx_evidence_events_created_at ON evidence_events(created_at);

-- Materialized view example (optional)
-- CREATE MATERIALIZED VIEW evidence_current AS ...
