import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import b01_model


class B01ModelTests(unittest.TestCase):
    def setUp(self):
        self.origination = b01_model.load_origination()
        self.memo = next(s for s in self.origination['sources'] if s['document_id'] == 'underwriting-memo.md')
        self.claim = 'Renewals depend on reliable workflow execution across the largest supported identity and ERP connectors.'
        self.citation = {'document_id': self.memo['document_id'], 'locator': self.memo['locator'], 'quote': self.claim}
        self.response = {'summary': 'FluxRail depends on supported workflow integrations.', 'assumptions': [
            {'id': 'B01-A01', 'title': 'Reliable integrations', 'claim': self.claim, 'source_assumption_id': 'A1',
             'basis': 'explicit', 'covenant_ids': ['S1', 'S2'], 'evidence': [self.citation]},
            {'id': 'B01-A02', 'title': 'Service continuity', 'claim': 'Continued service supports cash generation.',
             'source_assumption_id': None, 'basis': 'inferred', 'covenant_ids': ['C01'], 'evidence': [self.citation]}],
            'relationships': [{'source': 'B01-A01', 'target': 'B01-A02', 'type': 'influences', 'rationale': 'Reliable integrations support continued service.'}]}
        self.event = {'id': 'B01-E01', 'title': 'Connector failure', 'event_date': '2027-03-05',
                      'available_at': '2027-03-05', 'review_date': '2027-03-05',
                      'sources': [{'document_id': 'incident.md', 'locator': 'Incident', 'text': 'The supported connector stopped working.'}]}
        contract = self.origination['contract']
        self.version = {'version': '2.0', 'effective_at': '2027-03-01', 'status': 'effective',
                        'clauses': contract['clauses'], 'terms': {'fixed_rate': 9.75, 'leverage_max': 4.05},
                        'definitions_and_conventions': contract['definitions_and_conventions'], 'instrument_text': 'Current terms.'}

    def profile(self):
        return b01_model.generate_profile(api_key='', model='test', completion=lambda s, u: copy.deepcopy(self.response))['profile']

    def test_profile_uses_only_origination_and_separates_inferences(self):
        def completion(system, user):
            payload = json.loads(user)
            self.assertEqual({s['document_id'] for s in payload['sources']}, {
                'credit-agreement.md', 'contract-record.json', 'underwriting-memo.md', 'origination-financial-model.json'})
            self.assertNotIn('future-evidence', json.dumps([s['document_id'] for s in payload['sources']]))
            return self.response
        result = b01_model.generate_profile(api_key='', model='test', completion=completion)
        self.assertEqual(result['engine'], 'nemotron')
        self.assertEqual(result['profile']['assumptions'][0]['baseline_status'], 'approved_synthetic')
        self.assertEqual(result['profile']['assumptions'][1]['baseline_status'], 'working')
        self.assertEqual(len(result['profile']['relationships']), 1)

    def test_profile_withholds_foreign_ids_and_false_quotes(self):
        self.response['assumptions'].append({**self.response['assumptions'][0], 'id': 'T01'})
        self.response['assumptions'].append({**self.response['assumptions'][0], 'id': 'B01-A03',
                                             'evidence': [{**self.citation, 'quote': 'Not present in this package.'}]})
        self.response['relationships'].append({'source': 'T01', 'target': 'B01-A01', 'type': 'influences', 'rationale': 'Wrong company.'})
        result = b01_model.generate_profile(api_key='', model='test', completion=lambda s, u: self.response)
        self.assertEqual([a['id'] for a in result['profile']['assumptions']], ['B01-A01', 'B01-A02'])
        self.assertEqual(len(result['profile']['relationships']), 1)
        self.assertGreaterEqual(len(result['warnings']), 3)

    def test_event_uses_current_version_and_verifies_findings(self):
        citation = {'document_id': 'incident.md', 'locator': 'Incident', 'quote': 'The supported connector stopped working.'}
        findings = {'summary': 'Connector failure exposes integration reliability.', 'attributions': [
            {'target_type': 'assumption', 'target_id': 'B01-A01', 'relation_type': 'direct_assumption_evidence',
             'risk_direction': 'adverse', 'proposed_status': 'weakened', 'rationale': 'The connector failed.',
             'evidence': [citation], 'suggested_action': 'review_assumption', 'proposed_adjustment': '', 'path': []}],
            'candidates': [], 'covenant_assessments': [
                {'clause_id': 'S1', 'status': 'insufficient_evidence', 'rationale': 'Affected revenue and remediation dates are missing.', 'evidence': [citation]},
                {'clause_id': 'PC01', 'status': 'noncompliant', 'rationale': 'Wrong contract.', 'evidence': [citation]}]}
        def completion(system, user):
            payload = json.loads(user)
            self.assertEqual(payload['package_version']['terms']['fixed_rate'], 9.75)
            self.assertNotIn('T01', user)
            return findings
        result = b01_model.attribute_event(self.event, self.profile(), self.version, api_key='', model='test', completion=completion)
        self.assertEqual(result['package_version'], '2.0')
        self.assertEqual(len(result['attributions']), 1)
        self.assertEqual([a['clause_id'] for a in result['covenant_assessments']], ['S1'])
        self.assertTrue(result['attributions'][0]['evidence'][0]['verified'])

    def test_already_assessed_finding_must_point_at_a_supplied_earlier_event(self):
        citation = {'document_id': 'incident.md', 'locator': 'Incident', 'quote': 'The supported connector stopped working.'}
        findings = {'summary': 'Follow-up.', 'attributions': [], 'candidates': [], 'covenant_assessments': [
            {'clause_id': 'S1', 'status': 'noncompliant', 'rationale': 'Same missed duty.', 'already_assessed_in': 'B01-D01', 'evidence': [citation]},
            {'clause_id': 'S2', 'status': 'triggered', 'rationale': 'Claims an earlier finding that was never supplied.', 'already_assessed_in': 'B01-D99', 'evidence': [citation]},
            {'clause_id': 'C08', 'status': 'triggered', 'rationale': 'Points at an event that concerned another clause.', 'already_assessed_in': 'B01-D01', 'evidence': [citation]}]}
        profile = self.profile()
        profile['prior_covenant_findings'] = [{'clause_id': 'S1', 'status': 'noncompliant', 'event_id': 'B01-D01', 'review_date': '2027-03-01'}]
        result = b01_model.attribute_event(self.event, profile, self.version, api_key='', model='test', completion=lambda s, u: findings)
        earlier = {c['clause_id']: c['already_assessed_in'] for c in result['covenant_assessments']}
        self.assertEqual(earlier, {'S1': 'B01-D01', 'S2': None, 'C08': None})   # a new finding can never be hidden by an unfounded reference

    def test_hypothetical_scenario_carries_guard_context_and_all_approved_claims(self):
        seen = {}
        origin = b01_model.load_origination('H01')
        self.assertEqual(origin['contract']['source_mode'], b01_model.HYPOTHETICAL)
        passage = next(s for s in origin['sources'] if s['document_id'] == 'CROX-10K-FY2025')
        memo = next(s['text'] for s in origin['sources'] if s['document_id'] == 'underwriting-memo.md')
        claim = memo.split('### A1')[1].split('**Claim:** ')[1].split('\n')[0]

        def completion(system, user):
            seen['system'], seen['payload'] = system, json.loads(user)
            return {'summary': 's', 'relationships': [], 'assumptions': [
                {'id': 'H01-A01', 'title': 'Supply continuity', 'claim': claim, 'basis': 'explicit', 'source_assumption_id': 'A1', 'covenant_ids': ['C05'],
                 'evidence': [{'document_id': 'underwriting-memo.md', 'locator': 'Full document', 'quote': claim}]},
                {'id': 'H01-A07', 'title': 'Vietnam concentration', 'claim': 'Production concentration in Vietnam persists.', 'basis': 'inferred', 'source_assumption_id': None, 'covenant_ids': [],
                 'evidence': [{'document_id': 'CROX-10K-FY2025', 'locator': passage['locator'], 'quote': passage['text'][:60]}]}]}

        result = b01_model.generate_profile(api_key='', model='test', borrower_id='H01', completion=completion)
        self.assertIn('Never substitute or add anything you may recall about the real company', seen['system'])
        self.assertIn('all 6 approved memo claims', seen['system'])
        self.assertEqual(len(seen['payload']['approved_claims']), 6)
        statuses = {a['id']: a['baseline_status'] for a in result['profile']['assumptions']}
        self.assertEqual(statuses, {'H01-A01': 'approved_synthetic', 'H01-A07': 'working'})   # a sourced 10-K quote verifies, and stays an inference

    def test_no_key_remains_unassessed(self):
        result = b01_model.attribute_event(self.event, self.profile(), self.version, api_key='', model='test')
        self.assertEqual(result['engine'], 'unavailable')
        self.assertEqual(result['attributions'], [])
        self.assertTrue(all(c['status'] == 'unassessed' for c in result['coverage']))

    def test_approved_review_criteria_reach_the_model_without_altering_the_profile(self):
        seen = {}

        def completion(system, user):
            seen['payload'] = json.loads(user)
            seen['system'] = system
            return {'summary': 's', 'attributions': [], 'candidates': [], 'covenant_assessments': []}

        profile = self.profile()
        b01_model.attribute_event(self.event, profile, self.version, api_key='', model='test', completion=completion)
        supplied = {a['source_assumption_id']: a.get('review_criterion') for a in seen['payload']['profile']['assumptions']}
        approved = {key: value for key, value in supplied.items() if key}
        self.assertTrue(approved)                                                # the fixture profile has approved memo claims
        self.assertTrue(all(isinstance(value, str) and value for value in approved.values()))
        self.assertIsNone(supplied.get(None))                                   # inferred assumptions carry no approved criterion
        self.assertFalse(any('review_criterion' in a for a in profile['assumptions']))   # caller's profile is untouched
        self.assertIn('Judge materiality', seen['system'])

    def test_future_version_is_rejected(self):
        self.version['effective_at'] = '2027-04-01'
        with self.assertRaises(ValueError):
            b01_model.attribute_event(self.event, self.profile(), self.version, api_key='', model='test')

    def test_delayed_event_cannot_use_later_amendment(self):
        self.event['event_date'] = '2027-02-01'
        with self.assertRaises(ValueError):
            b01_model.attribute_event(self.event, self.profile(), self.version, api_key='', model='test')

    def test_optional_array_omission_and_text_null_preserve_actual_findings(self):
        raw = {'summary': 'An operative connector duty needs review.', 'attributions': [{
            'target_type': 'covenant', 'target_id': 'S1', 'relation_type': 'covenant_input',
            'risk_direction': 'adverse', 'proposed_status': 'null', 'rationale': 'The connector stopped.',
            'evidence': [{'document_id': 'incident.md', 'locator': 'Incident', 'quote': 'The supported connector stopped working.'}],
            'suggested_action': 'request_information', 'proposed_adjustment': None, 'path': []}]}
        result = b01_model.attribute_event(self.event, self.profile(), self.version, api_key='', model='test', completion=lambda s, u: raw)
        self.assertEqual(result['engine'], 'nemotron')
        self.assertIsNone(result['attributions'][0]['proposed_status'])
        self.assertEqual(result['raw_response']['attributions'][0]['proposed_status'], 'null')
        self.assertEqual(result['covenant_assessments'], [])

    def test_known_versions_excludes_future_and_draft_terms(self):
        self.version['known_versions'] = [{**self.version, 'version': '1.0', 'effective_at': '2026-12-31'},
            {**self.version, 'version': '3.0', 'effective_at': '2027-06-01'},
            {**self.version, 'version': '4.0', 'status': 'proposed'}]
        def completion(system, user):
            payload = json.loads(user)
            self.assertEqual([v['version'] for v in payload['known_versions']], ['1.0'])
            self.assertIn('ten Business Days', payload['resolution_conventions'])
            return {'summary': 'Insufficient financial evidence.', 'attributions': [], 'candidates': [], 'covenant_assessments': []}
        result = b01_model.attribute_event(self.event, self.profile(), self.version, api_key='', model='test', completion=completion)
        self.assertEqual(result['engine'], 'nemotron')

    def test_short_locator_resolves_only_to_unique_matching_source(self):
        self.event['sources'] = [{'document_id': 'incident.md', 'locator': 'P1 — monitoring', 'text': 'The connector failed.'},
                                {'document_id': 'incident.md', 'locator': 'P2 — follow-up', 'text': 'No notice was sent.'}]
        item = {'target_type': 'covenant', 'target_id': 'S1', 'relation_type': 'covenant_input',
                'risk_direction': 'adverse', 'proposed_status': None, 'rationale': 'Review connector failure.',
                'evidence': [{'document_id': 'incident.md', 'locator': 'P1', 'quote': 'The connector failed.'}],
                'suggested_action': 'request_information', 'proposed_adjustment': '', 'path': []}
        wrong = copy.deepcopy(item)
        wrong['evidence'][0]['locator'] = 'P2'
        raw = {'summary': 'Review connector failure.', 'attributions': [item, wrong], 'candidates': [], 'covenant_assessments': []}
        result = b01_model.attribute_event(self.event, self.profile(), self.version, api_key='', model='test', completion=lambda s, u: raw)
        self.assertEqual(len(result['attributions']), 1)
        self.assertEqual(result['attributions'][0]['evidence'][0]['locator'], 'P1 — monitoring')
        self.assertEqual(result['raw_response']['attributions'][0]['evidence'][0]['locator'], 'P1')

    def test_contract_calendar_observes_weekends_and_holidays(self):
        calendar = b01_model.business_calendar(2027)
        self.assertIn('2027-07-10', calendar['non_business_dates'])
        self.assertIn('2027-09-06', calendar['non_business_dates'])
        self.assertNotIn('2027-07-12', calendar['non_business_dates'])
        self.assertNotIn('2027-09-09', calendar['non_business_dates'])

    def test_amendment_requires_exact_prior_text_and_keeps_baseline(self):
        import prepare_b01_demo
        version = {'version': '1.0', 'effective_at': '2026-12-31', 'clauses': [
            {'id': 'S1', 'title': 'Compatibility', 'clause': 'Thirty days.'}], 'terms': {'fixed_rate': 9.25}}
        amendment = {'version': '1.1', 'parent_version': '1.0', 'effective_at': '2027-07-20',
                     'changes': [{'clause_id': 'S1', 'before': 'Thirty days.', 'after': 'Fifteen days.'}]}
        updated = prepare_b01_demo.apply_amendment(version, amendment)
        self.assertEqual(updated['clauses'][0]['clause'], 'Fifteen days.')
        self.assertEqual(version['clauses'][0]['clause'], 'Thirty days.')
        amendment['changes'][0]['before'] = 'Wrong prior text.'
        with self.assertRaises(ValueError):
            prepare_b01_demo.apply_amendment(version, amendment)

    def test_preparation_preserves_a_reviewed_seed_on_repeat(self):
        import prepare_b01_demo
        profile = self.profile()
        seed = {'profile': profile, 'complete': True, 'versions': [{'version': v} for v in ('1.0', '1.1', '1.2')],
                'events': [{'id': 'B01-D0' + str(i), 'status': 'completed'} for i in (1, 2, 3)]}
        with TemporaryDirectory() as folder:
            seed_path, profile_path = Path(folder) / 'seed.json', Path(folder) / 'profile.json'
            seed_path.write_text(json.dumps(seed), encoding='utf-8')
            profile_path.write_text(json.dumps({'engine': 'nemotron', 'profile': profile}), encoding='utf-8')
            before = seed_path.read_bytes()
            with patch.object(prepare_b01_demo, 'SEED', seed_path), patch.object(prepare_b01_demo, 'PROFILE_RESULT', profile_path):
                self.assertEqual(prepare_b01_demo.main(), 0)
            self.assertEqual(seed_path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
