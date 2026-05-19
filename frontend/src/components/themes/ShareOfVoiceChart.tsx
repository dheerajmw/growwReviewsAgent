import type { RankedTheme } from "../../types/pulse";

const BAR_COLORS = [
  "bg-primary-container",
  "bg-primary-hover",
  "bg-[#00A37A]",
  "bg-[#008F6A]",
  "bg-secondary-fixed-dim",
];

export function ShareOfVoiceChart({ themes }: { themes: RankedTheme[] }) {
  return (
    <div className="space-y-4">
      {themes.map((t, i) => (
        <div key={t.id} className="space-y-1">
          <div className="flex justify-between text-label-md">
            <span>{t.label}</span>
            <span className="font-bold">{t.pct_of_sample}%</span>
          </div>
          <div className="h-2 w-full overflow-hidden rounded-full bg-border-subtle">
            <div
              className={`h-full rounded-full transition-all duration-700 ${BAR_COLORS[i % BAR_COLORS.length]}`}
              style={{ width: `${t.pct_of_sample}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
