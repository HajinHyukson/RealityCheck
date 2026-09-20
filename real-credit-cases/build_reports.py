"""Build the dated report sequence and observed lender responses for a real-company case.

Usage: python build_reports.py R01-irobot-carlyle
Reads <case>/reports.json and writes ../realitycheck/<id>_scenarios.json in the format prepare_b01_demo.py replays.
Report text is copied verbatim by paragraph locator from the extracted SEC filings. The availability date of every
report is the SEC acceptance date of the filing that carried it, never the period end or an execution date.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
STOP = re.compile(r'^(About [A-Z]|Cautionary|Forward-Looking|Use of Non-GAAP|Non-GAAP Financial Measures|Certain statements|For \w+ Investors|Investor (Relations|Inquiries))')
LOGISTICS = re.compile(r'conference call|webcast|investor conferences|one-on-one meetings', re.I)
BALANCE_ROWS = re.compile(r'^\|\s*(Cash and cash equivalents|Restricted cash|Accounts receivable, net|Inventory|Total current assets|Total current liabilities|Term loan|Total revenue|Revenue)\b', re.I)


def narrative(rows):
    picked = []
    for row in rows:
        text = row['text']
        if STOP.match(text):
            break
        if LOGISTICS.search(text):
            continue
        if text.startswith('|'):
            if BALANCE_ROWS.match(text):
                picked.append(row)
            continue
        if len(text) >= 80:
            picked.append(row)
    return picked


def main(case):
    folder = HERE / case
    spec = json.loads((folder / 'reports.json').read_text(encoding='utf-8'))
    manifest = {d['id']: d for d in json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))['documents']}
    cid = spec['borrower_id']
    events = []
    for n, report in enumerate(spec['reports'], 1):
        sources, accepted = [], []
        for part in report['documents']:
            doc = manifest[part['id']]
            rows = json.loads((folder / 'extracted' / (part['id'] + '.json')).read_text(encoding='utf-8'))
            chosen = [r for r in rows if r['locator'] in part['locators']] if part.get('locators') else narrative(rows)
            accepted.append(doc['sec_accepted_at'])
            sources += [{'document_id': part['id'], 'locator': r['locator'], 'text': r['text']} for r in chosen]
        available = max(accepted)[:10]
        events.append({'id': f'{cid}-D{n:02d}', 'title': report['title'], 'event_date': report.get('event_date') or available,
                       'available_at': available, 'review_date': available, 'source_kind': 'public_filing',
                       'presentation_summary': report['summary'], 'allow_no_impact': True,
                       'provenance': [{'document_id': p['id'], 'url': manifest[p['id']]['url'], 'sec_accepted_at': manifest[p['id']]['sec_accepted_at'],
                                       'sha256': manifest[p['id']]['sha256']} for p in report['documents']],
                       'sources': sources})
        print(events[-1]['id'], available, len(sources), sum(len(s['text']) for s in sources), report['title'], flush=True)
    amendments = []
    # Track each clause's operative text so a verbatim replacement records the exact text it supersedes.
    contract = json.loads((folder / 'model_inputs' / 'contract-record.json').read_text(encoding='utf-8'))
    current_text = {c['id']: c['clause'] for c in contract['clauses']}
    for response in spec['observed_responses']:
        doc = manifest[response['described_in']]
        rows = {r['locator']: r['text'] for r in json.loads((folder / 'extracted' / (response['described_in'] + '.json')).read_text(encoding='utf-8'))}
        description = '\n\n'.join(rows[loc] for loc in response['locators'])
        # A response may have been disclosed on its own, between reports, in which case no report carries it.
        trigger = next((e for e in events if e['title'] == response.get('disclosed_with')), None)
        changes = []
        for swap in response.get('replace_clauses', []):
            # Only exhibits checked to be clean (no merged deleted/inserted language) may supply replacement text.
            source_rows = json.loads((folder / 'extracted' / (swap['document_id'] + '.json')).read_text(encoding='utf-8'))
            index = {r['locator']: i for i, r in enumerate(source_rows)}
            picked = [r for r in source_rows[index[swap['from']]:index[swap['to']] + 1] if not re.fullmatch(r'-?\d{1,3}-?|\|', r['text'])]
            after = '\n\n'.join(r['text'] for r in picked)
            changes.append({'clause_id': swap['clause_id'], 'before': current_text[swap['clause_id']], 'after': after,
                            'source': {'document_id': swap['document_id'], 'locators': [swap['from'], swap['to']], 'url': manifest[swap['document_id']]['url']}})
            current_text[swap['clause_id']] = after
        amendments.append({
            'id': f"{cid}-{response['id']}", 'version': response['version'], 'parent_version': response['parent_version'],
            'trigger_event_id': trigger['id'] if trigger else None, 'title': response['title'], 'status': 'observed_historical_response',
            'decision_at': doc['sec_accepted_at'][:10], 'effective_at': response['executed_at'],
            'publicly_available_at': doc['sec_accepted_at'],
            'rationale': 'Observed historical lender response, recorded from the company\'s SEC filing. It is not an analyst decision, '
                         'a recommendation of this tool or proof that the response was the right remedy. The lender\'s reasons are not public.',
            'changes': changes,
            # The executed amendment is filed as a redline; its operative text is not extracted. The company's own description is carried instead.
            'add_clauses': [{'id': response['clause_id'], 'title': response['title'] + ' (company description)', 'section': 'Form ' + doc['type'] + ' description',
                             'clause': description, 'thesis_ids': [],
                             'source': {'document_id': response['described_in'], 'locators': response['locators'], 'url': doc['url'], 'sha256': doc['sha256']}}],
            'instrument_text': 'Operative amendment text: ' + manifest[response['instrument']]['url'] + ' (SEC-filed exhibit; see the missing inputs for why its full text is not extracted). '
                               'Company description, verbatim from its Form ' + doc['type'] + ':\n\n' + description,
            'conditions': [], 'waiver_scope': response['waiver_scope'], 'not_pursued': None})
    out = {'borrower_id': cid, 'borrower': spec['borrower'], 'synthetic': False, 'source_mode': 'public_sec_filings',
           'description': spec['description'], 'original_terms': spec['original_terms'], 'presentation': spec['presentation'],
           'events': events, 'amendments': amendments}
    # Real-company records live under the benchmark folder, apart from the demo's state.
    target = HERE.parent / 'realitycheck' / 'benchmark' / cid / 'rolling' / 'scenarios.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print('wrote', target.name, len(events), 'reports', len(amendments), 'observed responses', flush=True)


if __name__ == '__main__':
    main(sys.argv[1])
