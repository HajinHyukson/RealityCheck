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

Python 3 (developed on 3.14). The application, the benchmark and the tests use the standard library only. Uploading PDFs needs `pymupdf` to read page text; `Pillow` is optional and only downscales page images before OCR.

```powershell
pip install pymupdf
cd realitycheck
python app.py 8013
```

Open **http://127.0.0.1:8013/**. Put `NVIDIA_API_KEY=...` in a `.env` file at the repository root: onboarding an agreement and analysing a report are live Nemotron calls, so the demo needs a key. `.env` is git-ignored; never commit a key. The benchmark page shows saved results and needs no key.

| Page | What it shows |
|---|---|
| `/` or `/companies` | Credit agreements: the upload form and one card per company workspace |
| `/u…` | A company workspace (the id is assigned when the agreement is uploaded) |
| `/benchmark` | Strict blind historical replay on real companies |
| `/legacy` | The first prototype (CedarBridge packet assessment) |

Tests: `cd realitycheck` then `python -m unittest test_attribution test_b01 test_b01_model test_event_api test_drift test_benchmark_blind test_uploads`. They use temporary databases and a stubbed model, and never call the network. One `test_b01` check lists the companies on disk, so it passes on a fresh clone and fails once uploaded workspaces exist locally.

## The demo: upload a credit agreement

There is no pre-seeded company. A fresh clone opens on an empty **Credit agreements** page, and every workspace in the demo is created by uploading documents through the same form a user would use. `realitycheck/uploads/` holds that runtime state and is git-ignored, so nothing the model produced ships with the repository.

**1. Onboard the agreement.** On `/`, enter a company name and an agreement date, add up to 10 files (PDF, image, TXT or Markdown; 12 MB each, 20 MB total) and label each one *Credit agreement*, *Memo* or *10-K*. At least one must be the agreement; memos and 10-Ks are optional origination evidence. Then, in the background:

- Text is read from each PDF's embedded text layer. Scanned pages and images go to NVIDIA Nemotron Parse 2.0 for OCR.
- Nemotron extracts up to 24 material clauses from the agreement. It does not return clause text. It points at each clause with a source locator and two short verbatim anchors, and the host copies the text between them from the source, so every stored clause is verbatim by construction. A clause whose anchors cannot be found in the source fails verification and the company is not activated.
- Nemotron then builds the assumption register from all the origination documents, with the same quotation checks as everywhere else. The uploaded agreement becomes package v1.0 and the workspace opens.

**2. Add reports one at a time.** In the workspace, upload a later report with the date it became available. Nemotron attributes it to the assumptions and to each covenant duty under the package version in force on that date. A report that arrives before an amendment is judged under the terms that applied then.

**3. Review.** Open a detection to see the quoted evidence, the assumptions exposed and each covenant duty assessed. Run the **"would we write this package today?"** comparison on the reports received so far. Dismiss a detection, or write an amendment by editing clause text in place: the edit is checked against the current wording, cannot be backdated before its evidence, and creates the next package version (v1.1, v1.2, ...) while the earlier versions and the original detection stay in the history.

### The documents behind the demo

`Sample Companies/` holds three authored document sets, **Duolingo**, **Planet Fitness** and **YETI**, numbered in upload order. Each folder's `00 Start Here.md` is the presenter guide and is not evidence to upload.

| Documents | Role | Used for |
|---|---|---|
| 01 | Company background digest, plus the company's public FY2025 annual report (beside it for Duolingo, in `sources/` for the other two) | Onboarding, as *Memo* and *10-K* |
| 02 | Original credit agreement | Onboarding, as *Credit agreement* |
| 03 to 05 | Underwriting memo, opening financial and operating schedules, lender review guidelines | Onboarding, as *Memo* |
| 06 to 12 | Dated reports: a routine month, an industry report that never names the borrower, a company impact and cash report, a mitigation update, then a counterparty notice, a revised cash forecast and actual cash results | Uploaded one at a time |
| 13 | A severe event: a shutdown, recall or closure with a missed or upcoming payment | Uploaded last |

Only the company name and its public business background are real. The borrowing entity, the lender, the credit agreement, every financial figure and every later report are invented, and each set states that no relationship with the real company is asserted. The reports name no covenant, request no amendment and prescribe no model answer.

### What is loaded for the presentation

The presentation machine holds four workspaces, all made this way from the Duolingo set and all analysed live by `nvidia/nemotron-3-super-120b-a12b`. Documents 01 to 05, including the full FY2025 Form 10-K, were onboarded once: 11 clauses extracted and verified, 7 assumptions in the register. That prepared workspace was then duplicated with **Copy credit agreement**, which exists so one onboarding run can be rehearsed more than once, and each copy was taken to a different point:

| Workspace | State | Shows |
|---|---|---|
| Duolingo Demo 1 | v1.0, no reports yet | The origination view, and a first report upload live |
| Duolingo Demo 2 | v1.0, report 06 analysed, package comparison run | A routine month that stays a report marker, not a detection; the comparison found no material drift |
| Duolingo Demo 3 | v1.0, reports 06 and 13 analysed and awaiting review | A severe detection before any analyst decision. The package comparison run here still returned no material drift, which is shown as it came back |
| Duolingo Demo 4 | v1.2, five reports analysed, two analyst-written amendments adopted | The full history: detections, amendments and version changes. A sixth report whose analysis failed is kept and shown as failed |

The onboarding run took a little over two minutes of hosted model calls, which is why prepared copies stand behind the live upload on stage. No Planet Fitness or YETI workspace is loaded at present; those sets go through the same form.

## The benchmark: does it work on real loans?

The demo shows the workflow. The benchmark asks whether the mechanism holds up on real history, following `RealityCheck-Benchmark-Testing-Plan.md`.

Two real private-credit facilities, iRobot / Carlyle and RumbleOn / Oaktree, are replayed from public SEC filings. Nemotron starts from the original executed agreement and receives each later report on the date the SEC accepted it. **Every actual amendment, waiver and description of one is withheld, even once public.** Outputs are locked by hash before the real lender history is opened. A comparator runs the same model on the same evidence without RealityCheck's assumption framework.

**First results are mixed and do not show an advantage over direct review.** The framework workflow detected more warranted reviews (2 of 5 and 4 of 4, against 1 of 5 and 3 of 4) but escalated unnecessarily at 2 of 3 no-escalation checkpoints where direct review escalated at none. On RumbleOn it escalated at every checkpoint; on iRobot it returned no action at the going-concern disclosure. Wherever it touched a clause a lender later amended, it proposed tightening where the lender loosened. Both companies are development histories, reference judgments are author-prepared, and there is one run per checkpoint. The full record, including every failure and the passages withheld from the model, is on `/benchmark` and in Section 13 of the plan.

## Where Nemotron sits, and the evidence

`nvidia/nemotron-3-super-120b-a12b` through NVIDIA NIM, with reasoning enabled for analysis and turned off for clause pointing, which needs none. Nemotron Parse 2.0 reads scanned pages. It is not a chat interface. It extracts the agreement's clauses, builds the assumption register, attributes evidence to assumptions and covenant duties, drafts candidate packages, and returns structured JSON that code validates before anything is shown.

Evidence it works, and where it does not:

- **Citation checks.** Every quotation is verified against its cited source paragraph. Unverifiable findings are withheld and counted, never repaired.
- **Failures found and fixed during development, with the failed outputs kept.** A one-day change in receivable collection (43 days against 42) was marked as a weakened assumption until each assumption's own review criterion from the memo was supplied to the model. An industry report was first attributed to every assumption and clause. A remediation report was first read as a new detection until earlier covenant findings were supplied so a finding could be marked as not new. Empty responses were traced to the reasoning budget (finish reason `length`) and are now retried with the budget recorded.
- **Upload failures found on the Duolingo agreement and fixed in code, not in the prompt.** The model mistyped the 32-character document id in 10 of 11 clauses, so a clause is now located by its verbatim start anchor, which must occur exactly once. It stopped a sentence or two early in 7 of 11 clauses, so a clause runs to the end of its paragraph. One clause was given another's ending and swallowed two neighbours, so a clause stops where the next verified clause begins. Pointing with reasoning off took 13 seconds against 55 to 257 with it on.
- **Failures shown, not hidden.** A report whose analysis fails stays in the history marked as failed. A package comparison that returned no material drift after a severe event is shown as it came back. The benchmark reports a result that does not favor the project.

## Data and track notes

- **The 30-company portfolio is synthetic.** No real account numbers, credentials or financial records.
- **The demo document sets use real company names (Duolingo, Planet Fitness, YETI) and public business background, including each company's public FY2025 annual report, with entirely synthetic loan terms, financial inputs, reports and events.** The annual report is a real public filing and contains the company's real financial statements; it is uploaded as company background only, and the sets' own rule is that real company financials are never substituted into the fictional loan. Using a real company name is a presentation choice and is not a claim of track eligibility.
- **The benchmark uses real public SEC filings**, fetched from sec.gov with content hashes and SEC acceptance timestamps in each case's `manifest.json`. The SEC permits reuse of public filings. Reconstructed assumptions and candidate packages are hypothetical. Actual amendments are historical evidence of what a lender did, not recommendations. No endorsement by any company, lender or the SEC is implied.
- The Compound track requires synthetic or sandbox data. The demo's loans, figures and reports are synthetic, and a run that leaves out the annual report uses authored documents only; the real-company benchmark is not synthetic and is presented as a separate evaluation, in line with the Xtract track's public-source allowance.

## Limits

This is a local, single-user hackathon build, not a production monitoring service. Evidence for the demo is synthetic and limited. There is no demonstrated real-world accuracy, analyst time saving or loss reduction. Amendments in the demo are written by the analyst in the workspace, not generated. The sample reports were authored for the demo, and the prepared workspaces hold one model run per report. Nemotron may know the real companies' outcomes from pretraining; hiding later filings does not remove that.

## Repository map

| Path | Contents |
|---|---|
| `realitycheck/` | The application, model code, upload pipeline, tests, benchmark runner and results. `realitycheck/README.md` has routes and data flow, and still describes two earlier curated scenarios that the app no longer serves |
| `Sample Companies/` | The Duolingo, Planet Fitness and YETI document sets uploaded in the demo, each with a presenter guide, editable Markdown sources and public source links |
| `real-credit-cases/` | Real-company source packets: fetch, extract and build scripts, manifests, blind inputs, exclusion logs, and the evaluator collection that is never given to the model |
| `hypothetical-scenarios/` | Generator and packet for an earlier curated scenario, kept for the record and not served by the app |
| `synthetic-credit-portfolio/` | Thirty authored synthetic borrower packages |
| `RealityCheck-Current-Status.md` | Progress and handoff record, including what is not done |
| `RealityCheck-Benchmark-Testing-Plan.md` | Benchmark design, execution record and first results |
| `RealityCheck.md` | Product strategy and data rules |
| `docs/` | Scenario narrative, verification record, case research |

## AI tools used

Required disclosure: this project was built with **Claude Code (Claude Fable 5.1)** for scaffolding, data authoring, model-prompt iteration, debugging, testing and documentation. **NVIDIA Nemotron** (`nemotron-3-super-120b-a12b`, with earlier trials of Nano Omni 30B and Ultra 550B) is the model inside the product.
