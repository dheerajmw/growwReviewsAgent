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
  const reviewCount = normalized ?? sample ?? "—";

  return (
    <>
      <section className="mb-12 flex flex-col justify-between gap-6 md:flex-row md:items-end">
        <div>
          <h1 className="mb-3 text-headline-xl font-extrabold tracking-tight text-on-surface">
            This week&apos;s pulse
          </h1>
          <p className="text-body-lg text-text-muted">Executive summary from mobile app reviews</p>
        </div>
        <Link to="/pulse" className="btn-primary group shrink-0">
          Read full pulse
          <Icon
            name="arrow_forward"
            className="h-5 w-5 transition-transform group-hover:translate-x-1"
          />
        </Link>
      </section>

      <section className="mb-12 grid grid-cols-1 gap-8 md:grid-cols-3">
        <MetricCard label="Reviews analyzed" value={reviewCount} />
        <MetricCard
          label="Word count"
          value={wordCount}
          suffix={`/ ${maxWords}`}
          valueClassName="text-status-success"
        />
        <MetricCard label="PII gate">
          <span className="inline-flex items-center gap-2 rounded-xl border border-status-success/20 bg-status-success/15 px-5 py-2.5 text-body-md font-bold text-status-success">
            <Icon name="verified_user" className="h-5 w-5" />
            {piiOk ? "Passed System Check" : "Blocked"}
          </span>
        </MetricCard>
      </section>

      <section className="mb-12 grid grid-cols-1 gap-10 lg:grid-cols-12">
        <div className="card-stitch lg:col-span-7">
          <ThemeProgressBars themes={topThemes} />
        </div>
        <div className="flex flex-col gap-8 lg:col-span-5">
          <DocLinkCard state={pipeline.data?.publish_state} />
          <DraftLinkCard state={pipeline.data?.publish_state} />
        </div>
      </section>

      <div className="info-strip">
        <span className="flex items-center gap-2">
          <Icon name="history" className="h-[18px] w-[18px]" />
          Last pipeline run
          {publishedAt ? ` · ${formatWeekEnding(publishedAt.slice(0, 10))}` : " · —"}
        </span>
        <span className="hidden h-1.5 w-1.5 rounded-full bg-on-surface/20 md:block" />
        <span className="flex items-center gap-2">
          <Icon name="schedule" className="h-[18px] w-[18px]" />
          GitHub Actions scheduled Mondays 06:00 UTC
        </span>
      </div>
    </>
  );
}
