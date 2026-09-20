// Browser boundary test: uploaded-company API responses are fixtures, never live writes.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch();
 const page=await browser.newPage({viewport:{width:1536,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const cid='u123456abcdef',base='http://127.0.0.1:8013';
 const response=await page.request.get(base+'/api/h01');const seed=await response.json();
 const snapshot={...seed,borrower:{id:cid.toUpperCase(),name:'Willow Harbor Test',source_mode:'uploaded_agreement'},
  versions:[seed.versions[0]],current_version:'1.0',events:[],pending_proposal:null,drift_assessments:[],
  presentation:{as_of:'2027-04-23'},current_profile:{assessments:{}},feed:{queued:0,processing:0,errors:[]},
  uploaded_documents:[{id:'agreement',filename:'agreement.txt',kind:'agreement',role:'agreement',download_url:'/api/'+cid+'/documents/origin'},
   {id:'underwriting-memo.md',filename:'memo.txt',kind:'agreement',role:'memo'},
   {id:'CROX-10K-FY2025',filename:'10k.txt',kind:'agreement',role:'10k'}]};
 let phase=0,posts=0,rejectUpload=false,lastPayload;
 const filesDir=path.join(__dirname,'..','tmp','report-file-selection');fs.mkdirSync(filesDir,{recursive:true});
 fs.writeFileSync(path.join(filesDir,'report.txt'),'The operating report confirms stable supply.');
 fs.writeFileSync(path.join(filesDir,'appendix.md'),'Supporting report evidence.');
 const assumption=seed.profile.assumptions[0];
 const event={id:cid.toUpperCase()+'-E-test',title:'April operating report',source_kind:'uploaded_report',uploaded:true,
  event_date:'2027-04-23',available_at:'2027-04-23',review_date:'2027-04-23',package_version:'1.0',decision:{action:'pending'},
  sources:[{document_id:'report-april',locator:'para 1',text:'The operating report confirms stable supply.'}],
  analysis:{engine:'nemotron',summary:'Supply remains stable.',attributions:[{target_type:'assumption',target_id:assumption.id,
   rationale:'The report confirms stable supply.',proposed_status:'supported',evidence:[{document_id:'report-april',locator:'para 1',quote:'The operating report confirms stable supply.'}]}],covenant_assessments:[]}};
 await page.route(base+'/'+cid,route=>route.fulfill({contentType:'text/html',body:fs.readFileSync(path.join(__dirname,'b01.html'),'utf8')}));
 await page.route(base+'/api/'+cid+'**',async route=>{
  const req=route.request();
  if(req.method()==='POST'){
   assert(req.url().endsWith('/upload'));const body=req.postDataJSON();assert.equal(body.files[0].filename,'report.txt');assert(body.files[0].b64);
   posts++;lastPayload=body;
   if(rejectUpload)return route.fulfill({status:503,json:{error:'Upload unavailable. Try again.'}});
   phase=1;return route.fulfill({status:202,json:{event_id:event.id,status:'queued'}});
  }
  if(req.url().endsWith('/library'))return route.fulfill({json:{reports:[]}});
  const state=structuredClone(snapshot);
  if(phase)state.events=[{...event,status:phase===1?'processing':phase===3?'failed':'completed',analysis:phase===1?null:phase===3?{engine:'unavailable',error:'Hosted analysis unavailable'}:event.analysis}];
  state.feed.processing=phase===1?1:0;
  return route.fulfill({json:state});
 });
 try{
  await page.goto(base+'/'+cid);await page.locator('.cg-node').first().waitFor();
  assert.deepEqual(await page.locator('.cg-column-title').allTextContents(),['Source records','Library','Contractual provisions']);
  assert.deepEqual((await page.locator('.cg-source[data-cg-node]').evaluateAll(nodes=>nodes.map(n=>n.dataset.cgNode))).sort(),['source:CROX-10K-FY2025','source:underwriting-memo.md']);
  const trigger=page.locator('#add-new-reports');assert.equal(await trigger.count(),1);
  assert.equal(await trigger.evaluate(el=>getComputedStyle(el).fontSize),await page.locator('.cg-tools h2').evaluate(el=>getComputedStyle(el).fontSize));
  await trigger.click();
  const chooser=page.waitForEvent('filechooser');
  await page.getByRole('button',{name:'Add files',exact:true}).click();
  await (await chooser).setFiles(path.join(filesDir,'report.txt'));
  await page.locator('#report-files').setInputFiles(path.join(filesDir,'appendix.md'));
  assert.equal(await page.locator('[data-remove-report-file]').count(),2,'Separate picks accumulate');
  await page.locator('#report-files').setInputFiles(path.join(filesDir,'report.txt'));
  assert.equal(await page.locator('[data-remove-report-file]').count(),2,'Selecting the same file twice adds no duplicate');
  await page.locator('#report-files').setInputFiles([]);
  assert.equal(await page.locator('[data-remove-report-file]').count(),2,'Canceling a picker preserves selections');
  await page.getByRole('button',{name:'Delete appendix.md',exact:true}).click();
  assert.equal(await page.locator('[data-remove-report-file]').count(),1);
  await page.getByRole('button',{name:'Delete report.txt',exact:true}).click();
  await page.locator('#submit-reports').click();
  assert.equal(posts,0,'An empty selection is not submitted');
  await page.locator('#report-files').setInputFiles(path.join(filesDir,'report.txt'));
  await page.locator('#report-files').setInputFiles(path.join(filesDir,'appendix.md'));
  await page.locator('#report-files').setInputFiles(Array.from({length:10},(_,i)=>({name:`extra-${i}.txt`,mimeType:'text/plain',buffer:Buffer.from('Extra evidence')})));
  assert.equal(await page.locator('[data-remove-report-file]').count(),2,'An oversized batch preserves the existing selection');
  assert((await page.locator('#report-upload-error').innerText()).includes('up to 10'));
  await page.setViewportSize({width:390,height:844});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(__dirname,'..','tmp','report-file-selection-mobile.png'),fullPage:true});
  await page.setViewportSize({width:1536,height:1000});
  rejectUpload=true;await page.locator('#submit-reports').click();
  await page.locator('#report-upload-error').getByText('Upload unavailable. Try again.',{exact:true}).waitFor();
  assert.equal(await page.locator('[data-remove-report-file]').count(),2,'Upload failure preserves the chosen files');
  rejectUpload=false;
  await page.locator('#report-title').fill('April operating report');await page.locator('#submit-reports').click();
  await page.locator('#report-upload-form').waitFor({state:'detached'});
  assert.equal(posts,2);assert.deepEqual(lastPayload.files.map(f=>f.filename),['report.txt','appendix.md']);assert(await page.locator('#report-processing').isVisible());
  assert.equal(await page.locator('.cg-source[data-cg-node]').count(),2,'Processing keeps only the two inception sources');
  phase=2;await page.evaluate(()=>refresh(true));
  assert((await page.locator('#report-analysis-notice').innerText()).includes('Analysis complete!'));
  assert.equal(await page.locator('.cg-source[data-cg-node]').count(),2,'Completion notice precedes the new dot');
  await page.locator('#show-report-evidence').click();
  assert.equal(await page.locator('.cg-source[data-cg-node]').count(),3);
  assert(await page.locator('[data-cg-revealing]').count()>0,'New evidence enters through an animation');
  assert(await page.locator('.cg-link[data-cg-from="source:report-april"]').count()>0);
  await page.reload();await page.locator('.cg-source[data-cg-node]').first().waitFor();
  assert.equal(await page.locator('#report-analysis-notice').isVisible(),false,'Previously viewed completion is not replayed');
  event.id+='-failure';phase=0;await page.evaluate(()=>refresh(true));
  await page.locator('#add-new-reports').click();
  await page.locator('#report-files').setInputFiles({name:'report.txt',mimeType:'text/plain',buffer:Buffer.from('A subsequent report.')});
  await page.locator('#submit-reports').click();await page.locator('#report-upload-form').waitFor({state:'detached'});
  phase=3;await page.evaluate(()=>refresh(true));
  assert((await page.locator('#report-analysis-notice').innerText()).includes('Hosted analysis unavailable'));
  assert.equal(await page.locator('.cg-source[data-cg-node]').count(),2,'Failed processing does not reveal a new source');
  assert.equal(await page.locator('#report-processing').isVisible(),false);
  await page.locator('[data-dismiss-report-notice]').click();
  event.id+='-retry';phase=0;await page.evaluate(()=>refresh(true));await page.emulateMedia({reducedMotion:'reduce'});
  await page.locator('#add-new-reports').click();
  await page.locator('#report-files').setInputFiles({name:'report.txt',mimeType:'text/plain',buffer:Buffer.from('A subsequent report.')});
  await page.locator('#submit-reports').click();await page.locator('#report-upload-form').waitFor({state:'detached'});
  phase=2;await page.evaluate(()=>refresh(true));await page.locator('#show-report-evidence').click();
  assert.equal(await page.locator('.cg-source[data-cg-node]').count(),3);
  assert.equal(await page.locator('[data-cg-revealing]').count(),0,'Reduced motion reveals evidence without animation');
  for(const width of [1280,390]){await page.setViewportSize({width,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}
  assert.deepEqual(errors,[]);
  console.log('Report upload boundary passed: additive file selection, delete/re-add, deduplication, limits and retry retention; inception sources, completion/reveal, reduced motion and responsive layouts.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
