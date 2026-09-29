// Complete beat/route render check, after early AOC-001 visual approval.
const fs=require('fs'),http=require('http'),path=require('path'),crypto=require('crypto');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),run=path.resolve(process.argv[2]||'content/AUTOMATED-TEST-001');
const receiptPath=path.join(run,'full-reader-gate.json');
const receipt=JSON.parse(fs.readFileSync(receiptPath));
const live=process.argv.includes('--live');
const deployment=live?JSON.parse(fs.readFileSync(path.join(run,'deployment-receipt.json'))):null;
const outputPath=live?path.join(run,'live-reader-gate.json'):receiptPath;
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const publicRoot=path.join(root,'public'),reader=path.join(root,receipt.reader);
const assets=JSON.parse(fs.readFileSync(path.join(run,'asset-persistence-receipt.json'))).assets;
const expected=new Set(assets.map(a=>a.path));
const defects=[],shots=[];
let browser;
function check(ok,reason){if(!ok)defects.push(reason)}
const server=http.createServer((req,res)=>{
 let u;try{u=decodeURIComponent(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400).end();return}
 let f=path.resolve(publicRoot,'.'+u);
 if(!f.startsWith(publicRoot+path.sep)){res.writeHead(403).end();return}
 if(u.endsWith('/'))f=path.join(f,'index.html');
 const mime=f.endsWith('.css')?'text/css':f.endsWith('.js')?'text/javascript':f.endsWith('.svg')?'image/svg+xml':f.endsWith('.png')?'image/png':'text/html';
 fs.readFile(f,(error,data)=>{res.writeHead(error?404:200,{'Content-Type':mime});res.end(error?'missing':data)});
});
async function finish(status){
 fs.writeFileSync(outputPath,JSON.stringify({...receipt,status,defects,screenshots:shots,
   ...(live?{reader_hashes:deployment.reader_hashes,deploy_id:deployment.deploy_id,
             url:deployment.url,commit:deployment.commit}:{}),
   asset_generation_authorized:false,publication_authorized:false},null,2)+'\n');
 if(browser)await browser.close().catch(()=>{});
 server.close();
 console.log(JSON.stringify({status,checked_assets:expected.size,defects,screenshots:shots.length}));
 if(status!=='PASS')process.exitCode=1;
}
(async()=>{
 check(sha(reader)===receipt.reader_sha256,'reader changed since assembly');
 check(expected.size===receipt.asset_count,'asset receipt count changed');
 if(live)check(deployment.status==='PASS'&&deployment.asset_integration_status==='PASS','deployment bytes not verified');
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const base=live?deployment.url:`http://127.0.0.1:${server.address().port}/${receipt.reader.replace(/^public\//,'').replace(/index.html$/,'')}`;
 for(const [name,width,height] of [['phone',390,844],['small-phone',320,740],['desktop',1440,900]]){
  console.log(`Full reader: ${name}`);
  const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
  page.setDefaultTimeout(12000);
  const pageErrors=[];page.on('pageerror',e=>pageErrors.push(e.message));
  page.on('response',response=>{if(response.status()>=400&&new URL(response.url()).origin===new URL(base).origin)pageErrors.push(`HTTP ${response.status()} ${response.url()}`)});
  await page.goto(base,{waitUntil:'networkidle'});
  {
   const dir=path.join(run,live?'live-gate-shots':'full-gate-shots');fs.mkdirSync(dir,{recursive:true});
   const opening=path.join(dir,`${name}-opening.png`);
   await page.locator('.hero').screenshot({path:opening});shots.push({path:live?path.relative(run,opening):path.relative(root,opening),sha256:sha(opening)});
   await page.evaluate(()=>{location.hash='perspectives'});
   const menu=page.locator('#perspectives');await menu.waitFor({state:'visible'});
   await menu.locator('img').evaluateAll(async images=>Promise.all(images.map(async image=>{image.loading='eager';await image.decode().catch(()=>{})})));
   const choice=path.join(dir,`${name}-perspectives.png`);
   await menu.screenshot({path:choice});shots.push({path:live?path.relative(run,choice):path.relative(root,choice),sha256:sha(choice)});
  }
  await page.locator('.enter').click();
  check(await page.locator('.hero').evaluate(e=>e.classList.contains('film-complete')),`${name}: opening reveal failed`);
  const firstHotspot=page.locator('.perspective-menu-image > .perspective-hotspot').first();
  const firstRoute=await firstHotspot.getAttribute('href');
  await firstHotspot.click();await page.locator(firstRoute).waitFor({state:'visible'});
  await page.locator(firstRoute+' header a[href="#perspectives"]').click();
  check(await page.locator(firstRoute).isHidden(),`${name}: Perspective exit failed`);
  await page.goBack();await page.locator(firstRoute).waitFor({state:'visible'});
  await page.evaluate(()=>{location.hash='perspectives'});
  const routes=await page.locator('.perspective-route').evaluateAll(es=>es.map(e=>e.id));
  const used=new Set();let sceneCount=0;
  for(const id of routes){
   await page.evaluate(id=>{location.hash=id},id);
   const route=page.locator('#'+id);await route.waitFor({state:'visible'});
   const observations=await route.locator('.scene').evaluateAll(async nodes=>{
    const output=[];
    for(const node of nodes){
     const img=node.querySelector('img');if(img){img.loading='eager';await img.decode().catch(()=>{})}
     const r=node.getBoundingClientRect(),p=node.querySelector('p'),h=node.querySelector('h2');
     const ir=img?.getBoundingClientRect(),s=img?getComputedStyle(img):null;
     output.push({id:node.id,path:img?new URL(img.src).pathname:null,decoded:!img||img.naturalWidth>0,
       width:r.width,height:r.height,imgWidth:ir?.width||0,imgHeight:ir?.height||0,
       fit:s?.objectFit,heading:h?parseFloat(getComputedStyle(h).fontSize):null,serif:h?getComputedStyle(h).fontFamily.includes('Georgia'):true,
       words:p?.textContent.trim().split(/\s+/).length||0,truth:!!node.querySelector('small'),
       source:!!node.querySelector('a[href^="#source-"]'),gradient:getComputedStyle(node,'::after').backgroundImage.includes('gradient'),
       blank:!img||!p?.textContent.trim()||node.matches('.text-scene,.graphic')});
    }
    return output;
   });
   for(const o of observations){
    sceneCount++;if(o.path)used.add(o.path);
    check(o.width>=width*.98&&o.height>=height*.98&&(o.heading===null||o.heading>=32)&&o.serif&&o.words<=70&&o.truth&&o.source&&!o.blank,
      `${name}/${o.id}: pacing, typography or truth boundary`);
    check(o.decoded&&o.path&&!o.path.endsWith('.svg')&&(!o.path||o.fit!=='cover'||(o.imgWidth>=o.width*.98&&o.imgHeight>=o.height*.98&&o.gradient)),
      `${name}/${o.id}: image decode, dominance or continuity`);
   }
   if(id.startsWith('route-')){
    check(await route.locator('.purposeful-ending').evaluateAll(es=>es.length===1&&!!es[0].dataset.sourceId&&!!es[0].querySelector('a[href^="https://"]')&&!!es[0].querySelector('p')?.textContent.trim()),`${name}/${id}: sourced purposeful ending missing`);
    check(await route.locator('.route-exit[href="#perspectives"]').count()===1,`${name}/${id}: choice return missing`);
    check(await route.locator('.route-end').evaluate(e=>{const a=e.querySelector('.purposeful-ending a'),details=e.querySelector('details'),exit=e.querySelector('.route-exit');return !!a&&!!details&&a.getBoundingClientRect().bottom+8<=details.getBoundingClientRect().top&&details.getBoundingClientRect().bottom+8<=exit.getBoundingClientRect().top}),`${name}/${id}: ending controls overlap`);
   }
   check(await route.locator('.scene').evaluateAll(nodes=>{const headings={};const prose=new Set();for(const node of nodes){headings[node.dataset.scene]=(headings[node.dataset.scene]||0)+node.querySelectorAll('h2').length;const text=node.querySelector('[data-prose]')?.textContent.trim();if(!text||prose.has(text))return false;prose.add(text)}return Object.values(headings).every(n=>n===1)}),`${name}/${id}: duplicate prose or scene heading`);
   if(observations.length){
    const indices=name==='phone'?observations.map((_,i)=>i):[0,observations.length-1];
    for(const index of new Set(indices)){
     const file=path.join(run,live?'live-gate-shots':'full-gate-shots',`${name}-${id}-beat-${index+1}.png`);fs.mkdirSync(path.dirname(file),{recursive:true});
     await route.locator('.scene').nth(index).screenshot({path:file});shots.push({path:live?path.relative(run,file):path.relative(root,file),sha256:sha(file)});
    }
    if(id.startsWith('route-')){const end=path.join(run,live?'live-gate-shots':'full-gate-shots',`${name}-${id}-ending.png`);await route.locator('.route-end').screenshot({path:end});shots.push({path:live?path.relative(run,end):path.relative(root,end),sha256:sha(end)});}
   }
  }
  check(sceneCount===receipt.beat_count,`${name}: rendered ${sceneCount} beats, planned ${receipt.beat_count}`);
  const nonScene=await page.locator('.hero img,.edition-menu-slice img').evaluateAll(async images=>{
   await Promise.all(images.map(async image=>{image.loading='eager';await image.decode().catch(()=>{})}));
   return images.map(image=>({path:new URL(image.src).pathname,ok:image.naturalWidth>0}));
  });
  for(const a of nonScene){if(a.ok)used.add(a.path);else defects.push(`${name}: opening/menu image failed to decode ${a.path}`)}
  const graphics=await page.locator('.graphic-evidence').evaluateAll(links=>links.map(link=>new URL(link.href).pathname));
  for(const p of graphics)used.add(p);
  check(graphics.length===9&&graphics.every(p=>p.endsWith('.svg')&&expected.has(p)),`${name}: explanatory graphics must remain accessible, verified references`);
  const menuPaths=await page.locator('.edition-menu-slice img').evaluateAll(images=>images.map(image=>new URL(image.src).pathname));
  check(new Set(menuPaths).size===menuPaths.length,`${name}: Perspective menu repeats imagery despite complete verified asset coverage`);
  check(await page.locator('.edition-menu-label span').evaluateAll(es=>new Set(es.map(e=>e.textContent.trim())).size===es.length),`${name}: menu teaser duplication`);
  check([...expected].every(p=>used.has(p)),`${name}: persisted visual missing from rendered reader: ${[...expected].filter(p=>!used.has(p)).join(', ')}`);
  await page.evaluate(()=>{location.hash='story'});await page.locator('#story').waitFor({state:'visible'});
  check((await page.locator('#story').innerText()).includes('FICTION'),`${name}: story truth boundary missing`);
  const storyShot=path.join(run,live?'live-gate-shots':'full-gate-shots',`${name}-story.png`);await page.locator('#story .boundary').first().screenshot({path:storyShot});shots.push({path:live?path.relative(run,storyShot):path.relative(root,storyShot),sha256:sha(storyShot)});
  if(name==='phone'){const last=path.join(run,live?'live-gate-shots':'full-gate-shots',`${name}-story-last.png`);await page.locator('#story .story-copy p').last().screenshot({path:last});shots.push({path:live?path.relative(run,last):path.relative(root,last),sha256:sha(last)});}
  await page.evaluate(()=>{location.hash='sources'});await page.locator('#sources').waitFor({state:'visible'});
  check(await page.locator('#sources details').count()>0,`${name}: sources absent`);
  const sourceShot=path.join(run,live?'live-gate-shots':'full-gate-shots',`${name}-sources.png`);await page.locator('#sources').screenshot({path:sourceShot});shots.push({path:live?path.relative(run,sourceShot):path.relative(root,sourceShot),sha256:sha(sourceShot)});
  check(!pageErrors.length,`${name}: browser errors: ${pageErrors.join('; ')}`);
  await page.close();
 }
 await finish(defects.length?'FAIL':'PASS');
})().catch(async error=>{defects.push(String(error));await finish('FAIL')});
