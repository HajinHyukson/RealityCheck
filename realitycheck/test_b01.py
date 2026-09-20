"""State/ingestion checks use a temporary database and no hosted requests."""
import copy
import importlib.util
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch


class B01StoreTest(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('b01'), 'B01 store is not implemented')
        import b01
        self.b = b01
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / 'demo.sqlite'
        self.seed = Path(self.tmp.name) / 'seed.json'
        versions = [{'version': v, 'effective_at': d, 'clauses': [{'id':'S2','clause':c}], 'terms':{}}
                    for v,d,c in [('1.0','2026-12-31','old'),('1.1','2027-07-20','old'),('1.2','2027-08-23','new')]]
        self.data = {'borrower':{'id':'B01','name':'Synthetic test'},
            'profile':{'summary':'Baseline','assumptions':[{'id':'B01-A01','claim':'Original claim'}]},
            'profile_provenance':{'engine':'nemotron'}, 'versions':versions,
            'events':[{'id':'B01-D03','title':'Pending source','event_date':'2027-09-07',
                'available_at':'2027-09-10','review_date':'2027-09-10','package_version':'1.2',
                'status':'completed','sources':[],'analysis':{'engine':'nemotron','attributions':[]},
                'decision':{'action':'pending'}}],
            'pending_proposal':{'version':'1.3','parent_version':'1.2','trigger_event_id':'B01-D03',
                'status':'proposed','title':'Draft','changes':[{'clause_id':'S2','before':'new','after':'revised'}]},
            'presentation':{'as_of':'2027-09-10'}}
        self.seed.write_text(json.dumps(self.data), encoding='utf-8')
        self.b.initialize(self.db,self.seed)

    def body(self, **kwargs):
        return {'title':'New company update','text':'A dated source statement.',
                'available_at':'2027-09-11','review_date':'2027-09-11', **kwargs}

    def test_seed_has_two_amendments_and_pending_third(self):
        s=self.b.snapshot(self.db)
        self.assertEqual(s['current_version'],'1.2')
        self.assertEqual(len(s['versions']),3)
        self.assertEqual(s['events'][0]['decision']['action'],'pending')
        self.b.initialize(self.db,self.seed)
        self.assertEqual(len(self.b.snapshot(self.db)['events']),1)

    def test_queue_is_idempotent_and_selects_historical_version(self):
        body=self.body(available_at='2027-08-10',review_date='2027-08-10')
        a=self.b.enqueue(body,'database_update',self.db,dedupe_key='one')
        b=self.b.enqueue(body,'database_update',self.db,dedupe_key='one')
        self.assertEqual(a['event_id'],b['event_id'])
        event=self.b.snapshot(self.db)['events'][-1]
        self.assertEqual(event['package_version'],'1.1')
        self.assertEqual(event['status'],'queued')

    def test_unavailable_future_source_is_rejected(self):
        with self.assertRaises(ValueError):
            self.b.enqueue(self.body(review_date='2027-09-09'),'manual',self.db)

    def test_updates_cannot_cross_borrower_profiles(self):
        with self.assertRaisesRegex(ValueError,'B01'):
            self.b.enqueue(self.body(borrower_id='B02'),'database_update',self.db)
        self.assertEqual(len(self.b.snapshot(self.db)['events']),1)

    def test_late_received_event_uses_terms_at_occurrence(self):
        self.b.enqueue(self.body(event_date='2027-08-09'),'manual',self.db)
        self.assertEqual(self.b.snapshot(self.db)['events'][-1]['package_version'],'1.1')

    def test_results_preserve_baseline_and_history(self):
        baseline=copy.deepcopy(self.b.snapshot(self.db)['profile'])
        event_id=self.b.enqueue(self.body(),'manual',self.db)['event_id']
        self.b.finish(event_id,{'engine':'nemotron','attributions':[{'target_type':'assumption',
            'target_id':'B01-A01','proposed_status':'weakened'}]},self.db)
        s=self.b.snapshot(self.db)
        self.assertEqual(s['profile'],baseline)
        self.assertEqual(len(s['events']),2)
        self.assertEqual(s['current_profile']['assessments']['B01-A01']['status'],'weakened')
        self.assertEqual(s['current_version'],'1.2')

    def test_adoption_checks_parent_and_does_not_backdate(self):
        with self.assertRaises(ValueError):
            self.b.decide({'event_id':'B01-D03','action':'adopt','reason':'test','effective_at':'2027-09-08'},self.db)
        s=self.b.decide({'event_id':'B01-D03','action':'adopt','reason':'test','effective_at':'2027-09-11'},self.db)
        self.assertEqual(s['current_version'],'1.3')
        self.assertEqual(s['versions'][-1]['clauses'][0]['clause'],'revised')
        self.assertEqual(s['versions'][2]['clauses'][0]['clause'],'new')
        self.assertIn('2027-09-11',s['versions'][-1]['instrument_text'])
        with self.assertRaises(ValueError):
            self.b.decide({'event_id':'B01-D03','action':'adopt','reason':'again','effective_at':'2027-09-12'},self.db)

    def test_dismissal_keeps_package_and_retains_detection(self):
        s=self.b.decide({'event_id':'B01-D03','action':'dismiss','reason':'Keep terms'},self.db)
        self.assertEqual(s['current_version'],'1.2')
        self.assertEqual(s['events'][0]['decision']['action'],'dismissed')
        self.assertIsNone(s['pending_proposal'])

    def test_analyst_can_write_an_amendment_without_a_prepared_proposal(self):
        with self.b.connection(self.db) as con:
            self.b._put(con,'pending_proposal',None)
        amend=lambda **kw:self.b.decide({'event_id':'B01-D03','action':'amend','reason':'Floor is too low','effective_at':'2027-09-11',
                                         'changes':[{'clause_id':'S2','before':'new','after':'analyst text'}],**kw},self.db)
        for bad in ([],[{'clause_id':'S2','before':'new','after':'new'}],[{'clause_id':'S9','before':'new','after':'x'}],
                    [{'clause_id':'S2','before':'old','after':'x'}]):   # nothing changed, unknown clause, edited against stale text
            with self.assertRaises(ValueError):
                amend(changes=bad)
        with self.assertRaises(ValueError):
            amend(effective_at='2027-09-08')
        s=amend()
        self.assertEqual((s['current_version'],s['versions'][-1]['parent_version']),('1.3','1.2'))
        self.assertEqual(s['versions'][-1]['clauses'][0]['clause'],'analyst text')
        self.assertEqual(s['versions'][2]['clauses'][0]['clause'],'new')   # the earlier version is preserved
        self.assertEqual(s['events'][0]['decision']['action'],'adopted')
        self.assertEqual(s['events'][0]['reviewed_proposal']['changes'][0]['after'],'analyst text')

    def test_file_ingestion_deduplicates_and_reports_bad_input(self):
        inbox=Path(self.tmp.name)/'inbox'; inbox.mkdir()
        (inbox/'update.json').write_text(json.dumps(self.body()),encoding='utf-8')
        (inbox/'bad.json').write_text('{',encoding='utf-8')
        self.b.scan_inbox(self.db,inbox)
        self.b.scan_inbox(self.db,inbox)
        s=self.b.snapshot(self.db)
        self.assertEqual(len(s['events']),2)
        self.assertTrue(s['feed']['errors'])

    def test_http_event_submission_and_invalid_decision(self):
        import app
        with patch.object(app.b01,'DB_PATH',self.db), patch.object(app.b01,'SEED_PATH',self.seed):
            server=app.ThreadingHTTPServer(('127.0.0.1',0),app.H)
            thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
            try:
                base='http://127.0.0.1:'+str(server.server_port)
                req=urllib.request.Request(base+'/api/b01/events',data=json.dumps(self.body()).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req) as response:
                    self.assertEqual(response.status,202)
                    self.assertEqual(json.load(response)['status'],'queued')
                with urllib.request.urlopen(base+'/api/b01') as response:
                    self.assertEqual(len(json.load(response)['events']),2)
                req=urllib.request.Request(base+'/api/b01/decision',data=json.dumps({'event_id':[], 'action':'adopt','reason':'test'}).encode())
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(req)
                self.assertEqual(error.exception.code,400)
                error.exception.close()
            finally:
                server.shutdown(); server.server_close(); thread.join()

    def test_report_library_introduces_live_or_recorded_once(self):
        folder=Path(self.tmp.name)/'reports'; (folder/'recorded').mkdir(parents=True)
        report={'borrower_id':'B01','title':'Industry analysis','report_type':'industry_analysis','library_summary':'s',
                'event_date':'2027-09-13','available_at':'2027-09-14','review_date':'2027-09-14',
                'sources':[{'document_id':'EXT-1','locator':'P1','text':'An external statement.'}]}
        for name in ('a.json','b.json'):
            (folder/name).write_text(json.dumps(report),encoding='utf-8')
        listed=self.b.library(self.db,folder)
        self.assertEqual([r['introduced'] for r in listed],[False,False])
        self.assertFalse(listed[0]['recorded_available'])
        with self.assertRaisesRegex(ValueError,'No recorded analysis'):
            self.b.introduce({'name':'a.json','mode':'recorded'},self.db,folder)
        with self.assertRaises(ValueError):
            self.b.introduce({'name':'../seed.json','mode':'live'},self.db,folder)
        first=self.b.introduce({'name':'a.json','mode':'live'},self.db,folder)
        self.assertEqual(first['status'],'queued')
        self.assertTrue(self.b.introduce({'name':'a.json','mode':'live'},self.db,folder)['duplicate'])
        recorded={**report,'id':'OLD','package_version':'1.2','status':'completed','decision':{'action':'pending'},
                  'analysis':{'engine':'nemotron','model':'m','generated_at':'2026-09-19T00:00:00+00:00','attributions':[]}}
        (folder/'recorded'/'b.json').write_text(json.dumps(recorded),encoding='utf-8')
        result=self.b.introduce({'name':'b.json','mode':'recorded'},self.db,folder)
        self.assertTrue(result['recorded_replay'])
        event=next(e for e in self.b.snapshot(self.db)['events'] if e['id']==result['event_id'])
        self.assertEqual(event['source_kind'],'recorded_replay')
        self.assertEqual(event['analysis']['generated_at'],'2026-09-19T00:00:00+00:00')   # original provenance kept
        self.assertEqual([r['introduced'] for r in self.b.library(self.db,folder)],[True,True])
        stale={**recorded,'package_version':'1.1'}
        (folder/'c.json').write_text(json.dumps(report),encoding='utf-8')
        (folder/'recorded'/'c.json').write_text(json.dumps(stale),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'now governs'):
            self.b.introduce({'name':'c.json','mode':'recorded'},self.db,folder)

    def test_a_detection_is_a_finding_worse_than_the_earlier_one(self):
        def report(i,status,covenants=()):
            return {'id':'E'+str(i),'review_date':'2027-0'+str(i)+'-01','analysis':{'attributions':[{'target_id':'A1','proposed_status':status}],
                    'covenant_assessments':[dict(zip(('status','already_assessed_in'),c)) for c in covenants]}}
        events=[report(1,'supported'),report(2,'contradicted'),report(3,'weakened'),report(4,'contradicted'),
                report(5,'supported',[('noncompliant','E4')]),report(6,'supported',[('noncompliant',None)])]
        self.assertEqual([self.b.is_detection(e,events) for e in events],[False,True,False,True,False,True])

    def test_second_company_is_isolated_and_routed(self):
        import app
        home=Path(self.tmp.name)
        other=dict(self.data,borrower={'id':'B02','name':'Second synthetic'},events=[],pending_proposal=None)
        (home/'b02_seed.json').write_text(json.dumps(other),encoding='utf-8')
        with patch.object(app.b01,'HERE',home), patch.object(app.b01,'DB_PATH',self.db), patch.object(app.b01,'SEED_PATH',self.seed):
            self.assertEqual(app.b01.companies(),['B01','B02'])
            db2,seed2,_=app.b01.paths('B02')
            self.assertNotEqual(db2,self.db)
            server=app.ThreadingHTTPServer(('127.0.0.1',0),app.H)
            thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
            try:
                base='http://127.0.0.1:'+str(server.server_port)
                req=urllib.request.Request(base+'/api/b02/events',data=json.dumps(self.body()).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req) as response:
                    self.assertTrue(json.load(response)['event_id'].startswith('B02-E-'))
                with urllib.request.urlopen(base+'/api/b02') as response:
                    self.assertEqual(json.load(response)['borrower']['id'],'B02')
                with urllib.request.urlopen(base+'/api/b01') as response:
                    self.assertEqual(len(json.load(response)['events']),1)
                with urllib.request.urlopen(base+'/api/companies') as response:
                    self.assertEqual([c['id'] for c in json.load(response)['companies']],['B01','B02'])
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base+'/api/b03')
                self.assertEqual(error.exception.code,404)
                error.exception.close()
                with self.assertRaisesRegex(ValueError,'B02'):
                    app.b01.enqueue(self.body(borrower_id='B01'),'manual',db2)
            finally:
                server.shutdown(); server.server_close(); thread.join()


if __name__ == '__main__':
    unittest.main()
