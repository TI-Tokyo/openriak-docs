'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { annotateSettings, parseSetting, settingFingerprint } = require('./settings-annotations');
const { parseMarkdown } = require('./cli-annotation-markdown');
const { buildAnnotatedReference } = require('./cli-annotations');
const { configurationReference } = require('./configuration-reference');
const { defaultsByOs } = require('./defaults-by-os');
const root = path.resolve(__dirname, '../..');
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const document = {settings: {example: {documentation: 'Original', datatype: {type:'integer'}, definitions: [{repository:'riak_kv',path:'priv/riak_kv.schema',line:1}]}}};
const original = {version:'3.4.1',settings:[{name:'example',description:'Original',internalName:'riak_kv.example',areas:['riak_kv'],datatype:{label:'Integer',options:[],units:[],constraints:[]},defaults:{alpine:{hasDefault:true,value:'7'}}}]};
function fixture(fn) { const directory = fs.mkdtempSync(path.join(os.tmpdir(),'settings-annotations-')); const write = (name, text) => {
 const file=path.join(directory,'example',name+'.md');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,text);return file;
}; try { return fn(directory,write); } finally {fs.rmSync(directory,{recursive:true,force:true});} }

test('all released settings have revised descriptions, categorized tags, current reviews and immutable defaults', () => {
 for(const version of ['3.4.0','3.4.1']) {
  const document=read(`content/openriak-kv/metadata/${version}/kv-settings.json`);
  const targets=read(`content/openriak-kv/metadata/${version}/kv-supported-os.json`).operating_systems;
  const oses=read(`tools/generated/openriak-kv/data/versions/${version}.json`).operatingSystems;
  const raw=configurationReference({productId:'openriak-kv'},version,{...document,effective_defaults:defaultsByOs(document,targets)},oses);
  const annotated=annotateSettings(raw,document);
  assert.equal(annotated.annotationCoverage.complete,427);
  assert.deepEqual(annotated.annotationCoverage.issues,[]);
  const anchors=new Set(annotated.settings.map(s=>s.anchor));
  assert.equal(anchors.size,annotated.settings.length);
  for(const [i,setting] of annotated.settings.entries()) {
   assert.equal(setting.name,raw.settings[i].name);
   assert.deepEqual(setting.defaults,raw.settings[i].defaults);
   assert.notEqual(setting.description,setting.source.documentation,setting.name);
   assert.ok(setting.description.length>70,setting.name);
   for(const category of ['feature','repository','module','concept']) assert.ok(setting.tags[category].length,`${setting.name}: ${category}`);
   assert.deepEqual(setting.source,document.settings[setting.name]);
   for(const related of setting.related) {
    assert.notEqual(related.name,setting.name);
    assert.ok(anchors.has(related.anchor));
    assert.ok(related.features.length && related.concepts.length);
   }
  }
  const cli=buildAnnotatedReference(read(`content/openriak-kv/metadata/${version}/kv-cli-commands.json`));
  for(const page of cli.pages) for(const category of ['feature','repository','module','concept']) assert.ok(page.reference.tags[category].length,`${page.key}: ${category}`);
 }
});

test('common and version sections merge, clear inherited values, and record only actual datatype changes', () => fixture((overrideRoot,write) => {
 write('common','# Description\nShared\n\n# Datatype\nCount\n\n# Allowed values\n- 7\n- 8\n\n# Tags\nfeature: storage\nconcept: capacity\n\n# Constraints\n- Positive\n\n# Notes\nA note');
 write('3.4.1','# Description\nRelease\n\n# Allowed values\n\n# Tags\nconcept: memory\n\n# Notes\n');
 const reference=annotateSettings(original,document,{overrideRoot});const setting=reference.settings[0];
 assert.equal(setting.description,'Release');assert.equal(setting.datatype.label,'Count');
 assert.deepEqual(setting.datatype.options,[]);assert.deepEqual(setting.tags.feature,['storage']);assert.deepEqual(setting.tags.concept,['memory']);assert.equal(setting.notes,'');
 assert.deepEqual(setting.defaults,original.settings[0].defaults);assert.equal(original.settings[0].description,'Original');
 assert.deepEqual(reference.annotationCoverage.corrections.map(c=>c.field),['datatype.label','datatype.options','datatype.constraints','datatype.options']);
 write('common','# Datatype\nInteger');fs.unlinkSync(path.join(overrideRoot,'example/3.4.1.md'));
 assert.deepEqual(annotateSettings(original,document,{overrideRoot}).annotationCoverage.corrections,[]);
}));

test('reject immutable fields, invalid tags, malformed lists, duplicate sections and unknown settings', () => fixture((overrideRoot,write) => {
 for(const heading of ['Name','Default','Default value','Defaults','Unsupported']) assert.throws(()=>parseSetting(`# ${heading}\nchanged`,'fixture'),/unknown or immutable/);
 for(const body of ['feature: Bad Tag','unknown: storage','feature: storage, storage','feature: storage\nfeature: other']) assert.throws(()=>parseSetting('# Tags\n'+body,'fixture'),/tags|category/);
 assert.throws(()=>parseSetting('# Allowed values\nnot a list','fixture'),/bullet list/);
 assert.throws(()=>parseSetting('# Notes\none\n# Notes\ntwo','fixture'),/duplicate/);
 assert.throws(()=>parseSetting('# Reviewed against\n3.4.1: bad','fixture'),/fingerprint/);
 write('common','# Description\nText');fs.renameSync(path.join(overrideRoot,'example'),path.join(overrideRoot,'missing'));
 assert.throws(()=>annotateSettings(original,document,{overrideRoot}),/missing setting/);
}));

test('review fingerprints track contracts, ignore source line shifts, and preserve Markdown fences', () => fixture((overrideRoot,write) => {
 const source=document.settings.example;const fingerprint=settingFingerprint(source);
 const moved=structuredClone(source);moved.definitions[0].line++;
 assert.equal(settingFingerprint(moved),fingerprint);moved.datatype.type='string';assert.notEqual(settingFingerprint(moved),fingerprint);
 write('common',`# Description\nParagraph.\n\n\`\`\`conf\n# Name\nexample = 7\n\`\`\`\n\n# Reviewed against\n3.4.1: ${fingerprint}`);
 let result=annotateSettings(original,document,{overrideRoot});assert.ok(result.settings[0].description.includes('# Name'));assert.ok(!result.annotationCoverage.issues.some(i=>['stale','unreviewed'].includes(i.status)));
 result=annotateSettings(original,{settings:{example:moved}},{overrideRoot});assert.ok(result.annotationCoverage.issues.some(i=>i.status==='stale'));
 assert.deepEqual(parseMarkdown('# Tags\nfeature: storage\nmodule: riak_kv_vnode').tags,{feature:['storage'],module:['riak_kv_vnode']});
}));

test('live settings watcher handles additions, changes, removals and invalid edits without losing the valid preview', async () => {
 const directory=fs.mkdtempSync(path.join(os.tmpdir(),'settings-watch-'));
 const inputRoot=path.join(directory,'metadata'),outputRoot=path.join(directory,'output'),overrideRoot=path.join(directory,'annotations');
 const save=(file,value)=>{fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,value);};
 save(path.join(inputRoot,'3.4.1/kv-settings.json'),JSON.stringify({...document,version:'3.4.1',schema_version:2,defaults_scope:'os',effective_defaults:{alpine:{example:{has_default:true,value:7}}}}));
 save(path.join(inputRoot,'3.4.1/kv-supported-os.json'),JSON.stringify({operating_systems:[]}));
 save(path.join(outputRoot,'openriak-kv/data/versions/3.4.1.json'),JSON.stringify({operatingSystems:[{id:'alpine',defaultsKey:'alpine'}]}));
 const file=path.join(overrideRoot,'example/common.md'),versionFile=path.join(overrideRoot,'example/3.4.1.md');
 const {watchSettings}=require('./watch-settings-reference');const log=console.log,error=console.error,errors=[];
 console.log=()=>{};console.error=e=>errors.push(e);let timer;
 const output=path.join(outputRoot,'openriak-kv/data/configuration-reference/3.4.1.json');
 const description=()=>JSON.parse(fs.readFileSync(output)).settings[0].description;
 const wait=()=>new Promise(resolve=>setTimeout(resolve,80));
 try {
  timer=watchSettings({inputRoot,outputRoot,overrideRoot,intervalMs:10});assert.equal(description(),'Original');
  save(file,'# Description\nShared');await wait();assert.equal(description(),'Shared');
  save(versionFile,'# Description\nRelease');await wait();assert.equal(description(),'Release');
  fs.unlinkSync(versionFile);await wait();assert.equal(description(),'Shared');
  save(file,'# Default value\n99');await wait();assert.equal(description(),'Shared');assert.ok(errors.some(e=>e.includes('keeping the last valid preview')));
  fs.unlinkSync(file);await wait();assert.equal(description(),'Original');
 } finally {clearInterval(timer);console.log=log;console.error=error;fs.rmSync(directory,{recursive:true,force:true});}
});
