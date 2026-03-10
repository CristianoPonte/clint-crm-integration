-- Schema minimo para historico de SLA (PostgreSQL)

CREATE TABLE IF NOT EXISTS sla_rules (
  id BIGSERIAL PRIMARY KEY,
  origin_id TEXT NOT NULL,
  from_stage_id TEXT NOT NULL,
  from_stage_label TEXT NOT NULL,
  to_stage_id TEXT NOT NULL,
  to_stage_label TEXT NOT NULL,
  target_minutes INTEGER NOT NULL CHECK (target_minutes >= 0),
  priority TEXT NOT NULL DEFAULT 'medium',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (origin_id, from_stage_id, to_stage_id)
);

CREATE TABLE IF NOT EXISTS sla_user_routes (
  id BIGSERIAL PRIMARY KEY,
  user_id TEXT NOT NULL UNIQUE,
  seller_label TEXT NOT NULL,
  seller_email TEXT,
  slack_channel TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sla_runs (
  id BIGSERIAL PRIMARY KEY,
  run_id TEXT NOT NULL UNIQUE,
  run_at TIMESTAMPTZ NOT NULL,
  timezone TEXT NOT NULL,
  origin_id TEXT NOT NULL,
  total_open INTEGER NOT NULL DEFAULT 0,
  total_overdue INTEGER NOT NULL DEFAULT 0,
  groups_count INTEGER NOT NULL DEFAULT 0,
  messages_sent INTEGER NOT NULL DEFAULT 0,
  messages_failed INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sla_overdue_snapshots (
  id BIGSERIAL PRIMARY KEY,
  run_id TEXT NOT NULL REFERENCES sla_runs(run_id),
  deal_id TEXT NOT NULL,
  origin_id TEXT NOT NULL,
  stage_id TEXT NOT NULL,
  stage_label TEXT NOT NULL,
  deal_status TEXT,
  close_bucket TEXT,
  user_id TEXT,
  seller_label TEXT,
  contact_id TEXT,
  contact_name TEXT,
  contact_email TEXT,
  latest_meeting_datetime TIMESTAMPTZ,
  latest_meeting_link TEXT,
  reference_ts TIMESTAMPTZ NOT NULL,
  age_minutes INTEGER NOT NULL,
  target_minutes INTEGER NOT NULL,
  overdue_minutes INTEGER NOT NULL,
  priority TEXT NOT NULL DEFAULT 'medium',
  payload_json JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sla_overdue_snapshots_run_id ON sla_overdue_snapshots (run_id);
CREATE INDEX IF NOT EXISTS idx_sla_overdue_snapshots_deal_id ON sla_overdue_snapshots (deal_id);
CREATE INDEX IF NOT EXISTS idx_sla_overdue_snapshots_user_id ON sla_overdue_snapshots (user_id);
CREATE INDEX IF NOT EXISTS idx_sla_overdue_snapshots_stage_id ON sla_overdue_snapshots (stage_id);
