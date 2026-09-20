"""Checks the Crocs hypothetical scenario packet itself: arithmetic, dates, amendment chain, labels, isolation and candidate coverage.
No hosted call is made and no demo database is touched."""
import copy
import json
import re
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

import b01
import b01_model
import drift
import prepare_b01_demo

HERE = Path(__file__).parent
TAG = 'Synthetic scenario document for the Crocs hypothetical private-credit scenario.'


class CrocsScenarioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenario = json.loads((HERE / 'h01_scenarios.json').read_text(encoding='utf-8'))
        cls.origin = b01_model.load_origination('H01')
        cls.contract = cls.origin['contract']
        cls.events = {e['id']: e for e in cls.scenario['events']}
        cls.clauses = {c['id']: c['clause'] for c in cls.contract['clauses']}

    def text(self, event_id):
        return ' '.join(s['text'] for s in self.events[event_id]['sources'])

    def money(self, text, pattern):
        return float(re.search(pattern, text).group(1))

    def test_cash_floor_arithmetic_follows_the_covenant_definition(self):
        report = self.text('H01-D05')
        bank = self.money(report, r'totaled \$([\d.]+) million')
        pledged = self.money(report, r'\$([\d.]+) million is held in a deposit account pledged')
        outside = self.money(report, r'and \$([\d.]+) million is held by')
        floor = self.money(self.clauses['C01'], r'less than \$([\d.]+) million')
        unrestricted = round(bank - pledged - outside, 1)
        self.assertEqual((bank, pledged, outside, unrestricted, floor), (39.8, 4.1, 2.1, 33.6, 35.0))
        self.assertLess(unrestricted, floor)
        # both exclusions used in the report are exclusions the clause actually defines
        self.assertIn('pledged or deposited to secure customs bonds', self.clauses['C01'])
        self.assertIn('held by any entity that is not a Loan Party', self.clauses['C01'])
        self.assertIn('not a Loan Party', report)

    def test_opening_model_reconciles(self):
        model = json.loads(next(s['text'] for s in self.origin['sources'] if s['document_id'] == 'origination-financial-model.json'))
        income, balance, metrics = model['income'], model['balance_sheet'], model['metrics']
        self.assertAlmostEqual(income['wholesale_m'] + income['direct_to_consumer_m'], income['revenue_m'])
        self.assertAlmostEqual(income['cost_of_goods_m'], income['revenue_m'] * (1 - income['gross_margin_pct'] / 100), places=1)
        net_debt = balance['term_debt_m'] - min(balance['unrestricted_cash_m'], 25.0)
        self.assertEqual(metrics['net_debt_m'], net_debt)
        self.assertEqual(metrics['net_leverage_x'], round(net_debt / income['covenant_ebitda_m'], 2))
        self.assertEqual(metrics['inventory_days'], round(balance['inventory_m'] / income['cost_of_goods_m'] * 365))
        self.assertEqual(metrics['wholesale_collection_days'], round(balance['wholesale_receivables_m'] / income['wholesale_m'] * 365))
        self.assertIn('Not Crocs, Inc. consolidated reporting', model['perimeter'])

    def test_scenario_facts_meet_the_definitions_they_are_meant_to_meet(self):
        disruption, slowdown = self.text('H01-D02'), self.text('H01-D04')
        self.assertGreaterEqual(int(re.search(r'(\d+)% of the Loan Parties', disruption).group(1)), 10)       # C05(a) volume test
        self.assertGreater(int(re.search(r'delay on that volume is (\d+) days', disruption).group(1)), 21)     # C05(a) delay test
        self.assertGreaterEqual(self.money(slowdown, r'combined \$([\d.]+) million'), 15.0)                    # C05(b) order-loss test
        low = self.money(slowdown, r'reaches a low of \$([\d.]+) million')
        self.assertTrue(35.0 < low < 45.0)                                                                     # C06 trigger met, C01 floor not breached
        self.assertGreater(float(re.search(r'older than 180 days was ([\d.]+)%', slowdown).group(1)), 10.0)    # assumption A2's review criterion

    def business_days_after(self, start, count):
        off = {y: set(b01_model.business_calendar(y)['non_business_dates']) for y in (2026, 2027)}
        day, seen = start, 0
        while seen < count:
            day += timedelta(days=1)
            seen += day.isoformat() not in off[day.year]
        return day

    def test_every_notice_forecast_and_report_is_timely_so_the_only_failure_is_the_cash_floor(self):
        self.assertLessEqual(date(2026, 12, 14), self.business_days_after(date(2026, 12, 9), 5))    # disruption notice
        self.assertLessEqual(date(2026, 12, 22), self.business_days_after(date(2026, 12, 9), 10))   # 13-week forecast
        self.assertLessEqual(date(2027, 2, 19), self.business_days_after(date(2027, 2, 17), 5))     # order-loss notice
        self.assertLessEqual(date(2027, 2, 22), self.business_days_after(date(2027, 2, 17), 10))    # updated forecast
        for month_end, delivered in ((date(2026, 10, 31), date(2026, 11, 18)), (date(2027, 1, 31), date(2027, 2, 18)), (date(2027, 3, 31), date(2027, 4, 16))):
            self.assertLessEqual(delivered, month_end + timedelta(days=20))
        for event in self.scenario['events']:
            self.assertGreaterEqual(event['review_date'], event['available_at'])

    def test_amendment_chain_applies_exactly_and_the_draft_matches_the_current_package(self):
        version = prepare_b01_demo.original_version(self.origin, self.scenario['original_terms'])
        self.assertEqual(len(version['clauses']), 9)
        for amendment in self.scenario['amendments']:
            trigger = self.events[amendment['trigger_event_id']]
            self.assertGreaterEqual(amendment['effective_at'], trigger['review_date'])              # never backdated before its evidence
            version = prepare_b01_demo.apply_amendment(version, amendment)
        self.assertEqual(version['version'], '1.2')
        current = {c['id']: c['clause'] for c in version['clauses']}
        proposal = self.scenario['events'][-1]['pending_proposal']
        self.assertEqual((proposal['status'], proposal['parent_version'], proposal['trigger_event_id']), ('proposed', '1.2', 'H01-D05'))
        for change in proposal['changes']:
            self.assertEqual(current[change['clause_id']], change['before'])                        # the same check the app makes before adoption
        self.assertIn('not waived', proposal['waiver_scope'])

    def test_real_and_fictional_material_are_labeled_and_no_financial_figure_is_imported(self):
        self.assertEqual(self.contract['source_mode'], b01_model.HYPOTHETICAL)
        self.assertEqual(self.contract['label'], 'Crocs — hypothetical private-credit scenario')
        for event in self.scenario['events']:
            for source in event['sources']:
                self.assertTrue(source['text'].startswith(TAG), source['locator'])
        context = json.loads((b01_model.origination_dir('H01') / 'company-context.json').read_text(encoding='utf-8'))
        self.assertEqual([p['locator'] for p in context['passages']], ['P0380', 'P0381', 'P0382', 'P0384'])
        for passage in context['passages']:
            self.assertEqual(passage['content_status'], 'real_sourced_business_context')
            self.assertTrue(passage['url'].startswith('https://www.sec.gov/'))
            self.assertNotRegex(passage['text'], r'\$\s?\d')                                        # sourcing and distribution facts only, no dollar figures
            self.assertNotIn('revenues', passage['text'].lower())
        memo = next(s['text'] for s in self.origin['sources'] if s['document_id'] == 'underwriting-memo.md')
        self.assertIn('not Crocs, Inc. disclosures and no such facility exists', memo)
        self.assertIn('Crocs, Inc. is not a Loan Party and gives no guarantee', self.contract['definitions_and_conventions'])

    def test_scenario_state_is_isolated_from_fluxrail_and_the_benchmark(self):
        db, seed, inbox = b01.paths('H01')
        self.assertEqual((db.name, seed.name, inbox.name), ('h01.sqlite', 'h01_seed.json', 'h01_inbox'))
        self.assertNotEqual(db, b01.DB_PATH)
        self.assertEqual(b01.reports_dir('H01').name, 'h01_reports')
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            base = {'profile': {'assumptions': []}, 'versions': [{'version': '1.0', 'effective_at': '2026-10-01', 'clauses': []}], 'events': [], 'presentation': {'as_of': '2027-04-19'}}
            (home / 'h01_seed.json').write_text(json.dumps({**base, 'borrower': {'id': 'H01', 'name': 'Crocs'}}), encoding='utf-8')
            (home / 'b01_seed.json').write_text(json.dumps({**base, 'borrower': {'id': 'B01', 'name': 'FluxRail'}}), encoding='utf-8')
            with patch.object(b01, 'HERE', home), patch.object(b01, 'DB_PATH', home / 'b01.sqlite'), patch.object(b01, 'SEED_PATH', home / 'b01_seed.json'):
                self.assertEqual(b01.companies(), ['B01', 'H01'])                                   # benchmark R cases never appear as demo companies
                h_db, h_seed, _ = b01.paths('H01')
                self.assertTrue(b01.initialize(h_db, h_seed))
                self.assertTrue(b01.initialize(home / 'b01.sqlite', home / 'b01_seed.json'))
                body = {'title': 'Update', 'text': 'A dated statement.', 'available_at': '2027-04-20', 'review_date': '2027-04-20'}
                queued = b01.enqueue(dict(body), 'manual', h_db)
                self.assertTrue(queued['event_id'].startswith('H01-E-'))
                with self.assertRaisesRegex(ValueError, 'H01'):
                    b01.enqueue({**body, 'borrower_id': 'B01'}, 'manual', h_db)
                self.assertEqual(len(b01.snapshot(home / 'b01.sqlite')['events']), 0)               # nothing crossed into FluxRail

    def test_candidate_path_covers_the_complete_nine_clause_package(self):
        seen = {}
        version = prepare_b01_demo.original_version(self.origin, self.scenario['original_terms'])
        profile = {'assumptions': [{'id': 'H01-A01', 'claim': 'Lead times hold.'}]}

        def completion(system, user):
            seen['payload'] = json.loads(user)
            return {'summary': 's', 'drift_judgment': 'no_material_drift', 'drift_reasons': 'r',
                    'clauses': [{'clause_id': c['clause_id'], 'action': 'retain', 'rationale': 'kept'} for c in seen['payload']['current_package']]}

        report = copy.deepcopy(self.events['H01-D02'])
        record = drift.generate_candidate('H01', profile, version, [report], mode='updated', review_date='2026-12-14', api_key='', model='test', completion=completion)
        self.assertEqual(record['engine'], 'nemotron')
        self.assertEqual([c['clause_id'] for c in seen['payload']['current_package']], [f'C0{i}' for i in range(1, 10)])
        self.assertEqual(len(record['clauses']), 9)                                                  # a complete candidate: every clause answered
        evidence_docs = {e['document_id'] for e in seen['payload']['evidence']}
        self.assertNotIn('credit-agreement.md', evidence_docs)                                        # clause text arrives once, as the package
        self.assertTrue({'underwriting-memo.md', 'origination-financial-model.json', 'CROX-10K-FY2025', 'HFM-2026-12-10'} <= evidence_docs)


if __name__ == '__main__':
    unittest.main()
