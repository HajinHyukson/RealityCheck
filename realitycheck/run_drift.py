"""Run one drift assessment (matched control and updated candidates) against a saved company seed.

Usage: python run_drift.py R02 2023-05-10 [--with-assessments]
Makes two hosted Nemotron calls, saves both raw candidates to <id>_drift_<date>.json and attaches the comparison to the seed
under drift_assessments. Operative terms, events and decisions are not changed.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main(cid, review_date, with_assessments=False):
    import app  # loads NVIDIA_API_KEY from the local .env without printing it
    import b01_model
    import drift
    stem = cid.lower()
    seed_path = HERE / (stem + '_seed.json')
    seed = json.loads(seed_path.read_text(encoding='utf-8'))
    # Only what was public by the review date: the package then in effect and the reports then available.
    known = [v for v in seed['versions'] if (v.get('publicly_available_at') or v['effective_at'])[:10] <= review_date]
    version = max(known, key=lambda v: v['effective_at'])
    reports = [e for e in seed['events'] if e['available_at'] <= review_date]
    later = [v for v in seed['versions'] if (v.get('publicly_available_at') or v['effective_at'])[:10] > review_date]
    observed = min(later, key=lambda v: v['effective_at']) if later else None
    model = seed.get('analysis_model') or b01_model.DEFAULT_MODEL
    key = os.environ.get('NVIDIA_API_KEY', '')
    assessments = {}
    if with_assessments:
        for event in sorted(reports, key=lambda e: e['review_date']):
            for finding in (event.get('analysis') or {}).get('attributions', []):
                if finding.get('target_type') == 'assumption' and finding.get('proposed_status'):
                    assessments[finding['target_id']] = {'assumption_id': finding['target_id'], 'status': finding['proposed_status'],
                                                         'review_date': event['review_date'], 'report_id': event['id'], 'rationale': finding.get('rationale', '')}
    suffix = '_with_assessments' if with_assessments else ''
    out_path = HERE / f'{stem}_drift_{review_date}{suffix}.json'
    plain = HERE / f'{stem}_drift_{review_date}.json'
    saved = json.loads(out_path.read_text(encoding='utf-8')) if out_path.exists() else {}
    if with_assessments and 'control' not in saved and plain.exists():
        # The control never sees reports or assessments, so the matched control from the plain run is the same experiment.
        saved['control'] = json.loads(plain.read_text(encoding='utf-8'))['control']
    for mode in ('control', 'updated'):
        if saved.get(mode, {}).get('engine') == 'nemotron':
            continue
        print(json.dumps({'stage': 'drafting', 'mode': mode, 'reports': [r['id'] for r in reports] if mode == 'updated' else []}), flush=True)
        saved[mode] = drift.generate_candidate(cid, seed['profile'], version, reports, mode=mode, review_date=review_date, api_key=key, model=model,
                                                 assessments=list(assessments.values()))
        out_path.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding='utf-8')
        if saved[mode]['engine'] != 'nemotron':
            print(json.dumps({'stage': 'failed', 'mode': mode, 'error': saved[mode]['error']}), flush=True)
            return 1
    comparison = drift.compare(saved['control'], saved['updated'], observed)
    saved['comparison'] = comparison
    out_path.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding='utf-8')
    kept = [a for a in seed.get('drift_assessments', [])
            if (a['review_date'], a.get('assessments_supplied', False)) != (review_date, with_assessments)]
    seed['drift_assessments'] = sorted(kept + [comparison], key=lambda a: (a['review_date'], a.get('assessments_supplied', False)))
    seed_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'stage': 'compared', 'control': comparison['control_judgment'], 'updated': comparison['updated_judgment'],
                      'attributable': [(c['clause_id'], c['change_type']) for c in comparison['evidence_attributable_changes']],
                      'also_in_control': [(c['clause_id'], c['change_type']) for c in comparison['changes_also_in_control']]}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1].upper(), sys.argv[2], '--with-assessments' in sys.argv))
