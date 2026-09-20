// Read-only regression for the canvas-first live demo. No write request reaches
// the server: save/adoption/ingestion endpoints are deliberately never exercised.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');

const base = process.env.REALITYCHECK_URL || 'http://127.0.0.1:8013';
const savedRecords = ({ feed, ...snapshot }) => JSON.stringify(snapshot);
const byAvailable = events => events.map((event, index) => ({ event, index }))
  .sort((a, b) => String(a.event.available_at).localeCompare(String(b.event.available_at)) || a.index - b.index)
  .map(row => row.event);

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1536, height: 1080 } });
  const page = await context.newPage();
  const errors = [], attemptedWrites = [];
  page.on('pageerror', error => errors.push(error.message));
  await context.route('**/*', route => {
    const request = route.request();
    if (['GET', 'HEAD'].includes(request.method())) return route.continue();
    attemptedWrites.push(`${request.method()} ${request.url()}`);
    return route.abort('blockedbyclient');
  });
  async function snapshot(cid) {
    const response = await context.request.get(`${base}/api/${cid}`);
    assert(response.ok(), `GET ${cid}: ${response.status()}`);
    return response.json();
  }
  const beforeH01 = await snapshot('h01'), beforeB01 = await snapshot('b01');
  const reports = byAvailable(beforeH01.events);
  const inspector = page.locator('#inspector-toggle');
  const detail = page.locator('#event-detail');
  const panelToggle = page.locator('#workspace-controls-toggle');
  async function settlePanel() {
    await page.evaluate(() => Promise.allSettled(['right-controls', 'connected-evidence', 'workspace-controls-toggle']
      .flatMap(id => document.getElementById(id).getAnimations()).map(animation => animation.finished)));
  }
  async function setPanel(open) {
    if ((await panelToggle.getAttribute('aria-expanded')) !== String(open)) await panelToggle.click();
    await settlePanel();
    assert.equal(await page.locator('#right-controls').isVisible(), open);
    assert.equal(await page.locator('#right-controls').evaluate(el => el.inert), !open);
  }
  const eventMarker = id => page.locator(`#chart [data-event="${id}"]`);

  async function load(cid) {
    await page.goto(`${base}/${cid}`);
    await page.waitForFunction(id => typeof state !== 'undefined' && state?.ready && state.borrower.id === id &&
      typeof cgGraph !== 'undefined' && cgGraph?.model, cid.toUpperCase());
    await page.locator('#workspace-stage').waitFor({ state: 'visible' });
    await page.locator('#connected-evidence .cg-node').first().waitFor({ state: 'visible' });
  }
  async function closeDialog() {
    await page.keyboard.press('Escape');
    await page.locator('#modal-root [role="dialog"]').waitFor({ state: 'detached' });
  }
  async function setInspector(open) {
    if ((await inspector.getAttribute('aria-expanded')) !== String(open)) await inspector.click();
    await page.waitForFunction(expected => document.querySelector('#inspector-toggle').getAttribute('aria-expanded') === String(expected), open);
    assert.equal(await detail.isVisible(), open, 'Inspector content follows the disclosure state');
  }
  async function assertNoOverflow(width) {
    await page.setViewportSize({ width, height: width === 390 ? 844 : 1080 });
    await page.waitForFunction(() => document.fonts.status === 'loaded');
    const bounds = await page.evaluate(() => ({ width: document.documentElement.clientWidth, scroll: document.documentElement.scrollWidth }));
    assert(bounds.scroll <= bounds.width + 2, `No document overflow at ${width}px: ${JSON.stringify(bounds)}`);
  }
  async function assertDotsOnly() {
    assert.equal(await page.locator('.cg-node-title:visible,.cg-node-label:visible,.cg-node-id:visible').count(), 0, 'Graph labels remain hidden until discovery');
    const nodes = await page.locator('#connected-evidence .cg-node').evaluateAll(els => els.map(el => ({
      text: el.innerText.trim(), name: el.getAttribute('aria-label'),
    })));
    assert(nodes.length > 0, 'Evidence canvas contains records');
    assert(nodes.every(node => !node.text && node.name?.trim()), 'Every dot is visually quiet and has an accessible name');
  }
  async function assertTooltip(node, focus = false) {
    if (focus) {
      await page.mouse.move(2, 2);
      await page.keyboard.press('Tab');
      await node.focus();
    } else await node.hover();
    const tip = page.locator('.cg-tooltip:visible');
    await tip.waitFor({ state: 'visible' });
    const text = await tip.innerText();
    assert(text.trim().length > 12, 'Floating tooltip provides a record summary');
    const bounds = await tip.boundingBox(), viewport = page.viewportSize();
    assert(bounds && bounds.x >= -1 && bounds.y >= -1 && bounds.x + bounds.width <= viewport.width + 1 && bounds.y + bounds.height <= viewport.height + 1,
      `Tooltip stays within viewport: ${JSON.stringify({ bounds, viewport })}`);
    const key = await node.getAttribute('data-cg-node');
    assert.equal(await node.evaluate(el => el.classList.contains('cg-preview')), true, 'Hover/focus previews the dot');
    const incident = await page.locator('.cg-link.cg-preview').evaluateAll((links, key) => links.every(link => link.dataset.cgFrom === key || link.dataset.cgTo === key), key);
    assert(incident, 'Preview highlights only incident connections');
  }
  async function assertReplay(count) {
    const visible = reports.slice(0, count), future = reports.slice(count), ids = visible.map(e => e.id);
    await page.waitForFunction(n => state.events.length === n, count);
    const actual = await page.evaluate(() => ({ ids: state.events.map(e => e.id), version: state.current_version,
      versions: state.versions.map(v => v.version), proposal: state.pending_proposal?.trigger_event_id || null,
      selected: selectedEventId, graphReview: cgGraph?.model.review?.id || null,
    }));
    const versions = beforeH01.versions.filter((v, i) => i === 0 || visible.some(e => e.decision?.version === v.version));
    assert.deepEqual(actual.ids.slice().sort(), ids.slice().sort());
    assert.equal(actual.version, versions.at(-1).version);
    assert.deepEqual(actual.versions, versions.map(v => v.version));
    assert.equal(actual.selected, visible.at(-1)?.id || null);
    assert.equal(actual.graphReview, visible.at(-1)?.id || null, 'Canvas follows replay selection');
    if (count === 0) {
      assert.deepEqual((await page.locator('.cg-source[data-cg-node]').evaluateAll(nodes => nodes.map(n => n.dataset.cgNode))).sort(),
        ['source:CROX-10K-FY2025', 'source:underwriting-memo.md'], 'Origination shows only the memo and 10-K');
    }
    assert.equal(actual.proposal, ids.includes(beforeH01.pending_proposal?.trigger_event_id) ? beforeH01.pending_proposal.trigger_event_id : null);
    const graphText = await page.locator('#connected-evidence').evaluate(el => el.textContent + '\n' +
      [...el.querySelectorAll('*')].flatMap(node => [...node.attributes].map(a => a.value)).join('\n'));
    const shownDocs = new Set(visible.flatMap(e => e.sources.map(source => source.document_id)));
    const baselineDocs = new Set(beforeH01.profile.assumptions.flatMap(a => (a.evidence || []).map(q => q.document_id)));
    for (const event of future) {
      assert(!graphText.includes(event.id), `Future ${event.id} is absent from graph`);
      assert(!graphText.includes(event.title), `Future event title is absent from graph at step ${count}`);
      for (const source of event.sources) if (!shownDocs.has(source.document_id) && !baselineDocs.has(source.document_id)) {
        assert(!graphText.includes(source.document_id), `Future source ${source.document_id} is absent at step ${count}`);
      }
    }
    assert.deepEqual((await page.locator('#chart [data-event]').evaluateAll(nodes => nodes.map(n => n.dataset.event))).sort(), ids.slice().sort());
    if (beforeH01.pending_proposal && !ids.includes(beforeH01.pending_proposal.trigger_event_id)) {
      assert(!(await page.locator('#chart').innerText()).includes('v' + beforeH01.pending_proposal.version), 'Proposal stays hidden until its trigger report');
    }
    if (count < reports.length) {
      assert.equal(await page.locator('#library').isVisible(), false, 'Future incoming reports stay hidden during replay');
    }
  }

  try {
    assert.equal(beforeH01.ready, true);
    assert(beforeH01.versions.some(version => version.version === beforeH01.current_version));
    assert(reports.length > 0, 'Recorded reports are available for replay');
    await load('h01');
    assert.equal(await page.locator('.rail:visible,.topbar:visible').count(), 0, 'Navigation rail and upper header are removed');
    assert.equal(await inspector.getAttribute('aria-expanded'), 'false', 'Detail inspector starts collapsed');
    assert.equal(await detail.isVisible(), false);
    assert.equal(await panelToggle.count(), 1, 'An edge button opens the shared history and details panel');
    assert.equal(await panelToggle.getAttribute('aria-expanded'), 'false', 'The shared panel starts closed');
    await setPanel(false);
    const canvasBox = await page.locator('#connected-evidence').boundingBox();
    assert(canvasBox.y < 300 && canvasBox.height > 360, 'Evidence canvas is the first-view main content');
    assert(canvasBox.width > 1450, 'Collapsed panel leaves the full desktop canvas available');
    await panelToggle.focus();
    await page.keyboard.press('Enter');
    await settlePanel();
    const historyBox = await page.locator('#history').boundingBox();
    assert(historyBox.x > canvasBox.x, 'History slides into the right side');
    assert((await page.locator('#connected-evidence').boundingBox()).width < canvasBox.width - 250, 'Open panel reserves its desktop space');
    await page.locator('#compare-button').focus();
    await page.keyboard.press('Escape');
    await settlePanel();
    assert.equal(await page.evaluate(() => document.activeElement.id), 'workspace-controls-toggle', 'Closing from inside restores focus to the edge button');
    assert(await page.locator('#source-library').evaluate(el => Boolean(document.querySelector('#drift').compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)),
      'The source library follows drift analysis in document order');
    await assertDotsOnly();
    await page.screenshot({ path: path.join(__dirname, 'workspace-progressive-desktop.png'), fullPage: true });
    const initialZoom = await page.evaluate(() => cgZoom);
    await page.locator('.cg-viewport').hover({ position: { x: 30, y: 100 } });
    await page.mouse.wheel(0, 500);
    await page.waitForFunction(() => window.scrollY > 200);
    assert.equal(await page.evaluate(() => cgZoom), initialZoom, 'Ordinary scrolling reaches content below without zooming the network');
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));

    // Both mouse discovery and keyboard discovery expose useful bounded summaries.
    const first = page.locator('.cg-node').first(), last = page.locator('.cg-node').last();
    await assertTooltip(first);
    await assertTooltip(last);
    await assertTooltip(first, true);
    const key = await first.getAttribute('data-cg-node');
    await page.keyboard.press('Enter');
    await settlePanel();
    assert.equal(await panelToggle.getAttribute('aria-expanded'), 'true', 'A deliberate dot selection reveals its details panel');
    await page.waitForFunction(() => document.querySelector('#inspector-toggle').getAttribute('aria-expanded') === 'true');
    assert.equal(await detail.isVisible(), true, 'Activating a dot opens its details');
    assert.equal(await page.evaluate(() => cgSelection), key);
    assert.equal(await page.evaluate(() => document.activeElement.dataset.cgNode), key, 'Keyboard dot activation retains focus');
    const selectedContext = await page.evaluate(() => ({ selection: cgSelection, event: selectedEventId, scope: cgScope, zoom: cgZoom, pan: cgPan }));
    const inspectorText = await detail.innerText();
    await setPanel(false);
    await page.evaluate(() => refresh(true));
    assert.equal(await panelToggle.getAttribute('aria-expanded'), 'false', 'Refresh does not reopen the collapsed panel');
    assert.deepEqual(await page.evaluate(() => ({ selection: cgSelection, event: selectedEventId, scope: cgScope, zoom: cgZoom, pan: cgPan })), selectedContext);
    await setPanel(true);
    assert.equal(await detail.innerText(), inspectorText, 'Drawer reopening restores the selected record');
    await setInspector(false);
    await page.evaluate(() => renderConnections());
    assert.equal(await inspector.getAttribute('aria-expanded'), 'false', 'Refreshing the canvas preserves collapsed inspector');
    assert.deepEqual(await page.evaluate(() => ({ selection: cgSelection, event: selectedEventId, scope: cgScope, zoom: cgZoom, pan: cgPan })), selectedContext,
      'Collapsing details retains selection, review, scope and pan/zoom');
    await setInspector(true);
    assert.equal(await detail.innerText(), inspectorText, 'Reopening details restores the selected record');
    await page.locator('#event-detail [data-cg-open]').click();
    await page.locator('#modal-root [role="dialog"]').waitFor();
    await closeDialog();
    assert.equal(await panelToggle.getAttribute('aria-expanded'), 'true', 'Escape closes the record dialog without closing its parent panel');
    await setInspector(false);

    for (const event of reports) {
      await eventMarker(event.id).click();
      const graph = await page.evaluate(() => ({ selected: selectedEventId, scope: cgScope, review: cgGraph.model.review?.id, version: cgGraph.model.version?.version }));
      assert.deepEqual(graph, { selected: event.id, scope: 'review', review: event.id, version: event.package_version }, 'History control scopes canvas to the corresponding agreement and report');
      assert.equal(await eventMarker(event.id).getAttribute('aria-pressed'), 'true');
      await assertDotsOnly();
    }

    // Keep original forms available; test invalid dates locally then cancel.
    await page.locator('#add-event').click();
    await page.locator('#event-form').waitFor();
    await page.locator('#event-title').fill('Read-only validation check — not saved');
    await page.locator('#event-text').fill('This verifies date validation only. No record is submitted.');
    await page.locator('#event-date').fill('2027-04-20');
    await page.locator('#available-date').fill('2027-04-20');
    await page.locator('#review-date').fill('2027-04-19');
    await page.locator('#submit-event').click();
    assert((await page.locator('#form-error').innerText()).includes('on or after'));
    await closeDialog();
    await page.locator('#compare-button').click();
    const comparison = await page.locator('#modal-root [role="dialog"]').innerText();
    assert(comparison.includes('v' + beforeH01.versions[0].version) && comparison.includes('v' + beforeH01.current_version));
    await closeDialog();
    if (beforeH01.pending_proposal) {
    await eventMarker(beforeH01.pending_proposal.trigger_event_id).click();
    await setInspector(true);
    await page.locator(`#event-detail [data-review="${beforeH01.pending_proposal.trigger_event_id}"]`).click();
    await page.locator('#decision-form').waitFor();
    assert.equal(await page.locator('#decision-form input[name="action"]').count(), 2);
    assert((await page.locator('#modal-root [role="dialog"]').innerText()).includes('v' + beforeH01.pending_proposal.version));
    await closeDialog();
    }
    await setInspector(false);

    await page.locator('#replay-reset').click();
    await assertReplay(0);
    for (let count = 1; count <= reports.length; count++) {
      await page.locator('#replay-next').click();
      await assertReplay(count);
    }
    await page.locator('#replay-reset').click();
    await page.locator('#replay-all').click();
    await assertReplay(reports.length);
    await page.locator('#saved-sources [data-source-record]').first().click();
    assert(await page.locator('#modal-root .source-text').count() > 0, 'Bottom source library still opens saved passages');
    await closeDialog();

    for (const width of [1536, 1280, 900, 390]) {
      await assertNoOverflow(width);
      await assertDotsOnly();
    }
    await load('h01');
    await assertNoOverflow(390);
    assert.equal(await inspector.getAttribute('aria-expanded'), 'false', 'Fresh mobile starts collapsed');
    await assertTooltip(page.locator('.cg-node').last());
    await page.locator('.cg-node').first().click();
    assert.equal(await inspector.getAttribute('aria-expanded'), 'true', 'Mobile dot selection exposes details');
    await setInspector(false);
    await page.screenshot({ path: path.join(__dirname, 'workspace-progressive-mobile.png'), fullPage: true });
    await page.emulateMedia({ reducedMotion: 'reduce' });
    assert.equal(await page.locator('.cg-mark').first().evaluate(el => getComputedStyle(el).transitionDuration), '0s');

    await page.setViewportSize({ width: 1536, height: 1080 });
    await load('b01');
    assert.equal(await page.evaluate(() => state.current_version), beforeB01.current_version);
    assert.equal(await page.locator('#chart [data-event]').count(), beforeB01.events.length);
    await assertDotsOnly();
    assert.deepEqual(attemptedWrites, [], 'No write requests were attempted');
    assert.deepEqual(errors, [], 'No browser runtime errors');
    assert.equal(savedRecords(await snapshot('h01')), savedRecords(beforeH01), 'H01 saved records remain unchanged');
    assert.equal(savedRecords(await snapshot('b01')), savedRecords(beforeB01), 'B01 saved records remain unchanged');
    console.log('Progressive workspace passed: canvas-first layout, dot discovery, inspector context, history-scoped graph, replay isolation, forms, source access, responsive layouts, no browser errors or writes.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
