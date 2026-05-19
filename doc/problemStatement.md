# Problem Statement — Weekly App Review Pulse (Milestone 3)

## Project Context

This milestone continues the **same product you selected in Milestone 1** (reference context: **Groww** — investing, mutual funds, stocks, and related money flows on mobile).

**Goal:** Turn recent **App Store** and **Play Store** public reviews into a **one-page weekly pulse** that product, support, and leadership can scan in under two minutes, then **deliver that pulse as a draft** via your Google workspace — without building custom Google API clients in application code.

**End-to-end flow:**

1. Ingest 8–12 weeks of public review exports (rating, title, text, date).
2. Cluster feedback into at most **5 themes** (e.g., onboarding, KYC, payments, statements, withdrawals).
3. Produce a scannable weekly note (top themes, quotes, action ideas).
4. Persist the note in **Google Docs** and create a **Gmail draft** to yourself (or an alias) containing the same content.

**Out of scope:** Investment advice, scraping behind store logins, or including PII in any artifact.

---

## Who This Helps

| Audience | Value |
|----------|--------|
| **Product / Growth** | See what to fix or prioritize next |
| **Support** | Know what users are saying and what to acknowledge |
| **Leadership** | Quick weekly health pulse on mobile sentiment |

---

## What You Must Build

1. **Import reviews** from the last **8–12 weeks** (fields: rating, title, text, date).
2. **Group reviews** into **≤5 themes** (examples: onboarding, KYC, payments, statements, withdrawals).
3. **Generate a weekly one-page note** with:
   - Top **3** themes
   - **3** anonymized user quotes
   - **3** action ideas
4. **Publish outputs:**
   - Create or update a **Google Doc** with the weekly note.
   - Create a **Gmail draft** with the note (send to yourself or a team alias).

---

## Integration Approach — MCP (Not Direct APIs)

**Do not** integrate Gmail or Google Docs via hand-rolled REST/SDK calls (e.g., `googleapis` clients, OAuth token refresh in app code, or custom Gmail/Docs API wrappers).

**Do** use a **Google Workspace MCP server** in Cursor so the agent can:

| Capability | MCP usage |
|------------|-----------|
| **Google Docs** | Create/read/update the weekly pulse document |
| **Gmail** | Create a draft email with the note body (and optional subject) |

**Recommended MCP:** [Google Workspace MCP](https://github.com/Dave-Nguyen-PM/google-workplace-mcp) (or an equivalent Workspace MCP that exposes **Docs** and **Gmail** tools).

**Setup (high level):**

1. Add the MCP server in Cursor (`~/.cursor/mcp.json` or Cursor MCP settings).
2. Complete OAuth once for the Google account that owns the Doc and draft mailbox.
3. Invoke MCP tools from the agent/workflow for Doc and draft operations — not raw API endpoints in application logic.

Other data sources (e.g., review CSV/JSON exports) may be read from the filesystem or local scripts; only **Google Docs and Gmail** must go through MCP.

---

## Key Constraints

- **Public review exports only** — no scraping behind App Store / Play Store logins.
- **Max 5 themes** for clustering.
- **Weekly note ≤250 words** — scannable, executive-friendly.
- **No PII** — no usernames, emails, device IDs, or other identifiers in the Doc, draft, or intermediate artifacts.
- **Quotes must be sanitized** — paraphrase or redact anything that could identify a user.

---

## Related documents

- [architecture.md](./architecture.md) — system design and MCP boundary
- [phasewiseImplementationPlan.md](./phasewiseImplementationPlan.md) — build phases
- [decision.md](./decision.md) — business and technical decision log
- [eval/README.md](./eval/README.md) — per-phase testing and exit criteria

---

## Deliverables Checklist

- [ ] Review ingest pipeline (8–12 weeks)
- [ ] Theme clustering (≤5 themes) + weekly note generator
- [ ] Google Doc with the weekly pulse (via MCP)
- [ ] Gmail draft to self/alias (via MCP)
- [ ] No PII in any output
