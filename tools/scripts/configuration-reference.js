'use strict';
const { labels, datatypeAlternatives } = require('./configuration-datatypes');
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

const configurationDatatype = (setting, validators) => {
  const datatype = setting.datatype || {};
  const type = String(datatype.type || 'unspecified');
  const simple = Object.hasOwn(labels, type);
  const alternatives = simple ? undefined : datatypeAlternatives(type);
  const options = type === 'enum'
    ? (datatype.values || [])
    : type === 'flag'
      ? (datatype.arguments || [])
      : simple ? [] : alternatives.map(choice => choice.value);
  const units = type === 'duration' ? (datatype.arguments || []) : [];
  const constraints = [...new Set((setting.validators || [])
    .map((name) => validators[name]?.message || name)
    .map(configurationConstraintText))];
  return {
    label: type === 'duration' && units.length
      ? `Duration (${units.map(configurationValueText).join(', ')})`
      : simple ? labels[type] : 'One of',
    options: options.map(configurationValueText),
    ...(!simple && {alternatives}),
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
