'use strict';

if (require.main === module && process.argv.slice(2).some((arg) => arg === '-h' || arg === '--help')) {
  console.log(`Generate Hugo product data and synchronize validated Docker download metadata.
Reads release metadata and local Docker records, then updates generated files.

Usage: node sync-product-metadata.js [OPTIONS]

Options:
  --docker-only                Update Docker image data without regenerating other product data.
  --output-root PATH           Generated product-data root (default: tools/generated/).
  --include-version SOURCE=VERSION
                               Restrict a source to exact versions; repeatable.
  --include-latest SOURCE      Restrict a source to its latest release; repeatable.
                               Sources are content directory names, e.g. riak-kv.
                               Unselected sources retain all discovered versions.
  -h, --help                  Show help and exit without synchronizing files.

Default paths are relative to the repository; explicit paths use the current directory.`);
  process.exit(0);
}

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const contentRoot = path.join(repositoryRoot, 'content');
const dockerStaticRoot = path.join(contentRoot, 'static', 'openriak-kv');
const { compareSemver, discoverVersions, productSources } = require('./generate-version-mounts.js');
const { configurationReference } = require('./configuration-reference');
const { annotateSettings } = require('./settings-annotations');
const { defaultsByOs } = require('./defaults-by-os');
const { buildAnnotatedReference } = require('./cli-annotations');
const { reviewMarkdown } = require('./cli-syntax');

const products = [
  { productId: 'openriak-kv', metadataProduct: 'kv', pickerSource: 'openriak-kv' },
  { productId: 'openriak-cs', metadataProduct: 'cs' },
  { productId: 'openriak-ts', metadataProduct: 'ts' }
];

const parseOptions = (argumentsList) => {
  const options = { includeVersions: {}, includeLatest: [] };
  for (let index = 0; index < argumentsList.length; index += 1) {
    if (argumentsList[index] === '--docker-only') {
      options.dockerOnly = true;
      continue;
    }
    if (argumentsList[index] === '--output-root') {
      options.outputRoot = path.resolve(argumentsList[++index] || '');
      continue;
    }
    if (argumentsList[index] === '--include-latest') {
      options.includeLatest.push(argumentsList[++index] || '');
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
const generatedProductsRoot = options.outputRoot || path.join(repositoryRoot, 'tools', 'generated');
const allVersionEntries = productSources.flatMap((product) => discoverVersions(contentRoot, product).map((version) => ({
  productId: product.target,
  version: version.raw,
  sourceDirectory: version.sourceDirectory,
  source: product.source
})));

for (const source of options.includeLatest) {
  const versions = allVersionEntries.filter((entry) => entry.source === source).sort((left, right) => compareSemver(left.version, right.version));
  if (!versions.length) throw new Error(`No versions exist in content/${source}`);
  includedVersions[source] = new Set([versions.at(-1).version]);
}

for (const [source, selected] of Object.entries(includedVersions)) {
  const discovered = new Set(allVersionEntries.filter((entry) => entry.source === source).map((entry) => entry.version));
  for (const version of selected) {
    if (!discovered.has(version)) throw new Error(`Requested version ${version} does not exist in content/${source}`);
  }
}

const familyNames = {
  alpine: 'Alpine Linux',
  'amazon-linux': 'Amazon Linux',
  debian: 'Debian',
  fedora: 'Fedora',
  'oracle-linux': 'Oracle Linux',
  raspbian: 'Raspbian',
  rhel: 'Red Hat Enterprise Linux',
  rocky: 'Rocky Linux',
  centos: 'CentOS',
  suse: 'SUSE Linux Enterprise Server',
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
  rocky: 'images/os/rocky.svg',
  centos: 'images/os/centos.svg',
  suse: 'images/os/suse.svg',
  fedora: 'images/os/fedora.svg',
  sles: 'images/os/suse.svg',
  ubuntu: 'images/os/ubuntu.svg'
};

const osAliases = require('../../content/openriak-kv/metadata/os-aliases.json');
const rhelAliases = osAliases.aliases.map((alias) => ({
  ...alias, name: alias.name, logo: familyLogos[alias.family]
}));

const preferredFamilyDefaults = {
  alpine: 'alpine-3.21-x86_64',
  'amazon-linux': 'amazon-linux-2023-x86_64',
  debian: 'debian-12-amd64',
  'oracle-linux': 'oracle-linux-9-x86_64',
  rhel: 'rhel-9-x86_64',
  ubuntu: 'ubuntu-noble-amd64'
};

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const dockerImagesForVersion = (version) => require('./docker-multiarch-metadata.js').multiarchDockerImages(
  version, path.join(repositoryRoot, 'records', 'openriak-docker', 'images'), dockerStaticRoot
);

const referencedValueKeys = (productRoot) => {
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

const forcedLegacyOtp = (metadataProduct, version) => (
  (metadataProduct === 'kv' && version.startsWith('2.'))
  || (metadataProduct === 'cs' && version.startsWith('2.'))
  || (metadataProduct === 'ts' && version.startsWith('1.'))
);

const downloadOtp = (product, version, osId, downloadId, item) => {
  if (forcedLegacyOtp(product.metadataProduct, version)) {
    if (product.metadataProduct === 'kv' && item.otp !== null && item.otp !== undefined && item.otp !== '' && item.otp !== 'R16B02') {
      throw new Error(`Unexpected OTP metadata for ${product.metadataProduct}/${version}/${osId}/${downloadId}: ${item.otp} != R16B02`);
    }
    return 'R16B02';
  }
  const filenameOtp = otpFromFilename(version, item.filename);
  if (item.otp !== null && item.otp !== undefined && item.otp !== '') {
    if (filenameOtp !== null && String(item.otp) !== String(filenameOtp)) {
      throw new Error(`OTP metadata does not match filename for ${product.metadataProduct}/${version}/${osId}/${downloadId}: ${item.otp} != ${filenameOtp}`);
    }
    return item.otp;
  }
  if (filenameOtp !== null) return filenameOtp;
  if ((product.metadataProduct === 'cs' || product.metadataProduct === 'ts') && version.startsWith('3.')) return null;
  throw new Error(`Unable to infer OTP version for ${product.metadataProduct}/${version}/${osId}/${downloadId}: ${item.filename}`);
};

const normalizeChecksum = (product, checksum, version, osId, downloadId) => {
  if (!checksum || checksum.algorithm !== 'sha256' || !/^[0-9a-f]{64}$/.test(checksum.value || '')) {
    throw new Error(`Missing or invalid SHA-256 checksum for ${product.metadataProduct}/${version}/${osId}/${downloadId}`);
  }
  return { algorithm: 'sha256', value: checksum.value };
};


if (options.dockerOnly) {
  const versions = includedVersions['openriak-kv'];
  if (!versions?.size || Object.keys(includedVersions).some((source) => source !== 'openriak-kv')) {
    throw new Error('--docker-only requires explicit --include-version openriak-kv=VERSION selections');
  }
  for (const version of versions) {
    const target = path.join(generatedProductsRoot, 'openriak-kv', 'data', 'versions', `${version}.json`);
    const output = readJson(target);
    output.dockerImages = dockerImagesForVersion(version);
    const serialized = `${JSON.stringify(output, null, 2)}\n`;
    if (fs.readFileSync(target, 'utf8') !== serialized) {
      const temporary = `${target}.${process.pid}.tmp`;
      fs.writeFileSync(temporary, serialized, 'utf8');
      fs.renameSync(temporary, target);
    }
    console.log(`Synced OpenRiak KV ${version}: ${output.dockerImages.length} tested Docker targets.`);
  }
} else for (const product of products) {
  const productRoot = path.join(contentRoot, product.productId);
  const versionsRoot = path.join(generatedProductsRoot, product.productId, 'data', 'versions');
  const configurationReferenceRoot = path.join(generatedProductsRoot, product.productId, 'data', 'configuration-reference');
  const writeVersionData = (version, output) => {
    const target = path.join(versionsRoot, `${version}.json`);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, `${JSON.stringify(output, null, 2)}\n`, 'utf8');
  };
  const writeConfigurationReferenceData = (version, output) => {
    const target = path.join(configurationReferenceRoot, `${version}.json`);
    if (output.annotationCoverage) {
      const report = path.join(generatedProductsRoot, product.productId, 'settings-coverage', `${version}.json`);
      fs.mkdirSync(path.dirname(report), {recursive: true});
      fs.writeFileSync(report, JSON.stringify(output.annotationCoverage, null, 2) + '\n');
    }
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, `${JSON.stringify(output, null, 2)}\n`, 'utf8');
  };
  const requestedKeys = referencedValueKeys(productRoot);
  const requiredValueKeys = product.metadataProduct === 'kv' ? ['ring_size', 'nodename'] : [];
  for (const key of requiredValueKeys) requestedKeys.add(key);
  const versionEntries = allVersionEntries
    .filter((entry) => entry.productId === product.productId)
    .filter(({ source, version }) => !includedVersions[source] || includedVersions[source].has(version))
    .sort((left, right) => compareSemver(left.version, right.version));

  for (const { version, sourceDirectory, source } of versionEntries) {
    const exposesOperatingSystemPicker = source === product.pickerSource;
    const metadataRoot = path.join(productRoot, 'metadata', version);
    const cliFile = path.join(metadataRoot, 'kv-cli-commands.json');
    if (product.metadataProduct === 'kv' && fs.existsSync(cliFile)) {
      const target = path.join(generatedProductsRoot, product.productId, 'data', 'cli-reference', `${version}.json`);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      const reference = buildAnnotatedReference(readJson(cliFile));
      fs.writeFileSync(target, JSON.stringify(reference, null, 2) + '\n');
      const report = path.join(generatedProductsRoot, product.productId, 'cli-coverage', `${version}.json`);
      fs.mkdirSync(path.dirname(report), { recursive: true });
      fs.writeFileSync(report, JSON.stringify(reference.annotationCoverage, null, 2) + '\n');
      const syntaxRoot = path.join(generatedProductsRoot, product.productId, 'cli-syntax-review');
      fs.mkdirSync(syntaxRoot, {recursive: true});
      fs.writeFileSync(path.join(syntaxRoot, `${version}.json`), JSON.stringify(reference.syntaxReview, null, 2) + '\n');
      fs.writeFileSync(path.join(syntaxRoot, `${version}.md`), reviewMarkdown(reference.syntaxReview));
    }
    const files = {
      supported: path.join(metadataRoot, `${product.metadataProduct}-supported-os.json`),
      downloads: path.join(metadataRoot, `${product.metadataProduct}-downloads.json`),
      defaults: path.join(metadataRoot, `${product.metadataProduct}-settings.json`)
    };
    const hasSupported = fs.existsSync(files.supported);
    const hasDownloads = fs.existsSync(files.downloads);
    if (!hasSupported && !hasDownloads) {
      writeVersionData(version, {
        product: product.productId,
        version,
        documentationSource: source,
        generatedFrom: `content/${source}/${sourceDirectory}`,
        metadataStatus: { supportedOs: 'unavailable', downloads: 'unavailable', defaults: 'unavailable' },
        metadataWarnings: ['No structured operating-system, download, or default-value metadata is available for this legacy release.'],
        defaultOs: null,
        operatingSystems: [],
        downloadOperatingSystems: [],
        downloads: {},
        values: {}
      });
      console.log(`Synced ${product.productId} ${version}: legacy content without structured OS metadata.`);
      continue;
    }
    if (!hasSupported || !hasDownloads) {
      const missing = hasSupported ? files.downloads : files.supported;
      throw new Error(`Incomplete metadata for ${product.metadataProduct}/${version}: missing ${path.basename(missing)}`);
    }

    const supported = readJson(files.supported);
    const downloads = readJson(files.downloads);
    const defaults = fs.existsSync(files.defaults) ? readJson(files.defaults) : null;
    const documents = { supported, downloads, ...(defaults ? { defaults } : {}) };
    for (const [name, document] of Object.entries(documents)) {
      const acceptedStatuses = name === 'defaults' ? ['complete', 'partial'] : ['complete', 'unavailable'];
      if (!acceptedStatuses.includes(document.status)) throw new Error(`Incomplete ${name} metadata for ${product.metadataProduct}/${version}: ${document.status}`);
      if (document.product !== product.metadataProduct || document.version !== version) throw new Error(`Mismatched ${name} metadata for ${product.metadataProduct}/${version}`);
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
    const nativeFamilies = new Set(operatingSystems.map((os) => os.family));
    const rhelOperatingSystems = operatingSystems.filter((os) => os.family === osAliases.source_family);
    for (const alias of rhelAliases) {
      if (alias.nativeFamily && nativeFamilies.has(alias.nativeFamily)) continue;
      for (const rhel of rhelOperatingSystems) {
        // Preserve legacy product aliases; current OpenRiak KV uses Fedora's own releases.
        const releases = exposesOperatingSystemPicker ? (alias.modernReleases || alias.releases) : (alias.family !== 'fedora' ? alias.releases : undefined);
        const release = releases?.[String(rhel.version)];
        operatingSystems.push({
          ...rhel,
          id: release
            ? `${alias.family}-${release.id}-${rhel.architecture}`
            : rhel.id.replace(/^rhel-/, `${alias.family}-`),
          family: alias.family,
          name: alias.name,
          displayName: `${alias.name} ${release?.version || rhel.version}`,
          version: release?.version || rhel.version,
          codename: rhel.architecture,
          logo: alias.logo,
          aliasOf: rhel.id
        });
      }
    }
    operatingSystems.sort((left, right) => (
      left.name.localeCompare(right.name)
      || String(right.version).localeCompare(String(left.version), undefined, { numeric: true })
      || left.architecture.localeCompare(right.architecture)
    ));

    const osDefaults = defaults ? defaultsByOs(defaults, supported.operating_systems) : {};
    for (const os of defaults ? operatingSystems : []) {
      const source = operatingSystems.find(candidate => candidate.id === os.aliasOf);
      os.defaultsKey = Object.hasOwn(osDefaults, os.family) ? os.family : (source?.family || os.family);
    }
    const values = {};
    if (defaults) {
      for (const os of operatingSystems) {
        const effective = osDefaults[os.defaultsKey] || {};
        if (Object.hasOwn(values, os.defaultsKey)) continue;
        values[os.defaultsKey] = {};
        for (const key of requestedKeys) {
          const setting = effective[key];
          if (!setting || !setting.has_default) continue;
          const value = setting.resolved_value ?? setting.value;
          if (value !== null && value !== undefined) values[os.defaultsKey][key] = value;
        }
      }
      for (const os of operatingSystems) {
        for (const key of requiredValueKeys) {
          if (!(key in values[os.defaultsKey])) throw new Error(`Missing required default ${key} for ${product.metadataProduct}/${version}/${os.id}`);
        }
      }
    }

    if (product.metadataProduct === 'kv' && compareSemver(version, '3.4.0') >= 0) {
      if (!defaults) throw new Error(`Configuration reference requires defaults metadata for ${product.metadataProduct}/${version}`);
      writeConfigurationReferenceData(version, annotateSettings(configurationReference(product, version,
        { ...defaults, effective_defaults: osDefaults }, operatingSystems), defaults));
    }

    const normalizedDownloads = {};
    for (const os of operatingSystems) {
      normalizedDownloads[os.id] = Object.entries(downloads.downloads[os.aliasOf || os.id] || {})
        .map(([id, item]) => {
          const subArchitecture = item.sub_architecture || downloadVariant(item.url);
          return {
            id,
            otp: downloadOtp(product, version, os.id, id, item),
            architecture: item.architecture,
            ...(subArchitecture ? { subArchitecture } : {}),
            format: item.format,
            filename: item.filename,
            packageRevision: item.package_revision,
            url: item.url,
            checksum: normalizeChecksum(product, item.checksum, version, os.id, id)
          };
        })
        .sort((left, right) => String(left.otp ?? '').localeCompare(String(right.otp ?? ''), undefined, { numeric: true }) || left.id.localeCompare(right.id));
    }

    const dockerImages = product.productId === 'openriak-kv' ? dockerImagesForVersion(version) : [];
    const output = {
      product: product.productId,
      version,
      documentationSource: source,
      generatedFrom: `content/${product.productId}/metadata/${version}`,
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
      ...(dockerImages.length ? { dockerImages } : {}),
      values
    };

    writeVersionData(version, output);
    const valueKeyCount = defaults ? requestedKeys.size : 0;
    console.log(`Synced ${product.productId} ${version}: ${operatingSystems.length} OS targets, ${Object.values(normalizedDownloads).flat().length} downloads, ${valueKeyCount} referenced value keys.`);
  }

  fs.mkdirSync(versionsRoot, { recursive: true });
  const expectedVersionFiles = new Set(versionEntries.map(({ version }) => `${version}.json`));
  for (const entry of fs.readdirSync(versionsRoot, { withFileTypes: true })) {
    if (entry.isFile() && entry.name.endsWith('.json') && !expectedVersionFiles.has(entry.name)) {
      fs.rmSync(path.join(versionsRoot, entry.name));
      console.log(`Removed stale ${product.productId} version metadata: ${entry.name}`);
    }
  }
  if (fs.existsSync(configurationReferenceRoot)) {
    const expectedConfigurationFiles = new Set(versionEntries
      .filter(({ version }) => product.metadataProduct === 'kv' && compareSemver(version, '3.4.0') >= 0)
      .map(({ version }) => `${version}.json`));
    for (const entry of fs.readdirSync(configurationReferenceRoot, { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith('.json') && !expectedConfigurationFiles.has(entry.name)) {
        fs.rmSync(path.join(configurationReferenceRoot, entry.name));
        console.log(`Removed stale ${product.productId} configuration-reference metadata: ${entry.name}`);
      }
    }
  }
}
