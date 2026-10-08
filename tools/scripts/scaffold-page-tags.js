'use strict';
const fs = require('node:fs');
const path = require('node:path');
const yaml = require('./vendor/js-yaml/js-yaml');
const {validateTags} = require('./annotation-tags');
const {annotationFiles, readMarkdownLayers} = require('./cli-annotation-markdown');
const {parseSetting} = require('./settings-annotations');

function tagPageSource(type, tag) {
  const label = type ? type[0].toUpperCase()+type.slice(1) : '';
  const params = {
    title:tag ? `${label}: ${tag}` : type ? `${label} tags` : 'Documentation tags',
    layout:'single', draft:true, reference_tag_page:true, hide_provenance:true,
    hide_reading_time:true, hide_sidebar:true, exclude_search:true, outputs:['HTML'],
    ...(tag ? {category:type, tag} : {})
  };
  return `---\n${yaml.dump(params)}---\n\n<!-- Add introductory text here. -->\n\n{{< tag-list >}}\n\n<!-- Add further context here. -->\n`;
}

// Collect every source used by command, settings and document tag links before
// Hugo runs. Missing pages are authored draft stubs, never generated substitutes.
function ensureVersionTagPages(release, product, {contentRoot, releaseDirectory} = {}) {
  const sets = [];
  for (const [key, source] of release.pages) {
    const front = source.match(/^---\n([\s\S]*?)\n---/);
    if (!front) continue;
    const params = yaml.load(front[1]);
    const tags = {...params.annotation_tags, ...(params.tags && !Array.isArray(params.tags) ? params.tags : {})};
    for (const [type, field] of Object.entries({feature:'features',concept:'concepts',repository:'repositories',module:'modules'})) {
      if(params[field]) tags[type] = [...new Set([...(tags[type] || []), ...params[field]])];
    }
    validateTags(tags, `${product}/${release.version}/${key}`);
    sets.push(tags);
  }
  const sourceProduct = path.basename(path.dirname(releaseDirectory));
  const annotations = path.join(contentRoot, 'annotations', sourceProduct);
  for (const layer of readMarkdownLayers(annotations, release.version)) {
    for (const entry of Object.values(layer.commands)) {
      if (entry.tags && (!entry.versions || entry.versions.includes(release.version))) sets.push(validateTags(entry.tags, layer.name));
    }
  }
  for (const file of annotationFiles(path.join(annotations,'settings'), release.version)) {
    const entry = parseSetting(fs.readFileSync(file,'utf8'),file);
    if (entry.tags) sets.push(validateTags(entry.tags,file));
  }
  const settingsFile = path.join(contentRoot,sourceProduct,'metadata',release.version,'kv-settings.json');
  if (fs.existsSync(settingsFile)) {
    const document = JSON.parse(fs.readFileSync(settingsFile,'utf8'));
    sets.push({metadata:[...new Set(Object.values(document.settings).flatMap(setting=>setting.tags || []))]});
  }
  const commandsFile = path.join(contentRoot,sourceProduct,'metadata',release.version,'kv-cli-commands.json');
  if (fs.existsSync(commandsFile)) {
    const document = JSON.parse(fs.readFileSync(commandsFile,'utf8'));
    for (const command of document.commands) if (command.reference?.tags) sets.push(validateTags(command.reference.tags,commandsFile));
  }
  const missing = new Map();
  for (const tags of sets) for (const [type, values] of Object.entries(tags)) for (const tag of values) {
    // Metadata tags retain their original case as labels (e.g. secretSettings).
    if (!/^[a-z0-9][a-z0-9_.+-]*$/i.test(tag)) throw new Error(`Invalid ${type} tag: ${tag}`);
    const slug = tag.toLowerCase();
    for (const [key, filename, contents] of [
      ['tags','tags/_index.md',tagPageSource()],
      [`tags/${type}`,`tags/${type}/_index.md`,tagPageSource(type)],
      [`tags/${type}/${slug}`,`tags/${type}/${slug}.md`,tagPageSource(type,tag)]
    ]) {
      if (!release.pages.has(key)) missing.set(key,{filename,contents});
    }
  }
  for (const [key,{filename,contents}] of missing) {
    const target = path.join(releaseDirectory, filename);
    fs.mkdirSync(path.dirname(target),{recursive:true});
    // Never overwrite an author's introduction, review state, or shortcode.
    if (!fs.existsSync(target)) fs.writeFileSync(target,contents);
    release.pages.set(key, fs.readFileSync(target,'utf8'));
  }
  return missing.size;
}
module.exports = {ensureVersionTagPages, tagPageSource};
