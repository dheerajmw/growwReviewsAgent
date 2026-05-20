import type { ReactNode } from "react";
import { Icon } from "../common/Icon";

export function MetricCard({
  label,
  value,
  suffix,
  trend,
  chip,
  children,
  valueClassName = "",
}: {
  label: string;
  value?: ReactNode;
  suffix?: string;
  trend?: string;
  chip?: ReactNode;
  children?: ReactNode;
  valueClassName?: string;
}) {
  return (
    <div className="card-stitch">
      <p className="mb-4 text-label-md font-bold uppercase tracking-wider text-text-muted">
        {label}
      </p>
      {children ?? (
        <div className="flex flex-wrap items-baseline gap-4">
          {value != null && value !== "" && (
            <span className={`metric-value ${valueClassName}`}>{value}</span>
          )}
          {suffix && <span className="text-headline-md font-bold text-text-muted/40">{suffix}</span>}
          {trend && (
            <span className="inline-flex items-center rounded-full border border-status-success/10 bg-status-success/15 px-3 py-1 text-label-md font-bold text-status-success">
              <Icon name="trending_up" className="mr-1 h-[18px] w-[18px]" />
              {trend}
            </span>
          )}
        </div>
      )}
      {chip && <div className="mt-2">{chip}</div>}
    </div>
  );
}
