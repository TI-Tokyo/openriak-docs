'use strict';
const fs = require('node:fs');
const path = require('node:path');
const yaml = require('./vendor/js-yaml/js-yaml');
const {validateTags} = require('./annotation-tags');

function tagPageSource(type, tag) {
  const label = type ? type[0].toUpperCase()+type.slice(1) : '';
  const params = {
    title:tag ? `${label}: ${tag}` : type ? `${label} tags` : 'Documentation tags',
    layout:'single', reference_tag_page:true, hide_provenance:true,
    hide_reading_time:true, hide_sidebar:true, exclude_search:true, outputs:['HTML'],
    ...(tag ? {category:type, tag} : {})
  };
  return `---\n${yaml.dump(params)}---\n\n<!-- Add introductory text here. -->\n\n{{< tag-list >}}\n\n<!-- Add further context here. -->\n`;
}

// Validate the effective mounted release, including inherited tag pages. The
// build stages editable stubs outside read-only content before reporting errors.
function validateVersionTags(release, product, {stubRoot} = {}) {
  const missing = new Map();
  for (const [key, source] of release.pages) {
    const front = source.match(/^---\n([\s\S]*?)\n---/);
    if (!front || !/^(features|concepts):/m.test(front[1])) continue;
    const params = yaml.load(front[1]);
    const tags = {feature:params.features || [], concept:params.concepts || []};
    validateTags(tags, `${product}/${release.version}/${key}`);
    for (const [type, values] of Object.entries(tags)) for (const tag of values) {
      for (const [required, filename, contents] of [
        ['tags','tags/_index.md',tagPageSource()],
        [`tags/${type}`,`tags/${type}/_index.md`,tagPageSource(type)],
        [`tags/${type}/${tag}`,`tags/${type}/${tag}.md`,tagPageSource(type,tag)]
      ]) {
        if (!release.pages.has(required)) missing.set(required,{filename,contents,referencedBy:key});
      }
    }
  }
  if (!missing.size) return;
  const destination = stubRoot && path.join(stubRoot, product, release.sourceDirectory || release.version);
  if (destination) for (const {filename,contents} of missing.values()) {
    const target = path.join(destination,filename);
    fs.mkdirSync(path.dirname(target),{recursive:true});
    if (!fs.existsSync(target)) fs.writeFileSync(target,contents);
  }
  throw new Error(`${product} ${release.version}: missing Markdown tag pages:\n`+
    [...missing].map(([key,{referencedBy}])=>`  ${key} (referenced by ${referencedBy})`).join('\n')+
    (destination ? `\nStub files created in ${destination}. Add them to the matching content release directory, then rebuild.` : ''));
}
module.exports = {validateVersionTags, tagPageSource};
