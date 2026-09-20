"""Compare locked strict-blind outputs with the actual history (benchmark plan sections 7 and 8, step 6).

Usage: python benchmark_evaluate.py R02
Refuses to run until benchmark_blind.py has locked the outputs, and checks every file against its recorded hash first.
This is the only module that opens the evaluator collection. It applies the rules fixed in evaluator/scoring_rules.json
before any blind output was read. It reports counts with denominators, every failure, and what was not assessable.
It does not produce an accuracy claim: reference judgments are author-prepared and both histories are development histories.
"""
from datetime import date
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
CASES = HERE.parent / 'real-credit-cases'
WORKFLOWS = ('realitycheck', 'direct_review')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def days(a, b):
    return (date.fromisoformat(b[:10]) - date.fromisoformat(a[:10])).days


def signal(candidate, comparison):
    if candidate is None or candidate.get('engine') != 'nemotron':
        return 'failed'
    if candidate['drift_judgment'] == 'material_drift' and comparison and comparison['evidence_attributable_changes']:
        return 'escalate'
    if candidate['drift_judgment'] in ('insufficient_evidence', 'material_drift'):
        return 'information_request'   # includes a drift claim whose changes all match the control
    return 'no_action'


def main(cid):
    out = HERE / 'benchmark' / cid / 'blind'
    lock = out / 'lock.json'
    if not lock.exists():
        raise SystemExit('Blind outputs are not locked. Run: python benchmark_blind.py ' + cid + ' lock')
    locked = load(lock)
    changed = [name for name, digest in locked['files'].items() if hashlib.sha256((out / name).read_bytes()).hexdigest() != digest]
    if changed:
        raise SystemExit('Locked outputs were modified after locking: ' + ', '.join(changed))
    case = next(iter(sorted(CASES.glob(cid + '-*'))))
    evaluator = case / 'evaluator'
    rules = load(evaluator / 'scoring_rules.json')
    reference = {c['id']: c for c in load(evaluator / 'reference_judgments.json')['checkpoints']}
    observed = {r['id']: r for r in load(evaluator / 'observed_responses.json')['observed_responses']}
    checkpoints = load(case / 'blind' / 'inputs.json')['checkpoints']
    exclusions = load(case / 'blind' / 'exclusion_log.json')['entries']

    rows, per_workflow = [], {}
    for workflow in WORKFLOWS:
        first_touch, previous_flags, stats = {}, {}, {'checkpoints': 0, 'failed': 0, 'withheld_findings': 0, 'seconds': 0.0,
                                                      'warranted': 0, 'warranted_detected': 0, 'warranted_escalated': 0,
                                                      'unwarranted': 0, 'unnecessary_escalations': 0, 'unresolved': 0}
        for checkpoint in checkpoints:
            cp = checkpoint['id']
            candidate_path = out / workflow / (cp + '_candidate.json')
            comparison_path = out / workflow / (cp + '_comparison.json')
            candidate = load(candidate_path) if candidate_path.exists() else None
            comparison = load(comparison_path) if comparison_path.exists() else None
            sig = signal(candidate, comparison)
            flags = []
            if workflow == 'realitycheck':
                attribution_path = out / workflow / (cp + '_attribution.json')
                attribution = load(attribution_path) if attribution_path.exists() else {'attributions': [], 'warnings': [], 'engine': 'missing'}
                stats['withheld_findings'] += sum('withheld' in w for w in attribution.get('warnings', []))
                stats['seconds'] += attribution.get('elapsed_seconds', 0)
                for finding in attribution.get('attributions', []):
                    if finding.get('target_type') == 'assumption' and finding.get('proposed_status') in ('weakened', 'contradicted'):
                        if previous_flags.get(finding['target_id']) != finding['proposed_status']:
                            flags.append(finding['target_id'] + ' ' + finding['proposed_status'])
                        previous_flags[finding['target_id']] = finding['proposed_status']
            if candidate:
                stats['withheld_findings'] += sum('withheld' in w for w in candidate.get('warnings', []))
                stats['seconds'] += candidate.get('elapsed_seconds', 0)
            changes = comparison['evidence_attributable_changes'] if comparison else []
            for change in changes:
                first_touch.setdefault(change['clause_id'], {'checkpoint': cp, 'cutoff': checkpoint['review_date'], 'direction': change.get('direction', 'other'),
                                                             'change_type': change['change_type']})
            ref = reference[cp]['reconsideration']
            stats['checkpoints'] += 1
            stats['failed'] += sig == 'failed'
            if ref == 'warranted':
                stats['warranted'] += 1
                stats['warranted_detected'] += sig in ('escalate', 'information_request')
                stats['warranted_escalated'] += sig == 'escalate'
            elif ref == 'unwarranted':
                stats['unwarranted'] += 1
                stats['unnecessary_escalations'] += sig == 'escalate'
            else:
                stats['unresolved'] += 1
            rows.append({'workflow': workflow, 'checkpoint': cp, 'cutoff': checkpoint['review_date'], 'title': checkpoint['title'],
                         'reference': ref, 'signal': sig, 'new_assumption_flags': flags,
                         'attributable_changes': [{'clause_id': c['clause_id'], 'change_type': c['change_type'], 'direction': c.get('direction', 'other'),
                                                   'change': c['change'], 'evidence': c['evidence']} for c in changes],
                         'also_in_control': [c['clause_id'] for c in (comparison or {}).get('changes_also_in_control', [])],
                         'model_judgment_overridden': (candidate or {}).get('model_judgment'),
                         'information_gap': reference[cp].get('information_gap')})
        correspondence = []
        for response in rules['responses']:
            actual = observed[response['id']]
            public, executed = (actual.get('publicly_available_at') or actual['decision_at'])[:10], actual['effective_at']
            touches = sorted(({**t, 'clause_id': clause} for clause, t in first_touch.items() if clause in response['clause_families'] and t['cutoff'] < public),
                             key=lambda t: t['cutoff'])
            entry = {'response': response['id'], 'title': actual['title'], 'executed': executed, 'public': public,
                     'lender_clause_families': response['clause_families'], 'lender_direction': response['lender_direction'],
                     'lender_added': response['lender_added'], 'assessable': response['assessable'], 'assessability_note': response['assessability_note']}
            if touches:
                first = touches[0]
                lender = response['lender_direction_by_clause']
                # Direction is compared clause by clause. The same clause touched the opposite way is not agreement.
                per_clause = [{'clause_id': t['clause_id'], 'candidate': t['direction'], 'lender': lender.get(t['clause_id']), 'checkpoint': t['checkpoint'],
                               'same_direction': t['direction'] == lender.get(t['clause_id'])} for t in touches]
                agree = [c['clause_id'] for c in per_clause if c['same_direction']]
                entry.update(anticipated=True, first_checkpoint=first['checkpoint'], first_cutoff=first['cutoff'], candidate_direction=first['direction'],
                             per_clause=per_clause,
                             direction_reading=('same direction on ' + ', '.join(agree) + '; opposite on ' + ', '.join(c['clause_id'] for c in per_clause if not c['same_direction'])
                                                if agree and len(agree) < len(per_clause) else 'same clause, same direction' if agree else 'same clause, opposite direction'),
                             days_before_execution=days(first['cutoff'], executed), days_before_public=days(first['cutoff'], public))
            else:
                entry.update(anticipated=False)
            correspondence.append(entry)
        stats['seconds'] = round(stats['seconds'])
        per_workflow[workflow] = {'stats': stats, 'correspondence': correspondence}

    config = load(out / 'config.json')
    result = {'case': cid, 'mode': config['mode'], 'model': config['model'], 'candidate_prompt_version': config['candidate_prompt_version'],
              'guidelines': {'id': config['guidelines']['id'], 'version': config['guidelines']['version'], 'status': config['guidelines']['status']},
              'locked_at': locked['locked_at'], 'development_history': config['development_history'],
              'reference_disclosure': load(evaluator / 'reference_judgments.json')['author_disclosure'],
              'rules': rules['rules'], 'exclusions': exclusions, 'workflows': per_workflow, 'checkpoints': rows,
              'interpretation_limits': [
                  'A small feasibility study: ' + str(len(checkpoints)) + ' checkpoints for this company. Checkpoints within a company are correlated, not independent borrowers.',
                  'Reference judgments are author-prepared and were not blind to the actual history. No independent credit reviewer was available.',
                  ('This is the unseen history: prompts, guidelines, exclusions, reference judgments and scoring rules were frozen before any model run touched it.'
                   if config.get('unseen') else 'This is a development history: prompts were changed after earlier outputs for it were seen.'),
                  'One run per checkpoint. Repeat-run stability and unchanged-evidence controls are not measured.',
                  'Nemotron may know these companies\' outcomes from pretraining. Instructions to ignore recalled knowledge do not remove that.',
                  'An actual amendment is an observed response, not a correct answer. Correspondence and reference agreement are separate measures.']}
    target = HERE / 'benchmark' / cid / 'evaluation.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    for workflow, data in per_workflow.items():
        s = data['stats']
        print(f"{cid} {workflow}: warranted detected {s['warranted_detected']}/{s['warranted']} (escalated {s['warranted_escalated']}), "
              f"unnecessary escalations {s['unnecessary_escalations']}/{s['unwarranted']}, unresolved {s['unresolved']}, failed {s['failed']}/{s['checkpoints']}, "
              f"withheld findings {s['withheld_findings']}, model time {s['seconds']}s; "
              f"responses anticipated {sum(c['anticipated'] for c in data['correspondence'])}/{len(data['correspondence'])}")


if __name__ == '__main__':
    main(sys.argv[1].upper())
