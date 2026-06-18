
CREATE TABLE IF NOT EXISTS share_links (
  share_id TEXT PRIMARY KEY,
  report_id TEXT NOT NULL,
  auditor_email TEXT,
  created_by TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL,
  status TEXT NOT NULL, -- active|revoked|expired
  allowed_files JSONB NOT NULL,
  constraints JSONB,
  watermark_enabled BOOLEAN NOT NULL DEFAULT TRUE,
  token_hash TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS portal_sessions (
  session_id TEXT PRIMARY KEY,
  share_id TEXT NOT NULL REFERENCES share_links(share_id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL,
  ip TEXT,
  user_agent TEXT
);

CREATE TABLE IF NOT EXISTS access_attempt_events (
  event_id TEXT PRIMARY KEY,
  share_id TEXT,
  report_id TEXT,
  attempted_at TIMESTAMPTZ NOT NULL,
  ip TEXT,
  user_agent TEXT,
  result TEXT NOT NULL,
  reason TEXT
);

CREATE TABLE IF NOT EXISTS download_events (
  event_id TEXT PRIMARY KEY,
  share_id TEXT,
  report_id TEXT,
  auditor_email TEXT,
  artifact_uri TEXT,
  artifact_sha256 TEXT,
  downloaded_at TIMESTAMPTZ NOT NULL,
  ip TEXT,
  user_agent TEXT,
  bytes BIGINT,
  result TEXT NOT NULL,
  reason TEXT
);
