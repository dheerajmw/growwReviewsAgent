import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorState } from "../components/common/ErrorState";
import { Icon } from "../components/common/Icon";
import { MetricCard } from "../components/dashboard/MetricCard";
import { ThemeProgressBars } from "../components/dashboard/ThemeProgressBars";
import { DocLinkCard } from "../components/publish/DocLinkCard";
import { DraftLinkCard } from "../components/publish/DraftLinkCard";
import { api } from "../services/api";
import { formatWeekEnding } from "../lib/format";

export function DashboardPage() {
  const pulse = useQuery({ queryKey: ["pulse"], queryFn: api.pulseLatest });
  const themes = useQuery({ queryKey: ["themes"], queryFn: api.themesRanked });
  const pipeline = useQuery({ queryKey: ["pipeline"], queryFn: api.pipelineStatus });

  if (pulse.isLoading || themes.isLoading) return <LoadingSpinner />;
  if (pulse.isError || themes.isError) return <ErrorState message="Could not load dashboard data" />;

  const topThemes = themes.data?.ranked.slice(0, 3) ?? [];
  const sample = (themes.data?.metadata?.sample_count as number) ?? pipeline.data?.sample_count;
  const normalized = pipeline.data?.normalized_count;
  const wordCount = pulse.data?.word_count ?? 0;
  const maxWords = pulse.data?.max_words ?? 250;
  const piiOk = pipeline.data?.pii_passed ?? false;
  const publishedAt = pipeline.data?.publish_state?.published_at;

  return (
    <>
      <section className="mb-10 flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <h1 className="mb-2 text-headline-xl text-on-surface">This week&apos;s pulse</h1>
          <p className="text-body-lg text-text-muted">Executive summary from mobile app reviews</p>
        </div>
        <Link
          to="/pulse"
          className="group flex items-center gap-1 font-bold text-status-success hover:underline"
        >
          Read full pulse
          <Icon name="arrow_forward" className="h-5 w-5 transition-transform group-hover:translate-x-1" />
        </Link>
      </section>

      <section className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
        <MetricCard
          label="Reviews analyzed"
          value={normalized ?? sample ?? "—"}
          trend={sample ? undefined : undefined}
        />
        <MetricCard
          label="Word count"
          value={<span className="text-status-success">{wordCount}</span>}
          suffix={`/ ${maxWords} max`}
        />
        <MetricCard label="PII gate">
          <span
            className={`inline-flex items-center gap-1.5 rounded-full px-4 py-1.5 text-label-md font-bold ${
              piiOk ? "bg-status-success/10 text-status-success" : "bg-status-error/10 text-status-error"
            }`}
          >
            <Icon name="verified_user" className="h-4 w-4" />
            {piiOk ? "Passed" : "Blocked"}
          </span>
        </MetricCard>
      </section>

      <section className="mb-8 grid grid-cols-1 gap-8 lg:grid-cols-12">
        <div className="card-stitch lg:col-span-7">
          <div className="mb-8 flex items-center justify-between">
            <h2 className="text-headline-md text-on-surface">Top 3 themes</h2>
            <Icon name="more_horiz" className="h-5 w-5 text-text-muted" />
          </div>
          <ThemeProgressBars themes={topThemes} />
        </div>
        <div className="flex flex-col gap-6 lg:col-span-5">
          <DocLinkCard state={pipeline.data?.publish_state} />
          <DraftLinkCard state={pipeline.data?.publish_state} />
        </div>
      </section>

      <div className="flex flex-wrap items-center gap-4 rounded-lg border border-border-subtle bg-white/50 px-6 py-3 text-caption text-text-muted">
        <span className="flex items-center gap-1.5">
          <Icon name="history" className="h-4 w-4" />
          Last pipeline run
          {publishedAt ? ` · ${formatWeekEnding(publishedAt.slice(0, 10))}` : " · —"}
        </span>
        <span className="h-1 w-1 rounded-full bg-border-subtle" />
        <span className="flex items-center gap-1.5">
          <Icon name="schedule" className="h-4 w-4" />
          GitHub Actions scheduled Mondays 06:00 UTC
        </span>
      </div>
    </>
  );
}
