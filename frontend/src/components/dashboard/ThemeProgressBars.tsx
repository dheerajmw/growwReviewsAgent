import type { RankedTheme } from "../../types/pulse";

const BAR_COLORS = ["bg-status-success", "bg-primary-hover", "bg-[#00A37A]"];

export function ThemeProgressBars({ themes }: { themes: RankedTheme[] }) {
  return (
    <div className="space-y-8">
      {themes.slice(0, 3).map((t, i) => (
        <div key={t.id} className="space-y-2">
          <div className="flex items-center justify-between text-body-md">
            <span className="font-semibold">{t.label}</span>
            <span className="text-text-muted">{t.pct_of_sample}%</span>
          </div>
          <div className="h-3 w-full overflow-hidden rounded-full bg-border-subtle">
            <div
              className={`h-full rounded-full transition-all duration-700 ${BAR_COLORS[i] ?? "bg-status-success"}`}
              style={{ width: `${t.pct_of_sample}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
