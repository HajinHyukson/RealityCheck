# Duolingo files

This folder is a self-contained, authored demonstration dataset. The core PDFs follow the requested classifications 01 to 13. There is one sourced public-background digest and twelve synthetic documents, including a PDF snapshot of the opening model. The model also has an editable XLSX workbook. Editable Markdown copies are in the editable folder. The real, complete 123-page FY2025 Duolingo Form 10-K and its public source links are in sources.

## Numbered file index

| Number | Classification | Format |
| --- | --- | --- |
| 01 | [Duolingo Company Background](<01 memo - Duolingo Company Background.pdf>) | PDF |
| 01 | [Duolingo Inc FY2025 Form 10-K](<sources/01 Duolingo FY2025 Form 10-K.pdf>) | PDF |
| 02 | [Original Credit Agreement](<02 Credit Agreement - Original Credit Agreement.pdf>) | PDF |
| 03 | [Underwriting Memo](<03 memo - Underwriting Memo.pdf>) | PDF |
| 04 | [Opening Financial and Operating Model](<04 memo - Opening Financial and Operating Model.xlsx>) | XLSX |
| 04 | [Opening Financial and Operating Schedules](<04 memo - Opening Financial and Operating Schedules.pdf>) | PDF |
| 05 | [Lender Review Guidelines](<05 memo - Lender Review Guidelines.pdf>) | PDF |
| 06 | [October Routine Management Report](<06 Reports - October Routine Management Report.pdf>) | PDF |
| 07 | [External Learning Subscription Report](<07 Reports - External Learning Subscription Report.pdf>) | PDF |
| 08 | [December Company Impact and Cash Report](<08 Reports - December Company Impact and Cash Report.pdf>) | PDF |
| 09 | [January Mitigation and Updated Forecast](<09 Reports - January Mitigation and Updated Forecast.pdf>) | PDF |
| 10 | [Processor Settlement Timing Notice](<10 Reports - Processor Settlement Timing Notice.pdf>) | PDF |
| 11 | [Treasury Forecast and Settlement Receivables](<11 Reports - Treasury Forecast and Settlement Receivables.pdf>) | PDF |
| 12 | [March Cash Results and Settlement Follow-up](<12 Reports - March Cash Results and Settlement Follow-up.pdf>) | PDF |
| 13 | [Service Shutdown and Missed Interest Payment](<13 Reports - Service Shutdown and Missed Interest Payment.pdf>) | PDF |

## Baseline upload

Use documents 01 to 05 together as of October 1, 2026. To demonstrate ingestion of an original SEC filing, use the full Form 10-K in sources for classification 01; the short 01 digest is a convenient reading companion. Attach the filing as real company background, with the hypothetical credit agreement and finances identified as synthetic. Document 01 is public background; 02 is the original credit agreement; 03 is the underwriting memo; 04 is the opening financial and operating model; 05 is the lender policy. For PDF-only upload, use 04's PDF rather than the XLSX. The workbook contains only origination assumptions and forecasts, not later scenario observations. Do not upload both formats as separate evidence records for the same document.

## Later uploads

Introduce 06 on November 18, 2026, 07 on December 7, 2026, 08 on January 19, 2027, and 09 on February 12, 2027. The date a report becomes available is different from the period it covers. The supplied classifications are not expected model answers. Industry report 07 does not name the borrower. Let the model connect the report to the earlier business assumptions, and let company report 08 establish the actual scenario exposure.

## Identity and evidence boundaries

Duolingo Inc is the real business reference. Duolingo Learning Services LLC and Scenario Lender D01 are fictional and have no asserted corporate relationship with Duolingo Inc. All financial figures, credit terms, future reports and survey results are invented. Real company financials must not be substituted into the hypothetical credit agreement. No actual executive, company signature, press-release logo or company endorsement is used.

The agreement includes separate actual-cash and forecast-reporting thresholds. Cohort counts use the scenario's definitions, not Duolingo's public KPI definitions. The original financial model is a simplified management model. Later reports distinguish annual billings, revenue, processing fees and cleared cash. No proposed or adopted amendments are included in the source reports; the original agreement remains operative. Reports 10-12 add business evidence for a further review.

## App readiness

These are source documents for the planned document-upload workflow. Creating this folder does not seed a second company in RealityCheck, run Nemotron or connect the PDFs to the existing H01 database. Current company onboarding still requires structured agreement and source records. Preserve this set as the input; retain generated records and model findings separately when that workflow is connected.

## Editing

Edit the numbered Markdown sources and workbook if needed. The PDFs are snapshots and do not automatically change when the workbook is edited. Reconcile any changed numbers across the agreement, memo, model and later reports before using revised files. The document register records IDs, availability dates and PDF hashes. The guide and register describe the dataset and are not borrower evidence to upload.

## Additional evidence reports: 10-12

These three reports extend the existing 06-09 sequence. They contain business evidence and no request for a covenant change, proposed replacement threshold or prescribed model response.

| Report | Available to analyst | Document |
| --- | --- | --- |
| 10 | 2027-02-19 | [Processor Settlement Timing Notice](<10 Reports - Processor Settlement Timing Notice.pdf>) |
| 11 | 2027-02-26 | [Treasury Forecast and Settlement Receivables](<11 Reports - Treasury Forecast and Settlement Receivables.pdf>) |
| 12 | 2027-04-01 | [March Cash Results and Settlement Follow-up](<12 Reports - March Cash Results and Settlement Follow-up.pdf>) |

The sequence is a confirmed business change, a revised cash forecast, then actual bank results and counterparty follow-up. Upload one at a time on the stated availability date, after 01-05 have established the original library and 06-09 have supplied the earlier history. Avoid giving the final actual results to the model in earlier steps.

Presenter check: compare the last report's actual freely available cash ($21.5000m) with the original C01 floor ($25.0000m). The stored agreement supplies the threshold; the new reports do not tell the model which clause to change. A useful outcome is evidence-linked review of the current terms and operating assumptions. Forecast risk, an actual failed test, notice/cure mechanics and a proposed amendment are distinct findings. No report itself changes the agreement, and the model may recommend review or another supported response.

These PDFs have not been ingested or run through Nemotron. Rehearse the upload and review flow to verify the actual application flags; the files alone do not guarantee a particular model output. This guide is presenter guidance and is not borrower evidence to upload.

## Severe event: report 13

Upload [13 Service Shutdown and Missed Interest Payment](<13 Reports - Service Shutdown and Missed Interest Payment.pdf>) on 2027-05-11, after report 12. 21-day service shutdown; conversion 1%, renewal 40%; cash $0.08m; April interest $450,000 still unpaid May 10.

The report includes five evidence sections: E01 incident and operating observations; E02 CFO-certified bank reconciliation and cash ledger; E03 dated payment records and reproduced counterparty confirmations; E04 underlying operating schedules; E05 reconciled thirteen-week funding forecast and assumptions. The report names no covenant, requests no amendment and specifies no model response. Negative forecast positions mean funding gaps, not actual negative cash. Preserve the prior reports as earlier evidence; do not replace them with this later stress event.

Presenter check: distinguish disruption of the business, current cash, missed or upcoming payments and future funding needs. Apply only terms in the existing fictional credit agreement. For Duolingo and YETI, the documented April 30 interest remains unpaid after May 7; no later payment is assumed. Planet Fitness's June 15 payroll is upcoming as of its report date. The agent should assess those facts without treating every adverse event as the same contractual outcome.

The report has not been run through Nemotron. The severity and arithmetic support a substantive review, but a particular application flag still needs a rehearsal. This guide is presenter material and is not borrower evidence to upload.
