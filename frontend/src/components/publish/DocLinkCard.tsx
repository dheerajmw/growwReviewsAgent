import { Icon } from "../common/Icon";
import type { PublishState } from "../../types/pulse";

export function DocLinkCard({ state }: { state?: PublishState }) {
  if (!state?.doc_url) {
    return (
      <div className="card-stitch flex items-start gap-6 opacity-60">
        <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-status-info/10 text-status-info shadow-inner">
          <Icon name="description" className="h-9 w-9" />
        </div>
        <div>
          <h3 className="text-headline-md font-black">Google Doc</h3>
          <p className="mt-1 text-body-md text-text-muted">Not published yet</p>
        </div>
      </div>
    );
  }
  return (
    <div className="card-stitch flex items-start gap-6">
      <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-status-info/10 text-status-info shadow-inner">
        <Icon name="description" className="h-9 w-9" />
      </div>
      <div className="flex-1">
        <h3 className="mb-1 text-headline-md font-black">Google Doc</h3>
        <p className="mb-6 text-body-md text-text-muted">Open latest weekly sync document</p>
        <a href={state.doc_url} target="_blank" rel="noreferrer" className="btn-secondary">
          Open in Docs
          <Icon name="open_in_new" className="h-[18px] w-[18px]" />
        </a>
      </div>
    </div>
  );
}
