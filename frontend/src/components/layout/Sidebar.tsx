import { NavLink } from "react-router-dom";
import { Icon } from "../common/Icon";

const links = [
  { to: "/", label: "Dashboard", icon: "dashboard" as const, end: true },
  { to: "/pulse", label: "Weekly Pulse", icon: "analytics" as const },
  { to: "/themes", label: "Themes", icon: "category" as const },
  { to: "/pipeline", label: "Pipeline", icon: "account_tree" as const },
  { to: "/settings", label: "Settings", icon: "settings" as const },
];

type SidebarProps = {
  mobileOpen?: boolean;
  onClose?: () => void;
};

function NavLinks({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <nav className="flex-1 space-y-1 px-4">
      {links.map((l) => (
        <NavLink
          key={l.to}
          to={l.to}
          end={l.end}
          onClick={onNavigate}
          className={({ isActive }) => (isActive ? "nav-active" : "nav-item")}
        >
          <Icon name={l.icon} className="h-5 w-5" />
          <span>{l.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}

function Brand() {
  return (
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
  );
}

export function Sidebar({ mobileOpen = false, onClose }: SidebarProps) {
  return (
    <>
      {/* Desktop sidebar */}
      <aside className="glass-nav hidden w-sidebar-width shrink-0 flex-col overflow-y-auto border-r border-white/20 py-8 md:flex">
        <Brand />
        <NavLinks />
      </aside>

      {/* Mobile overlay + drawer */}
      {mobileOpen && (
        <button
          type="button"
          className="fixed inset-0 z-[150] bg-on-surface/40 backdrop-blur-sm md:hidden"
          aria-label="Close menu"
          onClick={onClose}
        />
      )}
      <aside
        className={`glass-nav fixed left-0 top-[5rem] z-[160] flex h-[calc(100vh-5rem)] w-[min(280px,85vw)] flex-col overflow-y-auto border-r border-white/20 py-6 transition-transform duration-300 md:hidden ${
          mobileOpen ? "translate-x-0" : "-translate-x-full pointer-events-none"
        }`}
        aria-hidden={!mobileOpen}
      >
        <div className="mb-4 flex items-center justify-between px-6">
          <span className="text-label-md font-bold text-primary">Menu</span>
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 hover:bg-on-surface/5"
            aria-label="Close sidebar"
          >
            <Icon name="close" className="h-5 w-5" />
          </button>
        </div>
        <Brand />
        <NavLinks onNavigate={onClose} />
      </aside>
    </>
  );
}
