#!/usr/bin/env node
// Inspect the real deployed route at phone and desktop sizes, after deployment.
const fs=require('fs');
const {chromium}=require('playwright');
const [url, receiptPath, screenshotDir]=process.argv.slice(2);
if(!url || !receiptPath || !screenshotDir) {console.error('usage: node rendered_qa.cjs <deployed-url> <receipt> <screenshots>');process.exit(2)}
(async()=>{
  const errors=[], observations=[];
  const browser=await chromium.launch({headless:true});
  fs.mkdirSync(screenshotDir,{recursive:true});
  for(const config of [{name:'phone',width:390,height:844},{name:'desktop',width:1440,height:900}]){
    const page=await browser.newPage({viewport:{width:config.width,height:config.height},deviceScaleFactor:1});
    page.on('pageerror',error=>errors.push(`${config.name}: ${error.message}`));
    page.on('response',response=>{if(response.status()>=400 && new URL(response.url()).origin===new URL(url).origin)errors.push(`${config.name}: HTTP ${response.status()} ${response.url()}`)});
    const response=await page.goto(url,{waitUntil:'networkidle',timeout:60000});
    if(!response || !response.ok()) errors.push(`${config.name}: page unavailable`);
    const checks=await page.evaluate(()=>{
      const images=[...document.images];
      const links=[...document.querySelectorAll('a[href^="#"]')];
      const brokenAnchors=links.filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash);
      const overflow=[...document.querySelectorAll('body *')].filter(el=>el.getBoundingClientRect().right>innerWidth+2).slice(0,8).map(el=>el.tagName+'.'+el.className);
      return {brokenImages:images.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src), imageCount:images.length,
        routes:document.querySelectorAll('.route').length, cards:document.querySelectorAll('.cards a').length,
        brokenAnchors,overflow,fiction:document.querySelector('.story .boundary')?.textContent||'',sources:document.querySelectorAll('.sources details a[href^="https://"]').length,
        placeholder:/placeholder|pending image|lorem ipsum/i.test(document.body.innerText),scrollWidth:document.documentElement.scrollWidth};
    });
    for(const [key,values] of [['broken images',checks.brokenImages],['broken anchors',checks.brokenAnchors],['horizontal overflow',checks.overflow]])if(values.length)errors.push(`${config.name}: ${key}: ${values.join(', ')}`);
    if(checks.routes<1||checks.routes!==checks.cards)errors.push(`${config.name}: route/card mismatch`);
    if(!checks.fiction.includes('invented'))errors.push(`${config.name}: fiction boundary missing`);
    if(!checks.sources)errors.push(`${config.name}: sources inaccessible`);
    if(checks.placeholder)errors.push(`${config.name}: placeholder text visible`);
    await page.screenshot({path:`${screenshotDir}/${config.name}.png`,fullPage:true});
    observations.push({device:config.name,...checks,screenshot:`${screenshotDir}/${config.name}.png`});
    await page.close();
  }
  if(process.env.ATLAS_BENCHMARK_URL){
    const page=await browser.newPage({viewport:{width:390,height:844}});
    const response=await page.goto(process.env.ATLAS_BENCHMARK_URL,{waitUntil:'networkidle',timeout:60000});
    if(!response || !response.ok())errors.push('AOC-001 benchmark page unavailable');
    else await page.screenshot({path:`${screenshotDir}/benchmark-phone.png`,fullPage:true});
    await page.close();
  }
  await browser.close();
  const receipt={url,status:errors.length?'BLOCKED':'PASS',errors,observations,
    note:'Screenshot visual review is a separate mandatory gate; automated DOM checks cannot judge crop, contextuality, continuity or uniformity.'};
  fs.writeFileSync(receiptPath,JSON.stringify(receipt,null,2)+'\n');
  console.log(JSON.stringify(receipt,null,2));
  process.exit(errors.length?1:0);
})().catch(error=>{console.error(error);process.exit(1)});
