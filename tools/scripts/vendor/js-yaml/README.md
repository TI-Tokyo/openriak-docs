Vendored js-yaml 4.1.1 (MIT) from https://github.com/nodeca/js-yaml/tree/4.1.1.

`js-yaml.js` is the unmodified upstream `dist/js-yaml.js` bundle. The CVE
assessment loader uses its JSON schema and rejects duplicate mapping keys.
Vendoring keeps host, Docker build, and preview metadata commands independent
of an npm installation or network access. This parser is not shipped to browsers.

To update, replace the bundle and license from a reviewed upstream release,
update this version, and run `node tools/scripts/docker-cve-metadata.test.js`.
