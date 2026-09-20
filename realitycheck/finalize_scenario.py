"""Attach reviewer notes to a demo scenario seed and, once reviewed, mark it complete so the app will load it.

Usage: python finalize_scenario.py H01 [--complete]
Reads <id>_review_notes.json: {"profile": [...], "events": {"H01-D02": [...]}}. Notes are added beside the model's original
wording, which is never rewritten. Decisions, versions and the pending proposal are not touched. Without --complete the
seed stays unloaded. A seed with a failed analysis cannot be marked complete.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main(cid, complete):
    stem = cid.lower()
    path = HERE / (stem + '_seed.json')
    seed = json.loads(path.read_text(encoding='utf-8'))
    notes_path = HERE / (stem + '_review_notes.json')
    notes = json.loads(notes_path.read_text(encoding='utf-8')) if notes_path.exists() else {}
    unknown = set(notes.get('events', {})) - {e['id'] for e in seed['events']}
    if unknown:
        raise SystemExit('Review notes name unknown events: ' + ', '.join(sorted(unknown)))
    applied = 0
    for event in seed['events']:
        analysis = event.get('analysis') or {}
        for note in notes.get('events', {}).get(event['id'], []):
            if note not in analysis.setdefault('review_notes', []):
                analysis['review_notes'].append(note)
                analysis.setdefault('warnings', []).append(note)
                applied += 1
    provenance = seed['profile_provenance']
    for note in notes.get('profile', []):
        if note not in provenance.setdefault('warnings', []):
            provenance['warnings'].append(note)
            applied += 1
    failed = [e['id'] for e in seed['events'] if e['status'] != 'completed']
    if complete:
        if failed:
            raise SystemExit('Cannot mark complete; analyses not completed for: ' + ', '.join(failed))
        seed['complete'] = True
        seed['review_status'] = 'Reviewed for source, date, arithmetic and scope errors; reviewer notes are shown beside the original model wording.'
    path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'case': cid, 'events': len(seed['events']), 'versions': [v['version'] for v in seed['versions']], 'pending_proposal': bool(seed.get('pending_proposal')),
                      'notes_applied': applied, 'not_completed': failed, 'complete': seed.get('complete')}))


if __name__ == '__main__':
    main(sys.argv[1].upper(), '--complete' in sys.argv)
