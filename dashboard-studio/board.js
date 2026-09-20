(() => {
  'use strict';
  const ui = { view: 'board', filter: 'all', assumptionId: '', detail: 'assessment', companyId: '' };
  const list = value => Array.isArray(value) ? value : [];
  const value = v => v == null ? '' : typeof v === 'object' ? JSON.stringify(v) : String(v);
  const e = v => RC.esc(value(v));
  const words = v => value(v).replaceAll('_', ' ');
  const icon = name => `<svg class="b-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${({board:'<rect x="3" y="4" width="5" height="16" rx="1"/><rect x="10" y="4" width="5" height="11" rx="1"/><rect x="17" y="4" width="4" height="14" rx="1"/>',evidence:'<path d="M6 3h9l4 4v14H6zM14 3v5h5M9 12h7M9 16h5"/>',trace:'<circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M5 7v7a5 5 0 0 0 5 5h7M9 5h10v7m-4-4 4 4 4-4"/>',arrow:'<path d="M5 12h14m-5-5 5 5-5 5"/>',download:'<path d="M12 3v12m-4-4 4 4 4-4M4 17v4h16v-4"/>',check:'<path d="m5 12 4 4L19 6"/>',link:'<path d="m9 15 6-6M7 17l-1 1a4 4 0 0 1-6-6l5-5a4 4 0 0 1 6 0m2 0 1-1a4 4 0 1 1 6 6l-5 5a4 4 0 0 1-6 0" transform="translate(2 -1)"/>'})[name] || ''}</svg>`;
  const status = row => row?.status || 'not assessed';
  const short = (text, max = 140) => value(text).length > max ? value(text).slice(0, max).trim() + '…' : value(text);
  const sourceLink = (sourceId, title) => sourceId ? `<button class="b-source-link" data-source="${e(sourceId)}">${icon('evidence')}${e(title || 'Open source')}${icon('arrow')}</button>` : '<span class="b-source-link">Source not linked in record</span>';

  function context() {
    const company = RC.company();
    const event = RC.event() || list(company.events).at(-1) || {};
    if (ui.companyId !== company.id) { ui.companyId = company.id; ui.assumptionId = ''; ui.filter = 'all'; }
    const findings = list(event.findings);
    const assumptions = list(company.assumptions);
    const query = value(RC.state.query).toLowerCase();
    const visible = assumptions.filter(a => {
      const finding = findings.find(f => f.assumptionId === a.id);
      return (!query || value([a.id,a.title,a.claim,finding?.rationale,finding?.implication]).toLowerCase().includes(query)) &&
        (ui.filter !== 'attention' || /contradict|weaken|adverse|invalid|breach|uncertain/i.test(value([finding?.status,finding?.implication]))) &&
        (ui.filter !== 'evidence' || list(finding?.evidence).length > 0);
    });
    if (!visible.some(a => a.id === ui.assumptionId)) ui.assumptionId = visible[0]?.id || '';
    const assumption = visible.find(a => a.id === ui.assumptionId);
    const finding = findings.find(f => f.assumptionId === assumption?.id);
    return {company,event,findings,assumptions,visible,assumption,finding};
  }

  function queue(c) {
    return `<aside class="b-queue"><h2 class="b-section-label">Report queue <span>${list(c.events).length}</span></h2><p class="b-queue-intro">Choose a reporting moment to inspect its recorded assessment.</p>${[...list(c.events)].reverse().map(ev => `<button class="b-report ${ev.id === RC.state.eventId ? 'selected' : ''}" data-event="${e(ev.id)}"><time>${e(RC.date(ev.date))}</time><strong>${e(ev.title)}</strong><span class="b-report-foot"><span>${list(ev.findings).length} findings</span><span>${ev.id === RC.state.eventId ? 'In view' : icon('arrow')}</span></span></button>`).join('')}<div class="b-queue-bottom"><h3 class="b-section-label">Working context</h3><p>${e(c.sector || 'Credit monitoring')}<br>${list(c.assumptions).length} underwriting assumptions<br>${list(c.covenants).length} covenant records</p></div></aside>`;
  }

  function board({company, event, visible, assumption, finding, findings}) {
    const evidence = list(finding?.evidence);
    return `<div class="b-columns"><section class="b-column"><div class="b-column-title"><i class="b-dot"></i>Inquiry <span class="b-count">${visible.length}</span></div>${visible.length ? visible.map((a,i) => {
      const f = findings.find(x => x.assumptionId === a.id);
      return `<button class="b-inquiry ${a.id === ui.assumptionId ? 'selected' : ''}" data-b-select="${e(a.id)}"><div class="b-card-kicker"><span>${e(a.id)}</span><span>${String(i + 1).padStart(2,'0')}</span></div><h3>${e(a.title)}</h3><p class="b-clamp">${e(a.claim || a.basis)}</p><div class="b-card-foot"><span>${list(f?.evidence).length} evidence links</span><span>${icon('arrow')}</span></div></button>`;
    }).join('') : '<div class="b-empty">No inquiries match this view. Choose another filter or clear the search.</div>'}<div class="b-lane-note">Select an inquiry to follow its evidence and recorded conclusion.</div></section><section class="b-column"><div class="b-column-title"><i class="b-dot"></i>Evidence <span class="b-count">${evidence.length}</span></div><div class="b-unselected-note">${assumption ? `Linked to ${e(assumption.id)}` : 'Select an inquiry'}</div>${evidence.length ? evidence.map((item,i) => {
      const source = list(company.sources).find(s => s.id === item.sourceId);
      return `<article class="b-evidence"><div class="b-evidence-kind">${icon('evidence')}Source excerpt ${String(i+1).padStart(2,'0')}</div><blockquote>“${e(short(item.quote,230))}”</blockquote><details><summary>Expand evidence</summary><p>${e(item.quote)}</p><p>${e(item.locator || source?.locator || 'Locator not recorded')}</p></details><div class="b-card-foot"><span>${item.verified === true ? 'Quote verified' : item.verified === false ? 'Quote unverified' : 'Verification not recorded'}</span></div><div style="margin-top:11px">${sourceLink(item.sourceId, short(source?.title || 'Source document',46))}</div></article>`;
    }).join('') : '<div class="b-empty">No source excerpts are attached to this finding in the recorded analysis.</div>'}<div class="b-lane-note">Evidence is shown as saved. Open a source to inspect its original context.</div></section><section class="b-column"><div class="b-column-title"><i class="b-dot"></i>Findings <span class="b-count">${visible.filter(a=>findings.some(f=>f.assumptionId===a.id)).length}</span></div>${visible.map(a=>{
      const f = findings.find(x=>x.assumptionId===a.id);
      if(!f) return '';
      return `<article class="b-finding ${a.id===ui.assumptionId?'selected':''}"><div class="b-card-kicker"><span>${e(a.id)}</span><span>Recorded</span></div>${RC.badge(status(f))}<h3>${e(a.title)}</h3><p class="b-finding-rationale">${e(f.rationale || f.implication || 'No rationale recorded.')}</p><div class="b-finding-bottom"><p>${e(f.implication || 'No implication recorded')}</p><button data-b-select="${e(a.id)}" aria-label="Inspect ${e(a.title)}">${icon('arrow')}</button></div></article>`;
    }).join('') || '<div class="b-empty">No recorded findings for the current inquiries.</div>'}</section></div>`;
  }

  function evidenceTable({company,visible,findings}) {
    const rows = visible.flatMap(a=>list(findings.find(f=>f.assumptionId===a.id)?.evidence).map(item=>({a,item})));
    return `<p class="b-trace-intro">A source ledger for the inquiries in view. Each excerpt retains its saved locator and verification state.</p>${rows.length ? `<table class="b-source-table"><thead><tr><th>Source / inquiry</th><th>Recorded excerpt</th><th>Verification</th></tr></thead><tbody>${rows.map(({a,item})=>{
      const source = list(company.sources).find(s=>s.id===item.sourceId);
      return `<tr><td>${sourceLink(item.sourceId,source?.title || 'Source document')}<p class="b-num">${e(a.id)} · ${e(a.title)}</p></td><td><blockquote>“${e(item.quote)}”</blockquote><div style="margin-top:9px;font-size:10px">${e(item.locator || source?.locator || 'Locator not recorded')}</div></td><td>${item.verified === true ? 'Verified quote' : item.verified === false ? 'Unverified quote' : 'Not recorded'}</td></tr>`;
    }).join('')}</tbody></table>` : '<div class="b-empty">No evidence is linked to the inquiries in this view.</div>'}`;
  }

  function trace({company,event,assumption,finding}) {
    if(!assumption) return '<div class="b-empty">Select an inquiry to inspect its recorded relationships.</div>';
    const sourceIds = [...new Set(list(finding?.evidence).map(x=>x.sourceId).filter(Boolean))];
    const covenants = list(company.covenants).filter(x=>[...list(assumption.covenantIds),...list(finding?.covenantIds)].includes(x.id));
    const steps = [
      ['Underwriting assumption',assumption.claim || assumption.basis || assumption.title,`<button data-assumption="${e(assumption.id)}">Inspect ${e(assumption.id)}</button>`],
      ['Selected reporting moment',event.title,`<button data-event="${e(event.id)}">${e(RC.date(event.date))} · Report context</button>`],
      ['Linked source evidence',sourceIds.length ? `${sourceIds.length} source documents linked to this recorded finding.` : 'No source document links are saved for this finding.',sourceIds.map(id=>`<button data-source="${e(id)}">${e(short(list(company.sources).find(s=>s.id===id)?.title || id,60))}</button>`).join('')],
      ['Recorded assessment',finding ? `${words(status(finding))} — ${finding.rationale || finding.implication || 'No rationale recorded.'}` : 'No recorded assessment for this report.',''],
      ['Credit agreement context',covenants.length ? covenants.map(x=>x.title).join(' · ') : 'No covenant relationship is recorded for this inquiry.',`<button data-b-detail="covenants">Inspect linked covenants</button>`]
    ];
    return `<p class="b-trace-intro">The saved relationships behind <strong>${e(assumption.id)}</strong>. This view follows the record from underwriting context to the assessment and agreement references.</p>${steps.map(([title,body,buttons],i)=>`<div class="b-trace-row"><span class="b-trace-number">${i+1}</span><div class="b-trace-body"><h3>${e(title)}</h3><p>${e(body)}</p>${buttons ? `<div class="b-trace-chips">${buttons}</div>` : ''}</div></div>`).join('')}`;
  }

  function detail({company,assumption,finding}) {
    if(!assumption) return '<aside class="b-detail"><div class="b-empty">Select an inquiry to inspect its analysis.</div></aside>';
    let body;
    if(ui.detail==='history') {
      const history = list(company.events).map(ev=>({ev,f:list(ev.findings).find(x=>x.assumptionId===assumption.id)})).filter(x=>x.f);
      body = history.length ? [...history].reverse().map(({ev,f})=>`<article class="b-history"><time>${e(RC.date(ev.date))}</time><p>${e(ev.title)}</p>${RC.badge(status(f))}<p>${e(f.rationale || f.implication)}</p><button class="b-source-link" data-event="${e(ev.id)}">Open reporting moment ${icon('arrow')}</button></article>`).join('') : '<p class="b-detail-text">No recorded history for this inquiry.</p>';
    } else if(ui.detail==='covenants') {
      const covenants = list(company.covenants).filter(x=>[...list(assumption.covenantIds),...list(finding?.covenantIds)].includes(x.id));
      body = covenants.length ? '<p class="b-detail-text">Original package and added provisions. Dated amendments may change these terms.</p>' + covenants.map(c=>`<article class="b-linked-covenant"><div class="b-detail-label">${e(c.id)}</div><strong>${e(c.title)}</strong><p>${e(c.text)}</p></article>`).join('') : '<p class="b-detail-text">No covenant relationships are recorded for this inquiry.</p>';
    } else {
      body = `<div class="b-detail-label">Original assumption</div><p class="b-detail-text">${e(assumption.claim || assumption.basis || 'No assumption text recorded.')}</p><div class="b-detail-label">Recorded rationale</div><p class="b-detail-text">${e(finding?.rationale || 'No assessment rationale recorded for the selected report.')}</p>${finding?.action ? `<div class="b-action"><div class="b-detail-label">Recorded follow-up</div><p>${e(words(finding.action))}</p></div>` : ''}<div class="b-proof">${icon('evidence')} ${list(finding?.evidence).length} evidence excerpts · ${list(finding?.evidence).filter(x=>x.verified===true).length} verified</div>`;
    }
    return `<aside class="b-detail"><div><div class="b-detail-header"><span>Analysis inspector</span>${icon('board')}</div><div class="b-detail-id">${e(assumption.id)} / RECORDED ANALYSIS</div><h2>${e(assumption.title)}</h2>${RC.badge(status(finding))}</div><div class="b-detail-tabs">${[['assessment','Assessment'],['covenants','Covenants'],['history','History']].map(([id,label])=>`<button data-b-detail="${id}" class="${ui.detail===id?'active':''}">${label}</button>`).join('')}</div><div class="b-detail-body">${body}</div><div class="b-detail-footer"><button class="b-outline" data-assumption="${e(assumption.id)}">Open assumption record ${icon('arrow')}</button><p>${e(RC.event()?.analysisStatus || 'Recorded analysis')}</p><p>Recorded model: ${e(value(RC.event()?.model || company.model || 'Not specified in source record'))}</p></div></aside>`;
  }

  function render() {
    const c = context();
    const {company,event,findings,visible} = c;
    document.getElementById('app').innerHTML = `${RC.toolbar('board')}<div class="b-shell"><header class="b-top"><div class="b-crumb">WORKSPACE <span>/</span><b>${e(company.name)}</b><span>/</span> Investigation</div><div class="b-heading"><div><h1>Follow the evidence.</h1><p>Connect underwriting assumptions to what the reports actually say.</p></div><div class="b-heading-actions"><span class="b-stamp">${e(company.id)} · ${list(company.events).length} reporting moments</span><button class="b-outline" data-b-view="trace">${icon('trace')}View trace</button><button class="b-primary" data-export>${icon('download')}Export view</button></div></div><div class="b-top-nav"><nav class="b-tabs" aria-label="Investigation views">${[['board','Investigation board',visible.length],['evidence','Evidence ledger',findings.reduce((n,f)=>n+list(f.evidence).length,0)],['trace','Record trace','']].map(([id,label,count])=>`<button class="b-tab ${ui.view===id?'active':''}" data-b-view="${id}">${icon(id)}${label}${count!==''?`<small>${count}</small>`:''}</button>`).join('')}</nav><span class="b-stamp">Source-backed workspace</span></div></header><div class="b-layout">${queue(company)}<main class="b-main"><div class="b-context"><div><div class="b-section-label">${e(company.id)} / Selected reporting moment</div><h2>${e(event.title || 'No reporting moment available')}</h2><p>${e(short(event.summary || company.summary,220))}</p></div><span class="b-context-date">${e(RC.date(event.date))}</span></div><div class="b-tools"><div class="b-filter" aria-label="Filter inquiries">${[['all','All inquiries'],['attention','Needs attention'],['evidence','Has evidence']].map(([id,label])=>`<button data-b-filter="${id}" class="${ui.filter===id?'active':''}">${label}</button>`).join('')}</div><span class="b-tool-note">${visible.length} of ${list(company.assumptions).length} inquiries</span></div>${ui.view==='evidence'?evidenceTable(c):ui.view==='trace'?trace(c):board(c)}<footer class="b-board-footer"><span><i class="b-status-dot"></i> Saved repository records</span><span>Report → evidence → assessment</span><span>${e(RC.date(company.asOf))}</span></footer></main>${detail(c)}</div></div>`;
  }
  document.addEventListener('click',event=>{
    const button=event.target.closest('[data-b-view],[data-b-filter],[data-b-select],[data-b-detail]');
    if(!button)return;
    if(button.dataset.bView)ui.view=button.dataset.bView;
    if(button.dataset.bFilter)ui.filter=button.dataset.bFilter;
    if(button.dataset.bSelect){ui.assumptionId=button.dataset.bSelect;ui.detail='assessment';}
    if(button.dataset.bDetail)ui.detail=button.dataset.bDetail;
    render();
  });
  RC.init('board',render);
})();
