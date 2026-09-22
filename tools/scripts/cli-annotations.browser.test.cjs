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
   for(const [route,scenario,cases] of [
    ['riak/admin/cluster/plan','shell-riak-admin-cluster-plan',['no-pending-changes','joining-node-wrong-cookie','after-rejected-join','one-join-first-plan','one-join-repeat-plan','five-node-plan','after-five-node-commit']],
    ['riak/admin/cluster/commit','shell-riak-admin-cluster-commit',['no-reviewed-plan','empty-plan','joining-node-wrong-cookie','after-rejected-join','one-join-without-plan','one-join-after-plan','plan-changed','five-node-commit','commit-again']],
    ['riak/admin/transfers','shell-riak-admin-transfers',['before-commit','after-commit-queued','five-nodes-transferring','after-convergence']],
   ]) {
    assert.equal((await page.goto(`${root}${version}/reference/commands/${route}/`)).status(),200);
    for(const id of cases){
     const card=page.locator(`[data-cli-example-id="${scenario}:${id}"]`);
     assert.equal(await card.count(),1,id);
     assert.equal(await card.locator('.cli-test-details').getAttribute('open'),null);
     assert.equal(await card.locator('.cli-prerequisites').isVisible(),false);
     assert.doesNotMatch(await card.innerText(),/\b(fixture|disposable|the test|seeded)\b/i);
     assert.doesNotMatch(await card.innerText(),/VMARGS_PATH=|\/usr\/lib\/riak\/bin\/riak/);
     await card.locator('.cli-observed > summary').click();
     if(id==='five-node-plan'||id==='five-nodes-transferring')for(let n=1;n<=5;n++)assert.ok((await card.locator('.cli-observed').innerText()).includes(`node${n}.test`));
     if(id==='five-nodes-transferring')assert.match(await card.locator('.cli-observed').innerText(),/objects transferred: [1-9]/);
     if(id==='plan-changed')assert.match(await card.locator('.cli-observed').innerText(),/The plan has changed/);
     if(id==='one-join-after-plan'||id==='five-node-commit')assert.match(await card.locator('.cli-observed').innerText(),/Cluster changes committed/);
     await card.locator('.cli-test-details > summary').click();
     assert.match(await card.locator('.cli-test-details').innerText(),/Executed setup, command and verification steps/);
    }
    for(const link of await page.locator('.related-documentation a').all()){
     const url=new URL(await link.getAttribute('href'),page.url()).href;
     assert.equal((await page.request.get(url)).status(),200,url);
    }
   }
   for(const [route,caseId,result] of [
    ['riak/admin/cluster/join','shell-riak-admin-cluster-join:join-another-node','Success'],
    ['riak/admin/bucket-type/update','shell-riak-admin-bucket-type-update:a-named-bucket-type','updated'],
    ['riak/admin/set','shell-riak-admin-set:set-a-transfer-limit','transfer_limit set to "2"'],
    ['riak/admin/security/add-source','shell-riak-admin-security-add-source:a-loopback-client','Successfully added source'],
   ]) {
    assert.equal((await page.goto(`${root}${version}/reference/commands/${route}/`)).status(),200);
    const card=page.locator(`[data-cli-example-id="${caseId}"]`);
    assert.equal(await card.locator('.cli-example-outcome').count(),0,'working example must not be classified as an error');
    assert.match(await card.locator('.doc-code-block').first().innerText(),/riak admin /);
    assert.doesNotMatch(await card.locator('.doc-code-block').first().innerText(),/VMARGS_PATH=|\/usr\/lib\/riak\/bin\/riak/);
    if(route.endsWith('/join')){
     const command='riak admin cluster join openriak-kv@node2.test';
     const block=card.locator('.doc-code-block').first();
     assert.equal((await block.locator('.doc-code-highlight code').innerText()).trim(),command);
     await block.locator('[data-code-copy]').click();
     assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),command);
    }
    await card.locator('.cli-observed > summary').click();
    assert.ok((await card.locator('.cli-observed').innerText()).includes(result));
    const tested=card.locator('.cli-test-details');
    assert.equal(await tested.getAttribute('open'),null);
    assert.equal(await card.locator('.cli-prerequisites').isVisible(),false);
    await tested.locator('> summary').click();
    assert.match(await tested.innerText(),/Verified the resulting state/);
    assert.match(await tested.innerText(),/Recipe:.*\.json/);
    assert.match(await tested.innerText(),/Exact test invocation:[\s\S]*VMARGS_PATH=.*\/usr\/lib\/riak\/bin\/riak/);
    if(route.endsWith('/join'))assert.match(await page.locator('[data-cli-example-id$=":unreachable-destination"] .cli-example-outcome').innerText(),/Expected error/);
   }
   await page.goto(`${root}${version}/reference/commands/erlang/riak/code-hash/`);
   assert.match(await page.locator('.cli-example-outcome').first().innerText(),/Known runtime limitation/);
   for(const route of ['riak','riak/admin/aae-status']){
    assert.equal((await page.goto(`${root}${version}/reference/commands/${route}/`)).status(),200);
    assert.equal(await page.locator('.cli-generated-syntax').count(),1);
    if(route==='riak'){
     const syntax=page.locator('.cli-generated-syntax');
     assert.match(await syntax.innerText(),/^riak \{ .*admin.* \}$/);
     assert.equal(await syntax.locator('a[href$="/riak/admin/"]').count(),1);
     assert.match(await page.locator('#notes + p, #notes ~ p').allTextContents().then(a=>a.join(' ')),/--relx-disable-hooks/);
    }else{
     assert.equal(await page.locator('.cli-generated-syntax').innerText(),'riak admin aae-status');
     assert.match(await page.locator('#aliases + ul').innerText(),/riak admin aae_status/);
    }
   }
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
    const dates=await page.locator('.cli-test-details time').evaluateAll(es=>es.map(e=>e.textContent));
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
   for (const [route, detail] of [
    ['riak/admin/security/add-user', 'password'],
    ['riak/admin/stat/info', 'Erlang API'],
    ['riak/admin/tictacaae/fold', '--outfile'],
    ['riak/repl/nat-map/add', 'launcher'],
    ['erlang/riak-client/stream-list-keys', 'ack_keys'],
    ['erlang/riak-client/aae-fold/object-stats', 'Bucket'],
    ['erlang/riak-kv-replrtq-src/register-rtq', 'Queue'],
   ]) {
    assert.equal((await page.goto(`${root}${version}/reference/commands/${route}/`)).status(),200,route);
    assert.ok(await page.locator('.cli-example').count()>0,route+' examples');
    assert.ok(await page.locator('.cli-observed').count()>0,route+' verified evidence');
    assert.ok((await page.locator('.cli-command-reference').innerText()).toLowerCase().includes(detail.toLowerCase()),route+' detail');
   }
   await page.goto(`${root}${version}/reference/commands/riak/daemon/`);
   assert.ok(await page.locator('.cli-example').count()>0);
   assert.equal(await page.locator('.cli-observed').count(),0,'manual lifecycle example must not claim runtime verification');
   assert.equal((await page.goto(`${root}${version}/reference/commands/erlang/riak-client/aae-fold/merge-tree-range/`)).status(),200);
   const binaryOutput=page.locator('.cli-observed').filter({hasText:'{{<'}).first();
   await binaryOutput.locator('summary').click();
   assert.ok((await binaryOutput.innerText()).includes('{{<'),'Erlang binary tuples must render literally, without shortcode parsing');
   await binaryOutput.locator('[data-code-copy]').first().click();
   assert.ok((await page.evaluate(()=>navigator.clipboard.readText())).includes('{{<'),'copy retains literal Erlang output');
   for(const selector of ['erase-keys','reap-tombs']) {
    assert.equal((await page.goto(`${root}${version}/reference/commands/erlang/riak-client/aae-fold/${selector}/`)).status(),200);
    const syntax=await page.locator('.cli-generated-syntax').allTextContents();
    assert.equal(syntax.length,6);
    assert.ok(syntax.every(s=>s.includes('Bucket, KeyRange, SegmentFilter, ModifiedRange')&&!s.includes('...')));
    for(const method of ['count','local','{job, JobId}'])assert.ok(syntax.some(s=>s.includes(method)));
    const keyRange=page.locator('.cli-parameters tbody tr').filter({has:page.locator('td:first-child code',{hasText:/^KeyRange$/})});
    const values=keyRange.locator('td').nth(1);
    assert.deepEqual(await values.locator('li').allTextContents().then(xs=>xs.map(x=>x.trim())),['all','binary key bounds']);
    assert.deepEqual(await values.locator('code').allTextContents(),['all']);
    await values.locator('[data-copy-value="all"]').click();
    assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'all');
    const client=page.locator('.cli-parameters tbody tr').filter({has:page.locator('td:first-child code',{hasText:/^Client$/})});
    assert.equal(await client.locator('a[href$="/erlang/riak-client/#argument-client"]').count(),1);
    const example=page.locator('.cli-example').filter({has:page.locator('h3',{hasText:'Count five, remove one, count four'})});
    await example.locator('.cli-observed > summary').click();
    assert.match(await example.locator('.cli-observed pre:not([hidden])').innerText(),/\{5,1,4\}/);
   }
   await page.goto(`${root}${version}/reference/commands/erlang/riak-client/`);
   assert.match(await page.locator('#argument-client').innerText(),/riak:local_client/);
   assert.match(await page.locator('#argument-bucket').innerText(),/cli_examples.*orders/s);
   assert.ok(await page.locator('.doc-table-of-contents a[href="#shared-arguments"]').count());
   await page.goto(`${root}${version}/reference/commands/erlang/riak-client/aae-fold/`);
   assert.match(await page.locator('#argument-modifiedrange').innerText(),/2026-12-24T23:59:59Z/);
   assert.match(await page.locator('#argument-modifiedrange').innerText(),/1798156799/);
   console.log(version+': page order, annotations across command families, manual/verified examples, copy buttons, headings, shared errors, dates and evidence passed.');
  }
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
