export function formatWeekEnding(iso?: string): string {
  if (!iso || iso === "—") return "—";
  const d = new Date(iso + "T12:00:00");
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
}

export function lowRatingPct(theme: { review_count: number; low_rating_count: number }): number {
  if (!theme.review_count) return 0;
  return Math.round((theme.low_rating_count / theme.review_count) * 100);
}
