import { useState } from "react";
import { Outlet, NavLink } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Sidebar } from "./Sidebar";
import { Icon } from "../common/Icon";
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
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const { data: pipeline } = useQuery({
    queryKey: ["pipeline"],
    queryFn: api.pipelineStatus,
  });
  const weekRaw = pipeline?.publish_state?.week_ending;
  const weekLabel = formatWeekEnding(weekRaw);
  const piiOk = pipeline?.pii_passed ?? false;

  return (
    <div className="flex min-h-screen flex-col">
      <header className="app-header glass-nav flex h-20 w-full shrink-0 items-center gap-4 px-4 md:px-gutter">
        <button
          type="button"
          onClick={() => setMobileNavOpen(true)}
          className="inline-flex items-center justify-center rounded-xl border border-border-subtle bg-white p-2.5 text-primary shadow-sm transition-colors hover:bg-primary/5 md:hidden"
          aria-label="Open navigation menu"
        >
          <Icon name="menu" className="h-6 w-6" />
        </button>
        <span className="text-headline-md font-extrabold tracking-tight text-on-surface">
          Review Pulse
        </span>
        <div className="hidden flex-1 items-center justify-center md:flex">
          <span className="text-label-md font-semibold uppercase tracking-wider text-on-surface/60">
            Week ending {weekLabel}
          </span>
        </div>
        <span
          className={`ml-auto rounded-full border px-4 py-1.5 text-label-md font-bold ${
            piiOk
              ? "border-status-success/20 bg-status-success/15 text-status-success"
              : "border-status-error/20 bg-status-error/10 text-status-error"
          }`}
        >
          {piiOk ? "PII cleared ✓" : "PII blocked"}
        </span>
      </header>

      <div className="flex min-h-0 flex-1">
        <Sidebar mobileOpen={mobileNavOpen} onClose={() => setMobileNavOpen(false)} />

        <div className="flex min-w-0 flex-1 flex-col">
          <main className="flex-1 overflow-y-auto pb-24 md:pb-8">
            <div className="mx-auto max-w-content px-4 py-6 md:px-gutter">
              <Outlet />
            </div>
          </main>

          <footer className="hidden shrink-0 py-8 text-center md:block">
            <p className="text-caption font-medium uppercase tracking-widest text-text-muted">
              Data sourced from public App Store &amp; Play exports · Built with Weekly Pipeline
            </p>
          </footer>
        </div>
      </div>

      <nav className="glass-nav fixed bottom-0 left-0 right-0 z-40 md:hidden">
        <div className="flex justify-around py-2 text-xs">
          {mobileLinks.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              onClick={() => setMobileNavOpen(false)}
              className={({ isActive }) =>
                `px-2 py-1 ${isActive ? "font-bold text-primary" : "text-text-muted"}`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  );
}
