import { Icon } from "../common/Icon";
import type { PublishState } from "../../types/pulse";

export function DraftLinkCard({ state }: { state?: PublishState }) {
  const url = state?.draft_url ?? "https://mail.google.com/mail/u/0/#drafts";
  if (!state?.draft_id) {
    return (
      <div className="card-stitch flex items-start gap-4 opacity-60">
        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#F1F3F4] text-[#EA4335]">
          <Icon name="mail" className="h-8 w-8" />
        </div>
        <div>
          <h3 className="text-body-lg font-bold">Gmail draft</h3>
          <p className="mt-1 text-body-md text-text-muted">Not created yet</p>
        </div>
      </div>
    );
  }
  return (
    <div className="card-stitch flex items-start gap-4">
      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#F1F3F4] text-[#EA4335]">
        <Icon name="mail" className="h-8 w-8" />
      </div>
      <div className="flex-1">
        <h3 className="text-body-lg font-bold">Gmail draft</h3>
        <p className="mb-4 mt-1 text-body-md text-text-muted">Review before sending</p>
        <a href={url} target="_blank" rel="noreferrer" className="btn-secondary">
          Open Drafts
        </a>
      </div>
    </div>
  );
}
