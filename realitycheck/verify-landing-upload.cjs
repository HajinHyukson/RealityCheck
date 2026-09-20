// Browser boundary checks: every API request is intercepted. No records or model calls are created.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const base = process.env.REALITYCHECK_URL || 'http://127.0.0.1:8013';
const initial = { id: 'B01', ready: true, status: 'ready', borrower: { id: 'B01', name: 'FluxRail Workflow, Inc.', sector: 'Workflow orchestration software' }, current_version: '1.2', events: 3, pending: 1, assumptions: 6, exposed: 2, latest: { title: 'Operational update', available_at: '2027-09-10' } };
const uploaded = { id: 'U0123456789ab', ready: false, status: 'queued', stage: 'Queued for analysis', borrower: { id: 'U0123456789ab', name: 'Ridgeline Components', label: 'Uploaded agreement', source_mode: 'uploaded_agreement' } };
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();
    const errors = [], writes = [];
    page.on('pageerror', error => errors.push(error.message));
    let rows = [initial], offline = false, uploadError = false;
    await context.route('**/api/**', async route => {
      const req = route.request(), url = new URL(req.url());
      if (req.method() === 'GET' && url.pathname === '/api/companies') {
        if (offline) return route.abort('failed');
        return route.fulfill({ json: { companies: rows } });
      }
      writes.push({ method: req.method(), path: url.pathname, body: req.postDataJSON() });
      if (req.method() === 'POST' && url.pathname === '/api/companies') {
        if (uploadError) return route.fulfill({ status: 503, json: { error: 'Upload service unavailable. Please retry.' } });
        rows = [initial, { ...uploaded }];
        return route.fulfill({ status: 202, json: uploaded });
      }
      if (req.method() === 'POST' && url.pathname === '/api/companies/U0123456789ab/retry') {
        rows = [initial, { ...uploaded }];
        return route.fulfill({ status: 202, json: uploaded });
      }
      return route.abort('blockedbyclient');
    });
    await page.goto(`${base}/companies`);
    await page.getByRole('heading', { name: 'Add New Credit Agreement', exact: true }).waitFor({ timeout: 3000 });
    const original = page.locator('[data-company-id="B01"]');
    await original.locator('a[href="/b01"]').waitFor();
    await original.evaluate(el => { el.dataset.retained = 'yes'; });
    await page.getByLabel('Company name').fill('Ridgeline Components');
    await page.locator('#agreement-files').setInputFiles([
      { name: 'agreement.txt', mimeType: 'text/plain', buffer: Buffer.from('Credit agreement text') },
      { name: 'appendix.md', mimeType: 'text/markdown', buffer: Buffer.from('Supporting evidence') },
    ]);
    await page.getByLabel('Document type for appendix.md', { exact: true }).selectOption('memo');
    await page.locator('#agreement-files').setInputFiles({ name: 'annual_10-k.txt', mimeType: 'text/plain', buffer: Buffer.from('Annual filing') });
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 3, 'Picking another batch adds to existing documents');
    assert.equal(await page.getByLabel('Document type for appendix.md', { exact: true }).inputValue(), 'memo', 'Adding files preserves edited document roles');
    assert.equal(await page.getByLabel('Document type for annual_10-k.txt', { exact: true }).inputValue(), '10k');
    assert.equal(await page.getByText('Add more files', { exact: true }).count(), 1);
    // The browser reports the identical File object on a repeated selection.
    await page.locator('#agreement-files').evaluate(el => { const chosen = new DataTransfer(); chosen.items.add(el.files[1]); el.files = chosen.files; el.dispatchEvent(new Event('change', { bubbles: true })); });
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 3, 'An identical file is not added twice');
    await page.locator('#agreement-files').dispatchEvent('cancel');
    await page.locator('#agreement-files').setInputFiles([]);
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 3, 'Canceled or empty selection preserves earlier documents');
    await page.getByRole('button', { name: 'Delete agreement.txt', exact: true }).click();
    assert.equal(await page.getByRole('button', { name: 'Delete appendix.md', exact: true }).evaluate(el => document.activeElement === el), true, 'Deletion focuses the next remaining document');
    assert.equal(await page.getByLabel('Document type for appendix.md', { exact: true }).inputValue(), 'memo', 'Deleting another file preserves edited roles');
    await page.locator('#agreement-files').setInputFiles({ name: 'agreement.txt', mimeType: 'text/plain', buffer: Buffer.from('Credit agreement text') });
    await page.getByRole('button', { name: 'Upload & analyze', exact: true }).click();
    const card = page.locator('[data-company-id="U0123456789ab"]');
    await card.waitFor();
    assert.equal(await card.locator('h3').innerText(), 'Ridgeline Components', 'Uploaded card uses the company name');
    assert.equal(await card.locator('a').count(), 0, 'Queued company cannot navigate');
    assert.equal(await card.getAttribute('aria-busy'), 'true');
    assert.equal(writes[0].body.name, 'Ridgeline Components');
    assert.deepEqual(writes[0].body.files.map(f => [f.filename, f.role, Buffer.from(f.b64, 'base64').toString()]), [['appendix.md', 'memo', 'Supporting evidence'], ['annual_10-k.txt', '10k', 'Annual filing'], ['agreement.txt', 'agreement', 'Credit agreement text']]);
    assert.equal(await original.getAttribute('data-retained'), 'yes', 'Existing card is retained after upload');
    await original.locator('a').focus();
    rows = [{ ...initial, pending: 2 }, { ...uploaded, status: 'processing', stage: 'Extracting agreement terms' }];
    await card.getByText('Extracting agreement terms', { exact: true }).waitFor({ timeout: 6000 });
    assert.equal(await original.locator('a').evaluate(el => document.activeElement === el), true, 'Polling preserves focus on existing company');
    const shots = path.join(__dirname, '..', 'tmp'); fs.mkdirSync(shots, { recursive: true });
    await page.screenshot({ path: path.join(shots, 'agreement-landing-desktop.png'), fullPage: true });
    rows = [initial, { ...uploaded, ready: true, status: 'ready', current_version: '1.0', events: 0, assumptions: 4, exposed: 0, pending: 0 }];
    await card.locator('a[href="/u0123456789ab"]').waitFor({ timeout: 6000 });
    assert.equal(await card.getAttribute('aria-busy'), 'false');
    assert.equal(await card.locator('.facts').count(), 1, 'Completed upload has the regular agreement card');

    // A persisted failure is visible after reload and retries the same company.
    rows = [initial, { ...uploaded, status: 'failed', error: 'Document extraction failed. Try again.' }];
    await page.reload();
    await card.getByText('Document extraction failed. Try again.', { exact: true }).waitFor();
    await card.getByRole('button', { name: 'Retry analysis' }).click();
    await card.getByText('Queued', { exact: true }).waitFor();
    assert.equal(writes.at(-1).path, '/api/companies/U0123456789ab/retry');
    offline = true;
    await page.locator('#load-error').waitFor({ state: 'visible', timeout: 6000 });
    assert.equal(await original.count(), 1, 'Refresh failure retains existing cards');
    assert.equal(await card.locator('a').count(), 0, 'Network failure does not unlock processing card');
    offline = false;
    await page.getByRole('button', { name: 'Retry refresh' }).click();
    await page.locator('#load-error').waitFor({ state: 'hidden' });

    // An unsuccessful upload keeps the input and files so the user can retry.
    uploadError = true;
    await page.getByLabel('Company name').fill('Ridgeline Components');
    await page.locator('#agreement-files').setInputFiles({ name: 'agreement.txt', mimeType: 'text/plain', buffer: Buffer.from('Original agreement') });
    await page.getByLabel('Document type for agreement.txt', { exact: true }).selectOption('memo');
    await page.getByRole('button', { name: 'Upload & analyze', exact: true }).click();
    await page.locator('#upload-error').getByText('Upload service unavailable. Please retry.', { exact: true }).waitFor();
    assert.equal(await page.getByLabel('Company name').inputValue(), 'Ridgeline Components');
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 1);
    assert.equal(await page.getByLabel('Document type for agreement.txt', { exact: true }).inputValue(), 'memo', 'Failed submit preserves document roles');
    const postCount = writes.length;
    await page.locator('#agreement-files').setInputFiles({ name: 'script.exe', mimeType: 'application/octet-stream', buffer: Buffer.from('unsupported') });
    await page.locator('#upload-error').getByText('Files were not added. Unsupported file: script.exe. Choose a PDF, image, TXT or Markdown file. Your previous selection is unchanged.', { exact: true }).waitFor({ timeout: 3000 });
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 1, 'Unsupported new batch leaves prior files intact');
    assert.equal(await page.getByLabel('Document type for agreement.txt', { exact: true }).inputValue(), 'memo', 'Rejected addition preserves edited roles');
    assert.equal(writes.length, postCount, 'Unsupported files never leave the browser');
    await page.getByRole('button', { name: 'Delete agreement.txt', exact: true }).click();
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 0, 'All selected files can be removed');
    assert.equal(await page.locator('#agreement-files').evaluate(el => document.activeElement === el), true, 'Removing the last file returns focus to the picker');
    assert.equal(await page.getByText('Add files', { exact: true }).count(), 1);
    await page.locator('#agreement-files').setInputFiles(Array.from({ length: 6 }, (_, i) => ({ name: `memo-${i}.txt`, mimeType: 'text/plain', buffer: Buffer.from('Memo') })));
    await page.locator('#agreement-files').setInputFiles(Array.from({ length: 5 }, (_, i) => ({ name: `extra-${i}.txt`, mimeType: 'text/plain', buffer: Buffer.from('Extra memo') })));
    await page.locator('#upload-error').getByText('Files were not added. Choose up to 10 files. Your previous selection is unchanged.', { exact: true }).waitFor();
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 6, 'A batch exceeding the combined count is rejected without losing prior files');
    assert.equal(writes.length, postCount, 'Combined batches respect the file count limit');
    while (await page.getByRole('button', { name: /^Delete / }).count()) await page.getByRole('button', { name: /^Delete / }).first().click();
    await page.locator('#agreement-files').setInputFiles({ name: 'too-large.pdf', mimeType: 'application/pdf', buffer: Buffer.alloc(12 * 1048576 + 1) });
    await page.locator('#upload-error').getByText('Files were not added. Each file must be 12 MB or smaller. Your previous selection is unchanged.', { exact: true }).waitFor();
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 0, 'An oversized file is rejected');
    await page.locator('#agreement-files').setInputFiles({ name: 'part-one.pdf', mimeType: 'application/pdf', buffer: Buffer.alloc(11 * 1048576) });
    await page.locator('#agreement-files').setInputFiles({ name: 'part-two.pdf', mimeType: 'application/pdf', buffer: Buffer.alloc(10 * 1048576) });
    await page.locator('#upload-error').getByText('Files were not added. The selected documents exceed 20 MB. Choose fewer or smaller files. Your previous selection is unchanged.', { exact: true }).waitFor();
    assert.equal(await page.locator('#agreement-files').evaluate(el => el.files.length), 1, 'A batch exceeding the total bytes leaves prior files intact');
    assert.equal(writes.length, postCount, 'Per-file and combined byte limits block upload');
    await page.screenshot({ path: path.join(shots, 'agreement-landing-files-desktop.png'), fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1), 'No horizontal mobile overflow');
    await page.screenshot({ path: path.join(shots, 'agreement-landing-mobile.png'), fullPage: true });
    assert.deepEqual(errors, []);
    console.log('PASS: additive files, deduplication, cancellation, deletion/re-addition/focus, preserved roles, combined limits, upload payload, queued/processing/ready, failure/retry, network recovery, mobile layout. All API traffic intercepted.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
