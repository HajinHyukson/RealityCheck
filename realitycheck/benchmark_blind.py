"""Strict blind historical replay (benchmark plan section 6A).

Usage: python benchmark_blind.py R02 realitycheck     # framework workflow: report attribution, then a complete candidate, per checkpoint
       python benchmark_blind.py R02 direct_review    # comparator: same model, evidence, package and guidelines, no assumption framework
       python benchmark_blind.py R02 lock             # freeze outputs; required before any comparison with the actual history

Rules enforced here:
- The original executed agreement is the only contractual baseline at every checkpoint. No amendment is ever applied.
- Inputs come only from real-credit-cases/<case>/blind/inputs.json and the origination packet. This module never opens the
  evaluator collection or the rolling-replay records, and refuses to run once the outputs are locked.
- Every attempt is kept, including failures and timeouts. A failed checkpoint is recorded, retried on the next run, and counted.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
CASES = HERE.parent / 'real-credit-cases'
# Histories no model run touched before the configuration was frozen. Everything else is a development history.
UNSEEN = {'R03'}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def case_folder(cid):
    matches = sorted(CASES.glob(cid + '-*'))
    if len(matches) != 1:
        raise SystemExit('Unknown case ' + cid)
    return matches[0]


def lock(out):
    files = sorted(p for p in out.rglob('*.json') if p.name != 'lock.json')
    record = {'locked_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
              'statement': 'Outputs frozen before the actual amendment history was opened for comparison.',
              'files': {str(p.relative_to(out)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    write(out / 'lock.json', record)
    print(json.dumps({'stage': 'locked', 'files': len(files)}))


def main(cid, workflow):
    out = HERE / 'benchmark' / cid / 'blind'
    if workflow == 'lock':
        return lock(out)
    if (out / 'lock.json').exists():
        raise SystemExit('Outputs are locked. A new blind run needs a new output folder, not an overwrite.')
    import app  # loads NVIDIA_API_KEY from the local .env without printing it
    import b01_model
    import drift
    key = os.environ.get('NVIDIA_API_KEY', '')
    model = b01_model.DEFAULT_MODEL
    inputs = json.loads((case_folder(cid) / 'blind' / 'inputs.json').read_text(encoding='utf-8'))
    contract = b01_model.load_origination(cid, blind=True)['contract']
    original = {'version': contract['version'], 'effective_at': contract['effective_at'], 'status': 'effective', 'clauses': contract['clauses'],
                'definitions_and_conventions': contract['definitions_and_conventions'], 'terms': {}, 'instrument_text': contract.get('scope_note', '')}
    config = {'case': cid, 'mode': 'strict_blind_historical_replay', 'model': model, 'attribution_options': {'enable_thinking': True, 'max_tokens': 10000},
              'candidate_prompt_version': drift.PROMPT_VERSION, 'guidelines': json.loads(drift.GUIDELINES.read_text(encoding='utf-8')),
              'contractual_baseline': 'original package v' + contract['version'] + ' at every checkpoint',
              'unseen': cid in UNSEEN,
              'development_history': ('Unseen history. No model run of any kind touched this company before the prompts, guidelines, blind inputs, exclusion decisions, '
                                      'reference judgments and scoring rules were frozen. A retried failure re-runs the same frozen configuration.' if cid in UNSEEN else
                                      'Prompts and validation were adjusted after earlier rolling-replay outputs for this company were seen. '
                                      'This is a development history, not an unseen held-out case.')}
    write(out / 'config.json', config)

    def attempt(path, call):
        saved = json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
        if saved and saved.get('engine') == 'nemotron':
            return saved
        started = time.time()
        result = call()
        result['elapsed_seconds'] = round(time.time() - started, 1)
        if saved:  # keep the failed attempt beside the retry
            result['earlier_failed_attempts'] = saved.get('earlier_failed_attempts', []) + [{'error': saved.get('error'), 'generated_at': saved.get('generated_at')}]
        write(path, result)
        print(json.dumps({'stage': 'saved', 'file': path.name, 'engine': result['engine'], 'error': result.get('error'), 'seconds': result['elapsed_seconds']}), flush=True)
        return result

    if workflow == 'realitycheck':
        profile_result = attempt(out / 'profile_result.json',
                                 lambda: b01_model.generate_profile(api_key=key, model=model, borrower_id=cid, blind=True))
        if profile_result['engine'] != 'nemotron':
            return 1
        profile = profile_result['profile']
        control = attempt(out / 'realitycheck' / 'control.json',
                          lambda: drift.generate_candidate(cid, profile, original, [], mode='control', review_date=contract['known_at'],
                                                           api_key=key, model=model, blind=True, workflow='realitycheck'))
        if control['engine'] != 'nemotron':
            return 1
    elif workflow == 'direct_review':
        profile = {'assumptions': []}
        control = attempt(out / 'direct_review' / 'control.json',
                          lambda: drift.generate_candidate(cid, profile, original, [], mode='control', review_date=contract['known_at'],
                                                           api_key=key, model=model, blind=True, workflow='direct_review'))
        if control['engine'] != 'nemotron':
            return 1
    else:
        raise SystemExit('workflow must be realitycheck, direct_review or lock')

    released, assessments = [], {}
    for checkpoint in inputs['checkpoints']:
        event = {k: checkpoint[k] for k in ('id', 'title', 'event_date', 'available_at', 'review_date', 'sources')}
        released.append(event)
        if workflow == 'realitycheck':
            working = dict(profile, prior_assessments=list(assessments.values()))
            version = dict(original, known_versions=[original])
            analysis = attempt(out / 'realitycheck' / (checkpoint['id'] + '_attribution.json'),
                               lambda: _attribute(b01_model, event, working, version, key, model))
            if analysis['engine'] == 'nemotron':
                for finding in analysis['attributions']:
                    if finding.get('target_type') == 'assumption' and finding.get('proposed_status'):
                        assessments[finding['target_id']] = {'assumption_id': finding['target_id'], 'status': finding['proposed_status'],
                                                             'review_date': event['review_date'], 'report_id': event['id'], 'rationale': finding.get('rationale', '')}
        candidate = attempt(out / workflow / (checkpoint['id'] + '_candidate.json'),
                            lambda: drift.generate_candidate(cid, profile, original, list(released), mode='updated', review_date=event['review_date'],
                                                             api_key=key, model=model, blind=True, workflow=workflow,
                                                             assessments=list(assessments.values()) if workflow == 'realitycheck' else None))
        if candidate['engine'] == 'nemotron':
            write(out / workflow / (checkpoint['id'] + '_comparison.json'), drift.compare(control, candidate))
    print(json.dumps({'stage': 'workflow_complete', 'workflow': workflow, 'checkpoints': len(released)}), flush=True)
    return 0


def _attribute(b01_model, event, profile, version, key, model):
    try:
        return b01_model.attribute_event(event, profile, version, api_key=key, model=model, blind=True)
    except Exception as exc:  # a validation refusal is an outcome to record, not a crash
        return {'id': event['id'], 'engine': 'unavailable', 'model': model, 'error': str(exc)[:300], 'attributions': [],
                'covenant_assessments': [], 'warnings': [], 'generated_at': datetime.now(timezone.utc).isoformat()}


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1].upper(), sys.argv[2]))
