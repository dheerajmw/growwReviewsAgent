type IconName =
  | "dashboard"
  | "analytics"
  | "category"
  | "account_tree"
  | "settings"
  | "description"
  | "mail"
  | "open_in_new"
  | "north_east"
  | "trending_up"
  | "verified_user"
  | "check"
  | "schedule"
  | "history"
  | "arrow_forward"
  | "format_quote"
  | "check_circle"
  | "code"
  | "expand_more"
  | "close"
  | "info"
  | "more_horiz"
  | "calendar_month"
  | "refresh"
  | "block"
  | "warning"
  | "menu_book"
  | "shop"
  | "phone_iphone"
  | "menu";

const paths: Record<IconName, React.ReactNode> = {
  dashboard: (
    <path d="M3 3h8v8H3V3zm10 0h8v5h-8V3zM3 13h5v8H3v-8zm7 0h11v8H10v-8z" />
  ),
  analytics: <path d="M4 19V9m6 10V5m6 14v-7" strokeWidth="2" stroke="currentColor" fill="none" />,
  category: <path d="M4 6h7v7H4V6zm9 0h7v4h-7V6zm-9 9h4v7H4v-7zm5 0h10v7H9v-7z" />,
  account_tree: (
    <path d="M12 3v6m0 0-4 4m4-4 4 4M6 17h12v4H6v-4z" strokeWidth="2" stroke="currentColor" fill="none" />
  ),
  settings: (
    <path
      d="M12 15a3 3 0 100-6 3 3 0 000 6zm8.5-3a7.4 7.4 0 00-.1-1l2-1.6-2-3.4-2.4 1a7.6 7.6 0 00-1.7-1l-.4-2.6H9.1l-.4 2.6a7.6 7.6 0 00-1.7 1l-2.4-1-2 3.4 2 1.6a7.4 7.4 0 00-.1 1 7.4 7.4 0 00.1 1l-2 1.6 2 3.4 2.4-1a7.6 7.6 0 001.7 1l.4 2.6h3.8l.4-2.6a7.6 7.6 0 001.7-1l2.4 1 2-3.4-2-1.6c.07-.33.1-.66.1-1z"
      strokeWidth="1.5"
      stroke="currentColor"
      fill="none"
    />
  ),
  description: (
    <path d="M6 4h12v16H6V4zm2 4h8M8 14h8M8 18h5" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  mail: (
    <path d="M4 6h16v12H4V6zm0 0 8 7 8-7" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  open_in_new: (
    <path d="M14 4h6v6M10 14 20 4M16 4h4v4" strokeWidth="2" stroke="currentColor" fill="none" />
  ),
  north_east: (
    <path d="M6 18L18 6M10 6h8v8" strokeWidth="2" stroke="currentColor" fill="none" />
  ),
  trending_up: (
    <path d="M4 16l6-6 4 4 6-8" strokeWidth="2" stroke="currentColor" fill="none" />
  ),
  verified_user: (
    <path
      d="M12 2l7 3v5c0 5-3 8-7 10C8 18 5 15 5 10V5l7-3zm-2 7l2 2 4-4"
      strokeWidth="1.5"
      stroke="currentColor"
      fill="none"
    />
  ),
  check: <path d="M5 12l4 4 10-10" strokeWidth="2" stroke="currentColor" fill="none" />,
  schedule: (
    <path d="M12 6v6l4 2M12 2a10 10 0 100 20 10 10 0 000-20z" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  history: (
    <path d="M12 8v4l3 2M12 4a8 8 0 108 8" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  arrow_forward: (
    <path d="M5 12h14M13 6l6 6-6 6" strokeWidth="2" stroke="currentColor" fill="none" />
  ),
  format_quote: (
    <path d="M7 10H4V6c0-2 2-3 3-3M17 10h-3V6c0-2 2-3 3-3" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  check_circle: (
    <path d="M12 3a9 9 0 109 9M9 12l2 2 4-4" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  code: (
    <path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 4l-4 16" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  expand_more: (
    <path d="M6 9l6 6 6-6" strokeWidth="2" stroke="currentColor" fill="none" />
  ),
  close: <path d="M6 6l12 12M18 6L6 18" strokeWidth="2" stroke="currentColor" fill="none" />,
  info: (
    <path d="M12 16v-4M12 8h.01M12 3a9 9 0 100 18 9 9 0 000-18z" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  more_horiz: <path d="M6 12h.01M12 12h.01M18 12h.01" strokeWidth="3" stroke="currentColor" />,
  calendar_month: (
    <path d="M6 4h12v16H6V4zm2 2v2m8-2v2M6 10h12" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  refresh: (
    <path d="M4 12a8 8 0 0114-5M20 12a8 8 0 01-14 5" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  block: (
    <path d="M12 3a9 9 0 109 9M5 5l14 14" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  warning: (
    <path d="M12 4l9 16H3L12 4zm0 6v4m0 3h.01" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  menu_book: (
    <path d="M6 4h12v16H6V4zm2 4h8M8 12h8" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  shop: (
    <path d="M4 8h16l-2 12H6L4 8zm4-4h8l2 4H6l2-4z" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  phone_iphone: (
    <path d="M9 3h6v18H9V3zm3 14h.01" strokeWidth="1.5" stroke="currentColor" fill="none" />
  ),
  menu: (
    <path d="M4 7h16M4 12h16M4 17h16" strokeWidth="2" stroke="currentColor" strokeLinecap="round" fill="none" />
  ),
};

export function Icon({
  name,
  className = "h-5 w-5",
  filled,
}: {
  name: IconName;
  className?: string;
  filled?: boolean;
}) {
  const strokeIcons: IconName[] = [
    "analytics",
    "account_tree",
    "settings",
    "description",
    "mail",
    "open_in_new",
    "north_east",
    "trending_up",
    "verified_user",
    "check",
    "schedule",
    "history",
    "arrow_forward",
    "format_quote",
    "check_circle",
    "code",
    "expand_more",
    "close",
    "info",
    "calendar_month",
    "refresh",
    "block",
    "warning",
    "menu_book",
    "shop",
    "phone_iphone",
    "menu",
  ];
  const isStroke = strokeIcons.includes(name);
  return (
    <svg
      className={className}
      viewBox="0 0 24 24"
      aria-hidden
      fill={isStroke ? "none" : filled ? "currentColor" : "currentColor"}
    >
      {paths[name]}
    </svg>
  );
}
