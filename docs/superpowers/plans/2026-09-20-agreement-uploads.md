# Agreement uploads and report discovery

**Goal:** Accept a new company's agreement documents, prepare its workspace with genuine Nemotron analysis, and reveal new report evidence after analysis succeeds.

**Architecture:** Reuse the stdlib HTTP server, existing company snapshots, SQLite event queue, document parser and Nemotron profile/attribution validation. The landing page polls company onboarding status; the workspace polls stable report event IDs. Processing results are persisted, while the completion notice and graph reveal are presentation state.

**User-approved behavior:** White and dark-blue UI; "Add New Credit Agreement" on the agreement-list landing page; tinted noninteractive pending cards; v1.0 shows the inception memo and 10-K in Source records, alongside the origination library and contractual provisions; "Add new reports" beside the network heading; spinner during processing; completion notice before new source dots and verified links animate in. Missing inception documents are not invented.

- [x] Backend: isolated uploaded companies, persisted onboarding status, validated files, real hosted extraction/profile creation, report extraction and existing attribution queue, failure recovery. Test with temporary stores and substituted hosted responses; preserve saved demos.
- [x] Landing: upload portal, immediate pending card, polling, ready navigation and actionable errors. Exercise browser state transitions with explicit API fixtures.
- [x] Workspace: three labeled columns with only memo/10-K inception sources, report-upload dialog, processing indicator, completion notice and graph reveal, original document links, no invented terms. Preserve hover, inspector, drawer, history and replay behavior.
- [x] Integration: run backend and browser regressions, verify white desktop/mobile UI, restart the existing local server only after code validates, and check actual GET routes. Do not modify existing saved records or claim fixture tests made live model calls.

**API contract:** POST /api/companies with name/effective_at/files; GET /api/companies exposes status/stage/error; POST /api/<cid>/upload returns a stable queued event_id; GET /api/<cid> exposes processing events and uploaded_documents. Uploaded IDs use U plus 12 hex characters and source_mode uploaded_agreement. Root is the agreement landing page; the old packet demo remains at /legacy.

**Verification:** 74 offline backend tests pass. Landing, report-upload and read-only workspace browser checks pass, including exact memo/10-K sources at H01 origination, pending/failed/ready states, completion-before-reveal, reduced motion, replay, drawer and mobile layout. H01/B01 saved records are unchanged across restart. A genuine isolated hosted run extracted three verified clauses; the initial profile response exposed a malformed shape and conflicting schema defaults, corrected without weakening validation. A subsequent hosted profile returned five source-verified assumptions and one relationship with no validation warnings. These checks establish integration behavior, not the accuracy of credit judgments.

The subsequent genuine uploaded report completed with Nemotron: four attributions and three source-verified covenant assessments, no analysis error. All hosted smoke data is synthetic and isolated in `tmp/upload-smoke-retained`; no test company was added to the live landing page. The live server was restarted with the final implementation and GET/browser checks passed afterward.
