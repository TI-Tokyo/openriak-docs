// Build just the blog for browser tests, without rebuilding the mailing-list archive.
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const config=fs.readFileSync(path.join(root,'content/hugo-archives.yaml'),'utf8').split('\n').filter(line=>!line.includes('archive-mailing-list')&&!line.includes('mailing-list/')).join('\n');
fs.mkdirSync(path.join(root,'tools/generated'),{recursive:true});
fs.writeFileSync(path.join(root,'tools/generated/blog-preview.yaml'),config);
const version=fs.readFileSync(path.join(root,'.hugo-version'),'utf8').trim();
for(const [folder,base] of [['blog-preview','http://localhost:1410/docs/'],['blog-preview-root','http://localhost:1410/']]){
 const result=spawnSync('docker',['run','--rm','--user',`${process.getuid?.()||1000}:${process.getgid?.()||1000}`,'-e','GOMAXPROCS=2','-e','GOMEMLIMIT=2GiB','-v',`${root}:/project`,'-w','/project','--entrypoint','hugo',`ghcr.io/gohugoio/hugo:v${version}`,'--source=/project/content','--config=/project/tools/generated/blog-preview.yaml',`--destination=/project/tools/generated/${folder}`,`--baseURL=${base}`,'--noBuildLock'],{stdio:'inherit'});
 if(result.status!==0)process.exit(result.status||1);
}
