import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { diagramSources, generate, sourceKey } from './render-mermaid.mjs';

test('Markdown extraction respects outer fences, lists, blockquotes and CRLF', () => {
  assert.deepEqual(diagramSources('````markdown\n```mermaid\nnot a diagram\n```\n````'), []);
  assert.deepEqual(diagramSources('> ~~~mermaid\r\n> flowchart LR\r\n> A-->B\r\n> ~~~'), ['flowchart LR\nA-->B']);
  assert.deepEqual(diagramSources('- Example\n\n  ```mermaid\n  flowchart LR\n  A-->B\n  ```'), ['flowchart LR\nA-->B']);
});

test('build renders SVG, deduplicates sources, preserves mtimes and rejects broken input', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'openriak-mermaid-'));
  try {
    const content = path.join(root, 'content');
    const family = path.join(content, 'openriak-kv');
    const output = path.join(root, 'assets');
    fs.mkdirSync(family, { recursive: true });
    const source = 'flowchart LR\n accTitle: Test write\n A[Client]-->B[Coordinator]-->C[Replica]-->D[Storage]';
    const page = path.join(family, 'example.md');
    fs.writeFileSync(page, `\x60\x60\x60mermaid\n${source}\n\x60\x60\x60\n\n\x60\x60\x60mermaid\n${source}\n\x60\x60\x60`);
    assert.equal(generate(content, output), 1);
    const asset = path.join(output, `${sourceKey(source)}.wide.svg`);
    const svg = fs.readFileSync(asset, 'utf8');
    const narrowAsset = path.join(output, `${sourceKey(source)}.narrow.svg`);
    const narrow = fs.readFileSync(narrowAsset, 'utf8');
    assert.equal(fs.readdirSync(output).length, 2, 'duplicate sources produce only two layout assets');
    const position = (svg, id) => {
      const match = svg.match(new RegExp(`data-id="${id}" transform="translate\\(([^,]+),([^\\)]+)\\)"`));
      assert.ok(match, `node ${id} has a position`);
      return match.slice(1).map(Number);
    };
    const [wideA, wideB] = ['A', 'B'].map(id => position(svg, id));
    const [narrowA, narrowB] = ['A', 'B'].map(id => position(narrow, id));
    assert.equal(wideA[1], wideB[1], 'wide flowchart nodes share a row');
    assert.ok(wideB[0] > wideA[0]);
    assert.equal(narrowA[0], narrowB[0], 'narrow flowchart nodes share a column');
    assert.ok(narrowB[1] > narrowA[1]);
    assert.match(svg, /^<svg/);
    assert.match(svg, /Client/);
    assert.match(svg, /__OPENRIAK_DIAGRAM__/);
    assert.doesNotMatch(svg, /<script/);
    const mtime = fs.statSync(asset).mtimeMs;
    const narrowMtime = fs.statSync(narrowAsset).mtimeMs;
    const legacyAsset = path.join(output, `${sourceKey(source)}.svg`);
    fs.writeFileSync(legacyAsset, svg);
    generate(content, output);
    assert.equal(fs.statSync(asset).mtimeMs, mtime);
    assert.equal(fs.statSync(narrowAsset).mtimeMs, narrowMtime);
    assert.equal(fs.existsSync(legacyAsset), false, "obsolete single-layout assets are removed");
    fs.writeFileSync(page, '```mermaid\nflowchart LR\nA[Unclosed\n```');
    assert.throws(() => generate(content, output), /Mermaid diagram in .*example.md/);
    assert.equal(fs.readFileSync(asset, 'utf8'), svg);
    assert.equal(fs.readFileSync(narrowAsset, 'utf8'), narrow);
    fs.writeFileSync(page, 'No diagrams');
    assert.equal(generate(content, output), 0);
    assert.deepEqual(fs.readdirSync(output), []);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
