# RealityCheck

**A loan is approved on assumptions. RealityCheck keeps those assumptions attached to the loan and tells a credit analyst when new information means the package may no longer fit.**

Built at SteelHacks XIII, September 19 to 20, 2026.

> **Team:** _add each member's name and email here before submitting (required by the SteelHacks rules)._

## What it does

A private-credit analyst approves a loan with an underwriting memo, a financial model and a covenant package. Months later a report arrives: an outage, monthly accounts, an industry analysis. The question is not "what does this report say" but **"does this change what we believed when we wrote these terms?"**

RealityCheck:

1. Has NVIDIA Nemotron read the origination documents and build a company-specific register of the assumptions the loan rests on, each tied to a quoted source passage and to the covenants that protect it. Claims approved in the memo are kept apart from the model's own inferences.
2. Takes each new dated report and attributes it to those assumptions and to individual covenant duties under the package version in force on that date. Every finding must quote the report; a quotation that does not verify against the source is withheld and counted.
3. Keeps three things separate that are easy to blur: an assumption being exposed, a contractual duty being triggered or missed, and a formal default.
4. Asks **"would we write this package today?"** Nemotron drafts a candidate package twice under fixed guidelines, once from origination evidence only and once with the new reports. Only changes that appear with the new evidence count as possible drift.
5. Leaves every decision to the analyst. A detection never changes contractual terms. Adopting an amendment is a separate, explicit step, and the full history is preserved.

## Run it

Python 3 (developed on 3.14). The application, the FluxRail demo, the benchmark and the tests use the standard library only. Two optional packages are imported lazily and only by the first prototype's document upload: `pymupdf` for PDF pages and `Pillow` for image downscaling.

```powershell
cd realitycheck
python app.py 8013
```

Open **http://127.0.0.1:8013/b01**. On first start the demo database is rebuilt from `realitycheck/b01_seed.json`, so a fresh clone shows the same recorded history described below.

Recorded analyses work with no API key. For live analysis put `NVIDIA_API_KEY=...` in a `.env` file at the repository root. `.env` is git-ignored; never commit a key.

| Page | What it shows |
|---|---|
| `/h01` | The presentation scenario: Crocs with a fictional loan (see below) |
| `/b01` | FluxRail Workflow, Inc., an entirely fictional borrower |
| `/companies` | Company overview |
| `/benchmark` | Strict blind historical replay on real companies |
| `/` | The first prototype (CedarBridge packet assessment) |

Tests: `cd realitycheck` then `python -m unittest test_attribution test_b01 test_b01_model test_event_api test_drift test_benchmark_blind`. They use temporary databases and a stubbed model, and never touch the demo database or the network.

## The demo: FluxRail

FluxRail is fictional. Its agreement, memo, financial model, reports and amendments are synthetic, authored for this project. Dates in 2027 are scenario dates; analysis timestamps are real.

What you can do on `/b01`:

- **Replay the history.** *Start at origination*, then *Reveal next report*: the package moves from v1.0 to v1.2 across two adopted amendments, and a third detection is left pending on purpose.
- **Open a detection** to see the quoted evidence, the assumptions exposed, each covenant duty assessed, a suggested response, and a reviewer note wherever the model's reasoning was wrong.
- **Introduce a new report** from the report library: an industry analysis that never names FluxRail, routine monthly accounts, and a remediation report. Each can run as live Nemotron analysis or as a recorded replay, which is labeled as not fresh inference.
- **Read the candidate-package comparison** beside the authored draft amendment.

## The presentation scenario: Crocs, with a fictional loan

`/h01` is titled **"Crocs — hypothetical private-credit scenario."** Company background is sourced. Financial figures, loan terms, reports and scenario events are fictional.

A recognizable business makes the mechanism easier to follow: footwear made by third-party manufacturers overseas, shipped by ocean, sold through wholesale and direct channels. Only that background is real, taken as four verbatim passages from Crocs, Inc.'s FY2025 Form 10-K and cited where used. The borrowing entity, the lender, the $150 million facility, all nine covenants, every number, every report and every amendment were invented by `hypothetical-scenarios/build_h01.py`, which computes and checks the arithmetic. No such facility exists, nothing here describes Crocs' actual financing, and no figure from its financial statements is used. Nemotron is told to use only the scenario's defined figures and never anything it may recall about the real company.

The scenario runs from a routine month through a shipping disruption, a mitigation update and a wholesale slowdown to a recovery in direct sales that arrives with a month-end cash report below the covenant floor. It is a presentation scenario, not evidence: it is excluded from the benchmark below.

What the genuine Nemotron run did on it, reviewed and unedited: the routine month and the mitigation update stay report markers; the disruption and the wholesale slowdown each contradict one approved assumption; and in the last report the model worked out the $33.6 million covenant cash figure itself from three stated amounts, found the floor missed, and did not let better direct sales offset it. Its mistakes are shown too, as reviewer notes beside its wording (for example, a freight-cost finding that goes further than the memo's criterion supports), along with findings the validator withheld and one report that was revised and re-run after an authoring gap. The two adopted amendments are scripted scenario decisions; the third draft is left for the viewer. The candidate-package comparison found no drift from origination evidence alone and material drift with the reports, and its withheld cash-floor change pointed the opposite way (tighten) from the authored relief draft, the same pattern the benchmark shows.

## The benchmark: does it work on real loans?

The demo shows the workflow. The benchmark asks whether the mechanism holds up on real history, following `RealityCheck-Benchmark-Testing-Plan.md`.

Two real private-credit facilities, iRobot / Carlyle and RumbleOn / Oaktree, are replayed from public SEC filings. Nemotron starts from the original executed agreement and receives each later report on the date the SEC accepted it. **Every actual amendment, waiver and description of one is withheld, even once public.** Outputs are locked by hash before the real lender history is opened. A comparator runs the same model on the same evidence without RealityCheck's assumption framework.

**First results are mixed and do not show an advantage over direct review.** The framework workflow detected more warranted reviews (2 of 5 and 4 of 4, against 1 of 5 and 3 of 4) but escalated unnecessarily at 2 of 3 no-escalation checkpoints where direct review escalated at none. On RumbleOn it escalated at every checkpoint; on iRobot it returned no action at the going-concern disclosure. Wherever it touched a clause a lender later amended, it proposed tightening where the lender loosened. Both companies are development histories, reference judgments are author-prepared, and there is one run per checkpoint. The full record, including every failure and the passages withheld from the model, is on `/benchmark` and in Section 13 of the plan.

## Where Nemotron sits, and the evidence

`nvidia/nemotron-3-super-120b-a12b` with reasoning enabled, through NVIDIA NIM. It is not a chat interface. It builds the assumption register, attributes evidence to assumptions and covenant duties, drafts candidate packages, and returns structured JSON that code validates before anything is shown.

Evidence it works, and where it does not:

- **Citation checks.** Every quotation is verified against its cited source paragraph. Unverifiable findings are withheld and counted, never repaired.
- **Failures found and fixed, with the failed outputs kept.** A one-day change in receivable collection (43 days against 42) was marked as a weakened assumption until each assumption's own review criterion from the memo was supplied to the model. An industry report was first attributed to every assumption and clause. A remediation report was first read as a new detection until earlier covenant findings were supplied so a finding could be marked as not new. Empty responses were traced to the reasoning budget (finish reason `length`) and are now retried with the budget recorded.
- **Failures shown, not hidden.** Reviewer notes sit beside the original model wording wherever it misread a deadline, a threshold or a scope. The benchmark reports a result that does not favor the project.

## Data and track notes

- **FluxRail and the 30-company portfolio are synthetic.** No real account numbers, credentials or financial records.
- **The Crocs scenario uses a real company name and sourced business background with entirely synthetic financial inputs, terms and events.** The Compound rule excludes real financial records; none is used. Using a real company name is a presentation choice and is not a claim of track eligibility.
- **The benchmark uses real public SEC filings**, fetched from sec.gov with content hashes and SEC acceptance timestamps in each case's `manifest.json`. The SEC permits reuse of public filings. Reconstructed assumptions and candidate packages are hypothetical. Actual amendments are historical evidence of what a lender did, not recommendations. No endorsement by any company, lender or the SEC is implied.
- The Compound track requires synthetic or sandbox data. The FluxRail demo meets that; the real-company benchmark does not and is presented as a separate evaluation, in line with the Xtract track's public-source allowance.

## Limits

This is a local, single-user hackathon build, not a production monitoring service. Evidence for the demo is synthetic and limited. There is no demonstrated real-world accuracy, analyst time saving or loss reduction. Amendment instruments in the demo were authored, not generated. Nemotron may know the real companies' outcomes from pretraining; hiding later filings does not remove that.

## Repository map

| Path | Contents |
|---|---|
| `realitycheck/` | The application, model code, tests, FluxRail seed and report library, benchmark runner and results. See `realitycheck/README.md` for routes and data flow |
| `real-credit-cases/` | Real-company source packets: fetch, extract and build scripts, manifests, blind inputs, exclusion logs, and the evaluator collection that is never given to the model |
| `hypothetical-scenarios/` | The Crocs scenario: sourced 10-K context, the generator that authors and checks the fictional packet, and the packet itself |
| `synthetic-credit-portfolio/` | Thirty authored synthetic borrower packages |
| `RealityCheck-Current-Status.md` | Progress and handoff record, including what is not done |
| `RealityCheck-Benchmark-Testing-Plan.md` | Benchmark design, execution record and first results |
| `RealityCheck.md` | Product strategy and data rules |
| `docs/` | Scenario narrative, verification record, case research |

## AI tools used

Required disclosure: this project was built with **Claude Code (Claude Fable 5.1)** for scaffolding, data authoring, model-prompt iteration, debugging, testing and documentation. **NVIDIA Nemotron** (`nemotron-3-super-120b-a12b`, with earlier trials of Nano Omni 30B and Ultra 550B) is the model inside the product.
