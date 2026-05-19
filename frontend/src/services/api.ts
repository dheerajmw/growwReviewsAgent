const BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
  return res.json() as Promise<T>;
}

export const api = {
  health: () => get<{ status: string }>("/api/v1/health"),
  pulseLatest: () =>
    get<{
      note: import("../types/pulse").WeeklyNote | null;
      markdown: string;
      word_count: number;
      max_words: number;
    }>("/api/v1/pulse/latest"),
  pulseWeeks: () => get<{ weeks: string[] }>("/api/v1/pulse/weeks"),
  themesRanked: () =>
    get<{ ranked: import("../types/pulse").RankedTheme[]; metadata: Record<string, unknown> }>(
      "/api/v1/themes/ranked",
    ),
  themesClusters: () =>
    get<{ themes: { id: string; label: string; review_count: number }[] }>(
      "/api/v1/themes/clusters",
    ),
  pipelineStatus: () => get<import("../types/pulse").PipelineStatus>("/api/v1/pipeline/status"),
  publishState: () => get<import("../types/pulse").PublishState>("/api/v1/publish/state"),
};
