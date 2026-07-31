# AGENTS.md - Project Commands

## Rule source precedence (mandatory)

For this repository, project rules must be interpreted in this order:

1. Official organizer materials: `01-de-bai.md`, `02-guide.md`,
   `03-template-ai-spec.md`, `04-rubric.md`, `README.md`, and organizer
   checkpoint/FAQ/data-policy material supplied by the user.
2. The user's current project instructions, only where they are compatible
   with the official organizer materials.
3. Internal project documents such as `spec.md`, `PROJECT_RULES.md`, this
   `AGENTS.md`, and implementation conventions.

- A more specific official checkpoint/rubric requirement takes precedence over
  general official guidance. A later explicit organizer clarification takes
  precedence over older general wording.
- Never use a "stricter internal rule" to override or remove an option that the
  official materials explicitly permit.
- If a user-proposed or internally added rule conflicts with official
  materials, discard or revise that internal rule and preserve the official
  requirement. If two official sources genuinely conflict and neither is more
  specific or newer, report the conflict instead of silently choosing one.

## Git write policy (mandatory)
- Never run `git add`, `git commit`, `git push`, create a tag, or open a pull
  request unless the user explicitly asks to execute that exact Git action in
  the current turn.
- Implementing, testing, running locally, deploying locally, reviewing, or
  drafting a commit message does not authorize any Git write operation.
- If the user asks to draft or prepare a commit message, provide the proposed
  message only; do not commit unless they separately and explicitly request it.
- Leave completed changes uncommitted and report that status to the user.

## Deploy
- **Render (manual, explicit request only):** `git add . && git commit -m "message" && git push origin main`
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
- Keep the fixed Study Pack slice, citation validation, real-AI requirements
  for CP3 and the claimed Working path, declared mock boundaries, data security
  rules, and frozen quality bar from the official and project Markdown files.

## Data access and trust boundary (mandatory)

Access to course data is a limited privilege, not permission to own, publish,
redistribute, or reuse it outside the hackathon. These rules cover the official
data pack and every raw or derived copy of Chatlog AI Tutor data, its data
dictionary, lecture transcripts, Discord logs, exports, caches, traces, and
analysis artifacts.

1. **Allowed data only**
   - Per the official materials, use either the authorized hackathon data pack
     or clearly labelled self-generated synthetic/fake data. Do not use real
     personal data from outside the reviewed pack.
   - Synthetic/mock data is permitted for CP2 prototypes and other boundaries
     explicitly allowed by the official guide. It must be disclosed and must
     never be presented as observed evidence, a real user response, a manual
     review result, or measured production behavior.
   - Do not enrich it with unrelated personal data or reuse course data for
     another product, benchmark, or purpose.

2. **Discord is observation-only**
   - Observe or survey Discord only within the course scope.
   - Present only aggregated, anonymized insights. Do not reproduce user-level
     logs, handles, message histories, or identifiable quotes.

3. **No distribution or submission commit**
   - Do not share course data outside the course, post it on social media,
     attach it to public issues/PRs, or expose it through a public endpoint.
   - Do not add or commit the data pack, raw extracts, or reconstructable
     derived copies to the submission repository. A local working copy may be
     used only for the authorized build/evaluation workflow.
   - If protected data is already tracked or appears in a proposed Git change,
     stop and report it; do not publish or rewrite history without explicit
     user authorization.

4. **No re-identification and no secrets**
   - Never infer, guess, link, or attempt to recover identities from anonymized
     data, including by joining it with other sources.
   - Never place a real API key, credential, token, or secret in source code,
     Git, screenshots, logs, traces, fixtures, or generated artifacts. Read
     secrets from the runtime environment only.

5. **External tools: minimum necessary**
   - Before sending protected data to any external AI or other third-party
     tool, verify its data-retention and training/use policy for the selected
     account or API. If that policy has not been verified, stop and ask.
   - Send only the smallest selected source required for the current task;
     never upload the whole data pack, bulk chat/Discord logs, or unrelated
     sources. A full selected transcript is permissible only when it is
     necessary for the requested complete Study Pack and the provider policy
     has been verified.
   - For Google AI Studio/Gemini free or unpaid service, follow the official
     guide's boundary: send only clearly synthetic/fake data or the authorized
     data pack, never unrelated real-person data. Because unpaid-service terms
     may permit product-improvement use or human review, verify the current
     policy and apply the minimum-necessary rule before sending any protected
     data-pack content; if that cannot be confirmed, use synthetic/fake data.
   - Do not include direct identifiers, secrets, or unnecessary metadata in an
     external request.

6. **Deletion after the event**
   - When the organizer requests deletion after the event, remove all local and
     hosted copies within the stated scope, including downloads, temporary
     files, caches, exports, traces, and derived artifacts that can reconstruct
     protected data.
   - Because deletion is destructive, first resolve the exact targets and
     confirm the organizer/user request; then report what was deleted and
     whether any authorized backup or hosted copy remains.

## Product direction lock (mandatory)

The current product direction is the source of truth for all future work:

- **Track:** C / open track, new feature: `Study Pack 10 phút`.
- **Specific executor:** a course learner who has just completed one lecture
  and needs to review its important content before a quiz.
- **Core job:** review the important knowledge from one lecture, actively recall
  it, and see a transparent source-bounded answer-match result for the current ten-minute session
  without manually searching the whole source again.
- **One-sentence slice:** one learner selects one lecture transcript and the
  objective `Ôn quiz trong 10 phút`; AI proposes five key points and five
  active-recall questions; the learner types an answer to one cited question at
  a time, receives a source-bounded semantic match against the answer and
  cited evidence in the current HITL draft, and retries a below-threshold question
  after one intervening question during a ten-minute review session.
- **Automation boundary:** `Augment`. AI proposes; deterministic schema and
  citation checks reject unsupported output; the teacher can edit, add,
  delete, reorder, regenerate one question, and approve. AI must not make an
  unreviewable final educational decision.
  Teacher review is a safety/approval layer, not a second primary product job;
  the main story and demo must remain the learner's ten-minute review flow.
- **Recall-session extension (user-approved before CP4):** the learner sees one
  question at a time and must type an answer before seeing the cited answer.
  A model compares that attempt only against the reference answer and question
  citations in the current HITL draft; it returns a transparent match
  score, feedback and citation codes. `>=60%` advances; a lower match is
  reinserted after one other question. The displayed rate is local to that
  session only, never an AI judgment of learner capability or an official quiz
  score. It must not be persisted as learner history.
- **Frozen quality bar:** at least 85% of the full golden set passes all defined
  dimensions, 100% citation codes are valid, and zero ungrounded claims are
  shown as fact. Never lower or reinterpret this bar to fit observed results.
- **Non-goals:** no free-form chat, official quiz answers, automated learner
  ability scoring or proficiency labels, long-term personalization/history,
  VLearn or Discord integration, fabricated knowledge, fake login/analytics/
  feedback, or unrelated feature expansion. Source-bounded answer matching for
  the current review session is allowed; it must say that it is not an official
  score or capability assessment and must not be persisted as learner history.

### Direction check required for every request

Before acting on any user request, compare it with the executor, job,
one-sentence slice, automation boundary, non-goals, evidence obligations,
quality bar, and current checkpoint gaps above/below.

- For repo/product work, include a concise `Direction check` in commentary or
  the final handoff: `aligned`, `supports a checkpoint`, or `risks drift`.
- If a request only fixes correctness, security, groundedness, evaluation,
  validation, or demo reliability, treat it as aligned.
- If it adds another user, job, AI decision, output type, integration, or
  unsupported claim, identify the exact drift and its checkpoint/rubric impact
  before implementation. Do not silently broaden the product.
- A direction change requires an explicit user decision plus updates to
  `spec.md` sections 1, 2, 4, 5, 6, 7, and 9 as applicable. Preserve the
  rejected prior direction and reason rather than rewriting history.
- For a request unrelated to the product/repository, mark the direction check
  as not applicable; do not force product scope into unrelated answers.

## Checkpoint acceptance gates (mandatory)

The official checkpoint requirements, deadlines, submission windows, and
lateness rules remain authoritative. Do not distract an unrelated task with
schedule warnings, but never state or imply that an official deadline does not
apply.

### CP1 — Canvas is seven concrete lines

1. Selected track/direction.
2. One specific job executor, never “learners in general”.
3. One pain sentence: who is doing what, where they get stuck, and the
   consequence.
4. One or two initial pieces of evidence, expressed as reproducible counts or
   verbatim sourced statements—not team opinion.
5. A one-sentence slice containing one user, one job, one AI decision, and one
   result.
6. Automation level plus one cost-of-error reason.
7. At least three intended external testers and named ownership of each work
   area. “The whole team does everything” is not an acceptable assignment.

### CP2 — The main flow is clickable end to end

- A user must be able to start at the entry screen, provide/select the source,
  trigger the action, receive a result, and complete the core flow.
- A beautiful static screen, disconnected screens, or a submit button that
  does nothing does not pass.
- The official guide permits Sketch/Mock and clearly labelled synthetic/fake
  data at CP2; AI is not yet required at this checkpoint. Do not present a CP2
  mock as a Working or measured real-AI flow.

### CP3 — Real AI plus the first complete measurement

- The central AI decision must run live on allowed inputs; it must not return
  one hard-coded answer, support only pre-arranged cases, or rely on screenshots
  of an older run.
- Golden set has at least 20 cases, covers normal, rare, and all four
  product-specific failure classes, with at least two difficult cases per
  class.
- Run the whole set and retain every case, including failures. Report the
  honest numerator/denominator and percentage. A low truthful result passes the
  evidence requirement better than an unsupported high claim.
- Full protected outputs/traces remain in ignored private storage; committed
  artifacts contain reproducible hashes, methods, counts, labels, and short
  permitted excerpts only.

### CP4 — Spec and product decisions are concrete

- Evidence meets path A or B and has its complete log/method.
- Impact table compares at least three candidates and preserves rejected ideas
  with reasons.
- Four failure classes and at least eight scenarios are written specifically
  for Study Pack, not copied definitions.
- At least four HAX/PAIR principles point to exact implemented locations or
  behaviors.
- Numeric quality bar remains frozen at the value in `spec.md`.
- After CP4, do not add new features. Prioritize core fixes, safety, eval,
  validation, and demo reliability. A documented failure or validation issue
  may justify fixing the frozen feature, but not silently expanding scope.

### CP5 — Verification, user validation, and timed dry run

- At least five people outside the team perform a realistic task without being
  coached. Keep specific tester identity in an authorized private log; a public
  artifact must use consented or pseudonymized identifiers.
- Preserve concrete observations and verbatim quotes, including criticism.
  “Five people tried it and everyone liked it” is not evidence.
- Record the change made from feedback, or a reasoned decision to keep the
  behavior unchanged.
- Complete a timed demo dry run.
- Every member must be able to explain their named contribution and one real
  failure; AI-generated code does not remove this responsibility.

### CP6 — Evidence-led live demo

- Six-page story: user/job with evidence; three-candidate decision; slice,
  automation and live demo; full-set result versus frozen bar plus a meaningful
  failure; user-validation quotes and resulting change; next priorities tied to
  unresolved evidence/failures.
- Demo one normal case and one difficult/failure-handling case. Be ready for an
  unfamiliar judge-provided input; do not rely on three prepared happy paths.
- Every member speaks and can answer questions about their work.

## Evidence, FAQ, and judging guardrails

- Every quantitative claim needs all three parts:
  1. **Number:** numerator/denominator and percentage where relevant.
  2. **Meaning:** what extra work, loss, or risk the number creates for the
     specific executor.
  3. **Counting method:** source, filter, denominator, classification rule, and
     a reproducible script/log.
- Do not copy the slide example `582/1.261`; it is a demonstration of evidence
  shape, not evidence for Study Pack.
- “Many”, “users seem to want”, or team sentiment is not evidence. Lexical
  rules are audit signals until manually reviewed.
- Honest numbers are rewarded. Never hide failed cases, cherry-pick easy
  examples, change labels mid-run, or report 100% from a partial set.
- If all validation feedback is praise, the session is not considered
  successful: assign a harder task or test with different people.
- General FAQ constraints: teams normally have 3–5 members; an open topic is
  acceptable only with a real pain point and evidence; the pitch format is
  approximately five minutes plus Q&A; Discord use is observation/survey
  within the course and must be anonymized; investment judging uses up to 100
  reasoned points and no self-investment. Apply these together with the
  official permission to use the data pack or clearly labelled self-generated
  fake data.
- Optimize the pitch to withstand questions and unfamiliar cases, not merely
  to receive applause.

## Current checkpoint gaps (verify before claiming completion)

This list is a baseline, not permission to fabricate missing evidence. Recheck
the actual files and update it only when real artifacts exist.

- CP1: member names/ownership and at least three willing external testers are
  not yet documented in the current spec.
- Evidence: both 60-row manual-audit reviewer files currently have zero filled
  `reviewer_label` and `reviewer_note` fields; machine lexical counts must not
  be presented as manually validated conclusions.
- CP3: active-corpus full-run `run_20260731_103502` executed 22/22 cases with
  real Gemini calls and passed 22/22 deterministic gates. Gia Quốc marked all
  16 generated Study Packs `pass` for groundedness, relevance and active recall
  in an approximately 11:00–12:45 ICT review window; the run therefore records
  22/22 = 100% against the frozen 85% bar. Preserve the earlier AI-assisted
  3/16 precheck as a documented disagreement, not as a rewritten result. The
  current artifacts also remain uncommitted until the user explicitly
  authorizes the required Git actions.
- Recall-session interaction: scheduler unit tests cover the `missed → one
  intervening question → retry` rule, but the earlier 22/22 generator run did
  not measure this later UI behavior. It needs fresh CP5 user validation; do
  not present the old run as evidence of learner-session usability.
- CP5: `validation/` contains only a scaffold README; there are not yet five
  real external-user logs, resulting changes/keep decisions, or a timed dry-run
  artifact.
- CP6/submission: no final slide deck or individual reflection artifacts are
  currently present.
- Security: protected data remains in the public Git history and the old Render
  deployment remains publicly reachable until separately remediated. Do not
  describe the deployment as compliant merely because the working-tree fix
  exists.
