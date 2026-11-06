import {test} from 'node:test';import assert from 'node:assert/strict';import {parseHTML} from 'linkedom';
import {highlightText,resultURL,queryTerms} from '../../content/static/semantic-search/highlight.mjs';
test('highlights each entered word without interpreting HTML or regex syntax',()=>{
 const {document}=parseHTML('<div></div>'),element=document.querySelector('div');
 const value='Cluster with C++ and <img src=x onerror=bad()>: cluster';
 highlightText(element,value,'cluster C++ <img');
 assert.deepEqual([...element.querySelectorAll('mark')].map(m=>m.textContent),['Cluster','C++','<img','cluster']);
 assert.equal(element.querySelector('img'),null);assert.equal(element.textContent,value);
 highlightText(element,value,'cluster',false);assert.equal(element.querySelectorAll('mark').length,0);assert.equal(element.textContent,value);
});
test('result URLs carry individual words and retain paths, anchors and other parameters',()=>{
 const base='https://example.test/docs/';
 const enabled=new URL(resultURL('page/?other=1&highlight=old#section','node cluster',true,base));
 assert.equal(enabled.pathname,'/docs/page/');assert.equal(enabled.hash,'#section');assert.equal(enabled.searchParams.get('other'),'1');assert.deepEqual(enabled.searchParams.getAll('highlight'),['cluster','node']);
 assert.equal(new URL(resultURL(enabled.href,'node',false,base)).searchParams.has('highlight'),false);
 assert.deepEqual(queryTerms('node NODE node'),['node']);
});

test('single-character query words are excluded from marks and destination URLs',()=>{
 const {document}=parseHTML('<div></div>'),element=document.querySelector('div');
 highlightText(element,'Expand a cluster and add a node','expand a cluster');
 assert.deepEqual([...element.querySelectorAll('mark')].map(mark=>mark.textContent),['Expand','cluster']);
 assert.deepEqual(queryTerms('a I x'),[]);
 const url=new URL(resultURL('/docs/page/','expand a cluster',true,'https://example.test/'));
 assert.deepEqual(url.searchParams.getAll('highlight'),['cluster','expand']);
});
