"""Candidate-package comparison for a demo company: would we write this package today?

Usage: python run_b01_drift.py B01 2027-09-10            # two hosted calls; results saved to b01_drift_2027-09-10.json only
       python run_b01_drift.py B01 2027-09-10 --attach   # back up the database, then add the saved comparison to it

The run reads the company database and changes nothing in it. Attaching is a separate, explicit step: it writes one metadata
entry (drift_assessments). Events, decisions, package versions and the pending proposal are never touched.
For a synthetic demo company the comparison shown beside the candidate is the authored draft proposal, a scenario fixture,
not a lender's response.
"""
from datetime import datetime, timezone
import json
import os
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main(cid, review_date, attach):
    import app  # loads NVIDIA_API_KEY from the local .env without printing it
    import b01
    import b01_model
    import drift
    db, _, _ = b01.paths(cid)
    out_path = HERE / f'{cid.lower()}_drift_{review_date}.json'
    if attach:
        saved = json.loads(out_path.read_text(encoding='utf-8'))
        backup = HERE / f"{cid.lower()}_before_drift_attach_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.sqlite"
        source = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        target = sqlite3.connect(str(backup))
        source.backup(target)
        source.close(); target.close()
        with b01.connection(db) as con:
            kept = [a for a in b01._get(con, 'drift_assessments', []) if a['review_date'] != review_date]
            b01._put(con, 'drift_assessments', sorted(kept + [saved['comparison']], key=lambda a: a['review_date']))
        print(json.dumps({'stage': 'attached', 'backup': backup.name, 'review_date': review_date}))
        return 0
    state = b01.snapshot(db)
    known = [v for v in state['versions'] if v['effective_at'] <= review_date]
    version = max(known, key=lambda v: v['effective_at'])
    reports = [e for e in state['events'] if e['status'] == 'completed' and e['available_at'] <= review_date]
    assessments = {}
    for event in sorted(reports, key=lambda e: e['review_date']):
        for finding in (event.get('analysis') or {}).get('attributions', []):
            if finding.get('target_type') == 'assumption' and finding.get('proposed_status'):
                assessments[finding['target_id']] = {'assumption_id': finding['target_id'], 'status': finding['proposed_status'],
                                                     'review_date': event['review_date'], 'report_id': event['id'], 'rationale': finding.get('rationale', '')}
    model = os.environ.get('B01_NEMOTRON_MODEL') or state.get('analysis_model') or b01_model.DEFAULT_MODEL
    key = os.environ.get('NVIDIA_API_KEY', '')
    saved = json.loads(out_path.read_text(encoding='utf-8')) if out_path.exists() else {}
    for mode in ('control', 'updated'):
        if saved.get(mode, {}).get('engine') == 'nemotron':
            continue
        print(json.dumps({'stage': 'drafting', 'mode': mode, 'package': version['version'], 'reports': [r['id'] for r in reports] if mode == 'updated' else []}), flush=True)
        saved[mode] = drift.generate_candidate(cid, state['profile'], version, reports, mode=mode, review_date=review_date, api_key=key, model=model,
                                                 assessments=list(assessments.values()))
        out_path.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding='utf-8')
        if saved[mode]['engine'] != 'nemotron':
            print(json.dumps({'stage': 'failed', 'mode': mode, 'error': saved[mode]['error']}), flush=True)
            return 1
    proposal = state.get('pending_proposal')
    comparison = drift.compare(saved['control'], saved['updated'], proposal if proposal and proposal.get('parent_version') == version['version'] else None)
    if 'observed_response' in comparison:
        comparison['observed_response']['kind'] = 'authored_draft_proposal'
        comparison['observed_response']['note'] = ('The draft proposal is an authored scenario fixture for this fictional company, shown for comparison. It was not available to either '
                                                   'candidate run. Overlap means the same clauses were touched; it says nothing about direction or merit.')
    saved['comparison'] = comparison
    out_path.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'stage': 'compared', 'control': comparison['control_judgment'], 'updated': comparison['updated_judgment'],
                      'attributable': [(c['clause_id'], c['change_type'], c.get('direction')) for c in comparison['evidence_attributable_changes']],
                      'also_in_control': [(c['clause_id'], c['change_type']) for c in comparison['changes_also_in_control']]}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1].upper(), sys.argv[2], '--attach' in sys.argv))
