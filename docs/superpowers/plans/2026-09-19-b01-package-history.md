# B01 package history implementation plan

**Goal:** Deliver the authorized B01-only dashboard with three real Nemotron analyses, two adopted fictional amendments, and a final unresolved detection in red. Preserve manual event attribution and ingest company updates automatically.

**Architecture:** Keep the existing Python standard-library server. Add one B01 page, a dedicated SQLite store and background ingestion worker, a borrower-specific Nemotron adapter, and synthetic scenario fixtures. Existing CedarBridge routes and state stay intact. No Git repository is present; no commits or worktrees are created.

**Spec:** The user's approved branching history concept and request in this task. B01 is FluxRail Workflow, Inc.; original agreement is B01-CA-2026-01, fixed interest 9.25%, 11 covenants, four approved underwriting claims. Every source is synthetic. Model inputs are restricted to B01 origination files plus evidence available by each review date and the then-effective amendments. Evaluator and authoring files must never be model inputs.

## Ownership

- Scenario author: `realitycheck/b01_scenarios.json`, `docs/b01-scenarios.md`.
- Model implementer: `realitycheck/b01_model.py`, `realitycheck/test_b01_model.py`, `realitycheck/prepare_b01_demo.py`, recorded `b01_seed.json`.
- UI implementer: `realitycheck/b01.html` only.
- Root: `realitycheck/b01.py`, `realitycheck/test_b01.py`, integration in `app.py`, and documentation/verification.

## Data and UI contract

`GET /api/b01` returns borrower, baseline profile, profile_provenance, versions, events, current_version, current_profile, feed, pending_proposal and presentation. Versions contain effective dates, complete operative clauses/definitions, authored before/after changes and fictional amendment instruments. Model-generated baseline assumptions have B01-specific IDs, exact evidence and explicit/inferred labels. Current assessments are derived from dated event findings without rewriting baseline claims.

Events carry identity, source availability, review date, source kind, evidence paragraphs, selected package version, queued/processing/completed/failed status, actual model analysis and an adopted/pending/dismissed decision. Sources and results persist in SQLite. The three seeded events are presentation history; manual events append to history, never replace it. Original version and past events remain readable.

`POST /api/b01/events` validates typed evidence and queues it. `POST /api/b01/ingest` accepts the same dated source format for company database enrichment. Local `realitycheck/b01_inbox/*.json` files enter the same queue automatically using a content fingerprint; repeated unchanged files do not duplicate analyses. The worker processes queued rows outside database transactions, records unavailable states honestly, and resumes queued work after restart. The page polls status rather than claiming simulated ingestion is live external monitoring.

`POST /api/b01/decision` accepts an event ID, adopt/dismiss action, reason and effective date. Adoption is allowed only for the pending authored proposal, against its actual parent version, with no backdating before evidence/review. The UI displays the complete before/after terms before adoption. The root must not adopt the third proposal during verification. Dismissal means keep the existing package and retain the detection history.

## Tasks

- [x] Author three dated scenarios and two signed-in-simulation amendments; create a third draft proposal without activating it. First: S1 compatibility remediation failure. Second: qualifying S2 outage with timely reporting, prompting stronger prospective protections. Third: outage captured only by amended S2 thresholds, followed by a missed notice; retain distinction between reporting noncompliance and formal default.
- [x] Write model boundary tests before implementation for B01-only sources, exact citations, IDs, amendment version context, availability cutoff and explicit unavailable behavior. Generate the profile through Nemotron. Analyze each event sequentially against the correct version, save actual outputs and provenance, and adopt only the first two synthetic amendments after successful detections.
- [x] Write store tests first: missing seed state, queue deduplication, historical version selection, future-evidence rejection, immutable baseline, third proposal staying pending, stale/invalid adoption rejection, and preserved original seed events after manual analysis. Implement SQLite storage and one background worker with bounded hosted requests.
- [x] Build the timeline with date-scaled paths, two completed divergences and a third red marker, dimmed unpursued alternatives, clickable details, original/current terms and borrower-specific assumptions. Show exact evidence and recorded model provenance. Manual attribution remains available for presentation.
- [x] Integrate `/b01` and B01 APIs in the server, start the worker only in server main, and keep existing APIs working. Validate Python/JavaScript syntax, meaningful automated checks and the original tests.
- [x] Run a live source-file ingestion smoke test without adding an unintended fourth historical divergence, inspect the browser at desktop and narrow widths, verify node switching and manual-event errors, leave the final detection unresolved, and open the demo for the user.

## Verification boundaries

These are fictional amendments authorized by the user, not actual lending decisions or signed real contracts. Hosted output is saved exactly and traceability validated; model interpretation is still labeled as such. Report misses or outages rather than substituting authored answers. Do not change B01's source package or the other 29 businesses. No automatic general-purpose contractual amendment is implemented.

## Completion evidence

Final demonstration: http://127.0.0.1:8013/b01. Exactly three recorded Super 120B analyses, two adopted amendments, v1.2 active and v1.3 pending. Forty offline tests passed, original engine/parser checks passed, JavaScript syntax passed, and desktop/narrow browser checks passed. The final served page was visually inspected after loading the reviewed seed. A genuine background-ingestion smoke test in a temporary database returned no impacts for a routine archive update. Known model wording errors are annotated separately without rewriting raw outputs; see `docs/b01-demo-verification.md`.
