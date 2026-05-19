import type { RankedTheme } from "../../types/pulse";
import { lowRatingPct } from "../../lib/format";

export function ThemeRankList({
  themes,
  onSelect,
}: {
  themes: RankedTheme[];
  onSelect?: (t: RankedTheme) => void;
}) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="bg-surface-bright">
            <th className="px-6 py-4 text-label-md text-text-muted">Rank</th>
            <th className="px-6 py-4 text-label-md text-text-muted">Theme</th>
            <th className="px-6 py-4 text-label-md text-text-muted">Reviews</th>
            <th className="px-6 py-4 text-label-md text-text-muted">% of sample</th>
            <th className="px-6 py-4 text-label-md text-text-muted">Low ratings (1–2★)</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-border-subtle text-body-md">
          {themes.map((t, i) => {
            const lowPct = lowRatingPct(t);
            const top3 = i < 3;
            return (
              <tr
                key={t.id}
                className="cursor-pointer transition-colors hover:bg-surface-container-low"
                onClick={() => onSelect?.(t)}
              >
                <td
                  className={`px-6 py-4 font-bold ${top3 ? "border-l-4 border-primary" : "text-text-muted"}`}
                >
                  #{i + 1}
                </td>
                <td className="px-6 py-4 font-medium">{t.label}</td>
                <td className="px-6 py-4">{t.review_count}</td>
                <td className="px-6 py-4">{t.pct_of_sample}%</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <div className="h-1.5 w-24 rounded-full bg-border-subtle">
                      <div
                        className="h-full rounded-full bg-status-error"
                        style={{ width: `${Math.min(lowPct, 100)}%` }}
                      />
                    </div>
                    <span className="text-caption font-bold text-status-error">{lowPct}%</span>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
