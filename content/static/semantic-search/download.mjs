const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
export async function download(url,{request=fetch,onProgress=()=>{},json=false,retries=2,delay=pause,timeout=30000}={}) {
 for(let attempt=0;;attempt++) {
  const controller=new AbortController();let timer;
  const arm=()=>{clearTimeout(timer);timer=setTimeout(()=>controller.abort(),timeout);};
  try {
   arm();const response=await request(url,{signal:controller.signal});
   if(!response.ok){const error=Error(`Download failed: HTTP ${response.status}`);error.status=response.status;throw error;}
   if(!response.body?.getReader) return json?await response.json():await response.arrayBuffer();
   const total=Number(response.headers.get('content-length'))||0;
   const reader=response.body.getReader(),chunks=[];let loaded=0;
   while(true){const {done,value}=await reader.read();if(done)break;chunks.push(value);loaded+=value.length;arm();onProgress({loaded,total,attempt});}
   const bytes=new Uint8Array(loaded);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.length;}
   return json?JSON.parse(new TextDecoder().decode(bytes)):bytes.buffer;
  } catch(error) {
   controller.abort();
   const retryable=error.status?error.status===408||error.status===429||error.status>=500:!(error instanceof SyntaxError);
   if(!retryable||attempt>=retries)throw error;
   clearTimeout(timer);onProgress({retry:attempt+1,retries});await delay(1000*2**attempt);
  } finally {clearTimeout(timer);}
 }
}
export function progressText(event) {
 if(event.retry)return `${event.phase}: retry ${event.retry} of ${event.retries}…`;
 const part=event.parts?` (${event.part}/${event.parts})`:'';
 const unit=(event.total||event.loaded||0)<1048576?{scale:1024,name:'KiB'}:{scale:1048576,name:'MiB'};
 const bytes=event.loaded===undefined?'':` · ${(event.loaded/unit.scale).toFixed(1)}${event.total?' / '+(event.total/unit.scale).toFixed(1):''} ${unit.name}`;
 return `${event.phase}${part}${bytes}…`;
}

export function createProgress(status,isActive=()=>true) {
 const ui=globalThis.OpenRiakSearchStatus;
 let timer,last,phaseStarted,phase;
 return event=>{
  if(!isActive())return;
  if(event.restart||phase!==event.phase){phase=event.phase;phaseStarted=Date.now();}
  clearInterval(timer);
  const update=()=>{
   if(!isActive()||(last&&ui.current(status)!==last)){clearInterval(timer);return;}
   last=`${progressText(event)} (${Math.floor((Date.now()-phaseStarted)/1000)}s)`;
   ui.semantic(status,last);
  };
  last=ui.current(status);update();timer=setInterval(update,1000);
 };
}
