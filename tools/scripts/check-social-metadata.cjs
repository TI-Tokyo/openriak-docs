#!/usr/bin/env node
// Check the delivered HTML, not template source. External previews are always fetched.
const fs = require('node:fs');
const path = require('node:path');
const zlib = require('node:zlib');
const {parseHTML} = require('./social-html.cjs');
function imageInfo(b) {
  if (b.length >= 24 && b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))) {
    let offset=8, ended=false;const data=[];
    while(offset+12<=b.length) {
      const size=b.readUInt32BE(offset),end=offset+12+size;
      if(end>b.length)throw Error('invalid PNG: truncated chunk');
      const kind=b.toString('ascii',offset+4,offset+8);
      let crc=0xffffffff;for(const byte of b.subarray(offset+4,end-4)){crc^=byte;for(let bit=0;bit<8;bit++)crc=(crc>>>1)^((crc&1)?0xedb88320:0);}
      if(((crc^0xffffffff)>>>0)!==b.readUInt32BE(end-4))throw Error('invalid PNG: chunk checksum');
      if(offset===8 && (kind!=='IHDR'||size!==13))throw Error('invalid PNG: missing IHDR');
      if(kind==='IDAT')data.push(b.subarray(offset+8,end-4));
      if(kind==='IEND'){ended=size===0 && end===b.length;break;}offset=end;
    }
    if(!ended || !data.length || !zlib.inflateSync(Buffer.concat(data)).length)throw Error('invalid PNG: incomplete image');
    return {type:'image/png',width:b.readUInt32BE(16),height:b.readUInt32BE(20)};
  }
  if (b.length >= 10 && /^GIF8[79]a/.test(b.toString('ascii',0,6))) return {type:'image/gif',width:b.readUInt16LE(6),height:b.readUInt16LE(8)};
  if (b.length >= 30 && b.toString('ascii',0,4)==='RIFF' && b.toString('ascii',8,12)==='WEBP') {
    const kind=b.toString('ascii',12,16);
    if(kind==='VP8X') return {type:'image/webp',width:1+b.readUIntLE(24,3),height:1+b.readUIntLE(27,3)};
    if(kind==='VP8 ') return {type:'image/webp',width:b.readUInt16LE(26)&16383,height:b.readUInt16LE(28)&16383};
    if(kind==='VP8L') {const n=b.readUInt32LE(21);return {type:'image/webp',width:1+(n&16383),height:1+((n>>>14)&16383)};}
  }
  if(b[0]===255 && b[1]===216) {
    let i=2;
    while(i+4<b.length) {
      if(b[i++]!==255) break;
      let marker=b[i++];while(marker===255) marker=b[i++];
      if(marker===217 || marker===218) break;
      if(marker===1 || (marker>=208 && marker<=215)) continue;
      const size=b.readUInt16BE(i);if(size<2 || i+size>b.length) break;
      if([192,193,194,195,197,198,199,201,202,203,205,206,207].includes(marker)) return {type:'image/jpeg',height:b.readUInt16BE(i+3),width:b.readUInt16BE(i+5)};
      i+=size;
    }
  }
  throw Error('not a supported raster image');
}
function httpsURL(value) {const u=new URL(value);if(u.protocol!=='https:' || !u.hostname || u.username || u.password || u.hash)throw Error(`invalid HTTPS URL: ${value}`);return u;}
function webURL(value) {const u=new URL(value);if(!['http:','https:'].includes(u.protocol)||!u.hostname||u.username||u.password||u.hash)throw Error(`invalid HTTP(S) URL: ${value}`);return u;}
function siteURL(value,base) {const u=webURL(value);if(u.host===base.host){if(u.protocol!==base.protocol)throw Error(`URL protocol does not match baseURL: ${value}`);}else httpsURL(value);return u;}
function* files(dir) {for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())yield* files(p);else if(e.name.endsWith('.html'))yield p;}}
async function fetchImage(url,validate) {
 for(let hop=0;hop<6;hop++) {
  validate(url);
  const response=await fetch(url,{redirect:'manual',signal:AbortSignal.timeout(20000)});
  if([301,302,303,307,308].includes(response.status)) {
   const location=response.headers.get('location');
   if(!location)throw Error(`${url}: redirect has no Location`);
   url=new URL(location,url).href;continue;
  }
  return response;
 }
 throw Error(`${url}: too many redirects`);
}
async function check(root,baseURL,{http=false,assetRoot=root}={}) {
 const base=webURL(baseURL);const prefix=base.pathname.replace(/\/?$/,'/');
 const images=new Map();let count=0;
 for(const file of files(root)) {
  const doc=parseHTML(fs.readFileSync(file,'utf8'));
  const one=(key)=>{const a=doc.meta.get(key)||[];if(a.length!==1 || !a[0].trim())throw Error(`${file}: expected one nonempty ${key}`);return a[0];};
  if(doc.titles.length!==1 || !doc.titles[0].trim())throw Error(`${file}: missing/duplicate title`);
  if(doc.canonical.length!==1)throw Error(`${file}: missing/duplicate canonical`);
  const canonical=siteURL(doc.canonical[0],base);if(canonical.search)throw Error(`${file}: canonical query parameters`);
  if(one('og:url')!==canonical.href)throw Error(`${file}: canonical and og:url differ`);
  for(const k of ['title','description','image'])if(one(`og:${k}`)!==one(`twitter:${k}`))throw Error(`${file}: inconsistent ${k}`);
  if(one('description')!==one('og:description'))throw Error(`${file}: inconsistent description`);
  if(one('og:type')!=='website')throw Error(`${file}: unsupported og:type`);
  if(!['summary','summary_large_image'].includes(one('twitter:card')))throw Error(`${file}: invalid card`);
  one('og:image:alt');const url=one('og:image');siteURL(url,base);
  const entry={file,type:one('og:image:type'),width:doc.meta.get('og:image:width'),height:doc.meta.get('og:image:height')};
  for(const key of ['width','height']) if(entry[key] && (entry[key].length!==1 || !/^[1-9]\d*$/.test(entry[key][0])))throw Error(`${file}: invalid image ${key}`);
  if(!!entry.width!==!!entry.height)throw Error(`${file}: incomplete image dimensions`);
  if(!images.has(url))images.set(url,[]);images.get(url).push(entry);count++;
 }
 if(!count)throw Error('No HTML pages found');
 for(const [url,entries] of images) {
  const u=siteURL(url,base);const local=u.origin===base.origin && u.pathname.startsWith(prefix);let bytes;
  if(local) {
    const relative=decodeURIComponent(u.pathname.slice(prefix.length));const filename=path.resolve(assetRoot,relative);
    if(!filename.startsWith(path.resolve(assetRoot)+path.sep))throw Error('Image escapes output directory');
    bytes=fs.readFileSync(filename);
  }
  if(http || !local) {
    const validate=local?(value)=>siteURL(value,base):httpsURL;
    const response=await fetchImage(url,validate);
    if(!response.ok)throw Error(`${url}: HTTP ${response.status}`);validate(response.url);
    bytes=Buffer.from(await response.arrayBuffer());const info=imageInfo(bytes);
    if(response.headers.get('content-type')?.split(';')[0].trim().toLowerCase()!==info.type)throw Error(`${url}: incorrect HTTP Content-Type`);
  }
  const info=imageInfo(bytes);
  for(const e of entries) {
    if(info.type!==e.type)throw Error(`${e.file}: incorrect image MIME type for ${url}`);
    if(e.width && (+e.width[0]!==info.width || +e.height[0]!==info.height))throw Error(`${e.file}: incorrect image dimensions`);
  }
 }
 return {pages:count,images:images.size};
}
module.exports={check,imageInfo};
if(require.main===module){const args=process.argv.slice(2);const root=args[0],base=args[1];if(!root||!base){console.error('Usage: check-social-metadata.cjs OUTPUT BASE_URL [--http] [--asset-root DIR]');process.exit(2);}
 const at=args.indexOf('--asset-root');check(root,base,{http:args.includes('--http'),assetRoot:at<0?root:args[at+1]}).then(r=>console.log(`Social metadata verified: ${r.pages} HTML pages, ${r.images} images${args.includes('--http')?' (including HTTP checks)':''}.`)).catch(e=>{console.error(e.message);process.exitCode=1});}
