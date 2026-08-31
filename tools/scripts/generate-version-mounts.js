'use strict';

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const defaultContentRoot = path.join(repositoryRoot, 'content');
const defaultBaseConfig = path.join(defaultContentRoot, 'hugo.yaml');
const defaultOutput = path.join(repositoryRoot, 'tools', 'generated', 'hugo.yaml');
const defaultLatestRedirectRoot = path.join(repositoryRoot, 'tools', 'generated', 'latest-redirects');
const mountMarker = '    # GENERATED_VERSION_MOUNTS';
const latestAliases = {
  'openriak-kv': ['riak-kv']
};

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
const newReleaseSuffix = '-new-release';

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

const parseVersionDirectory = (sourceDirectory) => {
  const newRelease = sourceDirectory.endsWith(newReleaseSuffix);
  const version = newRelease
    ? sourceDirectory.slice(0, -newReleaseSuffix.length)
    : sourceDirectory;
  return {
    ...parseSemver(version),
    sourceDirectory,
    newRelease
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
    .map((entry) => parseVersionDirectory(entry.name))
    .sort(compareSemver);

  const publicVersions = new Set();

  for (const version of versions) {
    if (publicVersions.has(version.raw)) {
      throw new Error(`Duplicate public version ${version.raw} in content/${product.source}`);
    }
    publicVersions.add(version.raw);
    if (product.minVersion && compareSemver(version, product.minVersion) < 0) {
      throw new Error(`content/${product.source}/${version.sourceDirectory} is below the supported minimum ${product.minVersion}`);
    }
    if (product.maxVersionExclusive && compareSemver(version, product.maxVersionExclusive) >= 0) {
      throw new Error(`content/${product.source}/${version.sourceDirectory} must be below ${product.maxVersionExclusive}`);
    }
  }
  return versions;
};

const discoverLatestRedirects = (contentRoot, products = productSources) => {
  const latestByTarget = new Map();
  for (const product of products) {
    const versions = discoverVersions(contentRoot, product);
    if (!versions.length) continue;
    const version = versions[versions.length - 1];
    const current = latestByTarget.get(product.target);
    if (!current || compareSemver(version, current.version) > 0) {
      latestByTarget.set(product.target, { product, version });
    }
  }

  return [...latestByTarget.entries()].flatMap(([target, release]) => [target, ...(latestAliases[target] || [])]
    .map((route) => ({
      route,
      target,
      version: release.version.raw
    })));
};

const selectedVersionsFor = (includeVersions, source) => {
  const selected = includeVersions instanceof Map
    ? includeVersions.get(source)
    : includeVersions?.[source];
  return selected ? new Set(selected) : null;
};

const createVersionMounts = (contentRoot = defaultContentRoot, products = productSources, includeVersions = {}) => {
  const mounts = [];
  const targets = new Set();

  for (const product of products) {
    const versions = discoverVersions(contentRoot, product);
    const selectedVersions = selectedVersionsFor(includeVersions, product.source);
    if (selectedVersions) {
      const discovered = new Set(versions.map((version) => version.raw));
      for (const selected of selectedVersions) {
        if (!discovered.has(selected)) {
          throw new Error(`Requested version ${selected} does not exist in content/${product.source}`);
        }
      }
    }
    let baselineIndex = 0;
    for (let targetIndex = 0; targetIndex < versions.length; targetIndex += 1) {
      if (versions[targetIndex].newRelease) baselineIndex = targetIndex;
      const targetVersion = versions[targetIndex].raw;
      if (selectedVersions && !selectedVersions.has(targetVersion)) continue;
      const targetKey = `${product.target}/${targetVersion}`;
      if (targets.has(targetKey)) throw new Error(`Duplicate generated target: content/${targetKey}`);
      targets.add(targetKey);

      for (let sourceIndex = targetIndex; sourceIndex >= baselineIndex; sourceIndex -= 1) {
        mounts.push({
          source: `${product.source}/${versions[sourceIndex].sourceDirectory}`,
          target: `content/${product.target}/${targetVersion}`
        });
      }
    }
  }

  for (const redirect of discoverLatestRedirects(contentRoot, products)) {
    const releaseTarget = `content/${redirect.target}/${redirect.version}`;
    const latestTarget = `content/${redirect.route}/latest`;
    const releaseMounts = mounts.filter((mount) => mount.target === releaseTarget);
    if (redirect.route !== redirect.target) {
      mounts.push({
        source: `../tools/generated/latest-redirects/${redirect.route}-section`,
        target: `content/${redirect.route}`
      });
    }
    mounts.push({
      source: `../tools/generated/latest-redirects/${redirect.route}`,
      target: latestTarget
    });
    mounts.push(...releaseMounts.map((mount) => ({
      source: mount.source,
      target: latestTarget
    })));
  }
  return mounts;
};

const writeLatestRedirectRoots = (redirects, outputRoot = defaultLatestRedirectRoot) => {
  fs.rmSync(outputRoot, { recursive: true, force: true });
  for (const redirect of redirects) {
    const directory = path.join(outputRoot, redirect.route);
    fs.mkdirSync(directory, { recursive: true });
    const redirectParams = [
      `latest_redirect_route: ${redirect.route}`,
      `latest_redirect_product: ${redirect.target}`,
      `latest_redirect_version: ${redirect.version}`
    ];
    const source = [
      '---',
      `title: Latest ${redirect.target} documentation`,
      'layout: latest-redirect',
      'outputs: [HTML]',
      'sitemap:',
      '  disable: true',
      ...redirectParams,
      'type: product',
      `product_id: ${redirect.target}`,
      'build:',
      '  list: never',
      '  render: always',
      'cascade:',
      '  type: product',
      '  layout: latest-redirect',
      '  outputs: [HTML]',
      '  sitemap:',
      '    disable: true',
      '  build:',
      '    list: never',
      '    render: always',
      '  params:',
      `    product_id: ${redirect.target}`,
      ...redirectParams.map((line) => `    ${line}`),
      '---',
      ''
    ].join('\n');
    fs.writeFileSync(path.join(directory, '_index.md'), source, 'utf8');

    // An alias such as /riak-kv/latest/ creates a virtual parent section. Give
    // that parent a non-rendering source page so global section outputs do not
    // try to render or index a route that exists only to contain redirects.
    if (redirect.route !== redirect.target) {
      const sectionDirectory = path.join(outputRoot, `${redirect.route}-section`);
      fs.mkdirSync(sectionDirectory, { recursive: true });
      const sectionSource = [
        '---',
        `title: ${redirect.route} compatibility routes`,
        'type: product',
        `product_id: ${redirect.target}`,
        'outputs: []',
        'sitemap:',
        '  disable: true',
        'build:',
        '  list: never',
        '  render: never',
        'cascade:',
        '  type: product',
        '  params:',
        `    product_id: ${redirect.target}`,
        '---',
        ''
      ].join('\n');
      fs.writeFileSync(path.join(sectionDirectory, '_index.md'), sectionSource, 'utf8');
    }
  }
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
  latestRedirectRoot = defaultLatestRedirectRoot,
  products = productSources,
  includeVersions = {},
  versionDataRoot
} = {}) => {
  const source = fs.readFileSync(baseConfig, 'utf8');
  const markerCount = source.split(mountMarker).length - 1;
  if (markerCount !== 1) throw new Error(`Expected exactly one ${mountMarker.trim()} marker in ${baseConfig}`);

  const mounts = createVersionMounts(contentRoot, products, includeVersions);
  const latestRedirects = discoverLatestRedirects(contentRoot, products);
  writeLatestRedirectRoots(latestRedirects, latestRedirectRoot);
  let generated = source.replace(mountMarker, renderMounts(mounts));
  if (versionDataRoot) {
    const canonicalMount = "    - {source: '../tools/generated/openriak-kv/data/versions', target: 'data/versions/openriak-kv'}";
    if (!generated.includes(canonicalMount)) throw new Error('Unable to locate the OpenRiak KV version-data mount');
    const normalizedRoot = versionDataRoot.split(path.sep).join('/');
    generated = generated.replace(canonicalMount, `    - {source: '${normalizedRoot}', target: 'data/versions/openriak-kv'}`);
  }
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, generated, 'utf8');
  return { latestRedirects, mounts, output };
};

const parseArguments = (argumentsList) => {
  const options = { includeVersions: {} };
  for (let index = 0; index < argumentsList.length; index += 1) {
    const argument = argumentsList[index];
    if (argument === '--output') options.output = path.resolve(argumentsList[++index]);
    else if (argument === '--base-config') options.baseConfig = path.resolve(argumentsList[++index]);
    else if (argument === '--content-root') options.contentRoot = path.resolve(argumentsList[++index]);
    else if (argument === '--latest-redirect-root') options.latestRedirectRoot = path.resolve(argumentsList[++index]);
    else if (argument === '--version-data-root') options.versionDataRoot = path.resolve(argumentsList[++index]);
    else if (argument === '--include-version') {
      const value = argumentsList[++index] || '';
      const separator = value.indexOf('=');
      if (separator < 1 || separator === value.length - 1) {
        throw new Error('--include-version expects SOURCE=VERSION');
      }
      const source = value.slice(0, separator);
      const version = value.slice(separator + 1);
      parseSemver(version);
      (options.includeVersions[source] ||= []).push(version);
    }
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
  discoverLatestRedirects,
  discoverVersions,
  generateConfig,
  parseSemver,
  parseArguments,
  parseVersionDirectory,
  productSources,
  renderMounts,
  writeLatestRedirectRoots
};
