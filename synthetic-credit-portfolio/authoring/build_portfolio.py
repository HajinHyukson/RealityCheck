"""Assemble the authored borrower records into standalone synthetic contracts.

Standard library only. Run from any directory; assertions verify model arithmetic
and document/record parity. No app integration or market-validation claim.
"""
from __future__ import annotations

import calendar
import json
import re
import zipfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "model_inputs"
EVAL = ROOT / "evaluator"
AUTHOR = ROOT / "authoring"
ASOF = "2026-12-31"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def money(value):
    return f"${value:,.3f}m"


def observed(day):
    return day - timedelta(days=1) if day.weekday() == 5 else day + timedelta(days=1) if day.weekday() == 6 else day


def nth_weekday(year, month, weekday, nth):
    first = date(year, month, 1)
    return first + timedelta(days=(weekday - first.weekday()) % 7 + 7 * (nth - 1))


def holidays(year):
    result = set()
    for y in (year - 1, year, year + 1):
        for month, day in ((1, 1), (6, 19), (7, 4), (11, 11), (12, 25)):
            result.add(observed(date(y, month, day)))
        result.update([nth_weekday(y, 1, 0, 3), nth_weekday(y, 2, 0, 3),
                       nth_weekday(y, 9, 0, 1), nth_weekday(y, 10, 0, 2), nth_weekday(y, 11, 3, 4)])
        last = date(y, 5, 31)
        result.add(last - timedelta(days=last.weekday()))
    return result


def business(day):
    return day.weekday() < 5 and day not in holidays(day.year)


def roll(day):
    while not business(day):
        day += timedelta(days=1)
    return day


def bd_after(day, number):
    for _ in range(number):
        day += timedelta(days=1)
        while not business(day):
            day += timedelta(days=1)
    return day


def ce(p, reported, adjustment):
    return reported + min(adjustment, max(0, reported) * p["ebitda_cap_pct"] / 100)


def balance(cash, restricted, ar, other, fixed, goodwill, ap, accrual, debt, equity, client_obligation=0):
    assets = cash + restricted + ar + other + fixed + goodwill
    liabilities = ap + accrual + client_obligation + debt
    return {"cash_or_unfunded_deficit_m": cash, "restricted_cash_m": restricted,
            "trade_receivables_m": ar, "other_operating_current_assets_m": other,
            "fixed_and_capitalized_software_assets_net_m": fixed, "historical_goodwill_m": goodwill,
            "total_assets_m": assets, "trade_payables_m": ap, "operating_accruals_m": accrual,
            "restricted_funds_obligation_m": client_obligation, "funded_term_debt_m": debt,
            "total_liabilities_m": liabilities, "equity_m": equity,
            "balance_check_m": assets - liabilities - equity}


def income(revenue, ebitda, da, interest):
    pretax = ebitda - da - interest
    tax = max(0, pretax) * .25
    return {"revenue_m": revenue, "cash_operating_expenses_m": revenue - ebitda,
            "reported_ebitda_m": ebitda, "depreciation_and_amortization_m": da,
            "cash_interest_paid_m": interest, "pretax_income_m": pretax,
            "income_tax_expense_and_cash_paid_m": tax, "net_income_m": pretax - tax}


def advance(p, opening, revenue, ebitda, da, interest, capex, wc, amort,
            adjustment=0, cash_target=None, dsodays=None):
    inc = income(revenue, ebitda, da, interest)
    operating = ebitda - inc["income_tax_expense_and_cash_paid_m"] - interest - wc
    free = operating - capex - amort
    contribution = distribution = 0.0
    if cash_target is not None:
        net = cash_target - opening["cash_or_unfunded_deficit_m"] - free
        contribution, distribution = max(0, net), max(0, -net)
    closing_cash = opening["cash_or_unfunded_deficit_m"] + free + contribution - distribution
    ar = revenue * (dsodays if dsodays is not None else p["receivable_days"]) / 365
    other = opening["other_operating_current_assets_m"] + wc - (ar - opening["trade_receivables_m"])
    fixed = opening["fixed_and_capitalized_software_assets_net_m"] + capex - da
    closing = balance(closing_cash, p["restricted_cash_m"], ar, other, fixed,
                      opening["historical_goodwill_m"], opening["trade_payables_m"],
                      opening["operating_accruals_m"], opening["funded_term_debt_m"] - amort,
                      opening["equity_m"] + inc["net_income_m"] + contribution - distribution,
                      client_obligation=opening["restricted_funds_obligation_m"])
    eligible = max(0, closing_cash)
    net_debt = closing["funded_term_debt_m"] - min(eligible, p["cash_netting_cap_m"], closing["funded_term_debt_m"])
    covenant_ebitda = ce(p, ebitda, adjustment)
    leverage = net_debt / covenant_ebitda if covenant_ebitda > 0 else (0 if net_debt == 0 else None)
    numerator = ebitda - inc["income_tax_expense_and_cash_paid_m"] - capex - max(0, wc)
    return {"income_statement": inc, "closing_balance_sheet": closing,
            "cash_flow": {"opening_cash_m": opening["cash_or_unfunded_deficit_m"],
                          "operating_cash_after_interest_tax_and_working_capital_m": operating,
                          "capital_investment_m": capex, "working_capital_investment_m": wc,
                          "scheduled_principal_paid_m": amort, "shareholder_contribution_m": contribution,
                          "shareholder_distribution_m": distribution, "net_cash_change_m": free + contribution - distribution,
                          "closing_cash_or_unfunded_deficit_m": closing_cash},
            "ebitda_reconciliation": {"reported_ebitda_m": ebitda, "documented_restructuring_m": adjustment,
                                      "cap_m": max(0, ebitda) * p["ebitda_cap_pct"] / 100,
                                      "permitted_adjustment_m": covenant_ebitda - ebitda,
                                      "covenant_ebitda_m": covenant_ebitda},
            "metrics": {"eligible_cash_m": eligible, "net_debt_m": net_debt, "leverage_x": leverage,
                        "interest_coverage_x": covenant_ebitda / interest if interest > 0 else None,
                        "cash_coverage_x": numerator / (interest + amort) if interest + amort > 0 else None,
                        "unfunded_cash_need_m": max(0, -closing_cash)}}


def make_model(p):
    r, e, da, d = (p[k] for k in ("revenue_m", "ebitda_m", "da_m", "debt_m"))
    rate, capex, wc = p["annual_rate_pct"] / 100, p["capex_m"], p["working_capital_investment_m"]
    rev25, cash25, ar25 = r / 1.08, p["cash_m"] * .75, r / 1.08 * p["receivable_days"] / 365
    other25, fixed25, goodwill, ap, accrual = r * .12, da * 8, d * 1.15, r * .06, r * .04
    client_obligation = p["restricted_cash_m"] if p["restricted_cash_type"] == "custodial_client_funds" else 0
    net25 = cash25 + p["restricted_cash_m"] + ar25 + other25 + fixed25 + goodwill - ap - accrual - d - client_obligation
    b25 = balance(cash25, p["restricted_cash_m"], ar25, other25, fixed25, goodwill, ap, accrual, d, net25, client_obligation)
    i25 = income(rev25, e / 1.08, da / 1.05, d * rate)
    y26 = advance(p, b25, r, e, da, d * rate, capex, wc, 0,
                  adjustment=p["adjustment_m"], cash_target=p["cash_m"])
    b26 = y26["closing_balance_sheet"]
    rg, eg = 1 + p["base_revenue_growth_pct"] / 100, 1 + p["base_ebitda_growth_pct"] / 100
    base_r, base_e = r * rg, e * eg
    amort = d * p["amortization_pct"] / 100
    scenarios = {}
    for name, revfactor, efactor, wcfactor, dsodays in (
        ("base", 1, 1, 1, p["receivable_days"]),
        ("moderate", .94, 1 - p["moderate_ebitda_drop_pct"] / 100, 1.5, p["receivable_days"] + 7),
        ("severe", .84, 1 - p["severe_ebitda_drop_pct"] / 100, 2, p["receivable_days"] + 18)):
        scenarios[name] = advance(p, b26, base_r * revfactor, base_e * efactor, da,
                                  d * rate, capex, wc * wcfactor, amort, dsodays=dsodays)
        scenarios[name]["assumptions"] = {"revenue_relative_to_base": revfactor,
                                         "ebitda_relative_to_base": efactor,
                                         "working_capital_use_multiple": wcfactor,
                                         "receivable_days": dsodays,
                                         "capital_investment_held_constant": True,
                                         "restructuring_addback_forecast": 0}
    # Actual first-quarter inputs are a deliberately controlled realization of
    # the base operating plan. TTM values mix 2026 Q2-Q4 with 2027 Q1, not Q1*4.
    q_interest = d * rate * 90 / 365
    q = advance(p, b26, base_r / 4, base_e / 4, da / 4, q_interest, capex / 4, wc / 4, 0,
                dsodays=p["receivable_days"] * 4)
    qb = q["closing_balance_sheet"]
    q_ar = b26["trade_receivables_m"] + (base_r * p["receivable_days"] / 365 - b26["trade_receivables_m"]) / 4
    q_other = b26["other_operating_current_assets_m"] + wc / 4 - (q_ar - b26["trade_receivables_m"])
    qb["trade_receivables_m"], qb["other_operating_current_assets_m"] = q_ar, q_other
    ttm_e, ttm_adjust = .75 * e + .25 * base_e, .75 * p["adjustment_m"]
    ttm_ce = ce(p, ttm_e, ttm_adjust)
    q["metrics"]["leverage_x"] = q["metrics"]["net_debt_m"] / ttm_ce
    q["metrics"]["interest_coverage_x"] = None
    q["metrics"]["cash_coverage_x"] = None
    q["metrics"]["coverage_applicability"] = "Not yet due: optional coverage tests first apply December 31, 2027. No annualized quarter proxy is substituted."
    q["ttm_ebitda_reconciliation"] = {"reported_ebitda_m": ttm_e, "documented_restructuring_m": ttm_adjust,
                                        "permitted_adjustment_m": ttm_ce - ttm_e, "covenant_ebitda_m": ttm_ce}
    q["period"] = "2027-01-01 through 2027-03-31; balance sheet at March 31"
    q["available_at"] = "2027-06-01"
    q["receipt_status"] = "Underlying statements available June 1; submission compliance is not assumed"
    forecast = scenarios["base"]
    future = [{"year": 2027, "projection": forecast}]
    for year in range(2028, 2026 + p["term_years"]):
        prev = future[-1]["projection"]["closing_balance_sheet"]
        years = year - 2026
        forecast = advance(p, prev, r * rg ** years, e * eg ** years, da,
                           prev["funded_term_debt_m"] * rate * (366 if calendar.isleap(year) else 365) / 365,
                           capex, wc, amort)
        future.append({"year": year, "projection": forecast})
    maturity_year = 2026 + p["term_years"]
    last = future[-1]["projection"]["closing_balance_sheet"]
    maturity_projection = advance(p, last, r * rg ** p["term_years"], e * eg ** p["term_years"], da,
                                 last["funded_term_debt_m"] * rate * (366 if calendar.isleap(maturity_year) else 365) / 365,
                                 capex, wc, 0)
    reserve = max(p["transaction_cash_floor_m"], p["optional_threshold"] if p["optional_type"] == "liquidity" else 0)
    cash_before = maturity_projection["closing_balance_sheet"]["cash_or_unfunded_deficit_m"]
    balloon = last["funded_term_debt_m"]
    return {"currency": "USD", "scale": "millions", "agreement_id": p["id"] + "-CA-2026-01",
            "history": {"2025_comparative": {"income_statement": i25, "closing_balance_sheet": b25},
                        "2026": y26}, "q1_2027": q, "2027_scenarios": scenarios,
            "base_projection_to_prematurity": future,
            "maturity_funding": {"date": f"{maturity_year}-12-31", "balloon_m": balloon,
                                 "base_cash_before_balloon_m": cash_before, "operating_reserve_m": reserve,
                                 "projected_cash_available_for_balloon_m": max(0, cash_before - reserve),
                                 "refinancing_or_equity_needed_m": max(0, balloon - max(0, cash_before - reserve)),
                                 "committed_refinancing_m": 0,
                                 "assumption": "Base operating growth continues, no distributions or acquisitions; no refinancing commitment is assumed."},
            "model_conventions": ["2025 is comparative income and balance-sheet data; a 2025 cash-flow statement is not fabricated.",
                                  "2026 historical restructuring expense is spread evenly across the four quarters; it is not forecast to recur in 2027.",
                                  "Predecessor debt has the same principal and fixed interest rate, with no 2026 amortization; refinancing at par adds no cash or fees.",
                                  "2026 shareholder distributions or contributions reconcile the historical cash target and precede the new agreement.",
                                  "Payables and operating accruals (including accrued expenses and deferred customer billings) are held constant; receivables and other operating current assets absorb the stated working-capital change. Deferred customer billings are not forecast separately.",
                                  "Other operating current assets comprise prepaid expenses and unbilled contract assets; model movements are explicit, not new EBITDA addbacks.",
                                  "Historical goodwill represents earlier acquisitions and stays constant; fixed/software assets roll by capex less depreciation/amortization.",
                                  ("Restricted cash is custodial client money with an equal segregated-funds liability, excluded from lender collateral, leverage netting and available operating cash." if client_obligation else "Restricted cash is borrower-owned cash reserved by contract for operating performance obligations, not client money; it has no matching client-funds liability and no competing lien. It is excluded from leverage netting and available cash."),
                                  "Forecast negative cash is an unfunded deficit, not an actual bank balance or assumed new loan; such a scenario is infeasible without corrective financing or spending changes.",
                                  "Cash tax is 25% of positive pretax income, with no loss benefit or deferred-tax complexity.",
                                  "Q1 realizations are synthetic, with no assumed submission timestamp; every actual delivery obligation must be tested separately.",
                                  "Annual interest uses ACT/365F; principal installments are effective December 31, so within-year principal is constant."]}


def optional_clause(p):
    typ, value = p["optional_type"], p["optional_threshold"]
    if typ == "none":
        return None
    if typ == "liquidity":
        return {"id": "C09", "title": "Minimum operating cash and early cash forecast", "resolution": "F / R",
                "clause": f"At each month-end beginning January 31, 2027, Eligible Cash shall be at least {money(value)}. Equality passes. If month-end Eligible Cash is at or below {money(p['liquidity_trigger_m'])}, Borrower shall deliver within five Business Days one forecast covering the following 91 calendar days in thirteen consecutive seven-day periods, with weekly opening cash, receipts, payroll, taxes, capital investment, interest, principal and closing cash. No intervening weekly update is required. The forecast trigger does not itself breach the cash minimum. Restricted or client funds and undrawn or promised funding are excluded from both measures.",
                "evidence": "Month-end bank balances, account ownership and restrictions, and timestamped 13-week forecast when triggered.", "thesis_ids": ["A3", "A4"]}
    if typ == "interest":
        text = f"At each quarter-end beginning December 31, 2027, Cash Interest Coverage shall be at least {value:.2f}x. Divide same-period trailing-four-quarter Covenant EBITDA by Cash Interest. Cash Interest includes cash contractual interest paid or payable, including overdue amounts, finance-lease interest and recurring financing fees; exclude noncash amortization and capitalized PIK. Floor aggregate Cash Interest at zero. If it is zero, this test passes only with nonnegative Covenant EBITDA. Full-precision equality passes. No principal repayment is represented by this test."
    elif typ == "coverage":
        text = f"At each quarter-end beginning December 31, 2027, Cash Debt-Service Coverage shall be at least {value:.2f}x. Its numerator is trailing-four-quarter Reported EBITDA less cash income taxes paid, cash Capital Investment, and positive operating working-capital investment, counted once. Its denominator is cash interest paid or contractually payable for that period, including overdue interest, plus principal scheduled to fall due in the period, including finance-lease principal. Exclude voluntary principal payments and the final term-loan balloon. Operating working capital is trade receivables plus unbilled contract assets and prepaid operating expenses less trade payables and operating accruals; exclude cash, Debt, interest and taxes. Releases give no numerator uplift. If the denominator is zero, require a nonnegative numerator. Equality passes; the excluded balloon needs a separate funding plan."
    else:
        text = f"Aggregate cash Capital Investment shall not exceed {money(value)} per fiscal year beginning 2027 without prior written lender consent. Include equipment, capitalized software development and capitalized operating infrastructure once each. Exclude acquisition consideration tested under C05 and costs already expensed in Reported EBITDA. There is no carryforward, carryback, proceeds netting, or automatic insurance exception. Budget approval is not lender consent. Test at each cash payment; the payment exceeding the annual basket is restricted."
    return {"id": "C09", "title": {"interest": "Minimum cash interest coverage", "coverage": "Minimum cash debt-service coverage", "capex": "Annual capital investment envelope"}[typ],
            "clause": text, "resolution": "X" if typ == "capex" else "F",
            "evidence": "Same-period financial, debt-service and investment schedules reconciled to the signed certificate; actual spending dates for a capital limit.", "thesis_ids": ["A3", "A4"]}


def core_clauses(p):
    name = p["name"]
    clauses = [
        ("C01", "Maximum total net leverage", "F", f"{name} shall not permit Total Net Leverage to exceed {p['max_leverage']:.2f}x at any calendar quarter-end beginning March 31, 2027. The numerator is consolidated Debt less min(Eligible Cash, {money(p['cash_netting_cap_m'])}, Debt); the denominator is Covenant EBITDA for the four quarters ending on that date. This is a maintenance test independent of borrowing activity. Equality passes, full precision governs, and no stepdown or automatic equity cure is granted. Positive Net Debt with nonpositive Covenant EBITDA fails; zero Net Debt is defined as zero leverage for this simulation.", "Debt register, qualified cash balances, trailing-four-quarter EBITDA bridge and adjustment support."),
        ("C02", "Financial reporting and compliance certification", "R", f"Borrower shall deliver consolidated quarterly balance sheets, income statements and cash-flow statements and an officer-signed covenant certificate within {p['report_days']} calendar days after each quarter-end, beginning March 31, 2027. Include debt/cash reconciliations, adjustment evidence, policy changes, actual annual and outstanding basket usage, and every elected test. Fourth-quarter management reporting is still required. Annual audited statements and the auditor's report are due within 90 calendar days after year-end, first December 31, 2027; an audit qualification must be disclosed but is not alone a delivery breach. A board-approved monthly annual budget and cash forecast are due within 30 calendar days after each year begins, first 2027. If maturity falls within 18 months, include a documented maturity funding plan. A certificate disclosing failure can satisfy delivery; missing evidence does not establish a ratio failure.", "Statements, signed certificates, support schedules, audit/budget approvals and portal receipt timestamps."),
        ("C03", "Debt and lien limitations", "X / A", f"The Group shall incur no Debt or third-party guarantee except this facility and Loan Party guarantees, and finance leases not exceeding {money(p['lease_basket_m'])} principal outstanding in aggregate. A new lease requires no continuing Default and pro forma leverage no greater than {p['acquisition_max_leverage']:.2f}x. Actual principal repayment releases that outstanding basket; no annual reset applies. Lease security is limited to the financed asset. Other permitted liens are lender security and ordinary statutory liens not overdue or contested in good faith with GAAP reserves and a collection stay protecting Material Collateral. Other financing, PIK, seller notes, earnouts and letters of credit require prior written consent and an amendment defining treatment; no independent unfunded-guarantee basket exists. Voluntarily unauthorized Debt/liens use X; a remediable statutory-lien qualification failure uses A.", "Financing instruments, guarantee register, lease balances and asset schedule, lien searches and contest evidence."),
        ("C04", "Distributions and sponsor leakage", "X", f"Cash dividends to persons outside the Loan Party group shall not exceed {money(p['dividend_basket_m'])} in aggregate per calendar fiscal year and require no continuing Default, pro forma leverage no greater than {p['dividend_max_leverage']:.2f}x and at least {money(p['transaction_cash_floor_m'])} Eligible Cash after payment. No unused capacity carries forward or replenishes after repayment. Equity redemptions, sponsor monitoring fees, and voluntary junior-debt repayments require prior written consent and have no independent basket. Transfers among Loan Parties preserving security do not use the dividend basket. Ordinary employee compensation and payment for documented arm's-length operating services are not dividends, but payments to sponsor affiliates above $0.250m annually require disinterested board approval and pricing support.", "Executed payment evidence, recipient/control identity, annual usage, fair-pricing support and post-payment cash/leverage."),
        ("C05", "Acquisitions and investments", "X", f"Acquisitions within the Permitted Business may be made for aggregate cash consideration including fees not exceeding {money(p['acquisition_basket_m'])} per fiscal year, only with no continuing Default, pro forma leverage at or below {p['acquisition_max_leverage']:.2f}x, and at least {money(p['transaction_cash_floor_m'])} post-closing Eligible Cash. No carryforward, replenishment or transaction splitting is permitted. Historical target earnings must be verified under the same EBITDA definition; assumed Debt separately needs C03 permission. Contingent consideration and seller financing need prior consent. Other investments require prior written consent except ordinary bank deposits, trade receivables, and transfers between Loan Parties preserving security. An acquired subsidiary consolidates at control acquisition and must accede under C07; its cash is not Eligible Cash until it qualifies as a Loan Party. A proposal that has not closed is not an executed breach.", "Signed purchase/investment documents, related consideration, financing, historical target financials, group chart and accession records."),
        ("C06", "Business scope and asset protection", "X", f"The Group shall remain within the Permitted Business and may sell obsolete equipment at fair value only up to {money(p['asset_sale_basket_m'])} aggregate fair value per fiscal year, without carryforward or recycling. No receivables sale, material operating asset transfer, ownership transfer or exclusive license of Core IP outside the Loan Party group is permitted without prior written consent. Nonexclusive ordinary customer-use licenses and transfers between Loan Parties preserving security are permitted. Sale receipts must be paid to a Loan Party and may then fund ordinary operations, independently permitted transactions or Debt repayment; there is no additional proceeds sweep. A change in customer cancellation rights or permitted revenue mix is not automatically a business-scope breach. The sector-specific S clauses apply independently.", "Executed asset/IP documents, rights conveyed, fair values, business activities, recipient identity, annual usage and proceeds."),
        ("C07", "Existence insurance guarantees and collateral", "A / R / X", "Loan Parties shall preserve existence, maintain books and required operating assets, and pay taxes when due except amounts contested in good faith with GAAP reserves and a stay against sale of Material Collateral. Maintain property coverage at replacement cost for tangible Material Collateral, general liability of $2m per occurrence/$4m aggregate, and technology or professional liability plus cyber coverage of $5m aggregate per policy year, with deductibles no greater than $0.250m; lender shall be loss payee or additional insured where applicable. Renewal certificates are due five Business Days after renewal (R); restoring coverage remedies a lapse prospectively under A, preserving its history and uninsured losses. New domestic subsidiaries must guarantee the facility and deliver security accessions within ten Business Days of control acquisition, and complete perfection on existing assets and equity within 30 calendar days of that date. Other uncovered newly acquired assets require executed instruments within fifteen Business Days and perfection within 30 calendar days. Foreign subsidiaries, unrestricted designations and reorganizations outside a merger into a surviving Loan Party preserving guarantees/security require prior consent (X). Permit relevant lender inspection on five Business Days' notice, at borrower expense twice annually absent Default (R).", "Entity records, policies and endorsements, tax contest/stay, signed guarantees, actual filings/control evidence and access requests."),
        ("C08", "Default and material customer notices", "R", f"Within five Business Days of the earliest actual knowledge of the CEO, CFO or general counsel, Borrower shall notify lender of any contractual noncompliance and of an actual written termination or nonrenewal notice from a customer group accounting for at least {p['customer_notice_threshold_pct']}% of prior fiscal-year consolidated revenue. Aggregate customer affiliates under common control at receipt, counting revenue once. Include facts, knowledge and effective dates, exposure, and proposed mitigation. An executed grant of a cancellation right without an actual termination/nonrenewal notice does not alone trigger the customer-notice limb. Reporting does not cure another covenant. More specific notices under S1–S3 remain independently applicable.", "Actual underlying notice/event, officer knowledge evidence, customer-group revenue, delivered lender notice and timestamp.")]
    return [{"id": i, "title": t, "resolution": res, "clause": text, "evidence": ev,
             "thesis_ids": [a["id"] for a in p["assumptions"] if i in a["covenant_links"]]} for i, t, res, text, ev in clauses]


def definitions(p):
    return f"""**Group and Loan Parties.** Borrower and its two wholly owned domestic subsidiaries, {p['subsidiaries'][0]} and {p['subsidiaries'][1]}, are the only opening Group members and Loan Parties. Both subsidiaries guarantee all facility obligations. Consolidate and eliminate intercompany balances. Newly controlled subsidiaries consolidate immediately, even before guarantee accession. No unrestricted subsidiaries, outside guarantees or opening lease Debt exist. Control means power to direct management through voting rights, contract or otherwise; affiliate means control or common control. Lender security covers only Loan Party beneficial property; third-party client or custodial funds are expressly excluded from collateral, lender-benefit deposit control and operating resources.

**Permitted Business and Core IP.** Permitted Business is {p['sector'].lower()} and activities reasonably related to delivering the products and services described in the business schedule below. Relatedness depends on actual customers, products, capabilities and operating resources. Core IP is source code, operating documentation, proprietary datasets, marks and rights essential to that business. Material Collateral is any asset necessary to continue core service delivery, or other assets with aggregate fair value over $0.500m. These definitions do not turn business forecasts into covenants.

**Debt and Cash.** Debt includes funded borrowings, finance-lease principal, capitalized PIK, unreimbursed letter-of-credit drawings and funded guarantee obligations currently payable, without consolidated double counting. Exclude ordinary non-interest-bearing trade payables and operating leases. Permission to incur remains governed by C03. Eligible Cash is unrestricted USD cash owned by a Loan Party in a U.S. bank account, immediately accessible for debt service and subject to no security other than the lender's. Exclude client, trust, escrow, restricted, blocked and foreign-subsidiary cash. Leverage netting is capped at {money(p['cash_netting_cap_m'])} and Debt; transaction tests also exclude unspent proceeds of the Debt being incurred. A cash minimum, if elected, is uncapped.

**Earnings and investment.** Reported EBITDA is consolidated U.S. GAAP net income plus interest expense, income-tax expense, depreciation and amortization. Covenant EBITDA adds only documented cash restructuring costs deducted in Reported EBITDA, capped at {p['ebitda_cap_pct']}% of positive Reported EBITDA, and subtracts included nonoperating disposal gains. There are no forecast-synergy, stock-compensation, ordinary recurring-cost or other adjustments. Research costs follow GAAP; qualifying capitalized software development is amortized over three years when available for use. Capital Investment includes all cash equipment and capitalized development spending once, excluding acquisition consideration and already-expensed items. Reconcile policy changes to the closing basis. The closing adjustment is {money(p['adjustment_m'])}; its supporting restructuring expense is already in Reported EBITDA and must not be deducted twice in cash flow.

**Testing and pro forma calculations.** Quarter-end Debt/cash uses that date; earnings use the four then-ended fiscal quarters. No automatic annualization. For a proposed transaction, adjust debt/cash and historical earnings for the complete transaction and related steps, using verified target earnings for the same four-quarter period, eliminating overlap and disposed earnings. No forecast savings. Missing inputs mean permission is unestablished, not presumed. Compare unrounded values; displayed figures are rounded only for readability.

**Calendar and delivery.** New York time; Business Days exclude weekends and observed U.S. federal holidays. Exclude the triggering day. Calendar-day delivery and post-closing administrative-performance deadlines roll forward to the next Business Day; measurements do not. Delivery requires the lender's designated reporting portal timestamp by 5 p.m.; later receipts count on the next Business Day. Contractual interest and principal dates do not roll: if not a Business Day, prefund lender by the preceding Business Day for credit on the contractual date, with no interest extension. The financial schedules model the contractual credit date; prefunded amounts are unavailable cash until applied.

**Consent and baskets.** All amendments and waivers require a written instrument signed by the sole lender and Borrower, identifying affected terms/periods, effective date and conditions. Prior transaction consent requires the lender's written approval before execution. No-default conditions apply only where stated and include unremedied failures during a grace period. Annual baskets reset January 1; no carryforward, reclassification, replenishment or splitting unless expressly allowed. Outstanding baskets free capacity only upon actual principal repayment. An internal budget, unsigned draft or sponsor funding intention is not consent or received cash."""


def statement_table(model):
    y = model["history"]["2026"]
    b = y["closing_balance_sheet"]
    i = y["income_statement"]
    eb = y["ebitda_reconciliation"]
    rows = [("Revenue", i["revenue_m"]), ("Reported EBITDA", i["reported_ebitda_m"]),
            ("Documented permitted restructuring adjustment", eb["permitted_adjustment_m"]),
            ("Covenant EBITDA", eb["covenant_ebitda_m"]), ("Opening term Debt", b["funded_term_debt_m"]),
            ("Eligible operating cash", b["cash_or_unfunded_deficit_m"]), ("Restricted/client cash excluded", b["restricted_cash_m"])]
    return "| Closing financial schedule | USD millions |\n| --- | ---: |\n" + "\n".join(f"| {k} | {v:.3f} |" for k, v in rows)


def build_contract(p, model, clauses):
    maturity = model["maturity_funding"]
    amort = p["debt_m"] * p["amortization_pct"] / 100
    restricted_text = ("are client-owned custodial balances with an equal segregated-funds obligation, expressly outside lender collateral" if p["restricted_cash_type"] == "custodial_client_funds" else "are borrower-owned performance-reserve deposits subject to contractual withdrawal restrictions, with no matching client-funds liability or competing lien")
    clause_text = "\n\n".join(f"### {c['id']} {c['title']}\n\n{c['clause']}\n\nEvidence required: {c['evidence']} Resolution category: {c['resolution']}." for c in clauses)
    return f"""# {p['name']} Senior Secured Credit Agreement

Agreement {p['id']}-CA-2026-01, version 1.0. Synthetic execution, effective and known-at date: December 31, 2026. All entities, terms and events are fictional and operative only within this simulation. This is an individually selected contract, not a menu of unelected clauses. No real signature or practitioner validation is represented.

## Parties and financing terms

{p['name']} (Borrower), a Delaware entity, and {p['lender']} (sole Lender and collateral beneficiary) enter into the following simulated agreement. {p['sponsor']} controls Borrower but provides no funding guarantee. The two subsidiaries named in the definitions are guarantors and collateral grantors.

Lender advances {money(p['debt_m'])} at par on December 31, 2026, solely to refinance equal-principal predecessor operating-company debt. Sources and uses are equal; no incremental operating cash, closing fee or original-issue discount is assumed. Interest is fixed at {p['annual_rate_pct']:.2f}% per annum, actual days/365, on outstanding principal, payable each March 31, June 30, September 30 and December 31 beginning March 31, 2027. No PIK election, revolver or further commitment exists. Scheduled principal is {money(amort)} each December 31 from 2027 through {int(maturity['date'][:4]) - 1}; the remaining {money(maturity['balloon_m'])} falls due on {maturity['date']}. Voluntary prepayment at par is permitted on three Business Days' notice with accrued interest; it reduces the final balloon before scheduled installments and creates no reborrowing right. No prepayment premium or default-rate increase is imposed.

The collateral package is first-priority security over Loan Party beneficial assets, subject only to C03 permitted liens and the express exclusion of third-party client funds. Executed guarantees/security, required UCC and applicable IP filings, control over Eligible Cash accounts, evidence of borrower authorization and permitted insurance, and a signed opening Debt/cash/EBITDA schedule are closing conditions. The simulation assumes these conditions satisfied; filing jurisdictions and executed instruments must accompany a real documentary evaluation of perfection. There are no undisclosed post-closing deliverables or assumed third-party guarantees.

## Business and opening schedules

{p['description']}

{statement_table(model)}

Ownership: Borrower owns 100% of each named subsidiary; the sponsor controls Borrower. Debt schedule: this facility only. Permitted existing liens: lender security only. Restricted funds of {money(p['restricted_cash_m'])} {restricted_text}; they are excluded from repayment resources and receive no netting benefit. The financial model separately reconciles assets, liabilities, equity, earnings and cash movements; that model's projections do not modify this contract.

## Definitions and conventions

{definitions(p)}

## Covenants

{clause_text}

## Defaults waivers and remedies

`F`: failure of a financial maximum/minimum at its measurement time is an Event of Default, without automatic numerical grace or equity cure. `R`: a missed reporting/access requirement is noncompliance when due, becoming an Event of Default only if still unremedied at the close of ten Business Days after written lender notice. `A`: a remediable affirmative failure becomes an Event of Default if still unremedied at the close of 30 calendar days after written lender notice; an expressly irremediable failure is immediate. Restoration of insurance remedies ongoing coverage, preserving the historical gap. `X`: an executed prohibited transaction without required permission is an immediate Event of Default; a proposal is not execution. Clauses with two categories apply each to the specified duty. Nonpayment of principal when due is an Event of Default; unpaid interest has three Business Days after its contractual due date. A materially false signed compliance statement is an Event of Default if knowingly false when signed; incompleteness alone is treated under the reporting duty.

While an Event of Default continues, Lender may accelerate outstanding principal and accrued interest by written declaration delivered to Borrower. A waived or timely remedied failure does not support new acceleration. Enforcement of collateral requires separate action under the governing security documents and applicable law; neither a failed ratio nor a software output itself carries out enforcement. No unrelated-agreement cross-default or subjective material-adverse-change default is added by this synthetic agreement. Apply a signed waiver only to its specified obligation, period and conditions; retain the original test and missed dates. No covenant can be inferred from an underwriting belief.

New York law governs the simulated contractual relationship, subject to applicable mandatory law and the law governing asset perfection. Notices go to the parties' designated reporting portal; administrative notices require receipt evidence. This writing and identified signed amendments are the complete operative synthetic terms. No implied basket, cure, consent, sponsor commitment or lender commitment exists outside them.

## Authoring provenance and limitations

Every number and sentence above is authored synthetic content. Structural references: framework M1 (Artivion/Ares, January 18, 2024, §6.7) for leverage and negotiated restriction structure; M3 (Evolent/Ares, December 30, 2019, §§8.01 and 9.12) for reporting and business scope; M4 (NN/Oaktree, March 28, 2025 amendment §2(c), restating §7.14(b)) only where a cash-forecast trigger is elected. S1–S3 are entirely synthetic borrower-specific provisions. See the portfolio source register for direct links and limitations. No agreement supplies market-median values for this borrower. Source-informed drafting, financial arithmetic checks and internal AI review do not establish legal enforceability or practitioner comparability.
"""


def optional_result(p, row, measurement_date):
    typ, threshold = p["optional_type"], p["optional_threshold"]
    if typ == "none":
        return {"applicability": "not_elected", "summary": "Not elected"}
    if typ in {"interest", "coverage"} and measurement_date < "2027-12-31":
        return {"applicability": "not_yet_due", "first_test": "2027-12-31", "summary": "Not yet due"}
    if typ == "liquidity":
        metric = row["metrics"]["eligible_cash_m"]
        triggered = metric <= p["liquidity_trigger_m"]
        return {"applicability": "applicable_at_this_month_end", "metric_m": metric, "minimum_m": threshold,
                "minimum_complies": metric >= threshold, "forecast_triggered": triggered,
                "forecast_due_if_triggered": bd_after(date.fromisoformat(measurement_date), 5).isoformat() if triggered else None,
                "other_months": "Not determined from this measurement alone",
                "summary": f"Cash {metric:.3f}m: {'floor passes' if metric >= threshold else 'floor fails'}; {'forecast triggered' if triggered else 'no forecast trigger'}"}
    if typ == "capex":
        metric = row["cash_flow"]["capital_investment_m"]
        return {"applicability": "applicable_to_fiscal_year_spending_to_date", "spent_m": metric, "annual_cap_m": threshold,
                "complies": metric <= threshold, "summary": f"Spend {metric:.3f}m / cap {threshold:.3f}m: {'passes' if metric <= threshold else 'fails'}"}
    metric = row["metrics"]["interest_coverage_x" if typ == "interest" else "cash_coverage_x"]
    return {"applicability": "applicable", "metric_x": metric, "minimum_x": threshold,
            "complies": metric >= threshold,
            "summary": f"{metric:.3f}x / min {threshold:.2f}x: {'passes' if metric >= threshold else 'fails'}"}


def optional_calibration(p, model):
    typ, threshold = p["optional_type"], p["optional_threshold"]
    base = model["2027_scenarios"]["base"]
    if typ == "none":
        return "No separate C09 financial test is elected."
    if typ == "liquidity":
        return f"Opening cash headroom above the {money(threshold)} floor is {money(p['cash_m'] - threshold)}; cash at or below {money(p['liquidity_trigger_m'])} activates reporting before or at a possible floor failure. These are chosen cash-risk parameters, not market standards."
    if typ == "capex":
        return f"The annual cap of {money(threshold)} exceeds planned {money(p['capex_m'])} Capital Investment by {money(threshold - p['capex_m'])}, or {(threshold / p['capex_m'] - 1):.2%}."
    interest = base["income_statement"]["cash_interest_paid_m"]
    base_e = base["income_statement"]["reported_ebitda_m"]
    if typ == "interest":
        boundary = threshold * interest
        return f"At the first-test annual base interest of {money(interest)}, the {threshold:.2f}x coverage boundary is Covenant EBITDA of {money(boundary)}, {(1 - boundary / base_e):.2%} below the base forecast with no 2027 addback. This sensitivity holds interest fixed."
    denominator = interest + base["cash_flow"]["scheduled_principal_paid_m"]
    # Positive-tax branch follows the declared 25% cash-tax rule; below the tax
    # threshold no tax benefit is generated.
    untaxed_boundary = threshold * denominator + p["capex_m"] + p["working_capital_investment_m"]
    boundary = untaxed_boundary if untaxed_boundary <= p["da_m"] + interest else (untaxed_boundary - .25 * (p["da_m"] + interest)) / .75
    return f"With base interest, principal, investment and working-capital use held fixed and cash tax recalculated under the declared 25% rule, the {threshold:.2f}x coverage boundary is Reported EBITDA of {money(boundary)}, {(1 - boundary / base_e):.2%} below the first-test annual base. This is a cash-flow sensitivity, not the leverage boundary."


def model_summary(p, model):
    opening = model["history"]["2026"]["metrics"]
    ce0 = model["history"]["2026"]["ebitda_reconciliation"]["covenant_ebitda_m"]
    boundary = opening["net_debt_m"] / p["max_leverage"]
    h = 1 - boundary / ce0
    lines = ["| Scenario at December 31 2027 | Reported EBITDA | Covenant EBITDA | Cash or deficit | Debt | Net leverage | Selected C09 outcome |",
             "| --- | ---: | ---: | ---: | ---: | ---: | --- |"]
    for key, scenario in model["2027_scenarios"].items():
        i, b, m = scenario["income_statement"], scenario["closing_balance_sheet"], scenario["metrics"]
        optional = optional_result(p, scenario, "2027-12-31")
        lines.append(f"| {key.title()} projection | {i['reported_ebitda_m']:.3f} | {scenario['ebitda_reconciliation']['covenant_ebitda_m']:.3f} | {b['cash_or_unfunded_deficit_m']:.3f} | {b['funded_term_debt_m']:.3f} | {m['leverage_x']:.3f}x ({'passes' if m['leverage_x'] <= p['max_leverage'] else 'fails'}) | {optional['summary']} |")
    return f"Opening net leverage is {opening['leverage_x']:.3f}x against {p['max_leverage']:.2f}x. At fixed opening Net Debt of {money(opening['net_debt_m'])}, Covenant EBITDA reaches the boundary at {money(boundary)}, a {h:.2%} decline from {money(ce0)}. This is earnings-decline capacity, not the percentage increase in the ratio.\n\n" + "\n".join(lines) + "\n\n" + optional_calibration(p, model)


def build_underwriting(p, model):
    assets = model["history"]["2026"]["closing_balance_sheet"]
    asset_note = f"The authored balance sheet records trade receivables of {money(assets['trade_receivables_m'])} at {p['receivable_days']} collection days, other operating current assets of {money(assets['other_operating_current_assets_m'])}, net fixed/software assets of {money(assets['fixed_and_capitalized_software_assets_net_m'])}, and historical acquisition goodwill of {money(assets['historical_goodwill_m'])}. These are book balances, not collateral recovery estimates. See the model's explicit prepaid/unbilled and deferred-billing simplifications."
    parts = [f"# {p['name']} Underwriting memorandum", f"Memo {p['id']}-UW-2026-01. Synthetic approval and availability: {ASOF}. Proposed for a private-credit analyst. Dollar amounts are millions. Future scenarios are forecasts known at origination, not later observations.",
             "## Borrower and credit decision", p["description"], p["credit_rationale"],
             "## Four approved synthetic underwriting assumptions", "Baseline evidence descriptions below are authored source summaries within this simulated approved memo. Original bank statements, system exports and historical customer agreements are not separately reproduced unless explicitly supplied as evidence files. Treat these summaries as baseline memo evidence, not as independently inspected original records."]
    for a in p["assumptions"]:
        parts.append(f"### {a['id']}\n\n**Claim:** {a['statement']}\n\n**Baseline evidence:** {a['evidence']}\n\n**Review criterion:** {a['review_trigger']}\n\n**Contract relationship:** {a['protection']}; {', '.join(a['covenant_links']) or 'no direct covenant'}. These links describe possible protection and do not add a covenant.")
    parts += ["## Financial calibration", statement_table(model), model_summary(p, model),
              "## Optional protections selected and omitted",
              f"Selected optional family: **{p['optional_type']}**. The agreement includes C09 only for the selected family. No other liquidity, interest-coverage, cash-coverage or capex test is silently elected. No springing revolver or revenue-based test applies; this profitable borrower has a cash-flow term facility. S1–S3 address its particular operating risks. Omitted financial families avoid duplicating controls unless supported by a separate credit rationale and signed amendment.",
              "## Repayment and maturity", f"Annual principal before maturity is {money(p['debt_m'] * p['amortization_pct'] / 100)}. The final balloon is {money(model['maturity_funding']['balloon_m'])}. In the stated base forecast, cash before the balloon is {money(model['maturity_funding']['base_cash_before_balloon_m'])}; after preserving {money(model['maturity_funding']['operating_reserve_m'])} operating cash, uncommitted refinancing or equity needed is {money(model['maturity_funding']['refinancing_or_equity_needed_m'])}. No refinancing commitment or sponsor support is assumed. This result depends on the disclosed growth, no-distribution and no-acquisition assumptions and is not a prediction.",
              "## Financial model conventions", asset_note, "\n".join(f"- {s}" for s in model["model_conventions"]),
              "## Evidence boundary", "The financial model's 2027 cases and maturity projection are origination forecasts. Q1 2027 reporting and the June event are separate future documents with their own availability dates. Do not load those documents into an origination assessment. Ground truth lives only in the evaluator directory."]
    return "\n\n".join(parts)


def validate_company(p, model, clauses):
    assert len(p["specialized_covenants"]) == 3 and len(p["assumptions"]) == 4
    assert {c["id"] for c in p["specialized_covenants"]} == {"S1", "S2", "S3"}
    assert {a["id"] for a in p["assumptions"]} == {"A1", "A2", "A3", "A4"}
    ids = {c["id"] for c in clauses}
    for a in p["assumptions"]:
        assert set(a["covenant_links"]) <= ids, (p["id"], "undefined assumption link", a)
    assert set(p["event"]["evaluated_clause_ids"]) <= ids
    assert set(p["event"]["affected_assumption_ids"]) <= {"A1", "A2", "A3", "A4"}
    opening = model["history"]["2026"]
    base = model["2027_scenarios"]["base"]
    assert p["adjustment_m"] <= p["ebitda_m"] * p["ebitda_cap_pct"] / 100 + 1e-9
    assert 0 < p["cash_netting_cap_m"] <= p["cash_m"]
    assert p["transaction_cash_floor_m"] < p["cash_m"]
    assert opening["metrics"]["leverage_x"] < p["max_leverage"]
    assert opening["metrics"]["leverage_x"] <= p["dividend_max_leverage"] < p["max_leverage"], (p["id"], "dividend calibration")
    assert opening["metrics"]["leverage_x"] <= p["acquisition_max_leverage"] <= p["max_leverage"]
    assert base["metrics"]["leverage_x"] <= p["max_leverage"], (p["id"], "base leverage")
    assert base["closing_balance_sheet"]["cash_or_unfunded_deficit_m"] > 0, (p["id"], "base cash")
    typ, value = p["optional_type"], p["optional_threshold"]
    if typ == "liquidity":
        assert 0 < value < p["liquidity_trigger_m"] < p["cash_m"]
        assert base["metrics"]["eligible_cash_m"] >= value
    elif typ == "interest":
        assert base["metrics"]["interest_coverage_x"] >= value
    elif typ == "coverage":
        assert base["metrics"]["cash_coverage_x"] >= value, (p["id"], "cash coverage", base["metrics"]["cash_coverage_x"], value)
    elif typ == "capex":
        assert p["capex_m"] < value
    else:
        assert typ == "none" and value is None
    checks = [opening, model["q1_2027"], *model["2027_scenarios"].values(), *[x["projection"] for x in model["base_projection_to_prematurity"]]]
    for row in checks:
        inc, b, cf = row["income_statement"], row["closing_balance_sheet"], row["cash_flow"]
        assert abs(b["balance_check_m"]) < 1e-8, (p["id"], "balance")
        total = sum(b[k] for k in ("cash_or_unfunded_deficit_m", "restricted_cash_m", "trade_receivables_m", "other_operating_current_assets_m", "fixed_and_capitalized_software_assets_net_m", "historical_goodwill_m"))
        assert abs(total - b["total_assets_m"]) < 1e-8
        assert abs(total - b["total_liabilities_m"] - b["equity_m"]) < 1e-8
        assert b["other_operating_current_assets_m"] >= 0 and b["fixed_and_capitalized_software_assets_net_m"] >= 0
        assert abs(cf["opening_cash_m"] + cf["net_cash_change_m"] - cf["closing_cash_or_unfunded_deficit_m"]) < 1e-8
        assert abs(inc["revenue_m"] - inc["cash_operating_expenses_m"] - inc["reported_ebitda_m"]) < 1e-8
    return {"borrower_id": p["id"], "clause_count": len(clauses), "opening_leverage_x": opening["metrics"]["leverage_x"],
            "opening_ebitda_decline_capacity_pct": 100 * (1 - opening["metrics"]["leverage_x"] / p["max_leverage"]),
            "base_leverage_x": base["metrics"]["leverage_x"], "statement_checks": len(checks),
            "q1_reporting_due": roll(date(2027, 3, 31) + timedelta(days=p["report_days"])).isoformat(),
            "severe_unfunded_cash_need_m": model["2027_scenarios"]["severe"]["metrics"]["unfunded_cash_need_m"],
            "status": "arithmetic and record checks passed"}


def main():
    companies = []
    for file in sorted(AUTHOR.glob("batch_*.json")):
        companies.extend(json.loads(file.read_text(encoding="utf-8-sig")))
    companies.sort(key=lambda p: p["id"])
    assert [p["id"] for p in companies] == [f"B{i:02}" for i in range(1, 31)], "Need exactly B01-B30"
    assert len({p["name"] for p in companies}) == 30
    all_special = [c["clause"] for p in companies for c in p["specialized_covenants"]]
    assert len(set(all_special)) == 90, "Specialized provisions must be individually authored"
    index_rows, manifest, answers, qa = [], [], [], []
    for p in companies:
        p["restricted_cash_type"] = "custodial_client_funds" if p["id"] in {"B03", "B12", "B24", "B28"} else "borrower_owned_performance_reserve"
        model = make_model(p)
        clauses = core_clauses(p)
        optional = optional_clause(p)
        if optional:
            clauses.append(optional)
        clauses.extend(p["specialized_covenants"])
        result = validate_company(p, model, clauses)
        qa.append(result)
        slug = p["id"] + "-" + re.sub(r"[^a-z0-9]+", "-", p["name"].lower()).strip("-")
        folder = INPUT / slug
        contract = build_contract(p, model, clauses)
        write(folder / "credit-agreement.md", contract)
        write(folder / "underwriting-memo.md", build_underwriting(p, model))
        public_model = {k: v for k, v in model.items() if k != "q1_2027"}
        dump(folder / "origination-financial-model.json", public_model)
        contract_record = {"borrower_id": p["id"], "borrower": p["name"], "agreement_id": p["id"] + "-CA-2026-01",
                           "version": "1.0", "executed_at": ASOF, "effective_at": ASOF, "known_at": ASOF, "synthetic": True,
                           "lender": p["lender"], "sponsor": p["sponsor"], "sector": p["sector"],
                           "definitions_and_conventions": definitions(p), "optional_family": p["optional_type"],
                           "clauses": clauses, "complete_agreement_text": contract,
                           "assumptions": p["assumptions"], "ground_truth_included": False}
        dump(folder / "contract-record.json", contract_record)
        dump(folder / "future-evidence" / "2027-06-01-q1-financials.json", model["q1_2027"])
        event = p["event"]
        evtext = f"# {p['name']} {event['document_title']}\n\nSynthetic document {p['id']}-EV-2027-01. Event date: {event['event_date']}. Available to analyst: {event['available_at']}.\n\n" + "\n\n".join(f"## {x['id']}\n\n{x['text']}" for x in event["source_passages"])
        write(folder / "future-evidence" / "2027-06-16-operating-event.md", evtext)
        answer = {"borrower_id": p["id"], "review_date": event["review_date"],
                  "event_source": f"{slug}/future-evidence/2027-06-16-operating-event.md",
                  "source_spans": [x["id"] for x in event["source_passages"]],
                  **{k: v for k, v in event.items() if k.startswith("expected_") or k in ("rationale", "affected_assumption_ids", "evaluated_clause_ids")},
                  "q1_financial_result": {"measurement_date": "2027-03-31", "known_at": "2027-06-01",
                                          "leverage_x": model["q1_2027"]["metrics"]["leverage_x"], "maximum_x": p["max_leverage"],
                                          "leverage_complies": model["q1_2027"]["metrics"]["leverage_x"] <= p["max_leverage"],
                                          "selected_C09": optional_result(p, model["q1_2027"], "2027-03-31"),
                                          "certificate_delivery_result": "insufficient_evidence: availability to analyst is not a lender submission receipt"},
                  "reviewer_status": "Authored development answer; internal review, not practitioner adjudication"}
        answers.append(answer)
        files = ["credit-agreement.md", "contract-record.json", "underwriting-memo.md", "origination-financial-model.json"]
        manifest.append({"id": p["id"], "name": p["name"], "sector": p["sector"], "directory": slug,
                         "origination_files": files, "origination_available_at": ASOF,
                         "future_evidence": [{"file": "future-evidence/2027-06-01-q1-financials.json", "available_at": "2027-06-01"},
                                             {"file": "future-evidence/2027-06-16-operating-event.md", "available_at": event["available_at"]}],
                         "clause_count": len(clauses), "specialized_titles": [c["title"] for c in p["specialized_covenants"]]})
        index_rows.append(f"| {p['id']} | [{p['name']}](model_inputs/{slug}/credit-agreement.md) | {p['sector']} | {p['debt_m']:.1f} | {result['opening_leverage_x']:.2f}x / {p['max_leverage']:.2f}x | {p['specialized_covenants'][0]['title']} |")
        saved = json.loads((folder / "contract-record.json").read_text(encoding="utf-8"))
        assert saved["complete_agreement_text"].rstrip() == (folder / "credit-agreement.md").read_text(encoding="utf-8").rstrip()
        for c in clauses:
            assert c["clause"] in contract
        assert "expected_contract_result" not in json.dumps(saved)
    dump(ROOT / "manifest.json", {"schema_version": "1.0", "synthetic": True, "borrower_count": 30, "companies": manifest})
    dump(EVAL / "answers.json", answers)
    dump(ROOT / "validation-report.json", {"borrower_count": 30, "individually_authored_specialized_clauses": 90,
                                          "distinct_contracts": 30, "total_contractual_clauses": sum(r["clause_count"] for r in qa),
                                          "checked_financial_statements": sum(r["statement_checks"] for r in qa), "companies": qa})
    write(EVAL / "README.md", "# Evaluator material\n\nDo not put this directory or authoring/ into an inference prompt. answers.json contains authored expected answers for the dated June 2027 events and separately calculated Q1 leverage results. Availability is not proof of lender delivery. Outcomes apply to identified clauses only, not blanket compliance. These are development cases, not a held-out performance benchmark. All documents are synthetic; practitioner adjudication remains outstanding.")
    write(ROOT / "README.md", "# Thirty synthetic borrowers and their individual credit agreements\n\nThis portfolio corrects the earlier 30-clause interpretation: it contains **30 different profitable U.S. software or business-services companies, each with its own standalone specialized credit agreement**. Each contract selects 8 core duties, 3 individually authored operating covenants, and at most one optional financial family. The library is source-informed synthetic drafting; all names, figures, contracts and events are fictional.\n\n## Company index\n\nAmounts are USD millions. Leverage column shows opening ratio / contractual maximum.\n\n| ID | Individual agreement | Business | Term loan | Leverage | One tailored protection |\n| --- | --- | --- | ---: | --- | --- |\n" + "\n".join(index_rows) + "\n\n## What each company includes\n\n- A standalone credit agreement with selected terms, definitions, collateral/guarantees, reporting, transaction restrictions, three specialized operating covenants, defaults and remedies.\n- An underwriting memo with four company-specific assumptions, contract relationships, calibrations and base/downside scenarios.\n- A financial model reconciling income, cash movements, debt, balance sheets, EBITDA adjustments and maturity funding; historical 2025 comparatives and 2026 statements are separate from 2027 projections.\n- A structured contract record with exactly the same agreement text.\n- Two separately dated future evidence files: Q1 financial data and a company-specific June operating event.\n\n## Use the timeline correctly\n\nAt origination use only each manifest entry's origination_files. Forecasts known at origination may be used as forecasts. Add future-evidence files only when available_at is no later than the review date. The quarter-end date is not a receipt date. Never load evaluator/ or authoring/ into the model being tested. Do not treat the June operating event as a complete compliance certificate or infer a new financial ratio from qualitative evidence.\n\n## Scope and review status\n\nContracts are individually tailored covenant-focused simulated agreements, not production legal forms. The facility structure is deliberately restricted to sole-lender secured cash-flow term loans; no revolver, revenue-based pre-profitability loan, automatic equity cure, or undisclosed basket is assumed. Within that structure the companies differ in business economics, cash accessibility, earnings adjustments, leverage protection, amortization, tenor, pricing, reporting deadlines, transaction permissions and sector duties. Shared drafting is repeated inside every contract so no borrower depends on another borrower's definitions.\n\nThe financial checks verify arithmetic and consistency, not business forecasts or market comparability. All ordinary insurance limits, same-quarter accounting allocations and simplified tax assumptions are disclosed synthetic choices. No legal enforceability, OCC approval, practitioner validation or measured model performance is claimed. Source links are in [SOURCE-REGISTER.md](SOURCE-REGISTER.md). Authoring files and the runnable validation script are retained for reproducibility; the downloadable ZIP includes deliverables and evaluator material, excluding authoring internals.\n")
    source = """# Source register and design lineage

Authoring date September 19, 2026. The local Synthetic-Covenant-Framework.md is the agreed design authority. Each new borrower has an independent agreement identifier; the earlier CedarBridge 30-clause library is supporting material, not one of these 30 agreements.

| Reference | Historical source and locator | Applied structure and limitation |
| --- | --- | --- |
| M1 | [Artivion / Ares January 18 2024 agreement](https://www.sec.gov/Archives/edgar/data/784199/000095015724000061/ex10-1.htm), §6.7; restrictions §§6.1–6.8 | Maintenance leverage and negotiated permission structure. Borrower-specific amounts, ratios, exceptions and all prose here are synthetic; source industry is not a software pricing peer. |
| M3 | [Evolent / Ares December 30 2019 agreement](https://www.sec.gov/Archives/edgar/data/1628908/000162890819000084/exhibit101passportcredit.htm), §8.01 and §9.12 | Reporting and permitted business scope. Selected deadlines and substantive borrower protections remain synthetic. |
| M4 | [NN / Oaktree March 28 2025 sixth amendment](https://www.sec.gov/Archives/edgar/data/918541/000091854125000041/exhibit101termloansixthame.htm), amendment §2(c), restated §7.14(b) | Conditional 13-week cash reporting for liquidity profiles only. Original quarterly leverage/liquidity trigger is not copied; this portfolio's month-end trigger is an adapted design. |
| OCC design principles | [Commercial Loans](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/commercial-loans/pub-ch-commercial-loans.pdf), pp.14–15,20; [Leveraged Lending](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/leveraged-lending/pub-ch-leveraged-lending.pdf), pp.15,59–60,62,64 | Cash repayment analysis, reporting and definition-sensitive headroom. No numerical private-credit covenant requirement is attributed to OCC. See the existing framework for dated regulatory source-status research. |

These are historical operating-company loan sources, not complete current amendment chains. The source locators were checked in the preceding framework/library work; this generation introduces no new market-practice or law claim. Adapted structure applies to core financial/reporting restrictions and elected liquidity reporting. All S1–S3 sector provisions and all borrower names, facts, economics, events and contractual wording are entirely synthetic. The 30 contracts share no real borrower confidential data.
"""
    write(ROOT / "SOURCE-REGISTER.md", source)
    archive = ROOT.parent / "Thirty-Synthetic-Companies-and-Credit-Agreements.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for folder in (INPUT, EVAL):
            for path in sorted(folder.rglob("*")):
                if path.is_file():
                    z.write(path, path.relative_to(ROOT))
        for filename in ("README.md", "manifest.json", "SOURCE-REGISTER.md", "validation-report.json"):
            z.write(ROOT / filename, filename)
    print(json.dumps({"companies": 30, "contracts": 30, "specialized_clauses": 90,
                      "financial_statement_checks": sum(r["statement_checks"] for r in qa),
                      "archive": str(archive), "bytes": archive.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
