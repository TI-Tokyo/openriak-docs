#!/usr/bin/env node
// Render the existing section branding to raster cards. No logo redrawing.
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {spawnSync}=require('node:child_process');
const repo=path.resolve(__dirname,'../..');
const sections=JSON.parse(fs.readFileSync(path.join(repo,'layouts/common-docs/data/site_sections.json'),'utf8'));
const settings=fs.readFileSync(path.join(repo,'layouts/common-docs/layouts/site-section/settings.html'),'utf8');
sections.push({id:'settings',name:'Settings',pickerIcon:'settings',description:settings.match(/<p>(Preferences[^<]+)<\/p>/)[1]});
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const manifest={};
for(const section of sections){
 const image=`images/${section.id}-social-preview.png`;
 manifest[section.id]={image,name:section.name,description:section.description};
 let logo;
 if(section.pickerIcon==='openriak')logo=`<img class="wordmark" src="../../content/static/common/${section.logo}" alt="${escape(section.name)}">`;
 else logo=`<img class="wordmark" src="../../content/static/common/images/branding/openriak-project.png" alt="OpenRiak"><h1>${escape(section.name)}</h1>`;

 const html=`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>${escape(section.name)} social preview artwork</title><style>
*{box-sizing:border-box}html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#f3f6f8;color:#17222b;font-family:Arial,sans-serif;border-top:12px solid #f99d35;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:58px;padding:80px}
.wordmark{display:block;width:840px;height:auto}
p{margin:0;color:#56656f;font-size:34px;line-height:1.4;text-align:center;max-width:1000px}
body.section-card{gap:24px}.section-card .wordmark{width:840px;height:250px;object-fit:contain}.section-card h1{font-size:44px;line-height:1.15;margin:0;font-weight:600;text-align:center}.section-card p{font-size:30px}

</style></head><body${section.pickerIcon==='openriak'?'':' class="section-card"'}>
${logo}<p>${escape(section.description)}</p>
</body></html>\n`;
 const artwork=path.join(repo,'tools/assets',`${section.id}-social-preview.html`);
 fs.writeFileSync(artwork,html);
 if(!process.argv.includes('--source-only')){
  const chrome=process.env.OPENRIAK_BROWSER_EXECUTABLE;
  if(!chrome)throw Error('Set OPENRIAK_BROWSER_EXECUTABLE to Chromium, or use --source-only.');
  const result=spawnSync(chrome,['--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1200,630','--virtual-time-budget=1000',`--screenshot=${path.join(repo,'content/static/common',image)}`,pathToFileURL(artwork).href],{encoding:'utf8'});
  if(result.status!==0)throw Error(result.stderr||'Chromium render failed');
 }
}
fs.writeFileSync(path.join(repo,'layouts/common-docs/data/social_previews.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(`Generated ${sections.length} section social previews${process.argv.includes('--source-only')?' (artwork only)':''}.`);
