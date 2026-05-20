import { useEffect, useState } from "react";
import type { RankedTheme } from "../../types/pulse";

export function ShareOfVoiceChart({ themes }: { themes: RankedTheme[] }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    const t = requestAnimationFrame(() => setAnimate(true));
    return () => cancelAnimationFrame(t);
  }, [themes]);

  return (
    <div className="space-y-6">
      {themes.map((t) => (
        <div key={t.id} className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-body-lg font-extrabold text-on-surface">{t.label}</span>
            <span className="font-black text-primary">{t.pct_of_sample}%</span>
          </div>
          <div className="h-4 w-full overflow-hidden rounded-full bg-on-surface/5">
            <div
              className="bar-transition neon-glow h-full rounded-full bg-gradient-to-r from-status-success to-primary-fixed"
              style={{ width: animate ? `${t.pct_of_sample}%` : "0%" }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
