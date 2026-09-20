"""Finalize a real-company replay seed after its hosted calls are saved and a person has reviewed them.

Usage: python finalize_real_case.py R01 [--complete]
- Reports with no publicly disclosed lender response are recorded as such instead of 'pending': a historical replay has no analyst decision waiting.
- Reviewer notes from <id>_review_notes.json ({"profile": [...], "events": {"R01-D02": [...]}}) are attached beside the model's
  original wording, which is never rewritten.
- --complete marks the seed reviewed so the app will load it. Without it the seed stays unloaded.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main(cid, complete):
    stem = cid.lower()
    path = HERE / (stem + '_seed.json')
    seed = json.loads(path.read_text(encoding='utf-8'))
    if seed.get('synthetic', True):
        raise SystemExit('This step is only for real-company replays.')
    notes_path = HERE / (stem + '_review_notes.json')
    notes = json.loads(notes_path.read_text(encoding='utf-8')) if notes_path.exists() else {}
    failed = [e['id'] for e in seed['events'] if e['status'] != 'completed']
    if failed:
        raise SystemExit('Reports without a completed analysis: ' + ', '.join(failed))
    for event in seed['events']:
        if event['decision'].get('action') == 'pending':
            event['decision'] = {'action': 'dismissed', 'at': event['review_date'], 'observed_historical_response': True,
                                 'reason': 'Historical replay: no lender response was publicly disclosed with this report. The package then in effect continued. '
                                           'This records what is public, not an analyst decision.'}
        for note in notes.get('events', {}).get(event['id'], []):
            analysis = event['analysis']
            if note not in analysis.setdefault('review_notes', []):
                analysis['review_notes'].append(note)
                analysis.setdefault('warnings', []).append(note)
    provenance = seed['profile_provenance']
    for note in notes.get('profile', []):
        if note not in provenance.setdefault('warnings', []):
            provenance['warnings'].append(note)
    seed['pending_proposal'] = None
    if complete:
        seed['complete'] = True
        seed['review_status'] = 'Reviewed for source, date and scope errors; reviewer notes are shown beside the original model wording.'
    path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'case': cid, 'events': len(seed['events']), 'versions': [v['version'] for v in seed['versions']],
                      'complete': seed.get('complete'), 'notes_applied': sum(len(v) for v in notes.get('events', {}).values()) + len(notes.get('profile', []))}))


if __name__ == '__main__':
    main(sys.argv[1].upper(), '--complete' in sys.argv)
