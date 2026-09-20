const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1536,height:1080}});
 const errors=[],writes=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(r.method()!=='GET')writes.push(r.method()+' '+r.url())});
 await page.goto('http://127.0.0.1:8035/workspace.html');
 await page.locator('.ph-section').waitFor();
 assert.equal(await page.locator('[data-company]').inputValue(),'B01');
 assert.equal(await page.locator('.w-version-value').innerText(),'v1.2');
 assert((await page.locator('.w-pending-label').innerText()).includes('v1.3'));
 await page.screenshot({path:path.join(__dirname,'workspace-desktop.png'),fullPage:true});
 await page.locator('[data-ph-event="B01-D03"]').click();
 assert((await page.locator('.w-context').innerText()).includes('Focused'),'Clicking selected marker focuses evidence');
 await page.locator('[data-ph-range]').click();
 assert((await page.locator('.ph-window').innerText()).includes('Dec 31, 2026'));
 assert.equal(await page.evaluate(()=>RC.state.eventId),'B01-D03');
 await page.locator('[data-ph-range]').click();
 await page.locator('[data-ph-version]').last().click();
 assert((await page.locator('#rc-inspector').innerText()).includes('1.3'));
 assert((await page.locator('#rc-inspector').innerText()).toLowerCase().includes('no effective date'));
 await page.locator('[data-close]').click();
 await page.locator('[data-compare-packages]').click();
 assert((await page.locator('#rc-inspector').innerText()).includes('S1'));
 assert((await page.locator('#rc-inspector').innerText()).includes('S2'));
 await page.locator('[data-close]').click();
 for(const [eventId,version,term]of[['B01-D01','1.0','four'],['B01-D03','1.2','two']]){
   await page.locator(`[data-ph-event="${eventId}"]`).click();
   assert.equal(await page.evaluate(()=>RC.state.eventId),eventId);
   assert((await page.locator('.w-context').innerText()).includes('Focused'));
   await page.locator('[data-node="S2"]').click();
   assert((await page.locator('.c-inspector').innerText()).includes('Package v'+version));
   await page.locator('[data-open-covenant="S2"]').click();
   const text=await page.locator('#rc-inspector').innerText();
   assert(text.includes(term+' consecutive hours'),eventId+' has correct S2 threshold');
   await page.locator('[data-close]').click();
 }
 for(const cid of ['R01','R02','B01']){
  await page.locator('[data-company]').selectOption(cid);
  assert((await page.locator('.ph-section').innerText()).includes('Package history'));
  assert.equal(await page.evaluate(()=>RC.company().id),cid);
 }
 for(const width of [1280,900,768,390]){
  await page.setViewportSize({width,height:1000});
  const size=await page.evaluate(()=>({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}));
  assert(size.scroll<=size.client+2,'No page overflow at '+width+': '+JSON.stringify(size));
  if(width===390)await page.screenshot({path:path.join(__dirname,'workspace-mobile.png'),fullPage:true});
 }
 assert.deepEqual(errors,[]);assert.deepEqual(writes,[]);
 console.log('Combined workspace passed: package history, operative/pending state, full comparison, linked selection, date-specific S2 terms, all companies, responsive widths, no browser errors or writes.');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
