/* Saved package chronology. Selecting a report changes the shared investigation only. */
(() => {
  'use strict';
  const fullHistory = new Set();
  const day = 86400000;
  const list = value => Array.isArray(value) ? value : [];
  const esc = value => RC.esc(value == null ? '' : String(value));
  const time = value => Date.parse(String(value || '').slice(0, 10) + 'T12:00:00Z');
  const pending = version => version.isProposal || version.status === 'proposed';
  const effectiveDate = version => version.effectiveAt || String(version.summary || '').match(/Executed\/effective: (\d{4}-\d{2}-\d{2})/)?.[1] || version.date;
  const versionDate = (company, version) => company.id === 'B01' ? effectiveDate(version) : version.date;
  const eventDate = (company, event) => company.id === 'B01' ? event.eventDate || event.date : event.date;
  const shortDate = value => {
    const stamp = typeof value === 'number' ? value : time(value);
    return Number.isFinite(stamp) ? new Date(stamp).toLocaleDateString('en-US', {month:'short', day:'numeric', timeZone:'UTC'}) : 'Undated';
  };
  const date = value => value ? RC.date(value) : 'Not effective';
  const severity = status => ({weakened:1, contradicted:2, triggered:1, noncompliant:2}[status] || 0);

  function eventRecords(company, versions) {
    const previous = new Map();
    return [...list(company.events)].sort((a, b) => time(eventDate(company, a)) - time(eventDate(company, b))).map(event => {
      let detection = false;
      for (const finding of list(event.findings)) {
        const key = finding.assumptionId || finding.covenantId;
        if (severity(finding.status) > severity(previous.get(key))) detection = true;
        if (key && finding.status !== 'unassessed') previous.set(key, finding.status);
      }
      // Saved B01 review decisions also preserve detections about reporting duties.
      if (company.id === 'B01' && ['adopted', 'pending'].includes(event.decisionAction)) detection = true;
      const byVersion = versions.findIndex(version => version.version === event.packageVersion);
      const inferredLane = versions.reduce((lane, version, index) => time(versionDate(company, version)) <= time(eventDate(company, event)) ? index : lane, 0);
      return {event, detection, lane:byVersion >= 0 ? byVersion : inferredLane};
    });
  }

  function render(company, selectedEventId) {
    const allVersions = list(company.versions);
    const versions = allVersions.filter(version => !pending(version));
    if (!versions.length) return '<section class="ph-section"><div class="ph-empty"><h2>Package history</h2><p>No package versions are present in these saved records.</p></div></section>';
    const proposal = allVersions.find(pending);
    const current = versions.at(-1);
    const b01 = company.id === 'B01';
    const records = eventRecords(company, versions);
    const selected = records.find(record => record.event.id === selectedEventId);
    const eventPaths = new Map(records.map(record => [record.event.id, [versions[record.lane]?.id, ...allVersions.filter(version => version.triggerEventId === record.event.id).map(version => version.id)].filter(Boolean)]));
    const selectedPaths = new Set(eventPaths.get(selectedEventId) || []);
    const pathAttributes = (version, className) => `data-ph-path="${esc(version.id)}" class="${className}${selectedPaths.has(version.id) ? ' ph-path-selected' : ''}"`;
    const stamps = [time(company.asOf), ...versions.map(version => time(versionDate(company, version))), ...records.map(({event}) => time(eventDate(company, event)))].filter(Number.isFinite);
    const originalStart = Math.min(...stamps);
    const end = Math.max(...stamps);
    const full = fullHistory.has(company.id);
    const selectedTime = selected ? time(eventDate(company, selected.event)) : end;
    const firstEvent = Math.min(...records.map(({event}) => time(eventDate(company, event))).filter(Number.isFinite));
    const recentStart = b01 && Number.isFinite(firstEvent) ? firstEvent - 30 * day : Math.min(end - 120 * day, selectedTime - 15 * day);
    const start = full ? originalStart : Math.max(originalStart, recentStart);
    const span = Math.max(30 * day, end - start);
    const chartEnd = end + span * .13;
    const width = 850, left = 190, right = 816, top = 54, step = 64;
    const y = lane => top + lane * step;
    const laneCount = versions.length + (proposal ? 1 : 0);
    const axis = y(laneCount - 1) + 47;
    const height = axis + 36;
    const x = value => Math.max(left, Math.min(right, left + (time(value) - start) / (chartEnd - start) * (right - left)));
    const xp = stamp => left + (stamp - start) / (chartEnd - start) * (right - left);
    const visible = records.filter(({event}) => time(eventDate(company, event)) >= start);
    const ticks = Array.from({length:5}, (_, index) => start + (end - start) * index / 4);
    const svg = [`<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Package branches over time. Version and report controls follow the diagram.">`];
    ticks.forEach(stamp => {
      const xx = xp(stamp);
      svg.push(`<line x1="${xx}" y1="19" x2="${xx}" y2="${axis}" class="ph-grid-line"/><text x="${xx}" y="${axis + 25}" text-anchor="middle" class="ph-axis-label">${esc(span > 390 * day ? new Date(stamp).toLocaleDateString('en-US', {month:'short', year:'2-digit', timeZone:'UTC'}) : shortDate(stamp))}</text>`);
    });
    svg.push(`<line x1="${left}" y1="${axis}" x2="${right}" y2="${axis}" class="ph-axis-line"/>`);
    versions.forEach((version, index) => {
      const yy = y(index), xx = x(versionDate(company, version));
      const next = versions[index + 1];
      const stop = next ? x(versionDate(company, next)) : right;
      if (next) svg.push(`<path d="M ${stop} ${yy} H ${right}" class="ph-prior-line"/><text x="${right}" y="${yy - 12}" text-anchor="end" class="ph-prior-label">Prior terms</text>`);
      svg.push(`<path d="M ${xx} ${yy} H ${stop}" ${pathAttributes(version, 'ph-adopted-line')}/>`);
      if (index && time(versionDate(company, version)) >= start) svg.push(`<path d="M ${xx} ${y(index - 1)} V ${yy - 13} Q ${xx} ${yy} ${xx + 13} ${yy}" ${pathAttributes(version, 'ph-adopted-line')}/>`);
      svg.push(`<rect x="${xx - 3}" y="${yy - 3}" width="6" height="6" rx="1" class="ph-version-square"/>`);
      if (time(versionDate(company, version)) < start) svg.push(`<path d="M ${left + 6} ${yy - 4} L ${left + 2} ${yy} L ${left + 6} ${yy + 4}" class="ph-before-window"/>`);
    });
    if (proposal) {
      const origin = records.find(({event}) => event.id === proposal.triggerEventId) || records.find(({event}) => event.decisionAction === 'pending');
      const branchX = origin ? x(eventDate(company, origin.event)) : x(proposal.date);
      const fromLane = versions.findIndex(version => version.version === proposal.parentVersion);
      const fromY = y(fromLane < 0 ? versions.length - 1 : fromLane), toY = y(versions.length);
      const bend = Math.min(branchX + 22, right - 4);
      svg.push(`<path d="M ${branchX} ${fromY} C ${bend} ${fromY} ${branchX} ${toY} ${bend} ${toY} H ${right}" ${pathAttributes(proposal, 'ph-proposed-line')}/><text x="${right}" y="${toY - 12}" text-anchor="end" class="ph-proposed-label">Not adopted</text>`);
    }
    svg.push('</svg>');
    const versionButtons = allVersions.map((version, index) => {
      const proposed = pending(version), operative = version.id === current.id;
      const status = proposed ? 'Proposed' : index === 0 ? 'Original' : operative ? (b01 ? 'Operative' : 'Latest recorded') : (b01 ? 'Adopted' : 'Observed amendment');
      const subline = proposed ? 'Awaiting review · no effect' : `${b01 ? 'Effective' : 'Disclosed'} ${shortDate(versionDate(company, version))}${index === 0 ? ', ' + String(versionDate(company, version)).slice(0, 4) : ''}`;
      return `<button class="ph-version ${proposed ? 'ph-version-proposed' : ''} ${operative ? 'ph-version-current' : ''}" style="top:${y(index) / height * 100}%" data-ph-version="${esc(version.id)}" data-ph-paths="${esc(version.id)}" aria-label="View v${esc(version.version)}, ${esc(status)}, ${esc(version.title)}"><span class="ph-version-top"><b>v${esc(version.version)}</b><span>${esc(status)}</span></span><small>${esc(subline)}</small></button>`;
    }).join('');
    const eventButtons = visible.map(({event, detection, lane}) => {
      const isSelected = event.id === selectedEventId;
      const isPending = b01 && event.decisionAction === 'pending';
      const stamp = eventDate(company, event), yy = detection ? y(lane) : axis;
      const index = records.findIndex(record => record.event.id === event.id) + 1;
      const label = isPending ? 'Awaiting review' : detection ? 'Recorded detection' : 'Report, no new detection';
      return `<button class="ph-event ${detection ? 'ph-detection' : 'ph-report'} ${isPending ? 'ph-event-pending' : ''} ${isSelected ? 'ph-event-selected' : ''}" style="left:${x(stamp) / width * 100}%;top:${yy / height * 100}%" data-ph-event="${esc(event.id)}" data-ph-paths="${esc(eventPaths.get(event.id).join(' '))}" aria-pressed="${isSelected}" aria-label="${esc(event.title)}, ${esc(date(stamp))}. ${label}." title="${esc(event.title)} · ${esc(date(stamp))}">${detection ? `<span class="ph-node-mark">${String(index).padStart(2, '0')}</span>` : '<span class="ph-node-mark ph-tick"></span>'}<span class="ph-node-caption">${detection ? esc(isPending ? 'Review required' : 'Detection ' + index) : ''}</span></button>`;
    }).join('');
    const amendments = Math.max(0, versions.length - 1);
    return `<section class="ph-section" aria-label="Package history">
      <header class="ph-header"><div><span class="ph-eyebrow">The terms over time</span><h2>Package history</h2><p>${b01 ? 'Every revision, and the evidence behind it.' : 'Publicly disclosed amendments and recorded investigations.'}</p></div><div class="ph-controls"><span class="ph-count">${amendments} ${b01 ? 'adopted' : 'observed'} amendment${amendments === 1 ? '' : 's'}</span><button class="ph-range" data-ph-range aria-pressed="${full}">${full ? 'Recent history' : 'Full history'}<span aria-hidden="true">↔</span></button></div></header>
      <div class="ph-window"><span>${full ? 'Full history' : 'Review window'} · ${esc(date(new Date(start).toISOString().slice(0, 10)))} – ${esc(date(company.asOf || new Date(end).toISOString().slice(0, 10)))}</span><strong>${b01 ? 'Operative' : 'Latest recorded'} v${esc(current.version)}${proposal ? ' <i>·</i> <em>v' + esc(proposal.version) + ' proposed</em>' : ''}</strong></div>
      <div class="ph-scroll" tabindex="0" aria-label="Scrollable package branch diagram"><div class="ph-diagram" style="aspect-ratio:${width}/${height}">${svg.join('')}${versionButtons}${eventButtons}</div></div>
      <div class="ph-legend" aria-label="Diagram legend"><span><i class="ph-key-line"></i>${b01 ? 'Adopted history' : 'Recorded versions'}</span><span><i class="ph-key-line ph-key-prior"></i>Prior continuation</span>${proposal ? '<span><i class="ph-key-line ph-key-proposed"></i>Proposed revision</span><span><i class="ph-key-pending"></i>Awaiting review</span>' : ''}<span><i class="ph-key-report"></i>Report, no new detection</span></div>
      <p class="ph-note">Time runs left to right. Lanes identify versions; height does not represent rates or credit quality. ${b01 ? 'Version dates are effective dates; report markers use event dates.' : 'Dates show public availability. Amendments are observed records, not decisions made in this dashboard.'}${records.length > visible.length ? ` ${records.length - visible.length} earlier report${records.length - visible.length === 1 ? '' : 's'} in full history.` : ''}</p>
      ${selected ? `<div class="ph-selection"><span><small>Selected report · ${esc(date(eventDate(company, selected.event)))}</small><strong>${esc(selected.event.title)}</strong></span><button data-ph-inspect="${esc(selected.event.id)}">Read report <span aria-hidden="true">↗</span></button></div>` : ''}
    </section>`;
  }

  function changeHTML(change, previousVersion, version) {
    const text = String(change);
    const beforeIndex = text.indexOf('\n\nBefore: '), afterIndex = text.indexOf('\n\nAfter: ');
    if (beforeIndex < 0 || afterIndex < 0) return `<article class="ph-recorded-change">${esc(text)}</article>`;
    return `<article class="ph-change"><h3>${esc(text.slice(0, beforeIndex))}</h3><div class="ph-compare"><section><h4>Before · v${esc(previousVersion || '—')}</h4><p>${esc(text.slice(beforeIndex + 10, afterIndex))}</p></section><section><h4>${pending(version) ? 'Proposed' : 'After'} · v${esc(version.version)}</h4><p>${esc(text.slice(afterIndex + 9))}</p></section></div></article>`;
  }

  function showVersion(company, id) {
    const version = list(company.versions).find(item => item.id === id);
    if (!version) return;
    const versions = list(company.versions), index = versions.indexOf(version);
    const parent = version.parentVersion || versions[index - 1]?.version;
    const isPending = pending(version), original = index === 0;
    const current = versions.filter(item => !pending(item)).at(-1);
    const clauses = list(version.clauses).length ? version.clauses : original ? company.covenants : [];
    const changes = list(version.changes);
    const statusText = isPending ? `This draft has not been adopted. v${current.version} remains operative. No effective date is recorded.` : `${company.id === 'B01' ? 'Effective' : 'Recorded execution / effective date'}: ${date(effectiveDate(version))}.${version.date !== effectiveDate(version) ? ` ${company.id === 'B01' ? 'Decision' : 'Public disclosure'}: ${date(version.date)}.` : ''}`;
    RC.modal(`v${version.version} · ${version.title}`, `${company.name} · ${isPending ? 'Proposed · not operative' : original ? 'Original package' : company.id === 'B01' ? 'Recorded adopted amendment' : 'Observed historical amendment'}`,
      `<div class="ph-modal-status ${isPending ? 'ph-modal-pending' : ''}">${esc(statusText)}</div>
      <p class="ph-modal-summary">${esc(version.summary)}</p>
      ${changes.length ? `<section class="ph-modal-changes"><h3>${company.id === 'B01' ? 'Full recorded clause changes' : 'Amendment disclosure'}</h3>${changes.map(change => changeHTML(change, parent, version)).join('')}</section>` : '<p class="ph-modal-summary">This is the original package; it contains no amendment changes.</p>'}
      ${clauses.length ? `<details class="ph-clause-details" ${original ? 'open' : ''}><summary>${original ? 'Original package provisions' : 'Recorded provisions in this version'} (${clauses.length})</summary>${clauses.map(clause => `<article class="ph-recorded-change"><h3>${esc(clause.id)} · ${esc(clause.title)}</h3><p>${esc(clause.text)}</p></article>`).join('')}</details>` : ''}
      <p class="ph-modal-foot">${company.id === 'B01' ? 'Fictional borrower and authored amendment scenario. Recorded model findings are separate from the saved review decision.' : 'These are historical public disclosures. The lender’s private reasoning is not recorded here, and an observed response is not a recommendation.'}</p>`);
  }

  function compare(company, fromId, toId) {
    const versions = list(company.versions);
    const before = versions.find(version => version.id === fromId || version.version === fromId) || versions[0];
    const after = versions.find(version => version.id === toId || version.version === toId) || versions.filter(version => !pending(version)).at(-1);
    if (!before || !after) return;
    if (company.id !== 'B01') {
      const start = versions.indexOf(before), finish = versions.indexOf(after);
      RC.modal(`v${before.version} to v${after.version}`, 'Observed public amendment disclosures', `<p class="ph-modal-summary">These disclosures describe the recorded lender responses between the selected versions. They are not complete restated loan agreements.</p>${versions.slice(start + 1, finish + 1).map(version => `<section class="ph-modal-changes"><h3>v${esc(version.version)} · ${esc(version.title)}</h3>${list(version.changes).map(change => changeHTML(change, before.version, version)).join('')}</section>`).join('') || '<p>No amendments between these versions.</p>'}`);
      return;
    }
    const prior = new Map(list(before.clauses).map(clause => [clause.id, clause]));
    const next = new Map(list(after.clauses).map(clause => [clause.id, clause]));
    const clauseIds = [...new Set([...prior.keys(), ...next.keys()])];
    const changes = clauseIds.filter(id => prior.get(id)?.text !== next.get(id)?.text).map(id => `${id} · ${next.get(id)?.title || prior.get(id)?.title || ''}\n\nBefore: ${prior.get(id)?.text || 'Not included'}\n\nAfter: ${next.get(id)?.text || 'Removed'}`);
    // A draft may carry only its proposed changes, rather than a complete clause snapshot.
    const comparison = list(after.clauses).length ? changes : list(after.changes);
    RC.modal(`v${before.version} → v${after.version} · Package comparison`, `${company.name} · ${pending(after) ? 'Proposed changes' : 'Cumulative adopted changes'}`,
      `<div class="ph-modal-status ${pending(after) ? 'ph-modal-pending' : ''}">${pending(after) ? 'This proposal is not operative. The adopted package remains unchanged.' : `Original baseline: ${esc(date(effectiveDate(before)))}. Compared version effective: ${esc(date(effectiveDate(after)))}.`}</div><p class="ph-modal-summary">Every changed provision below is shown in full. ${pending(after) ? 'Before is the recorded parent package.' : 'Unchanged provisions retain their prior text.'}</p>${comparison.map(change => changeHTML(change, before.version, after)).join('') || '<p class="ph-modal-summary">No clause changes between these versions.</p>'}`);
  }

  function mount(container, company, selectedEventId) {
    if (!container) return;
    const paths = [...container.querySelectorAll('[data-ph-path]')];
    let hoveredControl = null, focusedControl = null;
    const emphasizePaths = () => {
      const related = new Set((hoveredControl || focusedControl)?.dataset.phPaths.split(' ') || []);
      paths.forEach(path => path.classList.toggle('ph-path-emphasis', related.has(path.dataset.phPath)));
    };
    container.querySelectorAll('[data-ph-paths]').forEach(button => {
      button.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') { hoveredControl = button; emphasizePaths(); } });
      button.addEventListener('pointerleave', event => { if (event.pointerType !== 'touch') { hoveredControl = null; emphasizePaths(); } });
      button.addEventListener('focus', () => { focusedControl = button; emphasizePaths(); });
      button.addEventListener('blur', () => { focusedControl = null; emphasizePaths(); });
    });
    const scroller = container.querySelector('.ph-scroll');
    if (scroller && scroller.scrollWidth > scroller.clientWidth + 2) {
      const selected = [...container.querySelectorAll('[data-ph-event]')].find(button => button.dataset.phEvent === selectedEventId);
      if (selected) scroller.scrollLeft = Math.max(0, selected.offsetLeft - scroller.clientWidth / 2);
      const hint = document.createElement('span');
      hint.className = 'ph-mobile-guide';
      hint.textContent = 'Swipe the diagram to explore the full history';
      container.querySelector('.ph-window')?.append(hint);
    }
    container.querySelectorAll('[data-ph-event]').forEach(button => button.addEventListener('click', event => {
      const id = button.dataset.phEvent, owner = button.ownerDocument;
      RC.setEvent(id);
      if (event.detail === 0) [...owner.querySelectorAll('.ph-section [data-ph-event]')].find(replacement => replacement.dataset.phEvent === id)?.focus({preventScroll:true});
    }));
    container.querySelectorAll('[data-ph-inspect]').forEach(button => button.addEventListener('click', () => RC.showEvent(button.dataset.phInspect)));
    container.querySelectorAll('[data-ph-version]').forEach(button => button.addEventListener('click', () => showVersion(company, button.dataset.phVersion)));
    container.querySelector('[data-ph-range]')?.addEventListener('click', () => {
      fullHistory.has(company.id) ? fullHistory.delete(company.id) : fullHistory.add(company.id);
      container.innerHTML = render(company, selectedEventId);
      mount(container, company, selectedEventId);
      container.querySelector('[data-ph-range]')?.focus();
    });
  }
  window.PackageHistory = {render, mount, openVersion:showVersion, compare};
})();
