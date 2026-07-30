# AGENTS.md - Project Commands

## Deploy
- **Render:** `git add . && git commit -m "message" && git push origin main`
- Docker build: `docker build -t study-pack . && docker run -p 8000:8000 study-pack`

## Test
- Python tests: `python -m pytest codebase/ -v`
- Syntax check: `python -m py_compile codebase/*.py`
- Frontend check: `node --check codebase/web/app.js`

## Run locally
- Web app: `python codebase/web_app.py --port 8000`
- CLI: `python codebase/main.py --transcript data/study-pack-corpus/transcript/transcript-10-clean.md --output pack.json`

## Active transcript corpus (mandatory)
- The product's active corpus is `data/study-pack-corpus/transcript/`: `T10`
  Paper and `T11`-`T15` for Day 01-05.
- Preserve `data/vlearn-pack/transcript/` unchanged for audit/history. Never
  delete, rename, or overwrite those six legacy transcript files.
- Web and current eval paths must default to the active corpus only. Legacy
  transcripts may be read only by explicitly targeted regression/audit tests.
- Every non-empty line in the combined source must remain once and in order as
  a `[Txx-NNN]` segment. Never summarize, paraphrase, fabricate, or silently
  truncate corpus content during ingestion.
- Use `data/study-pack-corpus/manifest.json` and
  `python tools/build_study_corpus.py <source.txt>` to verify/rebuild the corpus.
- Keep the fixed Study Pack slice, citation validation, real-API-only rule,
  data security rules, and frozen quality bar from the project Markdown files.
