import { Icon } from "../common/Icon";
import type { RankedTheme } from "../../types/pulse";
import { lowRatingPct } from "../../lib/format";

export function ThemeDetailDrawer({
  theme,
  open,
  onClose,
}: {
  theme: RankedTheme | null;
  open: boolean;
  onClose: () => void;
}) {
  if (!theme) return null;
  const lowPct = lowRatingPct(theme);

  return (
    <>
      <div
        className={`fixed inset-0 z-[90] bg-black/20 transition-opacity ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
        onClick={onClose}
        aria-hidden
      />
      <aside
        className={`fixed inset-y-0 right-0 z-[100] flex w-full max-w-[400px] flex-col bg-card-surface shadow-elevated transition-transform duration-300 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between border-b border-border-subtle px-6 py-6">
          <h2 className="text-headline-md text-on-surface">{theme.label}</h2>
          <button
            type="button"
            onClick={onClose}
            className="flex h-8 w-8 items-center justify-center rounded-full hover:bg-surface-bright"
            aria-label="Close"
          >
            <Icon name="close" className="h-5 w-5" />
          </button>
        </div>
        <div className="flex flex-1 flex-col gap-8 overflow-y-auto p-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-lg bg-surface-bright p-4">
              <p className="mb-1 text-caption text-text-muted">Impact score</p>
              <p className="text-headline-md font-bold text-primary">{theme.score.toFixed(0)}</p>
            </div>
            <div className="rounded-lg bg-surface-bright p-4">
              <p className="mb-1 text-caption text-text-muted">Low ratings</p>
              <p className={`text-headline-md font-bold ${lowPct > 20 ? "text-status-error" : "text-on-surface"}`}>
                {lowPct}%
              </p>
            </div>
          </div>
          <div>
            <h4 className="section-label mb-3">Overview</h4>
            <p className="text-body-md italic text-text-muted">
              {theme.review_count} reviews in sample ({theme.pct_of_sample}% share). Paraphrased
              summaries only — no raw reviewer text or identifiers.
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}
