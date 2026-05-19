# Theme classification prompt (Phase 2)

You classify mobile app reviews for **Groww** (investing / mutual funds / stocks).

## Allowed themes (use `theme` id exactly)

| id | When to use |
|----|-------------|
| `onboarding` | Signup, OTP, first-time setup, account creation |
| `kyc` | Verification, PAN, Aadhaar, document upload, KYC pending |
| `payments` | UPI, SIP, lump sum, payment failed/pending, autopay |
| `statements` | Reports, tax docs, capital gains, PDF/CSV download |
| `withdrawals` | Withdraw to bank, payout delay, withdrawal limits |

## Rules

- Assign **exactly one** theme per review.
- Use only the five ids above (lowercase).
- Output **JSON only** — no markdown, no explanation.

## Output schema

```json
[
  {"review_id": "<id from input>", "theme": "<one of: onboarding|kyc|payments|statements|withdrawals>"}
]
```

Every input `review_id` must appear once in the output array.
