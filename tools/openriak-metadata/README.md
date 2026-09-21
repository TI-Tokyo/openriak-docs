# OpenRiak metadata

`openriak-metadata` generates package, configuration-setting and CLI metadata, stages
it for inspection, and deploys it into the Hugo documentation checkout. It
requires Linux and Python 3.11 or newer. Settings extraction also requires Git
and access to GitHub. CLI discovery additionally requires Docker and a matching release image. Local package discovery works offline.

## Generate, inspect, deploy

From the repository root:

```sh
tools/openriak-metadata/openriak-metadata kv-packages \
  --version 3.4.0 --version 3.4.1 \
  --local-copy ~/GitHub/TI-Tokyo/openriak-build/artifacts/riak/ \
  --web-root https://files.tiot.jp/riak/

tools/openriak-metadata/openriak-metadata kv-settings
tools/openriak-metadata/openriak-metadata kv-cli-commands --version 3.4.0 --version 3.4.1
tools/openriak-metadata/openriak-metadata list
tools/openriak-metadata/openriak-metadata deploy
```

- `kv-packages` generates `supported-os.json` and `downloads.json` for the exact
  releases selected with repeatable `--version` arguments. Duplicate versions
  are processed once. Package metadata must be complete, with valid SHA-256
  checksums and no discovery warnings.
- `kv-settings` generates `defaults.json`, using the operating systems from
  staged package metadata and the exact `riak-VERSION` source tag with its
  recursively locked Erlang dependencies. It defaults to every staged KV
  version; repeat `--version` to select a subset. It does not rediscover packages.
- `kv-cli-commands` generates `cli-commands.json` for each repeated `--version`,
  using the release runtime and exact source tag. It can run independently of
  package and settings generation. See CLI discovery below.
- `list` shows each staged file's generation date in UTC, status and deployment
  readiness. Dates come from staged file modification times; deployment preserves
  them. Validation problems are printed and cause a nonzero exit. An empty stage
  is reported without error.
- `deploy` validates all selected staged releases, then installs their files
  beneath `content/openriak-kv/metadata/VERSION/` in this checkout. It uses the
  staged results without generating metadata or contacting package/source hosts.

All commands use `artifacts/openriak-metadata/` in this checkout by default,
with files beneath `kv/VERSION/`. This staging directory is ignored by Git.
Use `--metadata-dir DIR` (also spelled `--output DIR`) on each command to use
another staging directory. `list` and `deploy` default to every staged KV version
and accept repeatable `--version` filters. Use `deploy --repo /path/to/openriak-docs`
to target another checkout. An installed CLI defaults to the current directory
when it cannot locate its source checkout.

Generation publishes its batch only after every requested version validates.
A failed run leaves the previous staged results and dates intact. Regenerating
identical metadata updates its staged generation date. Each generation command preserves the other metadata files in the stage.
If new OS families are added, regenerate settings to cover them before deployment.

Deployment validates a snapshot before making replacements, replaces each file
atomically, and rolls back earlier replacements if installation fails. Identical
destination files are not rewritten. Package-only and CLI-only stages can be deployed;
existing settings, OS aliases, unselected releases and Docker test caches are
preserved. Deployment copies authoritative metadata into the Hugo content tree;
it does not publish the website or rebuild/restart Docker. To reload a running
Docker preview afterward:

```sh
docker compose -f docker/compose.yaml restart core
```

Settings with status `partial` are deployable when they contain extracted settings
and cover all staged OS targets, matching the Hugo adapter's handling of unresolved
source macros. `list` displays that status. Use `kv-settings --strict` to require
`complete` results. Unavailable or malformed settings cannot be staged or deployed.

## Package sources and public URLs

`kv-packages` accepts these roots, each ending immediately before `kv/`:

- `--local-copy DIR`: discover packages and compute SHA-256 from a local copy.
- `--remote-copy USER@HOST:PATH`: discover packages and compute SHA-256 on an SSH
  server. Requires SSH key/agent authentication and remote `find` and `sha256sum`.
  Relative remote paths are relative to the login directory. Use an absolute
  path instead of `~` for remote home directories.
- `--web-root URL`: public HTTP(S) URL prefix written into download metadata;
  defaults to `https://files.tiot.jp/riak/`. Without a copy option, an explicit
  web root is also used for HTTP discovery and downloads.

The copy options are mutually exclusive and only read the selected source.
Each requested version is read from `ROOT/kv/MAJOR.MINOR/VERSION/`, including
standalone Alpine packages beneath that tree. Copy checksums are recomputed each
run independently of the HTTP checksum cache. Four packages are hashed
concurrently; use `--checksum-workers` to change that limit.

Read the server copy over SSH:

```sh
tools/openriak-metadata/openriak-metadata kv-packages \
  --version 3.4.1 \
  --remote-copy "peter-clark@sftp.tiot.jp:/media/ebs-0001/ftp-root/riak/" \
  --web-root https://files.tiot.jp/riak/
```

With a copy or an explicit web root, discovery stays within the version tree.
Without those options, HTTP discovery includes both the standard version tree
and the separate `https://files.tiot.jp/alpine/` repository. HTTP checksum digests
are cached by URL; use `--refresh` to recompute them. Package bodies are not retained.
All generation commands accept `--cache-dir`, `--refresh` and `--strict`;
`kv-settings` and `kv-cli-commands` also accept `--keep-workdir`. Every command accepts `--log-level`.

## CLI discovery

```sh
tools/openriak-metadata/openriak-metadata kv-cli-commands \
  --version 3.4.0 --version 3.4.1 --strict

# Override the runtime for one version:
tools/openriak-metadata/openriak-metadata kv-cli-commands \
  --version 3.4.1 --runtime-image tiotjp/openriak-kv:3.4.1-alpine-3.24-otp26
```

The default is `tiotjp/openriak-kv:VERSION-alpine-3.24`. `--runtime-image` accepts
an image tag or digest; the literal `{version}` expands for each selected release.
An absent image is pulled; `--refresh` also pulls an existing tag. The output
records the immutable image ID, available repository digests, installed package
version, OTP version, root Git commit and dependency commits. A runtime version
mismatch fails generation.

The probe runs an isolated Erlang VM in a disposable container with no network,
read-only root filesystem, and no host mounts. It loads the shipped schemas,
registers Clique commands and reads their argument/flag specifications and help.
It reads launchers and BEAM abstract code to discover legacy admin, replication,
debug, configuration and release-helper commands. It never invokes administrative
callbacks or starts a Riak node. Shell dispatchers are inspected as text.

The historical `content/riak-kv/3.2.5-new-release` pages are a discovery checklist.
Use `--docs-root PATH` when those pages live in another checkout. Attach entries
include the exported `riak` and `riak_client` APIs, documented calls in other Riak
modules, and AAE query selectors recursively extracted from the runtime's type
union. Function arities, signatures, type definitions, examples and source
comments are retained. Historical examples are evidence, not verified runnable
examples: obsolete calls are recorded separately in the coverage report. The
Erlang shell can evaluate arbitrary expressions; that unbounded language is not
represented as a finite set of CLI commands.

Deprecated launchers/commands have `deprecated: true`. Missing handlers, removed
commands, and help-only topics have explicit availability values. Unadvertised
flags are retained. Built-in helpers are distinguished from the user-facing Riak
commands. When upstream supplies no help, `help_status` is `not_provided` rather
than invented text. Source dispatch and handler information is preserved for
options that cannot be reduced to a simple flag list.

Service variants are keyed by OS family **and service manager/deployment context**.
They include `rc-service riak start` for OpenRC, `systemctl start riak` for systemd,
`service riak start` for FreeBSD rc.d, and `riak daemon` for direct operation,
plus stop/restart/status equivalents. Service definitions from the selected tag
provide provenance. These are source-derived command forms, not a claim that
all service managers have been boot-tested inside the discovery container.

Discovery failures produce `status: "partial"` with warnings. Without `--strict`,
partial results can be staged for inspection; `list` reports them as undeployable
and `deploy` rejects them. `--strict` preserves the previous stage on any gap.
A `complete` result means the stated discovery scope was inspected, not that
state-changing commands were executed.
See [the CLI metadata schema](CLI-SCHEMA.md) for the consumer contract.

After `list` and `deploy`, create or refresh the Hugo reference pages:

```sh
node tools/scripts/generate-cli-pages.js --version 3.4.0
```

The command index links to dedicated pages with syntax, arguments, options,
available help, aliases and compatibility status. Erlang arities are combined;
AAE selectors have their own pages. Bundled helpers are listed separately.
Compiler-only private exports are excluded; historically documented internal
operations are retained and labelled. Service examples follow the docs OS picker.
The normal docs build prepares the rendering data without running discovery.
See [the tools guide](../README.md#cli-reference-pages) for regeneration and
version inheritance details.

## Command migration and settings format

`packages` is now `kv-packages`; `defaults` is now `kv-settings`. Both imply KV,
so `--product` is removed. TS and CS can receive their own commands when supported.
`--update-repo` is replaced by the separate `deploy` command.

`generate` has been removed: it only combined package and settings generation,
which the two explicit generation commands now cover. For package-only releases,
run `kv-packages`, `list`, then `deploy`.

The Hugo-facing filename remains `defaults.json`. It uses schema version 2 with
`defaults_scope: "os"`; `effective_defaults` is keyed by OS family (`alpine`,
`ubuntu`, `rhel`, etc.). All releases and architectures of an OS share an entry.
Adding another release of an existing OS does not require regenerating settings.
The docs adapter also supports legacy schema version 1 defaults.

## Install and test

```sh
python3 -m pip install ./tools/openriak-metadata
(cd tools/openriak-metadata && python3 -m unittest discover -s tests -v)
```
