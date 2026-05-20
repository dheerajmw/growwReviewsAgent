import { NavLink } from "react-router-dom";
import { Icon } from "../common/Icon";

const links = [
  { to: "/", label: "Dashboard", icon: "dashboard" as const, end: true },
  { to: "/pulse", label: "Weekly Pulse", icon: "analytics" as const },
  { to: "/themes", label: "Themes", icon: "category" as const },
  { to: "/pipeline", label: "Pipeline", icon: "account_tree" as const },
  { to: "/settings", label: "Settings", icon: "settings" as const },
];

export function Sidebar() {
  return (
    <aside className="glass-nav fixed left-0 top-20 z-40 hidden h-[calc(100vh-80px)] w-sidebar-width flex-col border-r border-white/20 py-8 md:flex">
      <div className="mb-10 px-8">
        <div className="flex items-center gap-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-status-success text-xl font-black text-white shadow-logo-glow">
            G
          </div>
          <div>
            <p className="text-body-lg font-bold text-on-surface">App Reviews</p>
            <p className="text-caption text-text-muted">Groww Platform</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 space-y-1 px-4">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.end}
            className={({ isActive }) => (isActive ? "nav-active" : "nav-item")}
          >
            <Icon name={l.icon} className="h-5 w-5" />
            <span>{l.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
