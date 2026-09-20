import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import b01_model
import benchmark_blind


def stub(system, user, **_):
    """Stand in for the hosted model. Also asserts the blind rules on what each prompt is allowed to contain."""
    assert 'Amendment No' not in user, 'a lender response leaked into a blind prompt'
    if system.startswith('Reconstruct'):
        return {'summary': 's', 'relationships': [], 'assumptions': [
            {'id': 'R02-A01', 'title': 't', 'claim': 'Earnings support leverage.', 'basis': 'inferred', 'source_assumption_id': None, 'covenant_ids': ['C01'],
             'evidence': [{'document_id': 'RMBL-8K-ORIGINATION', 'locator': 'P0049', 'quote': 'its Liquidity to be less than $25,000,000'}]}]}
    if system.startswith('You are drafting a candidate'):
        return {'summary': 's', 'clauses': [{'clause_id': 'C01', 'action': 'retain', 'rationale': 'r'}], 'drift_judgment': 'no_material_drift', 'drift_reasons': 'r'}
    return {'summary': 's', 'attributions': [], 'candidates': [], 'covenant_assessments': []}


class BlindReplayTest(unittest.TestCase):
    def run_workflow(self, tmp, workflow):
        with patch.object(benchmark_blind, 'HERE', Path(tmp)), patch.object(b01_model, '_complete', stub):
            return benchmark_blind.main('R02', workflow)

    def test_blind_replay_keeps_original_package_and_locks(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_workflow(tmp, 'realitycheck'), 0)
            self.assertEqual(self.run_workflow(tmp, 'direct_review'), 0)
            out = Path(tmp) / 'benchmark' / 'R02' / 'blind'
            inputs = json.loads((benchmark_blind.case_folder('R02') / 'blind' / 'inputs.json').read_text(encoding='utf-8'))
            ids = [c['id'] for c in inputs['checkpoints']]
            for cid in ids:
                candidate = json.loads((out / 'realitycheck' / (cid + '_candidate.json')).read_text(encoding='utf-8'))
                self.assertEqual(candidate['package_version'], '1.0')   # no amendment is ever applied
                self.assertTrue(candidate['blind'])
                self.assertTrue((out / 'direct_review' / (cid + '_candidate.json')).exists())
                self.assertTrue((out / 'realitycheck' / (cid + '_attribution.json')).exists())
            # each candidate sees only reports released so far
            first = json.loads((out / 'realitycheck' / (ids[0] + '_candidate.json')).read_text(encoding='utf-8'))
            last = json.loads((out / 'realitycheck' / (ids[-1] + '_candidate.json')).read_text(encoding='utf-8'))
            self.assertEqual(first['report_ids'], ids[:1])
            self.assertEqual(last['report_ids'], ids)
            self.run_workflow(tmp, 'lock')
            self.assertTrue((out / 'lock.json').exists())
            with self.assertRaises(SystemExit):
                self.run_workflow(tmp, 'realitycheck')

    def test_evaluation_requires_an_untampered_lock(self):
        import benchmark_evaluate
        with tempfile.TemporaryDirectory() as tmp:
            self.run_workflow(tmp, 'realitycheck')
            self.run_workflow(tmp, 'direct_review')
            with patch.object(benchmark_evaluate, 'HERE', Path(tmp)):
                with self.assertRaises(SystemExit):          # not locked yet
                    benchmark_evaluate.main('R02')
                self.run_workflow(tmp, 'lock')
                benchmark_evaluate.main('R02')
                result = json.loads((Path(tmp) / 'benchmark' / 'R02' / 'evaluation.json').read_text(encoding='utf-8'))
                stats = result['workflows']['realitycheck']['stats']
                self.assertEqual(stats['checkpoints'], 7)
                self.assertEqual(stats['warranted'] + stats['unwarranted'] + stats['unresolved'], 7)
                self.assertEqual(stats['warranted_detected'], 0)      # the stub retains every clause
                self.assertFalse(any(c['anticipated'] for c in result['workflows']['realitycheck']['correspondence']))
                victim = Path(tmp) / 'benchmark' / 'R02' / 'blind' / 'realitycheck' / 'R02-D01_candidate.json'
                victim.write_text(victim.read_text(encoding='utf-8').replace('no_material_drift', 'material_drift'), encoding='utf-8')
                with self.assertRaises(SystemExit):          # edited after locking
                    benchmark_evaluate.main('R02')

    def test_runner_never_reads_the_evaluator_collection(self):
        source = Path(benchmark_blind.__file__).read_text(encoding='utf-8')
        code = source.split('"""', 2)[2]
        self.assertNotIn('observed_responses', code)
        self.assertNotIn("'evaluator'", code)
        self.assertNotIn("'rolling'", code)


if __name__ == '__main__':
    unittest.main()
