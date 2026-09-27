#!/usr/bin/env node
// Exercise every reader view in a real browser. Hidden routes are inspected separately.
const fs=require('fs');
const path=require('path');
const crypto=require('crypto');
const {chromium}=require('playwright');
const [url, receiptPath, screenshotDir]=process.argv.slice(2);
(async()=>{
 const errors=[],observations=[],screenshots=[];
 const browser=await chromium.launch({headless:true});
 fs.mkdirSync(screenshotDir,{recursive:true});
 async function capture(page,name){
   const file=path.join(screenshotDir,name+'.png');
   await page.screenshot({path:file,fullPage:true});
   screenshots.push({path:path.relative(path.dirname(receiptPath),file),sha256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')});
 }
 try {
  for(const config of [{name:'phone',width:390,height:844},{name:'small-phone',width:320,height:740},{name:'desktop',width:1440,height:900}]){
   const page=await browser.newPage({viewport:{width:config.width,height:config.height},deviceScaleFactor:1});
   page.on('pageerror',e=>errors.push(`${config.name}: ${e.message}`));
   page.on('response',r=>{if(r.status()>=400 && new URL(r.url()).origin===new URL(url).origin)errors.push(`${config.name}: HTTP ${r.status()} ${r.url()}`)});
   const response=await page.goto(url,{waitUntil:'networkidle',timeout:60000});
   if(!response?.ok())throw Error('review page unavailable');
   const ids=await page.locator('[data-view]').evaluateAll(nodes=>nodes.map(n=>n.id));
   if(!ids.length)throw Error('no reader views');
   const links=await page.locator('a[href^="#"]').evaluateAll(nodes=>nodes.map(a=>a.getAttribute('href')));
   for(const hash of links)if(!await page.locator(`[id="${hash.slice(1)}"]`).count())errors.push('missing destination '+hash);
   for(const id of ids){
    await page.evaluate(id=>{location.hash=id},id);
    await page.waitForFunction(id=>!document.getElementById(id).hidden,id);
    const view=page.locator(`[id="${id}"]`);
    // Force decoding of every visible lazy image before checking or photographing it.
    await view.locator('img').evaluateAll(async images=>{await Promise.all(images.map(async image=>{image.loading='eager';try{await image.decode()}catch{}}))});
    if(id==='sources')await view.locator('details').evaluateAll(nodes=>nodes.forEach(n=>n.open=true));
    const checks=await page.evaluate(id=>{
      const view=document.getElementById(id);
      const visible=[...document.querySelectorAll('[data-view]')].filter(n=>!n.hidden).map(n=>n.id);
      const images=[...view.querySelectorAll('img')];
      return {id,visible,brokenImages:images.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),
        overflow:document.documentElement.scrollWidth>innerWidth+2,
        placeholder:/placeholder|pending image|lorem ipsum/i.test(view.innerText),
        imageCount:images.length};
    },id);
    if(checks.visible.length!==1||checks.visible[0]!==id)errors.push(`${config.name}: route separation ${id}`);
    if(checks.overflow)errors.push(`${config.name}: overflow ${id}`);
    if(checks.brokenImages.length)errors.push(`${config.name}: missing image ${id}: ${checks.brokenImages.join(',')}`);
    if(checks.placeholder)errors.push(`${config.name}: placeholder ${id}`);
    if(id.startsWith('route-')){
      await view.locator('footer').scrollIntoViewIfNeeded();
      if(await page.locator('.route:not([hidden])').count()!==1)errors.push('routes auto-chain');
      await view.locator('footer a[href="#perspectives"]').click();
      await page.waitForFunction(()=>!document.getElementById('perspectives').hidden);
      await page.locator(`.cards a[href="#${id}"]`).click();
      await page.waitForFunction(id=>!document.getElementById(id).hidden,id);
      await page.reload({waitUntil:'networkidle'});
      if(await view.getAttribute('hidden')!==null)errors.push('route reload failed '+id);
      await page.goBack({waitUntil:'networkidle'});
      if(await page.locator('#perspectives').getAttribute('hidden')!==null)errors.push('route back failed '+id);
      await page.goForward({waitUntil:'networkidle'});
    }
    await page.evaluate(()=>scrollTo(0,0));
    if(config.name!=='small-phone')await capture(page,`${config.name}-${id}`);
    observations.push({device:config.name,...checks});
   }
   if(!await page.locator('.story .boundary').textContent().then(t=>/fiction|invented/i.test(t)))errors.push('fiction boundary missing');
   const sourceLink=page.locator('.refs a').first();
   if(await sourceLink.count()){
     const hash=await sourceLink.getAttribute('href');
     await page.evaluate(hash=>{location.hash=hash},hash);
     await page.waitForFunction(hash=>document.getElementById(hash.slice(1)).open,hash);
     if(await page.locator('#sources').getAttribute('hidden')!==null)errors.push('source deep link hidden');
   }
   await page.close();
  }
  if(!process.env.ATLAS_BENCHMARK_URL)errors.push('benchmark URL missing');
  else{
    const page=await browser.newPage({viewport:{width:390,height:844}});
    let r;
    for(let attempt=1;attempt<=5;attempt++){
      try{
        r=await page.goto(process.env.ATLAS_BENCHMARK_URL,{waitUntil:'networkidle',timeout:60000});
        if(r?.status()!==429)break;
      }catch(error){if(attempt===5)throw error}
      const retryAfter=Number(r?.headers()?.['retry-after']||0);
      const delay=Math.min(60000,Math.max(attempt*15000,retryAfter*1000));
      await new Promise(resolve=>setTimeout(resolve,delay));
    }
    if(!r?.ok())throw Error('benchmark unavailable');
    await capture(page,'benchmark-phone');
    const entries=await page.locator('[data-perspective]').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('href')));
    for(const [i,href] of entries.entries()){
      await page.locator(`[data-perspective][href="${href}"]`).first().evaluate(a=>a.click());
      await page.locator(`${href} img`).evaluateAll(async images=>{await Promise.all(images.map(async i=>{i.loading='eager';try{await i.decode()}catch{}}))});
      await capture(page,`benchmark-route-${i}`);
    }
    await page.close();
  }
 }catch(error){errors.push(error.message)}
 finally{await browser.close()}
 fs.writeFileSync(receiptPath,JSON.stringify({url,status:errors.length?'BLOCKED':'PASS',errors,observations,screenshots},null,2)+'\n');
 console.log(JSON.stringify({status:errors.length?'BLOCKED':'PASS',errors,views:observations.length,screenshots:screenshots.length}));
 process.exitCode=errors.length?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
