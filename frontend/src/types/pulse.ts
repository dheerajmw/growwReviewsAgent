export interface ThemeLine {
  id: string;
  headline: string;
}

export interface Quote {
  theme_id: string;
  paraphrased: string;
  source_rating?: number;
}

export interface Action {
  theme_id: string;
  text: string;
}

export interface WeeklyNote {
  title: string;
  themes: ThemeLine[];
  quotes: Quote[];
  actions: Action[];
  metadata?: Record<string, unknown>;
}

export interface RankedTheme {
  id: string;
  label: string;
  review_count: number;
  low_rating_count: number;
  score: number;
  pct_of_sample: number;
}

export interface PublishState {
  doc_id?: string;
  doc_url?: string;
  draft_id?: string;
  draft_url?: string;
  draft_to?: string;
  published_at?: string;
  draft_created_at?: string;
  week_ending?: string;
}

export interface PhaseStatus {
  id: number;
  name: string;
  complete: boolean;
}

export interface PipelineStatus {
  pii_passed: boolean;
  blockers?: { publish_blocked?: boolean; findings?: unknown[] };
  phases: PhaseStatus[];
  normalized_count?: number;
  sample_count?: number;
  publish_state?: PublishState;
  scheduler?: { cron: string; description: string };
}
