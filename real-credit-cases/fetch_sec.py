"""Fetch a small, cached packet of SEC EDGAR filings for one real-company case.

Usage: python fetch_sec.py R01-irobot-carlyle

Reads <case>/packet.json (cik + documents), downloads each document once into <case>/sources/,
and writes <case>/manifest.json with content hashes, retrieval times and SEC acceptance timestamps.
Deliberately not a crawler: sequential requests, a pause between them, cache-first, back off on errors.
SEC fair-access policy asks for a descriptive User-Agent with a contact address.
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
# SEC fair-access policy asks for a contact address. It comes from the environment (or .env) so no personal address is committed.
USER_AGENT = os.environ.get('SEC_USER_AGENT', '')
REUSE_POLICY = 'https://www.sec.gov/about/webmaster-frequently-asked-questions'
PAUSE_SECONDS = 0.6


def get(url):
    if not USER_AGENT:
        raise SystemExit('Set SEC_USER_AGENT, for example "RealityCheck research you@example.com", before fetching from sec.gov. Cached documents need no fetch.')
    for attempt in range(4):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept-Encoding': 'identity'})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code not in (403, 429, 500, 502, 503, 504) or attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
        finally:
            time.sleep(PAUSE_SECONDS)


def cached(path, url):
    if not path.exists():
        path.write_bytes(get(url))
        return path.read_bytes(), datetime.now(timezone.utc).isoformat(timespec='seconds')
    retrieved = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec='seconds')
    return path.read_bytes(), retrieved


def accession_of(url):
    # .../Archives/edgar/data/<cik>/<accession without dashes>/<file>
    raw = url.split('/Archives/edgar/data/')[1].split('/')[1]
    return f'{raw[:10]}-{raw[10:12]}-{raw[12:]}'


def main(case):
    folder = HERE / case
    packet = json.loads((folder / 'packet.json').read_text(encoding='utf-8'))
    sources = folder / 'sources'
    sources.mkdir(exist_ok=True)
    cik = str(packet['cik']).zfill(10)
    raw, _ = cached(sources / 'edgar-submissions.json', f'https://data.sec.gov/submissions/CIK{cik}.json')
    submissions = json.loads(raw)
    recent = submissions['filings']['recent']
    filings = {acc: {key: recent[key][i] for key in ('form', 'filingDate', 'reportDate', 'acceptanceDateTime', 'items', 'primaryDocument')}
               for i, acc in enumerate(recent['accessionNumber'])}
    for extra in submissions['filings'].get('files', []):
        needed = {accession_of(d['url']) for d in packet['documents']} - set(filings)
        if not needed:
            break
        raw, _ = cached(sources / extra['name'], 'https://data.sec.gov/submissions/' + extra['name'])
        older = json.loads(raw)
        for i, acc in enumerate(older['accessionNumber']):
            filings.setdefault(acc, {key: older[key][i] for key in ('form', 'filingDate', 'reportDate', 'acceptanceDateTime', 'items', 'primaryDocument')})
    records, problems = [], []
    for doc in packet['documents']:
        accession = accession_of(doc['url'])
        name = doc['id'] + '__' + doc['url'].rsplit('/', 1)[1]
        try:
            body, retrieved = cached(sources / name, doc['url'])
        except (urllib.error.URLError, OSError) as exc:
            problems.append({'id': doc['id'], 'url': doc['url'], 'error': str(exc)[:200]})
            continue
        filing = filings.get(accession)
        if filing is None:
            problems.append({'id': doc['id'], 'url': doc['url'], 'error': 'Accession not found in EDGAR submissions index; availability unverified.'})
        records.append({**doc, 'company': packet['company'], 'facility': packet['facility'], 'publisher': 'U.S. SEC EDGAR',
                        'sec_accession': accession, 'cached_file': 'sources/' + name,
                        'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body), 'retrieved_at': retrieved,
                        'form': filing and filing['form'], 'filing_date': filing and filing['filingDate'],
                        'report_date': filing and filing['reportDate'], 'items': filing and filing['items'],
                        # SEC acceptance is when the filing became public: the available-at basis, never the execution date.
                        'sec_accepted_at': filing and filing['acceptanceDateTime'],
                        'content_status': 'actual_public_disclosure', 'reuse_policy_url': REUSE_POLICY,
                        'track_eligibility': {'xtract': 'public source permitted', 'compound': 'not eligible: real financial records'}})
        print(doc['id'], len(body), filing and filing['acceptanceDateTime'], flush=True)
    manifest = {'case': case, 'company': packet['company'], 'facility': packet['facility'], 'cik': packet['cik'],
                'review_period': packet.get('review_period'), 'user_agent_policy': 'descriptive User-Agent with contact; sequential cached requests',
                'manifest_written_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                'documents': records, 'problems': problems}
    (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps({'documents': len(records), 'problems': problems}), flush=True)
    return 1 if problems else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
