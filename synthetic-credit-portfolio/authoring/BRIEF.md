# Authoring brief for the corrected 30-company deliverable

User clarification: 30 synthetic companies, each with its own specialized private-credit contract, under the agreed profitable U.S. software/business-services framework. Output 30 standalone agreements, financial models, underwriting memos, and separately labeled evaluator material. This authoring directory is NOT model input.

Each author supplies a JSON array of 10 companies in the assigned batch file. No code or markdown wrappers. All money fields are millions of USD. Read ../../Synthetic-Covenant-Framework.md. Business, sponsor, lender, subsidiary and customer names must be fictional. Use a single direct lender per agreement (no syndicated voting complexity). New portfolio agreements are independent of the old CedarBridge clause library, even if its structural lessons are reused.

Each company record must contain these exact keys:

```
id: "B01" etc
name: legal borrower name ending Inc. or LLC
sector: short precise industry
description: 2 sentences, actual business/revenue model and distinctive operating risk
sponsor: fictional sponsor name
lender: fictional direct lender name
subsidiaries: two distinct fictional domestic legal entity names
revenue_m: number 35–200
ebitda_m: reported EBITDA number, margin 12–32%, positive
adjustment_m: documented one-time cash restructuring deducted in ebitda_m; 0–1.5, <= cap percentage of EBITDA
ebitda_cap_pct: 0, 5, 10, or 15
da_m: depreciation/amortization > 0, approximately 2–5% revenue
debt_m: opening term loan principal, economically plausible vs EBITDA
cash_m: eligible operating cash, normally 5–18
restricted_cash_m: additional third-party/restricted cash, 0–8; excluded from netting, constant in model
cash_netting_cap_m: <= cash_m
annual_rate_pct: fixed cash interest rate 8–11%, synthetic, not sourced pricing
amortization_pct: annual percent of ORIGINAL principal: 1, 2, 3, or 5
term_years: 4, 5, or 6
capex_m: annual cash capital investment including capitalized development, generally 2–6% revenue
working_capital_investment_m: annual positive operating working-capital use, generally 0.5–3% revenue
max_leverage: numeric maximum, choose so opening (debt-cashnetcap)/(ebitda+adjustment) has 15–30% EBITDA decline capacity; not sampled independently
optional_type: "none", "liquidity", "interest", "coverage", or "capex" (one only)
optional_threshold: number, or null for none; calibrate vs actual borrower metrics
liquidity_trigger_m: only for liquidity, > floor and < cash_m; otherwise null
lease_basket_m: additional finance-lease principal OUTSTANDING cap
dividend_basket_m: cash dividend annual cap, no carryforward
dividend_max_leverage: tighter than maintenance limit but >= opening leverage
transaction_cash_floor_m: < cash_m, all external dividends/acquisitions require post-transaction floor
acquisition_basket_m: annual cash acquisition consideration including fees, no carryforward
acquisition_max_leverage: <= maintenance limit but >= opening leverage
asset_sale_basket_m: annual fair-value cap for obsolete equipment
report_days: quarterly reporting deadline, 30/45/60 calendar days
customer_notice_threshold_pct: 10/15/20/25, prior fiscal year customer-group revenue
base_revenue_growth_pct: annual 2027 revenue growth 3–12%
base_ebitda_growth_pct: annual 2027 reported EBITDA growth 3–15%
moderate_ebitda_drop_pct: 10–20% below base 2027 EBITDA
severe_ebitda_drop_pct: 30–45% below base 2027 EBITDA
credit_rationale: explain chosen leverage, liquidity/coverage if any, cash needs, and critical underwriting vulnerability, 100–150 words; do not invent additional inconsistent figures
specialized_covenants: exactly 3 objects, each {id:"S1"/"S2"/"S3",title,clause,evidence,resolution:"R"/"A"/"X",thesis_ids:["A1",...]}. Full operative clause prose, 80–130 words each, self-contained definitions and precise trigger/permitted activity/deadline/exception. Genuine sector-specific duties; not three interchangeable generic clauses. R reporting = 10 Business Days after lender notice before Event of Default; A remediable operating failure = 30 calendar days after lender notice; X prohibited action = immediate on execution. Do not assume R reporting requires minimum KPI compliance. Refer to common C01 leverage, C02 reporting, C03 debt/liens, C04 distributions, C05 acquisitions/investments, C06 business/assets/IP, C07 preservation/collateral, C08 event notice; optional C09. S duties all operative from close Dec31 2026; ongoing quarterly specifics first March31 2027.
assumptions: exactly 4 objects {id:"A1".."A4",statement,evidence,review_trigger,covenant_links:["C01", "S1", ...],protection:"direct"/"reporting"/"analyst_judgment"}. Each has distinct specific synthetic baseline facts. First two sector specific, others cash/credit. Statement/evidence noncircular; evidence describes named baseline source paragraph. Memo approved Dec31 2026. These are beliefs, not extra covenants.
event: {event_date:"2027-06-15",available_at:"2027-06-16",review_date:"2027-06-18",document_title,source_passages:[{id:"P1",text}, {id:"P2",text}], affected_assumption_ids:[...], evaluated_clause_ids:[...], expected_applicability,expected_evidence_sufficiency,expected_contract_result,expected_resolution,expected_thesis_assessment,expected_credit_implication,rationale}. Two dated synthetic passages only: one primary executed/proposed contract or event and one management/rebuttal contextual passage. If event triggers a notice, knowledge date must be explicit. Choose stable, harmful-but-contract-compliant, benign/mitigated, missing evidence, proposed-not-executed, or actual defined sector-duty breach examples. Need diversity. Do not claim financial test failure from qualitative evidence. Avoid fabricated future financial amounts; root will provide Q1 routine financials and forecasts independently. No waiver/equity-cure events unless full operative mechanics are present (prefer omit).
```

Core assumptions for all profiles: consolidated two domestic wholly-owned guarantor subsidiaries, no unrestricted entities; refinance existing operating-company term debt at par at close, no new money, no transaction fees in this intentionally simplified refinancing. First annual principal installment Dec31 2027; maturity balloon disclosed. Fixed annual interest rate, payment quarterly on ACT/365F outstanding principal; models annualize constant within-year principal until Dec31 installment. Final quarterly interest receives the actual day count. Predecessor debt 2026 same rate but no amortization, refinanced at same principal; history may include sponsor distributions before current agreement becomes effective. Ordinary tax rate25% of positive pretax earnings. Root computes all tax, interest, cash bridges, balance sheets, base/downside metrics and covenant calibration.

Cash coverage if selected: (reported EBITDA − cash taxes − capital investment − positive working-capital investment)/(cash interest + scheduled principal excluding balloon), TTM tested first Dec31 2027. Interest coverage if selected: Covenant EBITDA/Cash Interest, TTM first Dec31 2027. Leverage tests quarterly firstMar31 2027, zero or negative EBITDA fails when net debt positive. Liquidity measured monthend firstJan31; one 13-week forecast due5BusinessDays if cash<=trigger; no weekly recurring report. Capex optional annual cap on cash capital investment. Cash floor and capex choice must not cause an opening/base forecast failure. If working capital-intensive, choose more cash/lower debt rather than make cashflow implausible.

Contract calendar: New York time, weekends and observed U.S. federal holidays excluded. Triggering day excluded. Calendar-day delivery and postclosing administrative-performance deadlines roll forward; measurement dates never roll. Receipt deadline 5pm portal timestamp. A financial failure under C01/C09 has no automatic cure; written lender waiver required. No inferred acceleration from model output.

Source labels: original prose and every term synthetic. Framework source structures M1 leverage/restrictions, M3 reporting/business scope, M4 conditional forecast. No industry market-median or regulatory claims. Do not browse for invented company facts. Do not copy external legal prose.
