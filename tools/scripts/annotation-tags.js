'use strict';
const categories = ['feature', 'repository', 'module', 'concept'];
function validateTags(tags, file = 'annotation') {
  if (!tags || typeof tags !== 'object' || Array.isArray(tags) || Object.entries(tags).some(([category, values]) =>
    !categories.includes(category) || !Array.isArray(values) || values.some(value => typeof value !== 'string' || !/^[a-z0-9][a-z0-9_.+-]*$/.test(value)) || new Set(values).size !== values.length)) {
    throw new Error(`${file}: tags must use feature, repository, module or concept and unique lowercase identifiers`);
  }
  return tags;
}
function parseTags(body, file) {
  const tags = {};
  for (const line of body.split('\n').filter(line => line.trim())) {
    const match = line.match(/^(feature|repository|module|concept):\s*(.*?)\s*$/);
    if (!match || Object.hasOwn(tags, match[1])) throw new Error(`${file}: expected one category: comma-separated tags line per category`);
    tags[match[1]] = match[2] ? match[2].split(',').map(value => value.trim()) : [];
  }
  return validateTags(tags, file);
}
function mergeTags(layers) {
  return Object.fromEntries(categories.map(category => [category, [...new Set(layers.flatMap(tags => tags?.[category] || []))].sort()]));
}
module.exports = { categories, validateTags, parseTags, mergeTags };
