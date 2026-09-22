'use strict';

const unique = items => [...new Set(items)];
const normalize = text => text.replace(/^\s*usage\b\s*:?\s*/i, '')
  .replace(/^riak-admin\b/, 'riak admin').replace(/^_ /, 'riak admin ').replace(/\s+/g, ' ').trim();
const plain = text => ({text});
const form = (tokens, label) => ({label, tokens, text: tokens.map(t => t.text).join('')});
const active = page => !['unavailable', 'help_only'].includes(page.availability);

function prefixTokens(words) {
  return [plain(words.join(' '))];
}
function bracketed(text, parameter, issues) {
  if (typeof parameter.required !== 'boolean') issues.push(`Whether ${parameter.name} is required is not recorded.`);
  if (typeof parameter.repeatable !== 'boolean') issues.push(`Whether ${parameter.name} is repeatable is not recorded.`);
  if (parameter.repeatable) text += ' ...';
  return parameter.required === false ? `[${text}]` : text;
}
function leafCandidates(page, items, reference, issues) {
  const variants = unique(items.filter(c => !c.path.includes('help')).map(c => {
    const literalTail = c.path.slice(page.path.length).filter(p => p !== '*');
    return [page.title, ...literalTail].join(' ');
  }));
  const args = page.parameters.filter(p => p.kind === 'Argument');
  const options = page.parameters.filter(p => p.kind === 'Option');
  if (items.some(c => c.arguments === 'unrestricted')) issues.push('The number and requiredness of unrestricted key=value arguments are not recorded.');
  if (items.some(c => c.wildcard_path) && !args.length) issues.push('The wildcard argument has no recorded name or structure.');
  if (page.forms.some(f => f.syntax.length > 1)) issues.push('The supplied usage has multiple forms; their argument relationships need review.');
  if (unique(items.map(c => JSON.stringify([c.arguments,c.options,c.global_options]))).length > 1) issues.push('Recorded variants have different parameter declarations; their applicability needs review.');
  // A list of usage placeholders cannot establish order, alternatives or mutual exclusion.
  if (items.some(c => Array.isArray(c.arguments) && c.arguments.some(a => a.source === 'usage_placeholder')) && !page.reference.argumentsDefined) {
    issues.push('Argument metadata was extracted as usage placeholders; positional order and grouping need review.');
  }
  const argumentText = args.map(a => {
    if (!a.name || /^Argument \d+$/.test(a.name)) issues.push('An argument has no recorded name.');
    const assignment = items.some(c => c.argument_format === 'key=value') && Boolean(a.key);
    return bracketed(assignment ? `${a.key}=<${a.name}>` : `<${a.name}>`, a, issues);
  });
  const helpOption = items.some(c => (c.global_options || []).some(o => o.name === '--help'))
    ? options.find(o => o.name === '--help') : null;
  const optionText = options.filter(o => o !== helpOption).map(o => {
    let suffix = '';
    if (o.allowedValues?.length) suffix = ` {${o.allowedValues.join('|')}}`;
    else if (o.value) suffix = ` <${o.value}>`;
    else if (!/^(boolean|bool|flag \(no value\))$/.test(o.datatype)) {
      issues.push(`Whether ${o.name} takes a value is not recorded.`);
      suffix = ' <value?>';
    }
    return bracketed(`${o.name}${o.short ? '|' + o.short : ''}${suffix}`, o, issues);
  });
  const forms = (variants.length ? variants : [page.title]).map(variant => form([
    ...prefixTokens(variant.split(' ')),
    ...[...argumentText, ...optionText].map(text => plain(' ' + text))
  ], variant));
  if (helpOption) forms.push(form([...prefixTokens(page.path),plain(` {${helpOption.name}${helpOption.short ? '|'+helpOption.short : ''}}`)],page.title+' — help'));
  return forms;
}

function suppliedForm(text, page, reference, choices) {
  const value = normalize(text);
  if (!value.startsWith(page.title)) return form([plain(value)],page.title);
  const tokens = prefixTokens(page.path);
  // Link discovered choices even when an incomplete parent retains supplied usage.
  const suffix = value.slice(page.title.length).split(/([A-Za-z_][\w-]*)/);
  for (const part of suffix) {
    const choice = choices.find(c => c.name === part);
    tokens.push(choice ? {text:part,route:choice.route} : plain(part));
  }
  return form(tokens,page.title);
}

function childChoices(page, reference) {
  // Include intermediate section pages, not just commands with their own runtime entry.
  return [...reference.pages, ...reference.sections].filter(p => p.route.startsWith(page.route + '/') &&
    !p.route.slice(page.route.length + 1).includes('/') && active(p))
    .map(p => ({name: p.path?.at(-1) || p.title, route: p.route}))
    .sort((a,b) => a.name.localeCompare(b.name));
}
function directSuppliedChoices(page, provided, reference) {
  const text = provided.find(s => normalize(s).startsWith(page.title + ' {'));
  if (!text) return null;
  const body = normalize(text).slice(page.title.length + 2);
  const branches = []; let depth = 0, current = '';
  for (const char of body) {
    if (char === '}' && depth === 0) {branches.push(current); break;}
    if (char === '|' && depth === 0) {branches.push(current);current='';continue;}
    if ('[{(<'.includes(char)) depth++;
    if (']})>'.includes(char)) depth--;
    current += char;
  }
  return unique(branches.map(b => b.trim().split(/\s+/)[0]).filter(Boolean).map(name => {
    const alias = reference.pages.find(p => p.aliases?.includes(page.title + ' ' + name));
    return alias?.path.at(-1) || name;
  })).sort();
}
function buildSyntax(reference, document) {
  const byId = new Map(document.commands.map(c => [c.id,c]));
  const reviews = [];
  for (const page of reference.pages) {
    const items = page.ids.map(id => byId.get(id));
    const supplied = unique(items.flatMap(c => c.context === 'erlang' ? (c.signatures || []).map(s => `${c.module}:${s}.`) : c.usage || []));
    const issues = []; let candidates, basis, incomplete = false;
    const choices = page.context === 'shell' ? childChoices(page, reference) : [];
    if (page.context === 'erlang') {
      // Function heads and selector expressions already come from the inspected Erlang AST.
      candidates = page.forms.flatMap(f => f.syntax.map(s => form([plain(s)],f.label)));
      basis = 'erlang_ast';
      if (!candidates.length) issues.push('No Erlang signature or selector expression was discovered.');
    } else if (choices.length) {
      const tokens = [...prefixTokens(page.path), plain(' { ')];
      choices.forEach((c,i) => tokens.push(...(i ? [plain(' | ')] : []),{text:c.name,route:c.route}));
      tokens.push(plain(' }'));
      candidates = [form(tokens,page.title)]; basis = 'command_tree';
      // Usage-derived flags on a parent can belong to a child (e.g. admin top).
      const ownOptions = items.flatMap(c => [...(c.options || []),...(c.global_options || [])]).filter(o => o.source !== 'usage');
      const usageOptions = unique(items.flatMap(c => c.options || []).filter(o => o.source === 'usage').map(o=>o.name));
      if (usageOptions.length) issues.push(`Options scraped from this parent's usage may belong to subcommands and are omitted from the parent form: ${usageOptions.join(', ')}.`);
      if (ownOptions.length || items.some(c => Array.isArray(c.arguments) && c.arguments.some(a => a.source !== 'usage_placeholder'))) {
        issues.push('This parent also has argument or option declarations; their position relative to subcommands needs review.');
        incomplete = true;
      }
    } else {
      candidates = leafCandidates(page,items,reference,issues);basis = 'arguments_and_options';incomplete = issues.length > 0;
    }
    if (page.context === 'shell' && !supplied.length) issues.push('No supplied usage is available for comparison.');
    const generated = unique(candidates.map(f => f.text));
    const expected = unique(generated.map(normalize)).sort();
    const actual = unique(supplied.map(normalize)).sort();
    const differs = supplied.length > 0 && JSON.stringify(expected) !== JSON.stringify(actual);
    if (differs) issues.push('Generated and supplied syntax differ; review the forms below (including order, grouping and option values).');
    if (page.context === 'shell' && !choices.length && differs) {
      const words = text => normalize(text).match(/--?[\w-]+|[A-Za-z_][\w.-]*/g) || [];
      const known = new Set(generated.flatMap(words).map(w=>w.toLowerCase()));
      const unrepresented = unique(supplied.flatMap(words).filter(w=>!known.has(w.toLowerCase())));
      if (unrepresented.length) {
        issues.push(`Supplied syntax contains terms absent from the structured form: ${unrepresented.join(', ')}. Check for missing arguments, options or constraints.`);
        incomplete = true;
      }
    }
    const suppliedChoices = choices.length ? directSuppliedChoices(page,supplied,reference) : null;
    const discoveredChoices = choices.map(c=>c.name).sort();
    const missingFromProvided = suppliedChoices ? discoveredChoices.filter(n=>!suppliedChoices.includes(n)) : [];
    const onlyInProvided = suppliedChoices ? suppliedChoices.filter(n=>!discoveredChoices.includes(n)) : [];
    if (missingFromProvided.length) issues.push(`Discovered subcommands missing from the supplied alternatives: ${missingFromProvided.join(', ')}.`);
    if (onlyInProvided.length) issues.push(`Supplied alternatives absent from the discovered subcommands: ${onlyInProvided.join(', ')}.`);
    if (page.reference.syntax) issues.push('A docs annotation overrides the displayed syntax; review it against the generated and supplied forms.');
    const fallback = incomplete && supplied.length > 0;
    const displayed = fallback ? supplied.map(s => suppliedForm(s,page,reference,choices)) : candidates;
    // Never publish incomplete candidate guesses. If no source exists, show only the known command path.
    const forms = incomplete && !supplied.length ? [form(prefixTokens(page.path),page.title)] : displayed;
    page.syntax = {forms,basis: fallback ? 'supplied_usage' : basis,hasSubcommands:choices.length > 0,
      reviewRequired:issues.length > 0};
    const review = {key:page.key,route:page.route,status:issues.length ? 'needs_review' : 'matched',basis,
      displayed:page.reference.syntax ? 'editorial_override' : fallback ? 'supplied_usage' : incomplete ? 'known_path_only' : 'generated',
      issues:unique(issues),generated,supplied,missingFromProvided,onlyInProvided,
      ...(page.reference.syntax ? {editorial:page.reference.syntax} : {})};
    page.syntax.review = review;reviews.push(review);
  }
  reference.syntaxReview = {version:document.version,total:reviews.length,
    needsReview:reviews.filter(r=>r.status==='needs_review').length,commands:reviews};
  return reference;
}
function reviewMarkdown(report) {
  const output = [`# OpenRiak KV ${report.version}: syntax review`, '',
    `${report.needsReview} of ${report.total} command topics need manual review.`, '',
    'Generated forms use the command tree, structured argument/option metadata and docs annotations. Supplied forms are retained for comparison. Whitespace and the riak-admin spelling are normalized; other differences are flagged conservatively, including differences that may be equivalent syntax.', '',
    'Incomplete candidates are review material, not verified invocations. Pages retain supplied usage when requiredness, repetition, value arity or grouping is unknown. No source metadata is rewritten.', ''];
  for (const entry of report.commands.filter(r=>r.status==='needs_review')) {
    output.push(`## ${entry.key}`, '', `Page: \`reference/commands/${entry.route}/\``, '', `Displayed: ${entry.displayed}`, '', ...entry.issues.map(i=>'- '+i), '', '### Generated candidates', '', '```text', ...entry.generated, '```', '', '### Supplied syntax', '', '```text', ...(entry.supplied.length ? entry.supplied : ['(not supplied)']), '```', '');
    if (entry.editorial) output.push('### Editorial syntax', '',entry.editorial,'');
  }
  return output.join('\n');
}
module.exports = {buildSyntax,reviewMarkdown,normalize};
