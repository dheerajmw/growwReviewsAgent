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
    <aside className="fixed left-0 top-16 z-40 hidden h-[calc(100vh-64px)] w-sidebar-width flex-col border-r border-border-subtle bg-surface-container-lowest py-4 md:flex">
      <div className="mb-8 px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-status-success font-bold text-white">
            G
          </div>
          <div>
            <p className="text-body-lg font-semibold text-on-surface">App Reviews</p>
            <p className="text-label-md text-text-muted">Weekly Review Pulse</p>
          </div>
        </div>
      </div>
      <nav className="flex-1">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.end}
            className={({ isActive }) =>
              isActive ? "nav-active translate-x-px" : "nav-item"
            }
          >
            <Icon name={l.icon} className="h-5 w-5" />
            <span>{l.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
