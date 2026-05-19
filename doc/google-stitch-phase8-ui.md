# Google Stitch UI Prompts — Groww Weekly Review Pulse (Phase 8)

**Purpose:** Copy-paste prompts for [Google Stitch](https://stitch.withgoogle.com) (or similar AI UI generators) to design the Phase 8 web dashboard aligned with [Groww](https://groww.in) visual language.

**Implementation plan:** [phasewiseImplementationPlan.md](./phasewiseImplementationPlan.md#phase-8--web-dashboard-proper-frontend) · **Architecture:** [architecture.md](./architecture.md#36-web-dashboard-phase-8--presentation-layer) · **Eval:** [eval/phase-08/eval.md](./eval/phase-08/eval.md)

---

## How to use these prompts

1. Run **§1 Master design system** once to set global tokens and tone.
2. Run **§2 App shell** for navigation and layout frame.
3. Run **§3–§7** for each screen (one prompt per screen).
4. Optionally run **§8 Component sheet** and **§9 Mobile** for variants.
5. Export specs / screenshots into `frontend/` implementation (React + Tailwind).

**Product name in UI:** **Groww — Weekly Review Pulse** (internal tool for App Store + Play Store review insights).

---

## 1. Master design system (run first)

```text
Design a design system for an internal fintech analytics dashboard called "Groww Weekly Review Pulse".

Visual reference: Match the clean, trustworthy investing UI of groww.in — light backgrounds, generous whitespace, rounded cards, minimal clutter, confident green accents. NOT a marketing landing page; this is a data dashboard for product and leadership.

Brand & colors:
- Primary green: #00D09C (CTAs, active nav, success chips) — same family as Groww.in
- Primary green hover: #00B88A
- Primary dark: #1D1D1F (headings)
- Body text: #44475B
- Muted text: #7C7E8C
- Page background: #F6F7F9
- Card surface: #FFFFFF
- Border: #E9E9EB
- Success: #00D09C | Warning: #F5A623 | Error: #DF514C | Info: #5367FF
- Subtle card shadow: 0 1px 3px rgba(0,0,0,0.06)

Typography:
- Font: Inter or system-ui sans-serif
- H1: 28px semibold #1D1D1F
- H2: 20px semibold
- Body: 14–16px regular, line-height 1.5
- Caption: 12px #7C7E8C

Layout:
- 8px spacing grid
- Card radius: 12px
- Button radius: 8px
- Max content width: 1200px centered
- Left sidebar nav (desktop), 240px width, white background

Components to define:
- Primary button (green fill, white text)
- Secondary button (white fill, green border)
- Status chips: Passed (green), Pending (gray), Failed (red)
- Data cards with title + metric
- Simple horizontal bar chart style (rounded bars, green fill)
- External link cards with icon (Google Doc, Gmail Draft)

Tone: Professional, calm, scannable in under 2 minutes. No stock tips or investment advice UI. No user PII fields.
```

---

## 2. App shell (layout frame)

```text
Create a desktop web app shell for "Groww Weekly Review Pulse" using the Groww design system (light #F6F7F9 background, green #00D09C accents, white cards).

Layout:
- Top header: Groww-style minimal bar — product name "Weekly Review Pulse" with small Groww sublabel "App Reviews", week badge "Week ending 19 May 2026" on the right, subtle PII status chip "PII cleared ✓" in green
- Left sidebar (240px): nav items with icons — Dashboard, Weekly Pulse, Themes, Pipeline, Settings. Active item has green left border + light green tint background
- Main content area: scrollable, padding 24px
- Footer: one line muted text "Data from public App Store & Play exports · Updated via weekly pipeline"

Style like groww.in: clean, airy, no heavy gradients. Simple line icons. Mobile: show hamburger menu placeholder.

Do not include login screens or Google OAuth embeds.
```

---

## 3. Dashboard page (`/`)

```text
Design the Dashboard home screen for "Groww Weekly Review Pulse" in Groww visual language (groww.in style: white cards on #F6F7F9, green #00D09C accents, Inter font).

Content sections:
1. Hero row: title "This week's pulse", subtitle "Executive summary from mobile app reviews", green text link "Read full pulse →"

2. Three metric cards in a row:
   - "Reviews analyzed" → 848
   - "Word count" → 120 / 250 max (green if under limit)
   - "PII gate" → Passed (green chip)

3. "Top 3 themes" card with horizontal bar mini-chart:
   - Payments 40%
   - Onboarding 30%
   - Statements 25%
   Green bars on gray track, labels left, percentage right

4. Two action cards side by side:
   - "Google Doc" — icon, "Open weekly document", secondary button "Open in Docs" (opens external)
   - "Gmail draft" — icon, "Review before sending", secondary button "Open Drafts"

5. Small info strip: "Last pipeline run · 19 May 2026, 19:23 UTC · GitHub Actions scheduled Mondays 06:00 UTC"

Keep it simple, attractive, lots of whitespace. No tables of raw reviews. No stock market tickers.
```

---

## 4. Weekly pulse page (`/pulse`)

```text
Design the "Weekly Pulse" reading page for Groww Weekly Review Pulse dashboard. Groww.in style: clean cards, green accents, readable typography.

Layout: two columns on desktop (70% / 30%).

Left column — main reading card (white, rounded 12px):
- Title: "Groww — Weekly Review Pulse (2026-05-19)"
- Section "Top themes" — numbered list 1–3, one line each with theme name and share %
- Section "What users are saying" — 3 bullet quotes, paraphrased, muted italic feel
- Section "Suggested actions" — numbered list 1–3, product-oriented actions
- Bottom: small badge "120 words · within 250 limit" in green

Right column — sidebar panels:
- "PII status" card — green check "Cleared for publish"
- "Quick links" — buttons for Google Doc and Gmail Draft (external links)
- "Structured data" collapsed accordion hint (themes / quotes / actions JSON summary — no raw IDs)

Typography optimized for leadership scan in under 2 minutes. No usernames, emails, or review IDs anywhere.

Style: similar trust and simplicity as groww.in blog/help pages — not flashy, not dark mode.
```

---

## 5. Themes page (`/themes`)

```text
Design the "Themes" analytics page for Groww Weekly Review Pulse. Match groww.in fintech dashboard aesthetics: light background, white cards, green #00D09C chart accents.

Top: page title "Review themes", subtitle "Up to 5 themes from sampled App Store & Play reviews"

Row 1 — two cards:
- Left (60%): Donut or bar chart "Share of voice" — 5 segments max, labels: Payments, Onboarding, Statements, Withdrawals, KYC. Use green shades + one gray for smallest
- Right (40%): Summary card "Sample size" 450 reviews, "Stores" App Store + Play Store icons

Row 2 — table card "Ranked themes":
Columns: Rank | Theme | Reviews | % of sample | Low ratings (1–2★)
5 rows with subtle zebra striping, rank 1–3 rows have faint green left accent

Optional: clicking a row opens a right drawer "Theme detail" with description placeholder only — NO individual review text, NO user IDs

Clean, data-focused, Groww-like spacing. No investment product cards.
```

---

## 6. Pipeline page (`/pipeline`)

```text
Design the "Pipeline" status page for Groww Weekly Review Pulse internal tool. Groww visual style: simple, trustworthy, light UI.

Page title "Pipeline status", subtitle "Phases 1–7 · automated refresh via GitHub Actions"

Main card — vertical stepper (7 steps):
1. Ingest reviews — ✓ complete (green)
2. Theme clustering (Groq) — ✓ complete
3. Weekly note — ✓ complete
4. PII gate — ✓ passed (green chip)
5. Google Doc publish — ✓ complete with link
6. Gmail draft — ✓ complete
7. E2E scheduler — ✓ GitHub Actions

Each step: icon circle, title, short status line, timestamp muted. Incomplete steps gray, failed steps red.

Below stepper:
- Alert banner (only if failed): red subtle background "PII blockers detected" with "View details" link
- Info card "Scheduler" — calendar icon, "Runs every Monday 06:00 UTC", link "View GitHub Actions"
- Optional admin row: green outline button "Refresh data", disabled state gray

No terminal logs, no JSON viewers. Keep executive-friendly like groww.in account settings pages.
```

---

## 7. Settings page (`/settings`)

```text
Design a minimal Settings page for Groww Weekly Review Pulse dashboard. Groww.in style: white form cards on #F6F7F9.

Sections as stacked cards:
1. "Week selection" — dropdown "Week ending 2026-05-19", helper text "Switch historical weekly pulses when available"

2. "Configuration status" (read-only, no secrets shown):
   - Google Doc ID — Configured ✓ (green dot)
   - Gmail draft recipient — Configured ✓
   - MCP server — Connected (green)
   - Groq API — Not shown / server-side only (gray muted)

3. "Developer" — text input "API base URL" placeholder http://localhost:8000, helper "Local BFF for development"

4. Links row: text links "Runbook", "GitHub repository" in green

Simple, sparse, no toggles for dangerous actions. No API key input fields visible.
```

---

## 8. Component sheet (optional)

```text
Create a component sheet / UI kit page for Groww Weekly Review Pulse on one artboard:

Include: primary button, secondary button, ghost button, status chips (passed/pending/failed/warning), metric card, theme bar chart snippet, external link card (Doc + Gmail), phase stepper node (complete/pending/failed), loading skeleton, empty state illustration (simple line art, green accent), error state card, word count badge "120/250", page header with breadcrumb, sidebar nav item default + active states.

Colors strictly: green #00D09C, background #F6F7F9, text #44475B, cards white, radius 12px.

Style reference: groww.in — clean Indian fintech, not crypto-neon, not dark terminal aesthetic.
```

---

## 9. Mobile responsive (375px)

```text
Adapt the Groww Weekly Review Pulse dashboard for mobile width 375px.

Changes:
- Sidebar becomes bottom tab bar or hamburger drawer with 5 nav items
- Dashboard metric cards stack vertically full width
- Pulse page becomes single column: reading card first, sidebar panels below
- Themes chart stacks above table; horizontal scroll on table if needed
- Pipeline stepper remains vertical, full width
- Touch-friendly tap targets 44px min
- Keep groww.in mobile feel: white cards, green CTAs, plenty of padding 16px

Show: Dashboard + Weekly Pulse mobile screens side by side in one frame.
```

---

## 10. Sample copy (use in all screens)

Use realistic placeholder copy consistent with the pipeline:

| Element | Sample text |
|---------|-------------|
| Product title | Groww — Weekly Review Pulse |
| Week badge | Week ending 2026-05-19 |
| Theme 1 | Payments — 40% of sampled reviews |
| Theme 2 | Onboarding — 30% |
| Theme 3 | Statements — 25% |
| Quote | Users report high fees and glitches during transactions |
| Action | Improve payment processing to reduce errors and fees |
| PII chip | PII cleared |
| Doc CTA | Open Google Doc |
| Draft CTA | Open Gmail Drafts |

**Do not use:** real user names, emails, phone numbers, stock tips, or "buy/sell" language.

---

## 11. Stitch → React handoff checklist

After Stitch export, implement in `frontend/` per Phase 8:

- [ ] Map green `#00D09C` → Tailwind `primary` token in `tailwind.config.js`
- [ ] Build `AppShell`, `Sidebar`, five routes from §3–§7
- [ ] Wire TanStack Query to `/api/v1/*` (see plan §8.3)
- [ ] Verify WCAG AA contrast on green buttons
- [ ] Test 375px and 1280px breakpoints
- [ ] No Google OAuth UI components

---

## Related links

- [Groww.in](https://groww.in) — visual reference (light fintech UI, green CTAs, card layouts)
- [Phase 8 implementation plan](./phasewiseImplementationPlan.md#phase-8--web-dashboard-proper-frontend)
- [Runbook](./runbook.md) — pipeline that feeds dashboard data
