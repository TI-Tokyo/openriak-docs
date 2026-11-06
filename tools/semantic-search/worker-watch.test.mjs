import {test} from 'node:test';
import assert from 'node:assert/strict';
import {watchWorker} from '../../content/static/semantic-search/worker-watch.mjs';
const pause=ms=>new Promise(r=>setTimeout(r,ms));
test('a hung worker times out even when new keystrokes keep arriving',async()=>{
 const worker=new EventTarget();let terminated=false,failed=false;
 worker.terminate=()=>terminated=true;
 const watch=watchWorker(worker,()=>failed=true,40);
 watch.start();await pause(25);watch.start();await pause(25);
 assert.ok(terminated&&failed);
});
test('real progress extends the deadline and completion cancels it',async()=>{
 const worker=new EventTarget();worker.terminate=()=>assert.fail('completed worker terminated');
 const watch=watchWorker(worker,()=>assert.fail('unexpected timeout'),80);
 watch.start();await pause(50);worker.dispatchEvent(new Event('message'));await pause(50);
 watch.stop();await pause(90);
});
