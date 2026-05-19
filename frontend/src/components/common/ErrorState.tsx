export function ErrorState({ message }: { message: string }) {
  return (
    <div className="card border-red-200 bg-red-50 text-red-800">
      <p className="font-medium">Something went wrong</p>
      <p className="mt-1 text-sm">{message}</p>
    </div>
  );
}
