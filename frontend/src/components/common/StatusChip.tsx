type Variant = "success" | "warning" | "error" | "neutral";

const styles: Record<Variant, string> = {
  success: "bg-green-50 text-green-700 border-green-200",
  warning: "bg-amber-50 text-amber-700 border-amber-200",
  error: "bg-red-50 text-red-700 border-red-200",
  neutral: "bg-gray-50 text-groww-muted border-groww-border",
};

export function StatusChip({ label, variant = "neutral" }: { label: string; variant?: Variant }) {
  return (
    <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${styles[variant]}`}>
      {label}
    </span>
  );
}
