// Browser regression: the exact previously approved article reader must fail.
const assert=require('assert/strict'),fs=require('fs'),http=require('http'),path=require('path'),os=require('os'),{spawnSync}=require('child_process');
const {chromium}=require('playwright'),{inspect,inspectOpening,checkComposition}=require('../tools/reader_contract.cjs');
const root=path.resolve(__dirname,'..');
(async()=>{
 const server=http.createServer((req,res)=>{const u=new URL(req.url,'http://local');let file=u.pathname.startsWith('/legacy/')?path.join(__dirname,'fixtures/legacy-reader',u.pathname.slice(8)):path.join(root,'public',u.pathname);if(u.pathname.endsWith('/'))file=path.join(file,'index.html');const type=file.endsWith('.css')?'text/css':file.endsWith('.js')?'text/javascript':file.endsWith('.png')?'image/png':file.endsWith('.svg')?'image/svg+xml':'text/html';fs.readFile(file,(e,b)=>{res.writeHead(e?404:200,{'Content-Type':type});res.end(e?'missing':b)})});await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const b=await chromium.launch({headless:true,executablePath:process.env.ATLAS_CHROMIUM_PATH||undefined,args:['--no-sandbox']});
 try{
  const p=await b.newPage({viewport:{width:390,height:844}}),base=`http://127.0.0.1:${server.address().port}`;
  async function measure(url){assert((await p.goto(url)).ok());await p.waitForTimeout(800);const h=await inspect(p);await p.evaluate(()=>location.hash='perspectives');await p.waitForTimeout(700);await p.locator('#perspectives img').evaluateAll(async es=>Promise.all(es.map(e=>e.decode().catch(()=>{}))));const menu=await inspect(p);await p.evaluate(()=>location.hash='route-H1');await p.waitForTimeout(700);return {...h,entries:menu.entries,menuWidth:menu.menuWidth,scenes:(await inspect(p)).scenes}}
  const legacy=await measure(base+'/legacy/');assert(checkComposition(legacy).some(e=>e.includes('hero')));assert(checkComposition(legacy).some(e=>e.includes('Perspective')));assert(checkComposition(legacy).some(e=>e.includes('typography')));console.log('Legacy violations',checkComposition(legacy));console.log('PASS: previous false-positive reader rejected from actual rendered geometry');
  const candidate=await measure(base+'/review/aet1-wc-002/');assert.deepEqual(checkComposition(candidate),[]);
  await p.goto(base+'/review/aet1-wc-002/');await p.locator('.opening-frame').first().evaluate(e=>e.decode());
  const opening=await inspectOpening(p);assert.equal(opening.mode,'verified_image_sequence');assert(opening.frameCount>=2&&opening.cover&&opening.running&&!opening.brokenImages);assert(opening.copyOpacity<.1);
  await p.waitForTimeout(500);const advanced=await inspectOpening(p);assert.notEqual(opening.transform,advanced.transform,'image motion must visibly advance');
  await p.waitForTimeout(3300);assert((await inspectOpening(p)).frameOpacities[1]>.75,'second verified image must crossfade in');
  await p.waitForTimeout(2600);assert((await inspectOpening(p)).frameOpacities[2]>.75,'final verified image must crossfade in');
  await p.locator('.skip-film').click();await p.waitForTimeout(1000);assert.equal(await p.locator('.hero').getAttribute('data-opening-state'),'skipped');assert((await inspectOpening(p)).copyOpacity>.9);
  await p.goto(base+'/review/aet1-wc-002/');await p.waitForTimeout(8400);assert.equal(await p.locator('.hero').getAttribute('data-opening-state'),'completed','timed opening must naturally reveal identity');
  const reduced=await b.newPage({viewport:{width:390,height:844},reducedMotion:'reduce'});await reduced.goto(base+'/review/aet1-wc-002/');assert.equal(await reduced.locator('.hero').getAttribute('data-opening-state'),'reduced-motion');assert((await inspectOpening(reduced)).copyOpacity>.9);await reduced.close();
  await p.goto(base+'/review/aet1-wc-002/');await p.addStyleTag({content:'.opening-frame{animation:none!important}'});assert.equal((await inspectOpening(p)).running,false,'static opening mutation must be rejected');
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'atlas-film-test-')),film=path.join(temp,'sample.mp4');
  const encode=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=black:s=64x64:r=12','-t','5','-c:v','libx264','-pix_fmt','yuv420p',film]);assert.equal(encode.status,0,encode.stderr?.toString());
  const filmPage=await b.newPage({viewport:{width:390,height:844}});
  const source=fs.readFileSync(path.join(root,'public/review/aet1-wc-002/index.html'),'utf8');
  const filmHtml=source.replace('data-opening-mode="verified_image_sequence"','data-opening-mode="approved_film"').replace(/<div class="opening-sequence".*?<\/div>/,'<video class="hero-video" autoplay muted playsinline preload="auto"><source src="/test-film.mp4" type="video/mp4"></video>');
  await filmPage.route('**/review/aet1-wc-002/',r=>r.fulfill({status:200,contentType:'text/html',body:filmHtml}));
  await filmPage.route('**/test-film.mp4',r=>r.fulfill({status:200,contentType:'video/mp4',body:fs.readFileSync(film)}));
  await filmPage.goto(base+'/review/aet1-wc-002/');await filmPage.waitForFunction(()=>document.querySelector('video').readyState>=2);const before=await inspectOpening(filmPage);assert.equal(before.mode,'approved_film');assert(before.muted&&before.inline&&before.duration>=4&&before.copyOpacity<.1);await filmPage.waitForTimeout(600);assert((await inspectOpening(filmPage)).time>before.time,'approved film must advance');await filmPage.locator('.skip-film').click();await filmPage.waitForTimeout(1000);assert.equal(await filmPage.locator('.hero').getAttribute('data-opening-state'),'skipped');await filmPage.close();fs.rmSync(temp,{recursive:true,force:true});
  for(const [name,css,expected] of [
   ['article',' .scene{min-height:0;display:block;width:70vw}.scene>img{position:static;height:200px}', 'pacing'],
   ['image loss','.scene>img{width:20%}', 'dominance'],
   ['dense copy','.scene-copy p{font-size:30px}', 'density'],
   ['wrong type','.scene h2{font:700 20px Arial}', 'typography'],
   ['dark grade','.scene>img{filter:brightness(.3)}','grade'],
   ['card menu','.perspective-list{display:grid;grid-template-columns:1fr 1fr}','Perspective']]){
    const good=await measure(base+'/review/aet1-wc-002/');await p.addStyleTag({content:css});let bad={...good,scenes:(await inspect(p)).scenes};if(name==='card menu'){await p.evaluate(()=>location.hash='perspectives');await p.waitForTimeout(700);const m=await inspect(p);bad.entries=m.entries;bad.menuWidth=m.menuWidth}assert(checkComposition(bad).some(e=>e.includes(expected)),name);console.log('PASS:',name,'mutation rejected');
  }
 }finally{await b.close();server.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
