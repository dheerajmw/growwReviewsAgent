import { Icon } from "../common/Icon";
import type { PhaseStatus, PublishState } from "../../types/pulse";

const PHASE_ICONS: Record<number, "check" | "verified_user" | "description" | "mail" | "schedule"> = {
  4: "verified_user",
  5: "description",
  6: "mail",
  7: "schedule",
};

export function PhaseStepper({
  phases,
  publishState,
}: {
  phases: PhaseStatus[];
  publishState?: PublishState;
}) {
  return (
    <div className="relative space-y-8">
      <div className="stepper-line absolute left-[19px] top-6 z-0 h-[calc(100%-24px)] w-0.5 bg-border-subtle" />
      {phases.map((p) => {
        const icon = PHASE_ICONS[p.id] ?? "check";
        const isScheduler = p.id === 7;
        return (
          <div key={p.id} className="relative z-10 flex gap-6">
            <div
              className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full ${
                p.complete && !isScheduler
                  ? "bg-status-success text-white shadow-success-glow"
                  : isScheduler
                    ? "bg-primary/10 text-primary"
                    : "bg-on-surface/5 text-text-muted"
              }`}
            >
              <Icon name={p.complete || isScheduler ? icon : "schedule"} className="h-5 w-5" />
            </div>
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <h3 className="text-body-lg font-semibold text-on-surface">{p.name}</h3>
              </div>
              {p.id === 4 && p.complete && (
                <div className="mt-1 flex items-center gap-2">
                  <span className="rounded-full bg-status-success/10 px-2 py-0.5 text-label-md text-status-success">
                    ✓ passed
                  </span>
                  <span className="text-body-md text-text-muted">Zero leaks detected</span>
                </div>
              )}
              {p.id === 5 && publishState?.doc_url && (
                <div className="mt-0.5 flex items-center gap-2">
                  <p className="text-body-md text-status-success">✓ complete</p>
                  <a
                    href={publishState.doc_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1 text-label-md text-primary hover:underline"
                  >
                    View Document
                    <Icon name="north_east" className="h-3.5 w-3.5" />
                  </a>
                </div>
              )}
              {p.id !== 4 && p.id !== 5 && (
                <p
                  className={`mt-0.5 text-body-md ${
                    p.complete ? "text-status-success" : "text-text-muted"
                  }`}
                >
                  {p.complete ? "✓ complete" : "Pending"}
                  {isScheduler && p.complete ? " · GitHub Actions" : ""}
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
