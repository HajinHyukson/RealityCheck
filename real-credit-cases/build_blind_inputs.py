"""Build the strict blind replay inputs for a real-company benchmark case (benchmark plan section 6A).

Usage: python build_blind_inputs.py R02-rumbleon-oaktree
Writes, under <case>/:
  blind/inputs.json          - inference inputs: dated reports with every passage that reveals a lender response removed
  blind/exclusion_log.json   - each removed passage, why, and what stayed despite matching the screen
  evaluator/observed_responses.json - the actual amendments, kept OUT of every inference input
Exclusions are reviewed decisions recorded in reports.json ("blind_exclusions"), not a regular expression. The screen
below only nominates passages; a nominated passage that stays in must carry a recorded reason. Financial facts are never
edited: a passage is kept whole or removed whole.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCREEN = re.compile(r'amend|waiv|forbear|lenders? (have |has )?agreed|covenant relief|not in compliance|noncompliance|event of default', re.I)


def main(case):
    folder = HERE / case
    spec = json.loads((folder / 'reports.json').read_text(encoding='utf-8'))
    rules = spec['blind_exclusions']
    scenarios = json.loads((HERE.parent / 'realitycheck' / 'benchmark' / spec['borrower_id'] / 'rolling' / 'scenarios.json').read_text(encoding='utf-8'))
    removed_docs = set(rules.get('documents', []))
    removed = {(r['document_id'], r['locator']): r['reason'] for r in rules.get('passages', [])}
    kept_reasons = {(r['document_id'], r['locator']): r['reason'] for r in rules.get('kept_despite_screen', [])}
    dependence = {r['report_id']: r['note'] for r in rules.get('dependence_notes', [])}
    unsuitable = {r['report_id']: r['reason'] for r in rules.get('unsuitable_checkpoints', [])}
    checkpoints, log, unreviewed = [], [], []
    for event in scenarios['events']:
        if event['id'] in unsuitable:
            log.append({'report_id': event['id'], 'action': 'checkpoint excluded from blind replay', 'reason': unsuitable[event['id']]})
            continue
        sources = []
        for source in event['sources']:
            key = (source['document_id'], source['locator'])
            if source['document_id'] in removed_docs:
                log.append({'report_id': event['id'], 'document_id': key[0], 'locator': key[1], 'action': 'removed',
                            'reason': 'Document is a filing about a lender response.', 'preview': source['text'][:160]})
            elif key in removed:
                log.append({'report_id': event['id'], 'document_id': key[0], 'locator': key[1], 'action': 'removed',
                            'reason': removed[key], 'preview': source['text'][:160]})
            else:
                if SCREEN.search(source['text']):
                    if key in kept_reasons:
                        log.append({'report_id': event['id'], 'document_id': key[0], 'locator': key[1], 'action': 'kept despite screen',
                                    'reason': kept_reasons[key], 'preview': source['text'][:160]})
                    else:
                        unreviewed.append((event['id'],) + key)
                sources.append(source)
        checkpoints.append({'id': event['id'], 'title': re.sub(r'\s+and Amendment No\. \d+$', '', event['title']), 'event_date': event['event_date'],
                            'available_at': event['available_at'], 'review_date': event['review_date'], 'sources': sources,
                            'provenance': [p for p in event.get('provenance', []) if p['document_id'] not in removed_docs]})
    if unreviewed:
        raise SystemExit('Passages match the leakage screen without a recorded decision: ' + json.dumps(unreviewed))
    blind = folder / 'blind'
    blind.mkdir(exist_ok=True)
    (blind / 'inputs.json').write_text(json.dumps({
        'borrower_id': spec['borrower_id'], 'borrower': spec['borrower'], 'mode': 'strict_blind_historical_replay',
        'contractual_baseline': 'original executed agreement only; no post-origination amendment, waiver or description of one',
        'checkpoints': checkpoints}, ensure_ascii=False, indent=2), encoding='utf-8')
    (blind / 'exclusion_log.json').write_text(json.dumps({'case': case, 'screen': SCREEN.pattern, 'entries': log}, ensure_ascii=False, indent=2), encoding='utf-8')
    evaluator = folder / 'evaluator'
    evaluator.mkdir(exist_ok=True)
    (evaluator / 'observed_responses.json').write_text(json.dumps({
        'warning': 'Evaluator collection. Never supply this file, or anything derived from it, to an inference run.',
        'borrower_id': spec['borrower_id'], 'observed_responses': scenarios['amendments'],
        # Notes that name hidden amendments live here, never beside the inference inputs.
        'dependence_notes': dependence}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(spec['borrower_id'], 'checkpoints', len(checkpoints), 'excluded checkpoints', len(unsuitable),
          'passages removed', sum(e['action'] == 'removed' for e in log), 'kept despite screen', sum(e['action'] == 'kept despite screen' for e in log))


if __name__ == '__main__':
    main(sys.argv[1])
