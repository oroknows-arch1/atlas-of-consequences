// Computed layout + actual interaction contract. No PASS from source-string presence.
const fs=require('fs'),path=require('path');
const grammar=JSON.parse(fs.readFileSync(path.join(__dirname,'../atlas/contracts/reader-grammar.json')));
function checkComposition(m){
 const t=grammar.thresholds, e=[];
 if(m.hero.height<m.viewport.height*.98||m.hero.width<m.viewport.width*.98)e.push('hero must fill viewport');
 if(!m.hero.cover)e.push('hero media must cover the viewport');
 if(m.hero.heading<t.hero_heading_min_px||m.hero.heading>t.hero_heading_max_px||m.hero.weight>500)e.push('hero type hierarchy');
 if(!m.hero.serif)e.push('hero serif identity missing');
 if(!m.entries.length||m.entries.length!==m.routeCount)e.push('Perspective choices must match routes');
 for(const x of m.entries){if(!x.image||x.width<m.menuWidth*.97||x.height<t.perspective_min_height||!x.layered)e.push('Perspective image-led vertical composition');}
 for(const s of m.scenes){
  if(s.width<m.viewport.width*.98||s.height<m.viewport.height*t.scene_min_viewport)e.push(s.id+': full-screen pacing');
  if(s.heading<t.heading_min_px||s.heading>t.heading_max_px||s.weight>500||!s.serif)e.push(s.id+': typography hierarchy');
  if(s.body<t.body_min_px||s.body>t.body_max_px||s.words>t.max_prose_words)e.push(s.id+': text density');
  if(s.copyHeight>m.viewport.height*t.copy_max_viewport_fraction)e.push(s.id+': text occupies image area');
  if(s.kind==='scene-overlay'){
   if(s.imageWidth<s.width*t.image_width_fraction||s.imageHeight<s.height*t.image_height_fraction||s.fit!=='cover'||!s.layered)e.push(s.id+': image dominance/layering');
   if(s.brightness<t.brightness_min||s.brightness>t.brightness_max||!s.gradient)e.push(s.id+': image grade/overlay');
  }else if(s.kind==='graphic'&&s.fit!=='contain')e.push(s.id+': diagram cropped');
 }
 if(m.overflow)e.push('viewport overflow');
 return [...new Set(e)];
}
async function inspect(page){return page.evaluate(()=>{
 const rect=e=>e?.getBoundingClientRect()||{width:0,height:0};
 const style=e=>e?getComputedStyle(e):{};
 const hero=document.querySelector('.hero'), h=hero?.querySelector('h1'),hi=hero?.querySelector('img');
 const entries=[...document.querySelectorAll('[data-perspective]')].map(e=>{const r=rect(e),i=e.querySelector('img');return {width:r.width,height:r.height,image:!!i?.naturalWidth,layered:style(i).position==='absolute'}});
 const scenes=[...document.querySelectorAll('[data-view]:not([hidden]) .scene')].map(e=>{
 const r=rect(e),c=e.querySelector('.scene-copy'),p=c?.querySelector('[data-prose],p'),h=c?.querySelector('h2'),img=e.querySelector('img'),ir=rect(img),cs=style(c),is=style(img),hs=style(h),ps=style(p);
 return {id:e.id,kind:e.classList.contains('graphic')?'graphic':e.classList.contains('scene-overlay')?'scene-overlay':'text-scene',width:r.width,height:r.height,heading:parseFloat(hs.fontSize)||0,weight:parseInt(hs.fontWeight)||0,serif:/Georgia/.test(hs.fontFamily),body:parseFloat(ps.fontSize)||0,words:p?.textContent.trim().split(/\s+/).length||0,copyHeight:rect(c).height-parseFloat(cs.paddingTop||0)-parseFloat(cs.paddingBottom||0),imageWidth:ir.width,imageHeight:ir.height,fit:is.objectFit,layered:is.position==='absolute'&&cs.position==='relative',brightness:parseFloat(is.filter?.match(/brightness\(([^)]+)/)?.[1]||1),gradient:getComputedStyle(e,'::after').backgroundImage.includes('gradient')};
 });
 return {viewport:{width:innerWidth,height:innerHeight},hero:{width:rect(hero).width,height:rect(hero).height,heading:parseFloat(style(h).fontSize)||0,weight:parseInt(style(h).fontWeight)||0,serif:/Georgia/.test(style(h).fontFamily),cover:style(hi).objectFit==='cover'},entries,menuWidth:rect(document.querySelector('.perspective-list')).width,routeCount:document.querySelectorAll('[data-view][id^="route-"]').length,scenes,overflow:document.documentElement.scrollWidth>innerWidth+2};
 });}
async function audit(browser,url,capture){
 const errors=[],measurements=[],motion=[],canonical=[];
 for(const v of grammar.viewports){
  const page=await browser.newPage({viewport:{width:v.width,height:v.height}});
  await page.goto(url,{waitUntil:'networkidle'});
  const initial=await inspectOpening(page);
  if(initial.mode==='approved_film'){
   if(initial.ready<2||!Number.isFinite(initial.duration)||initial.duration<4||!initial.muted||!initial.inline)errors.push(v.name+': opening film unavailable/invalid');
   if(initial.copyOpacity>.1)errors.push(v.name+': title appears before film');
   await capture(page,`${v.name}-opening`);
   await page.waitForTimeout(400);
   const advancing=await page.locator('video').evaluate(el=>el.currentTime);
   if(advancing<=initial.time)errors.push(v.name+': film did not play');
   motion.push({device:v.name,...initial,advancing});
  }else if(initial.mode==='verified_image_sequence'){
   if(initial.frameCount<2||initial.brokenImages||!initial.cover||!initial.running||initial.copyOpacity>.1)errors.push(v.name+': verified-image opening composition invalid');
   await capture(page,`${v.name}-opening`);
   await page.waitForTimeout(500);
   const later=await inspectOpening(page);
   if(initial.transform===later.transform&&initial.opacity===later.opacity)errors.push(v.name+': image sequence lacks visible motion');
   await page.waitForTimeout(3300);const middle=await inspectOpening(page);await capture(page,`${v.name}-opening-middle`);
   await page.waitForTimeout(2600);const final=await inspectOpening(page);await capture(page,`${v.name}-opening-final`);
   if(middle.frameOpacities[1]<.75||final.frameOpacities[initial.frameCount-1]<.75)errors.push(v.name+': opening crossfade progression missing');
   motion.push({device:v.name,...initial,later:{transform:later.transform,opacity:later.opacity},middle:middle.frameOpacities,final:final.frameOpacities});
  }else errors.push(v.name+': cinematic opening missing');
  if(initial.mode==='approved_film'||initial.mode==='verified_image_sequence'){
   await page.locator('.skip-film').click();await page.waitForTimeout(1000);
   if(!await page.locator('.hero').evaluate(e=>e.classList.contains('film-complete')))errors.push(v.name+': skip did not reveal identity');
   const revealed=await inspectOpening(page);
   if(revealed.copyOpacity<.9||!await page.locator('a.enter').isVisible())errors.push(v.name+': identity/navigation not revealed');
   motion[motion.length-1].skip=true;
  }
  await page.waitForTimeout(700);
  const hero=await inspect(page);await capture(page,`${v.name}-identity`);
  await page.locator('a.enter').click();await page.waitForTimeout(700);
  await page.locator('#perspectives img').evaluateAll(async imgs=>Promise.all(imgs.map(async i=>{i.loading='eager';await i.decode().catch(()=>{})})));
  const menu=await inspect(page);await capture(page,`${v.name}-perspective-menu`);
  const m={...hero,entries:menu.entries,menuWidth:menu.menuWidth,scenes:[],device:v.name};
  const ids=await page.locator('[data-view].route').evaluateAll(es=>es.map(e=>e.id));
  for(const id of ids){
   await page.evaluate(id=>{location.hash=id},id);await page.waitForFunction(id=>!document.getElementById(id).hidden,id);await page.waitForTimeout(650);
   await page.locator(`#${id} img`).evaluateAll(async imgs=>Promise.all(imgs.map(async i=>{i.loading='eager';await i.decode().catch(()=>{})})));
   m.scenes.push(...(await inspect(page)).scenes);
   if(v.name!=='small-phone'){
    const scenes=page.locator(`#${id} .scene`);
    for(let i=0;i<await scenes.count();i++){await scenes.nth(i).evaluate(el=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY));await page.waitForTimeout(120);await capture(page,`${v.name}-${id}-scene-${i}`);}
   }
  }
  errors.push(...checkComposition(m).map(e=>v.name+': '+e));measurements.push(m);
  await page.close();
  const ref=await browser.newPage({viewport:{width:v.width,height:v.height}});
  await ref.goto(process.env.ATLAS_BENCHMARK_URL||grammar.canonical_url,{waitUntil:'networkidle'});
  const film=await ref.locator('video').evaluate(el=>({source:el.currentSrc,duration:el.duration,ready:el.readyState}));
  if(!film.source||film.ready<2)errors.push(v.name+': canonical film unavailable');
  await capture(ref,`benchmark-${v.name}-opening`);
  if(await ref.locator('.skip-film').isVisible())await ref.locator('.skip-film').click();
  await ref.locator('.edition-geo-bg').evaluate(e=>e.decode());await ref.evaluate(()=>scrollTo(0,0));await ref.waitForTimeout(1000);await capture(ref,`benchmark-${v.name}-identity`);
  await ref.locator('.enter').click();await ref.waitForTimeout(600);await capture(ref,`benchmark-${v.name}-menu`);
  const links=await ref.locator('[data-perspective]').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
  for(const [i,href]of links.entries()){
   await ref.locator(`[data-perspective][href="${href}"]`).click();
   const scene=ref.locator(`${href} .scene`).first();await scene.locator('img').evaluate(el=>el.decode());
   await scene.evaluate(el=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY));await ref.waitForTimeout(500);
   if(v.name!=='small-phone')await capture(ref,`benchmark-${v.name}-route-${i}`);
   canonical.push({device:v.name,route:href,...await scene.evaluate(el=>{const r=el.getBoundingClientRect(),h=getComputedStyle(el.querySelector('h2'));return {width:r.width,height:r.height,heading:h.fontSize}})});
  }
  await ref.close();
 }
 return {version:grammar.version,status:errors.length?'BLOCKED':'PASS',errors,measurements,motion,canonical};
}
async function inspectOpening(page){return page.evaluate(()=>{
 const hero=document.querySelector('.hero'),v=hero?.querySelector('video'),seq=hero?.querySelector('.opening-sequence'),frames=[...seq?.querySelectorAll('img')||[]],first=frames[0],cs=first&&getComputedStyle(first);
 return {mode:hero?.dataset.openingMode||'missing',ready:v?.readyState||0,duration:v?.duration||0,time:v?.currentTime||0,muted:v?.muted,inline:v?.playsInline,frameCount:frames.length,frameOpacities:frames.map(i=>+getComputedStyle(i).opacity),brokenImages:frames.some(i=>!i.complete||!i.naturalWidth),cover:frames.every(i=>getComputedStyle(i).objectFit==='cover'&&i.getBoundingClientRect().width>=innerWidth*.98&&i.getBoundingClientRect().height>=innerHeight*.98),running:!!first&&cs.animationName!=='none'&&cs.animationPlayState==='running',transform:cs?.transform,opacity:cs?.opacity,copyOpacity:+getComputedStyle(hero.querySelector('.hero-copy')).opacity};
 });}
module.exports={audit,inspect,inspectOpening,checkComposition,grammar};
