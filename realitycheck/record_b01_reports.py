"""Record genuine Nemotron analyses of the FluxRail report library without touching the presentation database.

Usage: python record_b01_reports.py
Copies b01.sqlite to a temporary folder with SQLite's backup API, introduces each report in b01_reports/ in date order on
that copy, runs the normal worker step, and saves each completed event to b01_reports/recorded/. A recorded replay keeps its
original model provenance and is labeled as recorded wherever it is shown; it is never presented as fresh inference.
"""
import json
import os
import sqlite3
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
LIBRARY = HERE / 'b01_reports'


def main():
    import app  # loads NVIDIA_API_KEY from the local .env without printing it
    import b01
    key = os.environ.get('NVIDIA_API_KEY', '')
    tmp = Path(tempfile.mkdtemp(prefix='b01_record_')) / 'b01_copy.sqlite'
    source = sqlite3.connect(f'file:{b01.DB_PATH}?mode=ro', uri=True)
    target = sqlite3.connect(str(tmp))
    source.backup(target)
    source.close(); target.close()
    (LIBRARY / 'recorded').mkdir(exist_ok=True)
    for path in sorted(LIBRARY.glob('*.json')):
        out = LIBRARY / 'recorded' / path.name
        if out.exists() and json.loads(out.read_text(encoding='utf-8')).get('status') == 'completed':
            print(json.dumps({'stage': 'already_recorded', 'report': path.name}), flush=True)
            continue
        body = json.loads(path.read_text(encoding='utf-8'))
        queued = b01.enqueue(body, 'database_update', tmp, dedupe_key='library:' + path.name)
        print(json.dumps({'stage': 'analyzing', 'report': path.name, 'event_id': queued['event_id']}), flush=True)
        b01.process_one(key, app.MODEL, tmp)
        event = next(e for e in b01.snapshot(tmp)['events'] if e['id'] == queued['event_id'])
        event['recorded_replay'] = {'library_file': path.name, 'recorded_on_copy': True,
                                    'note': 'Genuine hosted Nemotron analysis recorded on a copy of the FluxRail database, with the library reports introduced in date order.'}
        out.write_text(json.dumps(event, ensure_ascii=False, indent=2), encoding='utf-8')
        analysis = event.get('analysis') or {}
        print(json.dumps({'stage': event['status'], 'report': path.name, 'package_version': event['package_version'], 'error': analysis.get('error'),
                          'attributions': len(analysis.get('attributions', [])), 'covenants': [(c['clause_id'], c['status']) for c in analysis.get('covenant_assessments', [])]}), flush=True)
    print(json.dumps({'stage': 'done', 'copy': str(tmp)}), flush=True)


if __name__ == '__main__':
    main()
