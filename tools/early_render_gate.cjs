// Rendered structural gate, before any image generation. Run with Playwright.
const fs=require('fs'),http=require('http'),path=require('path'),crypto=require('crypto');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),run=path.resolve(process.argv[2]||'content/AUTOMATED-TEST-001');
const receipt=JSON.parse(fs.readFileSync(path.join(run,'early-reader-gate.json')));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const publicRoot=path.join(root,'public'),reader=path.join(root,receipt.reader);
const checks=[];
function check(condition,message){if(!condition)checks.push(message)}
const server=http.createServer((req,res)=>{
 let url;try{url=decodeURIComponent(new URL(req.url,'http://localhost').pathname)}catch{res.writeHead(400).end();return}
 let file=path.resolve(publicRoot,'.'+url);
 if(!file.startsWith(publicRoot+path.sep)){res.writeHead(403).end();return}
 if(url.endsWith('/'))file=path.join(file,'index.html');
 const mime=file.endsWith('.css')?'text/css':file.endsWith('.js')?'text/javascript':file.endsWith('.svg')?'image/svg+xml':file.endsWith('.png')?'image/png':file.endsWith('.mp4')?'video/mp4':'text/html';
 fs.readFile(file,(err,data)=>{res.writeHead(err?404:200,{'Content-Type':mime});res.end(err?'missing':data)})
});
(async()=>{
 check(sha(reader)===receipt.reader_sha256,'reader changed after preview receipt');
 check(sha(path.join(root,'public/adaptive/adaptive.css'))===receipt.canonical_css_sha256,'canonical CSS changed');
 check(sha(path.join(path.dirname(reader),'adaptive.css'))===receipt.canonical_css_sha256,'inherited CSS differs');
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const base=`http://127.0.0.1:${server.address().port}/${receipt.reader.replace(/^public\//,'').replace(/index.html$/,'')}`;
 const expected=JSON.parse(fs.readFileSync(path.join(run,'causal_boundary_gate.json'))).output.routes.length;
 const shots=[];
 for(const [name,width,height] of [['phone',390,844],['small-phone',320,740],['desktop',1440,900]]){
  const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base,{waitUntil:'networkidle'});
  let state=await page.evaluate(()=>{
   const h=document.querySelector('.hero'),t=h.querySelector('h1'),s=getComputedStyle(t),bg=h.querySelector('.edition-geo-bg');
   return {height:h.getBoundingClientRect().height,heading:parseFloat(s.fontSize),serif:s.fontFamily.includes('Georgia'),cover:getComputedStyle(bg).objectFit==='cover',count:document.querySelectorAll('[data-perspective]').length,broken:[...document.images].filter(i=>i.complete&&!i.naturalWidth).length,overflow:document.documentElement.scrollWidth>innerWidth+2,copy:getComputedStyle(t).opacity};
  });
  check(state.height>=height*.98&&state.serif&&state.heading>=50&&state.cover,`${name}: canonical opening composition`);
  check(state.count===expected&&state.broken===0&&!state.overflow,`${name}: Perspective count, image decoding or viewport overflow`);
  await page.locator('.skip-film').click();
  check(await page.locator('.hero').evaluate(e=>e.classList.contains('film-complete')),`${name}: skip/reveal`);
  const dir=path.join(run,'early-gate-shots');fs.mkdirSync(dir,{recursive:true});
  for(const [label,selector] of [['opening','.hero'],['perspectives','#perspectives']]){
   if(label==='perspectives')await page.locator('.enter').click();
   const file=path.join(dir,`${name}-${label}.png`);await page.locator(selector).screenshot({path:file});shots.push({path:path.relative(root,file),sha256:sha(file)});
  }
  const first=await page.locator('[data-perspective]').first().getAttribute('href');
  await page.locator('[data-perspective]').first().click();
  const route=page.locator(first);check(await route.isVisible(),`${name}: chosen Perspective did not open`);
  await route.locator('img').evaluateAll(async images=>Promise.all(images.map(async image=>{image.loading='eager';await image.decode().catch(()=>{})})));
  const measures=await route.locator('.scene').evaluateAll(nodes=>nodes.map(e=>{
   const h=e.querySelector('h2'),p=e.querySelector('p'),img=e.querySelector('img'),r=e.getBoundingClientRect(),s=getComputedStyle(h),c=getComputedStyle(p);
   const ir=img?.getBoundingClientRect(),is=img?getComputedStyle(img):null;
   return {height:r.height,width:r.width,heading:parseFloat(s.fontSize),serif:s.fontFamily.includes('Georgia'),body:parseFloat(c.fontSize),image:img?img.complete&&img.naturalWidth>0:true,fit:is?.objectFit,imageWidth:ir?.width||0,imageHeight:ir?.height||0,layer:is?.position==='absolute',gradient:getComputedStyle(e,'::after').backgroundImage.includes('gradient'),words:p.textContent.trim().split(/\s+/).length,truth:!!e.querySelector('small'),source:!!e.querySelector('a[href^="#source-"]')};
  }));
  check(measures.length>0&&measures.every(m=>m.height>=height*.98&&m.width>=width*.98&&m.heading>=32&&m.serif&&m.body>=17&&m.image&&m.words<=70&&m.truth&&m.source),`${name}: scene pacing, type, image or truth boundary`);
  check(measures.every(m=>m.fit!=='cover'||(m.imageWidth>=m.width*.98&&m.imageHeight>=m.height*.98&&m.layer&&m.gradient)),`${name}: image dominance and overlay continuity`);
  const file=path.join(dir,`${name}-scene.png`);await route.locator('.scene').first().screenshot({path:file});shots.push({path:path.relative(root,file),sha256:sha(file)});
  await page.reload();check(await route.isVisible(),`${name}: deep link reload`);
  await page.locator('.route-exit').first().click();check(await page.locator('#perspectives').isVisible(),`${name}: return to choices`);
  await page.goBack();check(await route.isVisible(),`${name}: browser Back`);
  await route.locator('a[href^="#source-"]').first().click();
  check(await page.locator('#sources').isVisible()&&await page.locator('details[open]').count()>0,`${name}: evidence link and source limits`);
  check(!errors.length,`${name}: ${errors.join('; ')}`);
  await page.close();
 }
 await browser.close();server.close();
 const result={...receipt,status:checks.length?'FAIL':'PASS',defects:checks,screenshots:shots,asset_generation_authorized:false,publication_authorized:false};
 fs.writeFileSync(path.join(run,'early-reader-gate.json'),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({status:result.status,defects:checks,screenshots:shots.length}));
 if(checks.length)process.exitCode=1;
})().catch(e=>{server.close();console.error(e);process.exitCode=1});
