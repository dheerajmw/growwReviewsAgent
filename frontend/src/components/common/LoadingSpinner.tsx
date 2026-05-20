export function LoadingSpinner() {
  return (
    <div className="flex justify-center py-12" role="status">
      <div className="h-10 w-10 animate-spin rounded-full border-2 border-border-subtle border-t-status-success shadow-success-glow" />
    </div>
  );
}
