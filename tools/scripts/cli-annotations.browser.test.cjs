'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.OPENRIAK_BROWSER_EXECUTABLE});
 try {
  const context=await browser.newContext({permissions:['clipboard-read','clipboard-write']});
  const page=await context.newPage();
  const root=process.env.OPENRIAK_DOCS_TEST_URL || 'http://localhost:1410/docs/openriak-kv/';
  for(const version of ['3.4.0','3.4.1']){
   for(const route of ['riak/admin/describe','riak/admin/member-status','riak/admin','erlang/riak-client/get']){
    assert.equal((await page.goto(`${root}${version}/reference/commands/${route}/`)).status(),200);
    for(const id of ['syntax','arguments-and-options','description','notes','examples','errors','help'])assert.equal(await page.locator('#'+id).count(),1,route+' '+id);
    assert.ok(await page.locator('.cli-observed').count()>=1);
    const cards=page.locator('.cli-example');
    assert.match(await cards.first().locator('h3').innerText(),/Example 1: .+/);
    assert.equal(await cards.first().evaluate(e=>getComputedStyle(e).borderTopStyle),'solid');
    assert.equal(await page.locator('.doc-article > h1').evaluate(e=>getComputedStyle(e).borderLeftWidth),'0px');
    const headers=await page.locator('.cli-table-scroll th').evaluateAll(es=>es.map(e=>getComputedStyle(e).textAlign));
    assert.ok(headers.every(h=>h==='left'));
    const headingOrder=await page.locator('.cli-command-reference > h2').evaluateAll(es=>es.map(e=>e.textContent));
    assert.deepEqual(headingOrder,['Syntax','Arguments and options','Description','Notes','Examples','Errors','Help text']);
    const headings=await page.locator('.cli-command-reference h2[id], .cli-command-reference h3[id]').evaluateAll(es=>es.map(e=>({id:e.id,title:e.textContent.trim()})));
    const toc=page.locator('.doc-table-of-contents');
    await toc.locator('summary').click();
    for(const h of headings){const link=toc.locator(`a[href="#${h.id}"]`);assert.equal(await link.count(),1,h.id);assert.equal(await link.innerText(),h.title);}
    assert.equal(await toc.locator('a[href="#related-documentation-heading"]').count(),1);
    const dates=await page.locator('.cli-observed time').evaluateAll(es=>es.map(e=>e.textContent));
    assert.ok(dates.every(d=>/^\d{4}-\d{2}-\d{2}$/.test(d)));
    if(route.endsWith('/describe')){
     const format=page.locator('.cli-parameters tr').filter({has:page.locator('td:first-child code', {hasText:'--format'})});
     assert.equal(await format.count(),1);
     assert.deepEqual(await format.locator('.cli-parameter-tag').allTextContents(),['Optional','Not repeatable']);
     assert.equal((await format.locator('td').nth(2).innerText()).trim(),'human');
     assert.deepEqual(await format.locator('.cli-valid-values code').allTextContents(),['csv','human','json']);
     const copy=format.locator('[data-copy-value="json"]');await copy.click();assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'json');
     assert.ok(await format.locator('td:last-child p').count()>=2);
     const arg=page.locator('.cli-parameters tr').filter({hasText:'variable'});
     assert.deepEqual(await arg.locator('.cli-parameter-tag').allTextContents(),['Required','Repeatable']);
     assert.equal(await format.locator('.cli-parameter-kind--option').innerText(),'Option');
     assert.equal(await arg.locator('.cli-parameter-kind--argument').innerText(),'Argument');
     assert.notEqual(await format.locator('.cli-parameter-kind').evaluate(e=>getComputedStyle(e).color),await arg.locator('.cli-parameter-kind').evaluate(e=>getComputedStyle(e).color));
     const help=page.locator('.cli-parameters tr').filter({has:page.locator('td:first-child code',{hasText:'--help'})});
     assert.match(await help.locator('td').nth(1).innerText(),/flag \(no value\)/);
     assert.equal(await help.locator('td').nth(1).locator('code, button').count(),0);
     assert.equal(await arg.locator('td').nth(1).locator('code, button').count(),0);
     for(const [row,name] of [[format,'--format'],[arg,'variable'],[help,'-h']]){
      await row.locator(`td:first-child [data-copy-value="${name}"]`).click();
      assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),name);
     }
     assert.match(await cards.nth(2).locator('h3').innerText(),/Example 3: As JSON/);
     for(const id of ['format-json','format-csv','help','invalid-format']){
      const example=page.locator(`[data-cli-example-id="describe:${id}"]`);
      await example.locator('.cli-observed > summary').click();
      assert.match(await example.innerText(),/exit status 0/);
      if(id==='format-json')assert.match(await example.innerText(),/"type":"text"/);
     }
     for(const link of await page.locator('.related-documentation a').all()){
      const url=new URL(await link.getAttribute('href'),page.url()).href;
      assert.equal((await page.request.get(url)).status(),200,url);
     }
    }
    if(route==='riak/admin/member-status'){
     assert.equal(await cards.count(),1);assert.doesNotMatch(await page.locator('.cli-command-reference').innerText(),/RELX_COOKIE=wrong-reference-cookie/);
     assert.equal(await page.locator('.cli-command-reference a[href$="/riak/admin/#errors"]').count(),1);
    }
    if(route==='riak/admin'){
     assert.equal(await page.locator('[data-cli-example-id="admin:wrong-cookie"]').count(),1);
     const syntax=page.locator('.cli-generated-syntax').first();
     assert.match(await syntax.innerText(),/riak admin \{.*describe.*\}/s);
     const links=syntax.locator('a');assert.ok(await links.count()>20);
     const hrefs=await links.evaluateAll(es=>es.map(e=>e.href));
     assert.ok(hrefs.every(h=>h.includes(`/openriak-kv/${version}/reference/commands/riak/admin/`)&&!h.endsWith(`/riak/admin/`)));
     for(const href of hrefs)assert.equal((await page.request.get(href)).status(),200,href);
     assert.equal(await syntax.locator('a[href$="/node/"]').count(),version==='3.4.1'?1:0);
     await page.locator('.cli-syntax-copy').first().click();
     assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),await syntax.innerText());
    }
    await page.locator('.cli-sources > summary').click();
    if(route==='riak/admin'){
     const review=page.locator('.cli-syntax-review');await review.locator('summary').click();
     assert.match(await review.innerText(),/Supplied alternatives absent.*diag/);
     assert.match(await review.innerText(),/Discovered subcommands missing.*remove/);
    }
    const evidence=page.locator('.cli-sources details').filter({has:page.locator('summary', {hasText:'Original scenario evidence'})});await evidence.locator('summary').click();
    const proof=JSON.parse(await evidence.locator('pre code').first().innerText());
    assert.ok(proof.every(e=>e.verification.image_id.startsWith('sha256:')));
   }
   console.log(version+': page order, Markdown paragraphs, parameter flags, copy buttons, headings, shared errors, dates and evidence passed.');
  }
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
