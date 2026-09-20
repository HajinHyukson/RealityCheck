"""Summarize a real-company replay seed as Markdown: signal timing, validation withholds, reviewer corrections and drift runs.

Usage: python summarize_real_case.py R02 [R01 ...]   (prints Markdown to stdout)
Counts come straight from the saved seed. Nothing here is an accuracy claim: there is no held-out answer set for these cases.
"""
from datetime import date
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent


def days(a, b):
    return (date.fromisoformat(b[:10]) - date.fromisoformat(a[:10])).days


def summarize(cid):
    seed = json.loads((HERE / (cid.lower() + '_seed.json')).read_text(encoding='utf-8'))
    events = sorted(seed['events'], key=lambda e: e['review_date'])
    responses = [v for v in seed['versions'] if v.get('status') and v.get('parent_version')]
    lines = [f"## {cid} {seed['borrower']['name']}", '',
             f"{len(events)} reports, {len(seed['profile']['assumptions'])} reconstructed assumptions, {len(responses)} observed lender responses. "
             f"Model: `{seed.get('analysis_model')}`.", '',
             '| Report (public date) | Package | Assumptions flagged | Covenant findings kept | Withheld by validation | Reviewer notes |', '|---|---|---|---|---|---|']
    first_flag = {}
    for e in events:
        a = e['analysis']
        flagged = [f"{t['target_id']} {t['proposed_status']}" for t in a['attributions']
                   if t.get('target_type') == 'assumption' and t.get('proposed_status') in ('weakened', 'contradicted')]
        for t in a['attributions']:
            if t.get('target_type') == 'assumption' and t.get('proposed_status') in ('weakened', 'contradicted'):
                first_flag.setdefault(t['target_id'], e)
        withheld = sum('withheld' in w for w in a.get('warnings', []))
        findings = ', '.join(f"{c['clause_id']} {c['status'].replace('_', ' ')}" for c in a['covenant_assessments']) or 'none'
        lines.append(f"| {e['title']} ({e['available_at']}) | v{e['package_version']} | {', '.join(flagged) or 'none'} | {findings} | {withheld} | {len(a.get('review_notes', []))} |")
    lines += ['', '**First adverse flag versus the next publicly disclosed lender response.** Lead time is calendar days between two public dates. '
              'It shows ordering, not proven early warning: Nemotron may know these companies\' histories from pretraining, and reviewer notes below may withdraw a flag.', '',
              '| Assumption | First flagged | Next lender response public | Days between | Reviewer position |', '|---|---|---|---|---|']
    for aid, e in sorted(first_flag.items()):
        later = sorted((v for v in responses if (v.get('publicly_available_at') or v['decision_at'])[:10] >= e['available_at']),
                       key=lambda v: (v.get('publicly_available_at') or v['decision_at']))
        notes = ' '.join(e['analysis'].get('review_notes', []))
        position = 'corrected or qualified in reviewer notes' if aid in notes else 'not individually contested'
        if later:
            public = (later[0].get('publicly_available_at') or later[0]['decision_at'])[:10]
            lines.append(f"| {aid} | {e['title']} ({e['available_at']}) | v{later[0]['version']} ({public}) | {days(e['available_at'], public)} | {position} |")
        else:
            lines.append(f"| {aid} | {e['title']} ({e['available_at']}) | none in packet | n/a | {position} |")
    drift_runs = seed.get('drift_assessments', [])
    if drift_runs:
        lines += ['', '**Candidate-package drift runs.** One run each; repeat-run stability is not measured.', '',
                  '| Review date | Inputs | Control judgment | Updated judgment | Evidence-attributable changes | Also in control |', '|---|---|---|---|---|---|']
        for d in drift_runs:
            changes = ', '.join(f"{c['clause_id']} {c['change_type']}" for c in d['evidence_attributable_changes']) or 'none'
            shared = ', '.join(f"{c['clause_id']} {c['change_type']}" for c in d['changes_also_in_control']) or 'none'
            inputs = 'reports plus assumption assessments' if d.get('assessments_supplied') else 'reports only'
            lines.append(f"| {d['review_date']} | {inputs} | {d['control_judgment'].replace('_', ' ')} | {d['updated_judgment'].replace('_', ' ')} | {changes} | {shared} |")
    corrections = [(e['id'], n) for e in events for n in e['analysis'].get('review_notes', []) if 'model error' in n]
    if corrections:
        lines += ['', '**Model errors found in review** (original wording kept in the app, correction shown beside it):', '']
        lines += [f"- `{eid}`: {note}" for eid, note in corrections]
    return '\n'.join(lines)


if __name__ == '__main__':
    print('\n\n'.join(summarize(c.upper()) for c in sys.argv[1:]))
