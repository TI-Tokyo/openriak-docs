(() => {
  'use strict';
  const upgradeThreadIndex = () => {
    const oldIndex = document.querySelector('nav.mailing-list-toc');
    if (!oldIndex) return;
    [...oldIndex.querySelectorAll('ol')].reverse().forEach((orderedList) => {
      const list = document.createElement('ul');
      list.append(...orderedList.childNodes);
      orderedList.replaceWith(list);
    });
    oldIndex.querySelector('h2')?.remove();
    const disclosure = document.createElement('details');
    disclosure.className = 'mailing-list-toc';
    const summary = document.createElement('summary');
    summary.textContent = 'In this thread';
    oldIndex.replaceWith(disclosure);
    oldIndex.className = '';
    disclosure.append(summary, oldIndex);
  };
  const expandReply = (target, scroll = true) => {
    if (!target) return;
    for (let element = target; element; element = element.parentElement) {
      if (element instanceof HTMLDetailsElement) element.open = true;
    }
    if (scroll) window.requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  };
  const revealHashReply = () => {
    if (window.location.hash.length < 2) return;
    let id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch { return; }
    expandReply(document.getElementById(id));
  };
  upgradeThreadIndex();
  document.addEventListener('click', (event) => {
    const link = event.target.closest('.mailing-list-toc a[href^="#"]');
    if (!link) return;
    expandReply(document.getElementById(link.getAttribute('href').slice(1)), false);
  });
  window.addEventListener('hashchange', revealHashReply);
  revealHashReply();
})();

(() => {
 const normalize=value=>String(value||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 document.querySelectorAll('[data-mailing-list-search]').forEach(root=>{
  let index;
  const textSearch=async query=>{
   index ||= fetch(root.dataset.indexUrl).then(r=>{if(!r.ok)throw Error('Text index unavailable');return r.json();}).then(items=>items.map(item=>({...item,titleText:normalize(item.title),authorText:normalize(item.authors||item.author),contentText:normalize(item.content)}))).catch(error=>{index=null;throw error;});
   const terms=normalize(query).split(/\s+/).filter(Boolean),matches=[];
   for(const item of await index){
    if(!terms.every(term=>`${item.titleText} ${item.authorText} ${item.contentText}`.includes(term)))continue;
    let score=0;for(const term of terms)score+=(item.titleText.includes(term)?8:0)+(item.authorText.includes(term)?4:0)+(item.contentText.includes(term)?1:0);
    matches.push({item,score});
   }
   matches.sort((a,b)=>b.score-a.score||b.item.date.localeCompare(a.item.date)||a.item.title.localeCompare(b.item.title));
   return matches.slice(0,30).map(({item})=>{
    const url=new URL(item.url,new URL(root.dataset.indexUrl,location.href));
    // Search highlighting remains available on text results.
    query.split(/\s+/).filter(Boolean).slice(0,8).forEach(term=>url.searchParams.append('highlight', term));
    return {url:url.href,title:item.title,description:[item.author,item.date].filter(Boolean).join(' · ')};
   });
  };
  import(root.dataset.searchPanelUrl).then(({mountSearch})=>mountSearch({root,input:root.querySelector('[data-mailing-list-search-input]'),status:root.querySelector('[data-mailing-list-search-status]'),results:root.querySelector('[data-mailing-list-search-results]'),manifestURL:root.dataset.semanticIndexUrl,textSearch,noun:'conversations'}));
 });
})();
