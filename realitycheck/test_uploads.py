"""Upload lifecycle checks use isolated storage and a mocked hosted completion boundary."""
import base64
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

import b01
import b01_model


class UploadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root_patch = patch.object(b01, 'UPLOAD_ROOT', Path(self.temp.name), create=True)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.text = 'The borrower sells recurring software subscriptions. The borrower shall deliver monthly accounts within 30 days.'

    def file(self, text=None, filename='agreement.txt'):
        return {'filename': filename, 'b64': base64.b64encode((text or self.text).encode()).decode()}

    def completion(self, system, user, **kwargs):
        request = json.loads(user)
        cid = request['borrower_id']
        source = request['sources'][0]
        citation = {k: source[k] for k in ('document_id', 'locator')}
        if 'clause extraction' in system:
            return {'clauses': [{'id': 'C01', 'title': 'Monthly accounts', 'source': citation,
                                 'start': 'The borrower shall deliver', 'end': 'within 30 days.'}], 'missing_inputs': ['Financial statements']}
        return {'summary': 'Subscriptions support recurring cash generation.', 'assumptions': [
            {'id': cid + '-A01', 'title': 'Recurring subscriptions', 'claim': 'Subscriptions continue generating cash.',
             'basis': 'inferred', 'source_assumption_id': None, 'covenant_ids': ['C01'],
             'evidence': [{**citation, 'quote': self.text.split('. ')[0]}]}], 'relationships': []}

    def test_pending_ready_report_and_storage_isolation(self):
        import uploads
        row = uploads.create_company({'name': 'Upload test', 'effective_at': '2026-01-01', 'files': [self.file()]})
        self.assertEqual(row['status'], 'queued')
        db, seed, _ = b01.paths(row['id'])
        self.assertTrue(db.is_relative_to(Path(self.temp.name)))
        self.assertFalse(b01.snapshot(db)['ready'])
        with patch.object(b01_model, '_complete', side_effect=self.completion):
            self.assertTrue(uploads.process_company(row['id'], '', 'mock-model'))
        state = b01.snapshot(db)
        self.assertTrue(state['ready'])
        self.assertEqual(state['status'], 'ready')
        self.assertEqual(state['borrower']['source_mode'], 'uploaded_agreement')
        self.assertEqual(state['versions'][0]['terms'], {})
        self.assertEqual(state['versions'][0]['clauses'][0]['clause'], self.text.split('. ')[1])   # copied from the source between the anchors
        self.assertEqual(len(state['uploaded_documents']), 1)
        job = uploads.enqueue_report({'files': [self.file('Revenue fell by ten percent.', 'report.md')],
                                     'available_at': '2026-02-01'}, db)
        queued = b01.snapshot(db)['events'][-1]
        self.assertEqual(queued['id'], job['event_id'])
        self.assertEqual(queued['status'], 'queued')
        def analyze(system, user, **kwargs):
            request = json.loads(user)
            self.assertEqual(request['event']['sources'][0]['text'], 'Revenue fell by ten percent.')
            self.assertEqual(request['package_version']['terms'], {})
            self.assertEqual(b01.snapshot(db)['events'][-1]['status'], 'processing')
            return {'summary': 'Revenue decreased.', 'attributions': [], 'candidates': [], 'covenant_assessments': []}
        with patch.object(b01_model, '_complete', side_effect=analyze):
            self.assertTrue(b01.process_one('', 'mock-model', db))
        self.assertEqual(b01.snapshot(db)['events'][-1]['status'], 'completed')
        self.assertEqual(len(b01.snapshot(db)['uploaded_documents']), 2)
        uploads.enqueue_report({'files': [self.file('invalid image', 'report.png')], 'available_at': '2026-02-02'}, db)
        with patch('parse.parse_upload', side_effect=RuntimeError('Parse service unavailable')), patch.object(b01_model, '_complete') as model:
            b01.process_one('', 'mock-model', db)
        failed = b01.snapshot(db)['events'][-1]
        self.assertEqual(failed['status'], 'failed')
        self.assertIn('Parse service unavailable', failed['analysis']['error'])
        model.assert_not_called()

    def test_missing_key_is_persisted_failure_and_never_ready(self):
        import uploads
        row = uploads.create_company({'name': 'No key', 'files': [self.file()]})
        uploads.process_company(row['id'], '', 'mock-model')
        state = b01.snapshot(b01.paths(row['id'])[0])
        self.assertFalse(state['ready'])
        self.assertEqual(state['status'], 'failed')
        self.assertIn('NVIDIA_API_KEY', state['error'])
        retry = uploads.retry_company(row['id'])
        self.assertEqual(retry['id'], row['id'])
        self.assertEqual(retry['status'], 'queued')
        self.assertEqual(len(retry['uploaded_documents']), 1)
        with self.assertRaises(ValueError):
            uploads.retry_company(row['id'])

    def test_invalid_files_leave_no_company(self):
        import uploads
        for item in [self.file(filename='../bad.txt'), self.file(filename='bad.exe'), {'filename': 'a.txt', 'b64': '!!!'}]:
            with self.subTest(item=item['filename']), self.assertRaises(ValueError):
                uploads.create_company({'name': 'Bad', 'files': [item]})
        self.assertEqual(list(Path(self.temp.name).iterdir()), [])

    def test_inception_document_roles_are_persisted_and_reports_force_report(self):
        import uploads
        row = uploads.create_company({'name': 'Source roles', 'files': [
            self.file(), self.file(filename='underwriting-memo.md'), self.file(filename='annual-10-K.txt'),
            {**self.file(filename='supporting.txt'), 'role': '10k'}]})
        self.assertEqual([d['role'] for d in row['uploaded_documents']], ['agreement', 'memo', '10k', '10k'])
        with self.assertRaises(ValueError):
            uploads.create_company({'name': 'Invalid role', 'files': [{**self.file(), 'role': 'arbitrary'}]})
        files = uploads.validated_files({'files': [{**self.file(filename='memo.txt'), 'role': 'memo'}]}, reports=True)
        records = uploads.store_documents(row['id'], files, 'report')
        self.assertEqual(records[0]['role'], 'report')

    def test_full_annual_filing_reaches_profile_without_becoming_agreement_terms(self):
        import pymupdf
        import uploads
        with pymupdf.open() as pdf:
            for number in range(1, 124):
                page = pdf.new_page()
                page.insert_textbox(page.rect + (36, 36, -36, -36),
                                    f'Annual filing page {number}.\n' + 'Subscription revenue and operating risks.\n' * 40)
            filing = {'filename': 'annual-10-K.pdf', 'role': '10k',
                      'b64': base64.b64encode(pdf.tobytes()).decode()}
        row = uploads.create_company({'name': 'Full filing', 'files': [filing, self.file()]})
        def complete(system, user, **kwargs):
            payload = json.loads(user)
            if 'clause extraction' in system:
                self.assertEqual([s['role'] for s in payload['sources']], ['agreement'])
            else:
                filing_sources = [s for s in payload['sources'] if s['role'] == '10k']
                self.assertEqual(len(filing_sources), 123)
                self.assertGreater(sum(len(s['text']) for s in filing_sources), 120000)
                self.assertIn('Annual filing page 123.', filing_sources[-1]['text'])
                self.assertIn('(p123)', filing_sources[-1]['locator'])
                # Return a real source-verified assumption from the agreement.
                payload['sources'] = [s for s in payload['sources'] if s['role'] == 'agreement']
            return self.completion(system, json.dumps(payload), **kwargs)
        with patch('parse.parse_image', side_effect=AssertionError('Text PDFs must not call OCR')), \
                patch.object(b01_model, '_complete', side_effect=complete):
            uploads.process_company(row['id'], '', 'mock-model')
        state = b01.snapshot(b01.paths(row['id'])[0])
        self.assertTrue(state['ready'], state.get('error'))
        self.assertNotIn('Annual filing page', state['versions'][0]['instrument_text'])
        self.assertIn(self.text, state['versions'][0]['instrument_text'])

    def test_supporting_filing_cannot_supply_operative_clauses(self):
        import uploads
        row = uploads.create_company({'name': 'Wrong clause source', 'files': [
            self.file(), self.file('The issuer shall retain cash.', 'annual-10-K.txt')]})
        filing = row['uploaded_documents'][1]
        with patch.object(b01_model, '_complete', return_value={'clauses': [
                {'id': 'C01', 'title': 'Cash', 'start': 'The issuer shall', 'end': 'retain cash.',
                 'source': {'document_id': filing['id'], 'locator': 'Full document'}}]}):
            uploads.process_company(row['id'], '', 'mock-model')
        state = b01.snapshot(b01.paths(row['id'])[0])
        self.assertFalse(state['ready'])
        self.assertIn('source verification', state['error'])

    def test_clause_runs_to_the_end_of_its_paragraph_and_never_into_the_next(self):
        import uploads
        text = ('C01 Minimum cash\nCash must be at least $25 at each month-end.\nEquality with the floor is compliant.\n\n'
                'C02 Leverage\nLeverage must not exceed 2.50 times.\n\nC03 Reporting\nDeliver monthly accounts.')
        row = uploads.create_company({'name': 'Loose end anchors', 'files': [self.file(text)]})
        def complete(system, user, **kwargs):
            if 'clause extraction' not in system:
                return self.completion(system, user, **kwargs)
            source = json.loads(user)['sources'][0]
            cite = {'source': {k: source[k] for k in ('document_id', 'locator')}}
            return {'clauses': [{'id': 'C01', 'title': 'Minimum cash', **cite, 'start': 'C01 Minimum cash', 'end': 'at each month-end.'},   # stops early
                                {'id': 'C02', 'title': 'Leverage', **cite, 'start': 'C02 Leverage', 'end': 'Deliver monthly accounts.'},     # overshoots into C03
                                {'id': 'C03', 'title': 'Reporting', **cite, 'start': 'C03 Reporting', 'end': 'Deliver monthly accounts.'}]}
        with patch.object(b01_model, '_complete', side_effect=complete):
            uploads.process_company(row['id'], '', 'mock-model')
        origin = json.loads((b01.paths(row['id'])[0].parent / 'origination.json').read_text(encoding='utf-8'))
        self.assertEqual([c['clause'] for c in origin['contract']['clauses']],
                         ['C01 Minimum cash Cash must be at least $25 at each month-end. Equality with the floor is compliant.',
                          'C02 Leverage Leverage must not exceed 2.50 times.', 'C03 Reporting Deliver monthly accounts.'])

    def test_red_flag_report_queues_one_drift_check_and_the_button_reuses_the_cached_control(self):
        import uploads
        row = uploads.create_company({'name': 'Drift trigger', 'effective_at': '2026-01-01', 'files': [self.file()]})
        db = b01.paths(row['id'])[0]
        drafted = []
        def complete(system, user, **kwargs):
            payload = json.loads(user)
            if 'candidate covenant package' in system:
                drafted.append(payload['mode'])
                return {'summary': 'Protections still fit.', 'clauses': [{'clause_id': 'C01', 'action': 'retain', 'rationale': 'Unchanged.'}],
                        'drift_judgment': 'no_material_drift', 'drift_reasons': 'No evidence of drift.'}
            if 'event' in payload:
                source = payload['event']['sources'][0]
                return {'summary': 'Revenue decreased.', 'candidates': [], 'covenant_assessments': [], 'attributions': [
                    {'target_type': 'assumption', 'target_id': row['id'] + '-A01', 'relation_type': 'direct_assumption_evidence',
                     'risk_direction': 'adverse', 'proposed_status': 'weakened', 'rationale': 'Revenue fell.',
                     'evidence': [{'document_id': source['document_id'], 'locator': source['locator'], 'quote': 'Revenue fell by ten percent.'}],
                     'counterevidence': [], 'missing_information': [], 'suggested_action': 'review_assumption',
                     'proposed_adjustment': 'Revisit the cash assumption.', 'path': []}]}
            return self.completion(system, user, **kwargs)
        with patch.object(b01_model, '_complete', side_effect=complete):
            uploads.process_company(row['id'], '', 'mock-model')
            with self.assertRaisesRegex(ValueError, 'at least one analyzed report'):
                b01.request_drift(db)
            uploads.enqueue_report({'files': [self.file('Revenue fell by ten percent.', 'report.md')], 'available_at': '2026-02-01'}, db)
            self.assertTrue(b01.process_one('', 'mock-model', db))
            job = b01.snapshot(db)['drift_job']
            self.assertEqual((job['status'], job['triggered_by'][0]['kind']), ('queued', 'red_flag'))   # no click needed
            self.assertTrue(b01.process_drift('', 'mock-model', db))
            state = b01.snapshot(db)
            self.assertEqual(state['drift_job']['status'], 'done', state['drift_job'].get('error'))
            self.assertEqual(state['drift_assessments'][0]['triggered_by'][0]['kind'], 'red_flag')
            self.assertEqual(drafted, ['control', 'updated'])
            b01.request_drift(db)                                                                      # the Run drift check button
            self.assertTrue(b01.process_drift('', 'mock-model', db))
        self.assertEqual(drafted, ['control', 'updated', 'updated'])                                   # control drafted once per agreement version
        state = b01.snapshot(db)
        self.assertEqual([a['triggered_by'][0]['kind'] for a in state['drift_assessments']], ['manual'])  # same review date: replaced, not duplicated

    def test_delete_removes_a_finished_upload_and_refuses_pending_or_seeded_companies(self):
        import uploads
        row = uploads.create_company({'name': 'To delete', 'files': [self.file()]})
        folder = b01.paths(row['id'])[0].parent
        with self.assertRaisesRegex(ValueError, 'still working'):   # queued: the worker may claim it at any moment
            uploads.delete_company(row['id'])
        with patch.object(b01_model, '_complete', side_effect=self.completion):
            uploads.process_company(row['id'], '', 'mock-model')
        self.assertEqual(uploads.delete_company(row['id']), {'id': row['id'], 'deleted': True})
        self.assertFalse(folder.exists())
        self.assertNotIn(row['id'], b01.companies())
        for cid in ('B01', row['id']):   # seeded demo companies and already-deleted uploads
            with self.assertRaisesRegex(ValueError, 'Only an uploaded'):
                uploads.delete_company(cid)

    def test_copy_is_an_independent_workspace_with_its_own_ids(self):
        import uploads
        row = uploads.create_company({'name': 'Demo 1', 'effective_at': '2026-01-01', 'files': [self.file()]})
        with self.assertRaisesRegex(ValueError, 'still working'):
            uploads.copy_company(row['id'])
        with patch.object(b01_model, '_complete', side_effect=self.completion):
            uploads.process_company(row['id'], '', 'mock-model')
        uploads.enqueue_report({'files': [self.file('Revenue fell.', 'report.md')], 'available_at': '2026-02-01'}, b01.paths(row['id'])[0])
        with self.assertRaisesRegex(ValueError, 'still working'):   # a queued report would be analyzed twice
            uploads.copy_company(row['id'])
        b01.finish(b01.snapshot(b01.paths(row['id'])[0])['events'][0]['id'], {'engine': 'nemotron', 'attributions': []}, b01.paths(row['id'])[0])
        copy = uploads.copy_company(row['id'])
        self.assertNotEqual(copy['id'], row['id'])
        self.assertEqual(copy['borrower']['name'], 'Demo 2')
        self.assertIn(copy['id'], b01.companies())
        state = b01.snapshot(b01.paths(copy['id'])[0])
        self.assertNotIn(row['id'], json.dumps(state))   # assumption, event and download ids all point at the copy
        self.assertTrue(state['events'][0]['id'].startswith(copy['id']))
        self.assertTrue(uploads.document_path(copy['id'], state['uploaded_documents'][0]['id']).exists())
        uploads.delete_company(row['id'])
        self.assertTrue(b01.snapshot(b01.paths(copy['id'])[0])['ready'])   # the copy survives its original

    def test_fabricated_clause_is_failed(self):
        import uploads
        row = uploads.create_company({'name': 'Bad quote', 'files': [self.file()]})
        with patch.object(b01_model, '_complete', return_value={'clauses': [
            {'id': 'C01', 'title': 'Invented', 'start': 'Invented', 'end': 'duty.',
             'source': {'document_id': 'agreement.txt', 'locator': 'Full document'}}]}):
            uploads.process_company(row['id'], '', 'mock-model')
        state = b01.snapshot(b01.paths(row['id'])[0])
        self.assertFalse(state['ready'])
        self.assertEqual(state['status'], 'failed')

    def test_mistyped_document_id_is_relocated_by_the_verbatim_anchor(self):
        import uploads
        row = uploads.create_company({'name': 'Typo id', 'files': [self.file()]})
        def complete(system, user, **kwargs):
            result = self.completion(system, user, **kwargs)
            if 'clause extraction' in system:
                result['clauses'][0]['source']['document_id'] = result['clauses'][0]['source']['document_id'][1:]   # one hex character dropped
            return result
        with patch.object(b01_model, '_complete', side_effect=complete):
            uploads.process_company(row['id'], '', 'mock-model')
        state = b01.snapshot(b01.paths(row['id'])[0])
        self.assertTrue(state['ready'], state.get('error'))
        clause = state['versions'][0]['clauses'][0]
        self.assertEqual(clause['source']['document_id'], row['uploaded_documents'][0]['id'])
        self.assertEqual(clause['clause'], self.text.split('. ')[1])

    def test_one_degenerate_clause_response_is_retried(self):
        import uploads
        row = uploads.create_company({'name': 'Degenerate once', 'files': [self.file()]})
        calls = []
        def complete(system, user, **kwargs):
            if 'clause extraction' in system:
                calls.append(1)
                if len(calls) == 1:
                    return {'clauses': [{'id': 'C01', 'title': 'Monthly accounts      '}, 'start       ']}
            return self.completion(system, user, **kwargs)
        with patch.object(b01_model, '_complete', side_effect=complete):
            uploads.process_company(row['id'], '', 'mock-model')
        state = b01.snapshot(b01.paths(row['id'])[0])
        self.assertTrue(state['ready'], state.get('error'))
        self.assertEqual(len(calls), 2)

    def test_uploaded_profile_schema_has_no_explicit_claim_option(self):
        import uploads
        row = uploads.create_company({'name': 'Profile schema', 'files': [self.file()]})
        def complete(system, user, **kwargs):
            payload = json.loads(user)
            if 'clause extraction' not in system:
                schema = payload['response_schema']
                self.assertEqual(schema['assumptions'][0]['basis'], 'inferred')
                self.assertIsNone(schema['assumptions'][0]['source_assumption_id'])
            return self.completion(system, user, **kwargs)
        with patch.object(b01_model, '_complete', side_effect=complete):
            uploads.process_company(row['id'], '', 'mock-model')
        self.assertTrue(b01.snapshot(b01.paths(row['id'])[0])['ready'])

    def test_http_accepts_pending_company_and_downloads_exact_original(self):
        import app
        server = app.ThreadingHTTPServer(('127.0.0.1', 0), app.H)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        base = f'http://127.0.0.1:{server.server_port}'
        request = urllib.request.Request(base + '/api/companies', data=json.dumps(
            {'name': 'HTTP company', 'files': [self.file()]}).encode(), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request) as response:
            self.assertEqual(response.status, 202)
            row = json.load(response)
        with patch.object(b01, 'companies', return_value=[row['id']]):
            with urllib.request.urlopen(base + '/api/companies') as response:
                listed = json.load(response)['companies'][0]
            self.assertFalse(listed['ready'])
            self.assertEqual(listed['status'], 'queued')
            self.assertEqual(listed['borrower']['name'], 'HTTP company')
            with urllib.request.urlopen(base + row['uploaded_documents'][0]['download_url']) as response:
                self.assertEqual(response.read().decode(), self.text)
                self.assertIn('attachment', response.headers['Content-Disposition'])
            with urllib.request.urlopen(base + '/api/' + row['id'].lower()) as response:
                self.assertEqual(json.load(response)['status'], 'queued')
            request = urllib.request.Request(base + '/api/' + row['id'].lower() + '/upload', data=json.dumps(
                {'files': [self.file()]}).encode(), headers={'Content-Type': 'application/json'})
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(request)
            self.assertEqual(error.exception.code, 400)
            error.exception.close()

    def test_worker_start_recovers_interrupted_onboarding(self):
        import uploads
        row = uploads.create_company({'name': 'Interrupted', 'files': [self.file()]})
        db, _, _ = b01.paths(row['id'])
        with b01.connection(db) as con:
            job = b01._get(con, 'onboarding')
            job['status'] = 'processing'
            b01._put(con, 'onboarding', job)
        with patch.object(b01, '_worker', None), patch.object(b01, 'companies', return_value=[row['id']]), patch('threading.Thread.start'):
            b01.start_worker('', 'test')
        self.assertEqual(b01.snapshot(db)['status'], 'queued')

    def test_workers_run_companies_in_parallel_but_never_one_company_twice(self):
        import uploads
        ids = [uploads.create_company({'name': name, 'files': [self.file()]})['id'] for name in ('One', 'Two')]
        active, overlaps, both = set(), [], threading.Event()
        def process(cid, api_key, model):
            if cid in active:
                overlaps.append(cid)
            active.add(cid)
            if len(active) == 2:
                both.set()
            both.wait(5)
            active.discard(cid)
            b01._stop.set()
            return False
        self.addCleanup(b01._stop.clear)
        with patch.object(b01, '_worker', None), patch.object(b01, 'companies', return_value=ids), \
                patch.object(uploads, 'process_company', process):
            b01.start_worker('', 'test')
            for thread in threading.enumerate():
                if thread.name.startswith('company-updates'):
                    thread.join(10)
        self.assertTrue(both.is_set(), 'two companies were never in flight together')
        self.assertEqual(overlaps, [])


if __name__ == '__main__':
    unittest.main()
