"""Run genuine Nemotron calls in chronological order and save a resumable company demo seed.

Usage: python prepare_b01_demo.py [B02]  (defaults to B01; reads bNN_scenarios.json, writes bNN_seed.json)
"""
import copy
import json
import os
import sys
from pathlib import Path

import b01_model

HERE = Path(__file__).parent
SEED = HERE / 'b01_seed.json'
PROFILE_RESULT = HERE / 'b01_profile_result.json'
FIXTURES = HERE / 'b01_scenarios.json'


def write_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def original_version(origin, terms=None):
    contract = origin['contract']
    return {'version': contract['version'], 'parent_version': None, 'effective_at': contract['effective_at'],
            'decision_at': contract['executed_at'], 'status': 'effective', 'title': 'Original package',
            'terms': terms or {'fixed_rate': 9.25, 'leverage_max': 4.05}, 'clauses': copy.deepcopy(contract['clauses']),
            'definitions_and_conventions': contract['definitions_and_conventions'],
            # Real cases carry a verbatim clause subset, not a complete agreement text.
            'instrument_text': contract.get('complete_agreement_text') or contract.get('scope_note', ''), 'changes': []}


def apply_amendment(previous, amendment):
    if amendment['parent_version'] != previous['version']:
        raise ValueError('Amendment does not follow the current package version')
    version = copy.deepcopy(previous)
    for change in amendment['changes']:
        clause = next((c for c in version['clauses'] if c['id'] == change['clause_id']), None)
        if clause is None or clause['clause'] != change['before']:
            raise ValueError(f"Amendment before text does not match {change['clause_id']}")
        clause['clause'] = change['after']
    # An observed historical response can add a described provision instead of rewriting extracted clause text.
    for added in amendment.get('add_clauses', []):
        if any(c['id'] == added['id'] for c in version['clauses']):
            raise ValueError(f"Clause {added['id']} already exists")
        version['clauses'].append(copy.deepcopy(added))
    version.update(copy.deepcopy(amendment))
    version['status'] = 'effective'
    return version


def main(borrower_id='B01'):
    # app's existing loader reads local environment values without logging secrets.
    import app
    stem = borrower_id.lower()
    # B01 keeps its module-level paths so existing records and tests are untouched.
    SEED, PROFILE_RESULT, FIXTURES = ((globals()[name] if borrower_id == 'B01' else HERE / (stem + suffix))
        for name, suffix in (('SEED', '_seed.json'), ('PROFILE_RESULT', '_profile_result.json'), ('FIXTURES', '_scenarios.json')))
    model = os.environ.get('B01_NEMOTRON_MODEL', b01_model.DEFAULT_MODEL)
    origin = b01_model.load_origination(borrower_id)
    fixtures = json.loads(FIXTURES.read_text(encoding='utf-8'))
    if PROFILE_RESULT.exists():
        profile_result = json.loads(PROFILE_RESULT.read_text(encoding='utf-8'))
    else:
        profile_result = b01_model.generate_profile(api_key=os.environ.get('NVIDIA_API_KEY', ''), model=model, borrower_id=borrower_id)
        write_json(PROFILE_RESULT, profile_result)
    if profile_result['engine'] != 'nemotron' or not profile_result.get('profile'):
        print(json.dumps({'stage': 'profile', 'engine': profile_result['engine'], 'error': profile_result.get('error')}), flush=True)
        return 1
    if SEED.exists():
        seed = json.loads(SEED.read_text(encoding='utf-8'))
        if seed.get('profile') != profile_result['profile']:
            raise ValueError('Existing seed uses another profile. Preserve or explicitly archive it before rebuilding.')
        if seed.get('complete') is True:
            print(json.dumps({'stage': 'reviewed_seed_ready', 'complete': True, 'path': str(SEED)}), flush=True)
            return 0
    else:
        seed = {'borrower': {'id': borrower_id, 'name': origin['borrower'], 'sector': origin['contract']['sector'],
                             'source_mode': origin['contract'].get('source_mode', 'synthetic'),
                             'label': origin['contract'].get('label'), 'disclosure': origin['contract'].get('disclosure'),
                             'facility': origin['contract'].get('facility'), 'lender_role': origin['contract'].get('lender_role'),
                             'missing_inputs': origin['contract'].get('missing_inputs', [])},
                'profile': profile_result['profile'],
                'profile_provenance': {key: profile_result[key] for key in ('engine', 'model', 'generated_at', 'warnings', 'source_hashes')},
                'versions': [original_version(origin, fixtures.get('original_terms'))], 'events': [],
                'pending_proposal': fixtures['events'][-1].get('pending_proposal'),
                'presentation': fixtures.get('presentation') or {'as_of': '2027-09-10'}, 'raw_profile_response': profile_result['raw_response'],
                'synthetic': fixtures.get('synthetic', True), 'complete': False, 'failed_attempts': []}
        write_json(SEED, seed)
    seed['analysis_model'] = model
    seed['analysis_model_options'] = {'enable_thinking': True, 'max_tokens': 10000, 'response_format': 'json_object'}
    for raw_event in fixtures['events']:
        existing = next((e for e in seed['events'] if e['id'] == raw_event['id']), None)
        if existing and existing['status'] == 'completed':
            continue
        event = {key: raw_event[key] for key in ('id', 'title', 'event_date', 'available_at', 'review_date', 'sources')}
        current = seed['versions'][-1]
        print(json.dumps({'stage': 'analyzing', 'event': event['id'], 'package_version': current['version']}), flush=True)
        cached = existing.get('analysis', {}) if existing else {}
        replay = (cached.get('engine') == 'nemotron' and isinstance(cached.get('raw_response'), dict)
                  and cached.get('model') == model and cached.get('package_version') == current['version'])
        analysis = b01_model.attribute_event(event, seed['profile'], current,
                                            api_key=os.environ.get('NVIDIA_API_KEY', ''), model=model,
                                            completion=(lambda _system, _user: cached['raw_response']) if replay else None)
        if replay:
            analysis['revalidated_at'] = analysis['generated_at']
            analysis['generated_at'] = cached['generated_at']
            analysis['validation_source'] = 'Recorded genuine NVIDIA response; no new inference call'
        write_json(HERE / f"{stem}_{event['id'].lower()}_result.json", analysis)
        # A report with no material effect is a valid recorded outcome when the scenario says to expect one.
        success = analysis['engine'] == 'nemotron' and (bool(analysis['attributions']) or raw_event.get('allow_no_impact') is True)
        extras = {key: raw_event[key] for key in ('source_kind', 'presentation_summary', 'provenance') if key in raw_event}
        record = {**event, **extras, 'package_version': current['version'], 'status': 'completed' if success else 'failed',
                  'analysis': analysis, 'decision': {'action': 'pending'}}
        if existing:
            seed['events'].remove(existing)
        seed['events'].append(record)
        if not success:
            seed['failed_attempts'].append(analysis)
            write_json(SEED, seed)
            print(json.dumps({'stage': 'failed', 'event': event['id'], 'error': analysis.get('error'), 'warnings': analysis['warnings']}), flush=True)
            return 1
        amendment = next((a for a in fixtures['amendments'] if a['trigger_event_id'] == event['id']), None)
        if amendment:
            amended = apply_amendment(current, amendment)
            seed['versions'].append(amended)
            record['decision'] = {'action': 'adopted', 'version': amendment['version'], 'at': amendment['decision_at'], 'reason': amendment['rationale'],
                                  'observed_historical_response': amendment.get('status') == 'observed_historical_response'}
        write_json(SEED, seed)
        print(json.dumps({'stage': 'completed', 'event': event['id'], 'attributions': len(analysis['attributions']),
                          'covenant_assessments': analysis['covenant_assessments'], 'warnings': analysis['warnings']}), flush=True)
    seed['complete'] = False
    seed['review_status'] = 'All calls saved; independent semantic review required before publishing this demonstration.'
    write_json(SEED, seed)
    print(json.dumps({'stage': 'seed_awaiting_review', 'complete': seed['complete'], 'versions': len(seed['versions']), 'events': len(seed['events'])}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1].upper() if len(sys.argv) > 1 else 'B01'))
