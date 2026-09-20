"""Re-validate or re-run one event in a scenario seed, keeping the earlier attempt.

Usage: python rerun_scenario_event.py H01 H01-D04 revalidate "reason"   # saved genuine response, current validator, no inference call
       python rerun_scenario_event.py H01 H01-D03 rerun "reason"        # new hosted call using the event's current scenario sources

The event keeps its place, its package version and its decision. The earlier analysis is archived under <id>_attempts/ with the
reason, never deleted. A re-validation keeps the original generation time and states that no new inference was made.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main(cid, event_id, mode, reason):
    import app  # loads NVIDIA_API_KEY from the local .env without printing it
    import b01_model
    stem = cid.lower()
    seed_path = HERE / (stem + '_seed.json')
    seed = json.loads(seed_path.read_text(encoding='utf-8'))
    fixtures = json.loads((HERE / (stem + '_scenarios.json')).read_text(encoding='utf-8'))
    index = next(i for i, e in enumerate(seed['events']) if e['id'] == event_id)
    record = seed['events'][index]
    fixture = next(e for e in fixtures['events'] if e['id'] == event_id)
    version = next(v for v in seed['versions'] if v['version'] == record['package_version'])
    old = record.get('analysis') or {}
    attempts = HERE / (stem + '_attempts')
    attempts.mkdir(exist_ok=True)
    count = len(list(attempts.glob(event_id.lower() + '_*.json'))) + 1
    (attempts / f'{event_id.lower()}_attempt{count}.json').write_text(json.dumps({'archived_because': reason, 'mode_of_replacement': mode, 'event': record}, ensure_ascii=False, indent=2), encoding='utf-8')
    event = {key: fixture[key] for key in ('id', 'title', 'event_date', 'available_at', 'review_date', 'sources')}
    model = seed.get('analysis_model') or b01_model.DEFAULT_MODEL
    if mode == 'revalidate':
        if not isinstance(old.get('raw_response'), dict):
            raise SystemExit('No saved hosted response to re-validate.')
        event['sources'] = record['sources']   # the response is judged against the sources it was actually given
        analysis = b01_model.attribute_event(event, seed['profile'], version, api_key='', model=old.get('model') or model, completion=lambda system, user: old['raw_response'])
        analysis.update(revalidated_at=analysis['generated_at'], generated_at=old['generated_at'], model_options=old.get('model_options', analysis['model_options']),
                        validation_source='Recorded genuine NVIDIA response; re-validated with no new inference call. ' + reason)
        analysis['warnings'] = [w for w in old.get('warnings', []) if 'earlier attempt' in w.lower()] + analysis['warnings']
    elif mode == 'rerun':
        analysis = b01_model.attribute_event(event, seed['profile'], version, api_key=os.environ.get('NVIDIA_API_KEY', ''), model=model)
        analysis['rerun_note'] = reason
    else:
        raise SystemExit('mode must be revalidate or rerun')
    if analysis['engine'] != 'nemotron':
        print(json.dumps({'stage': 'failed', 'event': event_id, 'error': analysis.get('error')}))
        return 1
    extras = {key: fixture[key] for key in ('source_kind', 'presentation_summary', 'provenance', 'report_type', 'revision_note') if key in fixture}
    seed['events'][index] = {**record, **event, **extras, 'status': 'completed', 'analysis': analysis}
    seed_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8')
    (HERE / f'{stem}_{event_id.lower()}_result.json').write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'stage': mode, 'event': event_id, 'attributions': [(a['target_id'], a.get('proposed_status')) for a in analysis['attributions']],
                      'covenants': [(c['clause_id'], c['status']) for c in analysis['covenant_assessments']], 'warnings': len(analysis['warnings'])}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1].upper(), sys.argv[2].upper(), sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else ''))
