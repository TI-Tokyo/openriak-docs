'use strict';

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const contentRoot = path.join(repositoryRoot, 'content');
const productRoot = path.join(repositoryRoot, 'content', 'openriak-kv');
const generatedDataRoot = path.join(repositoryRoot, 'tools', 'generated', 'openriak-kv', 'data');
const metadataProduct = 'kv';
const productId = 'openriak-kv';
const { compareSemver, discoverVersions, productSources } = require('./generate-version-mounts.js');
const versionEntries = productSources
  .filter((product) => product.target === productId)
  .flatMap((product) => discoverVersions(contentRoot, product).map((version) => ({
    version: version.raw,
    sourceDirectory: version.sourceDirectory,
    source: product.source,
    hasMetadata: product.source === productId
  })))
  .sort((left, right) => compareSemver(left.version, right.version));

const familyNames = {
  alpine: 'Alpine Linux',
  'amazon-linux': 'Amazon Linux',
  debian: 'Debian',
  'oracle-linux': 'Oracle Linux',
  rhel: 'Red Hat Enterprise Linux',
  ubuntu: 'Ubuntu'
};

const familyLogos = {
  alpine: 'images/os/linux.svg',
  'amazon-linux': 'images/os/linux.svg',
  debian: 'images/os/debian.svg',
  'oracle-linux': 'images/os/linux.svg',
  rhel: 'images/os/red-hat.svg',
  ubuntu: 'images/os/ubuntu.svg'
};

const preferredFamilyDefaults = {
  alpine: 'alpine-3.21-x86_64',
  'amazon-linux': 'amazon-linux-2023-x86_64',
  debian: 'debian-12-amd64',
  'oracle-linux': 'oracle-linux-9-x86_64',
  rhel: 'rhel-9-x86_64',
  ubuntu: 'ubuntu-noble-amd64'
};

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const versionsRoot = path.join(generatedDataRoot, 'versions');
const writeVersionData = (version, output) => {
  const target = path.join(versionsRoot, `${version}.json`);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, `${JSON.stringify(output, null, 2)}\n`, 'utf8');
};

const referencedValueKeys = () => {
  const keys = new Set();
  const visit = (directory) => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const target = path.join(directory, entry.name);
      if (entry.isDirectory()) visit(target);
      else if (entry.name.endsWith('.md')) {
        const source = fs.readFileSync(target, 'utf8');
        for (const match of source.matchAll(/load-value[\s\S]*?key="([^"]+)"[\s\S]*?>}}/g)) keys.add(match[1]);
      }
    }
  };
  visit(productRoot);
  return keys;
};

const downloadVariant = (url) => {
  const decoded = decodeURIComponent(url);
  const match = decoded.match(/\((graviton\s*\d+)\)/i);
  return match ? match[1].replace(/graviton\s*/i, 'Graviton ') : '';
};

for (const { version, sourceDirectory, source, hasMetadata } of versionEntries) {
  if (!hasMetadata) {
    writeVersionData(version, {
      product: productId,
      version,
      generatedFrom: `content/${source}/${sourceDirectory}`,
      metadataStatus: {
        supportedOs: 'unavailable',
        downloads: 'unavailable',
        defaults: 'unavailable'
      },
      metadataWarnings: ['No structured operating-system, download, or default-value metadata is available for this legacy release.'],
      defaultOs: null,
      operatingSystems: [],
      downloads: {},
      values: {}
    });
    console.log(`Synced ${productId} ${version}: legacy content without structured OS metadata.`);
    continue;
  }

  const metadataRoot = path.join(productRoot, 'metadata', version);
  const files = {
    supported: path.join(metadataRoot, 'supported-os.json'),
    downloads: path.join(metadataRoot, 'downloads.json'),
    defaults: path.join(metadataRoot, 'defaults.json')
  };
  for (const file of Object.values(files)) {
    if (!fs.existsSync(file)) throw new Error(`Incomplete metadata for ${metadataProduct}/${version}: missing ${path.basename(file)}`);
  }

  const supported = readJson(files.supported);
  const downloads = readJson(files.downloads);
  const defaults = readJson(files.defaults);
  for (const [name, document] of Object.entries({ supported, downloads, defaults })) {
    const acceptedStatuses = name === 'defaults' ? ['complete', 'partial'] : ['complete'];
    if (!acceptedStatuses.includes(document.status)) throw new Error(`Incomplete ${name} metadata for ${metadataProduct}/${version}: ${document.status}`);
    if (document.product !== metadataProduct || document.version !== version) throw new Error(`Mismatched ${name} metadata for ${metadataProduct}/${version}`);
  }

  const requestedKeys = referencedValueKeys();
  const requiredValueKeys = ['ring_size', 'nodename'];
  const operatingSystems = supported.operating_systems.map((os) => ({
    id: os.id,
    family: os.family,
    name: familyNames[os.family] || os.display_name,
    displayName: os.display_name,
    version: os.release_version || os.release,
    codename: os.source_label || os.architecture,
    architecture: os.architecture,
    packageFamily: os.package_family,
    logo: familyLogos[os.family] || 'images/os/linux.svg',
    defaultForFamily: preferredFamilyDefaults[os.family] === os.id
  }));

  const values = {};
  for (const os of operatingSystems) {
    const effective = defaults.effective_defaults[os.id] || {};
    values[os.id] = {};
    for (const key of requestedKeys) {
      const setting = effective[key];
      if (!setting || !setting.has_default) continue;
      const value = setting.resolved_value ?? setting.value;
      if (value !== null && value !== undefined) values[os.id][key] = value;
    }
  }

  for (const os of operatingSystems) {
    for (const key of requiredValueKeys) {
      if (!(key in values[os.id])) throw new Error(`Missing required default ${key} for ${metadataProduct}/${version}/${os.id}`);
    }
  }

  const normalizedDownloads = {};
  for (const os of operatingSystems) {
    normalizedDownloads[os.id] = Object.entries(downloads.downloads[os.id] || {})
      .map(([id, item]) => ({
        id,
        otp: item.otp,
        architecture: item.architecture,
        format: item.format,
        filename: item.filename,
        packageRevision: item.package_revision,
        variant: downloadVariant(item.url),
        url: item.url,
        checksumUrl: item.checksum_url
      }))
      .sort((left, right) => left.otp - right.otp || left.id.localeCompare(right.id));
  }

  const output = {
    product: productId,
    version,
    generatedFrom: `content/openriak-kv/metadata/${version}`,
    metadataSchemaVersion: supported.schema_version,
    metadataStatus: {
      supportedOs: supported.status,
      downloads: downloads.status,
      defaults: defaults.status
    },
    metadataWarnings: defaults.warnings || [],
    defaultOs: operatingSystems.some((os) => os.id === 'ubuntu-noble-amd64') ? 'ubuntu-noble-amd64' : operatingSystems[0]?.id,
    operatingSystems,
    downloads: normalizedDownloads,
    values
  };

  writeVersionData(version, output);
  console.log(`Synced ${productId} ${version}: ${operatingSystems.length} OS targets, ${Object.values(normalizedDownloads).flat().length} downloads, ${requestedKeys.size} referenced value keys.`);
}

const expectedVersionFiles = new Set(versionEntries.map(({ version }) => `${version}.json`));
for (const entry of fs.readdirSync(versionsRoot, { withFileTypes: true })) {
  if (entry.isFile() && entry.name.endsWith('.json') && !expectedVersionFiles.has(entry.name)) {
    fs.rmSync(path.join(versionsRoot, entry.name));
    console.log(`Removed stale ${productId} version metadata: ${entry.name}`);
  }
}
