import { Icon } from "../common/Icon";
import type { PublishState } from "../../types/pulse";

export function DraftLinkCard({ state }: { state?: PublishState }) {
  const url = state?.draft_url ?? "https://mail.google.com/mail/u/0/#drafts";
  if (!state?.draft_id) {
    return (
      <div className="card-stitch flex items-start gap-6 opacity-60">
        <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-status-error/10 text-status-error shadow-inner">
          <Icon name="mail" className="h-9 w-9" />
        </div>
        <div>
          <h3 className="text-headline-md font-black">Gmail draft</h3>
          <p className="mt-1 text-body-md text-text-muted">Not created yet</p>
        </div>
      </div>
    );
  }
  return (
    <div className="card-stitch flex items-start gap-6">
      <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-status-error/10 text-status-error shadow-inner">
        <Icon name="mail" className="h-9 w-9" />
      </div>
      <div className="flex-1">
        <h3 className="mb-1 text-headline-md font-black">Gmail draft</h3>
        <p className="mb-6 text-body-md text-text-muted">Review stakeholder update draft</p>
        <a href={url} target="_blank" rel="noreferrer" className="btn-secondary">
          Open Drafts
        </a>
      </div>
    </div>
  );
}
