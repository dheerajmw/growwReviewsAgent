import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { Icon } from "../components/common/Icon";
import { api } from "../services/api";

function ConfigRow({
  label,
  hint,
  status,
  ok,
}: {
  label: string;
  hint: string;
  status: string;
  ok: boolean;
}) {
  return (
    <div className="flex items-center justify-between border-b border-border-subtle py-2 last:border-0">
      <div>
        <span className="text-body-md text-on-surface">{label}</span>
        <p className="text-caption italic text-text-muted">{hint}</p>
      </div>
      <div
        className={`flex items-center gap-2 rounded-full px-3 py-1 ${
          ok ? "bg-status-success/10" : "bg-secondary/10"
        }`}
      >
        <span className={`h-2 w-2 rounded-full ${ok ? "bg-status-success" : "bg-text-muted"}`} />
        <span className={`text-label-md ${ok ? "text-primary" : "text-text-muted"}`}>{status}</span>
      </div>
    </div>
  );
}

export function SettingsPage() {
  const health = useQuery({ queryKey: ["health"], queryFn: api.health });
  const publish = useQuery({ queryKey: ["publish"], queryFn: api.publishState });
  const weeks = useQuery({ queryKey: ["weeks"], queryFn: api.pulseWeeks });
  const [apiBase, setApiBase] = useState(import.meta.env.VITE_API_BASE_URL ?? "(proxy /api)");

  if (health.isLoading) return <LoadingSpinner />;

  const weekList = weeks.data?.weeks ?? [];

  return (
    <div className="mx-auto max-w-[800px] space-y-6">
      <header className="mb-8">
        <h1 className="text-headline-xl font-extrabold tracking-tight text-on-surface">Settings</h1>
        <p className="text-body-md text-text-muted">
          Manage your dashboard preferences and data pipeline configuration.
        </p>
      </header>

      <section className="card-stitch">
        <h3 className="mb-1 text-body-lg font-semibold">Week selection</h3>
        <p className="mb-4 text-caption text-text-muted">Switch historical weekly pulses when available</p>
        <select
          className="w-full max-w-md appearance-none rounded-lg border border-border-subtle bg-surface-bright px-4 py-2.5 text-body-md outline-none focus:border-primary focus:ring-2 focus:ring-primary"
          defaultValue={weekList[0] ?? ""}
        >
          {weekList.length ? (
            weekList.map((w) => (
              <option key={w} value={w}>
                Week ending {w}
              </option>
            ))
          ) : (
            <option>—</option>
          )}
        </select>
      </section>

      <section className="card-stitch">
        <h3 className="mb-6 text-body-lg font-semibold">Configuration status</h3>
        <div className="space-y-4">
          <ConfigRow
            label="Google Doc ID"
            hint="Read-only connection string"
            status={publish.data?.doc_id ? "Configured ✓" : "Not set"}
            ok={!!publish.data?.doc_id}
          />
          <ConfigRow
            label="Gmail draft recipient"
            hint="Automated weekly reporting stream"
            status={publish.data?.draft_id ? "Configured ✓" : "Not set"}
            ok={!!publish.data?.draft_id}
          />
          <ConfigRow
            label="MCP server"
            hint="Contextual data processing engine"
            status="Connected"
            ok
          />
          <ConfigRow
            label="Groq API"
            hint="LLM processing backend"
            status="Not shown / server-side only"
            ok={false}
          />
          <ConfigRow
            label="BFF health"
            hint="Phase 8 read API"
            status={health.data?.status === "ok" ? "Connected" : "Unknown"}
            ok={health.data?.status === "ok"}
          />
        </div>
      </section>

      <section className="card-stitch">
        <h3 className="mb-1 text-body-lg font-semibold">Developer</h3>
        <p className="mb-4 text-caption text-text-muted">Local BFF for development</p>
        <label className="mb-2 block text-label-md text-secondary">API base URL</label>
        <input
          type="text"
          className="w-full rounded-lg border border-border-subtle bg-surface-bright px-4 py-2.5 text-body-md outline-none focus:border-primary focus:ring-2 focus:ring-primary"
          value={apiBase}
          onChange={(e) => setApiBase(e.target.value)}
          placeholder="http://localhost:8080"
          readOnly
        />
      </section>

      <section className="flex items-center gap-8 px-4 py-2">
        <a
          href="https://github.com/dheerajmw/growwReviewsAgent/blob/main/doc/runbook.md"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 text-label-md font-medium text-status-success hover:underline"
        >
          <Icon name="menu_book" className="h-4 w-4" />
          Runbook
        </a>
        <a
          href="https://github.com/dheerajmw/growwReviewsAgent"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 text-label-md font-medium text-status-success hover:underline"
        >
          <Icon name="code" className="h-4 w-4" />
          GitHub repository
        </a>
      </section>
    </div>
  );
}
