import { Outlet, NavLink } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Sidebar } from "./Sidebar";
import { api } from "../../services/api";
import { formatWeekEnding } from "../../lib/format";

const mobileLinks = [
  { to: "/", label: "Home", end: true },
  { to: "/pulse", label: "Pulse" },
  { to: "/themes", label: "Themes" },
  { to: "/pipeline", label: "Run" },
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
    <div className="min-h-screen bg-page-bg">
      <header className="fixed left-0 top-0 z-50 flex h-16 w-full items-center justify-between border-b border-border-subtle bg-surface-container-lowest px-gutter shadow-sm">
        <span className="text-headline-md font-semibold text-on-surface">Weekly Review Pulse</span>
        <div className="hidden items-center gap-8 md:flex">
          <span className="border-b-2 border-primary py-5 text-label-md font-bold text-primary">
            Week ending {weekLabel}
          </span>
        </div>
        <span
          className={`rounded-full px-3 py-1 text-label-md font-bold ${
            piiOk ? "bg-status-success/10 text-status-success" : "bg-status-error/10 text-status-error"
          }`}
        >
          {piiOk ? "PII cleared ✓" : "PII blocked"}
        </span>
      </header>

      <Sidebar />

      <main className="ml-0 min-h-screen pb-20 pt-16 md:ml-sidebar-width md:pb-12">
        <div className="mx-auto max-w-content px-4 py-6 md:px-gutter">
          <Outlet />
        </div>
      </main>

      <nav className="fixed bottom-0 left-0 right-0 z-40 border-t border-border-subtle bg-surface-container-lowest md:hidden">
        <div className="flex justify-around py-2 text-xs">
          {mobileLinks.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.end}
              className={({ isActive }) =>
                `px-2 py-1 ${isActive ? "font-semibold text-primary" : "text-text-muted"}`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>
      </nav>

      <footer className="ml-0 hidden border-t border-transparent py-8 text-center md:ml-sidebar-width md:block">
        <p className="text-caption text-text-muted">
          Data from public App Store &amp; Play exports · Updated via weekly pipeline
        </p>
      </footer>
    </div>
  );
}
