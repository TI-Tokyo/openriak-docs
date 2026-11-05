(() => {
 const lines=element=>{
  if(!element.querySelector('[data-search-text-status]')){
   const text=document.createElement('span'),semantic=document.createElement('span');
   text.dataset.searchTextStatus='';semantic.dataset.searchSemanticStatus='';
   element.replaceChildren(text,document.createTextNode('\n'),semantic);
  }
  return [element.querySelector('[data-search-text-status]'),element.querySelector('[data-search-semantic-status]')];
 };
 const put=(element,index,value)=>{const line=lines(element)[index];line.textContent=value;line.title=value;};
 window.OpenRiakSearchStatus={
  text:(element,value)=>put(element,0,value),
  semantic:(element,value)=>put(element,1,value),
  current:element=>lines(element)[1].textContent,
  complete:(element,count)=>{put(element,0,'Semantic + text search');put(element,1,count);},
  unavailable:element=>put(element,1,'Semantic search unavailable — using text results.'),
  clear:element=>{put(element,0,'');put(element,1,'');}
 };
})();
