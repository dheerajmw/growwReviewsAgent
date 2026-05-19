# Raw review exports

Place **public** App Store Connect and Play Console export files here.

| Pattern | Source |
|---------|--------|
| `app_store*.csv` / `.json` | App Store Connect |
| `play_store*.csv` / `.json` | Play Console |

**Download public reviews** (no console login; uses public store pages):

```bash
pip install -r requirements.txt
python3 scripts/download_reviews.py --weeks 12
python3 scripts/ingest_reviews.py -v
```

**Sample fixtures** (offline dev):

```bash
python3 pipelines/phase1_ingest/generate_sample_exports.py
```

Do not commit files containing real reviewer PII from production exports unless your course policy allows it.
