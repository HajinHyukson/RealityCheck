# RealityCheck: Synthetic Covenant Framework

Research date: September 19, 2026. Version 1.0.

**Confirmed scope:** a profitable U.S. software or business-services borrower. Analyst review is the primary product objective; earlier detection remains a hypothesis to test.

**Purpose:** create internally consistent synthetic credit agreements, underwriting memos, and reporting packets that resemble the structure of negotiated private-credit deals. This is a dataset-authoring framework, not an executable loan agreement.

The appropriate claim today is **“market-informed synthetic covenants grounded in filed direct-lender agreements and OCC credit-risk principles.”** “Market standard” is not a single leverage number or mandatory list of covenants. Claiming market comparability requires review of the chosen segment, definitions, economics, and exceptions by a practitioner. No such review is represented as completed here.

## 1. What the OCC guidance contributes

The Comptroller's Handbook supports a disciplined approach to credit assessment. It is written for bank supervision; it does not prescribe the terms every private-credit fund must negotiate. Its discussion of sound practices must also be distinguished from underlying legal requirements. [OCC handbook foreword, printed p. 1](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/foreword/pub-ch-foreword.pdf#page=3)

Use these research findings as design inputs. The proposed applications are RealityCheck design choices.

| Source and locator | Research finding | Proposed application |
| --- | --- | --- |
| [Commercial Loans](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/commercial-loans/pub-ch-commercial-loans.pdf), printed pp. 14–15, 20 | Repayment analysis considers operating cash flow, debt service, capital spending, and business needs. Controls include reporting, certifications, and collateral safeguards. | Generate a cash-flow bridge and evidence obligations alongside financial tests. |
| [Leveraged Lending](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/leveraged-lending/pub-ch-leveraged-lending.pdf), printed pp. 15, 59–60, 62, 64 | EBITDA omits important cash needs. Headroom compares projections and thresholds at corresponding dates. Maintenance and incurrence tests operate differently. | Calculate downside capacity, preserve testing dates, and distinguish recurring tests from transaction permissions. |
| [Rating Credit Risk](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/rating-credit-risk/pub-ch-rating-credit-risk.pdf), printed pp. 16–17, 62–63 | Leverage assessment depends on context and definitions. Financial and nonfinancial weaknesses inform credit assessment. | Keep covenant results, economic interpretation, and thesis assessment separate. |
| [Lending and Loan Portfolio Risk Management](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/lending-loan-portfolio-risk-management/pub-ch-lending-loan-portfolio.pdf), printed pp. 37, 42–44, 110 | Monitoring includes statements, tests, and reviews. Waived breaches remain financial exceptions for tracking. Covenant protection should permit intervention before substantial deterioration. | Preserve exception history and distinguish reporting triggers, contractual failures, and analyst concerns. |

**Source status matters.** The OCC issued the new portfolio handbook on June 25, 2026, replacing the older Loan Portfolio Management booklet. The catalog says June 2026; the linked PDF cover says July 2026. Record it as Version 1.0 (2026), issued June 25, with that metadata discrepancy. [OCC Bulletin 2026-29](https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-29.html)

The OCC and FDIC withdrew the 2013 leveraged-lending guidance and 2014 FAQs on December 5, 2025. Do not turn their old numerical benchmarks into current OCC requirements. This finding concerns those two agencies. [Withdrawal statement](https://www.occ.treas.gov/news-issuances/news-releases/2025/nr-ia-2025-119.html)

Commercial Loans has a 1990 narrative and 1998 procedures; Leveraged Lending is dated 2008; Rating Credit Risk is dated 2001. They remain listed, with later updates noted in the PDFs. Their age and embedded historical references should remain visible in the source register. [Current handbook collection](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/index-comptrollers-handbook.html)

## 2. Use actual agreements to establish contractual structure

These are dated reference documents, not representations of the borrowers' current obligations. Publicly filed examples are a selected sample; they do not establish market-wide prevalence or median terms. Industry differences also limit numerical comparability.

| Reference | Useful observed structure | Appropriate use |
| --- | --- | --- |
| **M1: Artivion / Ares, January 18, 2024.** [Agreement](https://www.sec.gov/Archives/edgar/data/784199/000095015724000061/ex10-1.htm), §6.7 and definitions | Quarterly total-net-leverage limits step from 6.25x to 5.75x. Certain savings-related adjustments have a defined cap; the cap does not cover every EBITDA adjustment. | A recent cash-flow covenant, definition, and basket reference. Its medical-device business is not a software peer for threshold calibration. |
| **M2: Xponential Fitness / HPS and Fortress, December 8, 2025.** [Agreement](https://www.sec.gov/Archives/edgar/data/1802156/000119312525311452/d32941dex101.htm), §§7.12, 8.04 | Leverage limits vary by year. Equity cures have receipt deadlines, frequency limits, permitted uses, and restrictions on double counting. | Model amendments and cure mechanics. Fitness-sector leverage levels are not software-market averages. |
| **M3: Evolent Health / Ares, December 30, 2019.** [Agreement](https://www.sec.gov/Archives/edgar/data/1628908/000162890819000084/exhibit101passportcredit.htm), §§8.01, 9.12–9.13 | Reporting obligations, business-scope restrictions, and financial tests coexist. | Build semantic cases involving permitted business activity and evidence delivery. |
| **M4: NN / Oaktree, March 28, 2025 amendment.** [Amendment](https://www.sec.gov/Archives/edgar/data/918541/000091854125000041/exhibit101termloansixthame.htm), §7.14(b); [2021 original](https://www.sec.gov/Archives/edgar/data/918541/000119312521089609/d162543dex103.htm) | Low liquidity or elevated leverage triggers a 13-week cash-flow projection. The reporting trigger can activate while the liquidity minimum still passes. | Separate an additional reporting obligation from a failed financial minimum. |
| **M5: Instructure / Golub and Owl Rock, March 24, 2020.** [Agreement](https://www.sec.gov/Archives/edgar/data/1841804/000119312521201923/d47346dex101.htm), §10.13 | Recurring-revenue leverage and liquidity tests cease following a defined election; a different leverage test then applies. | A separate software variation for testing applicability changes. Do not import its pre-conversion revenue test into the profitable-borrower baseline. |

For each reusable clause, retain source URL, document date, clause and definition locators, borrower/lender, facility type, known amendments, extraction date, and limitations. Label its use as **observed structure**, **adapted structure**, or **entirely synthetic choice**. Retain a brief adaptation note; do not imply that a synthesized clause is a quotation.

## 3. Generation process

### Step 1: Specify the credit before writing its covenants

Choose the borrower, jurisdiction, business model, sponsor, purpose, facility size, maturity, amortization, security, guarantors, and repayment sources. Separate an operating-company loan from a fund's own borrowing facility.

For this dataset, start with a senior secured cash-flow term loan to a profitable software/services company. Add a revolver only when the case needs it. Asset-based, real-estate, recurring-revenue, distressed, and covenant-lite structures require separate templates.

### Step 2: Build a financially coherent borrower

Prepare historical and projected statements, debt and cash schedules, and an EBITDA reconciliation before selecting thresholds. Tie the balance sheet and cash movements together. Define debt service, taxes, maintenance investment, capitalized development costs, and working-capital needs.

Prepare a base case, a moderate downside, and a severe downside. Include refinancing assumptions for a balloon maturity; do not infer that a leverage covenant proves the principal can be repaid at maturity.

### Step 3: Write the underwriting thesis separately

Record three to five assumptions, their supporting evidence, materiality criteria, and what would prompt review. Preserve their original wording and approval date.

For each assumption, mark whether it is protected by a covenant, observed through reporting, or left primarily to analyst judgment. A customer-retention assumption does not become legally binding merely because it appears in the memo.

### Step 4: Select a coherent covenant package

Start with one primary leverage maintenance test, reporting/certification duties, and controls on debt, liens, distributions, investments, asset transfers, and business scope. Specify affirmative duties concerning existence, insurance, taxes, and collateral where relevant.

Select optional liquidity, coverage, capex, or additional reporting provisions only with an explicit borrower-risk rationale. More restrictions do not automatically make a dataset more realistic. Record omitted families and why they are unnecessary for the chosen case.

### Step 5: Define terms and exceptions before calibrating numbers

Complete the definitions in Section 4. Specify baskets, consent rights, measurement dates, and any activation conditions. The same nominal leverage limit can represent materially different protection under different definitions.

For a fixed-dollar basket, record whether it is an annual flow or an outstanding stock. For a grower basket, specify whether the permitted amount is the greater or lesser of the fixed amount and the formula. Define carryforward, replenishment, and reclassification explicitly; none is presumed.

### Step 6: Calibrate protection against the borrower model

Select parameters from the base case and stated tolerance for deterioration. Compare the resulting structure with suitable agreements, preserving differences in borrower risk, size, industry, date, and definitions. Do not sample each threshold independently from a broad range.

For a maximum leverage covenant, if net debt N stays constant, base EBITDA is E, and the desired EBITDA decline capacity is h, the implied limit is **L = N / [E × (1 − h)]**. This is an arithmetic design tool, not an OCC formula or an estimate of market practice.

For each proposed threshold, record the base value, boundary value, downside capacity, reason for selection, and sensitivity to changes in debt, cash, and adjustments. Compare like-for-like periods. Test the complete cash flow as well as the ratio.

### Step 7: Draft the clause and its interpretation record together

Produce plain-language contractual prose and a structured record using Section 5. They must describe the same obligation. Use a complete set of definitions and cross-references within the synthetic packet.

Draft defaults, cure rights, notices, waivers, amendments, and remedy conditions separately. A failed calculation does not authorize RealityCheck to take enforcement action.

### Step 8: Generate dated evidence and hidden answers

Freeze the agreement and thesis first. Generate borrower events and documents afterward. Provide the model only information available by the review date. Keep expected calculations, interpretations, and later outcomes in a separate evaluator file.

Use the case matrix in Section 9. Have a reviewer challenge whether the evidence actually supports each answer. Where the facts allow multiple reasonable interpretations, label the ambiguity instead of forcing a violation.

## 4. Required definition checklist

| Definition | Decisions the author must make |
| --- | --- |
| Borrower group | Consolidated entities, guarantors, restricted/unrestricted subsidiaries, excluded entities, and reporting perimeter. |
| Debt | Treatment of funded loans, revolver draws, finance leases, capitalized PIK, guarantees, earnouts, drawn and undrawn letters of credit, trade payables, and operating leases. |
| Eligible cash | Ownership, accessibility, restrictions, liens, geography, currency conversion, and netting cap. A balance-sheet cash total is not sufficient evidence. |
| Covenant EBITDA | Starting accounting measure; interest, tax, depreciation/amortization treatment; permitted adjustments; excluded gains; caps; documentation; pro forma changes; and anti-double-counting rules. |
| Software costs | Treatment of capitalized development, amortization, stock compensation, restructuring, and claimed implementation savings. Ordinary recurring costs cannot disappear through an unspecified add-back. |
| Test period | Quarter-end debt versus trailing-four-quarter earnings; first test; thresholds by date; permitted annualization; treatment of acquisitions/disposals. |
| Liquidity or coverage | Exact cash/access conditions or coverage numerator and denominator. Label cash interest versus total interest and scheduled versus total principal. |
| Materiality | Fixed, relative, or judgment-based criteria; relevant financial period; and which obligation uses them. |
| Business Day | Named holiday calendar, time zone, deadline rollover, and delivery method. Preserve calendar days where the clause uses them. |
| Pro forma calculation | Transactions included, effective date, historical target earnings, financing costs, cash usage, and limits on forecasts or synergies. |

**Important:** Contract-adjusted EBITDA is not interchangeable with reported EBITDA, cash generation, or the underwriting team's normalized EBITDA. Preserve each separately with its bridge.

## 5. Minimum record for every synthetic covenant

| Field group | Required contents |
| --- | --- |
| Identity and provenance | Covenant ID, borrower, facility, source classification and locators, adaptation note, author, synthetic designation. |
| Governing version | Agreement ID, execution date, effective date, known-at date, amendment ID, superseded version, affected periods. |
| Obligation | Affirmative/negative/financial family; maintenance/incurrence/reporting mechanism; obligor; beneficiary; complete prose. |
| Applicability | Start/end date, transaction or utilization trigger, exclusions, dormant conditions, facilities affected. |
| Calculation | Defined inputs, formulas, units, rounding/display rules, thresholds by date, comparison operator, required evidence. |
| Permissions | Baskets and usage, exceptions, consent authority, prerequisites, carryforward and aggregation rules. |
| Timing | Measurement date, due date, actual receipt, review date, knowledge/notice triggers, calendar. |
| Resolution | Default cross-reference, notice/grace provisions, cure scope and deadline, limits on cure use, waiver conditions, remedy prerequisites. |
| Thesis relationship | Assumption IDs, connection to repayment, limits of contractual protection, analyst review criteria. |
| Ground truth | Expected applicability, input values, arithmetic, result, unresolved facts, source spans, interpretation rationale, reviewer status. Store separately from model inputs. |

Use separate outputs for **applicability**, **evidence sufficiency**, **computed/interpretive result**, and **contractual resolution**. For example: applicable / sufficient / failed test / subsequently waived. An inactive covenant is not a passed test. A missing certificate is not proof of a ratio failure, although late delivery can itself fail a reporting obligation.

## 6. Worked synthetic package: CedarBridge Workflow, Inc.

All names, figures, deadlines, thresholds, and baskets in this section are invented design choices. They illustrate a relatively protective, simplified package. They are not claimed to be typical pricing or market medians, and they do not reproduce any one source agreement.

### Borrower and capital structure

U.S. software and related implementation-services company, consolidated with two wholly owned domestic operating subsidiaries. All three are loan parties. There are no unrestricted subsidiaries in this baseline.

The fictional loan closes on December 31, 2026; fiscal years end December 31. Opening earnings cover the four quarters ending on the closing date, and opening debt/cash balances are measured immediately after closing. Future dates in this example describe a simulation, not observed events.

| Item | Synthetic opening position |
| --- | --- |
| Annual revenue | $80m |
| Reported EBITDA, before contractual adjustment | $19m |
| Documented eligible restructuring cost | $1m |
| Covenant EBITDA | $20m |
| Senior secured funded term debt | $90m |
| Unrestricted eligible cash | $10m |
| Net debt for maintenance testing | $80m |
| Opening total net leverage | 4.00x |
| Loan term and amortization | Five years; $1m annual scheduled principal reduction, with remaining principal due at maturity. |
| Security and guarantees | First-priority security over material assets of the loan parties, subject to specified permitted liens; operating subsidiaries guarantee the borrower. |

Loan proceeds refinance existing funded debt. The ownership and security schedules must be supplied with each generated packet. This baseline has no revolver, finance lease, PIK, guarantee of third-party debt, letter of credit, or earnout outstanding.

Illustrative annual cash bridge: reported EBITDA $19m less cash taxes $2m, maintenance investment $3m, and working-capital investment $1m leaves $13m before cash debt service. Forecast cash interest of $9m and scheduled principal of $1m leave $3m. The $1m restructuring cost is already in reported EBITDA and is not deducted again. This cash bridge is credit analysis, not an additional coverage covenant. A complete scenario must supply the underlying statements and quarterly cash reconciliation.

### Definitions for this package

**Debt:** outstanding funded borrowings, finance-lease principal, capitalized PIK, unreimbursed letter-of-credit drawings, and due amounts under funded guarantees. Exclude ordinary non-interest-bearing trade payables and operating-lease liabilities. Other financing categories are prohibited unless an amendment defines their treatment.

**Eligible Cash:** unrestricted cash owned by a loan party, available for debt service, and subject only to the agent's permitted security interest. Restricted deposits and third-party cash are excluded. Cash netting for leverage is capped at $10m and cannot exceed Debt. For transaction-permission tests, exclude proceeds of the debt being incurred from cash netting.

**Covenant EBITDA:** consolidated trailing-four-quarter reported EBITDA, reconciled from GAAP net income by adding interest expense, income-tax expense, depreciation, and amortization; then add documented cash restructuring costs that were deducted in that starting measure, up to 10% of positive reported EBITDA. Subtract included non-operating disposal gains. Permit no projected synergies or other adjustments in the baseline. The $1m opening adjustment is below the $1.9m cap. Negative or zero EBITDA is handled explicitly as a failed leverage test while positive net debt remains, rather than dividing by zero or passing a negative ratio.

Development costs and stock compensation follow the stated accounting policy without additional contractual adjustments. Every packet must disclose that policy; policy changes require a reconciliation to the agreed basis. Acquisition pro forma EBITDA uses verified historical target earnings under the same definitions, excluding speculative savings.

### Core covenants and optional rider

| ID | Synthetic clause design | Boundaries and interpretation |
| --- | --- | --- |
| C01: Leverage | At each calendar quarter-end, beginning March 31, 2027, Total Net Leverage must be no more than 5.00x. It equals quarter-end Debt less permitted cash netting, divided by Covenant EBITDA for the four quarters then ended. | Applies every quarter, independent of borrowing activity. Compare unrounded values; equality passes. No automatic equity cure is granted in this baseline. |
| C02: Reporting | Deliver quarterly management financial statements and an officer-certified covenant calculation within 45 calendar days after every quarter-end; audited annual statements within 90 calendar days after year-end; and an annual budget within 30 calendar days after the fiscal year begins. | The fourth-quarter management packet remains due at 45 days; the audit does not replace it. Include debt/cash and EBITDA bridges. These deadlines are synthetic. |
| C03: Debt and liens | Additional debt and liens are restricted except scheduled existing obligations, ordinary-course statutory liens that are not overdue or are contested with adequate reserves, and permitted finance leases up to $2m principal outstanding in aggregate. | Lease security is limited to financed assets. New leases require no continuing contractual default and pro forma leverage at or below 4.50x. Include lease principal in Debt. No general unlimited debt basket exists. |
| C04: Distributions | Cash dividends are limited to $1m in aggregate per fiscal year, with no carryforward, and require no continuing default, pro forma leverage at or below 4.25x, and at least $8m Eligible Cash after payment. | All conditions apply. No unused annual capacity is carried into later years. This is a transaction permission, not another quarterly maintenance covenant. |
| C05: Acquisitions and investments | Acquisitions of related software or implementation-services businesses are permitted up to $5m total consideration per fiscal year, with no carryforward, no continuing default, pro forma leverage at or below 4.50x, and at least $8m Eligible Cash after closing. | Target operations enter the reporting group; material acquired assets remain within the collateral package. Other investments require written agent consent under the specified lender-voting rule. |
| C06: Business and assets | Maintain the existing workflow-software business and reasonably related services. Permit ordinary customer licenses and disposal of obsolete equipment up to $0.5m per fiscal year. Transfers of core product IP outside the loan-party group require prior written consent. | Relatedness needs evidence and judgment. A change in customer contract terms is not automatically a change in permitted business. Ordinary licenses are not treated as an IP sale. |
| C07: Preservation and notice | Maintain corporate existence, material insurance, and required collateral protections; pay taxes when due except amounts contested in good faith with adequate reserves. Notify the agent within five Business Days of a responsible officer learning of a contractual default or termination/nonrenewal notice from a customer that supplied at least 20% of prior-year revenue. | Identify the officer, knowledge date, actual notice, and customer share. A customer notice triggers reporting, not an automatic financial covenant failure. |
| R01: Optional liquidity rider | If elected at origination, month-end Eligible Cash must be at least $5m. At each month-end with Eligible Cash at or below $8m, deliver one cash-flow forecast covering the following 13 weeks, broken into weekly periods, within five Business Days. No weekly update obligation applies. | Elected for the liquidity-risk variation only. The $5m floor is justified by an assumed $3m near-term net stress cash need plus a $2m reserve; the $8m reporting trigger allows earlier review. Neither level is a sourced market norm. |

For this example, Business Days exclude weekends and U.S. federal holidays, use New York time, and exclude the triggering day when counting. A calendar-day delivery deadline falling on a non-Business Day rolls to the next Business Day. Measurement dates do not roll. All scenario dates must be computed against the specified calendar.

For the transaction permissions above, a continuing default includes unresolved covenant noncompliance even during an applicable remediation period, unless a written waiver expressly permits the transaction. Baseline consent or waiver means written agent approval authorized by lenders holding more than 50% of funded principal. Changes to principal, interest, or maturity require all affected lenders' approval. These voting choices are synthetic; amendments must state their actual authorization and scope.

Each generated packet must include a short default/resolution schedule: C01 has no extra numerical grace period or automatic equity cure; C02 delivery failures have a ten-Business-Day remediation period after agent notice; remediable C07 administrative failures have 30 calendar days after agent notice; transaction restrictions require consent before action. R01, when elected, has no automatic cure for its cash minimum, and its forecast-delivery failure uses the C02 remediation mechanism. These are simplified synthetic choices. Preserve the original missed date or failed test even if later remedied. Enforcement powers and voting require their own terms and analyst review; they are not inferred from the ratio.

### Why 5.00x was selected

At $80m net debt and $20m Covenant EBITDA, opening leverage is 4.00x. At constant net debt, EBITDA can fall to **$16m** before exceeding the 5.00x limit: **20% EBITDA decline capacity**. The ratio can increase by 25% from 4.00x to 5.00x; that is a different percentage.

| Independent sensitivity | Net debt | Covenant EBITDA | Leverage | C01 result |
| --- | ---: | ---: | ---: | --- |
| Base | $80m | $20m | 4.00x | Pass |
| Moderate earnings decline | $80m | $18m | 4.44x | Pass |
| Exact boundary | $80m | $16m | 5.00x | Pass |
| Greater earnings decline | $80m | $15m | 5.33x | Fail |
| Cash declines to $2m; Debt remains $90m | $88m | $20m | 4.40x | Pass; R01 cash minimum fails if elected |

These rows are independent sensitivities, not a cash-flow forecast. The final dataset must generate balance-sheet and cash-flow evidence consistent with each row. Passing the leverage test alone does not establish debt-service capacity or overall covenant compliance.

An optional future stepdown requires projected EBITDA and debt at each future test date. Do not automatically reduce the limit every year without checking the borrower's planned amortization, investment, and cash use.

## 7. Add realistic complexity through separate variations

Use one variation at a time initially. Retain the core packet as a control.

| Variation | Required authoring detail |
| --- | --- |
| Equity cure | Specify eligible funds, actual receipt deadline, notice, amount, frequency, affected quarters, permitted ratio benefit, cash/debt double counting, and use of proceeds. M2 is a reference for this structure. A sponsor's intention to fund is not receipt. |
| Waiver | Supply the signed waiver, covered obligation and periods, conditions, expiration, and authority. Preserve the pre-waiver result; apply only the stated legal effect. |
| Amendment | Record old/new clauses, definitions, thresholds, effective date, signature/approval, and when the analyst could know it. Handle expressly retroactive effect separately from historical knowledge. |
| Springing revolver test | Introduce a revolver and define the utilization trigger, numerator/denominator, test date, and beneficiary lenders. An inactive test is not a pass; a covenant that merely starts after a holiday is not necessarily utilization-based. |
| Grower basket | Replace one fixed basket with a fully defined greater-of rule; track use and testing basis. Do not silently grant annual replenishment or unlimited reclassification. |
| Revenue-based software loan | Use a different borrower profile and complete conversion mechanics, informed by M5. This is a separate archetype, not an extra ratio added to CedarBridge. |

Avoid combining all favorable borrower exceptions with all protective lender terms just because each appears somewhere in the source library. A practitioner should assess whether the resulting negotiated package makes sense as a whole.

## 8. Keep covenants and the thesis connected but distinct

Synthetic underwriting assumption A1: Customer Atlas represents 35% of revenue and is committed for two years without termination for convenience. The expected cash flow supports debt service.

New evidence: Atlas receives a 30-day termination right. Current revenue, earnings, and leverage remain unchanged.

Expected interpretation: A1 is contradicted under its explicit wording, and the forward cash-flow implications merit review. That clause change alone does not fail C01, violate C06, or satisfy C07's specific termination/nonrenewal-notice trigger. Whether another obligation applies depends on its wording and additional facts. If Atlas later issues an actual termination notice, C07 requires a separate knowledge-date and delivery analysis.

Generate a paired case with credible, dated replacement commitments or compensation. The original assumption can still be contradicted while the credit implication is neutral, beneficial, mixed, or unclear. Do not force every thesis change into an adverse rating or a covenant violation.

## 9. Evidence packets and evaluation cases

Each case needs: a dated synthetic agreement and schedules; approved underwriting memo; financial statements and covenant certificate; debt/cash and EBITDA bridges; relevant contracts or management updates; applicable amendments/waivers; an availability timeline; and a separate answer key.

Include at least these ten development case families before expanding the corpus:

| Case | Expected distinction |
| --- | --- |
| Stable borrower | Supplied evidence supports routine review; no manufactured alert. |
| Exact ratio boundary | 5.00x passes a maximum of 5.00x; unrounded arithmetic governs. |
| Ordinary earnings deterioration | C01 fails only when the defined, applicable test exceeds its limit. |
| Unsupported EBITDA adjustment | Reported EBITDA $14m plus $1m eligible adjustment gives $15m, even if management labels EBITDA $20m. With $80m net debt, leverage is 5.33x. |
| Restricted or inaccessible cash | Exclude ineligible cash; recompute both leverage and any elected cash minimum. |
| Reporting trigger before minimum failure | With R01 elected, $7m month-end cash passes its $5m floor but activates the $8m forecasting trigger. |
| Thesis change while tests pass | Use the Atlas termination-right example, without inventing a contractual prohibition. |
| Benign or mitigated change | Inspect counterevidence; do not equate a changed assumption with an adverse credit outcome. |
| Missing or late evidence | Distinguish an unknown ratio from a reporting failure and from a remediation period that has not expired. |
| Cure, waiver, or amendment | Preserve the original result and apply the actual scope and effective dates of the new document. |

Also test negation, proposed versus executed transactions, unsupported management assertions, entity mismatches, and annual versus outstanding basket usage. In later rounds, include springing tests and conflicting evidence.

Evaluate the model against an extraction-plus-rules baseline using identical inputs. Measure definition/period accuracy, citation validity, applicability accuracy, unsupported breach claims, missed obligations, thesis-assessment errors, and analyst review effort. Earlier warnings are useful only if warranted at that date and evaluated alongside false alerts.

Split by borrower and clause/scenario family, not merely document or quarter. Keep held-out answers and future documents away from prompt development. Synthetic correctness supports a mechanism claim, not real-market default prediction or validated lead time.

## 10. Quality gates and release labels

| Gate | Acceptance condition |
| --- | --- |
| Source traceability | Each borrowed structure has a real clause locator; all changed numbers and mechanics are labeled synthetic. Superseded guidance is not presented as current. |
| Economic coherence | Debt, cash, statements, debt service, and EBITDA reconcile; downside and refinancing assumptions are explicit. |
| Contract completeness | Definitions, applicability, deadlines, exceptions, consent, defaults, and resolution are specified for every tested obligation. |
| Consistency | Prose and structured records agree; baskets cannot be double spent; cures do not create ungranted benefits. |
| Temporal integrity | Measurement, availability, knowledge, notice, delivery, and effective dates are distinct; later facts do not leak backward. |
| Ground-truth quality | Calculations are independently checked; interpretations have evidence and counterevidence; ambiguity is preserved. |
| Market comparability | A practitioner reviews the package against the chosen borrower segment and flags implausible terms or missing provisions. |
| Evaluation integrity | Development/held-out separation and actual comparison results are recorded; no fabricated performance metrics. |

Use three separate release labels:

1. **Source-grounded draft:** provenance and design rationale exist. This framework is at this stage.
2. **Validated synthetic dataset:** complete generated packets pass arithmetic, timing, consistency, and independent answer-key checks. Not yet produced by this document.
3. **Practitioner-reviewed comparable dataset:** a qualified credit reviewer has assessed the complete terms and evidence against the chosen market segment. Record reviewer, date, scope, and qualifications; do not imply that this establishes statistical market representativeness.

There is no weighted score that can compensate for an undefined denominator, impossible balance sheet, or unsupported source claim.

## 11. Reusable authoring brief

Use the following brief when creating a complete case:

> Create a clearly fictional, profitable U.S. software/business-services borrower and a senior secured cash-flow loan using this framework. First specify the borrower, capital structure, repayment model, approved thesis, and chosen covenant profile. Use source agreements only for identified structural features; label all adapted and invented terms.
>
> Produce the agreement excerpt and complete definitions, clause records, reporting calendar, and a coherent financial model before generating subsequent events. Show why each threshold was selected, calculate boundary and downside cases, and distinguish contractual requirements from analyst review criteria.
>
> Generate dated evidence packets without revealing later information early. Keep every expected answer and future outcome in a separate evaluator document. Include a benign case, a real defined test failure, a reporting trigger without a minimum failure, insufficient evidence, and a thesis contradiction while financial tests pass. Include a cure or waiver only with an explicit operative document and complete mechanics.
>
> List unresolved facts and review needs. Do not claim OCC approval, universal market-standard thresholds, practitioner validation, or measured performance. Deliver a source register and completed quality-gate checklist with the case.

For the first build, use one borrower, the core package, and one elected variation. Generate a small, fully reconciled set of documents before increasing borrower count or contractual complexity.
