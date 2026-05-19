import { Icon } from "../common/Icon";
import type { PublishState } from "../../types/pulse";

export function DocLinkCard({ state }: { state?: PublishState }) {
  if (!state?.doc_url) {
    return (
      <div className="card-stitch flex items-start gap-4 opacity-60">
        <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#F1F3F4] text-[#4285F4]">
          <Icon name="description" className="h-8 w-8" />
        </div>
        <div>
          <h3 className="text-body-lg font-bold">Google Doc</h3>
          <p className="mt-1 text-body-md text-text-muted">Not published yet</p>
        </div>
      </div>
    );
  }
  return (
    <div className="card-stitch flex items-start gap-4">
      <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-[#F1F3F4] text-[#4285F4]">
        <Icon name="description" className="h-8 w-8" />
      </div>
      <div className="flex-1">
        <h3 className="text-body-lg font-bold">Google Doc</h3>
        <p className="mb-4 mt-1 text-body-md text-text-muted">Open weekly document</p>
        <a href={state.doc_url} target="_blank" rel="noreferrer" className="btn-secondary">
          Open in Docs
          <Icon name="open_in_new" className="h-4 w-4" />
        </a>
      </div>
    </div>
  );
}
