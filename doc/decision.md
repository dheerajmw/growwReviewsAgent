# Decision Log — Weekly App Review Pulse (Milestone 3)

This file records **business and technical decisions** that shape the project. When a choice affects scope, architecture, compliance, or integrations, add an entry here instead of only embedding it in chat or code comments.

**Related docs:** [problemStatement.md](./problemStatement.md) · [architecture.md](./architecture.md) · [phasewiseImplementationPlan.md](./phasewiseImplementationPlan.md) · [eval/README.md](./eval/README.md)

---

## How to use this log

1. Assign the next **D-###** id (see index below).
2. Copy the [template](#decision-template) at the bottom.
3. Set status: **Accepted** | **Superseded** | **Proposed** | **Rejected**
4. Link from `architecture.md` or phase docs if the decision changes build order or eval criteria.

---

## Decision index

| ID | Title | Type | Status | Date |
|----|-------|------|--------|------|
| [D-001](#d-001-product-context-groww-milestone-1-continuity) | Product context: Groww (Milestone 1 continuity) | Business | Accepted | 2026-05-17 |
| [D-002](#d-002-weekly-pulse-audience-and-format) | Weekly pulse audience and format | Business | Accepted | 2026-05-17 |
| [D-003](#d-003-review-data-source-public-exports-only) | Review data: public exports only | Business / Compliance | Accepted | 2026-05-17 |
| [D-004](#d-004-theme-cap-and-vocabulary) | Theme cap (≤5) and vocabulary | Business / Product | Accepted | 2026-05-17 |
| [D-005](#d-005-note-structure-and-word-limit) | Note structure and 250-word limit | Business | Accepted | 2026-05-17 |
| [D-006](#d-006-pii-policy-and-publish-gate) | PII policy and publish gate | Compliance | Accepted | 2026-05-17 |
| [D-007](#d-007-google-docs-and-gmail-via-mcp-not-direct-apis) | Google Docs & Gmail via MCP (not direct APIs) | Technical | Accepted | 2026-05-17 |
| [D-008](#d-008-mcp-server-choice-google-workspace-mcp) | MCP server: Google Workspace MCP | Technical | Accepted | 2026-05-17 |
| [D-009](#d-009-agent-orchestration-in-cursor) | Agent orchestration in Cursor | Technical | Accepted | 2026-05-17 |
| [D-010](#d-010-local-pipeline-vs-mcp-boundary) | Local pipeline vs MCP boundary | Technical | Accepted | 2026-05-17 |
| [D-011](#d-011-gmail-draft-only-no-auto-send) | Gmail: draft only, no auto-send | Business / Ops | Accepted | 2026-05-17 |
| [D-012](#d-012-doc-idempotency-same-calendar-week) | Doc idempotency (same calendar week) | Technical | Accepted | 2026-05-17 |
| [D-013](#d-013-review_id-internal-only) | `review_id` internal only | Technical / Privacy | Accepted | 2026-05-17 |
| [D-014](#d-014-ingest-window-812-weeks) | Ingest window: 8–12 weeks | Business | Accepted | 2026-05-17 |
| [D-015](#d-015-out-of-scope-investment-advice-and-scraping) | Out of scope: investment advice & scraping | Business | Accepted | 2026-05-17 |
| [D-016](#d-016-phase-1-content-normalization-filters) | Phase 1 content normalization filters | Technical | Accepted | 2026-05-17 |

---

## Decisions

### D-001: Product context — Groww (Milestone 1 continuity)

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business |
| **Date** | 2026-05-17 |

**Context:** Milestone 3 must use the same product chosen in Milestone 1 so review themes and actions stay relevant to one real mobile app.

**Decision:** Use **Groww** (investing, mutual funds, stocks, mobile money flows) as the reference product for prompts, theme vocabulary, and pulse titling.

**Consequences:**
- Theme examples align with fintech (KYC, payments, statements, withdrawals).
- Weekly note titles and email subjects include “Groww”.
- If Milestone 1 product differed, update this decision and downstream prompts.

**Alternatives considered:** Generic “fintech app” (rejected — weaker alignment with course continuity).

---

### D-002: Weekly pulse audience and format

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business |
| **Date** | 2026-05-17 |

**Context:** Output must serve product, support, and leadership without a live dashboard.

**Decision:** Deliver a **one-page weekly pulse** optimized for &lt;2 minute scan: top **3** themes (from ≤5 clusters), **3** paraphrased quotes, **3** action ideas. Primary channels: **Google Doc** (persistent) + **Gmail draft** (distribution to self/alias).

**Consequences:**
- Note generator enforces fixed sections (see D-005).
- “Top 3” is a presentation choice; clustering still allows up to 5 themes (D-004).

**Alternatives considered:** Slack post only; full PDF report (rejected — out of milestone scope).

---

### D-003: Review data — public exports only

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business / Compliance |
| **Date** | 2026-05-17 |

**Context:** Store consoles require authentication; scraping behind login is fragile and may violate terms.

**Decision:** Ingest reviews only from **downloaded public exports** (App Store Connect / Play Console CSV or JSON) placed in `data/raw/`. No automated login scraping in code.

**Consequences:**
- `scripts/ingest_reviews.py` reads local files only.
- Manual export step before each weekly run.
- Phase 1 eval verifies both stores present.

**Alternatives considered:** Third-party review APIs (deferred — cost/approval not in scope).

---

### D-004: Theme cap and vocabulary

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business / Product |
| **Date** | 2026-05-17 |

**Context:** Unbounded themes make weekly notes unreadable; product teams need familiar buckets.

**Decision:**
- Cluster into **at most 5 themes**.
- Default vocabulary: **onboarding, KYC, payments, statements, withdrawals**.
- Surface **top 3** ranked themes in the weekly note.
- Merge or relabel only when review corpus clearly requires it; still ≤5.

**Consequences:**
- `validate_themes.py` (or equivalent) enforces `len(themes) <= 5`.
- `prompts/themes.md` uses closed-set JSON output.

**Alternatives considered:** Open-ended tags (rejected — hard to compare week over week).

---

### D-005: Note structure and word limit

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business |
| **Date** | 2026-05-17 |

**Context:** Leadership asked for scannable updates, not essays.

**Decision:** Weekly note body **≤250 words**, with required sections: top 3 themes (one line each), 3 quotes, 3 action ideas. Store parallel structured copy in `data/weekly/note.json` for MCP publish.

**Consequences:**
- `scripts/validate_note.py` blocks publish if over limit or missing sections.
- Action ideas are product/support oriented, not investment advice (D-015).

**Alternatives considered:** 500-word memo (rejected — violates problem statement).

---

### D-006: PII policy and publish gate

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Compliance |
| **Date** | 2026-05-17 |

**Context:** Review exports may contain reviewer handles or identifiable text; Google artifacts must not leak PII.

**Decision:**
- **No PII** in Doc, Gmail draft, or published artifacts.
- **Paraphrase** quotes; redact emails, phones, @handles, long numeric IDs.
- Run `scripts/check_pii.py` on `note.md`; **block MCP publish** on failure (`data/weekly/blockers.json`).

**Consequences:**
- Phase 4 is a **hard gate** before Phases 5–6 (see eval docs).
- `review_id` never appears in published content (D-013).

**Alternatives considered:** Publish with redaction in Google only (rejected — PII must not leave local gate).

---

### D-007: Google Docs and Gmail via MCP (not direct APIs)

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Technical |
| **Date** | 2026-05-17 |

**Context:** Milestone requires Google workspace delivery; course/agent pattern favors MCP over bespoke OAuth clients in app code.

**Decision:** All **Google Docs** and **Gmail** operations go through a **Google Workspace MCP server** invoked from Cursor. **No** `googleapis`, `google-auth`, or hand-rolled REST clients in this repository for Docs/Gmail.

**Consequences:**
- Agent uses `CallMcpTool` (or Cursor MCP UI) for create/update Doc and create draft.
- OAuth lifecycle lives inside MCP server config.
- Phase 0/5/6 evals grep for forbidden Google SDK imports.

**Alternatives considered:** Python `google-api-python-client` in repo (rejected — conflicts with problem statement and D-007).

---

### D-008: MCP server choice — Google Workspace MCP

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Technical |
| **Date** | 2026-05-17 |

**Context:** Need Docs + Gmail draft tools in one integration surface.

**Decision:** Default to [Google Workspace MCP](https://github.com/Dave-Nguyen-PM/google-workplace-mcp). Course- or team-approved equivalent allowed if it exposes **Docs** and **Gmail draft** tools with same constraints as D-007.

**Consequences:**
- Configure in `~/.cursor/mcp.json` (or Cursor Settings → MCP).
- Document actual package name and env vars in README when implemented.

**Alternatives considered:** Separate single-purpose MCPs per service (acceptable if course requires; document swap here).

---

### D-009: Agent orchestration in Cursor

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Technical |
| **Date** | 2026-05-17 |

**Context:** Pipeline mixes deterministic scripts (ingest, validate) with LLM steps (themes, note) and MCP (publish).

**Decision:** **Cursor agent** is the orchestrator: runs local scripts, calls LLM via prompts in `prompts/`, routes Google work to MCP. Optional later: Cursor SDK agent with same MCP servers — must preserve D-007 boundary.

**Consequences:**
- Versioned prompts under `prompts/`.
- Single runbook prompt: “Run weekly pulse for Groww” (Phase 7).

**Alternatives considered:** Fully headless CI-only pipeline without Cursor (deferred — MCP is interactive in Phase 0).

---

### D-010: Local pipeline vs MCP boundary

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Technical |
| **Date** | 2026-05-17 |

**Context:** Clear split reduces accidental Google API code in scripts.

**Decision:**

| Layer | Responsibility |
|-------|----------------|
| **Local** (scripts / agent) | Ingest, normalize, theme clustering, note generation, PII check, validators |
| **MCP** | Google Docs create/update; Gmail draft create |
| **Human** | Download store exports; review draft before send |

**Consequences:**
- Artifacts: `data/reviews/`, `data/themes/`, `data/weekly/` local; `publish_state.json` stores MCP-returned ids.

---

### D-011: Gmail — draft only, no auto-send

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business / Ops |
| **Date** | 2026-05-17 |

**Context:** Automatic send risks wrong recipient, typos, or PII escaping human review.

**Decision:** MCP creates a **draft** to `PULSE_DRAFT_TO` (self or team alias). **Do not** auto-send unless a future decision explicitly overrides.

**Consequences:**
- Phase 6 eval confirms draft in Gmail Drafts, not Sent.
- Human sends after review.

**Alternatives considered:** Send immediately (rejected — operational risk).

---

### D-012: Doc idempotency (same calendar week)

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Technical |
| **Date** | 2026-05-17 |

**Context:** Re-running the agent the same week should not spam new Docs.

**Decision:** For the same **calendar week**, **update** the existing Google Doc (id in `data/weekly/publish_state.json`). Title pattern: `Weekly Review Pulse — Groww — YYYY-MM-DD`. New week → new Doc or explicit update policy documented in runbook.

**Consequences:**
- `publish_state.json` stores `doc_id`, `doc_url`, `published_at`.
- Phase 7 E2E tests second run behavior.

**Alternatives considered:** New Doc every run (rejected — clutters Drive).

---

### D-013: `review_id` internal only

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Technical / Privacy |
| **Date** | 2026-05-17 |

**Context:** Dedup requires stable ids; ids must not appear in stakeholder-facing artifacts.

**Decision:** Persist `review_id` in `normalized.jsonl` and theme JSON for dedup and QA only. **Never** include in `note.md`, `note.json` published fields, Google Doc, or Gmail body.

**Consequences:**
- Phase 1 eval documents internal-only use.
- PII checker may still flag long numeric strings in note text.

---

### D-014: Ingest window — 8–12 weeks

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business |
| **Date** | 2026-05-17 |

**Context:** Problem statement specifies rolling window for relevance vs volume.

**Decision:** Default ingest window **12 weeks**; minimum **8 weeks** when data is sparse. Configurable via ingest CLI flag; log dropped out-of-window rows.

**Consequences:**
- All `date` fields in normalized output fall within chosen window.
- Theme trends (optional) compare to prior `ranked.json` snapshots.

---

### D-015: Out of scope — investment advice and scraping

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Business |
| **Date** | 2026-05-17 |

**Context:** Groww is a financial product; model might drift into advisory language.

**Decision:** Explicitly **out of scope:**
- Investment advice or fund recommendations in pulse or actions.
- Scraping store consoles behind login.
- Collecting or publishing reviewer PII.

**Consequences:**
- Prompts and validators reject advisory phrasing where feasible.
- Action ideas target product UX, reliability, and support — not “buy/sell”.

---

### D-016: Phase 1 content normalization filters

| Field | Value |
|-------|--------|
| **Status** | Accepted |
| **Type** | Technical |
| **Date** | 2026-05-17 |

**Context:** Short, emoji-heavy, and non-English reviews add noise to theme clustering and the weekly pulse.

**Decision:** During ingest, after the date-window filter, drop reviews that:
- Have fewer than **6 English words** (title + body combined)
- Contain **emoji** or common ASCII emoticons
- Are **not English** (`langdetect`, with ASCII fallback for very short text)

Configured in `configs/phase1_ingest.yaml` under `normalization`. Skip reasons logged: `too_few_words`, `contains_emoji`, `non_english`.

**Consequences:**
- `pipelines/phase1_ingest/ingest/filters.py` implements rules; `langdetect` added to `requirements.txt`.
- Ingest summary includes `Filtered (normalization)` counts.

**Alternatives considered:** Keep all languages and filter in Phase 2 (rejected — cleaner corpus at ingest).

---

## Open / proposed decisions

Record new choices here until accepted, then move to the index with a full entry.

| ID | Topic | Status | Notes |
|----|-------|--------|-------|
| — | LLM provider / model for clustering & note | Proposed | Document model name and cost when implementation starts |
| — | Week-over-week trend arrows in note | Proposed | Optional Phase 7 enhancement |
| — | Embeddings vs pure LLM batch for themes | Proposed | Choose when review volume &gt; ~500 |

---

## Decision template

```markdown
### D-###: [Short title]

| Field | Value |
|-------|--------|
| **Status** | Proposed / Accepted / Superseded / Rejected |
| **Type** | Business / Technical / Compliance |
| **Date** | YYYY-MM-DD |

**Context:** [Why a decision was needed]

**Decision:** [What we chose]

**Consequences:** [Impact on code, docs, evals, ops]

**Alternatives considered:** [What we did not pick and why]
```

---

## Superseded decisions

_None yet._ When reversing a decision, mark the old entry **Superseded** and link to the replacing D-###.
