const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const zlib=require('node:zlib');
const {spawnSync}=require('node:child_process');
const {parseHTML}=require('./social-html.cjs');
const {check,imageInfo}=require('./check-social-metadata.cjs');
const repo=path.resolve(__dirname,'../..');
function png(w,h){
 const crc=b=>{let c=0xffffffff;for(const v of b){c^=v;for(let i=0;i<8;i++)c=(c>>>1)^((c&1)?0xedb88320:0);}return (c^0xffffffff)>>>0;};
 const chunk=(type,data)=>{const b=Buffer.concat([Buffer.from(type),data]);const n=Buffer.alloc(4),c=Buffer.alloc(4);n.writeUInt32BE(data.length);c.writeUInt32BE(crc(b));return Buffer.concat([n,b,c]);};
 const hdr=Buffer.alloc(13);hdr.writeUInt32BE(w);hdr.writeUInt32BE(h,4);hdr[8]=8;hdr[9]=2;
 return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',hdr),chunk('IDAT',zlib.deflateSync(Buffer.alloc((1+w*3)*h))),chunk('IEND',Buffer.alloc(0))]);
}
function fixture(){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'openriak-social-test-'));
 for(const p of ['content','layouts','layouts/shortcodes','static/images'])fs.mkdirSync(path.join(dir,p),{recursive:true});
 for(const section of Object.values(JSON.parse(fs.readFileSync(path.join(repo,'layouts/common-docs/data/social_previews.json'),'utf8'))))fs.copyFileSync(path.join(repo,'content/static/common',section.image),path.join(dir,'static',section.image));
 fs.writeFileSync(path.join(dir,'static/custom.png'),png(24,16));fs.writeFileSync(path.join(dir,'static/broken.png'),'not an image');
 fs.writeFileSync(path.join(dir,'layouts/all.html'),'<!doctype html><html><head>{{ partial "social/head.html" (dict "page" .) }}</head><body><nav>Unrelated navigation</nav></body></html>');
 fs.copyFileSync(path.join(repo,'layouts/common-docs/layouts/alias.html'),path.join(dir,'layouts/alias.html'));
 fs.writeFileSync(path.join(dir,'layouts/shortcodes/generated-menu.html'),'<nav>Generated navigation</nav>');
 return dir;
}
function page(dir,name,params={},body=''){fs.mkdirSync(path.dirname(path.join(dir,'content',name+'.md')),{recursive:true});fs.writeFileSync(path.join(dir,'content',name+'.md'),`---\n${JSON.stringify(params)}\n---\n${body}`);}
function build(dir,base,params={description:'Global description.'},title='OpenRiak Documentation'){
 const config={baseURL:base,title,disableKinds:['taxonomy','term','RSS','sitemap'],params,module:{mounts:[{source:'content',target:'content'},{source:path.join(repo,'layouts/common-docs/data/social_previews.json'),target:'data/social_previews.json'},{source:'layouts',target:'layouts'},{source:'static',target:'static'},{source:'static',target:'assets/social-static'},{source:path.join(repo,'layouts/common-docs/layouts/partials'),target:'layouts/_partials'}]}};
 fs.writeFileSync(path.join(dir,'hugo.json'),JSON.stringify(config));
 const args=['--source',dir,'--destination',path.join(dir,'public'),'--cleanDestinationDir'];
 return process.env.HUGO_BIN?spawnSync(process.env.HUGO_BIN,args,{encoding:'utf8'}):spawnSync('docker',['run','--rm','--user',`${process.getuid()}:${process.getgid()}`,'--entrypoint','hugo','-v',`${dir}:${dir}`,'-v',`${repo}:${repo}:ro`,'ghcr.io/gohugoio/hugo:v0.166.0',...args],{encoding:'utf8'});
}
function read(dir,name){const d=parseHTML(fs.readFileSync(path.join(dir,'public',name,'index.html'),'utf8'));return {get:k=>d.meta.get(k)?.[0],...d};}
for(const base of ['http://localhost:1410/docs/','https://example.test/','https://www.tiot.jp/openriak-docs-beta/'])test(`fallback matrix at ${base}`,async()=>{
 const dir=fixture();
 try{
  page(dir,'_index',{title:'Home'});
  page(dir,'explicit',{title:'Ordinary',social_title:'Custom & "title"',social_description:'Custom description',social_image:'custom.png',social_image_alt:'A custom image',description:'Ignored',images:['missing.png']});
  page(dir,'standard',{title:'Standard',description:'Page description',image:'custom.png'});
  page(dir,'noimage',{title:'No image',description:'Page description'});
  page(dir,'title',{title:'Only title'},'Main **content** [link](https://example.org).');
  page(dir,'bare',{},'Content without front matter metadata.');
  page(dir,'empty',{social_title:'  ',social_description:' \t ',description:' ',summary:' ',social_image:' ',image:null},'');
  page(dir,'summary',{summary:'A **summary** <em>with HTML</em>.',description:' '},'Ignored body');
  page(dir,'clean',{description:'  **Bold** <b>HTML</b> [label](https://example.org) {{< something >}} &amp; clean.  '});
  page(dir,'long',{},'A useful sentence. '.repeat(50));
  page(dir,'same',{title:'A guide · OpenRiak Documentation'});
  page(dir,'missing',{social_image:'missing.png',images:['','missing-too.png','custom.png']});
  page(dir,'svg',{social_image:'logo.svg'});
  page(dir,'badurl',{social_image:'https://bad host/image.png'});
  page(dir,'http',{social_image:'http://example.org/a.png'});
  page(dir,'broken',{social_image:'broken.png'});
  page(dir,'canonical',{canonical_url:'https://example.org/chosen/?utm_source=test#heading',aliases:['/old/']});
  page(dir,'badcanonical',{canonical_url:'javascript:bad'});
  page(dir,'card',{twitter_card:'summary'});
  page(dir,'badcard',{twitter_card:'anything'});
  page(dir,'bodyimage',{},'Only a body image: ![An image](custom.png)');
  page(dir,'shortcode',{},'{{< generated-menu >}}<nav>Navigation text</nav>');
  page(dir,'longexplicit',{social_description:'Explicit description. '.repeat(20)});
  page(dir,'absoluteimage',{social_image:base+'custom.png'});
  const opposite=base.replace(/^https?:/,base.startsWith('https:')?'http:':'https:');
  page(dir,'localprotocol',{social_image:opposite+'custom.png',canonical_url:opposite+'localprotocol/'});
  page(dir,'actualtype',{social_image:'mislabeled.jpg'});
  fs.writeFileSync(path.join(dir,'static/mislabeled.jpg'),png(24,16));
  page(dir,'bundle/index',{social_image:'photo.png',resources:[{src:'photo.png',params:{alt:'Resource alt text'}}]});
  fs.writeFileSync(path.join(dir,'content/bundle/photo.png'),png(30,20));
  let r=build(dir,base);assert.equal(r.status,0,r.stdout+r.stderr);
  for(const word of ['missing.png','logo.svg','bad host','broken.png'])assert.ok((r.stdout+r.stderr).includes(word));
  assert.equal(read(dir,'bodyimage').get('og:image'),base+'images/homepage-social-preview.png');
  assert.equal(read(dir,'shortcode').get('og:description'),'Global description.');
  assert.ok(read(dir,'longexplicit').get('og:description').length>200);
  assert.equal(read(dir,'absoluteimage').get('og:image:width'),'24');
  assert.equal(read(dir,'localprotocol').get('og:image'),base+'custom.png');
  assert.equal(read(dir,'localprotocol').get('og:url'),base+'localprotocol/');
  assert.equal(read(dir,'actualtype').get('og:image:type'),'image/png');
  assert.equal(read(dir,'bundle').get('og:image:width'),'30');
  assert.equal(read(dir,'bundle').get('og:image:height'),'20');
  assert.equal(read(dir,'bundle').get('og:image:alt'),'Resource alt text');
  const a=read(dir,'explicit');assert.equal(a.get('og:title'),'Custom & “title”');assert.equal(a.get('og:description'),'Custom description');assert.equal(a.get('og:image'),base+'custom.png');assert.equal(a.get('og:image:width'),'24');assert.equal(a.get('og:image:height'),'16');assert.equal(a.get('og:image:type'),'image/png');assert.equal(a.get('og:image:alt'),'A custom image');
  assert.equal(read(dir,'').get('og:title'),'OpenRiak Documentation');
  assert.equal(read(dir,'standard').get('og:description'),'Page description');assert.equal(read(dir,'standard').get('og:image'),base+'custom.png');
  for(const name of ['noimage','bare','empty','svg','badurl','http','broken']){const d=read(dir,name);assert.equal(d.get('og:image'),base+'images/homepage-social-preview.png');assert.equal(d.get('og:image:width'),'1200');assert.equal(d.get('og:image:height'),'630');assert.equal(d.get('og:image:alt'),'Homepage — OpenRiak Documentation');}
  assert.equal(read(dir,'title').get('og:description'),'Main content link.');assert.equal(read(dir,'empty').get('og:description'),'Global description.');assert.equal(read(dir,'summary').get('og:description'),'A summary with HTML.');assert.equal(read(dir,'clean').get('og:description'),'Bold HTML label & clean.');assert.ok(read(dir,'long').get('og:description').length<=200);
  assert.equal(read(dir,'same').get('og:title'),'A guide · OpenRiak Documentation');assert.equal(read(dir,'missing').get('og:image'),base+'custom.png');
  assert.equal(read(dir,'canonical').get('og:url'),'https://example.org/chosen/');assert.equal(read(dir,'badcanonical').get('og:url'),base+'badcanonical/');assert.equal(read(dir,'card').get('twitter:card'),'summary');assert.equal(read(dir,'badcard').get('twitter:card'),'summary_large_image');
  await check(path.join(dir,'public'),base);
  r=build(dir,base,{description:' ',social_image:'missing-global.png'},'');assert.equal(r.status,0,r.stdout+r.stderr);assert.equal(read(dir,'empty').get('og:description'),'OpenRiak documentation and reference guides.');assert.equal(read(dir,'').get('og:title'),'OpenRiak Documentation');
  assert.ok((r.stdout+r.stderr).includes('missing-global.png'));
  for(const bad of [null,Buffer.from('not a PNG'),png(20,20)]){
   const file=path.join(dir,'static/images/homepage-social-preview.png');if(bad)fs.writeFileSync(file,bad);else fs.unlinkSync(file);
   r=build(dir,base);assert.notEqual(r.status,0);assert.match(r.stdout+r.stderr,/Bundled social fallback must be a valid/);
  }
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
test('external images are unverified at template time, omit unknown dimensions, and require HTTP checks',async()=>{
 const dir=fixture();try{
  page(dir,'external',{social_image:'https://images.example.org/photo.png'});
  const r=build(dir,'https://example.test/');assert.equal(r.status,0,r.stdout+r.stderr);
  const d=read(dir,'external');assert.equal(d.get('og:image:width'),undefined);assert.equal(d.get('og:image:height'),undefined);
  const original=global.fetch;let calls=0;
  try{
   global.fetch=async()=>{calls++;return {ok:false,status:403}};await assert.rejects(check(path.join(dir,'public'),'https://example.test/'),/HTTP 403/);
   global.fetch=async()=>({ok:true,url:'https://images.example.org/photo.png',headers:new Map([['content-type','image/png']]),arrayBuffer:async()=>png(10,10)});await check(path.join(dir,'public'),'https://example.test/');assert.equal(calls,1);
   global.fetch=async()=>({status:302,headers:new Map([['location','http://images.example.org/unsafe.png']])});
   await assert.rejects(check(path.join(dir,'public'),'https://example.test/'),/invalid HTTPS URL/);
  }finally{global.fetch=original;}
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
});

test('image audit rejects truncated PNG data',()=>{
 assert.throws(()=>imageInfo(png(10,10).subarray(0,24)),/invalid PNG/);
});

test('each section and legacy product route selects its own bundled preview',async()=>{
 const dir=fixture();try{
  const routes={
   'openriak-kv/3.4.1/guide':'openriak-kv',
   'openriak-cs/2.1.3/guide':'openriak-cs',
   'openriak-ts/3.0.0/guide':'openriak-ts',
   'riak-kv/3.2.5/guide':'openriak-kv',
   'riak-cs/2.1.2/guide':'openriak-cs',
   'riak-ts/1.5.2/guide':'openriak-ts',
   'community/guide':'community',
   'archived-mailing-list/thread':'archived-mailing-list',
   'archived-technical-blog/post':'archived-technical-blog',
   'settings/appearance':'settings',
   'settings':'settings',
   'unknown/guide':'homepage'
  };
  for(const route of Object.keys(routes))page(dir,route,route==='settings'?{layout:'settings'}:{});
  fs.writeFileSync(path.join(dir,'layouts/settings.html'),fs.readFileSync(path.join(dir,'layouts/all.html')));
  page(dir,'_index',{});
  const base='https://example.test/beta/';let r=build(dir,base);assert.equal(r.status,0,r.stdout+r.stderr);
  for(const [route,section] of Object.entries(routes))assert.equal(read(dir,route).get('og:image'),`${base}images/${section}-social-preview.png`,route);
  assert.equal(read(dir,'').get('og:image'),base+'images/homepage-social-preview.png');
  await check(path.join(dir,'public'),base);
  page(dir,'openriak-kv/3.4.1/guide',{social_image:'custom.png'});
  r=build(dir,base);assert.equal(r.status,0,r.stdout+r.stderr);assert.equal(read(dir,'openriak-kv/3.4.1/guide').get('og:image'),base+'custom.png');
  r=build(dir,base,{social_image:'custom.png'});assert.equal(r.status,0,r.stdout+r.stderr);assert.equal(read(dir,'community/guide').get('og:image'),base+'custom.png');
  fs.unlinkSync(path.join(dir,'static/images/openriak-cs-social-preview.png'));
  r=build(dir,base);assert.notEqual(r.status,0);assert.match(r.stdout+r.stderr,/openriak-cs-social-preview.png/);
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
