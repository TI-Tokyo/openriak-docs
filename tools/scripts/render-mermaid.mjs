import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { parse, render } from './vendor/pele/pele-1.9.0.mjs';
import { marked } from './vendor/marked/marked-18.1.1.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
// Keep the 640px CSS container breakpoint aligned with Pele's direction threshold.
export const diagramLayouts = { wide: 960, narrow: 320 };
export const sourceKey = source => createHash('sha256').update(source.trim()).digest('hex');

export function diagramSources(markdown) {
  const sources = [];
  marked.walkTokens(marked.lexer(markdown), token => {
    if (token.type === 'code' && /^mermaid(?:\s|$)/i.test(token.lang || '')) sources.push(token.text.trim());
  });
  return sources;
}

function* markdownFiles(directory) {
  if (!fs.existsSync(directory)) return;
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) yield* markdownFiles(filename);
    else if (entry.isFile() && entry.name.endsWith('.md')) yield filename;
  }
}

export function generate(contentRoot = path.join(root, 'content'), outputRoot = path.join(root, 'tools/generated/mermaid')) {
  // Only active content uses the core code-block hook. Archives build independently.
  const families = ['homepage', 'community', 'riak-kv', 'riak-cs', 'riak-ts', 'openriak-kv', 'openriak-cs', 'openriak-ts'];
  const diagrams = new Map();
  for (const family of families) {
    for (const filename of markdownFiles(path.join(contentRoot, family))) {
      for (const source of diagramSources(fs.readFileSync(filename, 'utf8'))) {
        const key = sourceKey(source);
        if (diagrams.has(key)) continue;
        try {
          if (source.includes('{{<') || source.includes('{{%')) throw new Error('Use literal Mermaid text; Hugo shortcodes are not supported inside diagrams');
          const model = parse(source);
          diagrams.set(key, Object.fromEntries(Object.entries(diagramLayouts).map(([layout, maxWidth]) => [
            layout, render(model, { idPrefix: '__OPENRIAK_DIAGRAM__', responsive: true,
              fontFamily: 'sans-serif', maxWidth, autoDirection: true, directionBreakpoint: 640 }).svg
          ])));
        } catch (error) {
          throw new Error(`Mermaid diagram in ${filename}: ${error.message}`, { cause: error });
        }
      }
    }
  }
  // Validate the entire input before changing outputs; unchanged assets retain mtimes.
  fs.mkdirSync(outputRoot, { recursive: true });
  const expected = new Set();
  for (const [key, layouts] of diagrams) {
    for (const [layout, svg] of Object.entries(layouts)) {
      const name = `${key}.${layout}.svg`;
      expected.add(name);
      const filename = path.join(outputRoot, name);
      if (fs.existsSync(filename) && fs.readFileSync(filename, 'utf8') === svg) continue;
      fs.writeFileSync(`${filename}.tmp`, svg);
      fs.renameSync(`${filename}.tmp`, filename);
    }
  }
  for (const file of fs.readdirSync(outputRoot)) {
    if (/^[a-f0-9]{64}(?:\.(?:wide|narrow))?\.svg$/.test(file) && !expected.has(file)) fs.unlinkSync(path.join(outputRoot, file));
  }
  return diagrams.size;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log('Usage: node tools/scripts/render-mermaid.mjs [--watch]\nGenerate Pele SVG assets before Hugo; --watch regenerates after Markdown edits.');
  } else {
    const args = process.argv.slice(2);
    if (args.some(arg => arg !== '--watch')) throw new Error('Unknown argument; use --help');
    console.log(`Generated ${generate()} Mermaid diagrams (wide and narrow SVGs).`);
    if (args.includes('--watch')) {
      let timer;
      fs.watch(path.join(root, 'content'), { recursive: true }, (_event, filename) => {
        if (filename && !String(filename).endsWith('.md')) return;
        clearTimeout(timer);
        timer = setTimeout(() => {
          try { console.log(`Generated ${generate()} Mermaid diagrams (wide and narrow SVGs).`); }
          catch (error) { console.error(error.message); }
        }, 180);
      });
    }
  }
}
