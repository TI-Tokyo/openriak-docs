'use strict';

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const contentRoot = path.join(repositoryRoot, 'content');
const productRoot = path.join(repositoryRoot, 'content', 'openriak-kv');
const metadataProduct = 'kv';
const productId = 'openriak-kv';
const { compareSemver, discoverVersions, productSources } = require('./generate-version-mounts.js');
const parseOptions = (argumentsList) => {
  const options = { includeVersions: {} };
  for (let index = 0; index < argumentsList.length; index += 1) {
    if (argumentsList[index] === '--output-root') {
      options.outputRoot = path.resolve(argumentsList[++index] || '');
      continue;
    }
    if (argumentsList[index] !== '--include-version') throw new Error(`Unknown argument: ${argumentsList[index]}`);
    const value = argumentsList[++index] || '';
    const separator = value.indexOf('=');
    if (separator < 1 || separator === value.length - 1) throw new Error('--include-version expects SOURCE=VERSION');
    const source = value.slice(0, separator);
    const version = value.slice(separator + 1);
    (options.includeVersions[source] ||= new Set()).add(version);
  }
  return options;
};
const options = parseOptions(process.argv.slice(2));
const includedVersions = options.includeVersions;
const generatedDataRoot = options.outputRoot || path.join(repositoryRoot, 'tools', 'generated', 'openriak-kv', 'data');
const allVersionEntries = productSources
  .filter((product) => product.target === productId)
  .flatMap((product) => discoverVersions(contentRoot, product).map((version) => ({
    version: version.raw,
    sourceDirectory: version.sourceDirectory,
    source: product.source
  })))
  .sort((left, right) => compareSemver(left.version, right.version));
for (const [source, selected] of Object.entries(includedVersions)) {
  const discovered = new Set(allVersionEntries.filter((entry) => entry.source === source).map((entry) => entry.version));
  for (const version of selected) {
    if (!discovered.has(version)) throw new Error(`Requested version ${version} does not exist in content/${source}`);
  }
}
const versionEntries = allVersionEntries.filter(({ source, version }) => (
  !includedVersions[source] || includedVersions[source].has(version)
));

const familyNames = {
  alpine: 'Alpine Linux',
  'amazon-linux': 'Amazon Linux',
  debian: 'Debian',
  fedora: 'Fedora',
  'oracle-linux': 'Oracle Linux',
  raspbian: 'Raspbian',
  rhel: 'Red Hat Enterprise Linux',
  sles: 'SUSE Linux Enterprise Server',
  ubuntu: 'Ubuntu'
};

const familyLogos = {
  alpine: 'images/os/alpine.png',
  'amazon-linux': 'images/os/amazon.png',
  debian: 'images/os/debian.svg',
  fedora: 'images/os/fedora.png',
  'oracle-linux': 'images/os/oracle.png',
  raspbian: 'images/os/raspbian.png',
  rhel: 'images/os/red-hat.svg',
  sles: 'images/os/suse.png',
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

const otpFromFilename = (version, filename) => {
  const explicit = filename.match(/(?:^|[-_.])OTP([0-9]+)(?:\.[0-9]+)?(?:[-_.]|$)/i);
  if (explicit) return Number(explicit[1]);
  const escapedVersion = version.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const alpine = filename.match(new RegExp(`^riak-${escapedVersion}\\.([0-9]+)-r[0-9]+\\.apk$`, 'i'));
  return alpine ? Number(alpine[1]) : null;
};

const downloadOtp = (version, osId, downloadId, item) => {
  if (version.startsWith('2.')) {
    if (item.otp !== null && item.otp !== undefined && item.otp !== '' && item.otp !== 'R16B02') {
      throw new Error(`Unexpected OTP metadata for ${metadataProduct}/${version}/${osId}/${downloadId}: ${item.otp} != R16B02`);
    }
    return 'R16B02';
  }
  const filenameOtp = otpFromFilename(version, item.filename);
  if (item.otp !== null && item.otp !== undefined && item.otp !== '') {
    if (filenameOtp !== null && String(item.otp) !== String(filenameOtp)) {
      throw new Error(`OTP metadata does not match filename for ${metadataProduct}/${version}/${osId}/${downloadId}: ${item.otp} != ${filenameOtp}`);
    }
    return item.otp;
  }
  if (filenameOtp !== null) return filenameOtp;
  throw new Error(`Unable to infer OTP version for ${metadataProduct}/${version}/${osId}/${downloadId}: ${item.filename}`);
};

const normalizeChecksum = (checksum, version, osId, downloadId) => {
  if (!checksum || checksum.algorithm !== 'sha256' || !/^[0-9a-f]{64}$/.test(checksum.value || '')) {
    throw new Error(`Missing or invalid SHA-256 checksum for ${metadataProduct}/${version}/${osId}/${downloadId}`);
  }
  return { algorithm: 'sha256', value: checksum.value };
};

const requestedKeys = referencedValueKeys();
const requiredValueKeys = ['ring_size', 'nodename'];
for (const key of requiredValueKeys) requestedKeys.add(key);

for (const { version, sourceDirectory, source } of versionEntries) {
  const exposesOperatingSystemPicker = source === productId;
  const metadataRoot = path.join(productRoot, 'metadata', version);
  const files = {
    supported: path.join(metadataRoot, 'supported-os.json'),
    downloads: path.join(metadataRoot, 'downloads.json'),
    defaults: path.join(metadataRoot, 'defaults.json')
  };
  const hasSupported = fs.existsSync(files.supported);
  const hasDownloads = fs.existsSync(files.downloads);
  if (!hasSupported && !hasDownloads) {
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
  if (!hasSupported || !hasDownloads) {
    const missing = hasSupported ? files.downloads : files.supported;
    throw new Error(`Incomplete metadata for ${metadataProduct}/${version}: missing ${path.basename(missing)}`);
  }

  const supported = readJson(files.supported);
  const downloads = readJson(files.downloads);
  const defaults = fs.existsSync(files.defaults) ? readJson(files.defaults) : null;
  const documents = { supported, downloads, ...(defaults ? { defaults } : {}) };
  for (const [name, document] of Object.entries(documents)) {
    const acceptedStatuses = name === 'defaults' ? ['complete', 'partial'] : ['complete'];
    if (!acceptedStatuses.includes(document.status)) throw new Error(`Incomplete ${name} metadata for ${metadataProduct}/${version}: ${document.status}`);
    if (document.product !== metadataProduct || document.version !== version) throw new Error(`Mismatched ${name} metadata for ${metadataProduct}/${version}`);
  }

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
  for (const family of new Set(operatingSystems.map((os) => os.family))) {
    const members = operatingSystems.filter((os) => os.family === family);
    if (!members.some((os) => os.defaultForFamily)) members.at(-1).defaultForFamily = true;
  }

  const values = {};
  if (defaults) {
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
  }

  const normalizedDownloads = {};
  for (const os of operatingSystems) {
    normalizedDownloads[os.id] = Object.entries(downloads.downloads[os.id] || {})
      .map(([id, item]) => ({
        id,
        otp: downloadOtp(version, os.id, id, item),
        architecture: item.architecture,
        format: item.format,
        filename: item.filename,
        packageRevision: item.package_revision,
        variant: downloadVariant(item.url),
        url: item.url,
        checksum: normalizeChecksum(item.checksum, version, os.id, id)
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
      defaults: defaults?.status || 'not_generated'
    },
    metadataWarnings: [...new Set([
      ...(supported.warnings || []),
      ...(downloads.warnings || []),
      ...(defaults?.warnings || [])
    ])],
    defaultOs: exposesOperatingSystemPicker
      ? (operatingSystems.some((os) => os.id === 'ubuntu-noble-amd64') ? 'ubuntu-noble-amd64' : operatingSystems[0]?.id)
      : null,
    operatingSystems: exposesOperatingSystemPicker ? operatingSystems : [],
    downloadOperatingSystems: operatingSystems,
    downloads: normalizedDownloads,
    values
  };

  writeVersionData(version, output);
  const valueKeyCount = defaults ? requestedKeys.size : 0;
  console.log(`Synced ${productId} ${version}: ${operatingSystems.length} OS targets, ${Object.values(normalizedDownloads).flat().length} downloads, ${valueKeyCount} referenced value keys.`);
}

const expectedVersionFiles = new Set(versionEntries.map(({ version }) => `${version}.json`));
for (const entry of fs.readdirSync(versionsRoot, { withFileTypes: true })) {
  if (entry.isFile() && entry.name.endsWith('.json') && !expectedVersionFiles.has(entry.name)) {
    fs.rmSync(path.join(versionsRoot, entry.name));
    console.log(`Removed stale ${productId} version metadata: ${entry.name}`);
  }
}
