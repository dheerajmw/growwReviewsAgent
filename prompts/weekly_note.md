# Weekly note generation (Phase 3)

Given ranked themes and sample review excerpts, produce the weekly pulse as **JSON only** (no markdown).

## Output JSON schema

```json
{
  "title": "Groww — Weekly Review Pulse (YYYY-MM-DD)",
  "themes": [
    {
      "id": "payments",
      "headline": "One line: theme name, share of voice, and trend in plain English"
    }
  ],
  "quotes": [
    {
      "theme_id": "payments",
      "paraphrased": "One sentence paraphrasing a real user concern (no PII)",
      "source_rating": 1
    }
  ],
  "actions": [
    {
      "theme_id": "payments",
      "text": "One specific product or support action (not investment advice)"
    }
  ]
}
```

## Requirements

- **themes:** exactly **3** entries — use the **top 3** theme ids from input (same order).
- **quotes:** exactly **3** entries — one per top theme; paraphrase heavily; `source_rating` from input.
- **actions:** exactly **3** entries — one per top theme; actionable for product/growth/support.
- Total prose when rendered must be **≤250 words** (short sentences).
- Use week-ending date from input for title.
