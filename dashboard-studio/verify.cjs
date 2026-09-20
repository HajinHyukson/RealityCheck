const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = process.env.DASHBOARD_URL || 'http://127.0.0.1:8035';
const views = process.argv.slice(2).length ? process.argv.slice(2) : ['constellation','board','desk','storyline','matrix'];
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1536,height:1060},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const results=[];
 for(const view of views){
  const response=await page.goto(`${base}/${view}.html`);assert.equal(response.status(),200,view+' loads');
  await page.locator('[data-company]').waitFor();
  assert.equal(await page.locator('[data-company]').inputValue(),'R01');
  assert((await page.locator('body').innerText()).includes('iRobot'));
  await page.screenshot({path:path.join(__dirname,view+'-desktop.png'),fullPage:true});
  for(const cid of ['B01','R02','R01']){
   await page.locator('[data-company]').selectOption(cid);
   assert.equal(await page.evaluate(()=>RC.company().id),cid);
   assert.equal(await page.locator('[data-company]').inputValue(),cid);
   const source=await page.evaluate(()=>({id:RC.company().sources[0].id,title:RC.company().sources[0].title}));
   await page.evaluate(id=>RC.showSource(id),source.id);
   assert.equal(await page.locator('#rc-inspector').evaluate(x=>x.open),true);
   assert((await page.locator('#rc-inspector').innerText()).includes(source.title));
   assert((await page.locator('#rc-inspector .rc-source-text').innerText()).length>100);
   assert((await page.locator('#rc-inspector').innerText()).includes('Source coverage:'));
   await page.locator('[data-close]').click();
  }
  await page.locator('[data-query]').fill('no_such_record_98612');
  await page.waitForTimeout(230);
  assert.equal(await page.evaluate(()=>RC.state.query),'no_such_record_98612');
  await page.locator('[data-query]').fill('');await page.waitForTimeout(230);
  await page.evaluate(()=>RC.showAssumption(RC.company().assumptions[0].id));
  assert((await page.locator('#rc-inspector').innerText()).includes('Assessment history'));
  await page.locator('[data-close]').click();
  await page.evaluate(()=>RC.showEvent(RC.company().events.at(-1).id));
  assert((await page.locator('#rc-inspector').innerText()).includes('Recorded findings'));
  await page.locator('[data-note-key]').fill('Browser verification note');
  await page.locator('[data-save-note]').click();
  const saved=await page.locator('[data-note-key]').getAttribute('data-note-key');
  assert.equal(await page.evaluate(key=>localStorage.getItem('rc-note-'+key),saved),'Browser verification note');
  await page.evaluate(key=>localStorage.removeItem('rc-note-'+key),saved);
  await page.locator('[data-close]').click();
  for(const width of [1280,768,390]){
   await page.setViewportSize({width,height:1000});
   const d=await page.evaluate(()=>({screen:document.documentElement.clientWidth,content:document.documentElement.scrollWidth}));
   assert(d.content<=d.screen+2,view+' page overflows at '+width+': '+JSON.stringify(d));
   if(width===390)await page.screenshot({path:path.join(__dirname,view+'-mobile.png'),fullPage:true});
  }
  await page.setViewportSize({width:1536,height:1060});
  results.push(view+': companies, real-source inspection, search, assumption/event dialogs, notes, responsive widths passed');
 }
 assert.deepEqual(errors,[],'No uncaught browser errors');
 console.log(results.join('\n'));
 fs.writeFileSync(path.join(__dirname,'verification.json'),JSON.stringify({at:new Date().toISOString(),results,errors},null,2));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
