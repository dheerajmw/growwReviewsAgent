import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorState } from "../components/common/ErrorState";
import { EmptyState } from "../components/common/EmptyState";
import { Icon } from "../components/common/Icon";
import { api } from "../services/api";
import type { WeeklyNote } from "../types/pulse";

function PulseContent({ note }: { note: WeeklyNote }) {
  return (
    <div className="space-y-10">
      <div>
        <h2 className="section-label mb-4">Top themes</h2>
        <ul className="space-y-3">
          {note.themes.map((t, i) => (
            <li key={t.id} className="flex items-center justify-between text-body-lg">
              <div className="flex items-center gap-4">
                <span className="flex h-6 w-6 items-center justify-center rounded bg-primary-container/10 text-caption font-bold text-primary">
                  {i + 1}
                </span>
                <span>{t.headline}</span>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <div className="rounded-lg border-l-4 border-primary/20 bg-surface-bright p-6">
        <h2 className="section-label mb-4">What users are saying</h2>
        <ul className="space-y-4">
          {note.quotes.map((q) => (
            <li key={q.theme_id} className="flex gap-3">
              <Icon name="format_quote" className="mt-1 h-5 w-5 shrink-0 text-primary-container" />
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
              <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-primary text-caption font-bold text-primary">
                {i + 1}
              </span>
              <p className="text-body-md text-on-surface">{a.text}</p>
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
  const publish = pipeline.data?.publish_state;
  const docUrl = publish?.doc_url;
  const draftUrl = publish?.draft_url ?? "https://mail.google.com/mail/u/0/#drafts";

  return (
    <div className="grid grid-cols-1 items-start gap-gutter md:grid-cols-[1fr_320px]">
      <section className="card-stitch">
        <header className="mb-8 border-b border-border-subtle pb-6">
          <h1 className="text-headline-xl text-on-surface">{data.note.title}</h1>
        </header>
        <PulseContent note={data.note} />
        <footer className="mt-12 flex justify-end border-t border-border-subtle pt-6">
          <span className="inline-flex items-center gap-1 rounded-full bg-status-success/10 px-3 py-1 text-caption font-bold text-primary">
            {data.word_count} words · {withinLimit ? "within" : "over"} {data.max_words} limit
          </span>
        </footer>
      </section>

      <aside className="space-y-6">
        <div className="card-stitch p-6">
          <h3 className="section-label mb-4">PII status</h3>
          <div className="flex items-center gap-3 text-primary">
            <Icon name="check_circle" className="h-5 w-5" filled />
            <span className="text-body-md font-bold">
              {pipeline.data?.pii_passed ? "Cleared for publish" : "Blocked"}
            </span>
          </div>
          <p className="mt-2 text-caption text-text-muted">
            Automated scan — no sensitive identifiers in the summary.
          </p>
        </div>

        <div className="card-stitch p-6">
          <h3 className="section-label mb-4">Quick links</h3>
          <div className="space-y-3">
            {docUrl ? (
              <a
                href={docUrl}
                target="_blank"
                rel="noreferrer"
                className="group flex w-full items-center justify-between rounded-lg border border-border-subtle p-3 transition-colors hover:bg-surface-bright"
              >
                <div className="flex items-center gap-3">
                  <Icon name="description" className="h-5 w-5 text-[#4285F4]" />
                  <span className="text-body-md font-medium">Google Doc</span>
                </div>
                <Icon name="north_east" className="h-4 w-4 text-text-muted transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
              </a>
            ) : null}
            <a
              href={draftUrl}
              target="_blank"
              rel="noreferrer"
              className="group flex w-full items-center justify-between rounded-lg border border-border-subtle p-3 transition-colors hover:bg-surface-bright"
            >
              <div className="flex items-center gap-3">
                <Icon name="mail" className="h-5 w-5 text-[#EA4335]" />
                <span className="text-body-md font-medium">Gmail Draft</span>
              </div>
              <Icon name="north_east" className="h-4 w-4 text-text-muted transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            </a>
          </div>
        </div>

        <div className="overflow-hidden rounded-xl border border-border-subtle bg-card-surface">
          <button
            type="button"
            className="flex w-full items-center justify-between p-4 hover:bg-surface-bright"
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
