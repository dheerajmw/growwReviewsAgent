export function LoadingSpinner() {
  return (
    <div className="flex justify-center py-12" role="status">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-groww-border border-t-groww-primary" />
    </div>
  );
}
