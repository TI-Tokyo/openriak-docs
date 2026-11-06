import {chromium} from 'playwright';import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE,headless:true});
const base='http://localhost:1410/docs/';
try{
 for(const [section,path,query] of [['settings','settings/search/','font'],['archived-mailing-list','archived-mailing-list/','node'],['openriak-kv','openriak-kv/3.4.1/','quorum']]){
  const context=await browser.newContext();await context.addInitScript(section=>localStorage.setItem('openriak-docs-search:'+section,JSON.stringify({text:true,semantic:false,timing:'together'})),section);
  let release;const gate=new Promise(resolve=>release=resolve);

  const page=await context.newPage();await page.goto(base+path);await page.locator('[data-search-input]').fill(query);
  const panel=page.locator('.search-results'),status=page.locator('.search-status-panel');
  await panel.locator('[data-search-items] a').first().waitFor();
  await context.route('**/manifest.json',async route=>{await gate;await route.continue();});
  await page.evaluate(()=>{window.hiddenChanges=[];new MutationObserver(records=>{for(const record of records)window.hiddenChanges.push({old:record.oldValue,hidden:record.target.hidden});}).observe(document.querySelector('.search-results'),{attributes:true,attributeFilter:['hidden'],attributeOldValue:true});});
  const before=page.url();await status.getByRole('button',{name:'Turn on semantic search'}).click();
  await page.waitForTimeout(400);
  console.log(section,'visible:',await panel.isVisible(),'url:',page.url(),'transitions:',await page.evaluate(()=>hiddenChanges));
  assert.equal(page.url(),before);assert.equal(await panel.isVisible(),true);
  assert.ok(await page.locator('[data-search-input]').evaluate(node=>node===document.activeElement));
  assert.deepEqual(await page.evaluate(()=>hiddenChanges.filter(change=>change.hidden)),[]);release();
  await page.waitForFunction(()=>document.querySelector('.search-status-panel').textContent.startsWith('Semantic + text search'),{},{timeout:180000});
  assert.equal(await panel.isVisible(),true);await context.close();
 }
 console.log('PASS enabling semantic keeps panel visible without navigation');
}finally{await browser.close();}
