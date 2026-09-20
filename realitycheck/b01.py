"""Per-company local database, dated review queue and package history. B01 was the first company."""
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
import re
from pathlib import Path
import sqlite3
import threading
import uuid

import attribution

HERE = Path(__file__).parent
DB_PATH = HERE / 'b01.sqlite'
SEED_PATH = HERE / 'b01_seed.json'
INBOX = HERE / 'b01_inbox'
UPLOAD_ROOT = HERE / 'uploads'
COMPANY_ID = r'(?:[BRH]\d{2}|U[A-F0-9]{12})'
_worker = None
WORKERS = 4


def paths(borrower_id='B01'):
    # One SQLite file, seed and inbox per company keeps borrower histories strictly separate.
    # B-prefixed companies are synthetic; H-prefixed are hypothetical facilities set at a real company; R-prefixed are benchmark histories.
    if not isinstance(borrower_id, str) or not re.fullmatch(COMPANY_ID, borrower_id):
        raise ValueError('Unknown company.')
    if borrower_id.startswith('U'):
        folder = UPLOAD_ROOT / borrower_id.lower()
        return folder / 'company.sqlite', folder / 'seed.json', folder / 'inbox'
    if borrower_id == 'B01':
        return DB_PATH, SEED_PATH, INBOX
    stem = borrower_id.lower()
    return HERE / (stem + '.sqlite'), HERE / (stem + '_seed.json'), HERE / (stem + '_inbox')


def reports_dir(borrower_id='B01'):
    paths(borrower_id)  # validates the id
    if borrower_id.startswith('U'):
        return UPLOAD_ROOT / borrower_id.lower() / 'reports'
    return HERE / (borrower_id.lower() + '_reports')


def library(db_path=DB_PATH, folder=None):
    """Reports prepared for presentation. A report is not part of the company history until someone introduces it."""
    folder = Path(folder or reports_dir())
    with connection(db_path) as con:
        known = {row['dedupe']: row['status'] for row in con.execute("SELECT dedupe,status FROM events WHERE dedupe LIKE 'library:%'")}
    items = []
    for path in sorted(folder.glob('*.json')):
        body = json.loads(path.read_text(encoding='utf-8'))
        recorded = folder / 'recorded' / path.name
        ready = recorded.exists() and json.loads(recorded.read_text(encoding='utf-8')).get('status') == 'completed'
        items.append({'name': path.name, 'title': body.get('title'), 'report_type': body.get('report_type'), 'publisher': body.get('publisher'),
                      'available_at': body.get('available_at'), 'summary': body.get('library_summary'), 'synthetic': body.get('synthetic', True),
                      'introduced': 'library:' + path.name in known, 'status': known.get('library:' + path.name), 'recorded_available': ready})
    return items


def introduce(body, db_path=DB_PATH, folder=None):
    """Bring a library report into the company history, by live analysis or as a labeled recorded replay."""
    folder = Path(folder or reports_dir())
    name, mode = body.get('name'), body.get('mode')
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9._-]+\.json', name) or mode not in ('live', 'recorded'):
        raise ValueError('Choose a library report and either live or recorded analysis.')
    path = folder / name
    if not path.exists():
        raise ValueError('Unknown library report.')
    key = 'library:' + name
    report = json.loads(path.read_text(encoding='utf-8'))
    if mode == 'live':
        return enqueue(report, 'database_update', db_path, dedupe_key=key)
    recorded_path = folder / 'recorded' / name
    if not recorded_path.exists():
        raise ValueError('No recorded analysis exists for this report. Use live analysis.')
    record = json.loads(recorded_path.read_text(encoding='utf-8'))
    state = snapshot(db_path)
    terms_date = min(record['event_date'] or record['review_date'], record['review_date'])
    operative = _select_version(state['versions'], terms_date)['version']
    if record.get('status') != 'completed' or record['package_version'] != operative:
        # A saved analysis speaks only about the package it was run against.
        raise ValueError('The recorded analysis was made against package v' + str(record['package_version']) +
                         ', but v' + operative + ' now governs that date. Use live analysis.')
    event = deepcopy(record)
    event.update(id=state['borrower'].get('id', 'B01') + '-E-' + uuid.uuid4().hex[:12], source_kind='recorded_replay',
                 decision={'action': 'pending'}, received_at=stamp())
    with connection(db_path) as con:
        old = con.execute('SELECT id,status FROM events WHERE dedupe=?', (key,)).fetchone()
        if old:
            return {'event_id': old['id'], 'status': old['status'], 'duplicate': True}
        con.execute('INSERT INTO events(id,dedupe,status,payload) VALUES (?,?,?,?)', (event['id'], key, 'completed', json.dumps(event)))
        _put(con, 'last_update', stamp())
    return {'event_id': event['id'], 'status': 'completed', 'recorded_replay': True}


def companies():
    # Demo companies only. R-prefixed real-company histories belong to the benchmark and keep their state under benchmark/,
    # separate from the demonstration's persistent user state.
    found = ({'B01'} if SEED_PATH.exists() else set()) | {f.name[:3].upper() for f in HERE.glob('[bh][0-9][0-9]_seed.json')}
    found |= {f.parent.name.upper() for f in UPLOAD_ROOT.glob('u*/company.sqlite')
              if re.fullmatch(COMPANY_ID, f.parent.name.upper())}
    return sorted(found)
_stop = threading.Event()


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


@contextmanager
def connection(db_path=DB_PATH):
    con = sqlite3.connect(str(db_path), timeout=20)
    con.row_factory = sqlite3.Row
    try:
        with con:
            yield con
    finally:
        con.close()


def _get(con, key, default=None):
    row = con.execute('SELECT value FROM metadata WHERE key=?', (key,)).fetchone()
    return json.loads(row['value']) if row else default


def _put(con, key, value):
    con.execute('INSERT OR REPLACE INTO metadata VALUES (?,?)', (key,json.dumps(value)))


def initialize(db_path=DB_PATH, seed_path=SEED_PATH):
    with connection(db_path) as con:
        con.execute('CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY,value TEXT NOT NULL)')
        con.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT,id TEXT UNIQUE NOT NULL,dedupe TEXT UNIQUE,status TEXT NOT NULL,payload TEXT NOT NULL)')
        if _get(con,'seeded'):
            return True
        if not Path(seed_path).exists():
            return False
        seed=json.loads(Path(seed_path).read_text(encoding='utf-8'))
        if seed.get('complete') is False or not seed.get('profile'):
            return False
        for key in ('borrower','profile','profile_provenance','analysis_model','versions','pending_proposal','presentation'):
            _put(con,key,seed.get(key,{} if key!='versions' else []))
        _put(con,'drift_assessments',seed.get('drift_assessments',[]))
        for event in seed.get('events',[]):
            record=deepcopy(event)
            record.setdefault('source_kind','demo')
            con.execute('INSERT OR IGNORE INTO events(id,dedupe,status,payload) VALUES (?,?,?,?)',
                        (record['id'],'seed:'+record['id'],record.get('status','completed'),json.dumps(record)))
        _put(con,'seeded',True)
        _put(con,'seeded_at',stamp())
    return True


def snapshot(db_path=DB_PATH):
    with connection(db_path) as con:
        onboarding = _get(con, 'onboarding', {})
        documents = _get(con, 'uploaded_documents', [])
        if not _get(con,'seeded'):
            return {'ready':False,'status':onboarding.get('status', 'processing'),
                    'stage':onboarding.get('stage', 'Preparing company profile'),
                    'error':onboarding.get('error'), 'onboarding':onboarding, 'uploaded_documents':documents,
                    'borrower':_get(con, 'borrower', {'id':Path(db_path).stem.upper()}),'profile':{},'versions':[],
                    'events':[],'feed':{},'current_profile':{'assessments':{}}}
        result={key:_get(con,key,{}) for key in ('borrower','profile','profile_provenance','analysis_model','versions','pending_proposal','presentation')}
        result['drift_assessments']=_get(con,'drift_assessments',[])
        result['drift_job']=_get(con,'drift_job')
        result['events']=[json.loads(row['payload']) for row in con.execute('SELECT payload FROM events ORDER BY seq')]
        result['feed']={'mode':'Local company database · automatic analysis',
                        'last_scan':_get(con,'last_scan'), 'errors':_get(con,'feed_errors',[]),
                        'queued':sum(e['status']=='queued' for e in result['events']),
                        'processing':sum(e['status']=='processing' for e in result['events']),
                        'inbox':'realitycheck/'+str(result['borrower'].get('id','B01')).lower()+'_inbox', 'last_update':_get(con,'last_update')}
    result.update(ready=True, status='ready', stage='Ready', error=None,
                  onboarding=onboarding, uploaded_documents=documents)
    result['current_version']=result['versions'][-1]['version']
    assessments={}
    known={a['id'] for a in result['profile'].get('assumptions',[])}
    for event in sorted(result['events'],key=lambda e:(e.get('review_date',''),e.get('available_at',''))):
        for finding in (event.get('analysis') or {}).get('attributions',[]):
            target=finding.get('target_id')
            if finding.get('target_type')=='assumption' and target in known and finding.get('proposed_status'):
                assessments[target]={'status':finding['proposed_status'],'event_id':event['id'],
                                     'review_date':event.get('review_date'),'rationale':finding.get('rationale','')}
    result['current_profile']={'assessments':assessments,'basis':'Latest recorded model assessments; original claims preserved'}
    return result


_SEVERITY={'weakened':1,'contradicted':2}


def is_detection(event, events):
    """Same rule as the workspace page: an assumption finding worse than that assumption's latest earlier status,
    or a covenant newly triggered or noncompliant. A move from contradicted to weakened stays a report marker."""
    analysis=event.get('analysis') or {}
    earlier={}
    for other in events:
        if other['id']==event['id']:
            break
        if str(other.get('review_date') or '')>str(event.get('review_date') or ''):
            continue
        for finding in (other.get('analysis') or {}).get('attributions',[]):
            if finding.get('proposed_status'):
                earlier[finding.get('target_id')]=finding['proposed_status']
    return (any(_SEVERITY.get(f.get('proposed_status'),0)>_SEVERITY.get(earlier.get(f.get('target_id')),0) for f in analysis.get('attributions',[]))
            or any(c.get('status') in ('noncompliant','triggered') and not c.get('already_assessed_in') for c in analysis.get('covenant_assessments',[])))


def _select_version(versions, review_date):
    eligible=[v for v in versions if v['effective_at']<=review_date]
    if not eligible:
        raise ValueError('Review date precedes the original package availability.')
    return max(eligible,key=lambda v:v['effective_at'])


def enqueue(body, source_kind='manual', db_path=DB_PATH, dedupe_key=None, uploaded_documents=None):
    if not isinstance(body,dict):
        raise ValueError('Event must be a JSON object.')
    if source_kind not in ('manual','database_update','uploaded_report'):
        raise ValueError('Unsupported source kind.')
    state=snapshot(db_path)
    if not state['ready']:
        raise ValueError(state.get('error') or 'Company profile is still being prepared.')
    own=state['borrower'].get('id','B01')
    if body.get('borrower_id',own)!=own:
        raise ValueError('This company database accepts only '+own+' updates.')
    as_of=state['presentation'].get('as_of','2027-09-10')
    available=body.get('available_at') or as_of
    event={'id':own+'-E-'+uuid.uuid4().hex[:12], 'title':body.get('title') or 'Company update',
           'event_date':body.get('event_date') or '', 'available_at':available,
           'review_date':body.get('review_date') or available}
    if 'sources' in body:
        event['sources']=body['sources']
    else:
        event['sources']=[{'document_id':event['id'],'locator':'Event description','text':body.get('text')}]
    event=attribution._validated_event(event)
    terms_date=min(event['event_date'] or event['review_date'],event['review_date'])
    version=_select_version(state['versions'],terms_date)
    event.update(source_kind=source_kind,package_version=version['version'],status='queued',
                 analysis=None,decision={'action':'pending'},received_at=stamp())
    if uploaded_documents:
        event.update(uploaded=True, uploaded_documents=uploaded_documents, stage='Queued for document extraction')
    with connection(db_path) as con:
        if dedupe_key:
            old=con.execute('SELECT id,status FROM events WHERE dedupe=?',(dedupe_key,)).fetchone()
            if old:
                return {'event_id':old['id'],'status':old['status'],'duplicate':True}
        con.execute('INSERT INTO events(id,dedupe,status,payload) VALUES (?,?,?,?)',
                    (event['id'],dedupe_key,'queued',json.dumps(event)))
        if uploaded_documents:
            _put(con, 'uploaded_documents', _get(con, 'uploaded_documents', []) + uploaded_documents)
        _put(con,'last_update',stamp())
    return {'event_id':event['id'],'status':'queued'}


def finish(event_id, analysis, db_path=DB_PATH):
    with connection(db_path) as con:
        row=con.execute('SELECT payload FROM events WHERE id=?',(event_id,)).fetchone()
        if row is None:
            raise ValueError('Unknown event.')
        record=json.loads(row['payload'])
        record.update(analysis=analysis,status='failed' if analysis.get('engine')=='unavailable' else 'completed',analyzed_at=stamp())
        if record.get('uploaded'):
            record['stage'] = 'Analysis failed' if record['status'] == 'failed' else 'Analysis complete'
        con.execute('UPDATE events SET status=?,payload=? WHERE id=?',(record['status'],json.dumps(record),event_id))
        _put(con,'last_update',stamp())
        # A red flag (the same rule as the workspace markers) asks Nemotron whether the agreement would still be written this way.
        # Uploaded workspaces only: FluxRail and Crocs carry curated recorded comparisons that a live run must not displace mid-demo.
        flagged=(record['status']=='completed' and str(_get(con,'borrower',{}).get('id','')).startswith('U')
                 and is_detection(record,[json.loads(r['payload']) for r in con.execute('SELECT payload FROM events ORDER BY seq')]))
    if flagged:
        try:
            request_drift(db_path,record['review_date'],{'kind':'red_flag','event_id':record['id'],'title':record.get('title','')})
        except ValueError:
            pass   # a check is already running; the Run drift check button covers this report afterwards


def request_drift(db_path=DB_PATH, review_date=None, trigger=None):
    """Queue one candidate-agreement comparison. A job still waiting absorbs later requests, so two flagged reports produce one draft covering both."""
    with connection(db_path) as con:
        con.execute('BEGIN IMMEDIATE')
        completed=[json.loads(r['payload']) for r in con.execute("SELECT payload FROM events WHERE status='completed' ORDER BY seq")]
        if not completed:
            raise ValueError('Add at least one analyzed report before running a drift check.')
        review_date=review_date or max(e['review_date'] for e in completed)
        job=_get(con,'drift_job') or {}
        if job.get('status')=='processing':
            raise ValueError('A drift check is already running.')
        if any(a['review_date']==review_date and not a.get('triggered_by') for a in _get(con,'drift_assessments',[])):
            raise ValueError('A recorded comparison already covers this review date.')
        waiting=job.get('status')=='queued'
        job={'status':'queued','stage':'Waiting for Nemotron','error':None,'requested_at':stamp(),
             'review_date':max(review_date,job['review_date']) if waiting else review_date,
             'triggered_by':(job['triggered_by'] if waiting else [])+[trigger or {'kind':'manual'}]}
        _put(con,'drift_job',job)
    return job


def process_drift(api_key, model, db_path=DB_PATH):
    import b01_model, drift
    with connection(db_path) as con:
        con.execute('BEGIN IMMEDIATE')
        job=_get(con,'drift_job') or {}
        if job.get('status')!='queued':
            return False
        job.update(status='processing',stage='Nemotron is drafting the candidate agreement')
        _put(con,'drift_job',job)
        controls=_get(con,'drift_controls',{})
    try:
        state=snapshot(db_path)
        review_date=job['review_date']
        version=_select_version(state['versions'],review_date)
        reports=[e for e in state['events'] if e['status']=='completed' and e['available_at']<=review_date]
        assessments={}
        for event in sorted(reports,key=lambda e:e['review_date']):
            for finding in (event.get('analysis') or {}).get('attributions',[]):
                if finding.get('target_type')=='assumption' and finding.get('proposed_status'):
                    assessments[finding['target_id']]={'assumption_id':finding['target_id'],'status':finding['proposed_status'],
                        'review_date':event['review_date'],'report_id':event['id'],'rationale':finding.get('rationale','')}
        model=os.environ.get('B01_NEMOTRON_MODEL') or state.get('analysis_model') or b01_model.DEFAULT_MODEL
        draft=lambda mode:drift.generate_candidate(state['borrower']['id'],state['profile'],version,reports,mode=mode,review_date=review_date,
                                                   api_key=api_key,model=model,assessments=list(assessments.values()))
        # The origination-only control depends on the agreement version, not on the reports, so it is drafted once and each later check costs one call.
        key='|'.join((version['version'],model,drift.PROMPT_VERSION,str(json.loads(drift.GUIDELINES.read_text(encoding='utf-8'))['version'])))
        if key not in controls:
            controls[key]=draft('control')
            if controls[key]['engine']!='nemotron':
                raise ValueError(controls[key]['error'] or 'The origination-only control could not be drafted.')
            with connection(db_path) as con:
                _put(con,'drift_controls',controls)
        updated=draft('updated')
        if updated['engine']!='nemotron':
            raise ValueError(updated['error'] or 'The candidate agreement could not be drafted.')
        comparison={**drift.compare(controls[key],updated),'triggered_by':job['triggered_by'],'generated_at':stamp()}
        with connection(db_path) as con:
            kept=[a for a in _get(con,'drift_assessments',[]) if a['review_date']!=review_date]
            _put(con,'drift_assessments',sorted(kept+[comparison],key=lambda a:a['review_date']))
        job.update(status='done',stage='Complete',error=None,completed_at=stamp())
    except Exception as exc:
        job.update(status='failed',stage='Drift check failed',error=attribution._safe_error(exc,api_key))
    with connection(db_path) as con:
        _put(con,'drift_job',job)
    return True


def decide(body, db_path=DB_PATH):
    action=body.get('action')
    reason=body.get('reason','')
    if not isinstance(body.get('event_id'),str) or action not in ('adopt','amend','dismiss') or not isinstance(reason,str) or not reason.strip() or len(reason)>4000:
        raise ValueError('Choose adopt, amend or dismiss and provide a review reason (1–4000 characters).')
    with connection(db_path) as con:
        con.execute('BEGIN IMMEDIATE')
        row=con.execute('SELECT payload FROM events WHERE id=?',(body.get('event_id'),)).fetchone()
        if row is None:
            raise ValueError('Unknown event.')
        event=json.loads(row['payload'])
        if event.get('decision',{}).get('action')!='pending' or event['status']!='completed':
            raise ValueError('Only a completed, pending event may be decided.')
        decision={'action':'dismissed','at':stamp(),'reason':reason.strip()}
        proposal=_get(con,'pending_proposal')
        if action=='amend':
            # The analyst writes the amendment on the spot. It becomes the proposal and passes the same adoption checks as a prepared one;
            # each change carries the text the analyst edited, so an edit made against superseded terms is refused below.
            current=_get(con,'versions')[-1]
            changes=body.get('changes')
            if (not isinstance(changes,list) or not changes or len({c.get('clause_id') for c in changes if isinstance(c,dict)})!=len(changes)
                    or any(not isinstance(c.get(k),str) or not c[k].strip() or len(c[k])>20000 for c in changes for k in ('clause_id','before','after'))
                    or any(c['after'].strip()==c['before'].strip() for c in changes)):
                raise ValueError('Edit the text of at least one clause to write an amendment.')
            major,_,minor=str(current['version']).rpartition('.')
            proposal={'id':event['id']+'-AM','version':major+'.'+str(int(minor)+1),'parent_version':current['version'],
                      'trigger_event_id':event['id'],'title':'Analyst amendment: '+event.get('title',''),'rationale':reason.strip(),
                      'changes':[{'clause_id':c['clause_id'],'before':c['before'],'after':c['after'].strip()} for c in changes],
                      'authored_by':'analyst','conditions':[],'waiver_scope':'None.'}
        if action in ('adopt','amend'):
            versions=_get(con,'versions')
            if not proposal or proposal.get('trigger_event_id')!=event['id'] or proposal.get('parent_version')!=versions[-1]['version']:
                raise ValueError('No current, matching amendment proposal. Review the package first.')
            effective=attribution._parse_date(body.get('effective_at'),'effective_at')
            if effective<max(event['review_date'],event['available_at'],versions[-1]['effective_at']):
                raise ValueError('An amendment cannot be backdated before its evidence or parent version.')
            new=deepcopy(versions[-1])
            clauses={c['id']:c for c in new['clauses']}
            for change in proposal.get('changes',[]):
                clause=clauses.get(change['clause_id'])
                if clause is None or clause['clause']!=change['before']:
                    raise ValueError('Proposal terms no longer match the current package.')
                clause['clause']=change['after']
            new.update({k:deepcopy(v) for k,v in proposal.items() if k not in ('clauses','terms','definitions_and_conventions')})
            new.update(status='effective',effective_at=effective,decision_at=event['review_date'])
            new['draft_instrument_text']=proposal.get('instrument_text','')
            new['instrument_text']=(
                'Fictional amendment adopted by the user within the RealityCheck simulation. '
                'For this demo, Borrower and sole Lender agree to the following prospective changes effective '
                +effective+'. No real execution or signature is represented.\n\n'
                +'\n\n'.join(change['clause_id']+': '+change['after'] for change in proposal.get('changes',[]))
                +'\n\nHistorical findings are retained. Waiver scope: '+str(proposal.get('waiver_scope','None.')))
            versions.append(new)
            _put(con,'versions',versions)
            _put(con,'pending_proposal',None)
            decision.update(action='adopted',version=new['version'],effective_at=effective,
                            note=('Analyst-written' if action=='amend' else 'User-adopted')+' fictional amendment within the demo')
            presentation=_get(con,'presentation',{})
            presentation['as_of']=max(presentation.get('as_of',''),effective)
            _put(con,'presentation',presentation)
        if proposal and proposal.get('trigger_event_id')==event['id']:
            event['reviewed_proposal']=deepcopy(proposal)
            _put(con,'pending_proposal',None)
        event['decision']=decision
        con.execute('UPDATE events SET payload=? WHERE id=?',(json.dumps(event),event['id']))
    return snapshot(db_path)


def scan_inbox(db_path=DB_PATH, inbox=INBOX):
    Path(inbox).mkdir(parents=True,exist_ok=True)
    errors=[]
    if not snapshot(db_path).get('ready'):
        return
    for path in sorted(Path(inbox).glob('*.json')):
        try:
            raw=path.read_bytes()
            if len(raw)>200_000:
                raise ValueError('Source exceeds 200 KB.')
            body=json.loads(raw.decode('utf-8'))
            key='file:'+path.name+':'+hashlib.sha256(raw).hexdigest()
            enqueue(body,'database_update',db_path,dedupe_key=key)
        except (ValueError,UnicodeError,OSError) as exc:
            errors.append({'source':path.name,'error':str(exc)[:300]})
    with connection(db_path) as con:
        _put(con,'last_scan',stamp())
        _put(con,'feed_errors',errors)


def process_one(api_key, model, db_path=DB_PATH):
    import b01_model
    with connection(db_path) as con:
        con.execute('BEGIN IMMEDIATE')
        row=con.execute("SELECT payload FROM events WHERE status='queued' ORDER BY seq LIMIT 1").fetchone()
        if not row:
            return False
        event=json.loads(row['payload'])
        event['status']='processing'
        if event.get('uploaded'):
            event['stage'] = 'Extracting uploaded report'
        con.execute('UPDATE events SET status=?,payload=? WHERE id=?',('processing',json.dumps(event),event['id']))
        profile=_get(con,'profile')
        versions=_get(con,'versions')
        history=[json.loads(r['payload']) for r in con.execute("SELECT payload FROM events WHERE status='completed' ORDER BY seq")]
        successful_models=[e['analysis']['model'] for e in history if
                           (e.get('analysis') or {}).get('engine')=='nemotron' and e['analysis'].get('model')]
        model=(os.environ.get('B01_NEMOTRON_MODEL') or _get(con,'analysis_model') or
               (successful_models[-1] if successful_models else None) or
               _get(con,'profile_provenance',{}).get('model') or model)
    prior={}
    for old in sorted(history,key=lambda item:item.get('review_date','')):
        if old.get('review_date','')>event['review_date'] or old.get('available_at','')>event['review_date']:
            continue
        for finding in (old.get('analysis') or {}).get('attributions',[]):
            if finding.get('target_type')=='assumption' and finding.get('proposed_status'):
                prior[finding['target_id']]={'assumption_id':finding['target_id'],'status':finding['proposed_status'],
                    'review_date':old['review_date'],'event_id':old['id'],'rationale':finding.get('rationale','')}
    profile['prior_assessments']=list(prior.values())
    # Duties already found triggered or missed, so a later report that only confirms or remediates one is not read as a new detection.
    profile['prior_covenant_findings']=[{'clause_id':c['clause_id'],'status':c['status'],'event_id':old['id'],'review_date':old['review_date'],
        'package_version':c.get('package_version'),'rationale':c.get('rationale','')}
        for old in sorted(history,key=lambda item:item.get('review_date',''))
        if old.get('review_date','')<=event['review_date'] and old.get('available_at','')<=event['review_date']
        for c in (old.get('analysis') or {}).get('covenant_assessments',[]) if c.get('status') in ('noncompliant','triggered')]
    version=next(v for v in versions if v['version']==event['package_version'])
    version=deepcopy(version)
    version['known_versions']=[v for v in versions if v['effective_at']<=event['review_date']]
    try:
        if event.get('uploaded'):
            import uploads
            event.update(sources=uploads.extract_documents(event['uploaded_documents'], state_id=profile['borrower_id'],
                                                           max_chars=attribution.MAX_EVENT_TEXT), stage='Analyzing report')
            attribution._validated_event(event)
            with connection(db_path) as con:
                con.execute('UPDATE events SET payload=? WHERE id=?', (json.dumps(event), event['id']))
        analysis=b01_model.attribute_event(event,profile,version,api_key=api_key,model=model)
    except Exception as exc:
        analysis={'engine':'unavailable','model':model,'error':attribution._safe_error(exc,api_key),'attributions':[]}
    finish(event['id'],analysis,db_path)
    return True


def start_worker(api_key, model):
    global _worker
    if _worker and _worker.is_alive():
        return
    # A single local worker owns model calls; recover interrupted queued work after restart.
    for company in companies():
        db,seed,_=paths(company)
        initialize(db,seed)
        with connection(db) as con:
            onboarding = _get(con, 'onboarding', {})
            if onboarding.get('status') == 'processing':
                onboarding.update(status='queued', stage='Resuming after server restart', error=None)
                _put(con, 'onboarding', onboarding)
            drift_job = _get(con, 'drift_job') or {}
            if drift_job.get('status') == 'processing':
                drift_job.update(status='queued', stage='Resuming after server restart')
                _put(con, 'drift_job', drift_job)
            for row in con.execute("SELECT id,payload FROM events WHERE status='processing'").fetchall():
                event=json.loads(row['payload']); event['status']='queued'
                con.execute('UPDATE events SET status=?,payload=? WHERE id=?',('queued',json.dumps(event),row['id']))
    busy,claim=set(),threading.Lock()
    def run():
        while not _stop.is_set():
            worked=False
            for company in companies():
                # One worker per company at a time: each report is analyzed against the company's earlier completed reports.
                with claim:
                    if company in busy:
                        continue
                    busy.add(company)
                db,seed,inbox=paths(company)
                try:
                    if company.startswith('U') and not db.exists():
                        continue   # deleted after this pass listed it; initialize would recreate nothing but would raise on the missing folder
                    initialize(db,seed)
                    if company.startswith('U') and not snapshot(db).get('ready'):
                        import uploads
                        worked = uploads.process_company(company, api_key, model) or worked
                        continue
                    scan_inbox(db,inbox)
                    # Reports first, so a drift check drafted afterwards covers every report that arrived with the flagged one.
                    worked=(snapshot(db).get('ready') and (process_one(api_key,model,db) or process_drift(api_key,model,db))) or worked
                except Exception as exc:
                    if db.exists():   # a workspace deleted mid-pass has nowhere to record the error, and raising here would end this worker thread
                        with connection(db) as con:
                            _put(con,'feed_errors',[{'source':'worker','error':attribution._safe_error(exc,api_key)}])
                finally:
                    busy.discard(company)
            if not worked:
                _stop.wait(5)
    # ponytail: 4 threads, each model call takes 10 to 200 s, so this peaks under 10 of the key's 40 requests a minute. Raise WORKERS if the limit rises.
    for number in range(WORKERS):
        _worker=threading.Thread(target=run,name=f'company-updates-{number}',daemon=True)
        _worker.start()
