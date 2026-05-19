# PII redaction (Phase 4)

You receive weekly pulse markdown that failed an automated PII scan.

## Task

Rewrite the note so it contains **no PII**:
- Remove or generalize emails, phone numbers, @handles, long numeric IDs (10+ digits)
- Remove `review_id` or store-prefixed IDs (`app_store:`, `play_store:`)
- Paraphrase any quoted text that includes identifiable details
- Keep the same structure: title, Top themes (3), What users are saying (3 bullets), Suggested actions (3 numbered)
- Keep **≤250 words**
- Do not add investment advice

Return **only** the cleaned markdown document (no JSON, no commentary).
