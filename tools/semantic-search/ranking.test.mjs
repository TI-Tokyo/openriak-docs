import {test} from 'node:test';
import assert from 'node:assert/strict';
import {rank,cosineScores} from '../../content/static/semantic-search/ranking.mjs';
const passages=[
 {title:'Cluster recovery',heading:'Repair',text:'Bring a replacement machine into the cluster.',url:'recovery/'},
 {title:'Cluster recovery',heading:'Repair',text:'Replace a failed member safely.',url:'recovery/'},
 {title:'Configuration',heading:'n_val',text:'n_val controls the replica count.',url:'config/'},
 {title:'Other',heading:'',text:'Unrelated content',url:'other/'}
];
test('semantic results can match without shared words and deduplicate articles',()=>{
 const result=rank(passages,'recover unavailable nodes',[.8,.9,.1,.05]);assert.equal(result.length,1);assert.equal(result[0].url,'recovery/');
});
test('exact configuration keys remain searchable without a model',()=>{
 assert.equal(rank(passages,'n_val')[0].url,'config/');assert.deepEqual(rank(passages,'xyzunknown'),[]);assert.deepEqual(rank(passages,'!!!'),[]);
});
test('cosine comparison uses every passage and rejects invalid dimensions',()=>{
 assert.deepEqual(cosineScores(new Float32Array([1,0,0,1]),new Float32Array([1,0])),[1,0]);assert.throws(()=>cosineScores([1,2,3],[1,0]));
});

test('one-letter misspellings and transpositions find cluster expansion',async()=>{
 const {normaliseQuery}=await import('../../content/static/semantic-search/ranking.mjs');
 const docs=[
  {title:'Expand a cluster',heading:'Adding nodes',text:'Expand a cluster by joining another node.',url:'expand/'},
  {title:'Cluster membership',heading:'Membership',text:'Manage cluster membership.',url:'members/'},
  {title:'Client configuration',heading:'Options',text:'Configure a client.',url:'client/'},
 ];
 for(const query of ['expand a clister','expand a clsuter','expand a clustr']){
  assert.equal(normaliseQuery(docs,query),'expand a cluster');
  assert.equal(rank(docs,query)[0].url,'expand/');
 }
 assert.equal(normaliseQuery(docs,'n_val cluster_id riak-admin'),'n_val cluster_id riak-admin');
 assert.equal(normaliseQuery([...docs,{title:'Literal',heading:'',text:'clister is a literal custom value',url:'literal/'}],'clister'),'clister');
});

test('semantic-only mode does not include lexical matches',()=>{
 const results=rank(passages,'n_val',[.8,.9,.1,.05],8,{text:false});
 assert.deepEqual(results.map(p=>p.url),['recovery/']);
});
