import copy
import unittest

import b01_model
import drift


class DriftTest(unittest.TestCase):
    def setUp(self):
        contract = b01_model.load_origination('R02')['contract']
        self.version = {'version': '1.0', 'clauses': copy.deepcopy(contract['clauses']),
                        'definitions_and_conventions': contract['definitions_and_conventions']}
        self.profile = {'assumptions': [{'id': 'R02-A01', 'claim': 'EBITDA keeps leverage within the limit.'}]}
        self.report = {'id': 'R02-D02', 'available_at': '2023-05-10',
                       'sources': [{'document_id': 'TEST-PR', 'locator': 'P0001', 'text': 'Adjusted EBITDA decreased to $10.7 million in the quarter.'}]}
        self.good_quote = {'document_id': 'TEST-PR', 'locator': 'P0001', 'quote': 'Adjusted EBITDA decreased to $10.7 million'}

    def response(self, clauses, judgment='material_drift'):
        return {'summary': 's', 'clauses': clauses, 'drift_judgment': judgment, 'drift_reasons': 'r'}

    def candidate(self, raw, mode='updated', review_date='2023-05-10'):
        return drift.generate_candidate('R02', self.profile, self.version, [self.report], mode=mode, review_date=review_date,
                                        api_key='', model='test', completion=lambda system, user: copy.deepcopy(raw))

    def change(self, **kwargs):
        return {'clause_id': 'C05', 'action': 'modify', 'change_type': 'reporting_frequency', 'change': 'Monthly certificate.',
                'affected_assumptions': ['R02-A01', 'R02-A99'], 'rationale': 'Earnings fell.', 'evidence': [self.good_quote], **kwargs}

    def test_verified_change_is_kept_and_unknown_assumption_dropped(self):
        result = self.candidate(self.response([self.change(), {'clause_id': 'C03', 'action': 'retain', 'rationale': 'Adequate.'}]))
        self.assertEqual(result['engine'], 'nemotron')
        kept = [c for c in result['clauses'] if c['action'] == 'modify']
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0]['affected_assumptions'], ['R02-A01'])
        self.assertTrue(kept[0]['evidence'][0]['verified'])

    def test_change_without_verified_evidence_is_withheld_not_downgraded(self):
        fake = {'document_id': 'TEST-PR', 'locator': 'P0001', 'quote': 'Leverage reached 6.0x'}
        result = self.candidate(self.response([self.change(evidence=[fake])]))
        self.assertEqual(result['clauses'], [])
        self.assertTrue(any('withheld' in w for w in result['warnings']))

    def test_drift_claim_without_a_validated_change_is_not_a_detection(self):
        fake = {'document_id': 'TEST-PR', 'locator': 'P0001', 'quote': 'Leverage reached 6.0x'}
        result = self.candidate(self.response([self.change(evidence=[fake])], judgment='material_drift'))
        self.assertEqual(result['drift_judgment'], 'insufficient_evidence')
        self.assertEqual(result['model_judgment'], 'material_drift')

    def test_compare_rejects_mismatched_prompt_versions(self):
        base = {'review_date': 'd', 'package_version': '1.0', 'guidelines': {}, 'model': 'm', 'report_ids': [], 'summary': '',
                'drift_reasons': '', 'warnings': [], 'drift_judgment': 'no_material_drift', 'clauses': []}
        with self.assertRaises(ValueError):
            drift.compare({**base, 'prompt_version': '0.1'}, {**base, 'prompt_version': '0.2'})

    def test_control_cannot_cite_a_later_report(self):
        result = self.candidate(self.response([self.change()]), mode='control')
        self.assertEqual(result['clauses'], [])
        self.assertEqual(result['report_ids'], [])

    def test_report_after_review_date_is_rejected(self):
        with self.assertRaises(ValueError):
            self.candidate(self.response([]), review_date='2023-05-09')

    def test_reports_are_not_buried_under_a_filing_or_mistaken_for_later_events(self):
        from unittest.mock import patch
        origin = copy.deepcopy(b01_model.load_origination('R02'))
        origin['sources'] += [{'document_id': 'FILING', 'locator': 'p1', 'text': 'Annual report risk factors. ' * 400, 'role': '10k'},
                              {'document_id': 'MEMO', 'locator': 'p1', 'text': 'Underwriting memo.', 'role': 'memo'}]
        sent = {}
        def completion(system, user):
            sent.update(system=system, payload=__import__('json').loads(user))
            return self.response([], judgment='no_material_drift')
        report = {**self.report, 'title': 'Q1 results', 'available_at': '2023-05-10'}
        with patch.object(b01_model, 'load_origination', return_value=origin):
            drift.generate_candidate('R02', self.profile, self.version, [report], mode='updated', review_date='2023-05-10',
                                     api_key='', model='test', completion=completion)
        ids = [e['document_id'] for e in sent['payload']['evidence']]
        self.assertNotIn('FILING', ids)   # a whole annual filing is background, 15 times the size of every report together
        self.assertIn('MEMO', ids)
        supplied = next(e for e in sent['payload']['evidence'] if e['document_id'] == 'TEST-PR')
        self.assertEqual((supplied['report'], supplied['available_to_lender']), ('Q1 results', '2023-05-10'))
        self.assertIn('available to the lender by the review date', sent['system'])

    def test_invalid_judgment_is_an_error(self):
        result = self.candidate(self.response([], judgment='severe'))
        self.assertEqual(result['engine'], 'unavailable')
        self.assertIn('drift_judgment', result['error'])

    def test_compare_separates_new_evidence_from_control(self):
        shared = {'clause_id': 'C04', 'action': 'modify', 'change_type': 'scope', 'change': 'x', 'rationale': 'r', 'evidence': []}
        new = {'clause_id': 'C05', 'action': 'modify', 'change_type': 'reporting_frequency', 'change': 'y', 'rationale': 'r', 'evidence': []}
        base = {'review_date': '2023-05-10', 'package_version': '1.0', 'guidelines': {}, 'model': 'm', 'report_ids': [],
                'summary': '', 'drift_reasons': '', 'warnings': [], 'drift_judgment': 'no_material_drift'}
        control = {**base, 'clauses': [shared]}
        updated = {**base, 'clauses': [shared, new, {'clause_id': 'C03', 'action': 'retain', 'rationale': ''}], 'drift_judgment': 'material_drift', 'report_ids': ['R02-D02']}
        observed = {'version': '1.1', 'title': 'Amendment', 'changes': [{'clause_id': 'C01'}, {'clause_id': 'C05'}]}
        out = drift.compare(control, updated, observed)
        self.assertEqual([c['clause_id'] for c in out['evidence_attributable_changes']], ['C05'])
        self.assertEqual([c['clause_id'] for c in out['changes_also_in_control']], ['C04'])
        self.assertEqual(out['retained'], ['C03'])
        self.assertEqual(out['observed_response']['overlap_with_attributable'], ['C05'])


if __name__ == '__main__':
    unittest.main()
