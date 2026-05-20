import { Outlet, NavLink } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Sidebar } from "./Sidebar";
import { api } from "../../services/api";
import { formatWeekEnding } from "../../lib/format";

const mobileLinks = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/pulse", label: "Pulse" },
  { to: "/themes", label: "Themes" },
  { to: "/pipeline", label: "Pipeline" },
  { to: "/settings", label: "Settings" },
];

export function AppShell() {
  const { data: pipeline } = useQuery({
    queryKey: ["pipeline"],
    queryFn: api.pipelineStatus,
  });
  const weekRaw = pipeline?.publish_state?.week_ending;
  const weekLabel = formatWeekEnding(weekRaw);
  const piiOk = pipeline?.pii_passed ?? false;

  return (
    <div className="min-h-screen">
      <header className="glass-nav fixed left-0 top-0 z-50 flex h-20 w-full items-center justify-between px-gutter">
        <span className="text-headline-md font-extrabold tracking-tight text-on-surface">
          Review Pulse
        </span>
        <div className="hidden items-center gap-8 md:flex">
          <span className="text-label-md font-semibold uppercase tracking-wider text-on-surface/60">
            Week ending {weekLabel}
          </span>
        </div>
        <span
          className={`rounded-full border px-4 py-1.5 text-label-md font-bold ${
            piiOk
              ? "border-status-success/20 bg-status-success/15 text-status-success"
              : "border-status-error/20 bg-status-error/10 text-status-error"
          }`}
        >
          {piiOk ? "PII cleared ✓" : "PII blocked"}
        </span>
      </header>

      <Sidebar />

      <main className="ml-0 min-h-screen pb-24 pt-32 md:ml-sidebar-width md:pb-16">
        <div className="mx-auto max-w-content px-4 md:px-gutter">
          <Outlet />
        </div>
      </main>

      <nav className="glass-nav fixed bottom-0 left-0 right-0 z-40 md:hidden">
        <div className="flex justify-around py-2 text-xs">
          {mobileLinks.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              className={({ isActive }) =>
                `px-2 py-1 ${isActive ? "font-bold text-primary" : "text-text-muted"}`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>
      </nav>

      <footer className="ml-0 py-12 text-center md:ml-sidebar-width">
        <p className="text-caption font-medium uppercase tracking-widest text-text-muted">
          Data sourced from public App Store &amp; Play exports · Built with Weekly Pipeline
        </p>
      </footer>
    </div>
  );
}
