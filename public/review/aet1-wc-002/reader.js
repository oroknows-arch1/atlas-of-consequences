// Atlas reader grammar v1. Content topology is supplied by the edition, never fixed here.
(() => {
 const views=[...document.querySelectorAll('[data-view]')], hero=document.querySelector('.hero');
 const video=hero?.querySelector('video'), sequence=hero?.querySelector('.opening-sequence'), skip=hero?.querySelector('.skip-film'), play=hero?.querySelector('.play-film');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
 let sequenceTimer;
 function reveal(reason){clearTimeout(sequenceTimer);hero?.classList.add('film-complete');if(hero)hero.dataset.openingState=reason;video?.pause();if(play)play.hidden=true;}
 skip?.addEventListener('click',()=>reveal('skipped'));
 if(video){
  video.addEventListener('ended',()=>reveal('ended'));
  video.addEventListener('error',()=>{reveal('error');const n=hero.querySelector('.media-notice');n.hidden=false;n.textContent='The opening film could not load. You can continue reading.'});
  play?.addEventListener('click',()=>video.play().then(()=>{play.hidden=true}).catch(()=>{}));
  if(reduced)reveal('reduced-motion');else video.play().catch(()=>{play.hidden=false;hero.dataset.openingState='tap-to-play'});
 }else if(sequence){
  if(reduced)reveal('reduced-motion');else sequenceTimer=setTimeout(()=>reveal('completed'),8000);
 }else reveal('missing-media');
 function navigate(){
  let id;try{id=decodeURIComponent(location.hash.slice(1))||'edition'}catch{id='edition'}
  const target=document.getElementById(id)||document.getElementById('edition'), view=target.closest('[data-view]');
  if(!view)return;
  views.forEach(v=>{v.hidden=v!==view;v.classList.remove('view-enter')});
  view.classList.add('view-enter');if(target.tagName==='DETAILS')target.open=true;
  if(view.id!=='edition'&&!hero?.classList.contains('film-complete'))reveal('navigation');
  requestAnimationFrame(()=>{target.scrollIntoView({behavior:'instant',block:'start'});const heading=view.querySelector('h1,h2');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true})}});
 }
 const incoming=new URLSearchParams(location.search).get('perspective');
 const entry=[...document.querySelectorAll('[data-perspective]')].find(a=>a.dataset.perspective===incoming);
 if(entry){entry.classList.add('incoming-perspective');const m=document.createElement('span');m.className='incoming-marker';m.textContent='Connected to what brought you here';entry.querySelector('.perspective-copy').prepend(m)}
 addEventListener('hashchange',navigate);navigate();
})();
