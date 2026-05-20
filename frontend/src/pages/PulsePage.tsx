import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorState } from "../components/common/ErrorState";
import { EmptyState } from "../components/common/EmptyState";
import { Icon } from "../components/common/Icon";
import { DocLinkCard } from "../components/publish/DocLinkCard";
import { DraftLinkCard } from "../components/publish/DraftLinkCard";
import { api } from "../services/api";
import type { WeeklyNote } from "../types/pulse";

function PulseContent({ note }: { note: WeeklyNote }) {
  return (
    <div className="space-y-10">
      <div>
        <h2 className="section-label mb-4">Top themes</h2>
        <ul className="space-y-4">
          {note.themes.map((t, i) => (
            <li key={t.id} className="flex items-center gap-4 text-body-lg">
              <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-status-success/15 text-caption font-black text-primary">
                {i + 1}
              </span>
              <span className="font-semibold text-on-surface">{t.headline}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="rounded-xl border border-white/40 bg-surface-bright/80 p-6 backdrop-blur-sm">
        <h2 className="section-label mb-4">What users are saying</h2>
        <ul className="space-y-4">
          {note.quotes.map((q) => (
            <li key={q.theme_id} className="flex gap-3">
              <Icon name="format_quote" className="mt-1 h-5 w-5 shrink-0 text-status-success" />
              <p className="text-body-md italic leading-relaxed text-secondary">{q.paraphrased}</p>
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h2 className="section-label mb-4">Suggested actions</h2>
        <ul className="space-y-4">
          {note.actions.map((a, i) => (
            <li key={a.theme_id} className="flex items-start gap-4">
              <span className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border-2 border-primary text-caption font-black text-primary">
                {i + 1}
              </span>
              <p className="text-body-md font-medium text-on-surface">{a.text}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export function PulsePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["pulse"],
    queryFn: api.pulseLatest,
  });
  const pipeline = useQuery({ queryKey: ["pipeline"], queryFn: api.pipelineStatus });
  const [jsonOpen, setJsonOpen] = useState(false);

  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorState message="Could not load weekly pulse" />;
  if (!data?.note) {
    return <EmptyState title="No pulse yet" description="Run Phase 3 to generate the weekly note." />;
  }

  const withinLimit = data.word_count <= data.max_words;

  return (
    <div className="grid grid-cols-1 items-start gap-10 lg:grid-cols-[1fr_360px]">
      <section className="card-stitch">
        <header className="mb-8 border-b border-border-subtle pb-6">
          <h1 className="text-headline-xl font-extrabold tracking-tight text-on-surface">
            {data.note.title}
          </h1>
        </header>
        <PulseContent note={data.note} />
        <footer className="mt-12 flex justify-end border-t border-border-subtle pt-6">
          <span
            className={`inline-flex items-center gap-2 rounded-xl border px-4 py-2 text-caption font-bold ${
              withinLimit
                ? "border-status-success/20 bg-status-success/15 text-status-success"
                : "border-status-warning/20 bg-status-warning/10 text-status-warning"
            }`}
          >
            {data.word_count} words · {withinLimit ? "within" : "over"} {data.max_words} limit
          </span>
        </footer>
      </section>

      <aside className="space-y-8">
        <div className="card-stitch">
          <h3 className="section-label mb-4">PII status</h3>
          <div className="flex items-center gap-3">
            <Icon name="verified_user" className="h-6 w-6 text-status-success" filled />
            <span className="text-body-md font-bold text-primary">
              {pipeline.data?.pii_passed ? "Passed System Check" : "Blocked"}
            </span>
          </div>
          <p className="mt-2 text-caption text-text-muted">
            Automated scan — no sensitive identifiers in the summary.
          </p>
        </div>

        <div className="space-y-6">
          <h3 className="section-label">Quick links</h3>
          <DocLinkCard state={pipeline.data?.publish_state} />
          <DraftLinkCard state={pipeline.data?.publish_state} />
        </div>

        <div className="card-stitch overflow-hidden p-0">
          <button
            type="button"
            className="flex w-full items-center justify-between p-5 transition-colors hover:bg-on-surface/5"
            onClick={() => setJsonOpen(!jsonOpen)}
          >
            <div className="flex items-center gap-2">
              <Icon name="code" className="h-5 w-5 text-text-muted" />
              <span className="section-label">Structured data</span>
            </div>
            <Icon
              name="expand_more"
              className={`h-5 w-5 transition-transform ${jsonOpen ? "rotate-180" : ""}`}
            />
          </button>
          {jsonOpen && (
            <div className="border-t border-border-subtle bg-surface-container-low p-4">
              <pre className="overflow-x-auto text-caption text-secondary">
                {JSON.stringify(
                  {
                    themes: data.note.themes.map((t) => t.id),
                    quotes: data.note.quotes.length,
                    actions: data.note.actions.length,
                  },
                  null,
                  2,
                )}
              </pre>
            </div>
          )}
        </div>
      </aside>
    </div>
  );
}
