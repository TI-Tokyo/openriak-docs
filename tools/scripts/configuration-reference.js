'use strict';
const configurationValueText = (value) => {
  if (typeof value === 'string') return value;
  if (value === null || value === undefined) return '';
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return JSON.stringify(value);
};

const configurationConstraintText = (value) => {
  if (value && typeof value === 'object' && typeof value.$erlang_expression === 'string') {
    return `Calculated at runtime: \`${value.$erlang_expression}\``;
  }
  return configurationValueText(value);
};

const complexDatatypeOptions = (type) => {
  const options = [];
  const add = (value) => { if (value && !options.includes(value)) options.push(value); };
  for (const match of type.matchAll(/'\$erlang_tuple': \['atom', '([^']+)'\]/g)) add(match[1]);
  for (const match of type.matchAll(/'\$erlang_tuple': \['integer', (\d+)\]/g)) add(match[1]);
  for (const match of type.matchAll(/'\$erlang_tuple': \['duration', '([^']+)'\]/g)) add(`duration (${match[1]})`);
  for (const match of type.matchAll(/'\$erlang_tuple': \['enum', \[([^\]]+)\]\]/g)) {
    for (const value of match[1].matchAll(/'([^']+)'/g)) add(value[1]);
  }
  for (const match of type.matchAll(/'(integer|flag|bytesize|string|atom|float|directory|file|ip|list)'/g)) add(match[1]);
  return options;
};

const configurationDatatype = (setting, validators) => {
  const datatype = setting.datatype || {};
  const type = String(datatype.type || 'unspecified');
  const labels = {
    atom: 'Atom',
    bytesize: 'Byte size',
    directory: 'Directory path',
    duration: 'Duration',
    enum: 'Enum',
    file: 'File path',
    flag: 'Flag',
    float: 'Floating-point number',
    integer: 'Integer',
    ip: 'IP address',
    list: 'List',
    percent: 'Percentage',
    string: 'String',
    unspecified: 'Unspecified'
  };
  const simple = Object.hasOwn(labels, type);
  const options = type === 'enum'
    ? (datatype.values || [])
    : type === 'flag'
      ? (datatype.arguments || [])
      : simple ? [] : complexDatatypeOptions(type);
  const units = type === 'duration' ? (datatype.arguments || []) : [];
  const constraints = [...new Set((setting.validators || [])
    .map((name) => validators[name]?.message || name)
    .map(configurationConstraintText))];
  return {
    label: simple ? labels[type] : 'One of',
    options: options.map(configurationValueText),
    units: units.map(configurationValueText),
    constraints
  };
};

const configurationReference = (product, version, defaults, operatingSystems) => {
  const nativeOperatingSystems = operatingSystems.filter((os) => !os.aliasOf);
  const globalDefaultOperatingSystem = nativeOperatingSystems.find((os) => os.id === 'ubuntu-noble-amd64')
    || nativeOperatingSystems[0];
  const settings = Object.entries(defaults.settings || {})
    .filter(([, setting]) => !setting.hidden)
    .map(([name, setting]) => {
      const defaultsByOs = {};
      for (const os of operatingSystems) {
        const effective = defaults.effective_defaults?.[os.defaultsKey]?.[name];
        if (!effective?.has_default) {
          defaultsByOs[os.defaultsKey] = { hasDefault: false, value: '' };
          continue;
        }
        const value = effective.resolved_value ?? effective.value;
        defaultsByOs[os.defaultsKey] = { hasDefault: true, value: configurationValueText(value) };
      }
      const globalDefault = defaultsByOs[globalDefaultOperatingSystem?.defaultsKey] || { hasDefault: false, value: '' };
      for (const osDefault of Object.values(defaultsByOs)) {
        osDefault.osSpecific = osDefault.hasDefault !== globalDefault.hasDefault
          || (osDefault.hasDefault && osDefault.value !== globalDefault.value);
      }
      return {
        name,
        internalName: setting.erlang_target || '',
        description: setting.documentation || '',
        areas: [...new Set((setting.definitions || []).map((definition) => definition.repository).filter(Boolean))].sort(),
        datatype: configurationDatatype(setting, defaults.validators || {}),
        defaults: defaultsByOs
      };
    })
    .sort((left, right) => left.name.localeCompare(right.name, undefined, { numeric: true }));
  return { product: product.productId, version, settings };
};

module.exports = { configurationReference };
