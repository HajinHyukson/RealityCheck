# RealityCheck — Crocs Demo Presentation Plan

**Created:** September 20, 2026  
**Decision:** The user selected Crocs as the real-company setting for the presentation demo, with a synthetic private-credit package and covenants. Crocs is not a historical benchmark case.  
**Implementation status (updated September 20, 2026):** Build steps 1 to 6 are done. The scenario is at `/h01` (identity `H01`). The packet is authored and reconciled (`hypothetical-scenarios/build_h01.py`); the genuine Nemotron profile, five report analyses and the candidate-package comparison ran and were reviewed, with reviewer notes, withheld findings, one revised report and its archived first attempt all retained; two simulated amendments are recorded and the v1.3 draft is pending; the page was inspected in a browser and a rehearsal was run on copied state. Outcomes and remaining limitations are in the progress log in the [current status](RealityCheck-Current-Status.md). Section 8's closing sentence describes this document when it was a plan only.

## 1. Scope and purpose

Build one coherent Crocs presentation that shows an original loan package evolving as new information changes its supporting assumptions. The audience should be able to follow a report into a borrower exposure, an assumption, a package concern and an analyst decision.

Crocs is the immediate presentation priority. Retain the working FluxRail/B01 application, sources, SQLite state and pending third decision as a separate existing demonstration. The earlier three-company expansion is future scope rather than a prerequisite for this presentation. This sequencing does not delete the 30 synthetic borrower packages or require a new portfolio architecture.

The [historical benchmark](RealityCheck-Benchmark-Testing-Plan.md) continues separately with its existing cases and records. Do not add Crocs scenario reports, generated proposals or simulated approvals to its input sets, evaluator answers, scores or comparison timelines. A successful Crocs presentation demonstrates the workflow; it does not improve a benchmark score or erase a recorded failure.

## 2. What is real and what is synthetic

The starting business reference is [Crocs' FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1334036/000133403626000006/crox-20251231.htm). It supports the description of an international footwear business using overseas third-party manufacturers and wholesale and direct-to-consumer sales channels. Use source dates and distinguish Crocs, Inc. from a particular brand or subsidiary when assigning an exposure.

| Material | Required treatment |
|---|---|
| Company identity and business context | Real, sourced background. Use only the business facts needed to explain the scenario. |
| Opening financial model | Entirely synthetic, with coherent debt, cash, earnings, inventory, receivables and cash-flow schedules. It is not Crocs' reported financial position. |
| Underwriting memo and lender policy | Fictional scenario documents. Explicitly approve their initial assumptions for the simulation; do not attribute them to a real lender. |
| Original loan and covenants | Synthetic instruments authored for the scenario. Do not reuse the company's real credit agreement or imply the hypothetical facility exists. |
| New information | Labeled synthetic industry reports, operating updates and management accounts. Any separate real business reference retains its source and date. |
| Nemotron profile and findings | Genuine model output about the defined scenario, with source evidence, hypotheses and uncertainty distinguishable. |
| Proposed and adopted amendments | Hypothetical scenario terms and simulated analyst decisions, visibly separated from actual company history. |

Use the title **“Crocs — hypothetical private-credit scenario.”** Display: **“Company background is sourced. Financial figures, loan terms, reports and scenario events are fictional.”** Keep those labels on report cards, divergence details, candidate packages and exports. No fictional report should imitate an authentic Crocs press release or use an actual executive as its supposed author.

Supply the same distinctions in model inputs. Nemotron must use the scenario's defined financials and covenants, not substitute remembered Crocs figures, actual financing terms or later real outcomes. An assumption approved for this simulation is not evidence of what a historical lender believed.

The [recorded source rules](RealityCheck.md#10-data-strategy) require synthetic financial inputs for Compound. The real company name does not make copied actual financial statements synthetic, and its use is not blanket certification of prize eligibility. No real financial dataset is imported as part of this plan.

## 3. Synthetic opening package

Use a hypothetical working-capital term facility supporting footwear sourcing and inventory conversion. Define the borrower and guarantor perimeter within the simulation explicitly. Do not present a brand-level model as consolidated Crocs, Inc. financial reporting.

Author a self-contained original package using the [30-provision reference](Synthetic-Private-Credit-Covenants-30.md) as a drafting aid. Elect only provisions relevant to this facility; optional and alternative clauses do not become operative merely because they exist in the generic library.

The proposed package should cover:

| Protection | What the scenario must define before model runs |
|---|---|
| Minimum unrestricted cash | Included accounts/entities, restrictions, measurement date, threshold and delivery of supporting cash records. |
| Maximum net leverage | Defined debt and permitted cash netting, covenant EBITDA and adjustments, test period, threshold and certificate. |
| Financial reporting | Monthly management accounts and cash reporting; quarterly compliance certification; deadlines and calendar rules. |
| Inventory reporting | Aging buckets, valuation basis, write-down treatment, location/in-transit status and delivery frequency. |
| Material event notice | Objective definitions for supply disruption, material order loss or other selected events, knowledge condition and notice deadline. |
| Cash forecast and remediation reporting | When an updated forecast or action plan is required, its coverage and follow-up duties. |
| Restricted payments and discretionary investment | Applicable conditions, baskets and exceptions; distinguish expansion spending from ordinary operating needs. |
| Additional debt and liens | Permitted categories and any required approvals or reporting. |
| Amendment, waiver and default provisions | Effective dates, approvals, cure/notice conditions and the scope of any waiver. |

Finalize numerical terms and the complete financial schedules during packet authoring. Reconcile calculations and review boundary conditions before presenting any model outcome. Do not fabricate missing arithmetic during inference or call a scoped clause extract a complete agreement.

## 4. Initial assumption framework

Nemotron should derive the profile from the real business reference and fictional underwriting package. The following are proposed scenario dimensions, not preloaded claims that the model must declare true:

| Assumption dimension | Evidence to author and review | Relevant relationship |
|---|---|---|
| Supply continuity | Scenario sourcing locations, lead times, alternatives and supplier commitments. | Disruption can affect availability, shipment timing and inventory planning. |
| Inventory converts to cash as forecast | Inventory aging, expected sell-through, return rights and customer payment schedules. | Slow turnover or collections may consume cash despite recorded sales. |
| Sales-channel mix provides resilience | Separate wholesale and direct-sales forecasts, margins and costs. | Stronger direct sales may partly offset wholesale weakness; quantify the same-period effect before netting. |
| Margins can absorb or recover higher costs | Freight terms, cost responsibility, pricing and any documented mitigation. | A macro freight headline does not itself establish who bears the cost. |
| Liquidity remains adequate | Defined unrestricted cash, scheduled payments and a reconciled cash forecast. | Inventory and margin pressures can converge on liquidity without being counted as independent losses twice. |
| Reporting provides timely visibility | Data availability, owners, agreed reporting periods and deadlines. | Late or incomplete reports can create an obligation issue separately from underlying financial deterioration. |

Example transmission path:

```text
Synthetic shipping report
  → scenario routes and suppliers actually exposed?
  → higher cost or longer lead time, with conditions and mitigants
  → inventory conversion / margin assumptions
  → revised cash outlook
  → relevant reporting duties and potential package review
```

Keep the original assumptions and their approval history. New information updates the current assessment, not the original source claim. Unknown exposure remains unknown. A critical concern cannot be averaged away by unrelated positive evidence.

## 5. Report history and presentation narrative

Plan a short sequence containing three substantive developments, routine information and counterevidence. The intended presentation has two reviewed, simulated amendments followed by a final red detection awaiting a user decision. These are scenario design targets, not guaranteed Nemotron results.

| Stage | Synthetic input | Intended analytical question | Possible presentation state |
|---|---|---|---|
| Origination | Complete original financial model, memo, guidelines and agreement. | What assumptions justify the package, and what does it protect? | Original version v1.0. |
| Routine update | Management accounts consistent with the original scenario. | Can the system preserve a stable assessment and avoid unnecessary changes? | Report marker without a divergence. |
| Development 1: shipping disruption | Industry report plus company-specific scenario evidence of exposed routes, lead times and cost responsibility. | Does a disruption weaken supply and margin assumptions enough to justify better visibility? | First potential divergence; prospective forecast/supplier-reporting changes considered for v1.1. |
| Mitigation update | Evidence about alternative supply or cost recovery, including timing and limits. | Which earlier concerns are reduced, and which remain unresolved? | Update the assessment; no forced amendment. |
| Development 2: wholesale slowdown | Reduced scenario orders, inventory aging and updated cash forecast. | Is the original inventory-to-cash assumption still credible, and are existing protections sufficient? | Second potential divergence; inventory, liquidity and discretionary-spending protections considered for v1.2. |
| Development 3: recovery with unresolved cash pressure | Better direct-sales figures alongside dated cash/collection evidence that may establish a breach of the operative scenario cash floor. | Does positive sales news resolve the underlying issue, and what do the current terms actually require? | Final red detection if warranted; proposed v1.3 remains unadopted for the user. |

During authoring, set exact dates and numbers so the intended financial or reporting findings follow from the operative definitions. A cash-floor failure requires the defined cash inputs and threshold; future pressure alone does not establish it. Formal default must be assessed separately under the applicable notice and cure provisions.

Run the actual model and preserve its answers. If it misses a planned connection, makes an unsupported assertion or finds no material difference, show that outcome and review it. Do not manufacture a successful detection to satisfy the story. Any revised development case is labeled as such; it is not an unseen benchmark.

The first two adopted amendments need a recorded scenario-review rationale and effective date. Amendment generation, analyst edits and approval are separate records. Do not adopt the third proposal automatically. If amended terms provide relief rather than tightening, retain the rationale and compensating protections instead of treating every concern as a reason to raise a threshold.

## 6. Analysis and ingestion workflow

For each new report, use the existing intake/queue foundation and the [semantic ground rules](docs/semantic-intake-contract.md):

1. Preserve the report, fictional/source designation, paragraph locators and scenario availability date.
2. Extract its main point, underlying data, supporting points, stated implications and qualifications.
3. Retrieve the Crocs scenario's prior evidence, approved assumptions, exposure records and operative package.
4. Investigate uncertain implications using the prepared eligible scenario library. Record evidence and counterevidence; do not browse real future Crocs outcomes as if they occurred in the simulation.
5. Aggregate distinct economic effects, record assumptions exposed and assess duties under the current scenario terms.
6. Generate a complete candidate for the defined scenario package under fixed lender guidelines. Compare substantive terms with original/current versions and an origination-only control; unchanged terms are a valid result.
7. Save the raw model response, validation result, explanation, candidate and proposed review action. Human review governs changes to approved assumptions or terms.

Background ingestion should process newly introduced scenario reports through the same queue used by manual entry. Report reveal advances the scenario's available evidence; it does not fabricate a fresh model run. Keep **Add information** for a live presentation submission and save that attribution in the Crocs history. Label recorded replay with its original model and run date, and keep failures visible.

Before using the candidate path, confirm its coverage against the complete Crocs package. Existing benchmark runs use scoped packages; their existence does not establish readiness for this contract. Preserve this implementation boundary in the interface and records.

## 7. Display and state

Reuse the current browser interface, Python server, SQLite company separation, source viewer, report library and branching timeline where they support the scenario. Create a distinct Crocs scenario identity and state; do not relabel or overwrite B01, and do not allocate an `R01`/`R02`/`R03` benchmark identity. Check existing identities before choosing a runtime route; no Crocs route is created by this plan.

The presentation should show:

- A Crocs scenario header with the real/synthetic disclosure.
- The original package, current approved scenario version and any proposal as separate objects.
- A report library, scenario-time controls and manual information entry.
- The assumption map and source-to-assumption-to-covenant explanation.
- A horizontal time axis with package-version branches, dimmed superseded paths and selectable detections. Lanes represent versions, not interest-rate levels or credit quality.
- Two reviewed scenario amendments if supported by the authored history and actual model runs, with the final review left pending in red.
- Routine and mitigating reports that remain visible without creating false divergence markers.
- Model provenance, analyst edits and decisions, including a clear distinction between recorded and live output.

Keep simulated approvals out of the historical benchmark. Rehearse on a copy of presentation state so report introductions and decisions do not unexpectedly change the saved live demo.

## 8. Build order and completion evidence

| Step | Deliverable | Completion evidence |
|---|---|---|
| 1. Author the scenario | Reviewed business reference, synthetic financials, lender memo, complete agreement and dated report sequence. | Arithmetic and clause definitions reconcile; real/synthetic labels and source dates are present; no actual financial records copied into the scenario. |
| 2. Prepare isolated state | Crocs-specific sources, profile/assumption history, package versions and report queue using existing application patterns. | Cross-company isolation and preserved FluxRail/benchmark data. |
| 3. Run and review Nemotron | Genuine initial profile, sequential attributions and candidates, including a stable update and mitigation. | Raw responses, citations, model/settings, failures and reviewer corrections retained; no scripted success substitutions. |
| 4. Record the presentation history | Reviewed first and second simulated amendments, with the third proposal pending when supported. | Effective dates and operative versions are correct; no retroactive erasure of a failure. |
| 5. Present and verify | Crocs page, report reveal, timeline explanations, proposal review and saved manual attribution. | Browser inspection, meaningful arithmetic/date/isolation checks and a rehearsal on copied state; recorded/live output distinguishable. |
| 6. Update records | Current status, master plan and application instructions reflect what actually ran. | Planned features remain labeled until verified; Crocs stays excluded from benchmark scores. |

This document authorizes no claim of completed Crocs implementation. The current request is satisfied by planning and updating Markdown records; application changes and hosted model runs are subsequent work.
