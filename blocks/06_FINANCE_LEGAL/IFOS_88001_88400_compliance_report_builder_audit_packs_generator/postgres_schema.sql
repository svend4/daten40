
-- Report build jobs
CREATE TABLE IF NOT EXISTS report_jobs (
  report_id TEXT PRIMARY KEY,
  request_payload JSONB NOT NULL,
  status TEXT NOT NULL,
  progress NUMERIC NOT NULL DEFAULT 0,
  message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Output manifest
CREATE TABLE IF NOT EXISTS report_manifests (
  report_id TEXT PRIMARY KEY,
  manifest JSONB NOT NULL,
  generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
