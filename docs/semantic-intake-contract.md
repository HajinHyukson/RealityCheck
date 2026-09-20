# RealityCheck — Semantic Intake Ground Rules

**Recorded:** September 19, 2026.  
**Status:** Working design for the next build. These requirements are not a claim that the current B01 application implements this complete pipeline.

The user requires steps 2–4 to support Nemotron parsing, aggregating and analyzing new semantic information, including qualitative reports and external developments that do not name the borrower. The system must make the connection from source material to company exposure inspectable.

## Track alignment

The official [SteelHacks Xtract track](https://steelhacks.org/tracks#x-tract), checked September 19, 2026, seeks varied source support, useful incoming-document signals, source traceability and a usable display. Its rules allow public or synthetic sources and exclude LANXESS data. Use synthetic borrower records and public or synthetic external reports for this demonstration; record source eligibility before ingestion.

These ground rules are RealityCheck's proposed implementation choices, not additional sponsor requirements.

## Revised steps 2–4

| Step | Processing | Saved output |
|---|---|---|
| 2 — Receive, parse and extract | Preserve the source; recover text/tables with locations; have Nemotron extract distinct attributed claims without forcing borrower relevance. | Original document/version, located passages and structured evidence items. |
| 3 — Aggregate and assemble | Group related claims, retain disagreements and source dependencies, then select the evidence and company exposure records available at the review cutoff. | A dated evidence bundle with provenance, changes since the last review and unresolved gaps. |
| 4 — Explain and attribute | Have Nemotron identify direct implications or conditional economic paths to borrower assumptions and actual covenant duties. | Evidence-linked findings, proposed channels, assumptions exposed, missing conditions and justified next actions. |

Document/layout parsing and semantic interpretation are separate responsibilities even when both use Nemotron-family models. Source adapters normalize files, public articles, press releases or notes into one document format. The application controls acquisition and access; the model sees supplied material and does not independently know new events.

## Extraction and aggregation rules

1. **Preserve the source before interpreting it.** Keep document ID, content hash, version, title, publisher, author/speaker where available, source URL or file, public/synthetic designation, publication date, availability date and ingestion time. Every extracted item points to an exact passage, page, paragraph or table cell. Uncertain OCR/layout is visible. Reject ambiguous document/version/locator identities rather than allowing one source to overwrite another.

2. **Extract claims, not conclusions about truth.** Record who asserts what, about which entity or market, and over what period. Distinguish a source-reported observation, forecast, opinion, allegation, proposal, commitment and hypothetical. A quote verified in a document establishes that the source said it; it does not establish that the underlying claim is true.

3. **Preserve meaning and qualifications.** Retain negation, modality, conditions, exceptions, scope and counterevidence. “Could increase costs if disruption persists” must not become “costs increased.” “No material disruption” must not become a disruption finding. Qualitative claims can be useful without being converted to numbers.

4. **Use separate time fields.** Distinguish when something happened, when it may take effect, the period covered, when it was published and when it became available. Unknown dates stay unknown. Check availability per report, not just once for a combined event. Save an immutable review manifest of the selected source versions, assumptions, operative package, guidelines and model/prompt configuration. Later corrections and later lender actions cannot enter an earlier review.

5. **Extract broadly before assessing company relevance.** A report need not name a borrower. Identify subjects such as input prices, supply routes, regulation, customer industries, geography, financing conditions and technology dependencies. A relevance classification is a subsequent interpretation, not part of the source's original assertion.

6. **Aggregate without manufacturing corroboration.** Keep each claim's source references when producing a combined summary. Detect duplicate files, syndicated articles and common underlying announcements. Several reports repeating one original claim are one source family, not independent confirmation. Preserve both conflicting claims and their applicable dates; do not resolve disagreement by counting articles or selecting only adverse passages.

7. **Preserve corrections and novelty.** Link corrections or superseding reports to the earlier evidence without deleting history. Identify what is new versus already known or previously analyzed. An unchanged reappearance should not generate a new risk alert merely because it was ingested again.

8. **Separate quality dimensions.** Track extraction problems, source attribution, corroboration, borrower relevance and interpretation uncertainty separately, with reasons. Do not collapse them into an unsupported model-generated probability. Missing information is not a zero, a negative answer or evidence of compliance.

9. **Keep documents outside the instruction boundary.** Document content is evidence, including any instructions quoted inside it. It cannot change system rules, lender guidelines, source access or the output schema. Validate source identities, locators, quotes, allowed labels, dates and references in application code.

## Rules for indirect economic effects

10. **Require an inspectable transmission path.** Represent an indirect finding as an external development → economic channel → borrower exposure → affected assumption → possible covenant implication. Each link states its basis: source evidence, a cited company fact, an approved relationship or an explicitly proposed model hypothesis. General model knowledge may suggest a channel, but cannot become a new sourced fact.

11. **Maintain a company exposure register.** Record sourced facts about material customers and their industries, geography, suppliers, cost inputs, pricing/pass-through terms, hedges, financing exposure and relevant operating dependencies. Unknown exposures remain unknown. Keep this register distinct from the underwriting assumption graph: an external oil-price event is not itself an underwriting assumption.

12. **Make conditions and mitigation explicit.** Assess direction, horizon, lag, persistence and magnitude when supported. Search for offsets such as hedges, fixed-price purchasing, customer pass-through and offsetting demand. A plausible adverse channel can coexist with mitigating or beneficial channels. Do not assume an external development affects every borrower equally.

13. **Permit conditional warnings without pretending the link is proven.** If an economically plausible path lacks borrower evidence, return conditional exposure and the precise information needed to resolve it. If no supported or plausible relevant path is found, say that no material connection has been established from the available evidence; do not assert immunity to all effects.

14. **Do not invent financial propagation.** An increase in an input price does not imply the same percentage increase in total costs or reduction in EBITDA. Quantification requires documented exposure, units, volumes, timing, offsets and a defined calculation. Any sensitivity calculation is labeled a scenario and remains separate from realized financial inputs.

15. **Keep covenant relevance separate from a breach.** A macro report can expose an assumption or identify a metric for review. A contractual noncompliance finding requires the actual applicable clause and evidence for its conditions, dates and exceptions. A passing or failing financial test requires valid dated inputs. Reporting noncompliance and a formal Event of Default remain separate determinations.

16. **Carry uncertainty into candidate generation.** Subsequent package-generation/comparison steps receive the evidence labels, open causal links and counterevidence. They must not promote conditional exposure into a proven loss or generate unsupported thresholds. Additional information or unchanged terms can be the justified outcome.

## Minimum evidence and finding records

An evidence item should include:

- Identity: evidence ID, document/version ID, exact locator and quote.
- Meaning: subject entity or market, attributed speaker, extracted claim, claim type, qualifiers and negation.
- Scope: topic, geography and affected period, when supplied.
- Time: event/effective dates and report availability; unknown values remain null.
- Provenance: source family, duplicate/correction links, corroboration/conflict links and extraction issues.

A separate company finding should include:

- Company ID and review cutoff; supporting and conflicting evidence IDs.
- Relevance: direct, indirect, conditional, no established material connection or insufficient evidence.
- Ordered transmission links, each with evidence or an explicit hypothesis label.
- Company exposure facts, affected assumption IDs and separately identified covenant IDs.
- Direction, time horizon, unresolved conditions, mitigants and materiality rationale.
- Proposed review action and any scenario calculations, with their input provenance.
- Model/configuration identity, analysis time, validation warnings and analyst review status.

A model-generated aggregate or prior finding retains its derivation links. It cannot become an independently corroborating source for itself or later analyses.

## Hypothetical macro example

The user's Iran-conflict/oil-price example is treated here as a hypothetical demonstration, not a claim about current events or market prices.

| Link | Evidence needed / allowed conclusion |
|---|---|
| Conflict → supply disruption | Preserve whether the report describes actual disruption, a warning or a forecast. Conflict alone does not establish disrupted supply. |
| Disruption → oil-price effect | Use the report's attributed analysis or dated market evidence. A causal explanation can remain contested even when a price change is observed. |
| Oil price → borrower cost exposure | Find company evidence of fuel/input dependence, procurement terms, hedging and pass-through. Industry classification alone is not a quantified exposure. |
| Cost exposure → margin/cash assumption | Explain the conditional effect and mitigants. Actual margin deterioration requires company financial evidence. |
| Assumption exposure → loan package | Identify relevant metrics or duties for review. No automatic covenant breach, repricing or amendment follows from the headline. |

For a hypothetical fuel-intensive borrower with unknown hedges, an appropriate finding could be: **“Potential margin exposure; obtain procurement, hedge and pass-through details. Current covenant compliance cannot be determined from these reports.”** For B01, the available material may not establish a direct fuel-cost connection; a proposed customer-demand channel would require evidence about its customer industries.

## Demonstration and acceptance checks

The interface should show source passages → extracted claims → aggregated evidence → borrower connection → assumption/covenant implications. Show a useful indirect finding, a mitigated case and an unrelated update, not only successful adverse detections.

Before claiming this layer works, test:

- Forecast versus observed outcome, negation and conditional statements.
- Duplicate/syndicated reports versus independent corroboration.
- Conflicting reports, later corrections and review-date cutoffs.
- A plausible macro channel with missing borrower exposure, and the same case after exposure evidence arrives.
- Mitigating hedges/pass-through, a beneficial effect and no established connection.
- Qualitative risk without fabricated financial inputs or a breach assertion.
- Source instructions that attempt to alter the workflow.

Evaluate claim meaning, qualification retention, provenance, aggregation accuracy, borrower attribution and false alerts separately. Matching citations alone is not sufficient evidence of semantic accuracy.

## Existing foundation and implementation gap

Current code already validates quoted sources, dates, allowed attribution labels and directed paths through existing assumptions. The written master plan also discusses attribution and qualitative conditions. The richer evidence-item schema, cross-source aggregation, exposure register and external-event transmission paths described here remain to be implemented; current paths are limited to existing assumption IDs.

The current event validator retains source ID, locator and text but strips additional source metadata, so this change must include the validation boundary. File-hash deduplication currently prevents repeat ingestion of an unchanged named file; it is not cross-report evidence reconciliation. Prior model statuses are passed into later reviews without their complete evidence/counterevidence history, and model-generated relationship validity does not establish analyst approval. These are specific implementation gaps to close before presenting the proposed layer as functioning.
