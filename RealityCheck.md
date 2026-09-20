# RealityCheck
## Master Game Plan — Working Revision

Updated: September 20, 2026.

**Confirmed direction:** Detect possible environmental drift using decision-specific assumption frameworks, generated package comparisons and observed lender responses. Private credit is the first application; analyst review governs interpretation and any adoption of new terms.

This is the maintained direction and implementation guide. The [current status](RealityCheck-Current-Status.md) governs delivered functionality and recorded verification; this document governs agreed direction and instructions for the next build. Section 33 separates confirmed decisions from recommendations. No real-world detection performance or customer validation is claimed.

### Current baseline and next delivery

- **Delivered:** the local FluxRail (B01) demonstration, using a Python standard-library server, browser JavaScript and SQLite. Hosted Nemotron generated six assumptions (four approved synthetic source claims and two working inferences) and three event analyses. Two authored fictional amendments are adopted; v1.2 is active and v1.3 remains pending. Preserve that pending decision and the existing database.
- **Selected presentation:** Crocs, using real business context and a synthetic private-credit package, financial model, covenants and report history. Built at `/h01` following the [Crocs demo plan](RealityCheck-Crocs-Demo-Plan.md) (September 20, 2026); what ran, what the model got wrong and what remains limited are in the [current status](RealityCheck-Current-Status.md). Preserve the existing FluxRail workspace. Further company expansion follows this presentation rather than being a prerequisite; retain the 30 authored packages as a future pool.
- **Implementation boundary:** scoped candidate generation/comparison and recorded runs now exist; the [current status](RealityCheck-Current-Status.md) and [benchmark execution record](RealityCheck-Benchmark-Testing-Plan.md#13-execution-record) govern those results. The Crocs scenario exists with one reviewed run per analysis; repeat-run stability is unmeasured. Richer hypothesis research, historical-response learning and cross-domain transfer must not be presented as implemented by this plan.
- **Separate historical benchmark:** iRobot/Carlyle and RumbleOn/Oaktree have recorded development replays; PetIQ/Ares was run once as the unseen history, locked and compared. Crocs is exclusively the presentation scenario and is excluded from benchmark inputs, evaluator records and scores. Preserve all historical benchmark results and limits.
- **Data-use boundary:** SEC public filings support a public-data reconstruction, but track eligibility is separate. The current Compound track restricts financial data to synthetic/sandbox inputs; Xtract permits public/synthetic inputs. Section 10 gives the preparation and submission instructions, including this qualification to the earlier general data-use assessment.

The status record retains the dated implementation checks, model runs and their limitations. This Crocs documentation revision does not rerun tests, make hosted calls or change application state.

---

## 0. One-Line Definition

**RealityCheck aims to detect when changing conditions make an original decision or its terms worth reconsidering, using a framework native to that decision and evidence-linked comparisons.**

Core question:

> **Given what we know now, would the original decision and its terms still fit the environment?**

Private credit is the first demonstration: Nemotron reads a specialized deal, constructs its assumption framework, assesses new evidence, and would generate a complete fresh candidate package under explicit lender guidelines. Differences from original/current terms and actual historical amendments serve as signals of possible drift.

Primary objective: evidence-backed detection of material environmental change, with uncertainty and acceptable false-alert burden. Faster review and earlier recognition are benefits to test. Package generation/comparison, formal guideline controls, historical-response learning and transfer beyond credit are proposed, not implemented or validated; see the [current status](RealityCheck-Current-Status.md) for delivered scope.

---

## 1. The Core Problem

At underwriting, a lender forms a thesis about a borrower: its revenue quality, customer dependence, cash generation, leverage capacity, strategy, and downside resilience.

After origination, new evidence arrives through financial statements, management updates, lender notes, contract changes, and amendments. The monitoring task is to reconcile that evidence with the assumptions supporting the credit decision.

**The workflow problem to validate:** analysts must repeatedly reconstruct those links across documents, and the manual process can create delays, omissions, or duplicated work.

Existing analysts and monitoring products already consider financial and qualitative information. RealityCheck's proposed differentiation is an explicit, persistent relationship between:

```text
Original decision documents → Deal-specific assumption framework
    → New evidence and counterevidence under fixed judgment guidelines
    → Updated assessment + complete candidate package
    → Substantive comparison with original/current terms
    → Possible drift, explained through evidence and assumptions
    → Analyst review and preserved history

Historical evidence + actual lender amendments
    → Observed response patterns that inform drift detection
```

An adopted amendment is an observed response that can reveal environmental change; it is not presumed to be the correct remedy, definitive proof of drift or a target the model must imitate. The project must establish whether these signals improve detection beyond direct evidence-to-assumption analysis. Private credit tests the broader mechanism; other decision domains remain unvalidated.

## 2. User, Decision, and Value

**Initial user:** a private-credit analyst conducting periodic borrower reviews.

**Proposed workflow:** the analyst supplies original deal documents, applicable judgment guidelines and new evidence, then reviews affected assumptions, a newly generated candidate package and substantive differences linked to possible drift. Observed historical lender responses can inform detection. Adopting proposed terms is a separate optional decision.

**Decisions supported:** request additional information, continue routine monitoring, update the internal credit view, or refer a concern for a fresh credit review.

The likely buyer is a credit or portfolio-management team; the budget owner and purchase rationale remain unvalidated.

Before making commercial claims, investigate:

- How analysts currently revisit the original memo and subsequent amendments.
- Which parts consume time or cause omissions, using a recent review as an example.
- What evidence makes an alert actionable and what false-alert burden is tolerable.
- Whether suitable reporting packets can be provided for a pilot.

Success means improving a real review decision or reducing the effort required to reach it. More alerts alone are not a benefit.

## 3. Hypotheses and Evidence Required

| Priority | Hypothesis | Evidence needed |
| --- | --- | --- |
| Primary | Deal-specific frameworks and controlled package comparisons identify material environmental drift with useful attribution and an acceptable false-alert burden. | Held-out dated cases with environmental-change judgments assessed separately from amendment adoption; compare against direct assumption assessment. |
| Secondary | Historical lender responses improve detection without requiring the model to reproduce adopted terms. | Compare detection with/without eligible historical precedents, including amendments without drift and drift without amendments. |
| Secondary | RealityCheck improves analyst review speed or completeness. | A controlled exercise measuring time, missed concerns and unnecessary escalations. |
| Secondary | Semantic interpretation adds value beyond extraction and assumption-aware rules. | Comparison on unseen cases with identical available evidence, including an extraction-plus-rules baseline. |
| Exploratory | RealityCheck surfaces warranted concerns earlier than existing monitoring. | Evaluation using evidence available at each decision date, with comparable false-alert burden. |

A working demo demonstrates implementation. Synthetic tests demonstrate behavior on controlled cases. Neither alone establishes real-world early-warning performance or reduced credit losses.

## 4. Product Boundary

RealityCheck is a detection and review-support layer. Its central output is an evidence-backed assessment of possible drift. A candidate package is an analytical comparison instrument, not an optimal remedy or an automatically operative contract. Observed amendments are detection evidence, not correct-answer labels.

The MVP does not price loans, automatically change credit ratings, approve lending decisions, or predict defaults. A recommendation for a fresh review remains a recommendation; the analyst owns the decision.

The product retains the original thesis and subsequent approved revisions. It does not silently replace the lender's assumptions with an AI-generated version.

## 5. The Core Object: An Underwriting Assumption

Use a compact set of explicit assumptions native to each deal, covering the dimensions supported by its documents rather than forcing every borrower into an identical checklist. B01 currently has six: four approved synthetic source claims and two labeled working inferences. The earlier CedarBridge example uses five; neither count is mandatory for the additional companies.

Each assumption should contain:

- A stable identifier, dimension, and precise claim.
- Its source passage in the underwriting memo or approved amendment.
- Why it matters for repayment capacity or downside protection.
- Criticality and any agreed threshold, tolerance, or review trigger.
- Relevant definitions, such as recurring revenue or adjusted EBITDA.
- The evidence needed to assess it and its approved thesis version.

Example, explicitly synthetic:

> **A1 — Revenue predictability:** Customer A accounts for 35% of revenue and is committed for two years without termination for convenience. That commitment supports the base-case cash-flow forecast. A substantive reduction in the commitment requires review.

The analyst confirms extracted assumptions before they become the monitoring baseline. Keep the original version for historical comparison and use the applicable approved version for current review.

## 6. Assessment Framework

Keep three outputs separate.

### Assumption status

| Status | Meaning |
| --- | --- |
| Supported | Available evidence supports the assumption within its defined tolerances. |
| Weakened | Evidence challenges the assumption, but its scope, persistence, or materiality is not sufficient to establish contradiction. |
| Contradicted | Direct evidence materially conflicts with the assumption under the agreed rubric. |
| Insufficient evidence | Missing, stale, ambiguous, or conflicting evidence prevents a defensible assessment. |

Absence of a warning is not evidence that an assumption remains supported. Missing information is not automatically a contradiction.

### Credit implication

Record **adverse, neutral, beneficial, mixed, or unclear**, with an evidence-based explanation. An assumption can be contradicted while repayment capacity improves.

### Suggested analyst action

Record **continue routine monitoring, request information, review the credit view, or consider re-underwriting**. Include the reason and leave acceptance or override to the analyst.

At borrower level, summarize which critical assumptions require attention and what remains unknown. Do not combine these outputs into an unvalidated numerical risk score or average away one critical contradiction with several supported assumptions.

### Proposed review-priority rubric

**Direction recorded September 19, 2026; not implemented or validated.** Use a small ordinal consequence rubric to help prioritize review. Keep evidence support, borrower exposure, direction and timing separate. The following anchors are a proposed starting point; borrower-specific criteria and escalation rules must be defined in versioned lender guidelines and evaluated before use.

| Dimension | Representation |
| --- | --- |
| Potential consequence | **0:** supported immaterial effect; **1:** limited implication, monitor; **2:** potentially material; **3:** potentially decision-critical. Use unknown/unassessed when there is insufficient basis to assign a tier. |
| Evidence support | Direct evidence, supported inference, unresolved hypothesis or conflicting evidence, with reasons and source references. Directly quoted evidence is not automatically true. |
| Borrower exposure | Documented, conditional, unknown or demonstrably limited, supported by company facts. |
| Direction | Adverse, beneficial, neutral, mixed or unclear. A consequence tier does not encode direction. |
| Timing | Current, near-term, longer-term or unknown; retain exact dates, lags and obligation deadlines where available. |
| Covenant finding | Separate clause-specific interpretation or calculated result. A consequence tier never establishes a breach or changes terms. |

Nemotron proposes a tier by identifying the applicable rubric criteria and evidence. Save the guideline version, rationale, unresolved conditions and any analyst override. Unknown is not zero. Tiers are ordinal review aids, not probabilities, dollar amounts, additive risk units or thresholds for automatic lending decisions.

Do not multiply potential consequence by model confidence: a plausible decision-critical exposure with weak evidence may need urgent verification rather than a low queue position. Do not sum tiers into a borrower credit score or average away a critical obligation. A finding based on conditional exposure must retain those conditions even when its potential consequence is high. Urgency depends on consequence, evidence gaps and actual timing; the final routing policy remains to be specified.

Evaluate tier assignments and review routing on dated, analyst-reviewed cases. Repetition of the same report must not raise severity; unrelated upside must not cancel a critical obligation; missing evidence must not become a zero. Measure unsupported causal leaps, missed material connections, qualification retention and false alerts separately from citation accuracy. Do not describe model-generated confidence as a calibrated probability without outcome-based calibration evidence.

## 7. Nemotron's Role

**Confirmed September 19, 2026: event attribution is the entry point.** On receipt of an event description or reporting document, Nemotron should attribute the evidence to company assumptions and/or individual covenant clauses, identify direct changes and conditional downstream exposure, and propose adjustments for analyst review. The [assumption register and relationship map](./RealityCheck-Assumptions-and-Relationships.md) covers 24 working claims, 12 evaluation prerequisites, and all 30 clauses, with optional elections preserved. The expanded claims require their own approved baselines; they are not all existing signed-off lender beliefs.

The current B01 entry point uses one bounded semantic assessment over the new event, relevant reporting context, assumptions, covenant definitions, and explicit relationships:

1. Extract candidate changes with exact source references.
2. Map evidence and counterevidence to assumption identifiers and/or individual covenant identifiers, allowing several targets for one event.
3. Propose assumption status, credit implication, and a concise rationale.
4. Identify missing information, affected downstream assumptions, and a proposed adjustment or review action.

Keep event coverage separate from assumption status. Unaddressed means the event provides no assessment of that claim, not that the claim remains supported. Downstream exposure needs an inspectable path and any missing conditions; it does not propagate a contradiction, numerical loss, or covenant failure automatically. A directly relevant contractual event can be assessed without first contradicting a thesis assumption. Nemotron proposes changes; analyst review and versioned approval govern any revision of the baseline.

These are responsibilities within the initial analysis, not a requirement for four separate agents or calls. The planned argument-mapping and research loop below extends this entry point; targeted retrieval and reanalysis are not yet implemented.

### Input and semantic processing

The application collects evidence and supplies the selected documents to Nemotron. The model does not independently acquire private borrower information or know changes made after its training. The planned research loop uses actual retrieval from the company library and explicitly connected, eligible sources; it does not treat model recollection as newly obtained evidence. External source connections remain to be implemented.

For each review, provide the approved thesis, applicable covenant specifications and definitions, relevant prior evidence, and the newly available borrower packet. A small packet can be supplied in full, but even a short report may require targeted evidence lookup to test an indirect implication. Retrieve relevant company exposures, definitions, amendments, exceptions and counterevidence together with the apparent change. Additional retrieval infrastructure depends on corpus size and measured need; hypothesis testing does not depend on a report being long.

Within the semantic assessment:

1. Identify the borrower, affected entity/customer, document version, and relevant passage.
2. Extract a proposed fact or event with its exact quotation and locator. Preserve who made the claim rather than treating every statement as established fact.
3. Distinguish executed changes, proposals, future intentions, conditions, negations, and hypothetical scenarios. Record effective dates separately from when the evidence became available.
4. Compare the event with approved assumptions and applicable contractual language, including definitions and exceptions.
5. Propose the relevant assumption/covenant IDs, assessment, unresolved facts, counterevidence, and an explanation that an analyst can inspect.

Treat source documents as evidence, not instructions to the model. Validate identifiers, source spans, dates, permitted labels, and numerical inputs outside the model. A valid quote does not prove that a document is operative or that an interpretation is correct. Keep ambiguous evidence unresolved and give consequential semantic mappings an analyst acceptance/override step.

Nemotron may propose a relevant economic relationship, but it cannot silently add an approved formula, change a covenant definition, or convert a qualitative concern into an observed numerical loss. The relationship rules below determine how findings can affect calculations.

Illustrative output for a synthetic document whose cited passage reads exactly as quoted:

```json
{
  "assumption_id": "A1",
  "proposed_status": "contradicted",
  "credit_implication": "adverse",
  "evidence": [
    {
      "document_id": "demo-q2-update",
      "locator": "Customer contracts, paragraph 2",
      "quote": "Customer A may terminate its agreement on 30 days' notice without penalty."
    }
  ],
  "counterevidence": [],
  "missing_information": ["Expected renewal and replacement demand"],
  "suggested_action": "review_credit_view",
  "rationale": "The disclosed termination right contradicts A1's two-year commitment assumption. The effect on expected cash flow requires analyst review."
}
```

Validate document identifiers, quoted spans, dates, and calculations outside the model. Exact quotation establishes traceability, not the correctness of the inference; the analyst must still be able to assess that inference.

Display evidence coverage, unresolved contradictions, and source freshness. Do not present a model-generated confidence number as a calibrated probability.

### Qualitative intake, aggregation and indirect events

The next build must implement the [semantic intake ground rules](docs/semantic-intake-contract.md). A report need not name a borrower to be relevant. Keep the sequence inspectable:

1. **Receive and extract:** preserve the original report and located passages; extract attributed observations, forecasts, opinions, proposals and conditions without forcing a company connection. Preserve negation, exceptions, source uncertainty and dates.
2. **Aggregate by review cutoff:** group related claims while retaining each source, disagreement, correction and qualification. Syndicated copies of one announcement are one source family, not independent corroboration. Show what is new rather than raising a new alert for a duplicate.
3. **Attribute to each company:** use a sourced exposure register for customers, industries, suppliers, geography, cost inputs, hedges, pass-through and dependencies. Explain external development → economic channel → borrower exposure → affected assumption → possible covenant implication. Mark each link as sourced, approved or hypothesized.
4. **Preserve conditions in downstream analysis:** missing borrower exposure means a conditional finding or a request for information. An industry forecast is not realized borrower loss, and an exposed assumption is not an automatic covenant breach. Candidate generation must retain these uncertainty labels.

For example, a hypothetical oil-supply disruption can suggest margin exposure for a fuel-intensive borrower. Actual costs depend on procurement, hedges, pass-through, volumes and timing. Do not invent an EBITDA reduction or infer that FluxRail has the same exposure. Route a shared report independently to each relevant company and preserve different, mitigated and no-established-connection outcomes.

Current source checks and assumption paths are a foundation. The richer evidence schema, cross-report reconciliation, exposure register and external transmission paths remain design work; current B01 ingestion is not this complete pipeline.

### Article argument mapping and research into unstated implications

**User direction recorded September 19, 2026; implementation outstanding.** Nemotron must use the new report together with the established company library to understand how developments could affect the underlying package. The framework combines an argument map, a borrower exposure graph and targeted hypothesis testing. The library guides research early in the process; it must not force every new signal into an existing assumption or suppress unfamiliar exposures.

First decompose each article or report into the following source-linked structure:

| Component | Required treatment |
| --- | --- |
| Main point | Record the author's central claim, attributed to its source; prominence is not evidence strength. |
| Underlying data | Preserve observations, measurements, units, periods, definitions and cited original sources. Separate reported data from forecasts or estimates. |
| Supporting points | Identify the arguments supporting the main point and their evidence dependencies. Repetition or agreement with the headline does not establish validity. |
| Stated implications | Record consequences explicitly asserted by the author, preserving whether they are observed, predicted or conditional. |
| Qualifications and counterarguments | Retain exceptions, negation, uncertainty, contrary evidence, scope and dates. A qualification can be more consequential to the borrower than the headline. |

Then apply this loop:

1. **Retrieve borrower context before expanding implications.** Use company reports, assumptions, exposure facts, relationships, prior findings and operative covenants available at the review date. Relevant facts include customers, geography, suppliers, input costs, pricing/pass-through, hedges and financing structure. Retrieve counterevidence and exceptions alongside apparent risks.
2. **Form a bounded set of testable hypotheses.** Treat an unstated implication as a candidate to investigate, not a hidden fact the model must discover. Use the structure: if development X affects factor Y, and the borrower has exposure Z, assumption A may be affected through mechanism M. Consider adverse, mitigating, beneficial and no-material-effect alternatives. New relationships or assumptions remain proposed additions until reviewed.
3. **Research the uncertain links.** Ask specific questions about exposure, timing, offsets, whether an effect is already reflected in forecasts, and what would disconfirm it. The application retrieves actual eligible sources from the library or explicitly connected public sources under the data-use rules in Section 10. Model recollection is not new evidence. Record source dates and lineage, retrieval questions and unresolved gaps. Stop when a path is sufficiently supported, refuted, immaterial or unresolved within the bounded search; report gaps rather than extending speculative chains indefinitely.
4. **Build an inspectable transmission explanation.** Represent external development → economic channel → borrower exposure → affected assumption → possible covenant implication. Each link states whether its basis is source evidence, documented company facts, an approved relationship or an explicit model hypothesis. A relationship graph helps retrieval and explanation; it does not establish causation by itself.
5. **Aggregate distinct economic effects.** Group by underlying event/driver, exposed assumption, metric, period and scenario. Syndicated reports do not add independent corroboration. Higher costs → lower margins → lower EBITDA is one connected mechanism, not three independent risk increments. Keep gross effects and mitigants visible. Netting requires supported, realizable offsets affecting the same metric, period and scenario; unrelated upside cannot cancel a critical obligation.
6. **Produce separate findings.** Report assumption implications, current contractual duties/compliance, potential future pressure and possible package drift separately. Apply Section 6's proposed review-priority rubric with supporting evidence and uncertainty. Candidate-package generation receives these qualifications; it cannot promote a hypothetical effect into a realized loss, amend terms automatically or infer a breach from a priority tier.

The full output should make **source argument → researched connections → evidence and counterevidence → borrower assumptions → covenant/package implications → review priority** inspectable. Preserve the original sources and dated baseline; update derived assessments and revisit dependent findings when new information resolves a previously unknown exposure.

For a hypothetical oil-related report, Nemotron could investigate oil-supply pressure → fuel-intensive customer costs → customer spending → borrower renewals. It needs sourced customer-industry exposure and evidence about demand, pass-through and timing before claiming actual renewal deterioration. A valid outcome is potentially material conditional exposure with a request for customer guidance and no established current covenant breach.

Graph-based retrieval is an architectural pattern here, not a requirement to install a particular graph framework or replace SQLite. Combining connected entities/relationships with original document passages is described in [Microsoft's GraphRAG local-search documentation](https://microsoft.github.io/graphrag/query/local_search/). The hypothesis rules, covenant checks and consequence rubric are RealityCheck-specific design choices. [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/) supports context-specific evaluation and human judgment in selecting metrics and thresholds; it does not validate this proposed scoring scheme.

## 8. Proposed Package Comparison and Historical Response Learning

**Direction confirmed; coverage is partial.** Scoped candidate generation/comparison and recorded development runs exist; consult the [benchmark execution record](RealityCheck-Benchmark-Testing-Plan.md#13-execution-record) and current status. FluxRail's adopted amendment instruments were authored for its scenarios. The complete Crocs package flow and historical-response learning described here remain further work; scoped results do not establish complete contract coverage or improved detection.

### Reconstruct and compare under explicit guidelines

1. Preserve original/current packages and the deal-native assumption framework, separating approved claims, contractual requirements and model inferences.
2. Supply explicit lender guidelines for risk tolerance, materiality, permissible judgment and insufficient-evidence behavior. These are distinct from the assumptions specific to one deal.
3. Have Nemotron conduct a fresh assessment using newly available information and construct a complete candidate package. Retain unchanged protections where justified; a fresh package need not differ in every clause. Link substantive changes to evidence and affected assumptions, and do not invent thresholds or missing facts.
4. Compare scope, thresholds, definitions, reporting duties, triggers, permissions and cure periods with both the original and current approved packages. Equivalent wording contributes no drift signal. Original comparison shows cumulative change; current comparison shows gaps not already addressed by amendments.
5. Assess whether differences indicate material environmental change, no material drift or insufficient evidence. Explain attribution and competing explanations. Detection is the purpose; adoption is a separate decision.

**Matched control:** generate a candidate from original information and another from updated information while holding model, prompt, lender guidelines and eligible precedent set fixed. Compare both generated candidates as well as the approved packages. Changes already proposed from original information can reflect model preference or pre-existing gaps. Record guideline/model updates separately; they must not masquerade as borrower drift. Repeated runs and stable cases are needed to measure residual variability.

### Learn from observed responses as detection evidence

Preserve **dated evidence → affected assumptions → actual lender package/covenant changes**, with before/after terms, applicable lender policy, rationale when available and alternative explanations. Actual amendments are observable responses that may reveal changed conditions. They are not assumed to be correct remedies or optimal decisions; the learning objective is better detection and interpretation of drift, not amendment imitation.

Example: customer losses followed by a move from quarterly to monthly concentration reporting can inform a pattern associated with weakening revenue stability. The detector need not conclude that monthly reporting was the correct remedy. Policy changes, negotiation and administrative updates can also explain amendments; environmental change can occur without any amendment. Preserve unknown rationale rather than inferring certainty.

**Working recommendation:** first supply reviewed historical cases as inspectable precedents. Fine-tuning remains a later option if evaluation supports it, not a prerequisite or an implemented capability. Keep the deal framework, lender guidelines and historical response records separate and versioned. An observed amendment may support detection once available; it cannot be used to claim detection before that date or leaked from a held-out case's future into its inputs.

Success is improved detection on unseen cases, judged against evidence about environmental change independently of whether an amendment was adopted. Measure missed drift, false alerts and attribution quality. Include policy-only amendments, drift without amendments, beneficial changes, unchanged conditions and missing context. Compare with/without historical precedents and with direct assumption analysis alone.

### Transfer beyond private credit

The reusable structure is an original decision artifact, a native assumption framework, explicit judgment guidelines, new evidence, a reconstructed artifact and an evidence-linked comparison. Supplier requirements and project plans are candidate applications. Each requires domain-specific interpretation and validation; no second-domain implementation exists. The next presentation uses Crocs with a synthetic credit scenario; broader company and domain expansion remains later work.

### Optional semantic experiments

### Blind reconstruction

Experiment with describing the current borrower before showing the original conclusion. This may reduce anchoring, but could also omit relevant context or create apparent drift through wording differences.

Use the same assumption dimensions and definitions for both representations. Compare the result with the simpler direct-comparison approach on held-out cases. It is an optional experiment, not the central product claim.

### Skeptic pass

A second model pass may challenge unsupported interpretations or locate mitigating evidence. A pass using the same model is not independent verification.

Add either experiment only if it improves supported assessments or reduces false alerts enough to justify added latency, cost, and failure modes.

## 9. Structured and Semantic Analysis

The intended division is for deterministic calculations to handle defined quantities such as leverage, coverage, liquidity, recurring-revenue share, concentration, cash conversion and covenant headroom, using the applicable agreement and actual dated inputs. Current code has limited calculation checks; a full quantitative executor across B01 and the other agreements is not implemented. Do not present semantic attribution as an executed financial compliance test.

Semantic analysis handles the meaning of evidence: a changed termination right, conditional sponsor support, an announced strategy, or whether a statement actually contradicts an assumption.

Important distinctions:

- Recurring-revenue share and customer concentration are numerical signals; their detection alone does not demonstrate semantic value.
- Services revenue does not automatically mean nonrecurring revenue. Verify the definition and underlying contracts.
- Changes in PIK usage, amendments, or acquisitions require context; their presence alone does not establish adverse drift.
- Preserve metric definitions and reporting periods. Changing definitions can create apparent movement without an economic change.
- Surface disagreement between rules and model assessments for review.

Combine evidence at the assumption level. Keep financial calculations deterministic and the economic interpretation inspectable.

### Explicit relationships between evidence, assumptions, and covenants

Maintain a small set of typed relationships. Include thesis assumptions even when they have no corresponding covenant.

| Relationship | Example | Permitted effect |
| --- | --- | --- |
| Evidence supports or contradicts an assumption | An operative amendment introduces a cancellation right that conflicts with an assumed firm commitment. | Propose an assumption assessment with evidence and counterevidence. |
| Evidence supplies a defined input | A dated statement and reconciliation support eligible cash or permitted EBITDA adjustments. | A validated input can feed calculations for the matching entity, period, and definition. Preserve reported versus accepted values. |
| A metric is calculated from other inputs | Net leverage depends on defined debt, permitted cash netting, and covenant EBITDA. | Recalculate using an approved formula and the applicable covenant version. |
| An obligation applies when a condition is met | A specified cash level activates an additional forecasting obligation; an actual customer termination notice activates a notice duty. | Evaluate the explicit conditions and deadline. Activation is distinct from failure to meet the obligation. |
| A business change may affect a future metric | A new cancellation right may reduce future revenue and cash generation. | Identify exposure and request information or run an explicitly approved scenario. Do not automatically change reported revenue or EBITDA. |

Each relationship records source and target IDs, type, scope, applicable dates, formula/condition where relevant, supporting basis, and approval status. Reuse a variable only when its entity, period, units, and definition match. Financial EBITDA, covenant EBITDA, and underwriting-normalized EBITDA remain distinct measures.

Keep these relationships in the existing relational store (SQLite for B01); TigerData/PostgreSQL is an optional later migration, not a prerequisite. A graph database or general simulation engine is unnecessary for the focused demo. Use one approved calculation/obligation specification per covenant version. Model-proposed relationships remain candidates until accepted.

### Observed results versus modeled effects

Synthetic example: a customer gains a 30-day cancellation right. This can contradict the assumption of a firm two-year commitment while reported covenant EBITDA stays at $20m. With $80m net debt, actual leverage remains 4.00x against the illustrative 5.00x maximum.

A separate analyst-approved downside case might set EBITDA to $16m with net debt held at $80m, producing 5.00x. Those inputs are scenario assumptions, not conclusions implied by the cancellation clause. Equality passes this particular maximum. Deriving a revenue or EBITDA change requires further inputs such as affected revenue, cancellation behavior, timing, replacement sales, margins, and cost response.

A qualitative event can also have a direct contractual effect when the agreement says so. An actual termination notice may activate a reporting duty without waiting for earnings to decline. Check the exact trigger; permission to cancel is not the same event as exercising that permission.

## 10. Data Strategy

### Demonstration data

The implemented demonstration uses explicitly fictional borrowers and synthetic memos, agreements and reports. Public cases can now support a separately labeled historical reconstruction or inform a newly authored synthetic case, subject to the source and track rules below. Research does not authorize silently replacing B01 or importing real financial records into a Compound submission.

**Existing synthetic framework anchor:** a profitable software or business-services borrower. The companion [Synthetic Covenant Framework](./Synthetic-Covenant-Framework.md) remains a supporting template for agreements, definitions, reporting duties, exceptions and dated evidence. The current footwear presentation follows the [Crocs plan](RealityCheck-Crocs-Demo-Plan.md); adapt the economics, assumptions and protections to that scenario instead of reusing software-business claims. The companion's numerical choices are illustrative; practitioner review and complete dataset validation remain outstanding.

**Corrected scope September 19, 2026:** the user meant **30 synthetic companies, each with its own specialized contract**, rather than 30 clauses for CedarBridge. The [30-company portfolio index](./synthetic-credit-portfolio/README.md) links the individual agreements. Each borrower has three sector-specific covenants, four underwriting assumptions, an individually calibrated financial model, selected core/optional terms, and dated future evidence. The [portfolio manifest](./synthetic-credit-portfolio/manifest.json) records borrower identity and availability dates. Expected answers remain in a separate evaluator directory. These are synthetic covenant-focused agreements with internally checked financials; practitioner comparability and measured model evaluation remain outstanding.

The earlier [CedarBridge clause library](./Synthetic-Private-Credit-Covenants-30.md), its JSON/evaluator companions, and the CedarBridge assumption register remain supporting design artifacts. They do not represent the 30-company deliverable, and their PC/T/A identifiers must not be silently mapped to the portfolio's borrower-scoped C/S/A identifiers. B01 now has its own implemented workspace; the other 29 authored packages do not yet have generated borrower workspaces.

Keep contractual status separate from thesis status. Qualitative restrictions and additional reporting triggers already exist in credit agreements. A covenant can pass while an underwriting assumption is contradicted; a reporting obligation can activate before a financial minimum fails. Preserve failed calculations and the scope of any later cure, waiver, or amendment.

Public investment schedules can supply loan terms and valuation context. For example, Ares's schedule reports fields such as coupon, maturity, principal, cost, and fair value. That does not supply the complete reporting packet needed for this product. See Source 3 in Section 34.

### Pilot data

A useful real-world pilot requires lender-provided memos, approved amendments, borrower reporting, and analyst review outcomes. Data access is a prerequisite, not a problem solved by selecting a database.

### Evidence acquisition workflow

**Hackathon:** upload or select eligible synthetic reports or a separately identified public-source packet with a defined release schedule. Local B01 file/API ingestion exists; the broader report-reveal interface and external source connections remain to be built. A simulated timeline must not expose future documents early.

**Pilot:** connect an authorized lender document repository or accept analyst uploads of financials, compliance certificates, customer contracts, amendments, management updates, and lender notes. These are proposed sources, not integrations already implemented. A file-arrival event can initiate processing after access and identity checks.

**Supplemental public evidence:** company filings, official announcements, customer/supplier disclosures, and other attributable sources can identify developments worth investigating. Keep them separate from borrower-certified figures and operative contract documents. Public research will not supply every private contract change.

The ingestion process preserves the original file, borrower/entity association, document type and version, covered period, effective date where known, available-at date, and receipt time. Extract text and tables with stable page/section references; use OCR only for scanned material and flag extraction uncertainty. Detect duplicates and retain amendments as new versions rather than overwriting history.

Before assessment, show which expected documents are present, missing, or stale. A search returning no result is not evidence that an assumption is supported. Retrieval selects evidence; it does not verify truth or establish complete coverage.

### Historical evidence

Distinguish original contemporaneous material from reconstructed material. A reconstructed thesis is an illustrative interpretation, not evidence of what the lender actually believed.

Prevent hindsight: define the starting thesis before revealing subsequent events, and exclude information that was unavailable at the simulated review date. Do not choose only borrowers later known to have deteriorated.

For response learning, retain actual amendments and their preceding evidence as dated observations, alongside rationale and policy where available. Keep amendment occurrence separate from independently assessed environmental-change labels. Include cases without amendments. A later action can be retrospective context but cannot enter an earlier detection run; freeze eligible precedents by the evaluation cutoff.

### Real-company research: sufficient starting cases, incomplete private information

The [case research report](docs/real-private-credit-case-research.md) records verified source links, dated developments and gaps. These are document histories, not daily private-loan price series. A public operating company can borrow through a private-credit facility and disclose its agreement through SEC filings.

| Candidate | Useful starting material | Recommended use / limit |
| --- | --- | --- |
| RumbleOn / Oaktree | 2021 original agreement and 2023–2024 amendments with borrower reporting. | Strongest initial covenant-comparison candidate. Separate the term facility from floorplan financing, public Adjusted EBITDA from contractual EBITDA, and improved operations from relaxed limits. |
| iRobot / Carlyle | July 2023 agreement, dated operating reports, Amazon transaction termination and 2025 waivers/amendments. | Clear narrative for a public-document replay, initially through June 2025. The original agreement already contemplated merger failure; do not invent an assumption that closing was certain. |
| PetIQ / Ares | 2018 origination, 2019 restatement and 2020 definition/permission amendments with financial reporting. | Contrast with a simple deterioration story; investigate supply/licensing changes, EBITDA addbacks, debt treatment and collateral permissions. |

No complete internal underwriting memo, private lender-policy record or full contemporaneous lender-reporting stream was found for these cases. Missing schedules, compliance inputs and rationale must stay missing. Pluralsight lender marks and the Benitago/Thrasio retrospective records did not provide equally sufficient original-package histories in this search. Do not represent them as equivalent prepared datasets.

The named histories belong to the separate historical benchmark; consult its [execution record](RealityCheck-Benchmark-Testing-Plan.md#13-execution-record) for prepared packets and development runs. The user selected Crocs for a real-name synthetic presentation, not historical reconstruction. No production training dataset is approved by that selection.

### Source rights and SteelHacks eligibility

**Assessment recorded September 19, 2026.** The user authorized the 2025 Devpost rules as the general benchmark. That benchmark does not replace a verified current sponsor rule. Public accessibility, permission to reuse and prize eligibility are separate checks.

| Source or rule | Instruction |
| --- | --- |
| SEC EDGAR public filings | Prefer SEC-hosted original agreements, amendments, 8-K/10-K/10-Q text and filed exhibits. The SEC explicitly permits public-filing reuse and redistribution. Preserve source attribution; do not describe all third-party material as our own or assume that every publicly accessible website has the same policy. [SEC reuse FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions), [dissemination policy](https://www.sec.gov/about/privacy-information). |
| Company IR sites, news sites and court-document hosts | Treat the research links as discovery/reference sources until reuse terms are checked individually. iRobot and Carlyle website terms restrict reuse; use an equivalent SEC-filed copy when available. Otherwise omit the full document from the demo corpus until a suitable reuse basis is established. A citation alone does not confer reproduction rights. [iRobot terms](https://www.irobot.com/en_US/legal/terms-and-conditions.html), [Carlyle terms](https://www.carlyle.com/notices-and-disclaimers). |
| Current Compound track | The rule states: **“Use synthetic or sandbox data. No real account numbers, credentials, or financial records.”** Public SEC financial records are not expressly exempted. Use synthetic inputs for a Compound submission unless organizers clarify otherwise; changing company names or copying real figures into a sandbox does not make those records synthetic. [Official track](https://steelhacks.org/tracks#compound). |
| Current Xtract track | Public or synthetic sources are permitted; LANXESS data is excluded. Eligible SEC records fit its published source category, subject to reuse rights. This does not override Compound restrictions if seeking both prizes. [Official track](https://steelhacks.org/tracks#x-tract). |
| 2025 general rules, requested benchmark | AI and other tools must be credited in the README. Project work must meet the event build-window rule; the public open-source exception is not permission to prebuild and then publish the team's own project to evade that rule. The benchmark does not expressly prohibit pre-existing historical source documents. Its dates are September 20–21, 2025, not this year's schedule. [2025 rules](https://steelhacks-xii.devpost.com/rules). |
| Devpost submission rights | The submission must respect others' rights and permit the platform's described display/promotional use. Distinguish our code and analysis from third-party source material; do not apply the repository's code license indiscriminately to copied sources. [Devpost terms, section 7](https://info.devpost.com/legal/terms-of-service). |

**Qualification to the earlier recommendation:** an SEC-based reconstruction has a supported source-reuse path, but it is not blanket approval for the Compound prize. For a combined Compound/Xtract presentation, prepare synthetic financial inputs and eligible synthetic reports. Retain real-case research as background; do not bundle or display actual company financial records in that submission without resolving the track restriction. This documentation update does not select tracks or certify overall event eligibility.

### Instructions for preparing a real-company reconstruction

These are preparation requirements for an eligible public-data demo, not claims of completed ingestion.

1. **Choose a bounded company/facility and review period.** Start with one candidate and a small coherent set of clauses and operating reports. Record the exact borrower, lender role and facility; keep revolvers, floorplan lines and other loans separate. Use the original executed agreement as the origination reference, not a later conformed version containing future amendments.
2. **Create a source manifest before model use.** Record document ID/version, company/facility, title, publisher, SEC accession and URL, document type, content hash, relevant clause/page/table locators, retrieval time, reuse-policy URL and review date. Record public/synthetic status and track eligibility separately. Preserve the original file and extraction problems.
3. **Preserve all relevant dates.** Store covered period, event/execution date, effective date, publication/filing timestamp, available-at date and ingestion time separately. A retrospective amendment can be effective earlier than it was publicly disclosed. Never substitute quarter-end or execution date for public availability; leave unknowns unresolved.
4. **Acquire a small cached packet responsibly.** Identify scripted requests using a descriptive User-Agent and contact address; respect SEC fair access, including its aggregate maximum of 10 requests per second. Cache documents and back off on access errors. Do not build a broad crawler for this demonstration. Exclude SEC logos, seals and unrelated artwork. [SEC download guidance](https://www.sec.gov/about/webmaster-frequently-asked-questions), [SEC dissemination policy](https://www.sec.gov/about/privacy-information).
5. **Separate four kinds of content.** Tag actual public disclosures, researcher-inferred assumptions, synthetic scenario additions and model-generated candidate packages distinctly. Put hypothetical additions in separate documents/branches; never edit a historical filing into a purported actual company report. Analytical approval of an inferred assumption does not prove that the historical lender held it.
6. **Extract and review operative terms.** Check definitions, entities, threshold comparators, testing periods, exceptions, cure conditions, amendments and waivers against source passages. Inspect redlines and scanned exhibits; do not concatenate deleted and inserted language into one clause. Missing compliance inputs prevent a valid calculation. A public non-GAAP metric is not automatically contractual EBITDA.
7. **Build the reconstructed framework and guidelines.** Anchor each claim to a passage or label it as an inference with its limitations. If authentic lender guidelines are unavailable, use explicit synthetic evaluation guidelines and identify them as our modeling choice. Do not attribute invented risk tolerance, forecasts or thresholds to the actual lender.
8. **Freeze each review packet.** Save the exact eligible reports, operative package, assumption version, model/prompt/guideline configuration and historical precedents. Keep future outcomes, later amendments and evaluator answers outside model inputs. Preserve source/counterevidence links when passing earlier findings into later reviews; the model's own summary is not a new independent source.
9. **Run the intended comparison only when implemented.** Generate matched original-information and updated-information candidates under the same settings, then compare them and the original/current terms. Explain evidence-driven changes, unchanged protections and unresolved facts. If only a clause subset is supported, label the result a scoped prototype rather than a complete authentic lender package.
10. **Record observed responses without turning them into answers.** Store actual before/after terms, stated rationale or unknown, policy context and alternative explanations. An amendment can inform detection once public; it cannot establish advance warning when first disclosed with the supporting financial evidence. Judge environmental change separately from whether terms were amended.
11. **Verify the delivered packet.** Check every used URL/document identity, date cutoff, quotation, definition and calculation. Include a stable or mitigated update and an insufficient-evidence outcome. Record exact failures and reviewer limits. Famous historical outcomes may already be known to Nemotron through pretraining: date-filtered retrieval alone does not eliminate hindsight. Treat this replay as mechanism evidence, not proven early-warning accuracy.

### Instructions for a synthetic scenario informed by a real case

Keep the useful economic mechanism—such as a reporting-duty change or a covenant-definition change—while authoring an explicitly fictional borrower, coherent financials, assumptions, documents and dates. Validate the new arithmetic and contractual sequence independently. Retain a background citation describing the inspiration without asserting the fictional events occurred at the real company. Do not merely rename a real borrower while preserving its actual financial records and call the dataset synthetic.

**Selected September 20: Crocs is the presentation scenario.** Use sourced business context with fictional financials, underwriting assumptions, lender guidelines, loan terms, covenants and reports, following the [Crocs demo plan](RealityCheck-Crocs-Demo-Plan.md). Identify actual source facts and invented additions at the point of use. A real company name does not resolve Compound's financial-record restriction or authorize importing Crocs' actual financial statements into this scenario.

### Required disclosures and submission checks

The README and presentation must identify the source mode, company/facility and period, source links and reuse basis, inferred/synthetic additions, model and coding tools used, implemented versus proposed features, live versus recorded analyses and evaluation limits. Only describe historical-response learning or complete package generation as functioning after it has been implemented and checked. Do not imply company, lender or SEC endorsement.

Suggested disclosure for an eligible public-data reconstruction:

> RealityCheck uses publicly available SEC filings. Reconstructed assumptions and AI-generated alternative packages are hypothetical. Actual lender amendments are historical evidence of responses, not validated prescriptions. This demonstration does not reproduce a complete private underwriting file or establish predictive performance.

For the selected Crocs presentation, use: **“Crocs — hypothetical private-credit scenario. Company background is sourced; financial figures, loan terms, reports and scenario events are fictional.”** Preserve the distinction between sourced business context, a generated proposal, a simulated analyst adoption and an actual historical response. The historical benchmark's disclosure remains separate.

Before submission, verify the selected track's source restrictions, build-window compliance, required AI/tool credits and source inventory. The 2025 benchmark and this source review do not establish compliance with every current event, model/API or hosting term. Inference on an eligible packet is the near-term design; fine-tuning and public redistribution of model weights are separate proposed uses whose applicable terms must be checked if pursued.

## 11. Suggested Data Schema

Use a small relational schema with stable identifiers and source references. The fields below describe needed information rather than prescribing every implementation detail.

| Entity | Core information |
| --- | --- |
| Borrower | ID, name, industry, sponsor, origination date, loan type, real/synthetic designation. |
| Thesis version | ID, borrower ID, original or amendment source, effective date, approval date, approved by, superseded version. |
| Assumption | ID, thesis version, dimension, claim, source locator, economic rationale, criticality, definitions, review criteria. |
| Document | ID/version/hash, borrower/facility or shared-source associations, publisher, URL/accession, type, text, covered period, event/effective/publication/available-at/ingested-at dates, provenance, source eligibility and reuse basis. |
| Metric | Borrower ID, name, value, units, definition, measurement period, available-at date, document and source locator. |
| Evidence candidate | Document/version and exact locator, subject entity, extracted claim or change, attribution, proposed/executed/conditional status, effective date, qualifications, conflicting evidence, review status. |
| Covenant specification | Borrower/facility, approved version, definitions, input IDs, applicability, formula or obligation, threshold comparator, test dates, reporting deadlines, exceptions, cure/waiver links. |
| Relationship | Source/target IDs, relationship type, scope, applicable dates, approved formula/condition or economic rationale, provenance, approval status. |
| Scenario | Analyst-specified assumptions and affected variables, periods, source basis, owner, version, modeled outputs; stored separately from observed metrics. |
| Assessment | ID, borrower ID, as-of date, thesis version, input document IDs, model/prompt/rule version, execution time. |
| Assumption assessment | Assessment ID, assumption ID, status, credit implication, evidence references, counterevidence, missing information, suggested action, rationale. |
| Analyst decision | Assessment ID, reviewer, timestamp, accepted or overridden assessment, rationale, action taken. |
| Judgment guidelines (proposed) | Lender/domain, version, effective/available dates, risk tolerance, materiality, permitted responses and missing-evidence rules. |
| Candidate package comparison (proposed) | Original/current/candidate IDs, substantive differences, evidence and assumption links, drift assessment, matched-control outputs, model/prompt/guideline versions and precedent snapshot. |
| Observed response precedent (proposed) | Dated evidence, affected assumptions, before/after actual terms, lender action, stated rationale or unknown, policy context, alternative explanations and availability date; distinct from model proposals and evaluation labels. |
| Evidence aggregation (proposed) | Located claim IDs, source families, duplicates, corrections, disagreements, novelty and retained qualifications; a derived summary is not an independent source. |
| Company exposure and transmission (proposed) | Sourced company exposure facts, ordered economic-channel links, conditions, offsets, hypothesis/approval labels and evidence gaps; separate from realized financial inputs. |

An economic period, publication date, and actual availability date are different. Record unknown dates as unknown; do not substitute quarter-end for when a document became available. Synthetic cases must explicitly assign a simulated availability schedule.

Embeddings are optional. For a small reporting packet, direct retrieval by borrower, thesis version, and date is sufficient.

## 12. Storage and TigerData's Possible Role

B01 currently uses SQLite for its profile, source history, event queue, package versions and decisions. Preserve that working store. One database with enforced company/facility separation can support three independent report libraries; three physical databases are not required. Generalization and the final storage design remain outstanding.

TigerData/PostgreSQL is an optional migration if a demonstrated need or selected sponsor track justifies it. It is not required for the Crocs presentation; use the existing company-isolation mechanisms.

The essential capability is reproducible retrieval of **what was known at the review date**. Each assessment must retain the applicable thesis version and the exact input documents. A later amendment must not rewrite the basis of an earlier assessment.

Vector search and specialized time-series features are optional extensions. The database does not provide confidential borrower data or establish that a warning was early.

## 13. Working Technology Stack

Use the delivered stack as the starting point. The earlier Next.js/FastAPI/PostgreSQL proposal is superseded as the default build instruction; do not rewrite the working demo merely to match that proposal.

| Component | Current choice / boundary | Responsibility |
| --- | --- | --- |
| Interface | Existing HTML/CSS/browser JavaScript | Reuse the company-scoped timeline, report/source views, package comparison and analyst decisions for Crocs while preserving B01. |
| Backend | Python standard-library HTTP server | Local intake, queue, model calls, validation and calculations. |
| Model | Hosted `nvidia/nemotron-3-super-120b-a12b` for the recorded B01 profile/events | Framework generation and event attribution; final recorded events used reasoning enabled. Original CedarBridge parsing/assessment has separate model settings. |
| Storage | SQLite for B01; local JSON for the original CedarBridge flow | Preserve sources, assessments, operative versions and decisions. |
| Output validation | Existing Python source/date/identifier/label checks | Traceability and structural validation, distinct from correct interpretation. |
| Evaluation | Existing offline tests and recorded model/citation checks | Broader held-out detection evaluation remains pending. |
| Future infrastructure | Optional PostgreSQL/TigerData, retrieval or other libraries | Add only for a concrete need; no migration is implied by this plan. |

Keep model provenance on every run and recorded replay. Hosted access has been exercised, but availability and interpretation remain imperfect. Preserve failures rather than silently substituting a successful-looking result. See the [application README](realitycheck/README.md) and status record for routes, configuration and known model errors; do not copy credentials into documentation.

## 14. Core Product Architecture

The diagram below is the original assessment foundation. The planned detection extension follows it; see the current status record for the actual B01 implementation and storage stack.

```text
Analyst-confirmed thesis + applicable covenants + dated packet
                       |
              As-of evidence selection
                       |
          +------------+-------------+
          |                          |
Defined calculations          Nemotron assessment
and assumption rules          with source references
          |                          |
          +------------+-------------+
                       |
       Source, schema, date, and arithmetic checks
                       |
       Assumption status + credit implication
              + suggested action
                       |
             Analyst review / override
                       |
       Stored decision and reproducible history
```

If model analysis fails, show the failure and any completed calculations with their limited coverage. Do not present a cached or incomplete assessment as a fresh, complete result.

Planned detection extension:

```text
Deal framework + original/new evidence + fixed lender guidelines
                    + eligible historical response precedents
                                 |
          Matched original-information / updated-information runs
                                 |
                Complete candidate packages + source links
                                 |
       Substantive comparison with each other and original/current terms
                                 |
       Possible drift + attribution + uncertainty + control results
                                 |
                Analyst review and preserved detection history
                                 |
              Optional, separately approved package adoption
```

Observed lender amendments also enter as dated evidence of responses. They can inform detection without being adopted as model targets, and detection does not depend on a package adoption step.

## 15. User Experience

### Borrower review

Show the borrower, review date, thesis version, latest packet, and assumptions requiring attention. Make missing information visible.

### Assumption comparison

For each assumption, show the original claim, current status, credit implication, and suggested action. These must remain distinct labels.

### Evidence

Selecting an assessment opens the original source passage, new evidence, counterevidence, relevant metrics, and the concise explanation. Identify synthetic material prominently in the demo.

### Review timeline

Show three distinct layers: reports/evidence, credit assessments, and approved contractual packages. A new report can change an assessment without changing operative terms. Include supporting, mitigated and no-material-change updates without manufacturing divergence markers. Show when evidence became available, when an assessment ran, and what the analyst decided. Include accepted revisions without erasing the original thesis. Any later credit event is separately identified context.

The existing interaction is: inspect a claim, verify its support, and accept or override the proposed review action. The planned extension adds original/current/candidate terms, substantive differences, guideline versions and relevant historical responses beside the drift explanation. Label observed amendments and generated candidates separately.

## 16. Live Demo

**Current delivery direction:** build the [Crocs presentation](RealityCheck-Crocs-Demo-Plan.md), with real company context and wholly synthetic financial/credit material. Retain FluxRail as the working reference. Crocs is not a benchmark case. Reuse delivered report/timeline and candidate infrastructure after checking its coverage against the complete scenario agreement; scoped historical runs do not establish Crocs readiness.

### Crocs report presentation

1. Open **Crocs — hypothetical private-credit scenario** and show the approved synthetic package, generated framework and real/synthetic source distinctions.
2. Introduce a dated company or industry report that was unavailable at the previous review. Show its source eligibility and provenance; the report's availability controls its entry into a replay.
3. Extract and aggregate relevant claims, then show the direct or conditional path to that company's assumptions and covenant duties. Preserve supporting evidence, mitigants and missing links.
4. Save the report and actual model response in Crocs' isolated scenario history. Show a generated candidate and original/current comparisons only after coverage is implemented and checked; label any authored proposal separately.
5. Present possible drift, no material drift or insufficient evidence, along with a justified review action. Use supply disruption, wholesale/inventory pressure and direct-sales mitigation to explain why an external signal does or does not matter.
6. Record the analyst's decision. Only explicit adoption creates a new approved package with an effective date; detection itself does not require adoption. Preserve all earlier versions and the B01 pending third decision.

The Crocs scenario targets two reviewed simulated amendments and a final red detection/proposal left for the user, with routine and mitigating updates in between. Model outcomes are not guaranteed or hardcoded. Retain **Add information**, persistent report ingestion and clearly labeled recorded replay; each record keeps its original model/run provenance. Broader three-company comparison is a later option.

### Supporting CedarBridge mechanism example

The following retains the original CedarBridge example as a supporting mechanism story. Outcomes are intended test expectations under a predefined rubric, not hardcoded model results.

1. **Underwriting:** show five approved assumptions and their source passages. A key customer's two-year commitment supports forecast predictability.
2. **Routine update:** ingest a dated packet consistent with those assumptions. Show the evidence supporting continued routine monitoring.
3. **Meaningful contract change:** ingest an update stating that the key customer can now terminate on 30 days' notice without penalty. Reported revenue and leverage remain broadly stable. Show the original commitment, the changed clause, and a proposed credit review.
4. **Mitigated comparison:** use a separate case with a termination change but documented replacement commitments or compensation sufficient under that case's rubric. Explain the changed assumption while avoiding an unwarranted adverse escalation.
5. **Analyst decision:** open the evidence, record a review decision, and display the resulting history. If support is ambiguous, demonstrate a request for information.

The semantic test is whether the system correctly interprets the scope, conditions, and mitigation of a change and links it to the relevant assumption. Extraction-plus-rules remains a legitimate competitor.

A later adverse event is optional context. It is excluded from the earlier assessment and does not prove that the earlier alert was correct or useful.

## 17. Evaluation Plan

### Dataset and separation

Target 20–50 borrower-quarter cases across multiple borrower trajectories. Include stable borrowers, warranted review, temporary weakness, beneficial changes, conflicting reports, and missing evidence.

Separate development and evaluation by entire borrower trajectory. Freeze the prompts, rules, and label rubric before running the held-out set. Related quarters are not independent borrowers, and paraphrased copies do not establish independent generalization.

Have someone other than the prompt author prepare held-out cases. Ideally, two reviewers label assumption status, credit implication, and warranted analyst action without seeing model output or future events. Record disagreements and relevant reviewer experience. Team-only labels are provisional and should be described that way.

### Comparators

| Approach | Purpose |
| --- | --- |
| Assumption-aware rules | Compare all supplied structured facts with explicit underwriting criteria, including concentration and revenue quality. This is the numerical reference baseline. |
| Extraction plus assumption-aware rules | Extract a predefined set of facts from the same documents, then apply explicit criteria. This tests whether semantic judgment beyond extraction is needed. |
| Straightforward Nemotron prompt | Supply the same thesis and available packet with a simple instruction to identify supported concerns. |
| RealityCheck assessment foundation | Use explicit assumption records, sourced semantic assessment, deterministic checks, and review recommendations. |
| Planned package-comparison detector | Add matched candidate generation and substantive comparisons under fixed guidelines; test incremental detection value over the assessment foundation. |
| Planned detector with historical responses | Add only eligible dated precedents; test whether observed lender responses improve drift detection and attribution. |

All approaches receive the same available source information. Disclose differences in what each approach can process; beating a numerical-only baseline does not isolate semantic value. Use the same extraction stage when comparing extraction-plus-rules with the full assessment where practical.

Do not train a separate ML classifier on this small dataset merely to increase the number of comparisons.

## 18. Success Measures and Interpretation

### Primary: drift detection and attribution

- Precision and recall for material environmental change under an independently defined rubric; amendment adoption alone does not define the answer.
- False alerts on stable cases, policy-only amendments and equivalent wording; missed drift in cases without amendments.
- Evidence-supported attribution from changes in terms to changes in the environment, with explicit unresolved cases.
- Stability across repeated runs with unchanged evidence and fixed model, prompt, guidelines and precedents.
- Incremental value of package comparison and historical responses over direct assumption assessment.

Exact reproduction of adopted terms and the number of generated amendments are not detection success measures. An adopted response is a signal to interpret, not proof of drift or an optimal remedy.

### Secondary: usefulness of review

- Time to complete and verify a borrower review.
- Material concerns missed by the reviewer.
- Unnecessary review escalations and information requests.
- Evidence the reviewer can verify and assessments they accept or override, with reasons.

A small manual comparison can use matched cases and alternate assisted and unassisted review order to reduce learning effects. Report sample size and reviewer background. If no suitable reviewers are available, report system behavior only; do not claim analyst time savings.

### System behavior

- Precision and recall for warranted review alerts, using the frozen rubric.
- False alerts per stable borrower-quarter and repeated unresolved alerts.
- Unsupported factual claims and whether cited passages support the stated interpretation.
- Per-assumption assessment errors, abstention frequency, and coverage.
- Latency, failed analyses, and approximate cost per assessment.

Publish exact counts and denominators. Include missed concerns in abstained cases when reporting end-to-end results; a system that abstains on everything is not useful.

### Exploratory: earlier recognition

Measure the first warranted warning against the comparator's first warranted warning using evidence available at each review date. Compare at a similar false-alert burden and report cases with no warning. Time before a later credit event is a separate descriptive measure.

Acceptance thresholds should be set before the final evaluation based on the intended workflow. Until customer input exists, label any team-selected threshold as provisional. Strong synthetic results support controlled-case claims, not historical predictive or credit-loss claims.

## 19. What Counts as Drift?

**Change:** an observable difference in the borrower or its circumstances.

**Environmental drift:** a material change in conditions relevant to an original decision or its terms. It can be adverse, beneficial or mixed; it is not synonymous with default or deterioration.

**Package-change signal:** a substantive difference in observed lender terms or a candidate generated under fixed guidelines. It can indicate possible drift, but attribution requires supporting evidence. A policy change or model preference can also produce differences, and drift can occur without an amendment.

**Thesis drift:** a material weakening or contradiction of a specific approved underwriting assumption, established by evidence under its review criteria.

**Credit deterioration:** a worsening of repayment capacity or downside protection. It can occur with or without a changed business identity.

**Warranted review:** an action justified by material evidence, uncertainty, or the lender's review policy. Missing information can warrant review without establishing adverse drift.

A beneficial acquisition can contradict an original business-model assumption while improving credit quality. A borrower can also suffer weaker cash flow while its business model remains unchanged. Keep both possibilities visible.

## 20. Required Edge Cases

| Case | Expected handling |
| --- | --- |
| Temporary or seasonal weakness | Assess duration and the original tolerance before escalating. |
| Beneficial acquisition or strategy change | Separate the changed assumption from its credit implication. |
| Increased services mix | Verify recurrence and contract definitions rather than assume deterioration. |
| Conditional sponsor support | Distinguish a stated intention from a documented commitment. |
| PIK or amendment | Examine original terms, changes, and context. |
| Mitigating evidence | Preserve it and explain how it changes the proposed action. |
| Missing, conflicting, or stale reports | Identify the gap and use insufficient evidence where appropriate. |
| Changed reporting definitions | Reconcile comparability before interpreting a metric movement. |
| Approved thesis amendment | Use the applicable version and preserve prior review history. |
| Amendment caused by lender policy or administration | Preserve it as an observed response, distinguish its cause and do not automatically label borrower drift. |
| Environmental drift without an amendment | Detect from evidence/framework mismatch; no amendment is not a negative drift label. |
| Candidate differs because of model variability | Compare matched controls and repeated runs; do not count wording or unexplained drafting preferences as environmental change. |
| Later amendment in a historical case | Use only after its availability date; exclude it from earlier-warning inputs and held-out precedent leakage. |

## 21. Main Risks and Responses

| Risk | Practical response |
| --- | --- |
| The workflow pain is weaker than assumed | Validate a recent analyst review and the specific effort or omission the product addresses. |
| Existing products cover much of the workflow | Test the value of persistent assumption-to-evidence links; avoid claiming an empty market. |
| Synthetic scenarios encode the intended answer | Independently author held-out cases and state the limits of synthetic validation. |
| Missing access to real reporting | Treat access to suitable lender packets as a pilot prerequisite. |
| Rules match the full system | Use the simpler approach where it works and narrow the semantic role to demonstrated value. |
| Unsupported model interpretations | Use source checks, counterevidence, explicit uncertainty, and analyst review. |
| Too many alerts | Measure stable-case false alerts and repeated alerts alongside recall. |
| Excessive architecture | Keep optional agent passes, retrieval infrastructure, and portfolio features outside the MVP. |

For a production pilot, also establish acceptable document access, confidentiality, retention, and hosting arrangements with the participating lender. These are deployment requirements rather than features needed for a fictional-data demo.

## 22. Current Delivery Scope and Outstanding Build

The [status record](RealityCheck-Current-Status.md) is the implementation baseline. The selected presentation is Crocs with a synthetic package and reports, following the [dedicated plan](RealityCheck-Crocs-Demo-Plan.md). Reuse existing application patterns while keeping Crocs state distinct from B01 and the benchmark. Retain CedarBridge, FluxRail's pending decision and the 30-package pool. Additional-company expansion is not a prerequisite for this presentation.

Outstanding work, in dependency order:

1. Author and review Crocs' sourced business context, fictional financial model, lender memo/guidelines, complete synthetic agreement and dated report sequence. Use Section 10 for source rights, track restrictions and labeling.
2. Create isolated Crocs scenario records using existing company-scoped plumbing. Generate its profile from its own package; preserve definitions, evidence dates, original claims and operative scenario versions.
3. Implement qualitative evidence items, cross-source aggregation/corrections and sourced exposure paths according to the semantic intake contract. Carry evidence and counterevidence through successive reviews.
4. Populate and verify Crocs report reveal, explanation, manual entry and separate assessment/package histories. Reuse existing controls, preserve failed runs and distinguish recorded from live analysis.
5. Verify and extend candidate generation to cover the complete Crocs scenario contract, with fixed guidelines, original/current comparisons, origination controls and materiality judgments. Check stable evidence, missing facts and repeat-run variability.
6. Review genuine Crocs model outputs, record supported simulated amendments and preserve a final pending decision. Rehearse on copied state and inspect the scenario labels, dates, arithmetic and timeline.
7. Continue the historical benchmark separately with its frozen inputs, observed responses and failure records. Crocs presentation results are excluded; no improvement claim follows from a successful demo.

These are outstanding priorities, not features implemented by updating this document. Quantitative covenant expansion and an authorized external source connection remain further work; local file/API ingestion alone does not establish either capability.

## 23. Stretch Goals

After the Crocs presentation is implemented and checked:

- Compare blind reconstruction and skeptic passes through controlled experiments.
- Obtain a lender-reviewed sample and run a small real review exercise.
- Revisit the earlier three-company expansion and portfolio-level review prioritization if useful; no additional demo company is selected by the Crocs decision.
- Add ingestion and retrieval capabilities when document volume justifies them.
- Expand lender-specific review policies and approved thesis versioning.
- Broaden historical evaluation in the separate benchmark collection; do not use synthetic presentation outcomes as historical response labels.
- Test the framework in a second decision domain before claiming cross-domain transfer.
- Explore calibrated confidence only with appropriate labeled evaluation data.

Fine-tuning, broad SEC crawling, automated external notifications and portfolio risk scores remain outside the focused build. A small curated SEC packet for an eligible public-data demonstration is distinct from broad ingestion.

## 24. Team Workstreams

Assuming four people:

| Owner | Responsibility |
| --- | --- |
| Product / credit logic | Assumptions, label rubric, scenarios, analyst workflow, pitch, domain-review coordination. |
| AI / evaluation | One semantic assessment, evidence mapping, simple-prompt and extraction baselines, error analysis. |
| Backend / data | Dated input records, calculations, rule engine, provenance, database, API. |
| Frontend / demo | Assumption comparison, evidence navigation, decision capture, live demonstration. |

Separate held-out scenario authorship from prompt development as far as team size permits. The requested 2025 rule benchmark limits teams to one through four college students; do not plan a fifth team member under that benchmark. Record residual review-independence limits.

## 25. Suggested Hackathon Timeline

The table preserves the original 24-hour planning estimate, not the current progress state or permission to use work made outside the event window. Use Section 22 and the status record to identify remaining tasks; do not restart completed B01 work. Allocate the actual remaining event time to eligible data preparation, company isolation, report intake and presentation before adding optional experiments. Dates and build-window eligibility must come from the applicable event rules.

| Time | Milestone |
| --- | --- |
| Hours 0–2 | Confirm the review workflow, five assumptions, labeling rubric, demo cases, baseline definitions, and owners. Reserve held-out trajectories. |
| Hours 2–6 | Establish API access, dated input format, database records, interface skeleton, and one end-to-end assessment. Prepare evaluation cases separately. |
| Hours 6–10 | Add assumption rules, evidence checks, simple comparators, and source navigation. Test on development cases only. |
| Hours 10–14 | Integrate analyst decisions and the timeline. Exercise missing evidence, mitigation, and failure behavior. |
| Hours 14–18 | Freeze the candidate prompts, thresholds, and rubric. Run held-out evaluation and any feasible analyst-review exercise. Record errors and counts. |
| Hours 18–21 | Address demo reliability and analyze results. If evaluation cases drive changes, treat those cases as development data and disclose the loss of an untouched test. |
| Hours 21–23 | Rehearse the evidence-based pitch and both alert and benign cases. Prepare an accurately labeled backup recording. |
| Final hour | Freeze features, verify source links and demo inputs, and record final limitations. |

Evaluation design starts at the beginning, not after the product is finished.

## 26. Pitch Structure

1. **Problem:** Conditions change after a decision, and its original reasoning or terms may no longer fit.
2. **First application:** A private-credit analyst detecting meaningful changes in a specific deal; broader applications remain to be tested.
3. **Solution:** Build a framework native to the deal, interpret new evidence, and compare a newly constructed package under fixed guidelines with original/current terms. Learn detection patterns from actual lender responses without treating them as correct remedies.
4. **Demo:** Show the implemented assumption/evidence history and clearly distinguish authored amendments from generated analysis. Demonstrate live package generation/comparison only after it is implemented, including a no-drift case.
5. **Technology:** Nemotron constructs the framework and interprets evidence; candidate generation/comparison and historical-response learning are planned. Explicit calculations check supported financial conditions and versioned storage preserves the record.
6. **Evidence:** Present actual comparisons, exact counts, examples of errors, and the limits of synthetic cases.
7. **Next validation:** Test with lender-provided packets and analysts. Investigate earlier recognition only alongside false-alert burden.

Lead with the detection problem and evidence-linked mechanism. Distinguish intended capabilities from the implemented demo. Do not present detection accuracy, earlier warning, cross-domain transfer, reduced losses or model superiority as established without results.

## 27. Compound / Financial Track Positioning

The current official [Compound track](https://steelhacks.org/tracks#compound) is the financial-hack track. Its synthetic/sandbox data restriction is recorded in Section 10. Use the synthetic borrower workflow for that submission unless organizers clarify an exception for public financial records. Position RealityCheck around:

- **User:** private-credit analyst.
- **Task:** evaluate new borrower evidence against approved underwriting assumptions.
- **Decision:** which assumptions require information, reconsideration, or a fresh credit review.
- **Intended value:** faster verification, fewer missed concerns, and traceable decisions.
- **Evidence:** a working workflow and honestly bounded comparative evaluation.

This verifies the published source restriction, not overall prize eligibility or a final track selection.

### Xtract: evidence to company-specific insight

The official [Xtract track](https://steelhacks.org/tracks#x-tract) aligns with varied incoming reports, meaningful signals, source traceability and a usable output. Demonstrate passage → qualified claim → aggregated evidence → company exposure → assumption/covenant implication. Include a useful indirect connection, a mitigated case and an unrelated update. Follow the [semantic intake contract](docs/semantic-intake-contract.md); its proposed controls are project design choices, not extra sponsor rules. Public/synthetic source eligibility does not mean every public website permits document redistribution.

## 28. Nemotron Track Positioning

Nemotron constructs a deal-specific assumption framework and interprets evidence with scope, conditions and mitigation. The proposed extension reconstructs a complete candidate package under explicit guidelines so substantive differences can signal drift; historical lender responses would inform detection, not define correct amendments.

Demonstrate that contribution through comparison with a straightforward prompt and extraction-plus-rules. Multiple model roles are not evidence of improved performance.

Working explanation:

> **Nemotron builds the framework for each deal; RealityCheck aims to detect when new evidence changes how that deal would be assessed and structured.**

The official [Nemotron track](https://steelhacks.org/tracks#nemotron) asks for a role beyond conversation and evidence that it works, which can include an evaluation, comparison or documented failure. Present the recorded B01 contribution and its known interpretation errors. Claiming Nemotron is uniquely necessary requires a controlled model comparison; the recorded evolving-prompt model trials do not establish superiority.

## 29. Cold Start Positioning

If eligible, emphasize a complete and understandable workflow: original assumptions, new documents, a supported assessment, a human decision, and a measured comparison.

The current [Cold Start track](https://steelhacks.org/tracks#cold-start) requires at least 75% first-time hackers and no professional software-engineering experience among team members. Check the team's actual eligibility; the 2025 beginner-track criterion is not a substitute for this current sponsor/track rule. A reliable demonstration and honest evaluation matter more than the number of technologies or agent roles.

## 30. The Intellectual Core

Decisions depend on assumptions about the environment. New evidence can change whether their original terms still fit. A decision-specific framework makes that relationship inspectable.

The proposed moat is the accumulated, reviewed structure native to each decision: specialized definitions, assumptions, relationships, evidence, versioned terms and observed responses. Nemotron builds and updates candidate interpretations within that structure. Whether this creates a defensible commercial advantage depends on useful detection, reliable provenance, review quality and workflow adoption; it is a hypothesis, not an established advantage from using a particular model.

RealityCheck makes the connection inspectable:

> **What changed in the environment, and how is that change reflected in the terms we would choose today or the responses people actually made?**

Generated and observed changes are complementary detection signals. Their role is to reveal possible drift, not establish the optimal response. Private credit is the first application of this broader mechanism; attribution and generalization require evaluation.

## 31. Product Language

**Name:** RealityCheck.

**Working tagline:** Detect when the original decision needs another look.

**User-oriented description:** See when new information challenges the reasoning and terms of an original decision, with evidence you can verify. The first application is private credit.

**Technical direction:** RealityCheck combines a deal-native assumption framework with dated evidence and explicit judgment guidelines. Planned candidate-package comparisons and historical lender response patterns would detect possible drift, while preserving the distinction between signals, interpretations and approved terms.

**Research statement:** We aim to test whether package comparisons and observed lender responses improve drift detection beyond direct assumption assessment, with acceptable false alerts. Earlier recognition and transfer beyond private credit remain unvalidated.

Use measured results in the pitch only after evaluation; replace placeholders with actual sample sizes and outcomes.

## 32. Final Test Before Submission

A judge should be able to answer:

1. Who uses it, and during which review task?
2. Which original assumption is being assessed?
3. What evidence supports the assessment, and when was it available?
4. What credit implication is proposed, including uncertainty or mitigation?
5. What action does the analyst take or decline to take?
6. Does the system handle a benign change and insufficient evidence sensibly?
7. What did the comparison establish beyond a simple prompt or extraction-plus-rules?
8. Which materials are real disclosures, inferred assumptions, synthetic scenarios or generated candidates, and which performance claims remain untested?
9. Which source and track rules apply, and does the displayed dataset comply with them?
10. Is a changed package an observed amendment, an authored fixture or a new model output, and what evidence supports attributing its differences to environmental drift?

Every demonstrated assessment should be reproducible from its recorded inputs. Any claim of faster review needs review-time evidence. Any early-warning claim needs an appropriate temporal comparison and false-alert reporting.

Complete Section 10's source/disclosure checks and verify README credits, live/replay labels and the actual build window. Review a real-source packet separately from a synthetic combined-track submission; do not treat SEC reuse permission as an exception to Compound's data rule.

## 33. Decision Log and Open Judgments

### Confirmed user decision

| Date | Decision | Consequence |
| --- | --- | --- |
| September 20, 2026 | Use Crocs for the demo presentation: real company context, synthetic private-credit package and covenants; exclude Crocs from benchmark testing. Plan and update the Markdown files. | Added the Crocs demo plan and aligned active scope/source labels while preserving FluxRail and historical benchmark results. Crocs implementation/model runs remain subsequent work; further company expansion follows this presentation. |
| September 19, 2026 | Initial direction: analyst review first; test earlier detection. | Superseded as the primary positioning by the detection-focused decision below. Analyst review remains part of the workflow; earlier-warning performance remains unvalidated. |
| September 19, 2026 | Anchor synthetic covenant examples on a profitable software or business-services company. | Begin with a cash-flow loan template; use revenue-based or other industry structures as separate variations. |
| September 19, 2026 | Clarified that “30 covenants” means 30 synthetic companies and an individual specialized contract for each. | Produce a 30-borrower portfolio with distinct economics, contractual terms, sector protections, and borrower-scoped assumption/evidence records. Keep the earlier single-borrower clause library as supporting material. |
| September 19, 2026 | Keep the masterplan updated as the project is refined. | Record confirmed judgments separately from working recommendations and revise affected sections during the conversation. |
| September 19, 2026 | Cover all 30 covenant provisions in the assumption register, marking optional provisions. | Preserve profile selection and mutually exclusive alternatives; coverage does not elect all clauses. |
| September 19, 2026 | Attribute new events with Nemotron to company assumptions and/or individual covenants, identify exposed assumptions and proposed adjustments; implement this in the demo. | Add an event-first workflow with evidence, direct/downstream distinctions, event coverage, and analyst review; do not silently rewrite approved assumptions. |
| September 19, 2026 | Focus the next demo on three companies with separately scoped report histories. | Extend B01 with two additional companies; retain the 30 packages as a future pool. See current status for implementation boundaries. |
| September 19, 2026 | Include a complete fresh Nemotron package based on new information and compare it with old packages to detect possible drift. | Add a proposed detection stage under fixed guidelines with original/current comparisons and matched controls; authored demo amendments are not generated results. |
| September 19, 2026 | Treat private credit as the first application of a broader decision-specific workflow. | Preserve domain-native assumptions and judgment rules; test a second domain before claiming generalization. |
| September 19, 2026 | Set model judgment guidelines and use prior drifts and lender actions to inform detection. Adopted amendments are signals of environmental change, not correct remedies. | Detection is the central objective. Keep guidelines, deal assumptions and historical responses separate; assess attribution and temporal validity without optimizing amendment imitation. Learning method remains a working choice. |
| September 19, 2026 | Require semantic intake and aggregation of qualitative reports, including external events that do not name the borrower. | Implement sourced company exposure and conditional transmission paths under the semantic intake contract; retain Xtract traceability and missing-evidence boundaries. This is design work. |
| September 19, 2026 | Investigate real-company private-credit histories as potential starting material for hypothetical scenarios or reconstruction. | Research found RumbleOn/Oaktree, iRobot/Carlyle and PetIQ/Ares sufficient as starting document histories, with private-information gaps. Case selection and ingestion remain outstanding. |
| September 19, 2026 | Use the 2025 Devpost rules as the general compliance benchmark and document detailed data-use instructions. | Record SEC reuse permissions, source-specific limits and disclosure requirements. A newly verified current Compound restriction still excludes real financial records absent organizer clarification; Xtract's public-source allowance does not override it. |
| September 19, 2026 | Align the master plan with current implementation and all agreed direction. | Preserve B01/Python/SQLite, the pending third decision and the three-company scope; distinguish source research and proposed capabilities from completed model runs and features. |
| September 19, 2026 | Record article decomposition, research into unstated implications, company-context analysis and the proposed scoring approach in both project documents. | Add source-linked argument mapping, early borrower-library retrieval, bounded hypothesis testing and aggregation by distinct economic driver. Record ordinal review-priority tiers with evidence/exposure/timing separate; thresholds and routing remain unvalidated, and no application behavior changes through documentation. |

### Working recommendations in this revision

- Use Crocs with a synthetic private-credit scenario as the next presentation; retain FluxRail and keep historical benchmark work separate. Broader company/domain expansion follows the focused delivery.
- Evaluate controlled candidate-package differences and actual lender responses as detection signals; retain explicit attribution to evidence and assumptions.
- Begin historical-response learning with reviewed precedents; consider fine-tuning only if it adds measured detection value.
- Extend the current single semantic assessment with argument mapping and bounded, borrower-guided hypothesis research; retain deterministic checks and assumption-aware rules. Separate reasoning responsibilities do not automatically require separate model agents.
- Use a proposed ordinal consequence tier only as a review aid, alongside separate evidence support, exposure, direction and timing. Final lender-specific criteria and escalation rules require definition and evaluation; no summed borrower score, confidence multiplication or score-based breach rule is approved.
- Separate assumption status, credit implication, and analyst action.
- Use clearly synthetic financial material for Compound; prepare a separately labeled public reconstruction only for an eligible source/track mode. Include benign comparisons and a separate held-out benchmark.
- Treat blind reconstruction and skeptic passes as optional experiments.
- Measure evidence quality, omissions, and false alerts before promoting lead-time claims.
- Collect evidence through the application using local inputs now, curated eligible public packets where appropriate, and authorized lender sources for a future pilot.
- Use explicit relationships for evidence, assumptions, defined financial inputs, and contractual obligations. Keep possible economic effects separate from deterministic formulas and observed values.
- Store approved specifications in the existing relational database; add retrieval complexity only when document volume warrants it.

### Remaining judgments

- Exact initial analyst segment and access to a domain reviewer or lender pilot.
- Crocs' exact synthetic financials, contractual thresholds, report dates and scenario identity; company selection for this presentation is resolved. Additional-company expansion remains later scope.
- Access to complete private reporting packets and suitable pilot handling arrangements; public contract/report histories have now been located but are incomplete substitutes.
- Final track selection, current general build-window rules and team eligibility. Hosted API access has been exercised; operational availability remains a limitation. Compound public-financial-record use needs organizer clarification if pursued.
- Assumption-specific materiality criteria and acceptable review burden.
- Lender-specific anchors for the proposed 0–3 consequence rubric, unknown handling and urgency/routing policy; evaluate them separately from evidence support and covenant findings.
- Permitted targeted research sources, query budget and stopping criteria for each review; research must respect the selected source/track mode and historical availability cutoff.
- Final scope and independent review capacity for the evaluation dataset.
- Guideline format, substantive comparison/materiality rubric, and independent environmental-change labels for detection evaluation.
- Extraction and review of the located historical amendments, availability of authentic lender rationale/guidelines, and whether precedents or later fine-tuning improve detection.
- Selection of a second decision domain after the focused credit demonstration.

Record later user decisions here and update all affected sections. Working recommendations are not evidence of user approval or completed validation.

## 34. References and Evidence Limits

1. [S&P Global: iLEVEL Document Search announcement, August 7, 2025](https://press.spglobal.com/2025-08-07-S-P-Global-brings-together-Artificial-Intelligence-and-Private-Asset-Portfolio-Management-with-iLEVEL-Document-Search). Describes document analysis, source annotations, and related credit-monitoring capabilities. Supports the need to differentiate within an existing market; it does not establish a feature-by-feature equivalence with RealityCheck.
2. [Moody's for Private Credit, June 9, 2026](https://www.moodys.com/web/en/us/insights/credit-risk/private-credit/announcing-moodys-for-private-credit.html). Describes ongoing monitoring and monthly risk signals. These are vendor descriptions, not independent performance comparisons.
3. [Ares Capital Corporation 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1287750/000128775026000006/arcc-20251231.htm). Its investment schedule illustrates available loan and valuation fields. It is not a substitute for a borrower's complete private reporting packet or original lender memo.
4. [NVIDIA: Build a RAG Agent with NVIDIA Nemotron](https://developer.nvidia.com/blog/build-a-rag-agent-with-nvidia-nemotron/). Demonstrates application-side document ingestion, retrieval, and model access to retrieved context. The tutorial's stack is an example, not a requirement for this MVP; check current model availability before copying its configuration.
5. [NVIDIA NIM: Get Started with Nemotron 3.5 Lightning](https://docs.nvidia.com/nim/large-language-models/2.0.10/get-started/advanced/get-started-nemotron-3.5-lightning.html). Background serving/configuration reference, not the selected B01 model or evidence of its quality. Use the current status and application README for actual hosted model runs and limitations.
6. [Real private-credit case research](docs/real-private-credit-case-research.md). Verified starting histories and primary links for RumbleOn, iRobot and PetIQ, plus insufficiency findings for alternatives. Source discovery is complete; packet preparation and model evaluation are not.
7. [Semantic intake ground rules](docs/semantic-intake-contract.md). Working requirements for qualitative extraction, aggregation, company exposure and indirect-event attribution; not a completed pipeline.
8. [SEC reuse FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions) and [dissemination policy](https://www.sec.gov/about/privacy-information). Source-reuse and scripted-access basis for the SEC subset, checked September 19, 2026. Not a license for every external research link.
9. [2025 SteelHacks rules](https://steelhacks-xii.devpost.com/rules), the user-requested general benchmark; [current official tracks](https://steelhacks.org/tracks) for Compound, Xtract, Nemotron and Cold Start requirements checked September 19, 2026. Section 10 distinguishes source rights from track eligibility.

These references informed the project evaluation and documentation on September 19, 2026. The market comparison is illustrative rather than exhaustive. Synthetic examples remain fictional; the linked real-company histories contain public observations and actual amendments, with explicitly identified gaps. Neither constitutes a completed detection benchmark or a complete private underwriting file. Preserve this distinction when updating the plan or pitch.
