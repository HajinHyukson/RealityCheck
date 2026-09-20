(() => {
  'use strict';
  const { esc: e } = RC;
  const ui = { companyId: '', sourceId: '', tab: 'documents', kind: 'all', find: null, roomy: false, match: -1 };
  const icons = {
    doc: '<svg viewBox="0 0 18 22" aria-hidden="true"><path d="M3 1h8l4 4v16H3zM11 1v5h4M6 10h6M6 13h6M6 16h4"/></svg>',
    export: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 2v10m-4-4 4 4 4-4M3 13v4h14v-4"/></svg>',
    expand: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 3H3v4m10-4h4v4M3 13v4h4m10-4v4h-4M3 3l5 5m9-5-5 5M3 17l5-5m9 5-5-5"/></svg>',
    copy: '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7 6h10v12H7zM13 6V2H3v12h4"/></svg>'
  };
  const text = value => value == null ? '' : typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value);
  const pretty = value => text(value).replace(/[_-]/g, ' ');
  const date = value => value ? RC.date(value) : 'Date not supplied';
  const status = value => `<span class="desk-status">${e(pretty(value || 'recorded'))}</span>`;
  const query = () => ui.find ?? RC.state.query ?? '';
  function highlight(value) {
    const source = text(value), q = query().trim();
    if (!q) return e(source);
    const matcher = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    let end = 0, result = '';
    for (const found of source.matchAll(matcher)) {
      result += e(source.slice(end, found.index)) + `<mark>${e(found[0])}</mark>`;
      end = found.index + found[0].length;
    }
    return result + e(source.slice(end));
  }
  function passages(source) {
    if (!source || !text(source.text).trim()) return '<div class="desk-empty">The local source record does not include full text. Open its provenance link to inspect the original.</div>';
    return text(source.text).split(/\n\s*\n/).filter(Boolean).map((paragraph, i) => {
      let body;
      if (/^#{1,6}\s/.test(paragraph)) {
        const lines = paragraph.split('\n');
        const heading = lines.shift().replace(/^#{1,6}\s*/, '');
        body = `<h3>${highlight(heading)}</h3>${lines.length ? `<p>${highlight(lines.join('\n'))}</p>` : ''}`;
      } else if (/^```/.test(paragraph)) body = `<pre>${highlight(paragraph.replace(/^```[^\n]*\n?|```$/g, ''))}</pre>`;
      else body = `<p>${highlight(paragraph)}</p>`;
      return `<section class="desk-paragraph" id="desk-passage-${i + 1}"><span class="passage-num" aria-hidden="true">${String(i + 1).padStart(2, '0')}</span>${body}</section>`;
    }).join('');
  }
  function sourceRelations(company, sourceId) {
    const current = RC.event();
    return company.assumptions.map(assumption => {
      const finding = (current?.findings || []).find(f => f.assumptionId === assumption.id && (f.evidence || []).some(x => x.sourceId === sourceId));
      const evidence = [...(finding?.evidence || []), ...(assumption.evidence || [])].filter(x => x.sourceId === sourceId);
      const distinct = evidence.filter((x, i, all) => all.findIndex(y => y.quote === x.quote && y.locator === x.locator) === i);
      return { assumption, finding, evidence: distinct };
    }).filter(x => x.evidence.length);
  }
  function modelDetails(company) {
    const model = RC.event()?.model || company.model;
    if (!model) return '<p>No model metadata is included in this local record.</p>';
    if (typeof model === 'string') return `<p>${e(model)}</p>`;
    return `<dl>${Object.entries(model).slice(0, 8).map(([key, value]) => `<div class="desk-definition"><dt>${e(pretty(key))}</dt><dd>${e(text(value))}</dd></div>`).join('')}</dl>`;
  }
  function library(company, source) {
    const globalQuery = (RC.state.query || '').toLowerCase();
    const sources = company.sources.filter(s => (ui.kind === 'all' || s.kind === ui.kind) && (!globalQuery || `${s.title} ${text(s.text)}`.toLowerCase().includes(globalQuery)));
    const kinds = [...new Set(company.sources.map(s => s.kind).filter(Boolean))];
    return `<aside class="desk-library" aria-label="Document library">
      <div class="desk-panel-label">Source library <small>${sources.length} of ${company.sources.length}</small></div>
      <label class="sr-only" for="desk-kind">Document type</label><select id="desk-kind" class="desk-select"><option value="all">All document types</option>${kinds.map(k => `<option value="${e(k)}" ${ui.kind === k ? 'selected' : ''}>${e(pretty(k))}</option>`).join('')}</select>
      <div class="desk-doclist">${sources.length ? sources.map(s => `<button class="desk-document ${s.id === source?.id ? 'selected' : ''}" data-desk-source="${e(s.id)}" aria-pressed="${s.id === source?.id}"><span class="desk-doc-icon">${icons.doc}</span><span><strong>${e(s.title)}</strong><small>${e(date(s.date))} · ${e(pretty(s.kind || 'Source'))}</small>${s.id === source?.id ? '<em>Currently reading</em>' : ''}</span></button>`).join('') : '<div class="desk-empty">No documents match this search or document type.</div>'}</div>
      <div class="desk-library-foot"><strong>About this collection</strong><p>${e(text(company.provenance))}</p><p>${company.sources.length} local source records<br>${company.assumptions.length} underwriting assumptions</p></div>
    </aside>`;
  }
  function reader(source) {
    if (!source) return '<div class="desk-empty">No source documents are included in this company record.</div>';
    const external = /^https?:\/\//i.test(source.url || '');
    return `<section class="desk-reader" aria-label="Document reader">
      <div class="desk-reader-bar"><span>DOCUMENT READER <span aria-hidden="true">/</span> ${e(source.id)}</span><div class="desk-reader-tools"><button class="desk-tool ${ui.roomy ? 'active' : ''}" data-desk-action="type" title="Toggle larger reading text" aria-label="Toggle larger reading text" aria-pressed="${ui.roomy}">Aa</button><button class="desk-tool" data-desk-action="copy" title="Copy source citation" aria-label="Copy source citation">${icons.copy}</button><button class="desk-tool" data-source="${e(source.id)}" title="Open full source dialog" aria-label="Open full source dialog">${icons.expand}</button></div></div>
      <div class="desk-search-row"><label for="desk-find">Find in document</label><input id="desk-find" type="search" placeholder="Search this source…" value="${e(query())}" autocomplete="off"><span class="desk-match-count" id="desk-match-count"></span><button class="desk-tool" data-desk-action="previous" aria-label="Previous search match">↑</button><button class="desk-tool" data-desk-action="next" aria-label="Next search match">↓</button></div>
      <div class="desk-paper" id="desk-paper"><div class="desk-paper-meta"><span>${e(pretty(source.kind || 'Source document'))}</span><span>·</span><span>${e(date(source.date))}</span></div><h2>${e(source.title)}</h2>
      <div class="desk-provenance"><strong>Source record</strong> ${e(source.id)}<br>${source.locator ? `${e(text(source.locator))}<br>` : ''}${external ? `<a href="${e(source.url)}" target="_blank" rel="noopener noreferrer">View original source ↗</a>` : source.url ? e(source.url) : 'Text from the local project collection'}</div>
      <article class="desk-passages ${ui.roomy ? 'roomy' : ''}" id="desk-passages">${passages(source)}</article><div class="desk-paper-end"><span>End of local source text</span><span>${text(source.text).trim().split(/\s+/).filter(Boolean).length.toLocaleString()} words in record</span></div></div>
      <div class="desk-reader-bottom"><span>Original source text · ${e(pretty(source.kind || 'document'))}</span><span id="desk-copy-status" class="desk-copy-status" aria-live="polite">Read-only collection</span></div>
    </section>`;
  }
  function margin(company, source) {
    const current = RC.event(), relations = source ? sourceRelations(company, source.id) : [];
    return `<aside class="desk-margin" aria-label="Evidence annotations"><section class="desk-context"><div class="desk-panel-label">Analysis in context <small>Recorded</small></div><label class="sr-only" for="desk-event">Select recorded event</label><select class="desk-select" id="desk-event">${company.events.map(ev => `<option value="${e(ev.id)}" ${current?.id === ev.id ? 'selected' : ''}>${e(ev.title)}</option>`).join('')}</select>${current ? `<h3>${e(current.title)}</h3><div class="desk-link-top"><span>${e(date(current.date))}</span>${status("recorded analysis")}</div><p>${e(current.summary || '')}</p><button class="desk-small-action" data-inspect-event="${e(current.id)}">Inspect recorded analysis →</button>` : '<p>No recorded analysis is included in this company collection.</p>'}</section>
      <section class="desk-linked"><div class="desk-panel-label">Linked assumptions <small>${relations.length} in this source</small></div>${relations.length ? relations.map(({ assumption: a, finding, evidence }) => `<article class="desk-link-item"><div class="desk-link-top"><span>${e(a.id)}</span>${status(finding?.status || 'baseline citation')}</div><h4><button data-assumption="${e(a.id)}">${e(a.title)}</button></h4>${finding?.implication ? `<p class="desk-implication">${e(finding.implication)}</p>` : `<p class="desk-implication">${e(a.claim || '')}</p>`}${evidence[0]?.quote ? `<blockquote>“${e(evidence[0].quote)}”</blockquote>` : ''}<div class="desk-cite">${e(text(evidence[0]?.locator || source?.locator || 'Source-level reference'))}</div>${evidence[0]?.quote ? `<button class="desk-small-action" data-desk-quote="${e(evidence[0].quote)}" style="margin-top:9px">Find passage in source →</button>` : ''}</article>`).join('') : '<div class="desk-empty">No evidence citations link this source to an assumption in the selected analysis. Select another document to explore its references.</div>'}</section><p class="desk-margin-note">Connections reflect citations saved in the project. An unlinked source is not evidence that an assumption remains valid.</p></aside>`;
  }
  function records(company) {
    return `<div class="desk-records"><section><div class="desk-section-intro"><div class="desk-eyebrow">The analysis ledger</div><h2>Every event, in the record.</h2><p>Explore saved findings and the evidence cited at that point in the credit story.</p></div>${company.events.length ? company.events.map(ev => `<article class="desk-record"><div class="desk-record-heading"><div><small>${e(date(ev.date))} · ${e(ev.id)}</small><h3>${e(ev.title)}</h3></div>${status("recorded analysis")}</div><p>${e(ev.summary || '')}</p>${(ev.findings || []).map(f => { const a = company.assumptions.find(x => x.id === f.assumptionId); return `<section class="desk-finding"><div class="desk-link-top"><span>${e(f.assumptionId)}</span>${status(f.status)}</div><h4>${e(a?.title || f.assumptionId)}</h4><p>${e(f.implication || f.rationale || '')}</p><button class="desk-small-action" data-assumption="${e(f.assumptionId)}">Review assumption →</button></section>`; }).join('')}<div class="desk-record-actions"><button class="desk-button" data-inspect-event="${e(ev.id)}">Open analysis</button>${(ev.sourceIds || []).slice(0, 3).map(id => `<button class="desk-button quiet" data-desk-source="${e(id)}">Read ${e(id)}</button>`).join('')}</div></article>`).join('') : '<div class="desk-empty">No analyses are recorded for this company.</div>'}</section><aside class="desk-record-aside"><div class="desk-eyebrow">Recorded analysis metadata</div><h3>Inside the saved record</h3><p>The model information below belongs to the selected saved analysis.</p>${modelDetails(company)}<p>${e(text(company.provenance))}</p></aside></div>`;
  }
  function versions(company) {
    return `<div class="desk-records"><section><div class="desk-section-intro"><div class="desk-eyebrow">Underwriting lineage</div><h2>A versioned credit story.</h2><p>Saved revisions from the company package, with their original summaries and changes.</p></div>${company.versions.length ? company.versions.map(v => `<article class="desk-version"><div><div class="desk-version-num">${e(text(v.version || v.id))}</div><div class="desk-version-date">${e(date(v.date))}</div></div><div><div class="desk-link-top">${status(v.status)}</div><h3>${e(v.title || v.id)}</h3><p>${e(v.summary || '')}</p>${Array.isArray(v.changes) ? `<ul>${v.changes.map(c => `<li>${e(text(c))}</li>`).join('')}</ul>` : v.changes ? `<p>${e(text(v.changes))}</p>` : ''}</div></article>`).join('') : '<div class="desk-empty">This collection contains no saved version history.</div>'}</section><aside class="desk-record-aside"><div class="desk-eyebrow">Company context</div><h3>${e(company.name)}</h3><p>${e(company.summary || '')}</p><div class="desk-definition"><dt>Sector</dt><dd>${e(company.sector || 'Not supplied')}</dd></div><div class="desk-definition"><dt>Record as of</dt><dd>${e(date(company.asOf))}</dd></div><p>${e(text(company.provenance))}</p></aside></div>`;
  }
  function render() {
    const company = RC.company();
    if (ui.companyId !== company.id) Object.assign(ui, { companyId: company.id, sourceId: '', kind: 'all', find: null, match: -1 });
    if (!company.sources.some(s => s.id === ui.sourceId)) ui.sourceId = company.sources[0]?.id || '';
    const source = company.sources.find(s => s.id === ui.sourceId);
    document.getElementById('app').innerHTML = `${RC.toolbar('desk')}<main class="desk-shell"><header class="desk-masthead"><div><div class="desk-eyebrow"><i class="desk-square"></i> RealityCheck / Research desk</div><h1>A closer read. <strong>${e(company.name)}</strong></h1><p>Sources, assumptions, and the credit story between them.</p></div><div class="desk-masthead-right"><div class="desk-date">COLLECTION AS OF<strong>${e(date(company.asOf))}</strong></div><button class="desk-button" data-export>${icons.export} Export collection</button></div></header><nav class="desk-nav" aria-label="Research desk views">${[['documents', 'Documents', company.sources.length], ['analyses', 'Analysis record', company.events.length], ['versions', 'Version history', company.versions.length]].map(([id, title, count]) => `<button class="${ui.tab === id ? 'active' : ''}" data-desk-tab="${id}" aria-current="${ui.tab === id ? 'page' : 'false'}">${title}<span>${count}</span></button>`).join('')}<div class="desk-mode"><i></i> Local research collection</div></nav>${ui.tab === 'documents' ? `<div class="desk-layout">${library(company, source)}${reader(source)}${margin(company, source)}</div>` : ui.tab === 'analyses' ? records(company) : versions(company)}<footer class="desk-footer"><span>REALITYCHECK · RESEARCH DESK</span><span>Source-led investigation · Recorded analyses</span></footer></main>`;
    updateMatchCount();
  }
  function updateMatchCount() {
    const count = document.querySelectorAll('#desk-passages mark').length;
    const label = document.getElementById('desk-match-count');
    if (label) label.textContent = query().trim() ? `${count} ${count === 1 ? 'match' : 'matches'}` : '';
  }
  function jump(direction) {
    const marks = [...document.querySelectorAll('#desk-passages mark')];
    if (!marks.length) return;
    ui.match = (ui.match + direction + marks.length) % marks.length;
    marks.forEach((m, i) => m.classList.toggle('current', i === ui.match));
    marks[ui.match].scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'center' });
    const label = document.getElementById('desk-match-count');
    if (label) label.textContent = `${ui.match + 1} / ${marks.length}`;
  }
  document.addEventListener('click', async event => {
    const sourceButton = event.target.closest('[data-desk-source]');
    if (sourceButton) { ui.sourceId = sourceButton.dataset.deskSource; ui.tab = 'documents'; ui.find = null; ui.match = -1; render(); return; }
    const tab = event.target.closest('[data-desk-tab]');
    if (tab) { ui.tab = tab.dataset.deskTab; render(); return; }
    const quote = event.target.closest('[data-desk-quote]');
    if (quote) { ui.find = quote.dataset.deskQuote; ui.match = -1; render(); jump(1); return; }
    const action = event.target.closest('[data-desk-action]')?.dataset.deskAction;
    if (action === 'next') jump(1);
    if (action === 'previous') jump(-1);
    if (action === 'type') { ui.roomy = !ui.roomy; document.getElementById('desk-passages')?.classList.toggle('roomy', ui.roomy); const button = document.querySelector('[data-desk-action="type"]'); button?.classList.toggle('active', ui.roomy); button?.setAttribute('aria-pressed', String(ui.roomy)); }
    if (action === 'copy') {
      const source = RC.company().sources.find(s => s.id === ui.sourceId);
      const label = document.getElementById('desk-copy-status');
      try { await navigator.clipboard.writeText(`${source.title}. ${date(source.date)}. ${text(source.locator || '')} ${source.url || ''}`.trim()); label.textContent = 'Citation copied'; }
      catch { label.textContent = 'Clipboard unavailable. Open source to copy its citation.'; }
    }
  });
  document.addEventListener('change', event => {
    if (event.target.id === 'desk-kind') { ui.kind = event.target.value; render(); }
    if (event.target.id === 'desk-event') RC.setEvent(event.target.value);
  });
  document.addEventListener('input', event => {
    if (event.target.id !== 'desk-find') return;
    ui.find = event.target.value; ui.match = -1;
    const source = RC.company().sources.find(s => s.id === ui.sourceId);
    document.getElementById('desk-passages').innerHTML = passages(source); updateMatchCount();
  });
  document.addEventListener('keydown', event => { if (event.target.id === 'desk-find' && event.key === 'Enter') { event.preventDefault(); jump(event.shiftKey ? -1 : 1); } });
  RC.init('desk', render);
})();
