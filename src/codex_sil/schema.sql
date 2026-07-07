pragma foreign_keys = on;

create table if not exists settings (
  key text primary key,
  value text not null,
  updated_at text not null default current_timestamp
);

create table if not exists schema_migrations (
  name text primary key,
  applied_at text not null default current_timestamp
);

create table if not exists sessions (
  id integer primary key autoincrement,
  path text not null unique,
  rel_path text not null,
  mtime integer not null,
  size integer not null,
  sha256 text not null,
  status text not null default 'new',
  first_seen_at text not null default current_timestamp,
  last_processed_at text
);

create table if not exists runs (
  id integer primary key autoincrement,
  kind text not null,
  status text not null,
  started_at text not null default current_timestamp,
  finished_at text,
  detail text
);

create table if not exists run_steps (
  id integer primary key autoincrement,
  run_id integer not null references runs(id) on delete cascade,
  name text not null,
  status text not null,
  started_at text not null default current_timestamp,
  finished_at text,
  detail text
);

create table if not exists candidates (
  id integer primary key autoincrement,
  type text not null,
  title text not null,
  text text not null,
  normalized text not null,
  destination text not null,
  rewrite_suggestion text not null,
  status text not null default 'review',
  safety text not null default 'review',
  confidence real not null default 0,
  extractor text not null,
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp,
  unique(type, normalized)
);

create table if not exists recommendations (
  id integer primary key autoincrement,
  candidate_id integer not null unique references candidates(id) on delete cascade,
  recommendation text not null,
  recommendation_en text not null default '',
  recommendation_zh text not null default '',
  recommendation_reason text not null,
  recommendation_reason_en text not null default '',
  recommendation_reason_zh text not null default '',
  suggested_action text not null,
  engine text not null,
  error text not null default '',
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp
);

create table if not exists candidate_analyses (
  id integer primary key autoincrement,
  candidate_id integer not null unique references candidates(id) on delete cascade,
  engine text not null,
  evidence_assessment text not null,
  evidence_assessment_en text not null default '',
  evidence_assessment_zh text not null default '',
  stability text not null,
  scope text not null,
  risk_level text not null,
  conflicts text not null,
  conflicts_en text not null default '',
  conflicts_zh text not null default '',
  rewrite_quality text not null,
  rewrite_quality_en text not null default '',
  rewrite_quality_zh text not null default '',
  recommended_next_step text not null,
  recommended_next_step_en text not null default '',
  recommended_next_step_zh text not null default '',
  error text not null default '',
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp
);

create table if not exists evolution_proposals (
  id integer primary key autoincrement,
  candidate_id integer not null unique references candidates(id) on delete cascade,
  engine text not null,
  target_type text not null,
  target_path text not null,
  proposed_text text not null,
  proposed_text_en text not null default '',
  proposed_text_zh text not null default '',
  rationale text not null,
  rationale_en text not null default '',
  rationale_zh text not null default '',
  verification text not null,
  verification_en text not null default '',
  verification_zh text not null default '',
  requires_manual_approval integer not null default 1,
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp
);

create table if not exists merge_suggestions (
  id integer primary key autoincrement,
  group_key text not null unique,
  primary_candidate_id integer not null references candidates(id) on delete cascade,
  duplicate_candidate_ids text not null,
  recommended_text text not null,
  reason text not null,
  status text not null default 'review',
  created_at text not null default current_timestamp,
  updated_at text not null default current_timestamp
);

create table if not exists candidate_sources (
  id integer primary key autoincrement,
  candidate_id integer not null references candidates(id) on delete cascade,
  session_id integer not null references sessions(id) on delete cascade,
  evidence text not null,
  created_at text not null default current_timestamp,
  unique(candidate_id, session_id, evidence)
);

create table if not exists candidate_fingerprints (
  fingerprint text primary key,
  candidate_id integer not null references candidates(id) on delete cascade,
  created_at text not null default current_timestamp
);

create table if not exists scan_results (
  id integer primary key autoincrement,
  candidate_id integer references candidates(id) on delete cascade,
  severity text not null,
  rule text not null,
  message text not null,
  created_at text not null default current_timestamp
);

create table if not exists reviews (
  id integer primary key autoincrement,
  candidate_id integer not null references candidates(id) on delete cascade,
  status text not null,
  note text,
  rewrite_text text,
  created_at text not null default current_timestamp
);

create table if not exists promotions (
  id integer primary key autoincrement,
  candidate_id integer references candidates(id) on delete set null,
  target_type text not null,
  target_path text not null,
  backup_path text,
  status text not null,
  detail text,
  created_at text not null default current_timestamp
);

create table if not exists skills (
  id integer primary key autoincrement,
  name text not null unique,
  path text not null,
  description text,
  updated_at text not null default current_timestamp
);

create table if not exists skill_usage (
  id integer primary key autoincrement,
  skill_name text not null,
  status text not null default 'success',
  used_at text not null default current_timestamp,
  detail text
);

create table if not exists schedules (
  id integer primary key autoincrement,
  name text not null unique,
  platform text not null,
  command text not null,
  status text not null,
  updated_at text not null default current_timestamp
);

create table if not exists audit_log (
  id integer primary key autoincrement,
  action text not null,
  target text,
  detail text,
  created_at text not null default current_timestamp
);

create table if not exists digests (
  id integer primary key autoincrement,
  run_id integer references runs(id) on delete set null,
  digest_date text not null,
  summary text not null,
  new_candidates integer not null default 0,
  recommended_promotions integer not null default 0,
  risk_items integer not null default 0,
  skill_usage_changes integer not null default 0,
  failed_runs integer not null default 0,
  created_at text not null default current_timestamp
);
