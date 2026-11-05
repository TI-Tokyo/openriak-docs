import {test} from 'node:test';
import assert from 'node:assert/strict';
import {sentences,makePassages} from './passages.mjs';
const count=text=>text.trim().split(/\s+/).length+2;
test('three-sentence windows roll by one sentence and carry title and heading',()=>{
 const p=makePassages('Article','# Heading\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence.',count);
 assert.deepEqual(p.map(p=>p.text),['First sentence. Second sentence. Third sentence.','Second sentence. Third sentence. Fourth sentence.','Third sentence. Fourth sentence. Fifth sentence.']);
 assert.ok(p.every(p=>p.input.startsWith('Article\nHeading\n')));
});
test('headings are boundaries and short sections remain searchable',()=>{
 const p=makePassages('Article','Intro.\n\n# One\n\nFirst sentence. Second sentence.\n\n# Two\n\nThird sentence.',count);
 assert.deepEqual(p.map(p=>[p.heading,p.text]),[['','Intro.'],['One','First sentence. Second sentence.'],['Two','Third sentence.']]);
});
test('prose windows cross paragraphs, but not code or list blocks',()=>{
 const p=makePassages('Article','# Heading\n\nFirst sentence.\n\nSecond sentence. Third sentence.\n\n```sh\nriak-admin status\necho 3.4.1\n```\n\n- Set n_val to 3.\n- Restart the node.\n\nFinal sentence.',count);
 assert.equal(p[0].text,'First sentence. Second sentence. Third sentence.');
 assert.ok(p.some(p=>p.kind==='code'&&p.text==='Third sentence. riak-admin status echo 3.4.1'));
 assert.ok(p.some(p=>p.kind==='list'&&p.text==='Set n_val to 3. Restart the node.'));
 assert.equal(p.at(-1).text,'Final sentence.');
});
test('technical punctuation and common abbreviations do not create false sentences',()=>{
 assert.deepEqual(sentences('Use v3.4.1 with `riak.conf`. See https://example.test/docs/a.b for details. Set a value, e.g. three replicas.'),['Use v3.4.1 with `riak.conf`.','See https://example.test/docs/a.b for details.','Set a value, e.g. three replicas.']);
});
test('oversized sentences and literals are split without losing their tail',()=>{
 const text=Array.from({length:600},(_,i)=>`word${i}`).join(' ')+'.';
 const p=makePassages('Article','# Heading\n\n'+text,count);
 assert.ok(p.every(p=>count(p.input)<=256));assert.equal(p.map(p=>p.text).join(' '),text);
 const huge='x'.repeat(600);const q=makePassages('A',huge,s=>s.length,256);
 assert.equal(q.map(p=>p.text).join(''),huge);assert.ok(q.every(p=>p.input.length<=256));
});
test('navigation and script content are excluded',()=>{
 const p=makePassages('Article','<nav>Ignore menu.</nav>\n\n<script>Ignore script.</script>\n\nUseful text.',count);
 assert.deepEqual(p.map(p=>p.text),['Useful text.']);
});
test('very long captured output uses bounded tokenizer probes',()=>{
 const text='x'.repeat(20000);
 const count=text=>{assert.ok(text.length<4200,'Do not repeatedly tokenise an entire large output line');return text.length;};
 const p=makePassages('Output','```text\n'+text+'\n```',count);
 assert.equal(p.map(p=>p.text).join(''),text);assert.ok(p.every(p=>p.input.length<=256));
});

test('mailing-list bodies retain direct text and nested reply content',()=>{
 const body='<section><article><div>First message. Second sentence. Third sentence.</div><details><summary>Reply</summary><div>A useful reply. More context. A final sentence.</div></details></article></section>';
 const chunks=makePassages('Thread',body,s=>s.split(/\s+/).length,256,true);
 assert.ok(chunks.some(p=>p.text.includes('First message.')));
 assert.ok(chunks.some(p=>p.text.includes('A useful reply.')));
});
