import type { ReactNode } from "react";
import { Icon } from "../common/Icon";

export function MetricCard({
  label,
  value,
  suffix,
  trend,
  chip,
  children,
}: {
  label: string;
  value?: ReactNode;
  suffix?: string;
  trend?: string;
  chip?: ReactNode;
  children?: ReactNode;
}) {
  return (
    <div className="card-stitch transition-transform hover:-translate-y-0.5">
      <p className="mb-2 text-body-md text-text-muted">{label}</p>
      {children ?? (
        <div className="flex items-baseline gap-3">
          {value != null && value !== "" && (
            <span className="text-headline-xl text-on-surface">{value}</span>
          )}
          {suffix && <span className="text-body-lg text-text-muted">{suffix}</span>}
          {trend && (
            <span className="flex items-center gap-1 rounded-full bg-status-success/10 px-2 py-0.5 text-label-md font-medium text-status-success">
              <Icon name="trending_up" className="h-4 w-4" />
              {trend}
            </span>
          )}
        </div>
      )}
      {chip && <div className="mt-2">{chip}</div>}
    </div>
  );
}
