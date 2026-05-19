export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="card text-center">
      <p className="font-semibold text-groww-dark">{title}</p>
      <p className="mt-2 text-sm text-groww-muted">{description}</p>
    </div>
  );
}
