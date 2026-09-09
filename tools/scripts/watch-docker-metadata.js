'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { cveStamp, enrichImages } = require('./docker-cve-metadata');

const sourceRoot = path.resolve(__dirname, '../generated/openriak-kv/data/versions');

// Poll file stamps because host changes on Docker bind mounts may not emit fs.watch events.
// Merge only Docker entries: the preview owns its other generated metadata.
const watchDockerMetadata = ({ source = sourceRoot, target, intervalMs = 1000, onError = console.error,
  cveCacheRoot, cveAssessmentRoot }) => {
  const stamps = new Map();
  const cveStamps = new Map();
  const sync = () => {
    for (const filename of fs.readdirSync(target).filter((name) => /^\d+\.\d+\.\d+\.json$/.test(name))) {
      try {
        const from = path.join(source, filename);
        if (!fs.existsSync(from)) continue;
        const stat = fs.statSync(from);
        const stamp = `${stat.mtimeMs}:${stat.ctimeMs}:${stat.size}`;
        const version = filename.slice(0, -5);
        const scanStamp = cveStamp(version, cveCacheRoot, cveAssessmentRoot);
        if (stamps.get(filename) === stamp && cveStamps.get(filename) === scanStamp) continue;
        // A newly generated preview can be newer than the repository adapter.
        if (!stamps.has(filename) && fs.statSync(path.join(target, filename)).mtimeMs > stat.mtimeMs) {
          stamps.set(filename, stamp);
        }
        const incoming = JSON.parse(fs.readFileSync(stamps.get(filename) === stamp ? path.join(target, filename) : from, 'utf8'));
        if (Array.isArray(incoming.dockerImages)) {
          incoming.dockerImages = enrichImages(incoming.dockerImages, version, cveCacheRoot, cveAssessmentRoot);
          const destination = path.join(target, filename);
          const current = JSON.parse(fs.readFileSync(destination, 'utf8'));
          if (JSON.stringify(current.dockerImages) !== JSON.stringify(incoming.dockerImages)) {
            current.dockerImages = incoming.dockerImages;
            const temporary = `${destination}.${process.pid}.tmp`;
            fs.writeFileSync(temporary, `${JSON.stringify(current, null, 2)}\n`);
            fs.renameSync(temporary, destination);
            console.log(`Updated preview Docker downloads for OpenRiak KV ${filename.slice(0, -5)}.`);
          }
        }
        stamps.set(filename, stamp);
        cveStamps.set(filename, scanStamp);
      } catch (error) {
        onError(`Unable to sync preview Docker metadata ${filename}: ${error.message}`);
      }
    }
  };
  sync();
  const timer = setInterval(sync, intervalMs);
  return { close: () => clearInterval(timer) };
};

if (require.main === module) {
  const target = process.argv[2];
  if (!target) throw new Error('Usage: node watch-docker-metadata.js PREVIEW_VERSION_DIRECTORY');
  watchDockerMetadata({ target: path.resolve(target) });
}

module.exports = { watchDockerMetadata };
