// Complete beat/route render check, after early AOC-001 visual approval.
const fs=require('fs'),http=require('http'),path=require('path'),crypto=require('crypto');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),run=path.resolve(process.argv[2]||'content/AUTOMATED-TEST-001');
const receiptPath=path.join(run,'full-reader-gate.json');
const receipt=JSON.parse(fs.readFileSync(receiptPath));
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
 fs.writeFileSync(receiptPath,JSON.stringify({...receipt,status,defects,screenshots:shots,
   asset_generation_authorized:false,publication_authorized:false},null,2)+'\n');
 if(browser)await browser.close().catch(()=>{});
 server.close();
 console.log(JSON.stringify({status,checked_assets:expected.size,defects,screenshots:shots.length}));
 if(status!=='PASS')process.exitCode=1;
}
(async()=>{
 check(sha(reader)===receipt.reader_sha256,'reader changed since assembly');
 check(expected.size===receipt.asset_count,'asset receipt count changed');
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const base=`http://127.0.0.1:${server.address().port}/${receipt.reader.replace(/^public\//,'').replace(/index.html$/,'')}`;
 for(const [name,width,height] of [['phone',390,844],['small-phone',320,740],['desktop',1440,900]]){
  console.log(`Full reader: ${name}`);
  const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
  page.setDefaultTimeout(12000);
  const pageErrors=[];page.on('pageerror',e=>pageErrors.push(e.message));
  await page.goto(base,{waitUntil:'networkidle'});
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
       fit:s?.objectFit,heading:parseFloat(getComputedStyle(h).fontSize),serif:getComputedStyle(h).fontFamily.includes('Georgia'),
       words:p?.textContent.trim().split(/\s+/).length||0,truth:!!node.querySelector('small'),
       source:!!node.querySelector('a[href^="#source-"]'),gradient:getComputedStyle(node,'::after').backgroundImage.includes('gradient')});
    }
    return output;
   });
   for(const o of observations){
    sceneCount++;if(o.path)used.add(o.path);
    check(o.width>=width*.98&&o.height>=height*.98&&o.heading>=32&&o.serif&&o.words<=70&&o.truth&&o.source,
      `${name}/${o.id}: pacing, typography or truth boundary`);
    check(o.decoded&&(!o.path||o.fit!=='cover'||(o.imgWidth>=o.width*.98&&o.imgHeight>=o.height*.98&&o.gradient)),
      `${name}/${o.id}: image decode, dominance or continuity`);
   }
   if(id.startsWith('route-')){
    check(await route.locator('.purposeful-ending').count()===1,`${name}/${id}: purposeful ending missing`);
    check(await route.locator('.route-exit[href="#perspectives"]').count()===1,`${name}/${id}: choice return missing`);
   }
   if(observations.length&&(id===routes[0]||id===routes[routes.length-2])&&name!=='small-phone'){
    const file=path.join(run,'full-gate-shots',`${name}-${id}.png`);fs.mkdirSync(path.dirname(file),{recursive:true});
    await route.locator('.scene').first().screenshot({path:file});shots.push({path:path.relative(root,file),sha256:sha(file)});
   }
  }
  check(sceneCount===receipt.beat_count,`${name}: rendered ${sceneCount} beats, planned ${receipt.beat_count}`);
  const nonScene=await page.locator('.hero img,.perspective img').evaluateAll(async images=>{
   await Promise.all(images.map(async image=>{image.loading='eager';await image.decode().catch(()=>{})}));
   return images.map(image=>({path:new URL(image.src).pathname,ok:image.naturalWidth>0}));
  });
  for(const a of nonScene){if(a.ok)used.add(a.path);else defects.push(`${name}: opening/menu image failed to decode ${a.path}`)}
  check([...expected].every(p=>used.has(p)),`${name}: persisted visual missing from rendered reader: ${[...expected].filter(p=>!used.has(p)).join(', ')}`);
  await page.evaluate(()=>{location.hash='story'});await page.locator('#story').waitFor({state:'visible'});
  check((await page.locator('#story').innerText()).includes('FICTION'),`${name}: story truth boundary missing`);
  await page.evaluate(()=>{location.hash='sources'});await page.locator('#sources').waitFor({state:'visible'});
  check(await page.locator('#sources details').count()>0,`${name}: sources absent`);
  check(!pageErrors.length,`${name}: browser errors: ${pageErrors.join('; ')}`);
  await page.close();
 }
 await finish(defects.length?'FAIL':'PASS');
})().catch(async error=>{defects.push(String(error));await finish('FAIL')});
