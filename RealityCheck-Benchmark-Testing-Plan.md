# RealityCheck — Benchmark Testing Plan

**Created:** September 19, 2026  
**Last updated:** September 20, 2026  
**Status:** Strict blind replay run, locked and compared for two development histories (iRobot, RumbleOn) and one unseen history (PetIQ). Results are mixed and show no advantage over direct review; see Section 13. Stability checks and an independent reviewer are outstanding.  
**Primary benchmark:** Replay real-company information chronologically, withhold actual subsequent package/covenant amendments, and compare RealityCheck's independently generated progression with the observed lender history afterward.  
**Scope:** The complete RealityCheck credit-review workflow, with a later analyst study to measure decision quality and effort.

This is the maintained benchmark record. **User instruction: update this document as the benchmark is discussed and refined in this conversation.** Record confirmed direction separately from proposed controls and unresolved choices. It supplements the [master plan](RealityCheck.md) and [current status](RealityCheck-Current-Status.md). Recording this plan does not implement capabilities, ingest real-company data, recruit reviewers or run the benchmark.

### Demo and benchmark scope

| Item | Dataset and purpose | Current state |
|---|---|---|
| Working application demo | FluxRail (B01), a fictional company, with synthetic evidence and an authored package/amendment history. Demonstrates the interactive workflow. | Implemented: two adopted fictional amendments and a third pending detection/proposal. |
| Selected next presentation demo | **Crocs**, using sourced real business context with synthetic financial inputs, loan terms, covenants and scenario reports. | **User-selected September 20 for the demo, explicitly not the benchmark.** Planning and documentation only; the Crocs dataset and application experience are not built. See the [Crocs demo plan](RealityCheck-Crocs-Demo-Plan.md). |
| Earlier demo expansion | Three company workspaces with separate report histories. | Retained as a later expansion direction. As an implementation sequencing choice, prioritize the selected Crocs presentation before adding further borrowers; this does not record a user cancellation of the earlier three-company idea. |
| Historical benchmark | Real-company origination information and dated reports, with actual subsequent amendments withheld for later comparison. Tests the complete mechanism against observed history. | iRobot/Carlyle (R01) and RumbleOn/Oaktree (R02) have source packets, blind inputs, exclusion logs and a separate evaluator collection. Both are development histories (Section 13). PetIQ/Ares (R03) has cached source documents only and is the one history no model run has touched. Crocs is excluded from this benchmark. |

The presentation and the historical benchmark have separate purposes and datasets. Crocs is the selected next presentation scenario; FluxRail remains the working synthetic demo and is preserved. The September 20 selection updates the earlier presentation direction without changing the historical benchmark histories, controls or results.

### Selected demo: Crocs, synthetic credit scenario

**User-selected September 20, 2026; planned, not implemented.** Use Crocs as the real business setting for the fictional private-credit presentation. The user explicitly excluded Crocs from benchmark testing and requested the plan and Markdown changes at this stage. Recognition of the business should help explain the exposures; the fictional facility and scenario events must not be presented as actual Crocs financing or developments. The [Crocs demo plan](RealityCheck-Crocs-Demo-Plan.md) governs the presentation design and build sequence.

Recommended design:

| Layer | Treatment |
|---|---|
| Real company context | Use sourced, dated descriptions of the business, products and relevant operating exposures. Distinguish documented facts from inferred connections. |
| Synthetic opening deal | Author coherent financial inputs, underwriting assumptions, lender guidelines, loan terms and covenants. Label them hypothetical; do not present them as the company's actual financing or private lender records. |
| Synthetic developments | Use clearly labeled scenario reports and financial updates. Do not imitate actual company announcements or describe fictional deterioration, missed payments or breaches as real events. |
| Nemotron output | Analyze the defined scenario and cite its evidence. Label generated packages and any finding of noncompliance as hypothetical scenario results. Retain uncertainty and human review. |

Use the visible title **“Crocs — hypothetical private-credit scenario”** and a short explanation: **“Company background is sourced; financial inputs, loan terms and scenario events are fictional.”** Preserve these distinctions on the profile, report cards, divergence details and exported material. Input metadata and prompts should carry the same labels so Nemotron does not silently substitute remembered real financing terms or historical outcomes for the scenario's defined facts.

Build Crocs's scenario around its documented footwear sourcing, wholesale and direct-to-consumer business exposures; changing the name on FluxRail's software-business package would not create a coherent scenario. Preserve the working FluxRail demo and its user state while preparing Crocs as a separate presentation scenario. Detailed synthetic terms and report outcomes remain to be authored and verified under the demo plan.

Keep Crocs in a separate company/scenario record from the historical benchmark. Exclude its company context, synthetic inputs, reports, model runs and amendments from historical benchmark inference inputs, evaluator collections and scores. Its invented amendments cannot be scored as correspondence with actual lender behavior, and it must not contaminate reserved unseen benchmark histories. R01/R02 development status, R03's reserved unseen status and the Section 13 execution record remain unchanged by this presentation selection.

**Data boundary checked September 20, 2026:** the [official Compound track](https://steelhacks.org/tracks#compound) requires synthetic/sandbox data and excludes real financial records. A fictional loan layered over copied actual financial statements does not make those statements synthetic. Keep the scenario's financial inputs synthetic; the published rule does not specifically resolve every aspect of presenting a real company name. Public business context and financial records must remain distinguishable. This option is a presentation recommendation, not a blanket eligibility finding.

### Company shortlist and selection record

**Researched and selection updated September 20, 2026.** The user selected **Crocs** from the three prospective presentation companies. Wayfair and Sweetgreen remain unselected alternatives; the earlier recommendation ordering is superseded by that choice. These presentation candidates are separate from the iRobot, RumbleOn and PetIQ historical benchmark histories.

| Option | Verified business context | Illustrative synthetic scenario and review targets | Presentation fit |
|---|---|---|---|
| **Wayfair — unselected alternative** | Home-goods retail supported by suppliers and its CastleGate/Wayfair Delivery Network logistics operations. [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1616707/000161670726000027/w-20251231.htm). | A hypothetical facility supporting logistics investment. Fictional shipping disruption and weaker home-goods demand test assumptions about delivery costs, order volume and cash generation. Review scenario liquidity protections, cash-flow reporting and discretionary capital expenditure. Determine who bears freight costs and whether logistics fees or other mitigants offset them before asserting a borrower effect. | Rich connection from external developments through borrower operations to a package decision. |
| **Crocs — selected for the presentation demo** | Footwear supplied by overseas third-party manufacturers and sold through wholesale and direct-to-consumer channels. [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1334036/000133403626000006/crox-20251231.htm). | A hypothetical working-capital facility. Fictional freight delays followed by a wholesale slowdown test supplier reliability, inventory conversion and margin assumptions. Review scenario inventory reporting, liquidity and leverage protections; introduce stronger direct sales as counterevidence. | Recognizable product and a clear global-sourcing-to-cash-flow explanation. |
| **Sweetgreen — unselected alternative** | Restaurant business with domestic food partners and regional distribution networks. [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1477815/000162828026012520/sg-20251228.htm). | A hypothetical restaurant-expansion facility. Fictional crop disruption raises scenario ingredient costs, while weaker traffic pressures restaurant economics. Test cost and expansion assumptions; review scenario cash minimums, restaurant reporting and conditions on expansion spending. | Familiar unit economics make the report-to-package connection quick to explain. |

All financing purposes, events, numerical effects and covenant responses above are scenario proposals, not statements about the companies' actual financing, current creditworthiness or recent events. These annual reports verify business context only; actual financial statements are not being copied into the synthetic demo. The presentation selection is Crocs; the retained alternatives document the earlier shortlist and are not a financial ranking or additional implementation commitments.

## 1. The question the benchmark must answer

> Does using RealityCheck lead to better, earlier and more defensible decisions about whether a loan package still fits the borrower's circumstances?

The unit of evaluation is **a borrower relationship over time**. The test must cover the original decision, its assumption framework, new evidence, reconstructed packages, substantive comparisons, analyst decisions and the effect of those decisions on later monitoring.

**The first benchmark will test this through historical replay.** Starting from a real company's original deal information, can RealityCheck identify evidence-supported reasons to reconsider the package and generate a defensible progression of proposals without seeing the actual subsequent amendments? After the outputs are frozen, compare the timing, affected provisions, direction and rationale with the lender's observed progression.

The broader product hypothesis remains that RealityCheck helps an analyst recognize when a package warrants reconsideration, while controlling unnecessary escalations and verification effort. A later analyst study is needed to measure that benefit directly. Historical agreement alone does not prove that RealityCheck is better than an analyst or that a lender's actual amendment was optimal.

Extraction accuracy, citation checks and individual attribution results remain useful diagnostics. They cannot substitute for evaluating the final credit-review decision. More alerts, more package changes or longer explanations do not establish improvement.

## 2. The complete workflow under test

```text
Original borrower documents and lender guidelines
    → Nemotron-generated company profile, assumptions and relationships
    → Analyst review of the initial framework
    → Successive dated reports and accumulated company evidence
    → Updated assessment, including researched indirect implications
    → Complete generated candidate package
    → Comparison with original and current approved terms
    → Evidence-linked finding about possible drift
    → Analyst decision and any explicitly approved amendment
    → Correct use of the operative package at the next review
```

Begin from source documents, not a manually perfected assumption map. Record initial omissions, unsupported inferences, analyst corrections and setup time. Preserve both raw model output and the approved framework so human repairs are not credited to the model.

At each review point, RealityCheck must retain the distinction between:

- A change in business conditions or an exposed assumption.
- A current contractual duty, failure or unresolved compliance question.
- A protection gap that may justify reconsidering the package.
- A proposed package and an adopted, operative amendment.

A complete candidate may preserve most or all existing provisions. Score the justification and coherence of its terms, including retained protections. Do not require a change to every clause or assume that a newly drafted package is superior merely because it differs.

In the primary blind replay, actual later amendments and adoption decisions are unavailable to the model. Its generated candidates form an analytical proposal history; they do not become the real company's operative contracts. The adoption and subsequent-operative-monitoring stages are exercised separately as described in Section 6.

## 3. Comparison workflows

### Primary comparison: RealityCheck's independent progression versus actual history

**Confirmed user direction:** supply the initial library-building information and subsequent new information, while withholding the actual subsequent package/covenant amendments from Nemotron. The original agreement and original covenants are part of the starting input.

| Material | Treatment in the strict blind replay |
|---|---|
| Original borrower profile, financials, original agreement and contemporaneous deal rationale | Supplied to build the initial library. Missing private underwriting assumptions remain missing or explicitly reconstructed. |
| Lender guidelines | Supply authentic contemporaneous guidelines if available; otherwise disclose and freeze reconstructed evaluation guidelines before examining the target amendments. |
| Subsequent operating, financial and industry information | Released chronologically using eligible passages available at the checkpoint; retain dates, provenance and qualifications. |
| Actual later amendments, restatements, waivers, lender decisions and descriptions of their terms | Held in a separate evaluator collection and withheld throughout the strict replay, including when they have become public. |
| RealityCheck's generated profiles, findings and candidate packages | Saved as its independent progression, with no feedback from the hidden actual history. |
| Later company outcomes and retrospective explanations | Withheld until appropriate retrospective evaluation; never used to justify what the model should have known earlier. |

At each checkpoint, freeze RealityCheck's assessment and complete candidate. After the replay is complete, reveal the actual amendment history for evaluation. Compare whether the same underlying exposure was recognized, which provisions were addressed, how terms changed, whether any overlap was justified by the available evidence, and what differed or remained unknown.

An actual amendment supplies an observed response, not an unquestionable answer. A defensible mismatch may arise from missing private information, different lender policy or negotiation. Conversely, matching an amendment without supported reasoning does not demonstrate useful detection. Preserve both response correspondence and independent assessment of evidence quality.

### Secondary comparison: does the RealityCheck mechanism add value?

Run a capable Nemotron workflow that directly reviews the existing package under the same blind information restrictions. Both receive the same original deal, chronological evidence and lender guidelines, and may identify a need for review or propose changes. RealityCheck additionally maintains its explicit framework and generates complete candidates for structured comparison.

Hold model version and inference settings fixed where applicable. Use the same frozen, eligible evidence collection and record retrieval, context selection, token usage and processing budgets. Do not weaken the comparator by giving it only the newest article or withholding relevant borrower documents. Neither workflow receives hidden amendments.

Compare both with the same hidden historical record and independently reviewed criteria. This supports a claim about the contribution of RealityCheck's architecture beyond a general model-assisted review; it does not establish analyst time savings.

### Later product study: analyst workflow with and without RealityCheck

| Condition | Information and tools | Required output |
|---|---|---|
| Conventional credit review | Original memo, financial information, current agreement, prior amendments and all reports available at the review date, using the reviewer's normal tools. Document those tools, including any ordinary AI assistance. | Current assessment; whether to maintain monitoring, request information, update the internal view or initiate a package review; supporting reasons and any proposed changes. |
| RealityCheck-assisted review | The same available evidence and lender guidelines, plus RealityCheck's generated profile, assumption history, candidate package, comparison and explanation. | The same decisions, with the analyst accepting, correcting or rejecting the system's findings and proposed terms. |

This is a separate study of analyst benefit, not the primary historical benchmark. It can give both conditions the known operative amendments as of each date, because its purpose is realistic current-package review. Recruit reviewers with relevant credit-review experience and record their experience and role. Use different, matched histories in the two conditions, with assignments and order rotated to reduce case-memory effects. Keep evidence releases and review tasks equivalent.

Measure the analyst's final decision separately from the system's uncorrected finding. Record all verification and correction effort. Human rescue of an incorrect output is useful workflow evidence, but is not a correct unassisted model result.

Further comparisons that remove individual stages, or substitute other Nemotron models, are optional diagnostics after the complete workflow has been evaluated. They are not the headline benchmark.

## 4. Borrower histories and test cases

**Primary benchmark direction: real-company historical cases.** The [public-case research](docs/real-private-credit-case-research.md) identifies RumbleOn/Oaktree, iRobot/Carlyle and PetIQ/Ares as candidate histories with original agreements, subsequent changes and borrower reporting. These remain candidates; this update does not select final cases or claim that complete packets are prepared.

No complete private underwriting memo, authentic lender guidelines or full private reporting stream was located in that research. Label the initial library as reconstructed from public evidence where appropriate. Do not attribute inferred beliefs or invented policy to the historical lender, or fill missing inputs from later amendments.

Keep this research benchmark distinct from the existing synthetic presentation dataset. The [recorded data-use instructions](RealityCheck.md#10-data-strategy) state that the Compound submission requires synthetic/sandbox financial inputs absent organizer clarification; public-source permission for Xtract does not override that restriction. The real-company replay can be planned here without asserting eligibility for every prize. Recheck the selected submission's rules before ingestion or inclusion in a submission.

B01 remains a development and presentation example. Its existing three scenarios have influenced prompts and corrections and must not be described as unseen benchmark cases. Crocs is the selected next presentation scenario and is excluded from this historical benchmark's inputs, evaluator collection and scores. Synthetic histories can test mechanisms and leakage controls separately, but must not be labeled actual company or lender progression.

The following are proposed story types, not selected additional borrowers or authored test results:

| History | Product capability challenged | Required decision tension |
|---|---|---|
| Deterioration before a formal breach | Recognize that the original underwriting rationale or protections may no longer fit even while financial covenants pass. | Escalate when available evidence justifies review without inventing a current breach. |
| Concern followed by mitigation | Integrate borrower-specific protections, contradictory evidence and recovery over time. | Avoid unnecessary escalation or amendment; revise earlier concerns when the evidence changes. |
| Changing contractual history | Compare an independently generated proposal sequence with several actual amendments; separately replay known terms for operational testing. | Keep hidden historical terms out of the blind run and use correct operative duties when testing the separate amendment-aware mode. |

Each history should include origination, several predetermined review dates, stable periods, uncertainty and meaningful changes where the source record supports them. Six to eight updates per company is a planning target, not a required number of divergences. Do not invent reports or amendments to make a real history fit a desired story. Include regularly scheduled no-change and insufficient-evidence checkpoints instead of selecting only dates near known amendments.

Prepare test histories independently of prompt development. Freeze the test versions before running either workflow. If a case is used to tune prompts, move it to development and reserve a different history for the next unseen evaluation. Preserve the original result when a failed test later motivates a fix.

Three histories provide a small feasibility study. Multiple checkpoints from one company and repeated model runs are correlated observations; report the number of companies, histories and checkpoints separately rather than presenting every checkpoint as an independent borrower.

## 5. Reference judgments and temporal controls

Maintain two reference layers: **observed historical responses** extracted from executed amendments, and **evidence-based judgments** about what the allowed information justified at each checkpoint. A reviewer should prepare the latter without seeing model outputs and, where feasible, without first seeing the target amendment. Use a fixed rubric, adjudicate disagreements and preserve uncertainty. If independent credit review is unavailable, disclose author review and avoid claiming expert-validated decisions.

Each reference record should specify:

- Evidence available at the cutoff, with publication, availability and effective dates where relevant.
- The terms visible in the tested mode and applicable lender guidelines; retain actual later operative terms separately in the evaluator record.
- Whether material reconsideration is warranted, unwarranted or unresolved, and why.
- Affected original assumptions and the supported connection to the decision.
- Covenant findings relative to the disclosed contractual baseline, distinct from future pressure or protection gaps. In the strict blind run, do not score a finding as an actual current breach under amendments the model was not permitted to see.
- Acceptable actions and package constraints, allowing multiple defensible responses.
- Missing information, unsupported conclusions and evidence that would resolve uncertainty.
- The earliest checkpoint at which a particular review or information request is justified by available evidence.

Do not use an adopted historical amendment as the sole correct answer. Negotiation, lender policy and administrative changes may explain a revision; environmental drift can also occur without one. Grade substantive reasoning and acceptable protections rather than exact wording, a single preferred interest rate or similarity to an authored amendment.

Maintain hidden evaluator records separately from inference inputs. In the strict blind run, exclude **all post-origination actual amendments**, including amendments dated before a later checkpoint. Exclude later reports, later outcomes and held-out case answers as well. Other historical precedents must have been available at the cutoff and must not reveal the evaluated company's hidden responses.

Use frozen source snapshots for reproducible research. The benchmark should not accidentally expose current web material when replaying an earlier decision date. Both workflows must have equivalent access to the eligible evidence, even if they organize or retrieve it differently.

### Amendment leakage inside ordinary reports

An operating report, filing, note, compliance certificate or linked exhibit may quote amended limits, describe a waiver or announce that lenders changed terms. Audit these passages as potential target leakage even if the document is otherwise eligible. Preserve the original source and prepare a separately labeled, reviewed input version that excludes response-revealing material, with an exclusion log. Check headings, metadata and retrieved snippets as well as body text.

Do not silently alter financial facts or remove difficult evidence to improve scores. Where operational facts and the amendment cannot be separated without distortion, use an earlier independent source or mark the checkpoint unsuitable for blind evaluation. Later interest expense, liquidity or borrowing balances may themselves reflect a hidden amendment; label this dependence and do not treat the actual trajectory as the economic outcome of RealityCheck's unadopted proposals.

If the first public evidence of a problem appears alongside or after the amendment, the public-data replay cannot establish advance detection of that response. Record the information gap rather than treating missing private lender information as a failure to reason.

Famous company outcomes may already be present in model training. Date filtering and hiding files cannot eliminate pretrained hindsight. Disclose this limitation and use additional unseen synthetic mechanisms or new held-out histories to test generalization. Masking names can be a sensitivity check, not proof that contamination has been removed.

## 6. Keep replay modes separate

### A. Primary: strict blind historical replay

Both workflows start from the same original package and receive the same allowed information sequence. The actual post-origination amendment history stays hidden for the entire run, including from any person whose feedback is returned to the inference workflow. Save and lock all outputs before revealing that history for comparison.

Keep the original contract as the known contractual baseline. Generated candidates may be retained and compared with prior candidates to show the proposed progression; they are not automatically adopted. Later model findings must identify whether they refer to original terms or a proposed package. Because actual intervening changes are hidden, this mode tests independent reconstruction and detection, not compliance monitoring against undisclosed current terms.

### B. Optional: rolling replay with known prior amendments

For a separate realistic-monitoring test, predict before a target amendment, lock the output, then reveal that amendment only once it was actually available. Use it as the operative context for later checkpoints while withholding future amendments. Give both workflows identical known package states.

This is a different experiment from the user's strict blind benchmark. Report its results separately; it tests one-step reassessment with known past decisions, not independent reconstruction of the entire amendment history.

### C. Adaptive demonstration using simulated review decisions

Run a separate sequence in which an analyst's explicit decision updates the operative package. Then introduce another report and verify that RealityCheck uses the revised terms, preserves the prior state and carries unresolved issues forward correctly.

The analyst may adopt, modify, defer or reject a proposal. A new red detection can remain pending. No-change decisions are valid outcomes.

Label this as an adaptive demonstration. Do not combine its later scores with the controlled comparison as if both workflows had identical package states. Unless the scenario explicitly models an amendment's economic effect, do not claim the amendment changed the borrower's subsequent financial outcome.

### D. Controls for apparent drift caused by generation

Generate an origination-only candidate under the same model, prompt, guidelines and eligible precedent settings used for the updated-information candidate. A gap already identified from original information should be labeled a pre-existing concern rather than newly emerging drift.

Repeat unchanged-evidence assessments and test equivalent wording. Record unstable proposals and false divergence markers. Freeze model and policy settings within comparisons; later changes to either must not be presented as changes in the borrower.

## 7. Measures and scoring

The primary outcome is the quality of the decision to revisit the package, assessed together with unnecessary escalation and missed-review burden. Agree the materiality definitions, acceptable action sets, time budget and tolerable false-alert burden with reviewers before examining results. Do not select thresholds afterward to favor RealityCheck.

For the historical benchmark, report **correspondence with observed amendments** alongside **independent support for the proposed decisions**. These answer different questions. A recommendation without a matching actual amendment is not automatically a false alert; absence of a recommendation before an amendment is not automatically an error when the necessary evidence was unavailable.

| Question | Measure and interpretation |
|---|---|
| How did the proposed progression correspond to actual changes? | Compare affected clause families, substantive direction, scope and stated rationale. Predefine how related proposals and amendments are matched, including one-to-many events and the time window. Report exact threshold correspondence separately when the source inputs support it. |
| How did timing compare with the historical response? | Record the model's first evidence-supported finding, actual execution/effective date and public disclosure date separately. An earlier simulated finding supports an advance-warning claim only when its permitted evidence was available before the actual response; earlier than disclosure alone is insufficient. |
| Which historical responses were assessable? | Report amendments with sufficient preceding public evidence, those with missing or inseparable evidence, and unknown lender rationale. Define eligibility before scoring; retain excluded cases and reasons in the inventory. |
| Was a warranted review identified? | Count justified review checkpoints or episodes detected and missed, using a predefined rule for grouping repeat alerts. Show numerator and denominator. |
| Were unnecessary interventions avoided? | Count escalations at reference checkpoints where escalation is not warranted; report the rate among eligible no-escalation checkpoints. Distinguish a justified information request from an unnecessary package review. |
| Was detection earlier? | Compare the first justified detection checkpoint for the same concern at comparable false-alert burden. Report missed cases separately; do not calculate lead time only on successful cases and imply universal detection. |
| Did reconstruction reveal a meaningful gap? | Record supported protection gaps found, material gaps missed and proposed differences unsupported by new evidence or already present at origination. |
| Was the complete candidate package coherent? | Review lender-guideline compliance, coverage of the actual exposure, retained protections, definitions, internal consistency, thresholds, timing and corrections needed. Score the complete package, not only changed clauses. |
| Did the initial framework work? | Record critical source assumptions omitted, unsupported claims introduced and analyst corrections needed before monitoring. Include onboarding time. |
| Did the analyst make a better decision? | In the later analyst study, compare final decisions against acceptable reference actions; record any model error corrected or propagated by the reviewer. Historical correspondence alone does not answer this question. |
| Did the workflow save effort? | In the analyst study, measure active review, verification and editing time. In every run, record elapsed time, model latency and token/tool usage. Report setup and recurring costs separately. |
| Was state preserved correctly? | Check evidence cutoffs, resolved versus outstanding findings and prior versions. In the blind run, verify the original/proposed/hidden-actual separation; in rolling or adaptive modes, check the operative version and effective date. |

Use a simple anchored assessment for package defects: **no material defect**, **correction required**, or **material defect affecting the decision**. Define examples with reviewers before the run; retain individual dimensions and rationale instead of hiding contradictions inside one average score.

The proposed 0–3 potential-consequence tier in the master plan prioritizes review. It is not the benchmark's accuracy score or proof that a breach occurred. Assess the correctness and usefulness of prioritization separately.

Report results per history and in aggregate, with raw counts, denominators, disagreements, failures and missing outputs. Treat timeouts, invalid packages and unsuccessful runs as recorded outcomes, not silently discarded examples. Record retries and any human intervention. Repeated runs reveal variability but do not create additional independent test cases.

## 8. Execution sequence and retained evidence

1. **Confirm readiness.** Verify that the tested workflow can generate its own profile, maintain history, generate complete candidates, compare terms and record analyst decisions. List any absent stage explicitly.
2. **Prepare development and test histories.** Select eligible historical borrower/facility periods, assemble original and subsequent information, audit embedded amendment leakage and keep actual amendments in the evaluator collection. Define source releases and missing-data exclusions. Preserve the live B01 presentation database and pending third decision.
3. **Prepare and review reference judgments.** Freeze acceptable actions, package criteria, historical-response matching rules, scoring rules and evidence cutoffs before outputs are inspected. Label authentic, inferred, reconstructed and synthetic material separately.
4. **Freeze configurations and reviewer assignments.** Record model identifiers, settings, prompts, guidelines, source manifests, allowed tools and run budgets. Allocate matched histories across conditions.
5. **Run and lock the strict blind replays.** Start at origination, release information sequentially and retain every checkpoint result. Do not feed back any part of the hidden actual progression.
6. **Assess the outputs and reveal the actual history.** Review evidence support without model/condition labels where feasible, then compare the locked proposals with historical amendments. Keep the independent judgment and response-correspondence records separate.
7. **Run stability checks and any later modes.** Label rolling replay, adaptive demonstration and analyst-study results separately. Their visible contractual information differs from the primary blind experiment.
8. **Publish the full result record.** Include per-case outcomes, package differences, corrections, timings, failures and limits on interpretation. Select presentation examples after the complete result set is retained, without omitting unfavorable results from the summary.

For every run, retain the borrower/history/checkpoint IDs, replay mode, cutoff, visible contractual baseline, source manifest and exclusion log, configuration versions, raw model output, generated candidate, substantive comparison, system finding, analyst corrections, final action, simulated adopted version if any, evaluator judgment, timing and resource usage. Keep target amendment IDs and matching results in the evaluation records, outside the inference context.

Store benchmark state separately from the demonstration's persistent user state. Never reset or overwrite `realitycheck/b01.sqlite` to run these tests.

## 9. Benchmark results presentation

This section presents the historical benchmark evidence. The separate Crocs application presentation follows the [Crocs demo plan](RealityCheck-Crocs-Demo-Plan.md); its synthetic amendments are not an actual-history comparison lane or benchmark results.

Show two synchronized timelines: **the company's actual package/amendment progression** and **RealityCheck's independently generated findings and proposed packages**. Reveal the actual-history lane only after the blind outputs have been locked. Distinguish report arrival, a supported review finding, a generated proposal and a historical executed amendment. The optional direct-review model can appear as a third comparison lane.

Suggested presentation sequence:

1. Introduce the original borrower rationale and package, with the generated assumption framework.
2. Advance the report history to a checkpoint that tests whether the package still fits.
3. Show RealityCheck's saved finding and proposal at that cutoff, with the actual amendment still hidden.
4. Open the pivotal detection to inspect the evidence, changed assumptions, complete generated candidate and substantive differences.
5. Reveal the actual historical change and compare its timing, affected clauses and rationale with the locked proposal. Show the independent reference judgment, unresolved facts and reviewer corrections alongside the comparison.
6. Demonstrate a mitigated or unchanged case to make unnecessary escalation visible.
7. In the separate adaptive sequence, review an amendment and show how the next event is evaluated under the new operative terms. Leave the final detection pending where appropriate.
8. Display the full benchmark summary, including failures and processing/review effort.

Use genuine saved runs for reproducible results, labeled with model and execution date. A fresh live analysis may supplement them. A live case without a prepared or subsequently reviewed reference remains unscored until that review occurs; a saved result must not be presented as a fresh inference.

## 10. Current implementation boundary and outstanding choices

The [B01 verification record](docs/b01-demo-verification.md) documents genuine hosted Nemotron profile/event analyses, authored amendment instruments, versioned state and a branching interface. Existing offline tests and citation verification demonstrate particular implementation properties; they do not establish comparative product performance.

Scoped candidate generation/comparison and development replays are recorded in Section 13. Complete Crocs scenario coverage, the expanded research loop, additional-company presentation scope and the analyst study remain further work. Authored B01 amendments must not be counted as Nemotron-generated packages. The recorded development results do not demonstrate a benchmark advantage or analyst productivity improvement.

The user's historical-replay clarification replaces this document's earlier proposal to make an analyst comparison on synthetic histories the first benchmark. That comparison remains a later product study. The subsequent Crocs selection applies to the presentation demo only: planning and Markdown updates are authorized at this stage, FluxRail is preserved, and no Crocs implementation or benchmark run is recorded here. Historical benchmark execution and results are recorded in Section 13.

Before execution, finalize:

- The historical companies, facilities, periods and source eligibility, plus separate development material.
- Reviewer availability, expertise, independent adjudication and condition assignment.
- Materiality criteria, acceptable actions, package-quality anchors and false-alert tolerance.
- Exact review checkpoints, amendment matching windows, leakage exclusions, repetition budget, time limits and failure handling.
- The conventional toolset and the strong direct-review Nemotron comparator.
- Which proposed capabilities are ready to include and which claims remain outside scope.

If qualified reviewers are unavailable, label the technical replay and author-reviewed judgments accordingly. It can show how the complete system's proposals correspond to observed history; it cannot establish expert-validated decision quality or analyst time savings. Incomplete public inputs and pretrained hindsight limit inference about historical prediction. Three histories also do not establish improved lending outcomes, customer demand or willingness to pay; those require broader evaluation and user research.

## 11. Relationship to the Nemotron track

The [official Nemotron track](https://steelhacks.org/tracks), checked September 19, 2026, accepts evidence such as an evaluation, comparison, benchmark or documented failure. This plan makes Nemotron's contribution visible through the complete product: constructing the framework, reassessing the relationship and producing the candidate and explanation used in review.

The proposed methodology is RealityCheck's evaluation design, not a sponsor-prescribed benchmark. [NIST AI RMF guidance](https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/) supports validation against intended use, human–AI performance and clearly documented test conditions; it does not validate RealityCheck or this particular protocol.

The eventual presentation should report the observed result, including mixed or negative findings. A defensible conclusion identifies the tested histories, workflow, decision measures and costs, rather than claiming that the system generally produces optimal loan terms.

## 12. Benchmark discussion log

| Date | Direction or clarification | Effect on this plan |
|---|---|---|
| September 19, 2026 | Evaluate the complete RealityCheck workflow rather than limiting the benchmark to ingestion or attribution. | Retained origination, generated assumptions, package reconstruction, comparison, decisions and history in the evaluation scope. |
| September 19, 2026 | User requested an ongoing benchmark document and clarified the intended comparison: real-company progression, with initial and subsequent information supplied but actual later amendments withheld. | Made strict blind historical replay the primary benchmark; moved the analyst study later; separated hidden actual amendments from generated proposals and optional rolling/adaptive modes. No ingestion, model calls or benchmark runs performed. |
| September 19, 2026 | Clarified which companies belong to the demo versus the benchmark. | Recorded the working FluxRail synthetic demo, planned expansion to three synthetic companies including FluxRail, and separate proposed real-company benchmark. No additional companies selected or implemented; no scope change. |
| September 19, 2026 | User restated the split after real-company workspaces had been built into the demo app: **the demo is FluxRail; the benchmark is portrayed with the existing real companies**, following this plan. | Real cases removed from the demo company list and their state moved to `realitycheck/benchmark/`. Earlier real-company runs reclassified as rolling-mode development runs (Section 6B), not the primary benchmark. Strict blind inputs, exclusion logs, evaluator collection, blind runner and comparator built; first blind runs started. Section 13 added. |
| September 20, 2026 | User asked about an actual company with a synthetic private-credit scenario for the demo. | Recorded as an option: sourced business context, fictional financial inputs/terms/reports, visible scenario labels, and separation from historical benchmark records. FluxRail preserved; no company selected, replacement approved, dataset built or model run performed for this proposal. |
| September 20, 2026 | User requested three prospective companies for that hypothetical demo. | Added Wayfair, Crocs and Sweetgreen, with primary-source business context, illustrative synthetic credit stories and presentation tradeoffs. Wayfair recommended for indirect-event reasoning; no selection, application changes or model runs. |
| September 20, 2026 | User selected Crocs: real company context with a synthetic package and covenants, explicitly for the demo presentation and not benchmark testing; requested planning and Markdown changes. | Crocs is the selected next presentation scenario, with synthetic financials and reports under the linked demo plan. Preserve FluxRail; sequence further company expansion after Crocs. Exclude Crocs from historical benchmark inputs, evaluator collections and scores. Wayfair and Sweetgreen remain unselected alternatives. Documentation only; no Crocs application changes, data ingestion or model runs, and no changes to R01/R02/R03 or Section 13 results. |

## 13. Execution record

This section records implementation, execution and locked scores. The initial implementation snapshot below predates scoring; the later result subsections record completed and scored R01, R02 and R03 histories.

### Initial implementation snapshot (before scoring)

| Plan element | Implementation | State |
|---|---|---|
| Source packets (Section 4) | `real-credit-cases/R01-irobot-carlyle`, `R02-rumbleon-oaktree`: SEC-hosted documents with content hashes and SEC acceptance timestamps (`manifest.json`); verbatim clause subsets by paragraph locator; origination evidence checked to be public by origination. | Built for R01 and R02. R03 PetIQ: seven documents cached and extracted, nothing else. |
| Blind inputs and leakage audit (Section 5) | `build_blind_inputs.py` writes `blind/inputs.json` and `blind/exclusion_log.json`. A text screen nominates passages; each exclusion is a recorded, reviewed decision in `reports.json`, and an unreviewed match stops the build. Passages are kept whole or removed whole; no financial fact is edited. | R01: 9 checkpoints, 3 passages and 2 documents removed, 1 checkpoint unsuitable. R02: 7 checkpoints, 8 passages removed. A scan of both input files finds no remaining amendment or waiver wording. |
| Evaluator collection (Sections 3, 5) | `evaluator/observed_responses.json` holds the actual amendments and the notes that name them. The blind runner never opens it; an offline test checks its source for references to the evaluator or rolling folders. | Built. |
| Strict blind replay (Section 6A) | `realitycheck/benchmark_blind.py`. Original package v1.0 is the only contractual baseline at every checkpoint; no amendment is applied. Per checkpoint: report attribution, then a complete candidate package, with an origination-only control under the same model, prompt and guidelines. Failed attempts are kept and counted. `lock` hashes every output and later runs refuse to write. | Implemented; offline dry run passes; hosted runs in progress. |
| Secondary comparator (Section 3) | `direct_review` workflow: same model, settings, evidence, original package and guidelines, but no assumption framework and no carried assumption assessments. | Implemented; hosted runs in progress. |
| Origination-only control (Section 6D) | Part of both workflows. | Implemented. Repeat runs on unchanged evidence and equivalent-wording tests are **not** done. |
| Evaluation guidelines | `realitycheck/lender_guidelines.json` v0.1, labeled synthetic and not any lender's policy. | Frozen for these runs. |

### Deviations and limits to disclose with any result

1. **Both histories are development histories.** Before the blind runs, rolling-mode outputs for R01 and R02 were seen and used to change the profile prompt, the citation rules, the candidate prompt (versions 0.1 to 0.3) and a judgment-consistency rule. Under Section 4 that makes them development material. PetIQ is the only candidate no model run has touched; it would be the first unseen history, and it is not prepared.
2. **The earlier real-company runs were rolling-mode, and leaky.** They applied each actual amendment as the operative package once public, and five checkpoints supplied the amendment's own description to the model (R01 reports 8 to 10, R02 reports 3 and 7). They are kept under `realitycheck/benchmark/<case>/rolling/` as development records and must not be reported as the primary benchmark.
3. **A second leakage path was found and closed.** RumbleOn's notes on missing inputs, which are passed into every prompt, named Amendments 5 to 8 with dates. Blind runs use a separate `missing_inputs_blind` list, and RumbleOn's assumption profile was regenerated under it. iRobot's notes never mentioned an amendment, so its origination-only profile was reused.
4. **Information gaps, not reasoning failures.** RumbleOn's first public statements of covenant noncompliance (June 30, 2023 and June 30, 2024) appear only in the same passages that describe Amendments 5 and 8. They cannot be separated without editing the text, so they are withheld, and this replay cannot show advance detection of those statements. iRobot's full-year 2024 results were accepted by the SEC eight minutes before the filing disclosing Amendment No. 1.
5. **Dependence on hidden amendments.** Facts kept in later reports (RumbleOn's $100 million rights offering, asset sales and debt paydown; iRobot's return of $40 million to restricted cash) were required by amendments the model cannot see. They are labeled in the evaluator collection. Later leverage, liquidity and debt figures are not outcomes of any RealityCheck proposal.
6. **Scoped packages.** Candidates are drafted over a bounded clause subset (five clauses for R01, six for R02), not a complete agreement. Compliance cannot be calculated: compliance certificates are private, iRobot's Schedule 7.07 is absent from the filed agreement, and RumbleOn's contractual EBITDA is not its public Adjusted EBITDA.
7. **Reviewer.** No independent credit reviewer is available. Reference judgments will be author-prepared and disclosed as such; the author had already seen rolling-mode outputs for both companies.
8. **Hindsight.** Nemotron may know both companies' outcomes from pretraining. Prompts instruct it to use only supplied evidence; that does not remove the risk.

### First locked results (September 19 to 20, 2026)

Strict blind replay, one run per checkpoint, model `nvidia/nemotron-3-super-120b-a12b`, candidate prompt v0.3, guidelines RC-GUIDE v0.1. Outputs were locked by hash before the evaluator collection was opened. Both histories are development histories and the reference judgments are author-prepared, so these are feasibility observations, not accuracy results. The full record is `realitycheck/benchmark/<case>/evaluation.json`, shown at `/benchmark`.

| Measure | iRobot: RealityCheck | iRobot: direct review | RumbleOn: RealityCheck | RumbleOn: direct review |
|---|---|---|---|---|
| Warranted reviews detected | 2 of 5 (both as package review) | 1 of 5 (information request) | 4 of 4 | 3 of 4 |
| Unnecessary escalations | 1 of 2 | 0 of 2 | 1 of 1 | 0 of 1 |
| Unresolved checkpoints (not scored) | 2 | 2 | 2 | 2 |
| Runs still failed after retry | 0 of 9 | 0 of 9 | 0 of 7 | 0 of 7 |
| Findings withheld by validation | 11 | 0 | 20 | 1 |
| Model time | about 27 minutes | about 5 minutes | about 16 minutes | about 4 minutes |
| Actual responses whose clauses were touched earlier | 3 of 3, all opposite direction | 0 of 3 | 2 of 2, all opposite direction | 1 of 2 (same direction on C03, opposite on C01 and C02) |

**What the results say.**

1. **The candidate-package signal does not yet discriminate.** On RumbleOn the framework workflow escalated at all seven checkpoints, including the stabilizing quarter the reference marks as no-escalation. Detecting four of four warranted reviews means little when nothing is ever left alone.
2. **On iRobot it missed the checkpoints that matter most.** It escalated at the first checkpoint, which the reference calls unwarranted because those conditions were known at origination, then returned no action at the November 2024 draw on cash reserved for loan repayment, at the March 2025 going-concern disclosure and at May 2025. Direct review also missed most of these, producing one information request at the going-concern disclosure.
3. **Correspondence with the lenders' amendments is not foresight.** Wherever the framework touched the clauses a lender later amended, it proposed tightening while the lender loosened or waived, and its first touch was at the first checkpoint, 146 to 576 days before execution. That pattern is a standing tendency to tighten financial covenants, not anticipation of a response. The synthetic guidelines contain no logic for distress, where a lender trades covenant relief for reporting, fees, equity or repayment.
4. **The framework costs about four to five times the model time** and produces most of the findings that validation withholds.
5. **The direct-review comparator was more conservative**: no unnecessary escalations in three no-escalation checkpoints across both histories, and fewer detections.

**Deviations in these runs.** One attribution call in each history returned malformed JSON and succeeded on retry (`run_deviations.json`). RumbleOn's was the last checkpoint. iRobot's was the third, retried after later checkpoints had been drafted, so iRobot candidates from the fourth checkpoint onward did not receive that checkpoint's assumption assessments. Outputs were not regenerated to hide this.

**Evaluator correction.** The first comparison matched direction by substring against a free-text description and reported a candidate that tightened C01 as agreeing with a lender who loosened C01 but tightened C03. Direction is now compared per clause. The rule fixed beforehand, the locked outputs and the reference judgments did not change.

**Bearing on viability.** These two histories do not support a claim that the complete workflow detects reconsideration points better than a direct model review. They do show the mechanism running end to end on real filings under blind conditions, with leakage controls, locking and a comparator, and they identify what to change before the next unseen history: a materiality threshold so that any surviving change is not an escalation, guidelines that cover distress and relief as well as tightening, and a check on whether long prompts degrade the later iRobot checkpoints.

### Unseen history: PetIQ / Ares (prepared and launched September 20, 2026)

PetIQ is the one candidate no model run had touched. It was prepared after the first two histories were locked and compared, with everything frozen beforehand: model code and prompts, candidate prompt v0.3, guidelines RC-GUIDE v0.1, blind inputs, exclusion decisions, reference judgments and scoring rules. `realitycheck/benchmark/R03/freeze.json` records their hashes at 2026-09-20T02:13:24Z, before the first model call. The scoring rules are the ones fixed on the development histories, applied unchanged.

- **Packet:** 22 SEC documents; six verbatim clauses from the January 17, 2018 agreement (Sections 7.13, 6.04(a), 6.04(b), 6.04(c), 6.05, 7.02); 11 earnings-release checkpoints from March 2018 to August 2020.
- **Observed responses (evaluator only):** the July 8, 2019 amended and restated $220 million facility; the Second Amendment (convertible notes permitted, margin raised); the Third Amendment (Consolidated EBITDA add-back and permitted debt for terminating the CAP IM agreements); the Fourth Amendment (up to $14.5 million of headquarters construction debt). Checked against the filed text: the restatement reset the leverage schedule to 6.25x where the original stood at 3.50x.
- **Leakage review:** the keyword screen was written around waiver and amendment wording and nominated only two passages, both about the separate bank revolver (kept, with reasons). PetIQ's responses are a refinancing and permissions, so every passage mentioning the term loan, lender, refinancing, convertible notes, indebtedness or headquarters was also read by hand. Two passages were withheld: the statement that Ares had committed $145 million of new term loan financing (May 2019) and the statement that the acquisition was financed with it (August 2019). Both are inseparable from the surrounding sentence and are withheld whole. The acquisition itself stays visible through other passages. Debt balances from August 2019 onward reflect hidden responses and are labeled in the evaluator collection.
- **Lesson recorded:** a leakage screen tuned on two histories missed this history's response types entirely. A keyword screen can nominate passages; it cannot clear a packet.
- **Character of the history:** growth, two acquisitions and a pandemic quarter. The lender's responses followed corporate actions, not deterioration, so this history mainly tests restraint. Reference judgments: 5 unwarranted, 4 warranted, 2 unresolved.
- **Reviewer disclosure:** reference judgments are author-prepared. The author had read the amendment descriptions while building the evaluator collection, so the judgments are not blind to the lender's history; no model output for this company existed when they were written.

**Locked result (September 20, 2026).** Both workflows completed all 11 checkpoints with no failed run and no retry. 60 output files were locked by hash before the evaluator collection was opened. One run per checkpoint.

| Measure | PetIQ: RealityCheck | PetIQ: direct review |
|---|---|---|
| Warranted reviews detected | 1 of 4 (the pandemic quarter, as a package review) | 1 of 4 (the acquisition announcement, as a package review) |
| Unnecessary escalations | 1 of 5 | 2 of 5 |
| Unresolved checkpoints (not scored) | 2 | 2 |
| Failed runs | 0 of 11 | 0 of 11 |
| Findings withheld by validation | 9 | 1 |
| Model time | about 23 minutes | about 10 minutes |
| Actual responses whose clauses were touched earlier | 2 of 4 | 2 of 4 |

What the unseen history says:

1. **No advantage over direct review, and no disadvantage.** Each workflow found one of the four warranted reviews, and they found different ones. Both missed the completed acquisition (August 2019) and the second pending acquisition (March 2020). RealityCheck also missed the acquisition announcement that direct review caught.
2. **The over-escalation seen on RumbleOn did not recur.** RealityCheck signalled a package review at 2 of 11 checkpoints here, against 7 of 7 on RumbleOn, and made fewer unnecessary escalations than direct review. One unseen history cannot show whether that reflects the history or the workflow.
3. **The correspondence is not foresight.** Both workflows touched the leverage covenant in the lender's direction (loosen) before the July 2019 restatement, but at strong-growth checkpoints the reference marks as no-escalation, 237 and 328 days before execution. Neither anticipated the convertible-note or construction-debt permissions, which no earlier report mentioned.
4. **Cost.** The framework used about 2.4 times the model time and produced nine of the ten withheld findings.

Across the three histories the complete workflow has not shown better detection than a direct model review. It has shown that the blind protocol, leakage controls, locking and comparator run end to end on real filings, and it has located specific weaknesses: escalation that does not discriminate on a deteriorating borrower, missed recognition that a large acquisition changes what a package was written for, and guidelines without distress or transaction logic.

A validator change made after the PetIQ runs started (tolerating a closing period at the point a quotation is cut) did not affect them: those processes had already loaded the frozen code, and the comparison does not re-validate saved outputs.


### Presentation readiness and remaining evaluation work

The three histories now have reference judgments, locked outputs and scored comparisons. PetIQ supplies the first unseen history. The records above disclose development status, reviewer limitations, failures and retries, withheld findings, model timings and clause correspondence. The one-slide results summary is recorded in Section 14.

Still outstanding: stability checks (Section 6D), independent credit review, additional unseen histories and the full interactive two-lane presentation in Section 9. The completed technical replay does not establish analyst time savings or lending outcomes.

## 14. Benchmark performance slide (September 20, 2026)

The user requested a single horizontal PDF slide presenting the completed benchmark. The deliverable is [RealityCheck benchmark performance](output/pdf/realitycheck-benchmark-performance.pdf), a one-page 16:9 slide generated from the three saved `evaluation.json` records. This presentation work made no model calls, reran no histories, changed no reference labels and performed no rescoring.

The slide compares RealityCheck with direct Nemotron review on warranted review detection, unnecessary escalation and recorded model time. It shows each history separately, marks iRobot and RumbleOn as development histories, highlights unseen PetIQ, and labels pooled totals as descriptive and inclusive of development material. It does not present a pooled accuracy score or treat clause-family overlap as successful amendment prediction.

| Displayed measure | RealityCheck | Direct Nemotron review |
|---|---|---|
| Pooled warranted reviews detected | 7 of 13 | 5 of 13 |
| Pooled unnecessary escalations | 3 of 8 | 2 of 8 |
| Recorded successful checkpoint-call time | 66.6 minutes | 18.7 minutes |
| Unseen PetIQ: warranted reviews detected | 1 of 4 | 1 of 4 |
| Unseen PetIQ: unnecessary escalations | 1 of 5 | 2 of 5 |

**Presentation conclusion:** historical replay shows mixed performance. PetIQ has equal detection counts and one fewer unnecessary escalation under RealityCheck, at approximately 2.4 times the recorded model time. A single unseen history does not demonstrate a general performance advantage.

**Metric definitions:** warranted detection includes either a package review or an information request. RealityCheck's seven detections are all package reviews; direct review's five comprise four package reviews and one information request. Unnecessary escalation counts package review at an unwarranted checkpoint; an information request is not counted as an unnecessary escalation. Six unresolved checkpoints are excluded from scored denominators. There are 27 distinct checkpoints per workflow across three companies, not 27 independent borrowers.

**Time scope:** the displayed values sum the saved successful checkpoint attribution and candidate-generation call durations. Direct review has candidate generation only. They exclude profile construction, origination-only controls, orchestration, analyst review and failed attempts replaced by retries. These are recorded model-call durations, not end-to-end turnaround, financial cost or analyst productivity.

The slide visibly discloses AI-author-prepared reference labels with knowledge of lender history, the lack of independent credit review, bounded clause sets, one run per checkpoint and the absence of a stability study. PetIQ's unseen designation means its configuration and inputs were frozen before any model run on that history; its reference author was not blind to actual lender amendments. Crocs remains the separate presentation demo and contributes no benchmark scores.

The delivered PDF was checked against the source counts, rendered for visual inspection and verified as a single landscape page. The presentation audit also verified all 150 files in the existing output locks against their recorded SHA-256 hashes.

## 15. What the benchmark supports in the pitch (September 20, 2026)

The user asked what argument to make with the benchmark. The intended product hypothesis is: **does RealityCheck's maintained borrower-assumption framework improve the identification of when a loan package deserves review, compared with the same Nemotron model reviewing the evidence directly?** The locked results do not yet establish that improvement. The benchmark should be presented as evidence of technical feasibility and a candid comparative evaluation, not as proof of superior credit decisions or commercial viability.

The demonstrated capability is the scoped workflow running on real borrower histories: origination context and original clauses, sequential report attribution, carried assumption assessments, candidate package generation, evidence validation and comparison against withheld historical lender responses. This is broader than an ingestion test. Successful execution does not establish that its judgments or proposed amendments are correct.

Across the two development histories, RealityCheck detected 6 of 9 warranted review needs versus 4 of 9 for direct review, but made 2 unnecessary escalations in 3 unwarranted checkpoints versus none. On unseen PetIQ, each detected 1 of 4 warranted review needs and missed 3; they detected different needs. RealityCheck made 1 unnecessary escalation versus 2 in 5 unwarranted checkpoints, using about 2.4 times the recorded model-call time. The observed reduction of one unnecessary escalation is too small and narrow to claim better overall selectivity or decision quality.

Suggested presenter wording:

> We tested whether an evolving borrower-assumption framework helps identify when a loan package needs reconsideration. We replayed three real-company histories, withheld subsequent lender amendments from the model inputs, and compared RealityCheck with direct review by the same Nemotron model. The scoped review workflow runs, but its additional detections in development did not carry over to the unseen history. That case had equal detection counts and one fewer unnecessary escalation, at higher model time. The benchmark establishes a working research prototype and exposes where its review decisions need improvement; it does not yet establish superior credit judgment.

The strict replay kept the original contractual package as the baseline at every checkpoint. It did not apply RealityCheck's proposals as operative amendments or test later decisions under those adopted terms. Therefore it does not validate the entire adaptive relationship of analyst adoption, successive amendments and subsequent monitoring.

The Crocs demo can demonstrate the intended analyst experience: inspect an event, trace its connection to assumptions and clauses, compare a proposal with current terms, and retain the user's decision in the package history. These are product capabilities. Reduced analyst effort, better explanations, more appropriate amendments and improved lending outcomes remain hypotheses until measured. Neither a review signal nor clause-family correspondence establishes a confirmed covenant breach or a correctly predicted amendment.

Use the benchmark as the evidence-and-limits part of the presentation, with the demo showing the workflow's practical purpose. Do not describe the pooled detection count as general accuracy, the held-back amendments as an independently blinded expert reference, or the recorded model time as analyst time saved. Reference judgments remain AI-author-prepared with knowledge of actual lender history. Any next-version performance claim should come from a separately frozen workflow and additional unseen histories, preserving these locked results as the baseline. This clarification changed no outputs, scoring rules, reference labels or PDF figures.
