import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import assert from 'node:assert/strict';import {chromium} from 'playwright';
const roots=['content/static','layouts/common-docs/static','layouts/docs-theme/static','content/static/common','content/static/archive-mailing-list','content/static/archived-technical-blog','tools/generated/semantic-render/panels','build/archives'];
const server=http.createServer((req,res)=>{
 let name=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/docs\//,'');if(name.includes('..')){res.writeHead(400).end();return;}if(name.endsWith('/'))name+='index.html';
 const file=roots.map(root=>path.join(root,name)).find(f=>fs.existsSync(f)&&fs.statSync(f).isFile());if(!file){res.writeHead(404).end();return;}
 res.writeHead(200,{'Content-Type':({'.js':'text/javascript','.mjs':'text/javascript','.json':'application/json','.html':'text/html','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.wasm':'application/wasm'})[path.extname(file)]||'application/octet-stream','Content-Length':fs.statSync(file).size});fs.createReadStream(file).pipe(res);
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}/docs/`;
const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE,headless:true});
try{
 const context=await browser.newContext(),page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'settings/search/');
 await page.locator('[data-search-section="settings"]').waitFor();
 assert.equal(await page.locator('[data-search-section]').count(),7);assert.equal(await page.locator('[data-search-section="homepage"]').count(),0);
 assert.equal(await page.locator('[data-search-section] input:checked').count(),21);
 assert.ok(await page.locator('[data-search-section] img').evaluateAll(images=>images.every(img=>img.complete&&img.naturalWidth>0)));
 const identities=await page.locator('[data-search-section]').evaluateAll(rows=>rows.map(row=>{
   const id=row.dataset.searchSection;
   const menu=document.querySelector(id==='settings'?'.site-section-panel [data-settings-link]':`.site-section-panel [data-site-section-id="${id}"]`);
   return row.querySelector('.settings-search-identity').innerHTML===menu.innerHTML;
 }));assert.ok(identities.every(Boolean),'table must reuse the menu identities');
 const community=page.locator('[data-search-section="community"]');
 const tableTop=(await page.locator('.settings-search-table').boundingBox()).y;
 await community.locator('input').first().uncheck();
 await page.waitForTimeout(1100);
 await community.locator('select').selectOption('together');
 const notices=page.locator('[data-settings-status] .settings-notice');
 assert.equal(await notices.count(),2);
 assert.equal((await page.locator('.settings-search-table').boundingBox()).y,tableTop);
 assert.equal(await page.locator('[data-settings-status]').evaluate(el=>el.nextElementSibling.textContent),'Reset Search');
 assert.equal(await notices.first().evaluate(el=>getComputedStyle(el).transitionDuration),'0.5s');
 await page.waitForFunction(()=>document.querySelector('.settings-notice')?.classList.contains('is-fading'));
 assert.equal(await notices.count(),2);assert.equal(await notices.last().evaluate(el=>el.classList.contains('is-fading')),false);
 await page.waitForFunction(()=>document.querySelectorAll('.settings-notice').length===1);
 await page.waitForFunction(()=>document.querySelectorAll('.settings-notice').length===0);
 await page.reload();
 assert.equal(await community.locator('input').first().isChecked(),false);assert.equal(await community.locator('select').inputValue(),'together');
 let downloads=0;page.on('request',r=>{if(/manifest.json|\.bin$|model_quantized/.test(r.url()))downloads++;});
 await page.evaluate(()=>OpenRiakSearchPreferences.write('settings',{text:false,semantic:false}));
 const input=page.locator('[data-settings-search]'),status=page.locator('[data-settings-search-status]'),results=page.locator('[data-settings-results]');
 await input.fill('font');await page.waitForTimeout(400);
 assert.equal(await results.locator('[data-search-items] button').count(),3);assert.equal(downloads,0);
 assert.equal(await status.getByRole('button').count(),2);
 await results.getByRole('button',{name:'Text search',exact:true}).click();
 await page.waitForFunction(()=>document.querySelector('[data-settings-search-status]').textContent.includes('Text search ·'));
 assert.ok(await results.locator('[data-search-items] a').count());assert.equal(downloads,0);
 assert.ok(await results.locator('[data-search-items] mark.search-highlight').count());
 const highlightedHref=await results.locator('[data-search-items] a').first().getAttribute('href');
 assert.ok(new URL(highlightedHref).searchParams.has('highlight'));
 const destination=await context.newPage();await destination.goto(highlightedHref);
 await destination.locator('[data-search-highlight-root] mark.search-highlight').first().waitFor();
 assert.equal((await destination.locator('[data-search-highlight-root] mark.search-highlight').first().textContent()).toLowerCase(),'font');
 await destination.locator('.search-highlight-clear').click();assert.equal(await destination.locator('mark.search-highlight').count(),0);await destination.close();

 const highlightToggle=page.locator('[data-search-section="settings"] input[aria-label="Settings: result highlighting"]');
 await highlightToggle.uncheck();
 await page.waitForFunction(()=>document.querySelector('[data-settings-results] [data-search-items] a')&&!document.querySelector('[data-settings-results] [data-search-items] mark'));
 assert.equal(new URL(await results.locator('[data-search-items] a').first().getAttribute('href')).searchParams.has('highlight'),false);
 assert.equal(await page.evaluate(()=>OpenRiakSearchPreferences.read('community').highlight),true);
 await highlightToggle.check();
 await page.locator('[data-settings-results] mark.search-highlight').first().waitFor();

 assert.equal(await status.getByRole('button',{name:'Turn on semantic search'}).count(),1);
 let release;const gate=new Promise(r=>release=r);
 await context.route('**/model_quantized.onnx',async route=>{await gate;await route.continue();});
 await page.evaluate(()=>OpenRiakSearchPreferences.write('settings',{text:true,semantic:true,timing:'together'}));
 await page.waitForFunction(()=>document.querySelector('[data-settings-search-status]').textContent.includes('semantic model'),{},{timeout:60000});
 assert.equal(await results.locator('[data-search-items]').isVisible(),false);assert.equal(await results.isVisible(),true);assert.match(await status.locator('[data-search-text-status]').innerText(),/Text search ·/);
 release();await page.waitForFunction(()=>document.querySelector('[data-settings-search-status]').textContent.startsWith('Semantic + text search'),{},{timeout:60000});assert.ok(await results.isVisible());
 await page.evaluate(()=>OpenRiakSearchPreferences.write('settings',{text:false,semantic:true}));
 await page.waitForFunction(()=>document.querySelector('[data-settings-search-status]').textContent.includes('Semantic search ·'));
 assert.equal(await status.getByRole('button',{name:'Turn on text search'}).count(),1);assert.ok(await results.locator('[data-search-items] a').count());
 await status.getByRole('button',{name:'Turn on text search'}).click();
 await page.waitForFunction(()=>document.querySelector('[data-settings-search-status]').textContent.startsWith('Semantic + text search'));
 for(const [choice,expected] of [['Semantic search','Semantic search ·'],['Text + semantic search','Semantic + text search']]){
  await page.evaluate(()=>OpenRiakSearchPreferences.write('settings',{text:false,semantic:false}));
  await results.getByRole('button',{name:choice,exact:true}).click();
  await page.waitForFunction(expected=>document.querySelector('[data-settings-search-status]').textContent.includes(expected),expected,{timeout:60000});
 }
 assert.equal(await page.evaluate(()=>OpenRiakSearchPreferences.read('openriak-kv').text),true);
 const snapshot=await page.evaluate(()=>OpenRiakSettings.snapshot(['search']));assert.ok(snapshot.settings['openriak-docs-search:settings']);
 await page.evaluate(()=>sessionStorage.setItem('openriak-docs-settings-return-context',JSON.stringify({url:location.origin+'/docs/openriak-kv/3.4.1/',project:'OpenRiak KV',version:'3.4.1',title:'OpenRiak KV 3.4.1'})));
 for(const group of ['','appearance/','code/','platform/','tables/','search/','examples/','advanced/','transfer/']){
   await page.goto(base+'settings/'+group);
   assert.equal(await page.locator('[data-settings-return]').textContent(),'Return to documentation (OpenRiak KV 3.4.1)');
   const noticeArea=page.locator('[data-settings-status]');
   await page.waitForFunction(()=>document.querySelector('[data-settings-status]')?.parentElement.matches('section, .settings-clear-area'));
   assert.equal(await noticeArea.count(),1);
   assert.equal(await noticeArea.evaluate(node=>node.parentElement.matches('section, .settings-clear-area')),true);
   const headingTop=await page.locator('h1').evaluate(node=>node.getBoundingClientRect().top+scrollY);
   if(group==='appearance/')await page.locator('[data-settings-page]').getByLabel('Colour theme',{exact:true}).selectOption('dark');
   else if(group==='code/')await page.getByLabel('Line Numbers for DEFAULT',{exact:true}).selectOption('true');
   else if(group==='platform/')await page.getByLabel('Default documentation version for OpenRiak KV',{exact:true}).selectOption('3.4.1');
   else if(group==='tables/')await page.getByLabel('Configuration search mode',{exact:true}).selectOption('regex');
   else if(group==='search/'){
     const toggle=page.locator('[data-search-section="community"] input').first();
     await toggle.setChecked(!await toggle.isChecked());
   }
   else if(group==='examples/'){
     await page.getByRole('button',{name:'Add cluster',exact:true}).click();
     await page.getByRole('button',{name:'Add cluster',exact:true}).click();
     assert.equal(await noticeArea.locator('.settings-notice').count(),2,'notices survive rebuilding controls');
   }
   else if(group==='advanced/')await page.getByRole('switch',{name:'Show internal configuration settings'}).check();
   else if(group==='transfer/'){
     page.once('dialog',dialog=>dialog.accept());
     await page.getByRole('button',{name:'Reset all settings',exact:true}).click();
   }else{
     await page.locator('[data-settings-clear]').click();
     await page.getByRole('dialog').getByRole('button',{name:'Clear all',exact:true}).click();
   }
   await noticeArea.locator('.settings-notice').first().waitFor({state:'attached'});
   assert.ok(await noticeArea.locator('.settings-notice').count()>0,`bottom notice for ${group||'overview'}`);
   assert.equal(await page.locator('h1').evaluate(node=>node.getBoundingClientRect().top+scrollY),headingTop);
   assert.equal(await noticeArea.locator('.settings-notice').first().evaluate(node=>getComputedStyle(node).transitionDuration),'0.5s');
   if(group!=='code/')assert.equal(await noticeArea.evaluate(node=>node.nextElementSibling?.matches('[data-settings-reset], [data-settings-clear]')),true);
   else assert.equal(await noticeArea.evaluate(node=>!node.nextElementSibling),true);
 }
 await page.evaluate(()=>sessionStorage.setItem('openriak-docs-settings-return-context',JSON.stringify({url:location.origin+'/docs/openriak-kv/3.4.1/using/',project:'OpenRiak KV',version:'3.4.1',title:'Using OpenRiak KV'})));
 await page.goto(base+'settings/search/');assert.equal(await page.locator('[data-settings-return]').textContent(),'Return to documentation (OpenRiak KV 3.4.1: Using OpenRiak KV)');

 assert.deepEqual(errors,[]);console.log('PASS All Settings bottom notices, Search table/defaults/logos, persistence, disabled links/choices, no disabled downloads, text-only, semantic-only and wait-for-both');
}finally{await browser.close();server.close();}
