"""Author the Crocs hypothetical private-credit scenario (H01) and check that it reconciles.

Usage: python build_h01.py
Writes H01-crocs/model_inputs/ (origination packet) and ../realitycheck/h01_scenarios.json plus ../realitycheck/h01_reports/.

What is real: four business-context passages from Crocs, Inc.'s FY2025 Form 10-K, copied verbatim with locator, URL and SEC
acceptance time. What is fictional: the borrowing entity, the facility, every financial figure, the underwriting memo, the lender
policy, every covenant, every report and every amendment. No Crocs financial statement figure is used anywhere.
Every number below is computed or asserted here, so an arithmetic slip stops the build instead of reaching the model.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
CASE = HERE / 'H01-crocs'
APP = HERE.parent / 'realitycheck'
LABEL = 'Crocs — hypothetical private-credit scenario'
DISCLOSURE = 'Company background is sourced. Financial figures, loan terms, reports and scenario events are fictional.'
FICTION = ('Fictional scenario document. The borrowing entity, facility, figures and events below were invented for a RealityCheck demonstration. '
           'They are not Crocs, Inc. disclosures and no such facility exists.')


def m(x):
    return f'${x:,.1f} million'


# ---- Synthetic opening model for the fictional perimeter (USD millions, twelve months ended September 30, 2026) ----
revenue, wholesale_share, gross_margin = 1040.0, 0.55, 0.52
wholesale, dtc = round(revenue * wholesale_share, 1), round(revenue * (1 - wholesale_share), 1)
cogs = round(revenue * (1 - gross_margin), 1)
covenant_ebitda, debt, cash, netting_cap = 78.0, 150.0, 64.0, 25.0
inventory, receivables = 164.0, 72.1
net_debt = debt - min(cash, netting_cap)
leverage = round(net_debt / covenant_ebitda, 2)
inventory_days = round(inventory / cogs * 365)
collection_days = round(receivables / wholesale * 365)
CASH_FLOOR, FORECAST_TRIGGER, MAX_LEVERAGE = 35.0, 45.0, 2.75
assert (wholesale, dtc, cogs) == (572.0, 468.0, 499.2)
assert net_debt == 125.0 and leverage == 1.60 and inventory_days == 120 and collection_days == 46
assert cash > FORECAST_TRIGGER > CASH_FLOOR and leverage < MAX_LEVERAGE

# ---- Scenario facts used by the reports, each checked against the covenant definitions it is meant to meet or miss ----
affected_volume_pct, delay_days, base_lead_days = 38, 24, 55
assert affected_volume_pct >= 10 and delay_days > 21                       # C05 supply-disruption definition is met
assert base_lead_days + delay_days == 79 and 79 > 70                        # A1 review criterion is met
remaining_delayed_pct = round(affected_volume_pct * 0.40, 1)
assert remaining_delayed_pct == 15.2 and remaining_delayed_pct >= 10          # after rerouting, the delayed share still meets C05's volume test
freight_before, freight_after = 6.8, round(6.8 * (1 - 0.45), 1)
assert freight_after == 3.7
order_cut = 22.0
assert order_cut >= 15.0                                                    # C05 order-loss definition is met
aged_pct = 14.2
assert aged_pct > 10.0                                                      # A2 review criterion is met
forecast_low = 41.3
assert CASH_FLOOR < forecast_low < FORECAST_TRIGGER                         # C06 trigger met, C01 floor not breached
bank, customs_deposit, outside_perimeter = 39.8, 4.1, 2.1
unrestricted = round(bank - customs_deposit - outside_perimeter, 1)
assert unrestricted == 33.6 and unrestricted < CASH_FLOOR                   # C01 floor missed at March 31, 2027
temporary_floor = 30.0
assert temporary_floor < unrestricted                                       # the proposed relief would not itself be breached on these facts

CLAUSES = [
    ('C01', 'Minimum Unrestricted Cash',
     f'The Loan Parties shall not permit Unrestricted Cash to be less than {m(CASH_FLOOR)} as of the last day of any calendar month, beginning October 31, 2026. '
     'Unrestricted Cash means cash and cash equivalents held by the Loan Parties in deposit accounts subject to the Lender\'s control agreement, excluding (a) cash pledged or deposited to secure customs bonds, letters of credit or other obligations, '
     '(b) cash held by any entity that is not a Loan Party, and (c) cash in transit that has not been credited to such an account. Compliance is shown by the monthly cash report delivered under C03.', ['A5']),
    ('C02', 'Maximum Net Leverage',
     f'The Loan Parties shall not permit Net Leverage to exceed {MAX_LEVERAGE:.2f}x as of the last day of any fiscal quarter, beginning December 31, 2026. Net Leverage is Debt less the lesser of Unrestricted Cash and {m(netting_cap)}, '
     'divided by Covenant EBITDA for the four fiscal quarters then ended. Covenant EBITDA is reported EBITDA of the Loan Parties plus documented non-recurring restructuring costs not exceeding 10% of reported EBITDA. '
     'Compliance is shown by the quarterly Compliance Certificate delivered under C03.', ['A4', 'A5']),
    ('C03', 'Financial reporting',
     'The Borrower shall deliver to the Lender (a) within 20 calendar days after each calendar month-end, unaudited management accounts and a cash report listing each deposit account, its balance, its holder and any restriction; and '
     '(b) within 45 calendar days after each fiscal quarter-end, quarterly financial statements and a Compliance Certificate signed by the chief financial officer showing the calculation of Net Leverage and of Unrestricted Cash at each month-end in the quarter. '
     'A deadline that falls on a day that is not a Business Day moves to the next Business Day.', ['A6']),
    ('C04', 'Inventory reporting',
     'Within 20 calendar days after each calendar month-end the Borrower shall deliver an inventory report stating inventory at the lower of cost and net realizable value, aged in buckets of 0 to 90 days, 91 to 180 days and more than 180 days, '
     'separately identifying goods in transit and goods held at each distribution location, and stating write-downs recorded in the month.', ['A2', 'A6']),
    ('C05', 'Material event notice',
     'The Borrower shall notify the Lender in writing within five Business Days after a Responsible Officer first has knowledge of (a) a Supply Disruption, meaning an event expected to delay by more than 21 days the delivery of goods representing at least 10% of '
     'the Loan Parties\' purchase volume for the preceding twelve months; or (b) a Material Order Loss, meaning cancellations or reductions of confirmed wholesale orders totaling at least $15.0 million in any fiscal quarter. '
     'The notice shall state the affected volume or orders, the expected duration and the actions being taken.', ['A1', 'A3']),
    ('C06', 'Cash forecast and remediation reporting',
     f'Within 10 Business Days after a Responsible Officer first has knowledge of a Supply Disruption or a Material Order Loss, or after any month-end at which Unrestricted Cash is less than {m(FORECAST_TRIGGER)}, '
     'the Borrower shall deliver a 13-week cash forecast reconciled to the latest cash report, with a written plan addressing any forecast week in which Unrestricted Cash is below that amount.', ['A5', 'A6']),
    ('C07', 'Restricted payments and discretionary investment',
     f'No Loan Party shall pay a dividend or make a distribution to any person that is not a Loan Party unless, after giving effect to it, Unrestricted Cash is at least $50.0 million and Net Leverage does not exceed 2.25x. '
     'Expansion Capital Expenditure, meaning spending on new retail locations, new distribution capacity or new product tooling, shall not exceed $12.0 million in any fiscal year. Maintenance spending needed to operate existing facilities is not Expansion Capital Expenditure.', ['A5']),
    ('C08', 'Additional debt and liens',
     'No Loan Party shall incur Debt or grant a lien other than (a) the Facility, (b) purchase-money equipment financing not exceeding $10.0 million outstanding, (c) liens arising by operation of law in the ordinary course, including carriers\' and customs liens for amounts not overdue, '
     'and (d) other Debt or liens approved in writing by the Lender. The Borrower shall report any new Debt or lien in the next monthly management accounts.', ['A5']),
    ('C09', 'Amendments, waivers and defaults',
     'No amendment or waiver is effective unless in writing and signed by the Lender, and each states its effective date and scope; a waiver of one failure is not a waiver of any other. '
     'A failure to comply with C01 or C02 is an Event of Default if it continues for 10 Business Days after the Lender gives written notice of it. A failure to deliver a report or notice under C03, C04, C05 or C06 is an Event of Default if it continues for 5 Business Days after the Lender gives written notice of it. '
     'A failure to comply with C07 or C08 is an Event of Default when it occurs. Until an Event of Default exists and is continuing the Lender may not accelerate the Facility.', ['A6']),
]
CLAUSE_TEXT = {cid: text for cid, _, text, _ in CLAUSES}

ASSUMPTIONS = [
    ('A1', 'Third-party manufacturers and at least two ocean routings from each major origin keep lead times from factory to distribution center within about 55 days.',
     'Sourcing and Logistics paragraph of this memo.', 'Lead time exceeds 70 days for at least 10% of purchase volume, or a routing is lost without a working alternative.', 'C05, C04'),
    ('A2', 'Inventory turns in about 120 days and wholesale receivables collect in about 46 days, so seasonal purchases fund themselves within a season.',
     'Working Capital paragraph of this memo and the origination financial model.', 'Inventory older than 180 days exceeds 10% of inventory at cost, or wholesale collection exceeds 55 days.', 'C04, C01'),
    ('A3', 'Direct-to-consumer sales of about 45% of revenue give margin and cash timing that partly offset swings in wholesale orders.',
     'Channel Mix paragraph of this memo.', 'Confirmed wholesale orders fall by at least $15.0 million in a quarter without a same-period direct-to-consumer offset shown in cash.', 'C05'),
    ('A4', 'Goods are bought on FOB-origin terms, so the Borrower bears ocean freight; freight and duty are about 9% of cost of goods, and pricing can recover about half of a freight increase within two quarters.',
     'Margin paragraph of this memo.', 'Freight cost per pair rises by more than 20% for two consecutive months without documented recovery.', 'C02'),
    ('A5', f'Unrestricted Cash stays above $50.0 million in the base forecast, against a {m(CASH_FLOOR)} floor.',
     'Liquidity paragraph of this memo and the base monthly cash forecast.', f'Month-end Unrestricted Cash falls below {m(FORECAST_TRIGGER)}, or a forecast low point falls below $40.0 million.', 'C01, C06, C07'),
    ('A6', 'Monthly accounts, cash reports and inventory reports delivered within 20 days give the lender timely visibility of working capital.',
     'Reporting paragraph of this memo.', 'A required report or notice is late or incomplete.', 'C03, C04, C05, C06'),
]


def amendment(aid, version, parent, trigger, title, decision_at, effective_at, rationale, edits, conditions, waiver_scope, not_pursued, status='adopted'):
    changes = []
    for cid, after in edits:
        changes.append({'clause_id': cid, 'before': CLAUSE_TEXT[cid], 'after': after})
        CLAUSE_TEXT[cid] = after
    text = (f'Fictional amendment {aid} within the {LABEL}. No real instrument exists. ' + title + '. '
            + ' '.join(f'{c["clause_id"]} is replaced as shown.' for c in changes) + ' ' + rationale)
    return {'id': aid, 'version': version, 'parent_version': parent, 'trigger_event_id': trigger, 'title': title, 'decision_at': decision_at,
            'effective_at': effective_at, 'status': status, 'rationale': rationale, 'changes': changes, 'instrument_text': text,
            'conditions': conditions, 'waiver_scope': waiver_scope, 'not_pursued': not_pursued}


def source(doc, locator, text):
    return {'document_id': doc, 'locator': locator, 'text': text}


def main():
    out = CASE / 'model_inputs'
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((CASE / 'manifest.json').read_text(encoding='utf-8'))['documents'][0]
    rows = {r['locator']: r['text'] for r in json.loads((CASE / 'extracted' / 'CROX-10K-FY2025.json').read_text(encoding='utf-8'))}
    context = [{'document_id': 'CROX-10K-FY2025', 'locator': loc, 'text': rows[loc], 'content_status': 'real_sourced_business_context',
                'url': manifest['url'], 'sec_accepted_at': manifest['sec_accepted_at']} for loc in ('P0380', 'P0381', 'P0382', 'P0384')]
    (out / 'company-context.json').write_text(json.dumps({
        'label': LABEL, 'disclosure': DISCLOSURE,
        'note': 'Verbatim passages from Crocs, Inc.\'s FY2025 Form 10-K describing how the real business sources and distributes footwear. They are background only. '
                'They say nothing about the fictional facility, and no financial statement figure from the filing is used in this scenario.',
        'passages': context}, ensure_ascii=False, indent=2), encoding='utf-8')

    definitions = ('Business Day means a day other than a Saturday, a Sunday or a United States federal holiday. Loan Parties means the Borrower and Crocs Footwear Distribution LLC, both fictional entities created for this scenario; '
                   'Crocs, Inc. is not a Loan Party and gives no guarantee. Debt means funded borrowings and finance-lease principal of the Loan Parties. Responsible Officer means the chief financial officer, the treasurer or the head of supply chain of the Borrower. '
                   'All financial definitions apply to the Loan Parties only and not to Crocs, Inc. on a consolidated basis.')
    agreement = [f'# {LABEL}: working-capital term facility', '', FICTION, '',
                 f'Hypothetical Borrower: Crocs Footwear Sourcing LLC. Hypothetical Lender: Meridian Private Credit Fund I (fictional). Facility: {m(debt)} senior secured term loan, closing October 1, 2026, maturing October 1, 2029, fixed interest 8.50%, '
                 'scheduled principal of $1.0 million at the end of each fiscal quarter. Purpose: footwear sourcing and inventory conversion.', '', '## Definitions and conventions', '', definitions, '', '## Covenants', '']
    for cid, title, text, _ in CLAUSES:
        agreement += [f'### {cid} {title}', '', text, '']
    agreement += ['## Defaults waivers and remedies', '', CLAUSES[-1][2], '', '## Authoring provenance', '',
                  'Authored for the RealityCheck demonstration on September 20, 2026 using the project\'s 30-provision reference as a drafting aid. Only the nine provisions above are elected. It is a scoped scenario agreement, not a complete credit agreement.']
    agreement_text = '\n'.join(agreement)
    (out / 'credit-agreement.md').write_text(agreement_text, encoding='utf-8')

    contract = {'borrower_id': 'H01', 'borrower': 'Crocs — hypothetical scenario', 'sector': 'Footwear sourcing and distribution (hypothetical facility)',
                'source_mode': 'hypothetical_real_company', 'label': LABEL, 'disclosure': DISCLOSURE,
                'agreement_id': 'H01-CA-2026', 'version': '1.0', 'executed_at': '2026-10-01', 'effective_at': '2026-10-01', 'known_at': '2026-10-01',
                'clauses': [{'id': cid, 'title': title, 'clause': text, 'thesis_ids': thesis} for cid, title, text, thesis in CLAUSES],
                'definitions_and_conventions': definitions, 'complete_agreement_text': agreement_text,
                'original_terms': {'facility_m': debt, 'fixed_rate': 8.5, 'minimum_unrestricted_cash_m': CASH_FLOOR, 'leverage_max': MAX_LEVERAGE}}
    (out / 'contract-record.json').write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding='utf-8')

    memo = [f'# {LABEL}: underwriting memorandum', '', FICTION, '',
            'Memo H01-UW-2026-01. Approved October 1, 2026 by the fictional lender\'s credit committee for this simulation. Dollar amounts are millions and describe the fictional Loan Parties, not Crocs, Inc.', '',
            '## Borrower and credit decision', '',
            'The scenario borrower buys finished footwear from third-party manufacturers, mainly in Vietnam with others in China, Indonesia, India and Mexico, ships it by ocean to distribution centers in the United States and the Netherlands, and sells it through wholesale customers and direct-to-consumer channels. '
            'The facility funds the seasonal build of inventory. Repayment depends on inventory turning into cash on schedule, so the package relies on liquidity and reporting protections more than on leverage.', '',
            f'**Sourcing and Logistics.** Lead time from factory to distribution center is about {base_lead_days} days. Each major origin has at least two ocean routings. About 38% of purchase volume moves on Asia to United States East Coast routings.', '',
            f'**Working Capital.** Inventory of {m(inventory)} turns in about {inventory_days} days. Wholesale receivables of {m(receivables)} collect in about {collection_days} days. Inventory older than 180 days is 5.5% of inventory at cost.', '',
            f'**Channel Mix.** Wholesale is {m(wholesale)} of revenue and direct-to-consumer is {m(dtc)}, about 45%.', '',
            '**Margin.** Goods are bought FOB origin, so the Borrower pays ocean freight. Freight and duty are about 9% of cost of goods.', '',
            f'**Liquidity.** Unrestricted Cash at closing is {m(cash)}. The base monthly forecast has a low point of $52.0 million in February 2027.', '',
            '**Reporting.** Management accounts, cash reports and inventory reports are due within 20 days after each month-end.', '',
            f'## Six approved synthetic underwriting assumptions', '']
    for aid, claim, evidence, criterion, links in ASSUMPTIONS:
        memo += [f'### {aid}', '', f'**Claim:** {claim}', '', f'**Baseline evidence:** {evidence}', '', f'**Review criterion:** {criterion}', '',
                 f'**Contract relationship:** {links}. These links describe possible protection and do not add a covenant.', '']
    memo += ['## Lender policy for this simulation', '',
             'Fictional policy of the fictional lender: prefer better visibility and reporting before tighter thresholds; grant relief only with compensating protection and a stated end date; never treat unrelated good news as curing a missed obligation. '
             'This is a scenario assumption, not any real lender\'s policy.', '', '## Evidence boundary', '',
             'Forecasts in this memo are origination forecasts. Later reports are separate documents with their own availability dates and must not be loaded into an origination assessment.']
    (out / 'underwriting-memo.md').write_text('\n'.join(memo), encoding='utf-8')

    model = {'label': LABEL, 'disclosure': DISCLOSURE, 'currency': 'USD', 'scale': 'millions', 'perimeter': 'Fictional Loan Parties only. Not Crocs, Inc. consolidated reporting.',
             'twelve_months_ended': '2026-09-30',
             'income': {'revenue_m': revenue, 'wholesale_m': wholesale, 'direct_to_consumer_m': dtc, 'cost_of_goods_m': cogs, 'gross_margin_pct': gross_margin * 100, 'covenant_ebitda_m': covenant_ebitda},
             'balance_sheet': {'unrestricted_cash_m': cash, 'inventory_m': inventory, 'wholesale_receivables_m': receivables, 'term_debt_m': debt},
             'metrics': {'net_debt_m': net_debt, 'net_leverage_x': leverage, 'inventory_days': inventory_days, 'wholesale_collection_days': collection_days, 'inventory_over_180_days_pct': 5.5},
             'base_monthly_unrestricted_cash_forecast_m': {'2026-10': 61.0, '2026-11': 58.5, '2026-12': 56.0, '2027-01': 54.0, '2027-02': 52.0, '2027-03': 55.5, '2027-04': 59.0},
             'conventions': ['All figures are invented and internally reconciled by build_h01.py.', 'Net debt nets at most $25.0 million of Unrestricted Cash.', 'Forecasts are origination forecasts, not later observations.']}
    assert min(model['base_monthly_unrestricted_cash_forecast_m'].values()) == 52.0
    (out / 'origination-financial-model.json').write_text(json.dumps(model, ensure_ascii=False, indent=2), encoding='utf-8')

    tag = 'Synthetic scenario document for the Crocs hypothetical private-credit scenario. '
    events = [
        {'id': 'H01-D01', 'title': 'October 2026 management accounts', 'event_date': '2026-10-31', 'available_at': '2026-11-18', 'review_date': '2026-11-18', 'source_kind': 'scenario_report',
         'report_type': 'company_financial', 'allow_no_impact': True, 'presentation_summary': 'A routine month on the origination case. Tests that an ordinary report stays in the history without a false detection.',
         'sources': [source('H01-MGMT-2026-10', 'P1 — cash and working capital', tag + 'Unaudited management accounts for October 2026, delivered November 18, 2026. Unrestricted Cash was $61.2 million at October 31, against $61.0 million in the base forecast. Inventory was $168.0 million, turning in about 121 days. Wholesale receivables collected in 46 days. Inventory older than 180 days was 5.8% of inventory at cost.'),
                     source('H01-MGMT-2026-10', 'P2 — operations', tag + 'No shipment delays beyond normal variation were recorded. No wholesale orders were cancelled or reduced beyond ordinary adjustments. No dividends, new Debt or liens arose in the month. The cash report lists all deposit accounts as held by Loan Parties with no restriction.')]},
        {'id': 'H01-D02', 'title': 'Ocean shipping disruption on Asia to East Coast routings', 'event_date': '2026-12-09', 'available_at': '2026-12-14', 'review_date': '2026-12-14', 'source_kind': 'scenario_report',
         'report_type': 'industry_and_company', 'presentation_summary': 'An industry disruption, plus company evidence showing which routings and costs are actually exposed.',
         'sources': [source('HFM-2026-12-10', 'P1 — industry report', tag + 'Harborline Freight Monitor, a fictional industry publication, reported on December 10, 2026 that major carriers suspended canal transits on Asia to United States East Coast services and are routing around the Cape. It estimates added transit time of 18 to 26 days and spot container rates up 62% on those services. The report names no shipper and expects the disruption to last at least through the first quarter of 2027; that is a forecast.'),
                     source('H01-OPS-2026-12-11', 'P2 — exposed volume and cost responsibility', tag + f'Operations note dated December 11, 2026. {affected_volume_pct}% of the Loan Parties\' purchase volume for the preceding twelve months ships on the affected routings. Expected delivery delay on that volume is {delay_days} days, taking lead time from about {base_lead_days} days to about {base_lead_days + delay_days} days. Goods are bought FOB origin, so the Borrower bears the ocean freight. About 70% of the affected containers move at spot rates. No alternative routing had been booked as of this note.'),
                     source('H01-OPS-2026-12-11', 'P3 — knowledge and notice', tag + 'The head of supply chain first learned of the carrier suspensions on December 9, 2026. The Borrower delivered written notice to the Lender on December 14, 2026 stating the affected volume, the expected duration and the actions being taken. A 13-week cash forecast had not yet been delivered as of December 14.')]},
        {'id': 'H01-D03', 'title': 'Rerouting and freight surcharge update', 'event_date': '2027-01-15', 'available_at': '2027-01-19', 'review_date': '2027-01-19', 'source_kind': 'scenario_report',
         'report_type': 'company_remediation', 'allow_no_impact': True, 'presentation_summary': 'Mitigation evidence. Tests which earlier concerns are reduced and which remain.',
         'revision_note': 'Revised development case (September 20, 2026). The first version of this report did not restate the 38% exposure or evidence the forecast refresh that version 1.1 requires, so the model could not judge either. Both facts were added; the first analysis is kept in h01_attempts/.',
         'sources': [source('H01-OPS-2027-01-15', 'P1 — rerouting', tag + f'Operations update dated January 15, 2027. The affected routings carry {affected_volume_pct}% of the Loan Parties\' purchase volume for the preceding twelve months. 60% of that affected volume has been rebooked through United States West Coast ports with rail to the distribution center, which cuts the delay on that portion from 24 days to 9 days. The remaining 40% of the affected volume, about {remaining_delayed_pct}% of purchase volume, still moves around the Cape with a 24-day delay. No further alternative capacity is available before April 2027.'),
                     source('H01-OPS-2027-01-15', 'P2 — cost recovery', tag + f'Incremental freight cost for the first quarter of 2027 is estimated at {m(freight_before)}. Wholesale customers representing most of the affected volume accepted a freight surcharge from February 1, 2027 that recovers 45% of the incremental cost, leaving about {m(freight_after)} unrecovered. The surcharge does not apply to direct-to-consumer sales.'),
                     source('H01-OPS-2027-01-15', 'P3 — forecasts delivered', tag + 'The head of supply chain first learned of the disruption on December 9, 2026, and the 13-week cash forecast required after it was delivered on December 22, 2026. The first refreshed forecast required every two weeks under version 1.1 was delivered on January 8, 2027; the next is due January 22, 2027. The January 8 forecast has a low point of $48.9 million in February 2027.')]},
        {'id': 'H01-D04', 'title': 'Wholesale customers cut spring orders; inventory ages', 'event_date': '2027-02-17', 'available_at': '2027-02-22', 'review_date': '2027-02-22', 'source_kind': 'scenario_report',
         'report_type': 'company_operating', 'presentation_summary': 'Reduced orders, older inventory and a lower cash forecast arrive together.',
         'sources': [source('H01-SALES-2027-02-19', 'P1 — order reductions', tag + f'Sales note dated February 19, 2027. Two wholesale customers reduced confirmed spring 2027 orders by a combined {m(order_cut)} in the fiscal quarter ending March 31, 2027, citing slower sell-through of late-arriving winter product. The chief financial officer first learned of the reductions on February 17, 2027 and the Borrower delivered written notice to the Lender on February 19, 2027. Direct-to-consumer sales for January were 3% above the prior year.'),
                     source('H01-INV-2027-01', 'P2 — January inventory report', tag + f'Inventory report for January 31, 2027, delivered February 18, 2027. Inventory at the lower of cost and net realizable value was $181.5 million. Inventory older than 180 days was {aged_pct}% of inventory at cost, compared with 5.5% at origination, mostly winter product that arrived after its selling window. No write-down was recorded in January.'),
                     source('H01-FCST-2027-02-22', 'P3 — updated cash forecast', tag + f'Updated 13-week cash forecast delivered February 22, 2027. Forecast Unrestricted Cash reaches a low of {m(forecast_low)} at the end of April 2027, against {m(CASH_FLOOR)} required and $52.0 million in the origination base forecast. The plan proposes deferring $4.0 million of new distribution capacity spending; it has not been approved.')]},
        {'id': 'H01-D05', 'title': 'Direct sales recover; March month-end cash report', 'event_date': '2027-03-31', 'available_at': '2027-04-19', 'review_date': '2027-04-19', 'source_kind': 'scenario_report',
         'report_type': 'company_financial', 'presentation_summary': 'Good sales news arrives with a month-end cash report. Tests whether positive news is allowed to cancel a missed obligation.',
         'sources': [source('H01-MGMT-2027-03', 'P1 — sales', tag + 'Management accounts for March 2027, delivered April 16, 2027. Direct-to-consumer sales were 18% above March 2026, helped by spring product that arrived on the rerouted services. Wholesale shipments were 11% below plan.'),
                     source('H01-CASH-2027-03', 'P2 — month-end cash report', tag + f'Cash report as of March 31, 2027, delivered April 16, 2027. Bank balances across all listed accounts totaled {m(bank)}. Of that, {m(customs_deposit)} is held in a deposit account pledged to secure customs bonds, and {m(outside_perimeter)} is held by Crocs Footwear Retail Asia Pte. Ltd., a fictional entity that is not a Loan Party. No cash was in transit at month-end.'),
                     source('H01-MGMT-2027-03', 'P3 — collections and lender contact', tag + 'Wholesale receivables collected in 61 days in March, compared with 46 days at origination, as two customers paid late. As of April 19, 2027 the Lender had not given written notice of any failure to comply.')],
         'pending_proposal': None},
    ]
    for e in events:
        assert sum(len(s['text']) for s in e['sources']) < 48000 and e['review_date'] >= e['available_at']

    a1 = amendment('H01-AM01', '1.1', '1.0', 'H01-D02', 'Routing visibility and recurring forecasts during a supply disruption', '2026-12-22', '2026-12-28',
                   'Simulated analyst decision. The disruption exposes supply and margin assumptions while no threshold is near. In line with the scenario lender policy, the response adds visibility before tightening any limit.',
                   [('C04', CLAUSE_TEXT['C04'] + ' Beginning with the report for December 31, 2026, the inventory report shall also state purchase volume and goods in transit by ocean routing and by manufacturer, and the expected arrival date of goods delayed by more than 21 days.'),
                    ('C06', CLAUSE_TEXT['C06'] + ' While a Supply Disruption notified under C05 continues, the Borrower shall deliver a refreshed 13-week cash forecast every two weeks, beginning January 8, 2027.')],
                   ['13-week cash forecast delivered December 22, 2026.'], 'None. No failure had occurred.',
                   {'title': 'Tighten the cash floor immediately', 'description': 'Considered and not pursued: raising the Unrestricted Cash floor. Cash was well above it and the evidence concerned visibility, not a shortfall.'})
    a2 = amendment('H01-AM02', '1.2', '1.1', 'H01-D04', 'Aged-inventory reporting, weekly cash reporting and a pause on expansion spending', '2027-03-04', '2027-03-08',
                   'Simulated analyst decision. Inventory older than 180 days passed the memo\'s review level and the forecast low fell below the forecast trigger while still above the floor. The response protects liquidity through spending discipline and faster reporting, without changing the floor.',
                   [('C04', CLAUSE_TEXT['C04'] + ' Beginning with the report for February 28, 2027, the report shall state, for inventory older than 180 days, units, cost, net realizable value, planned sell-through channel and any reserve.'),
                    ('C06', CLAUSE_TEXT['C06'] + f' While any forecast week shows Unrestricted Cash below {m(FORECAST_TRIGGER)}, the Borrower shall deliver a cash report each Monday for the preceding week.'),
                    ('C07', CLAUSE_TEXT['C07'] + ' From March 8, 2027, no Expansion Capital Expenditure shall be committed while month-end Unrestricted Cash is below $50.0 million.')],
                   ['Borrower confirmed deferral of $4.0 million of new distribution capacity spending.'], 'None. No failure had occurred.',
                   {'title': 'Leave the package unchanged and monitor', 'description': 'Considered and not pursued: relying on existing monthly reporting while the forecast low approached the floor.'})
    proposal = amendment('H01-AM03-DRAFT', '1.3', '1.2', 'H01-D05', 'Time-limited cash-floor relief with weekly collections reporting', None, None,
                         'Unsigned discussion draft for the user to review. The March 31, 2027 month-end was below the floor while direct sales improved and collections slowed. Under the scenario lender policy, relief is offered only with a stated end date and compensating protection. Good sales news does not cure the missed floor; the historical failure is not waived by this draft.',
                         [('C01', CLAUSE_TEXT['C01'] + f' For the month-ends of April 30, May 31 and June 30, 2027 only, the amount is {m(temporary_floor)}; it returns to {m(CASH_FLOOR)} from July 31, 2027.'),
                          ('C03', CLAUSE_TEXT['C03'] + ' From the effective date of Amendment 3 until July 31, 2027, the Borrower shall also deliver each Monday a wholesale collections report listing each receivable more than 15 days past due, the customer and the expected payment date.')],
                         ['Would require signature by the fictional Lender and a stated effective date.'], 'The March 31, 2027 failure under C01 is not waived by this draft.',
                         {'title': 'Keep version 1.2 and send a notice of the failure', 'description': 'Open alternative, not yet rejected: give written notice under C09, require a cure within 10 Business Days and keep the current terms. Neither path has been selected.'},
                         status='proposed')
    proposal.update(clause_id='C01', description='Draft relief for three month-ends with weekly collections reporting. Not adopted.', draft_at='2027-04-19')
    events[-1]['pending_proposal'] = proposal

    scenarios = {'borrower_id': 'H01', 'borrower': 'Crocs — hypothetical scenario', 'synthetic': True, 'source_mode': 'hypothetical_real_company', 'label': LABEL, 'disclosure': DISCLOSURE,
                 'description': 'Six-month scenario: a routine month, a shipping disruption, mitigation, a wholesale slowdown, and a recovery that arrives with a missed cash floor. Two simulated amendments are adopted; a third draft is left for the user.',
                 'original_terms': contract['original_terms'], 'presentation': {'as_of': '2027-04-19'}, 'events': events, 'amendments': [a1, a2]}
    (APP / 'h01_scenarios.json').write_text(json.dumps(scenarios, ensure_ascii=False, indent=2), encoding='utf-8')

    library = APP / 'h01_reports'
    library.mkdir(exist_ok=True)
    (library / '2027-04-26-footwear-tariff-analysis.json').write_text(json.dumps({
        'borrower_id': 'H01', 'report_type': 'industry_analysis', 'publisher': 'Northgate Research (fictional)', 'synthetic': True,
        'title': 'Industry analysis: proposed tariff on footwear made in Vietnam', 'library_summary': 'An external report that never names the borrower. Tests that an industry development is tied to the scenario\'s real sourcing exposure without becoming a borrower fact.',
        'event_date': '2027-04-23', 'available_at': '2027-04-26', 'review_date': '2027-04-26',
        'sources': [source('NGR-2027-FOOTWEAR-TARIFF', 'P1 — proposal', tag + 'Northgate Research, a fictional analyst firm, reported on April 23, 2027 that a proposed United States tariff would add 12 percentage points of duty to footwear made in Vietnam from September 1, 2027. The proposal has not been adopted and Northgate puts the chance of adoption at about even; that is an analyst estimate. The report names no importer.'),
                    source('NGR-2027-FOOTWEAR-TARIFF', 'P2 — who bears it', tag + 'Northgate notes that importers buying on FOB-origin terms are importer of record and pay the duty, and that in earlier tariff rounds importers recovered between one third and two thirds of the added duty through pricing within a year. Importers able to move production to other countries did so over 9 to 18 months.'),
                    source('NGR-2027-FOOTWEAR-TARIFF', 'P3 — limits', tag + 'The report uses public trade data only. It contains no information about any company\'s sourcing mix, contracts, pricing power or lenders.')]}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'built': 'H01', 'clauses': len(CLAUSES), 'assumptions': len(ASSUMPTIONS), 'events': len(events), 'amendments': 2, 'pending': proposal['version'],
                      'opening': {'net_debt': net_debt, 'leverage': leverage, 'inventory_days': inventory_days, 'collection_days': collection_days},
                      'march_31_unrestricted_cash': unrestricted, 'context_passages': len(context)}))


if __name__ == '__main__':
    main()
