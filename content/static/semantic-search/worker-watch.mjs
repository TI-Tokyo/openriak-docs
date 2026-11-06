// A worker can hang during WASM initialisation without emitting an error.
// Only real worker activity extends this deadline, not keystrokes or UI timers.
export function watchWorker(worker,onTimeout,timeout=120000) {
 let timer,active=false;
 const stop=()=>{clearTimeout(timer);active=false;};
 const arm=()=>{clearTimeout(timer);timer=setTimeout(()=>{stop();worker.terminate();onTimeout(Error('Semantic search stopped responding'));},timeout);};
 worker.addEventListener('message',()=>{if(active)arm();});
 return {start(){if(!active){active=true;arm();}},stop};
}
