(() => {
  'use strict';
  const { esc: e } = RC;
  const ui = { companyId: '', tab: 'matrix', scope: 'all', status: 'all', sourceId: '', assumptionId: '', compact: false };
  const exportIcon = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2v10m-4-4 4 4 4-4M3 13v4h14v-4"/></svg>';
  const pretty = value => String(value || 'unassessed').replaceAll('_', ' ');
  const tone = status => ({ supported: 'supported', weakened: 'weakened', contradicted: 'contradicted', baseline: 'baseline', unassessed: 'unassessed' })[status] || 'unassessed';
  const symbol = status => ({ supported: '↗', weakened: '↘', contradicted: '×', baseline: '·', unassessed: '○' })[status] || '○';
  const date = value => value ? RC.date(value) : 'Undated';
  function scopedEvents(company) { return ui.scope === 'all' ? company.events : company.events.filter(ev => ev.id === RC.event()?.id); }
  function relationships(company, sourceId, assumptionId) {
    const a = company.assumptions.find(x => x.id === assumptionId);
    const records = [];
    const baseline = (a?.evidence || []).filter(x => x.sourceId === sourceId);
    if (baseline.length) records.push({ status: 'baseline', evidence: baseline, kind: 'baseline', assumption: a });
    for (const ev of scopedEvents(company)) for (const finding of ev.findings || []) {
      if (finding.assumptionId !== assumptionId) continue;
      const evidence = (finding.evidence || []).filter(x => x.sourceId === sourceId);
      if (evidence.length) records.push({ ...finding, status: finding.status || 'unassessed', evidence, event: ev, kind: 'finding', assumption: a });
    }
    return records;
  }
  function matrixData(company) {
    const rows = [...company.sources].sort((a, b) => String(b.date || '').localeCompare(String(a.date || '')));
    const map = new Map();
    for (const s of rows) for (const a of company.assumptions) map.set(`${s.id}|${a.id}`, relationships(company, s.id, a.id));
    const all = [...map.values()].filter(list => list.length);
    const queries = String(RC.state.query || '').toLowerCase();
    const visibleRows = rows.filter(s => !queries || `${s.title} ${s.kind} ${s.text}`.toLowerCase().includes(queries) || company.assumptions.some(a => `${a.title} ${a.claim}`.toLowerCase().includes(queries) && map.get(`${s.id}|${a.id}`).length));
    return { rows, visibleRows, map, all };
  }
  function stats(company, data) {
    const cited = data.rows.filter(s => company.assumptions.some(a => data.map.get(`${s.id}|${a.id}`).length)).length;
    const unlinked = data.rows.length - cited;
    const possible = company.sources.length * company.assumptions.length;
    return `<section class="mx-summary" aria-label="Collection overview"><div class="mx-stat"><div class="mx-stat-label">Source documents</div><div class="mx-stat-line"><span class="mx-stat-value">${company.sources.length}</span><span class="mx-stat-unit">in collection</span></div><div class="mx-stat-track"><span style="width:${data.rows.length ? cited / data.rows.length * 100 : 0}%"></span></div></div><div class="mx-stat"><div class="mx-stat-label">Underwriting assumptions</div><div class="mx-stat-line"><span class="mx-stat-value">${company.assumptions.length}</span><span class="mx-stat-unit">tracked</span></div><div class="mx-stat-track"><span style="width:${company.assumptions.length ? company.assumptions.filter(a => company.sources.some(s => data.map.get(`${s.id}|${a.id}`).length)).length / company.assumptions.length * 100 : 0}%"></span></div></div><div class="mx-stat"><div class="mx-stat-label">Cited source–assumption pairs</div><div class="mx-stat-line"><span class="mx-stat-value">${data.all.length}</span><span class="mx-stat-unit">of ${possible} possible</span></div><div class="mx-stat-track"><span style="width:${possible ? data.all.length / possible * 100 : 0}%"></span></div></div><div class="mx-stat"><div class="mx-focal-number">${unlinked}</div><div class="mx-focal-text"><strong>Sources without saved citations</strong><p>${ui.scope === 'all' ? 'Across baseline evidence and all recorded analyses.' : 'Across baseline evidence and the selected analysis.'}</p></div></div></section>`;
  }
  function cell(records, s, a) {
    const selected = s.id === ui.sourceId && a.id === ui.assumptionId;
    const latest = records.at(-1);
    const faded = ui.status !== 'all' && latest?.status !== ui.status;
    const label = latest ? `${s.title}: ${a.title}, ${pretty(latest.status)}; ${records.length} recorded ${records.length === 1 ? 'connection' : 'connections'}` : `${s.title}: ${a.title}, no recorded citation`;
    return `<td class="${selected ? 'mx-selected-cell' : ''}"><button class="${latest ? `mx-cell ${tone(latest.status)} ${faded ? 'filtered' : ''} ${selected ? 'selected' : ''}` : 'mx-empty-cell'}" data-mx-cell="${e(s.id)}" data-mx-assumption="${e(a.id)}" aria-label="${e(label)}" title="${e(label)}" aria-pressed="${selected}">${latest ? `<span class="mx-cell-symbol" aria-hidden="true">${symbol(latest.status)}</span>${e(pretty(latest.status))}${records.length > 1 ? `<span class="mx-cell-count">${records.length}</span>` : ''}` : '—'}</button></td>`;
  }
  function grid(company, data) {
    const statuses = [...new Set(data.all.map(records => records.at(-1).status))].sort((a, b) => ['supported', 'weakened', 'contradicted', 'unassessed', 'baseline'].indexOf(a) - ['supported', 'weakened', 'contradicted', 'unassessed', 'baseline'].indexOf(b));
    return `<section class="mx-matrix-panel"><div class="mx-panel-top"><div><h2>Evidence relationships</h2><p>Documents × underwriting assumptions · newest sources first</p></div><div class="mx-panel-top-right"><div class="mx-scope-control"><label for="mx-scope">Analysis scope</label><select id="mx-scope"><option value="all" ${ui.scope === 'all' ? 'selected' : ''}>All recorded analyses + baseline</option><option value="selected" ${ui.scope === 'selected' ? 'selected' : ''}>Selected analysis + baseline</option></select></div></div></div><div class="mx-filter-bar"><span class="mx-filter-label">Highlight status</span><button class="mx-filter ${ui.status === 'all' ? 'active' : ''}" data-mx-status="all">All connections</button>${statuses.map(s => `<button class="mx-filter ${ui.status === s ? 'active' : ''}" data-mx-status="${e(s)}"><span class="mx-dot"></span>${e(pretty(s))}</button>`).join('')}<label class="mx-density"><input type="checkbox" id="mx-compact" ${ui.compact ? 'checked' : ''}> Compact</label></div>${ui.scope === 'selected' ? `<div class="mx-filter-bar"><label class="mx-filter-label" for="mx-event">Recorded event</label><div class="mx-scope-control" style="flex:1"><select id="mx-event" style="max-width:100%;width:100%">${company.events.map(ev => `<option value="${e(ev.id)}" ${ev.id === RC.event()?.id ? 'selected' : ''}>${e(date(ev.date))} · ${e(ev.title)}</option>`).join('')}</select></div></div>` : ''}<div class="mx-table-wrap" id="mx-table-wrap"><table class="mx-table ${ui.compact ? 'compact' : ''}" style="min-width:${Math.max(660, 223 + company.assumptions.length * 112)}px"><thead><tr><th class="mx-source-col" scope="col"><div class="mx-axis-label">ROWS / DOCUMENTS<strong>COLUMNS / ASSUMPTIONS →</strong></div></th>${company.assumptions.map(a => `<th scope="col"><button class="mx-column-title" data-assumption="${e(a.id)}"><span>${e(a.id)}</span><strong>${e(a.title)}</strong><small>${company.sources.filter(s => data.map.get(`${s.id}|${a.id}`).length).length} linked sources ↗</small></button></th>`).join('')}</tr></thead><tbody>${data.visibleRows.map(s => `<tr class="${s.id === ui.sourceId ? 'selected-row' : ''}"><th scope="row" class="mx-source-col"><button class="mx-row-source" data-mx-source="${e(s.id)}"><strong>${e(s.title)}</strong><span class="mx-row-meta"><span class="mx-file-sign">DOC</span>${e(date(s.date))}</span></button></th>${company.assumptions.map(a => cell(data.map.get(`${s.id}|${a.id}`), s, a)).join('')}</tr>`).join('')}</tbody></table>${data.visibleRows.length ? '' : '<div class="mx-empty-state">No source documents match this search.<br>Clear the company search to restore the full matrix.</div>'}</div><div class="mx-table-foot"><span>${data.visibleRows.length} of ${company.sources.length} source documents · ${company.assumptions.length} assumptions</span><span>Select a cell to investigate →</span></div></section><div class="mx-legend"><div class="mx-legend-list"><span class="mx-legend-item"><i class="supported"></i> Supported</span><span class="mx-legend-item"><i class="weakened"></i> Weakened</span><span class="mx-legend-item"><i class="contradicted"></i> Contradicted</span><span class="mx-legend-item"><i class="baseline"></i> Baseline citation</span><span class="mx-legend-item"><i class="unassessed"></i> Unassessed</span></div><p>A cell shows the latest recorded status citing that source. A dash means no saved citation; it does not imply support.</p></div>`;
  }
  function detail(company, data) {
    const source = company.sources.find(s => s.id === ui.sourceId);
    const a = company.assumptions.find(a => a.id === ui.assumptionId);
    const records = data.map.get(`${ui.sourceId}|${ui.assumptionId}`) || [];
    const latest = records.at(-1);
    if (!source || !a) return '<aside class="mx-detail"><div class="mx-empty-state">Select a source–assumption cell to inspect its recorded evidence.</div></aside>';
    return `<aside class="mx-detail" aria-label="Selected relationship"><header class="mx-detail-head"><div class="mx-detail-eyebrow"><span>Relationship inspector</span><span>${records.length ? 'CITED' : 'NO CITATION'}</span></div><h2>${e(a.title)}</h2><div class="mx-detail-id">${e(a.id)}</div></header><div class="mx-detail-body"><section class="mx-detail-section"><div class="mx-section-label">Underwriting assumption</div><p>${e(a.claim || 'No claim text supplied.')}</p><button class="mx-text-link" data-assumption="${e(a.id)}">View full assumption →</button></section><section class="mx-detail-section"><div class="mx-section-label">Source document</div><button class="mx-detail-source" data-source="${e(source.id)}">${e(source.title)}<small>${e(date(source.date))} · Open source ↗</small></button><div class="mx-citation">${e(source.locator || 'Local source record')}</div></section><section class="mx-detail-section"><div class="mx-section-label">${latest?.kind === 'baseline' ? 'Original evidence' : 'Recorded assessment'}</div>${latest ? `<div class="mx-detail-status"><span class="mx-cell ${tone(latest.status)}"><span class="mx-cell-symbol">${symbol(latest.status)}</span>${e(pretty(latest.status))}</span>${latest.event ? `<span class="mx-citation">${e(date(latest.event.date))}</span>` : ''}</div>${latest.event ? `<h3>${e(latest.event.title)}</h3><p>${e(latest.implication || latest.rationale || '')}</p>` : '<p>This passage was cited when the underwriting assumption was recorded.</p>'}${latest.evidence.map(item => `<blockquote class="mx-quote">“${e(item.quote || 'Quotation not included in record.')}”</blockquote><div class="mx-citation">${e(item.locator || source.locator || item.sourceId)} · ${item.verified ? 'Quote matched to source' : 'Verification not recorded'}</div>`).join('')}${latest.event ? `<button class="mx-text-link" style="margin-top:13px" data-inspect-event="${e(latest.event.id)}">Inspect saved analysis →</button>` : ''}${records.length > 1 ? `<div class="mx-citation" style="margin-top:13px">${records.length} saved connections for this pair. Showing the latest record.</div>` : ''}` : '<div class="mx-no-evidence">There is no recorded citation connecting this source to this assumption in the current scope. Review the source to investigate the gap.</div>'}</section>${latest?.action ? `<section class="mx-detail-section"><div class="mx-section-label">Recorded follow-up</div><p>${e(pretty(latest.action))}</p></section>` : ''}</div><footer class="mx-detail-footer"><span>Source-linked record</span><button class="mx-btn" data-source="${e(source.id)}">Open document ↗</button></footer></aside>`;
  }
  function coverage(company, data) {
    return `<section class="mx-coverage-panel"><header class="mx-coverage-heading"><div><div class="mx-kicker">Citation coverage</div><h2>Where the record has support.</h2><p>Inspect the source documents cited for each assumption. Coverage describes saved references, not whether a credit claim is valid.</p></div><button class="mx-btn" data-mx-tab="matrix">Back to matrix →</button></header>${company.assumptions.map(a => {
      const sources = company.sources.filter(s => data.map.get(`${s.id}|${a.id}`).length);
      const evidence = sources.flatMap(s => data.map.get(`${s.id}|${a.id}`).flatMap(x => x.evidence));
      return `<article class="mx-audit-row"><div><div class="mx-audit-id">${e(a.id)}</div><h3><button class="mx-text-link" data-assumption="${e(a.id)}" style="font-size:13px;color:inherit">${e(a.title)}</button></h3><p>${e(a.claim || '')}</p></div><div class="mx-audit-sources">${sources.length ? sources.map(s => `<button data-source="${e(s.id)}">${e(s.title)} ↗</button>`).join('') : '<p>No source citation is attached to this assumption.</p>'}<div class="mx-citation">${evidence.filter(x => x.verified).length} of ${evidence.length} citation records matched to supplied source text</div></div><div class="mx-audit-count">${sources.length}<span>linked sources</span></div></article>`;
    }).join('')}</section>`;
  }
  function trail(company) {
    return `<section class="mx-coverage-panel"><header class="mx-coverage-heading"><div><div class="mx-kicker">Analysis trail</div><h2>How the evidence developed.</h2><p>Saved event assessments in reverse chronological order. Open a record to inspect the cited passages, model metadata, and retained reviewer notes.</p></div></header>${[...company.events].reverse().map(ev => `<article class="mx-timeline"><div class="mx-timeline-date">${e(date(ev.date))}<strong>${e(ev.id)}</strong></div><div><h3>${e(ev.title)}</h3><p>${e(ev.summary || '')}</p><div class="mx-timeline-findings">${(ev.findings || []).map(f => `<button data-assumption="${e(f.assumptionId)}">${e(f.assumptionId)} · ${e(pretty(f.status))}</button>`).join('')}</div><div class="mx-record-status">${e(ev.analysisStatus || 'Recorded analysis')}</div><button class="mx-text-link" data-inspect-event="${e(ev.id)}">Inspect full analysis →</button></div></article>`).join('') || '<div class="mx-empty-state">No event analyses are included in this collection.</div>'}</section>`;
  }
  function render() {
    const company = RC.company();
    if (ui.companyId !== company.id) Object.assign(ui, { companyId: company.id, sourceId: '', assumptionId: '', status: 'all', scope: 'all' });
    const data = matrixData(company);
    if (!company.sources.some(s => s.id === ui.sourceId)) {
      const first = data.visibleRows.find(s => company.assumptions.some(a => data.map.get(`${s.id}|${a.id}`).length)) || data.visibleRows[0];
      ui.sourceId = first?.id || '';
    }
    if (!company.assumptions.some(a => a.id === ui.assumptionId)) ui.assumptionId = company.assumptions.find(a => data.map.get(`${ui.sourceId}|${a.id}`)?.length)?.id || company.assumptions[0]?.id || '';
    document.getElementById('app').innerHTML = `${RC.toolbar('matrix')}<main class="mx-shell"><header class="mx-header"><div><div class="mx-kicker"><span class="mx-mini-grid" aria-hidden="true"><i></i><i></i><i></i><i></i></span> Signal matrix / ${e(company.sector || 'Credit research')}</div><h1>Follow the evidence. <span>${e(company.name)}</span></h1><p>Every source. Every assumption. The connections that change the credit story.</p></div><div class="mx-header-meta"><div class="mx-asof">COLLECTION AS OF<strong>${e(date(company.asOf))}</strong></div><button class="mx-btn accent" data-export>${exportIcon} Export data</button></div></header><nav class="mx-navigation" aria-label="Matrix views">${[['matrix', 'Relationship matrix', data.all.length], ['coverage', 'Coverage audit', company.assumptions.length], ['trail', 'Analysis trail', company.events.length]].map(([id, title, n]) => `<button class="mx-nav-button ${ui.tab === id ? 'active' : ''}" data-mx-tab="${id}" aria-current="${ui.tab === id ? 'page' : 'false'}">${title}<span class="mx-nav-count">${n}</span></button>`).join('')}<span class="mx-nav-note">Recorded analysis · Local collection</span></nav>${stats(company, data)}${ui.tab === 'matrix' ? `<div class="mx-workspace"><div class="mx-main">${grid(company, data)}</div>${detail(company, data)}</div>` : ui.tab === 'coverage' ? coverage(company, data) : trail(company)}<footer class="mx-footer"><span>REALITYCHECK / SIGNAL MATRIX</span><span>${e(company.id)} · ${e(company.provenance)} · Source-level citations</span></footer></main>`;
  }
  function rerenderPreservingScroll() {
    const area = document.getElementById('mx-table-wrap');
    const pos = area ? { top: area.scrollTop, left: area.scrollLeft } : null;
    render();
    const next = document.getElementById('mx-table-wrap');
    if (next && pos) { next.scrollTop = pos.top; next.scrollLeft = pos.left; }
  }
  document.addEventListener('click', event => {
    const cell = event.target.closest('[data-mx-cell]');
    if (cell) { ui.sourceId = cell.dataset.mxCell; ui.assumptionId = cell.dataset.mxAssumption; rerenderPreservingScroll(); return; }
    const source = event.target.closest('[data-mx-source]');
    if (source) { ui.sourceId = source.dataset.mxSource; const company = RC.company(); ui.assumptionId = company.assumptions.find(a => relationships(company, ui.sourceId, a.id).length)?.id || company.assumptions[0]?.id || ''; rerenderPreservingScroll(); return; }
    const filter = event.target.closest('[data-mx-status]');
    if (filter) { ui.status = filter.dataset.mxStatus; rerenderPreservingScroll(); return; }
    const tab = event.target.closest('[data-mx-tab]');
    if (tab) { ui.tab = tab.dataset.mxTab; render(); }
  });
  document.addEventListener('change', event => {
    if (event.target.id === 'mx-scope') { ui.scope = event.target.value; ui.status = 'all'; rerenderPreservingScroll(); }
    if (event.target.id === 'mx-event') RC.setEvent(event.target.value);
    if (event.target.id === 'mx-compact') { ui.compact = event.target.checked; document.querySelector('.mx-table')?.classList.toggle('compact', ui.compact); }
  });
  RC.init('matrix', render);
})();
