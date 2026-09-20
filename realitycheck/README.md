# RealityCheck demo

Know which underwriting assumptions need another look.

A private-credit analyst loads a dated reporting packet, sees each approved underwriting assumption marked **Supported / Weakened / Contradicted / Insufficient evidence** with a separate **credit implication** and **suggested action**, opens the exact quoted evidence, and records an accept or override. CedarBridge and B01 are existing synthetic demos (see `../Synthetic-Covenant-Framework.md`). **The presentation scenario is Crocs (`/h01`): real business context with a synthetic private-credit scenario.** Crocs is excluded from the separate historical benchmark, which uses actual SEC-filed company and amendment histories.

## Run

```
cd realitycheck
python app.py            # http://localhost:8000  (Python 3.10+, stdlib only)
python test_engine.py    # prints "ok" and "parse ok"
python -m unittest test_attribution test_event_api  # event validation and API checks; no hosted calls
python eval.py           # baseline vs Nemotron against the frozen answer key
```

`NVIDIA_API_KEY` is read from `.env` (this folder or the parent). With it, two Nemotron models are used through the hosted NIM endpoint at `integrate.api.nvidia.com`:

| Role | Model id | Verified live |
|---|---|---|
| Document parsing (upload -> text) | `nvidia/nemotron-parse-2.0` | 2026-09-19, 1.5 s per page |
| Semantic assessment | `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | 2026-09-19, 5 to 20 s per packet |

Override with `NEMOTRON_PARSE_MODEL` and `NEMOTRON_MODEL`. Without a key the original packet assessment runs the extraction-plus-rules baseline and labels it on screen; the event-attribution flow instead records an explicit unavailable/unassessed result. `nvidia/nemotron-3.5-lightning-30b-a3b` was tried and timed out at 90 s; the hosted endpoint returns 503 under load, so `eval.py` retries three times and reports any packet it could not score.

## Selected presentation: Crocs (`/h01`)

The landing page at `/` lists saved agreements and offers **Add New Credit Agreement**. Choose the company name, optional inception date and documents; mark each inception document as agreement, memo or 10-K. A pending company card stays tinted and disabled until genuine Nemotron clause extraction and profile generation finish. Failed processing stays visible and can be retried using the saved documents. Uploaded companies have separate storage under `uploads/`; their terms and sources do not come from the saved demo scenarios.

At inception, **Source records contains only the memo and 10-K**, when provided, alongside the library and contractual provisions. **Add new reports** beside the network heading uploads subsequent evidence. Its spinner tracks the persisted analysis job; a successful result shows **Analysis complete!** before the new source dot and verified links animate into the network. Failed analyses show an error and do not reveal findings. Original uploaded documents can be downloaded from the source library. The completion animation respects reduced-motion preferences.

Both upload forms let you **Add files** in separate batches and **Delete** individual selections before uploading. Existing selections and agreement document types stay in place as you add files; identical files are not added twice. Canceling the file picker or a failed submission keeps the selected list available to edit and retry.

Uploads accept PDF, images, TXT and Markdown: up to 10 files, 12 MB per file, 20 MB total and 300 pages per PDF. Embedded PDF text is read directly with page citations; Nemotron Parse handles images and pages without usable text layers, limited to 20 OCR pages per PDF. Onboarding accepts up to 600,000 extracted characters across its documents, including full annual filings such as the 123-page Duolingo 10-K. Memos and 10-Ks are optional supporting evidence; only documents labeled Credit agreement supply operative clauses and agreement text. All supplied sources remain available for profile generation and quote verification. Later report uploads retain their separate event-text limit. Agreement preparation extracts up to 24 source-verified material clauses, so the resulting provision list is a subset of the supplied contract. Company and report status survives server restart. API: `POST /api/companies`, `POST /api/companies/<id>/retry`, `POST /api/<id>/upload`, and `GET /api/<id>/documents/<filename>`. The earlier CedarBridge interface remains at `/legacy`.

`python -m unittest discover -p 'test_*.py'` runs the offline backend checks. With Playwright available, `node verify-landing-upload.cjs` and `node verify-report-upload.cjs` verify upload UI transitions with explicit API fixtures, while `node verify-workspace.cjs` exercises the saved demo read-only.

Built following the [Crocs demo plan](../RealityCheck-Crocs-Demo-Plan.md). Open **http://127.0.0.1:8013/h01**. The page is titled **“Crocs — hypothetical private-credit scenario”** and carries the disclosure that company background is sourced while financial figures, loan terms, reports and scenario events are fictional.

Identity `H01` (an `H` prefix marks a hypothetical facility set at a real company). State is separate from B01 and from `benchmark/`: `h01_seed.json`, `h01.sqlite`, `h01_reports/`, `h01_attempts/`. The packet is authored and arithmetic-checked by `../hypothetical-scenarios/build_h01.py`; `test_h01_scenario.py` re-derives the figures, deadlines, amendment chain, labels and isolation.

The live workspace uses a white canvas with dark-blue accents in `b01.html`, shared by the company routes. The network groups unlabeled nodes and connections under Source records, Assumptions and Contractual provisions; hover or keyboard focus reveals a summary, and selecting a node opens its collapsible inspector. Agreement history, recorded replay and the selected-record inspector share a right-hand drawer that starts closed. The edge button slides it in or out; selecting a node also opens it. Closing the drawer preserves replay, selection and graph position. Keyboard Escape closes the drawer after any active dialog, and reduced-motion preferences disable the animation. Selecting a history event focuses the network on that report and its applicable agreement. Normal scrolling reaches drift detection, expandable underwriting context and the source library below; use the zoom buttons or Ctrl/Command-scroll to zoom the graph. All views respect the replay-filtered API snapshot. Report introduction, Add information and amendment review remain connected. `node verify-progressive-workspace.cjs` runs the browser regression with Playwright available; it blocks browser writes and checks that saved H01/B01 records are unchanged.

| Review | Operative terms | Report | What Nemotron found | Shown as |
|---|---|---|---|---|
| Nov 18, 2026 | v1.0 | Routine month | All assumptions supported | Report marker |
| Dec 14, 2026 | v1.0 | Shipping disruption (38% of volume, 24-day delay) | Supply assumption contradicted; notice timely | Detection 1; simulated v1.1 adds routing visibility and recurring forecasts |
| Jan 19, 2027 | v1.1 | Rerouting and surcharge update | Supply assumption improves from contradicted to weakened; forecasts delivered | Report marker (mitigation is not a new detection) |
| Feb 22, 2027 | v1.1 | Wholesale order cut, 14.2% aged inventory | Inventory-to-cash assumption contradicted | Detection 2; simulated v1.2 adds aged-inventory and weekly cash reporting and pauses expansion spending |
| Apr 19, 2027 | v1.2 | Direct sales recover; March cash report | Model derived $33.6 million Unrestricted Cash from the stated figures; C01 noncompliant; good sales news did not offset it | Red, pending. The v1.3 draft (time-limited floor relief) is left for the user |

The analyses are genuine saved Nemotron responses shown as a recorded replay, not fresh inference. Reviewer notes sit beside the model's wording and are listed in `h01_review_notes.json`; withheld findings, the one revised report (`H01-D03`, first attempt kept in `h01_attempts/`) and both token-budget retries are visible. The amendments are scripted scenario decisions, not model output. `h01_drift_2027-04-19.json` holds the candidate-package comparison: no drift from origination evidence alone, material drift with the five reports (C04, C05, C06), and a withheld C01 change whose direction (tighten) is the opposite of the authored relief draft.

To rebuild: `python ../hypothetical-scenarios/build_h01.py`, `python prepare_b01_demo.py H01` (hosted calls), review, `python finalize_scenario.py H01 --complete`, `python run_b01_drift.py H01 2027-04-19` then `--attach`. `rerun_scenario_event.py` re-validates or re-runs one report and archives the earlier attempt. Rehearse introductions and decisions on a copy of the folder on another port, not on the saved `h01.sqlite`. Crocs is never added to historical benchmark inputs, evaluators or scores.

## B01 package-history demo

Run `python app.py 8013` and open **http://127.0.0.1:8013/b01**. The original CedarBridge demo remains at `/`. B01 is FluxRail Workflow, Inc.; it uses its own origination agreement and underwriting memo from `synthetic-credit-portfolio/model_inputs/B01-fluxrail-workflow-inc/`. Its 11 actual clauses and four approved claims are separate from the generic 30-clause library. Two additional generated assumptions are marked working AI inferences.

The B01 page reads the recorded Nemotron profile and three analyses from SQLite. The timeline presents the original package, two adopted fictional amendments and a final unresolved detection. Select a circle to inspect the dated event, attributed assumptions, operative covenant, verified source quotations and amendment changes. Dim branches show terms that were not continued. The default window emphasizes the three reviews; **Full history** includes origination. Interest remains 9.25% throughout: the paths represent package versions, not a yield chart.

| Review | Operative terms | Event and intended review distinction | Package decision |
|---|---|---|---|
| July 13, 2027 | v1.0 | Connector remediation deadline missed; S1 noncompliance is distinct from formal default | v1.1 effective July 20, after remediation; stronger prospective S1 protections and a narrow historical waiver |
| August 10, 2027 | v1.1 | Six-hour outage affecting 12% of revenue; S2 activated and notice delivered on time | v1.2 effective August 23; lower prospective incident thresholds and recurrence reporting |
| September 10, 2027 | v1.2 | Three-hour outage affecting 7%; captured by amended S2 and notice deadline missed | Red, pending. The user reviews the proposed v1.3 changes and chooses whether to adopt or retain v1.2 |

These are authored synthetic events and amendments, not model-generated contractual instruments. The model's actual recorded interpretation appears separately. Origination files are unchanged, no evaluator answer files enter model requests, and later amendments cannot become operative before their effective dates. Covenant noncompliance, exposure of an underwriting assumption and a formal Event of Default are separate findings.

**Additional companies.** The store, routes and page are company-scoped. A company exists once `realitycheck/bNN_seed.json` is present: it gets its own `bNN.sqlite`, `bNN_inbox/`, workspace at `/bNN` and API at `/api/bNN` (`/events`, `/ingest`, `/decision`); `GET /api/companies` lists them. To add one, author `bNN_scenarios.json` in the B01 format (optional `original_terms`, `presentation`, and per-event `allow_no_impact` for reports expected to have no material effect), run `python prepare_b01_demo.py BNN` to make the hosted profile and event calls, review the saved seed, then mark it `complete`. Each database rejects updates addressed to another borrower. Only B01 is seeded today.

## Historical benchmark on real companies (public SEC filings)

FluxRail is the existing fictional demo; Crocs (`/h01`) is the real-name synthetic presentation. The historical cases described in [the benchmark plan](../RealityCheck-Benchmark-Testing-Plan.md) are shown at `/benchmark` and retain their actual report/amendment histories under `benchmark/`. Those records and results are separate from both demo scenarios. Crocs is not a historical benchmark case.

> RealityCheck uses publicly available SEC filings. Reconstructed assumptions and AI-generated candidate packages are hypothetical. Actual lender amendments are historical evidence of responses, not validated prescriptions. This benchmark does not reproduce a complete private underwriting file or establish predictive performance. No endorsement by any company, lender or the SEC is implied.

**Primary mode: strict blind historical replay.** Nemotron starts from the original executed package and receives each later report on the date the SEC accepted it. Every actual amendment, waiver and description of one is withheld, even once public, and the original package stays the only contractual baseline. At each checkpoint the framework workflow attributes the report to its reconstructed assumptions and then drafts a complete candidate package; an origination-only control under the same model, prompt and guidelines separates new-evidence changes from drafting preference. A direct-review comparator gets the same model, evidence, package and guidelines without the assumption framework. `benchmark_blind.py <case> lock` hashes the outputs; `benchmark_evaluate.py` refuses to run on unlocked or modified outputs and is the only module that opens the evaluator collection.

| Case | Facility and period | State |
|---|---|---|
| `R01` iRobot / Carlyle | $200M senior secured term loan of July 24, 2023; 9 blind checkpoints, November 2023 to May 2025 | Blind inputs, exclusion log, evaluator collection and reference judgments built; hosted runs started September 19, 2026 |
| `R02` RumbleOn / Oaktree | Term loan of August 31, 2021 (term facility only, not floorplan); 7 blind checkpoints, March 2023 to August 2024 | Same |
| `R03` PetIQ / Ares | $75M term loan of January 17, 2018, restated July 8, 2019 | Source documents cached only. The one history no model run has touched |

Both prepared histories are **development histories**: prompts and validation were changed after earlier outputs for them were seen, so neither is an unseen test. Earlier rolling-mode runs, which applied each amendment once public and at five checkpoints supplied the amendment's description to the model, are kept under `benchmark/<case>/rolling/` as development records only. Reference judgments are author-prepared and disclosed as such; no independent credit reviewer was available.

**Source mode and reuse basis.** Every document is fetched from `sec.gov` by `../real-credit-cases/fetch_sec.py` (sequential, cached, descriptive User-Agent). Earnings releases are the SEC-filed Form 8-K exhibits, not copies from company websites. Each case's `manifest.json` records the URL, SEC accession, content hash, retrieval time and SEC acceptance timestamp. The SEC permits reuse of public filings ([SEC FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions)). These cases use real financial records, so they are **not eligible for the Compound track**, whose rule requires synthetic or sandbox data; they fit Xtract's public-source category.

**What is actual, reconstructed or generated.**

- *Actual public disclosure:* clause text, definitions, default provisions, report paragraphs and amendment descriptions. All are copied verbatim by paragraph locator (`extract_text.py`, `build_case.py`, `build_reports.py`); nothing is summarized or edited.
- *Reconstructed:* every assumption. No lender underwriting memo is public, so Nemotron reconstructs an assumption framework from filings available at origination. Each carries the label "reconstructed from public filings · not the lender's thesis"; an assumption survives only if at least one quotation verifies against its cited source.
- *Generated:* report analyses and covenant assessments are Nemotron interpretations. Recorded runs are replays of saved hosted responses and are labeled as such.
- *Observed historical response:* each amendment is recorded as what the lender actually did, with the company's own description. It is not an analyst decision and not a recommended remedy.

**Dates.** A report becomes available to the model on the date the SEC accepted the filing that carried it, never the period end or execution date. Examples that limit what can be claimed: iRobot's full-year 2024 going-concern results and the filing disclosing Amendment No. 1 were accepted eight minutes apart, and RumbleOn's Amendments No. 6 and 7 became public five and two months after execution.

**Missing inputs stay missing.** Monthly compliance certificates, lender covenant calculations and iRobot's Schedule 7.07 step-down amounts are not public, so covenant compliance is reported as `insufficient_evidence` rather than estimated. iRobot's Amendments 1 and 3 are filed as redlines and RumbleOn's Amendment 8 exhibit runs deleted and inserted text together, so their operative text is not extracted. Each case lists its gaps in `clauses.json`. Blind runs use a separate `missing_inputs_blind` list, because a note that names a later amendment would itself leak it.

**Hindsight.** Nemotron may already know these companies' outcomes from pretraining. Date-filtered inputs and a prompt instruction do not remove that. Treat these replays as evidence that the mechanism works on real documents, not as proof of early warning. Later events, including iRobot's December 2025 Chapter 11 filing, are excluded from the packets.

To rebuild a case, from `real-credit-cases/`: `python fetch_sec.py <case>`, `extract_text.py`, `build_case.py`, `build_blind_inputs.py`. Then here: `python benchmark_blind.py R02 realitycheck`, `python benchmark_blind.py R02 direct_review`, `python benchmark_blind.py R02 lock`, `python benchmark_evaluate.py R02`. Each makes hosted calls except `lock` and the evaluation.

**Background company updates.** POST dated JSON to `/api/b01/ingest`, or write a UTF-8 `.json` file into `realitycheck/b01_inbox/` while the server runs:

```json
{
  "borrower_id": "B01",
  "title": "September operating update",
  "event_date": "2027-09-12",
  "available_at": "2027-09-13",
  "review_date": "2027-09-13",
  "sources": [{
    "document_id": "B01-OPS-2027-09-12",
    "locator": "Operations review, paragraph 1",
    "text": "Replace this text with the dated company evidence to analyze."
  }]
}
```

The local worker checks files every five seconds, fingerprints their contents, queues each new revision once and calls Nemotron outside the database transaction. It saves evidence, model provenance and findings, and derives the current assumption view while retaining the original claims. Rejected input and hosted failures are visible. This is a working local file/API ingestion connection; external news, email and company data providers are not connected. Ordinary information does not amend terms automatically.

**Manual presentation.** Use **Add information** to enter a new event, or POST the same format to `/api/b01/events` (`text` is also accepted instead of `sources`). It uses the same persistent analysis queue. Source availability and review dates are required to establish the information cutoff; a missing incident date is treated as unknown. A failed hosted analysis remains recorded as failed rather than displaying invented findings. Resubmission creates a new record.

`b01.sqlite` stores the company profile, package versions, evidence, analysis queue and decisions. `b01_seed.json` is the replay seed; initialization never overwrites an existing initialized database. The final proposal stays pending until the user explicitly records a decision and reason. Adoption only applies the displayed draft against its matching parent, and creates a fictional amendment effective no earlier than the review; it does not erase the historical detection. The first two amendments were authored and adopted as part of the requested scenario.

`B01_NEMOTRON_MODEL` overrides the B01 analysis model. Otherwise the worker uses the seed's analysis model or latest successful event model, with the profile's generator as fallback. Recorded results retain the model that actually produced them. Regeneration is explicit: `python prepare_b01_demo.py` makes hosted calls and saves checkpoints; an incomplete run cannot initialize a new presentation database. Do not replace a database containing user decisions to refresh a seed.

Run `python -m unittest test_b01 test_b01_model test_attribution test_event_api` plus `python test_engine.py` for offline verification. The B01 tests use temporary databases and mocked completions; they do not submit decisions to the presentation or establish broad model accuracy. The authored scenario details are in `../docs/b01-scenarios.md`.

The final recorded B01 sequence uses **Nemotron Super 120B with reasoning enabled**. All three core detections succeeded, with visible reviewer notes correcting remaining date, threshold-boundary and scope errors in the original model wording. Forty offline tests, original engine/parser checks and browser checks passed; a genuine local-file ingestion smoke test completed without creating a false divergence. See [verification and model limitations](../docs/b01-demo-verification.md).

## Original event attribution

The event flow answers: **Which assumptions or covenant clauses does this new information affect, and what needs review?** It is separate from the original five-assumption packet assessment below.

1. Enter an event with its source availability and review dates, then analyze it. Alternatively select a reporting packet and attribute it, or upload a document; a successful parse enters the same attribution flow. Packet availability comes from the stored source, with a separate packet review date; selecting a packet does not change typed-event dates.
2. Choose the applicable covenant profile. CORE is always included; optional riders are explicitly selected. GOVERNANCE includes PC22/PC23, LIQUIDITY includes PC24/PC25, MONTHLY adds PC26, INVESTMENT adds PC29, INTEREST and CASH-COVERAGE are mutually exclusive, and REVOLVER replaces PC01 with PC30. All 30 definitions remain available for matching, with inactive clauses labeled. Selection alone does not establish that a clause is triggered or its test is due.
3. Nemotron receives the dated source text, the 24-claim working register, directed relationships, and covenant clauses/shared definitions. It proposes direct assumption evidence, downstream exposure, covenant inputs/triggers/permissions, or evidence gaps. The separate evaluator answer file is never part of this request.
4. Each proposed link identifies the assumption or clause, source quotations, risk direction, missing facts, relationship path where relevant, suggested action and adjustment. Source verification establishes traceability, not whether the interpretation is correct. Downstream exposure does not automatically contradict the downstream assumption.
5. Accept or dismiss each attribution with a reason. Decisions and events remain in the review history. This records review of the proposal; it does not edit an approved thesis or amend a covenant.

The [complete register and maps](../RealityCheck-Assumptions-and-Relationships.md) explain all 24 assumptions, 12 evaluation prerequisites, 30 clause mappings, formulas, and examples. `assumption_registry.json` is the compact runtime catalog. T01 repeats the library's approved synthetic Atlas claim; the other expanded claims are explicitly working analytical assumptions, requiring lender-specific confirmation and materiality criteria. Existing A1–A5 packet records retain their original meanings.

No linkage means **unaddressed by this event**, not supported. Invalid target IDs, wrong source locators, unsupported quotes and relationship paths are withheld with warnings. Evidence unavailable at the requested review date is rejected. If the hosted model fails or no API key is available, the record stays unassessed; the system does not invent a model answer or silently substitute keyword routing.

The event flow proposes covenant relevance and interpretations; it does not implement a full deterministic executor for all 30 authoring clauses. The original C01 calculator remains separate. New source documents or typed events trigger analysis through the app; there is no external company-news or repository watcher.

API routes: `GET /api/attribution-context`, `POST /api/attribute`, `POST /api/attribution-decision`. `GET /api/history` includes both original `assessments` and new `events`. Data stays in the local JSON state; this is a single-process demo, not a production audit/versioning database.

Verification on September 19, 2026: all 18 event/API tests and the original engine checks passed; frontend syntax and browser form/history checks passed. One hosted Atlas amendment test produced a source-verified T01 attribution and its review decision persisted. The model's proposed severity and missing-fact selection needed refinement; the final prompt's live browser test received HTTP 503, displayed all 24 assumptions as unassessed and offered retry. Hosted availability and interpretation quality therefore remain limitations; this smoke test does not establish accuracy across all 30 clauses. The new upload-to-attribution connection was reviewed in code, without repeating a live parser upload.

## Demo script (plan section 16)

1. **Thesis.** Five approved assumptions with their memo passages.
2. **Q1 2027.** All supported, C01 passes at 3.92x. Continue routine monitoring.
3. **Q2 2027.** Atlas gains a 30-day termination right while leverage is unchanged. A1 contradicted, adverse, review credit view. Click A1: original passage, new clause, "verified in source".
4. **Q2 2027 (mitigated case).** Same clause plus a signed Beacon replacement commitment. Rules baseline: A1 contradicted, mixed, request information, counterevidence in green. Nemotron missed the mitigation in testing (see below), which is itself a talking point.
5. **Q3 2027.** Certificate missing and a non-binding $7m letter of intent. A3 insufficient evidence (numbers withheld, not guessed); A5 stays supported because the deal is proposed, not executed.
6. **Upload.** Choose `samples/cedarbridge-q2-2027.png` (regenerate with `python make_sample_packet.py`). Nemotron Parse 2.0 turns the page into paragraphs with section-based locators such as "Customer contracts, para 1 (p1)". Run the assessment: A1 contradicted with the quote verified against the parsed text. A2 to A4 show insufficient evidence because no structured certificate was extracted; that is the honest answer, not a bug.
7. **Decision.** Accept or override any row. The timeline records what was available, when it was assessed, which engine ran, and what the analyst decided.

## Where Nemotron sits and why

```
PNG / JPG / PDF page                  dated packet + approved assumptions
        |                                     |                      |
 Nemotron Parse 2.0                    deterministic checks    Nemotron 3 Nano: one bounded
 -> classes, bboxes, text              (C01 leverage, share,   semantic pass -> status, implication,
 -> {locator: paragraph}                free cash flow)         action, verbatim quotes, counterevidence
        |                                     |                      |
        +----------------> validation outside the model <------------+
                 allowed labels, known assumption ids,
                 every quote must exist in the packet text
                 (unverifiable quote -> insufficient evidence)
                                      |
                numbers override prose on leverage; analyst accepts or overrides
```

Parse 2.0 request details that cost an hour to find: text part first, then `image_url` (data URL); prompt is the control-token string from the model card; `skip_special_tokens: false` is required or the bbox and class tags are stripped and the response is empty; context is 4096 tokens so `max_tokens` stays at 4000; output tags are `<x_..><y_..>text<x_..><y_..><class_..>` and are parsed with the regex from NVIDIA's `postprocessing.py`. Page headers, footers, and pictures are dropped; section headers become locator prefixes.

## Eval (plan section 17), run 2026-09-19

Four development packets, five assumptions each, 20 scored rows, frozen answer key in `data.py`.

| Engine | status | implication | action | false alerts | missed | unverified quotes |
|---|---|---|---|---|---|---|
| extraction + rules | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 |
| nemotron-3-nano-omni | 16/20 | 12/20 | 13/20 | 4 | 0 | 1 |

The rules score is not a result: the packets and the rules were written together. The Nemotron rows are the useful part. Failures found:

- **Missed mitigation.** On the mitigated case it cited the termination clause but not the signed Beacon replacement, so it called A1 adverse instead of mixed.
- **Over-flagging silence.** On three packets that say nothing about acquisitions it returned insufficient evidence for A5 and asked for information, where the rubric expects routine monitoring. This is a rubric judgment (the plan says absence of a warning is not confirmation) and is the main source of the false-alert count.
- **Label drift.** Stable leverage and cash flow were called "beneficial" rather than neutral.
- **Non-determinism.** At temperature 0 the Q3 letter-of-intent row came back "supported, continue" on one run and "contradicted, consider re-underwriting" on another. The second run treated a non-binding LOI as executed, the exact failure the plan's edge-case table predicts.
- **One fabricated quote** was caught by the source check and downgraded on screen.

## What could go wrong (and what the demo does about it)

- **Hallucinated evidence.** Quotes are string-matched against the packet; a miss downgrades the row and is labeled on screen.
- **Prose contradicting numbers.** The deterministic leverage result overrides any semantic claim on A3.
- **Proposed treated as executed.** The Q3 LOI case tests this; the rules baseline handles it by keyword, Nemotron by instruction, and got it wrong once.
- **Missing report read as good news.** No certificate yields insufficient evidence, never supported.
- **Hindsight.** Packets carry an available-at date; nothing later is used.
- **Model outage.** The failure is shown, calculations remain, the baseline runs, and the engine label changes.

## Limits

Four development packets authored by the same people who wrote the rules. They demonstrate mechanism, not accuracy. No analyst-time or early-warning claim is made. Uploaded packets have no structured metrics yet, so their deterministic rows report insufficient evidence; certificate table extraction from Parse 2.0's `Table` elements is the next step. Storage is a JSON file; the plan's Postgres/TigerData versioning and Next.js UI are the upgrade path.

AI coding tools used: Claude Code (Claude Fable 5.1) for scaffolding, data authoring, endpoint debugging, and this README.
