import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import type { RankedTheme } from "../../types/pulse";

const COLORS = ["#00D09C", "#00B88A", "#7DD3B0", "#B8E6D5", "#E9E9EB"];

export function ThemeShareChart({ themes }: { themes: RankedTheme[] }) {
  const data = themes.map((t) => ({
    name: t.label,
    pct: t.pct_of_sample,
  }));

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ left: 8, right: 16 }}>
          <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fontSize: 12 }} />
          <YAxis type="category" dataKey="name" width={90} tick={{ fontSize: 12 }} />
          <Tooltip formatter={(v: number) => `${v}%`} />
          <Bar dataKey="pct" radius={[0, 4, 4, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
