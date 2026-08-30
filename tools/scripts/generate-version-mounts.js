'use strict';

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const defaultContentRoot = path.join(repositoryRoot, 'content');
const defaultBaseConfig = path.join(defaultContentRoot, 'hugo.yaml');
const defaultOutput = path.join(repositoryRoot, 'tools', 'generated', 'hugo.yaml');
const mountMarker = '    # GENERATED_VERSION_MOUNTS';

const productSources = [
  {
    source: 'riak-kv',
    target: 'openriak-kv',
    minVersion: '2.0.0',
    maxVersionExclusive: '3.4.0'
  },
  {
    source: 'openriak-kv',
    target: 'openriak-kv',
    minVersion: '3.4.0'
  },
  { source: 'openriak-cs', target: 'openriak-cs' },
  { source: 'openriak-ts', target: 'openriak-ts' }
];

const semverPattern = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?$/;

const parseSemver = (value) => {
  const match = semverPattern.exec(value);
  if (!match) throw new Error(`Invalid semantic version directory: ${value}`);
  return {
    raw: value,
    major: Number(match[1]),
    minor: Number(match[2]),
    patch: Number(match[3]),
    prerelease: match[4] ? match[4].split('.') : []
  };
};

const compareIdentifiers = (left, right) => {
  const leftNumeric = /^\d+$/.test(left);
  const rightNumeric = /^\d+$/.test(right);
  if (leftNumeric && rightNumeric) return Number(left) - Number(right);
  if (leftNumeric !== rightNumeric) return leftNumeric ? -1 : 1;
  return left.localeCompare(right);
};

const compareSemver = (leftValue, rightValue) => {
  const left = typeof leftValue === 'string' ? parseSemver(leftValue) : leftValue;
  const right = typeof rightValue === 'string' ? parseSemver(rightValue) : rightValue;
  for (const key of ['major', 'minor', 'patch']) {
    if (left[key] !== right[key]) return left[key] - right[key];
  }
  if (!left.prerelease.length || !right.prerelease.length) {
    if (left.prerelease.length === right.prerelease.length) return 0;
    return left.prerelease.length ? -1 : 1;
  }
  const length = Math.max(left.prerelease.length, right.prerelease.length);
  for (let index = 0; index < length; index += 1) {
    if (left.prerelease[index] === undefined) return -1;
    if (right.prerelease[index] === undefined) return 1;
    const result = compareIdentifiers(left.prerelease[index], right.prerelease[index]);
    if (result) return result;
  }
  return 0;
};

const discoverVersions = (contentRoot, product) => {
  const productRoot = path.join(contentRoot, product.source);
  if (!fs.existsSync(productRoot)) {
    throw new Error(`Missing product source directory: content/${product.source}`);
  }

  const versions = fs.readdirSync(productRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^\d/.test(entry.name))
    .map((entry) => parseSemver(entry.name))
    .sort(compareSemver);

  for (const version of versions) {
    if (product.minVersion && compareSemver(version, product.minVersion) < 0) {
      throw new Error(`content/${product.source}/${version.raw} is below the supported minimum ${product.minVersion}`);
    }
    if (product.maxVersionExclusive && compareSemver(version, product.maxVersionExclusive) >= 0) {
      throw new Error(`content/${product.source}/${version.raw} must be below ${product.maxVersionExclusive}`);
    }
  }
  return versions;
};

const createVersionMounts = (contentRoot = defaultContentRoot, products = productSources) => {
  const mounts = [];
  const targets = new Set();

  for (const product of products) {
    const versions = discoverVersions(contentRoot, product);
    for (let targetIndex = 0; targetIndex < versions.length; targetIndex += 1) {
      const targetVersion = versions[targetIndex].raw;
      const targetKey = `${product.target}/${targetVersion}`;
      if (targets.has(targetKey)) throw new Error(`Duplicate generated target: content/${targetKey}`);
      targets.add(targetKey);

      for (let sourceIndex = targetIndex; sourceIndex >= 0; sourceIndex -= 1) {
        mounts.push({
          source: `${product.source}/${versions[sourceIndex].raw}`,
          target: `content/${product.target}/${targetVersion}`
        });
      }
    }
  }
  return mounts;
};

const renderMounts = (mounts) => [
  '    # BEGIN GENERATED VERSION MOUNTS — run tools/scripts/generate-version-mounts.js',
  ...mounts.map(({ source, target }) => `    - {source: '${source}', target: '${target}'}`),
  '    # END GENERATED VERSION MOUNTS'
].join('\n');

const generateConfig = ({
  contentRoot = defaultContentRoot,
  baseConfig = defaultBaseConfig,
  output = defaultOutput,
  products = productSources
} = {}) => {
  const source = fs.readFileSync(baseConfig, 'utf8');
  const markerCount = source.split(mountMarker).length - 1;
  if (markerCount !== 1) throw new Error(`Expected exactly one ${mountMarker.trim()} marker in ${baseConfig}`);

  const mounts = createVersionMounts(contentRoot, products);
  const generated = source.replace(mountMarker, renderMounts(mounts));
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, generated, 'utf8');
  return { mounts, output };
};

const parseArguments = (argumentsList) => {
  const options = {};
  for (let index = 0; index < argumentsList.length; index += 1) {
    const argument = argumentsList[index];
    if (argument === '--output') options.output = path.resolve(argumentsList[++index]);
    else if (argument === '--base-config') options.baseConfig = path.resolve(argumentsList[++index]);
    else if (argument === '--content-root') options.contentRoot = path.resolve(argumentsList[++index]);
    else throw new Error(`Unknown argument: ${argument}`);
  }
  return options;
};

if (require.main === module) {
  try {
    const result = generateConfig(parseArguments(process.argv.slice(2)));
    console.log(`Generated ${result.mounts.length} version mounts in ${result.output}`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

module.exports = {
  compareSemver,
  createVersionMounts,
  discoverVersions,
  generateConfig,
  parseSemver,
  productSources,
  renderMounts
};
