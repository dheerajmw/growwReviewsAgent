import { useQuery } from "@tanstack/react-query";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { ErrorState } from "../components/common/ErrorState";
import { Icon } from "../components/common/Icon";
import { PhaseStepper } from "../components/pipeline/PhaseStepper";
import { api } from "../services/api";

export function PipelinePage() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["pipeline"],
    queryFn: api.pipelineStatus,
  });

  if (isLoading) return <LoadingSpinner />;
  if (isError || !data) return <ErrorState message="Could not load pipeline status" />;

  const blocked = data.blockers && (data.blockers as { publish_blocked?: boolean }).publish_blocked;

  return (
    <>
      <header className="mb-8">
        <h1 className="text-headline-xl font-extrabold tracking-tight text-on-surface">Pipeline status</h1>
        <p className="mt-1 text-body-md text-text-muted">
          Phases 1–7 · automated refresh via GitHub Actions
        </p>
      </header>

      <div className="grid grid-cols-1 items-start gap-gutter lg:grid-cols-12">
        <div className="card-stitch lg:col-span-8">
          <PhaseStepper phases={data.phases} publishState={data.publish_state} />
        </div>

        <div className="space-y-gutter lg:col-span-4">
          <div className="card-stitch">
            <div className="mb-4 flex items-start gap-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-bright text-secondary">
                <Icon name="calendar_month" className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-body-lg font-semibold">Scheduler</h3>
                <p className="text-body-md text-text-muted">
                  {data.scheduler?.description ?? "Monday 06:00 UTC"}
                </p>
              </div>
            </div>
            <a
              href="https://github.com/dheerajmw/growwReviewsAgent/actions"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-2 text-label-md font-bold text-primary hover:text-primary-hover"
            >
              View GitHub Actions
              <Icon name="open_in_new" className="h-4 w-4" />
            </a>
          </div>

          <div className="card-stitch">
            <h3 className="section-label mb-4">Admin controls</h3>
            <div className="space-y-3">
              <button
                type="button"
                className="flex w-full items-center justify-center gap-2 rounded-xl border-2 border-primary py-3 text-body-md font-bold text-primary transition-all hover:bg-primary hover:text-white"
                onClick={() => window.location.reload()}
              >
                <Icon name="refresh" className="h-4 w-4" />
                Refresh data
              </button>
              <button
                type="button"
                disabled
                className="flex w-full cursor-not-allowed items-center justify-center gap-2 rounded-lg border border-border-subtle bg-page-bg py-2.5 text-body-md font-bold text-text-muted"
              >
                <Icon name="block" className="h-4 w-4" />
                Emergency Stop
              </button>
            </div>
          </div>

          {blocked && (
            <div className="rounded-xl border border-error/20 bg-error-container/40 p-card-padding">
              <div className="flex gap-3">
                <Icon name="warning" className="h-5 w-5 shrink-0 text-status-error" />
                <div>
                  <p className="text-body-md font-semibold text-on-error-container">
                    PII blockers detected
                  </p>
                  <p className="mt-1 text-caption text-on-error-container/80">
                    Publish is blocked until PII gate passes.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
