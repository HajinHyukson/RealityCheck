"""Assemble model inputs for a real-company case from extracted SEC paragraphs. Nothing is rewritten:
clause, definition and remedy text is copied verbatim by paragraph locator, and each piece keeps its source locators.

Usage: python build_case.py R01-irobot-carlyle
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main(case):
    folder = HERE / case
    spec = json.loads((folder / 'clauses.json').read_text(encoding='utf-8'))
    manifest = {d['id']: d for d in json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))['documents']}
    agreement = manifest[spec['agreement_document']]
    rows = json.loads((folder / 'extracted' / (spec['agreement_document'] + '.json')).read_text(encoding='utf-8'))
    index = {r['locator']: i for i, r in enumerate(rows)}

    def span(start, end):
        # Bare page numbers from the filed HTML are layout, not agreement text.
        picked = [r for r in rows[index[start]:index[end] + 1] if not re.fullmatch(r'-?\d{1,3}-?|[ivxl]{1,5}|\|', r['text'])]
        return '\n\n'.join(r['text'] for r in picked), [r['locator'] for r in picked]

    clauses = []
    for item in spec['clauses']:
        text, locators = span(item['from'], item['to'])
        clauses.append({'id': item['id'], 'title': item['title'], 'section': item['section'], 'clause': text, 'thesis_ids': [],
                        'source': {'document_id': spec['agreement_document'], 'locators': [locators[0], locators[-1]],
                                   'url': agreement['url'], 'sha256': agreement['sha256']}})
    definitions = '\n\n'.join(span(loc, loc)[0] for loc in spec['definitions'])
    resolution = '\n\n'.join(span(part['from'], part['to'])[0] for part in spec['resolution'])
    record = {key: spec[key] for key in ('borrower_id', 'borrower', 'sector', 'lender_role', 'facility', 'version', 'executed_at', 'effective_at', 'scope_note', 'missing_inputs', 'missing_inputs_blind')}
    # Public availability is the SEC acceptance time of the filing that carried the agreement, never the execution date.
    record.update(known_at=agreement['sec_accepted_at'][:10], sec_accepted_at=agreement['sec_accepted_at'],
                  source_mode='public_sec_filings', content_status='actual_public_disclosure',
                  clauses=clauses, definitions_and_conventions=definitions, resolution_conventions=resolution)
    out = folder / 'model_inputs'
    out.mkdir(exist_ok=True)
    # Origination evidence: individually located paragraphs, each checked against the facility's public availability date.
    evidence = []
    for group in spec.get('origination_sources', []):
        doc = manifest[group['document_id']]
        if doc['sec_accepted_at'][:10] > record['known_at']:
            raise ValueError(group['document_id'] + ' became public after origination and cannot be origination evidence')
        texts = {r['locator']: r['text'] for r in json.loads((folder / 'extracted' / (group['document_id'] + '.json')).read_text(encoding='utf-8'))}
        evidence += [{'document_id': group['document_id'], 'locator': loc, 'text': texts[loc], 'title': doc['title'],
                      'sec_accepted_at': doc['sec_accepted_at'], 'url': doc['url'], 'content_status': 'actual_public_disclosure'}
                     for loc in group['locators']]
    (out / 'origination-sources.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')
    print('origination evidence paragraphs', len(evidence), sum(len(e['text']) for e in evidence), flush=True)
    (out / 'contract-record.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    for clause in clauses:
        print(clause['id'], clause['section'], len(clause['clause']), clause['source']['locators'], flush=True)
    print('definitions', len(definitions), 'resolution', len(resolution), 'known_at', record['known_at'], flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
