import {mountSearch} from './panel.mjs?v=20261105-highlighting2';
import {download} from './download.mjs?v=20261105-highlighting2';
import {loadPassages} from './index-loader.mjs?v=20261105-highlighting2';
import {rank} from './ranking.mjs?v=20261105-highlighting2';
const root=document.querySelector('[data-sidebar-search]');
if(root){
 const siteBase=new URL('../',import.meta.url);
 const manifestURL=root.dataset.semanticIndexUrl||new URL('semantic-indexes/archived-technical-blog/manifest.json',siteBase).href;
 let index;
 const textSearch=async query=>{
  index ||= (async()=>{const manifest=await download(manifestURL,{json:true});return loadPassages(manifest,new URL('./',new URL(manifestURL,location.href)));})().catch(error=>{index=null;throw error;});
  return rank(await index,query,null,30).map(p=>({...p,url:new URL(p.url,siteBase).href,description:[root.dataset.semanticScopeLabel,p.heading,p.text.slice(0,220)].filter(Boolean).join(' · ')}));
 };
 mountSearch({root,input:root.querySelector('[data-search-input]'),status:root.querySelector('[data-search-status]'),results:root.querySelector('[data-search-results]'),manifestURL,textSearch,label:root.dataset.semanticScopeLabel||'',noun:'pages'});
}
