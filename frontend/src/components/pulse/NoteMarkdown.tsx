export function NoteMarkdown({ markdown }: { markdown: string }) {
  const lines = markdown.split("\n");
  return (
    <article className="prose-sm max-w-none space-y-4 text-groww-body">
      {lines.map((line, i) => {
        if (line.startsWith("# ")) {
          return (
            <h1 key={i} className="text-xl font-semibold text-groww-dark">
              {line.slice(2)}
            </h1>
          );
        }
        if (line.startsWith("## ")) {
          return (
            <h2 key={i} className="mt-4 text-lg font-semibold text-groww-dark">
              {line.slice(3)}
            </h2>
          );
        }
        if (/^\d+\.\s/.test(line)) {
          return (
            <p key={i} className="ml-4">
              {line}
            </p>
          );
        }
        if (line.startsWith("- ")) {
          return (
            <p key={i} className="ml-4 text-groww-body">
              • {line.slice(2)}
            </p>
          );
        }
        if (!line.trim()) return null;
        return (
          <p key={i}>
            {line}
          </p>
        );
      })}
    </article>
  );
}
