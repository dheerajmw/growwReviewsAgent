import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorState } from "../components/common/ErrorState";
import { EmptyState } from "../components/common/EmptyState";
import { Icon } from "../components/common/Icon";
import { ShareOfVoiceChart } from "../components/themes/ShareOfVoiceChart";
import { ThemeRankList } from "../components/themes/ThemeRankList";
import { ThemeDetailDrawer } from "../components/themes/ThemeDetailDrawer";
import { api } from "../services/api";
import type { RankedTheme } from "../types/pulse";

export function ThemesPage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["themes"],
    queryFn: api.themesRanked,
  });
  const [selected, setSelected] = useState<RankedTheme | null>(null);

  if (isLoading) return <LoadingSpinner />;
  if (isError) return <ErrorState message="Could not load themes" />;
  if (!data?.ranked?.length) {
    return <EmptyState title="No themes" description="Run Phase 2 clustering first." />;
  }

  const sample = data.metadata?.sample_count as number | undefined;

  return (
    <>
      <section className="mb-6 flex flex-col gap-1">
        <h1 className="text-headline-xl text-on-surface">Review themes</h1>
        <p className="text-body-md text-text-muted">
          Up to 5 themes from sampled App Store &amp; Play reviews
        </p>
      </section>

      <section className="mb-6 grid grid-cols-1 gap-6 md:grid-cols-10">
        <div className="card-stitch md:col-span-6">
          <div className="mb-6 flex items-center justify-between">
            <h3 className="text-body-md text-text-muted">Share of voice</h3>
            <Icon name="info" className="h-5 w-5 text-text-muted" />
          </div>
          <ShareOfVoiceChart themes={data.ranked} />
        </div>
        <div className="flex flex-col gap-6 md:col-span-4">
          <div className="card-stitch flex flex-1 flex-col justify-center">
            <h3 className="mb-2 text-body-md text-text-muted">Sample size</h3>
            <div className="flex items-baseline gap-2">
              <span className="text-headline-xl text-primary">{sample ?? "—"}</span>
              <span className="text-body-md text-text-muted">reviews</span>
            </div>
          </div>
          <div className="card-stitch flex flex-1 flex-col justify-center">
            <h3 className="mb-4 text-body-md text-text-muted">Stores</h3>
            <div className="flex flex-wrap gap-6">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-container-low">
                  <Icon name="shop" className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <span className="text-label-md font-bold">Play Store</span>
                  <p className="text-caption text-text-muted">Public export</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-container-low">
                  <Icon name="phone_iphone" className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <span className="text-label-md font-bold">App Store</span>
                  <p className="text-caption text-text-muted">Public export</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="overflow-hidden rounded-xl border border-border-subtle bg-card-surface shadow-card">
        <div className="flex items-center justify-between border-b border-border-subtle px-card-padding py-4">
          <h3 className="text-headline-md">Ranked themes</h3>
        </div>
        <ThemeRankList themes={data.ranked} onSelect={setSelected} />
      </section>

      <ThemeDetailDrawer theme={selected} open={!!selected} onClose={() => setSelected(null)} />
    </>
  );
}
