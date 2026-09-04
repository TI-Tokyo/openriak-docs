'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const contentRoot = path.join(repositoryRoot, 'content');
const dockerCacheRoot = path.join(repositoryRoot, 'tools', 'cache', 'openriak-docker');
const dockerStaticRoot = path.join(contentRoot, 'static', 'openriak-kv');
const { compareSemver, discoverVersions, productSources } = require('./generate-version-mounts.js');

const products = [
  { productId: 'openriak-kv', metadataProduct: 'kv', pickerSource: 'openriak-kv' },
  { productId: 'openriak-cs', metadataProduct: 'cs' },
  { productId: 'openriak-ts', metadataProduct: 'ts' }
];

const parseOptions = (argumentsList) => {
  const options = { includeVersions: {}, includeLatest: [] };
  for (let index = 0; index < argumentsList.length; index += 1) {
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

const suseReleaseAliases = {
  5: { id: '10-sp1', version: '10 SP1' },
  6: { id: '11-sp1', version: '11 SP1' },
  7: { id: '12', version: '12' },
  8: { id: '15-sp1', version: '15 SP1' },
  9: { id: '15-sp4', version: '15 SP4' }
};

const rhelAliases = [
  { family: 'rocky', name: familyNames.rocky, logo: familyLogos.rocky },
  { family: 'centos', name: familyNames.centos, logo: familyLogos.centos },
  { family: 'suse', name: familyNames.suse, logo: familyLogos.suse, nativeFamily: 'sles', releases: suseReleaseAliases },
  { family: 'fedora', name: familyNames.fedora, logo: familyLogos.fedora, nativeFamily: 'fedora' }
];

const preferredFamilyDefaults = {
  alpine: 'alpine-3.21-x86_64',
  'amazon-linux': 'amazon-linux-2023-x86_64',
  debian: 'debian-12-amd64',
  'oracle-linux': 'oracle-linux-9-x86_64',
  rhel: 'rhel-9-x86_64',
  ubuntu: 'ubuntu-noble-amd64'
};

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const sha256File = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');

const successfulDockerReports = (targetRoot) => {
  const reportFiles = [path.join(targetRoot, 'report.json')];
  const runsRoot = path.join(targetRoot, 'runs');
  if (fs.existsSync(runsRoot)) {
    for (const entry of fs.readdirSync(runsRoot, { withFileTypes: true })) {
      if (entry.isDirectory()) reportFiles.push(path.join(runsRoot, entry.name, 'report.json'));
    }
  }
  return reportFiles
    .filter((file) => fs.existsSync(file))
    .map((file) => ({ file, report: readJson(file) }))
    .filter(({ report }) => [1, 2].includes(report.schema_version) && report.status === 'passed')
    .sort((left, right) => String(right.report.finished_at || '').localeCompare(String(left.report.finished_at || '')));
};

const dockerImagesForVersion = (version) => {
  const versionRoot = path.join(dockerCacheRoot, version);
  if (!fs.existsSync(versionRoot)) return [];
  const images = [];
  for (const osEntry of fs.readdirSync(versionRoot, { withFileTypes: true })) {
    if (!osEntry.isDirectory()) continue;
    const osRoot = path.join(versionRoot, osEntry.name);
    for (const downloadEntry of fs.readdirSync(osRoot, { withFileTypes: true })) {
      if (!downloadEntry.isDirectory()) continue;
      const targetRoot = path.join(osRoot, downloadEntry.name);
      const successfulReports = successfulDockerReports(targetRoot);
      if (!successfulReports.length) continue;
      const { file: reportFile, report } = successfulReports[0];
      if (report.product !== 'openriak-kv' || report.target?.version !== version) {
        throw new Error(`Mismatched Docker cache report: ${reportFile}`);
      }
      if (report.target.os_id !== osEntry.name || report.target.download_id !== downloadEntry.name) {
        throw new Error(`Misplaced Docker cache report: ${reportFile}`);
      }
      const artifacts = report.artifacts || {};
      const artifactNames = report.schema_version === 2
        ? [['dockerfile', 'Dockerfile'], ['compose_single', 'compose.single.yaml'], ['compose_cluster', 'compose.cluster.yaml']]
        : [['dockerfile', 'Dockerfile'], ['compose', 'compose.yaml']];
      for (const [name, filename] of artifactNames) {
        const artifact = artifacts[name];
        const expectedPrefix = `downloads/docker/${version}/`;
        if (!artifact || artifact.filename !== filename || !artifact.url?.startsWith(expectedPrefix)
          || !/^[0-9a-f]{64}$/.test(artifact.sha256 || '')) {
          throw new Error(`Invalid ${name} artifact in Docker cache report: ${reportFile}`);
        }
        const cachedFile = path.join(path.dirname(reportFile), filename);
        const publishedFile = path.join(dockerStaticRoot, artifact.url);
        if (!fs.existsSync(cachedFile)) {
          throw new Error(`Missing cached ${filename} for Docker cache report: ${reportFile}`);
        }
        if (!fs.existsSync(publishedFile)) {
          throw new Error(`Missing published ${filename} for Docker cache report: ${reportFile}`);
        }
        if (sha256File(cachedFile) !== artifact.sha256 || sha256File(publishedFile) !== artifact.sha256) {
          throw new Error(`Checksum mismatch for ${filename} in Docker cache report: ${reportFile}`);
        }
      }
      const image = {
        osId: report.target.os_id,
        osName: report.target.os_name,
        osRelease: report.target.os_release,
        otp: report.target.otp,
        architecture: report.target.architecture,
        image: report.image,
        node: report.node,
        testedAt: report.finished_at,
        baseImage: report.base_image?.pinned || '',
        dockerfile: artifacts.dockerfile
      };
      if (report.schema_version === 2) {
        image.composeSingle = artifacts.compose_single;
        image.composeCluster = artifacts.compose_cluster;
        image.clusterNodes = report.generation?.cluster_nodes || null;
      } else {
        image.compose = artifacts.compose;
      }
      images.push(image);
    }
  }
  return images.sort((left, right) => (
    left.osName.localeCompare(right.osName)
    || String(left.osRelease).localeCompare(String(right.osRelease), undefined, { numeric: true })
    || String(left.otp).localeCompare(String(right.otp), undefined, { numeric: true })
    || left.architecture.localeCompare(right.architecture)
  ));
};

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
        const effective = defaults.effective_defaults?.[os.aliasOf || os.id]?.[name];
        if (!effective?.has_default) {
          defaultsByOs[os.id] = { hasDefault: false, value: '' };
          continue;
        }
        const value = effective.resolved_value ?? effective.value;
        defaultsByOs[os.id] = { hasDefault: true, value: configurationValueText(value) };
      }
      const globalDefault = defaultsByOs[globalDefaultOperatingSystem?.id] || { hasDefault: false, value: '' };
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

for (const product of products) {
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
    const files = {
      supported: path.join(metadataRoot, 'supported-os.json'),
      downloads: path.join(metadataRoot, 'downloads.json'),
      defaults: path.join(metadataRoot, 'defaults.json')
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
    const rhelOperatingSystems = operatingSystems.filter((os) => os.family === 'rhel');
    for (const alias of rhelAliases) {
      if (alias.nativeFamily && nativeFamilies.has(alias.nativeFamily)) continue;
      for (const rhel of rhelOperatingSystems) {
        const release = alias.releases?.[String(rhel.version)];
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

    const values = {};
    if (defaults) {
      for (const os of operatingSystems) {
        const effective = defaults.effective_defaults[os.aliasOf || os.id] || {};
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
          if (!(key in values[os.id])) throw new Error(`Missing required default ${key} for ${product.metadataProduct}/${version}/${os.id}`);
        }
      }
    }

    if (product.metadataProduct === 'kv' && compareSemver(version, '3.4.0') >= 0) {
      if (!defaults) throw new Error(`Configuration reference requires defaults metadata for ${product.metadataProduct}/${version}`);
      writeConfigurationReferenceData(version, configurationReference(product, version, defaults, operatingSystems));
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
