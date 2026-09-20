# B01 package-history demonstration

This is an additional synthetic history for **FluxRail Workflow, Inc. (B01)**. It uses the borrower's actual authored package in `synthetic-credit-portfolio/model_inputs/B01-fluxrail-workflow-inc` and follows its benign June 16, 2027 operating evidence. All dates and later evidence are fictional. The baseline agreement is version 1.0, effective December 31, 2026, with fixed interest of **9.25%** and maximum quarterly net leverage of **4.05x**. No optional financial covenant family is elected.

The machine-readable fixtures are in [b01_scenarios.json](../realitycheck/b01_scenarios.json). They contain evidence, two simulated executed amendments, and a third unsigned discussion draft. No model result or expected-answer key is embedded in the evidence text. The observations below are scenario-author expectations for testing; they must not be passed to Nemotron as evidence or represented as Nemotron's findings. The saved actual model responses establish what Nemotron detected.

## Timeline

| Stage | Event and analyst availability | Decision and effective date | Operative change |
| --- | --- | --- | --- |
| Original | Package known December 31, 2026 | Effective December 31, 2026 | Version 1.0: S1 has a 30-day remediation window; S2 covers incidents longer than 4 hours affecting at least 10% of prior-year revenue. |
| Detection 1 | Deadline passes July 12, 2027; evidence available July 13 | Fictional execution July 19; effective July 20 | Version 1.1 replaces S1 prospectively. Future interface changes receive 15 days, specified independent testing, and exception reporting. |
| Detection 2 | Six-hour outage August 9; evidence available August 10 | Fictional execution August 20; effective August 23 | Version 1.2 replaces S2 prospectively. New incident thresholds become longer than 2 hours and at least 5% of revenue, with recurrence follow-up. |
| Open detection | Three-hour outage September 7; reconciled evidence available September 10 | **No decision or effective date** | Version 1.2 remains operative. A proposed version 1.3 adds reporting controls and remains unsigned. |

The first two detections connect to actual simulated amendments. Alternatives are dimmed. The last detection stays red because a user decision remains open. A detection date, an evidence-availability date, an amendment decision date, and its effective date are separate fields; the display must not collapse them into one implied date.

## Detection 1: compatibility bridge withdrawn

The vendor published its breaking interface on June 10. The platform serves customers representing 18% of 2026 revenue. The bridge previously described as passing staging tests failed a July 5 production security test and was quarantined. As of July 12 at 5:30 p.m. New York time, there was neither a compatible production connector nor a documented secure workaround. The old endpoint still supported service, so there was no qualifying production outage or customer termination notice in the record.

**Expected analytical distinction:** A1's renewal-reliability premise is exposed, and S1's remediation deadline has passed. Thirty calendar days after June 10 is July 10, a Saturday; the agreement's administrative-performance deadline rolls to Monday, July 12. S1 affirmative noncompliance is supported, but an Event of Default cannot be inferred without its separate category-A lender-notice and cure analysis. C08 notice timing is a separate obligation; the CFO first learns of the consolidated failure July 13, so its deadline has not yet passed at this review. No current C01 result can be calculated from this operating evidence.

**Subsequent amendment:** A compatible connector is deployed July 19, with completed production-equivalent security and compatibility testing. The simulated July 19 instrument confirms conditions and narrowly waives the historical S1 failure through restoration; it does not rewrite the missed deadline. Version 1.1 is effective July 20. Only interface changes published on or after that date get the new 15-day window. This later deployment and instrument must not be included in Nemotron's July 13 input.

## Detection 2: a qualifying outage with timely reporting

A queue-lock defect prevents regulated approvals for six hours on August 9 and affects customers representing 12% of prior-year revenue. The technology officer learns the relevant scope at 9:15 a.m. The lender receives the initial notice August 10 at 11 a.m. Service is restored, reconciliation finds no data-integrity loss, and no customer termination notice is received. The connectors remain compatible; this is a runtime reliability issue.

**Expected analytical distinction:** A1 is exposed and S2's incident-reporting duty is triggered. The initial notice is timely. At the August 10 review, the root-cause report is not yet due: restoration August 9 plus 15 calendar days gives August 24. A qualifying outage is not, by itself, a breach of this reporting covenant. The model should not invent S1 incompatibility, customer termination, or a financial-ratio breach.

**Subsequent amendment:** The simulated instrument records delivery of the complete root-cause report August 12. The parties sign August 20 and make version 1.2 effective August 23. S2 now captures new incidents longer than two hours affecting at least 5% of prior-year revenue. It also requires reporting of an identified material unresolved recurrence risk and weekly follow-up. The amendment applies prospectively and grants no historical waiver. The September incident deliberately tests these revised thresholds.

## Detection 3: a smaller incident crosses the new threshold

On September 7, a three-hour regulated-workflow outage affects customers representing 7% of prior-year revenue. A responsible technology officer acknowledges the scope at 9:20 a.m. The full lender-portal and notice-dispatch reconciliation through September 10 contains no notice for this incident. Internal routing still uses the superseded four-hour/10% settings. The system restores service at noon with no identified lost or corrupted records. Engineering is investigating whether the cause repeats the August defect, but causal identity is not established.

**Expected analytical distinction:** Under version 1.2, the incident meets S2's amended duration and affected-revenue thresholds. Its two-Business-Day notice deadline is September 9 at 5 p.m. The complete reconciled absence through September 10 supports missed reporting, while the corresponding original S2 threshold would not have captured this three-hour/7% incident. That is the key amended-context test. No category-R Event of Default is yet established because no written lender cure notice has been delivered. The September root-cause report is not due until September 22. A possible recurring defect does not establish the separately defined material unresolved recurrence-risk trigger. No leverage failure, customer termination, or configuration-custody transfer is established.

**Open user decision:** The unsigned version 1.3 discussion draft retains the two-hour/5% thresholds and proposes a version-controlled threshold register, independent routing tests, named reporting owners, manual fallback, and verified lender receipts. These address the observed process failure. The user may request evidence, keep version 1.2 and correct the process, or negotiate an amendment. No path is preselected; the proposal waives nothing and carries no effective date. Accepting an attribution finding is not execution of an amendment.

## Model-run and history rules

1. Analyze D01 against version 1.0 and information available July 13. Only afterward introduce the July 19 instrument and activate version 1.1 on July 20.
2. Analyze D02 against version 1.1 and information available August 10. Only afterward introduce the August 20 instrument and activate version 1.2 on August 23.
3. Analyze D03 against version 1.2 and information available September 10. Keep the proposed version 1.3 outside the operative covenant context.
4. Preserve evidence document IDs, locators and quotes; separate source facts, model interpretations, user decisions and executed synthetic instruments.
5. Save actual Nemotron engine/model identifiers, prompts or context versions, responses, timestamps and any unavailable/error status. A fixture's authored expectation never substitutes for a successful model run.
6. Keep fixed interest at 9.25% and C01 at 4.05x throughout. These divergences change operational protections. They do not fabricate a repricing or later financial statement.

The D03 source imitates an automatic company-database synchronization. That fixture alone does not prove an external ingestion connector or recurring monitor exists; the application must label the actual ingestion mechanism accurately.
