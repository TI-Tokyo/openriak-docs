'use strict';

const labels = {
  atom: 'Atom', bytesize: 'Byte size', directory: 'Directory path', duration: 'Duration',
  enum: 'Enum', file: 'File path', flag: 'Flag', float: 'Floating-point number',
  integer: 'Integer', ip: 'IP address', fqdn: 'Hostname', list: 'List',
  percent: 'Percentage', string: 'String', unspecified: 'Unspecified'
};

// Metadata serializes compound datatypes as Python-style lists/dicts. Parse
// this data-only subset without evaluating code or scanning inside tuple values.
function parseDatatype(text) {
  let position = 0;
  const skip = () => { while (/\s/.test(text[position] || '') && position < text.length) position++; };
  const expect = character => {
    skip();
    if (text[position++] !== character) throw new Error(`Invalid datatype expression: ${text}`);
  };
  function value() {
    skip();
    const start = text[position];
    if (start === "'" || start === '"') {
      position++;
      let result = '';
      while (position < text.length) {
        const character = text[position++];
        if (character === start) return result;
        if (character !== '\\') { result += character; continue; }
        const escaped = text[position++];
        const escapes = {n:'\n', r:'\r', t:'\t', b:'\b', f:'\f', '\\':'\\', "'":"'", '"':'"'};
        if (Object.hasOwn(escapes, escaped)) result += escapes[escaped];
        else throw new Error(`Unsupported escape in datatype: ${text}`);
      }
      throw new Error(`Unterminated datatype string: ${text}`);
    }
    if (start === '[' || start === '{') {
      position++;
      const array = start === '[', end = array ? ']' : '}';
      const result = array ? [] : Object.create(null);
      skip();
      while (text[position] !== end) {
        const item = value();
        if (array) result.push(item);
        else { expect(':'); result[item] = value(); }
        skip();
        if (text[position] === end) break;
        expect(',');
        skip();
      }
      expect(end);
      return result;
    }
    const number = text.slice(position).match(/^-?\d+(?:\.\d+)?/);
    if (number) { position += number[0].length; return Number(number[0]); }
    throw new Error(`Unsupported datatype expression: ${text}`);
  }
  const parsed = value();
  skip();
  if (position !== text.length) throw new Error(`Trailing datatype expression: ${text}`);
  return parsed;
}

function datatypeAlternatives(type) {
  const choices = [];
  const add = (kind, value) => {
    value = String(value);
    if (!choices.some(choice => choice.kind === kind && choice.value === value)) choices.push({kind, value});
  };
  function visit(term) {
    if (Array.isArray(term)) { term.forEach(visit); return; }
    if (typeof term === 'string') {
      if (term === 'flag') { add('value', 'on'); add('value', 'off'); }
      else add('type', labels[term] || term);
      return;
    }
    const tuple = term?.$erlang_tuple;
    if (!Array.isArray(tuple)) throw new Error(`Unsupported compound datatype: ${type}`);
    const [name, argument] = tuple;
    if (name === 'enum') argument.forEach(value => add('value', value));
    else if (name === 'duration' || name === 'percent') add('type', `${labels[name]} (${argument})`);
    else if (name === 'flag') tuple.slice(1).forEach(value => add('value', value?.$erlang_tuple?.[0] ?? value));
    else if (['atom', 'integer', 'string', 'float', 'bytesize', 'file', 'directory'].includes(name)) add('value', argument);
    else throw new Error(`Unsupported compound datatype: ${type}`);
  }
  visit(parseDatatype(type));
  return choices;
}

module.exports = { labels, datatypeAlternatives };
