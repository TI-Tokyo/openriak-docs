# OpenRiak KV Docker cache

For all commands, options, and defaults, see the [command reference](#command-reference).

This tool derives Docker targets from the authoritative release records in
`content/openriak-kv/metadata/{version}/supported-os.json` and
`downloads.json`. It accepts OpenRiak KV 3.4.0 and newer only; legacy Riak KV
releases are rejected. It does not run as part of a normal documentation build.

Refresh the package listings from `files.tiot.jp` before discovering new Docker
targets with the [metadata tool](../openriak-metadata/README.md):

```sh
tools/openriak-metadata/openriak-metadata packages \
  --product kv --version 3.4.0 --version 3.4.1 --refresh --update-repo
```

The metadata tool stages and validates all requested versions before replacing
the repository's OS/package JSON files. This command does not build images.

The generator now creates one shared Dockerfile for each OpenRiak KV version,
OS release, and OTP combination. Architecture-specific package stages select the
matching official package using BuildKit's `TARGETARCH`; unsupported architectures
are not advertised. Each stage pins its OS release image by digest. The current
3.4.0/3.4.1 matrix size follows the current package metadata; use `matrix` to inspect the current targets.

The generator does not explicitly install curl. Integration HTTP probes use the
package-bundled Erlang runtime to request `/ping` and verify both HTTP status 200
and body `OK`. Alpine retains GNU coreutils for runtime command compatibility.
Other OS bases or package dependencies may already include curl/libcurl; these
are not forcibly removed. Existing cached images require regeneration and
retesting to adopt the dependency change.

The standard OS installation stages update existing OS packages before
installing OpenRiak KV: Alpine uses `apk upgrade`, Debian/Ubuntu use
`apt-get update` and `apt-get dist-upgrade`, and RPM images use the available
`dnf`, `microdnf`, `yum`, or `zypper` update command with refreshed repository
metadata. Updates stay within the base image's configured release repositories;
they do not switch OS releases. Archived releases can only receive updates
available in their archives. Update failures fail the build.
For releases using the validated `rpm-root` strategy described below, DNF instead
installs current runtime packages into an empty filesystem. The full base image
supplies installer tools, and its layers do not become part of the runtime.

Amazon Linux 2023 uses `dnf --releasever=latest` for upgrades and dependency
installation so an older base image's repository snapshot cannot hold back
available fixes. This selects the newest **AL2023 repository snapshot**; the
Docker base still uses the release-specific `amazonlinux:2023` tag and its
resolved digest. See [Amazon's repository update documentation](https://docs.aws.amazon.com/linux/al2023/ug/managing-repos-os-updates.html).

SUSE images remove `container-suseconnect` after repository operations and
OpenRiak KV installation. This removes the registration helper's embedded Go
runtime, which accounted for the SUSE findings in the September 2026 Scout
review. RPM dependency checks remain enabled during removal. Derived images
needing SUSE host-entitlement integration must reinstall the helper; ordinary
OpenRiak KV startup does not require it. OS package databases and runtime
dependencies remain present. Alpine continues to retain coreutils.
Removal is verified in the running container and RPM database. Validated SUSE
releases also use the `clean-root` strategy below, so the removed helper cannot
remain in inherited image layers. The amd64 prototypes produced zero Scout
findings. Older approved images can still report the deleted helper from their
base layer; adopting the new layout requires regeneration, rebuilding and a new
scan. Full results and limitations are in the
[minimal-runtime validation report](reports/minimal-runtime-validation-2026-09-08.md).

Package updates address fixes available from the selected repositories. They do
not fix unsupported OS releases, vendor-deferred vulnerabilities, or every
scanner finding. Do not replace system Python packages with arbitrary PyPI
versions to bypass distro dependency checks.

Updates run during image creation, never at container startup or during a normal
docs build. Use `refresh --force` to regenerate, rebuild and retest existing
images with this change. Existing approved Dockerfiles and published downloads
are retained until explicitly refreshed. An immutable base digest pins the base
image, but repository package updates can change between fresh builds.

An explicit refresh builds with `--no-cache`, so package upgrades run even when
the pulled OS release tag resolves to the same digest. This applies to every OS
family. Complete compatible passed targets still use the normal approval cache
unless `--force` requests regeneration. OCI export then reuses the tested layers.

Package downloads are checksum-verified in separate `FROM scratch` stages.
The installation stage uses a temporary read-only BuildKit bind mount. Standard
installers copy, install, and remove the package within one `RUN`; `rpm-root`
installers consume the mounted package directly. The final image contains the
OS runtime and installed files, without the downloaded package layer.
RPM installation also removes `/var/cache/dnf`, `/var/cache/yum`, and
`/var/cache/zypp` before the installation layer is saved, including caches left
by the switch from `microdnf` to `dnf`. Debian/Ubuntu run `apt-get clean` and
remove repository lists; Alpine uses `apk --no-cache`. Runtime dependencies
and package databases are retained.
The download can remain in BuildKit's local cache for reuse. See the
[Dockerfile mount reference](https://docs.docker.com/reference/dockerfile/#run---mounttypebind).

Existing approved Dockerfiles retain their original contents. To adopt this
change, regenerate and retest with the `--force` command below (add
`--extra-namespace tiotjp` if wanted). `--do-not-test` deliberately uses saved
approved files, so it cannot apply generator changes to older approvals.

To rebuild every group overnight from the repository root:

```sh
tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 --version 3.4.1 \
  --timeout 1800 --force --nohup
```

`--nohup` starts a detached worker and returns immediately. It prints the worker
PID, the absolute log path, a `tail -n 100 -f` command, and a `kill -TERM` command for
graceful shutdown. Do not add shell redirection or `&`; the tool handles both.
Standard output and errors go to the same log with unbuffered Python output.
The worker survives terminal hangups and runs in its own session.

Log files are created beneath `tools/cache/openriak-docker/logs/` and named
`refresh-YYYY-MM-DD_HH-MM-SS.microseconds+offset-unique.log`, using the launch
time and local UTC offset. Each invocation gets a new file. With standalone
`--output PATH`, logs go beneath `PATH/logs/` instead, keeping docs untouched.
`generate` also accepts `--nohup` and uses a `generate-` log filename prefix.
Both foreground and background startup headers include the process ID; a
background header also identifies its log file.

Use the same option with `--retry-failed` to resume an incomplete matrix in the
background. Argument/selection validation happens before launching the worker.
`--whatif --nohup` remains a read-only preview in the foreground and creates no
background worker or log file. Subsequent worker failures are reported in its
log, since the launching command has already returned.

## Previewing rebuild decisions

Add `--whatif` to a refresh command to see what would rebuild, what would skip,
and why, without contacting Docker or changing generated files, caches,
reports, published downloads, or metadata:

```sh
tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 --version 3.4.1 \
  --timeout 1800 --retry-failed --whatif
```

The plan compares cached inputs and artifact checksums using the existing
refresh rules. Reasons include changed startup/healthcheck code, changed
Dockerfile/Compose/environment generator code, changed packages or options,
missing/modified files, incomplete platform results, and explicit `--force`.
Generator content changes still invalidate passed caches and cause regeneration,
rebuilding, and testing. The plan also shows which architectures can reuse
passed tests when retrying an unchanged shared Dockerfile.

`--whatif` accepts the usual selection, `--force`, `--retry-failed`, standalone
`--output`, identity, and extra-namespace options. With `--do-not-test`, it checks
saved approvals and lists the tags that would be applied without retesting.
It reports blocked targets when the real command would require `--retry-failed`
or `--force`, or cannot use a report. The exit status is nonzero for blocked
targets or an empty `--do-not-test` selection. `--all --whatif` does not require
`--yes`, since it cannot perform the expensive work.

The result is a snapshot of local cache state. Running workers can change that
state after the preview, and remote release-tag digests are not checked. To
perform the planned work, rerun the same command without `--whatif`.

## Cleaning up previous runs

`--before` is optional and defaults to **now**, captured once when cleanup starts.
Cleanup always logs the exact timestamp and UTC offset it uses before planning
any removals. Activity at or after that cutoff is retained.

Accepted cutoff formats:

| Value | Meaning |
| --- | --- |
| `2026-09-06` | Midnight at the start of that date in the machine's local timezone |
| `2026-09-06T15:30:00` | That date and time in the machine's local timezone |
| `2026-09-06T15:30:00+09:00` | That exact instant with an explicit UTC offset |
| Omitted | The current local date and time when cleanup starts |

Local cutoffs use the machine's UTC offset applicable to that date, including
daylight saving time where applicable. Explicit offsets and `Z` (UTC) remain
supported. For example, on a machine in Japan, `2026-09-06` is logged as
`2026-09-06T00:00:00.000000+09:00`.

Preview old diagnostic files and OCI archives that can be removed:

```sh
tools/openriak-docker/openriak-docker cleanup --before 2026-09-06T15:30:00+09:00
```

For a preview using the current time, simply run:

```sh
tools/openriak-docker/openriak-docker cleanup
```

Add `--delete` to apply the previewed cleanup. Normal cleanup retains all JSON
reports, current artifacts, and runs referenced by current reports. A run is
retained in full if its recorded activity or any file modification is at or
after the cutoff.

To extend the same cutoff to current caches, Docker metadata, published files,
images, build cache, and running generator workers, add `--remove-all`:

```sh
# Preview only; no workers are stopped and no files or Docker resources change.
tools/openriak-docker/openriak-docker cleanup \
  --before 2026-09-06T15:30:00+09:00 --remove-all

# Apply the broader cleanup.
tools/openriak-docker/openriak-docker cleanup \
  --before 2026-09-06T15:30:00+09:00 --remove-all --delete
```

`--remove-all` still respects the cutoff; it does not mean an unconditional reset.
It removes eligible old compact reports as well as old generated files. It
updates only `dockerImages` in the generated version JSON files, which the
preview metadata watcher picks up. Package download records and authoritative
OS/package metadata remain unchanged.

The broader mode sends SIGTERM to this repository's generator workers started
before the cutoff and their subprocesses, then waits for graceful cleanup
(`--timeout 1800` by default). Workers started at or after the cutoff are kept;
if any are active, applying `--remove-all` refuses to proceed, to avoid racing
their cache and metadata writes. Wait for those workers to finish, and do not
start another generator invocation while cleanup is applying.

Docker cleanup selects old harness test containers and their unused networks,
recorded generated image tags (including recorded extra namespaces), and labeled
generated images without tags. Images created or rebuilt since the cutoff, or
used by retained containers, are kept. It prunes unused cache last used before
the cutoff only in the dedicated `openriak-kv-multiarch` builder. The builder
itself remains available, along with its newer cache records. Shared OS base
images, unrelated containers/images, and other builders' cache are retained.
If the dedicated builder is stopped, applying cleanup temporarily bootstraps it
to prune its cache, then stops it again (including when pruning fails). A running
builder remains running. Preview mode never starts or stops builders.
See [Docker's cache filter documentation](https://docs.docker.com/reference/cli/docker/buildx/prune/#provide-filter-values---filter)
for the `until` filter's last-use semantics.

Cleanup covers the repository's legacy and multiarch cache roots and docs
downloads; standalone output directories created with `--output` are outside
this command's scope. Docker access is required only for `--remove-all`.
Nothing is removed unless `--delete` is supplied.

If cleanup reports a permission error, files from an earlier `sudo` refresh may
still belong to root. Cleanup checks planned directory writes before stopping
workers or deleting Docker resources and reports the full path and owner IDs.
On the original WSL checkout, the legacy cache may need this one-time repair,
run as your normal user from the repository root:

```sh
sudo find tools/cache/openriak-docker -uid 0 -exec chown -h "$(id -u):$(id -g)" {} +
```

This restores ownership only for root-owned entries in that cache and preserves
their content and modification timestamps. Then retry the original cleanup
command without `sudo`, so new reports and metadata remain owned by your user.

## Branded images and standalone output

`refresh` and `generate` accept the same image identity options:

| Option | Default |
| --- | --- |
| `--vendor` | `OpenRiak` |
| `--source` | `https://github.com/OpenRiak/openriak-docs` |
| `--url` | `https://openriak.org` |
| `--namespace` | `openriak` |

`--namespace` selects the primary repository for **every** canonical tag and
shorter alias, including `latest`, and updates Compose image references and the
original-image label. `--extra-namespace` additionally mirrors a refresh's tags
without changing its primary repository or labels. Label values and the primary
namespace participate in cache compatibility checks.

Generate company-branded files separately, without building images, running
integration tests, or updating the docs:

```sh
tools/openriak-docker/openriak-docker generate \
  --version 3.4.0 --version 3.4.1 \
  --vendor "TI Tokyo" \
  --source "https://github.com/TI-Tokyo/openriak-docs" \
  --url "https://www.tiot.jp/openriak-docs/" \
  --namespace tiotjp \
  --output "$HOME/openriak-docker-tiotjp" --no-docs \
  --timeout 1800
```

The output layout is `PATH/{version}/{image-tag}/`, containing `Dockerfile`,
`compose.single.yaml`, `compose.cluster.yaml`, `example.env`, and `report.json`.
Run snapshots and diagnostics are retained beneath `runs/`. Reports say
`generated`, not `passed`: branding changes do not inherit a previous test
approval. Each newly generated group receives a fresh initial cookie shared by
its four files. Existing cluster cookies still follow the preservation and
coordinator-adoption rules described below.

`generate` requires `--output`. It reuses matching recorded base-image digests
from the selected output or the docs cache; if none exists, it pulls and resolves
the release tag. It never builds or tests. `--force` pulls fresh release digests
and regenerates the selected files, retaining a snapshot of the previous files,
including operator edits. Without `--force`, unchanged output is skipped and
changed/incompatible files are reported as errors.

To build and test the company set later, use the same identity and output options
with `refresh --retry-failed`:

```sh
tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 --version 3.4.1 \
  --vendor "TI Tokyo" \
  --source "https://github.com/TI-Tokyo/openriak-docs" \
  --url "https://www.tiot.jp/openriak-docs/" \
  --namespace tiotjp \
  --output "$HOME/openriak-docker-tiotjp" --no-docs \
  --retry-failed --timeout 1800
```

The separate output directory holds that set's test cache and build archives as
well as its current files. Passed company targets remain outside the Downloads
page. No registry push occurs. Running the normal `refresh --force` command
above without identity/output overrides generates the default OpenRiak set for
the docs.

`--output` automatically disables publication, metadata regeneration, and preview
updates. `--no-docs` makes the intent explicit and requires `--output` so the
results cannot enter the watched docs cache indirectly. Output paths overlapping
the docs content, generated metadata, or built-in test caches are rejected.

Rebuild-only mode (`--do-not-test`) preserves approved labels. It rejects label
change options (`--vendor`, `--source`, `--url`); use generation/refresh for those.
For an approved company set, select it with `--namespace tiotjp --output PATH
--do-not-test`; its recorded labels remain unchanged. The file headers continue
to credit TI Tokyo as the creator of the generator, independently of image labels.

Progress counters are zero-padded to the width of the total, for example
`[01/35]`. Continuation lines and per-target results are indented so their
timestamps align with the target line.

To rebuild only already-approved groups without running integration tests:

```sh
tools/openriak-docker/openriak-docker refresh \
  --all --yes --do-not-test --extra-namespace tiotjp --timeout 1800
```

`--do-not-test` uses the saved, approved Dockerfile and other artifacts exactly
as tested. It verifies their SHA-256 values against the group and individual
platform approvals before building. It does not regenerate files, cookies, or
release-image digests, and it does not change test timestamps or publish new
test results. Groups without a passed approval are skipped; changed or incomplete
approved files are errors. An older approved renderer remains usable when its
saved files and approvals still match. `--force` and `--retry-failed` cannot be
combined with `--do-not-test`, because those options regenerate or retest files.

This mode rebuilds all approved platforms with `--no-cache`, exports the OCI
archive, then reuses those layers to load the host architecture locally. Build
commands and separate `built`/`failed` records are stored under
`{group-directory}/rebuilds/{run-id}/`; these are not new integration passes.
The original passed report and downloadable files remain unchanged. The
Dockerfile's package-installation checks still run as part of its build.

`--extra-namespace tiotjp` retains every original tag and adds a corresponding
`tiotjp/openriak-kv:...` tag, including applicable OS, version, and `latest`
aliases. Repeat the option to add more namespaces. The tags apply to the OCI
archive and, where supported, the host-platform image loaded into Docker; no
registry push occurs. Extra namespaces also apply to builds made by a normal
refresh. A passed group skipped by a normal refresh remains skipped; use
`--do-not-test` to rebuild it and add the extra namespace. Additional tags are
recorded in the build report, not added to the original test approval.

To follow a background run, use the exact `tail -n 100 -f` command printed by
`--nohup`. Ctrl-C stops the log viewer. To stop the worker gracefully, use the
printed `kill -TERM PID` command.

Use `--retry-failed` instead of `--force` to resume. An unchanged group's passed
platforms are retained, including when another platform failed. A force refresh
resolves fresh release digests, creates a new initial cookie, and retests every
platform. Architecture-specific filters select the entire matching OS/OTP group,
including its other package-backed architectures. `matrix --json` lists the
shared image, aliases, platforms, and individual package selections without
pulling or building anything.

The script requires Docker access, Buildx, Compose, Python 3, and Node.js. It
creates/reuses the `openriak-kv-multiarch` Buildx container builder. `refresh`,
including `--do-not-test`, starts it when needed and keeps it running across the
selected groups. On completion, failure, Ctrl-C, or SIGTERM, it stops a builder
that was initially stopped or was created by this invocation; an initially
running builder stays running. The builder and its cache are retained. Runs
that skip every build, and `--whatif`, leave the builder untouched. Docker works
without sudo in this WSL checkout; run as the repository owner so generated
files remain writable. Emulated builds and tests retain the selected phase
timeout, including `riak admin test` on the single node and every cluster node.

`refresh`, `generate`, and `cleanup` use a common `--timeout` default of 1,800
seconds per operation or readiness wait. Cleanup applies it to Docker commands
as well as worker shutdown. Readiness probes share the wait's remaining budget;
there is no hidden 300-second cluster minimum. This is not a whole-matrix limit.
Generated image healthchecks and Compose shutdown grace have separate settings:

| Generator option | Default | Meaning |
| --- | --- | --- |
| `--healthcheck-interval` | `10s` | Time between health probes |
| `--healthcheck-timeout` | `60s` | Maximum duration of one probe |
| `--healthcheck-start-period` | `120s` | Startup period before failures count; `0` disables it |
| `--healthcheck-retries` | `3` | Consecutive failures before unhealthy |
| `--stop-grace-period` | `120s` | Compose shutdown allowance before SIGKILL |

Use these options with `refresh` or standalone `generate`. Durations accept
whole seconds, or `s`, `m`, and `h` suffixes (for example `--stop-grace-period 3m`).
Health settings are written to the Dockerfile and inherited by both Compose
examples. Stop grace is written to every service in both examples. Changes
invalidate the cached generated files and require retesting. `--do-not-test`
rejects these overrides because it must rebuild the approved files unchanged.
During testing, stop grace is bounded by the selected operation timeout.
Cleanup identifies harness Compose files by their directory and file names,
including runs created under a custom `TMPDIR` from an earlier invocation.

Base-image selection is configured in [`base-images.json`](base-images.json).
Each family has ordered `rules` with an `image` template; optional `architectures`
and `minimum_major` restrict a rule. Templates accept `{release}`, `{os_release}`
(the original metadata release), `{major}`, and `{architecture}`. `release_maps`
provide named substitutions such as RHEL-to-UBI versions; families can require a
mapping rather than falling back. `release_replacements` normalizes names such
as SUSE service packs, and `alias` reuses another family's mapping. Every image
must have an explicit release tag; `latest` is rejected. The selected base tag
is part of the cache inputs, so changed mappings require an affected target to
be regenerated and retested. Editing this file does not add package targets.

Runtime filesystem construction is configured separately in
[`runtime-images.json`](runtime-images.json). Only releases that have passed
the prototype integration tests are enabled. Target discovery and base-image
selection still come from the existing metadata and base-image configuration.

- `rpm-root` installs release identity, runtime dependencies and the official
  OpenRiak KV RPM into an empty filesystem, then copies it into `FROM scratch`.
  It retains the RPM database and `/usr/share/openriak-build/runtime-packages.txt`.
  Python, Perl, pip, setuptools and package-manager executables are excluded;
  unused libstdc++ Python debugger helpers are removed. Update these runtime
  images by rebuilding, since they do not contain DNF or RPM executables.
- `clean-root` installs into the selected OS image and exports its cleaned
  filesystem into `FROM scratch`. This prevents deleted base-image files from
  remaining in lower layers. Debian's runtime removes `perl-base` and dependent
  administration tools through apt, including its explicit essential-package
  removal flag. This is a runtime image, not a general-purpose Debian system.
  SUSE removes its unused registration helper through RPM as described above.

The release settings also support these reviewed cleanup options:

- `remove_packages` lists exact optional RPM names. Removal preserves dependency
  checks and fails if a retained package still requires one. CentOS 8 and RHEL 8
  omit Vim and sudo; the official OpenRiak KV launcher uses the retained
  `runuser` command instead of sudo. Oracle Linux 9 uses `rpm-root` to exclude
  libssh and its package-manager dependencies from the final filesystem.
- `minimum_packages` requires installed Debian or RPM packages to meet minimum
  security versions. Ubuntu Jammy requires `libc6 >= 2.35-0ubuntu3.15`, and Noble
  requires `libc6 >= 2.39-0ubuntu8.9`. Rocky 8 requires the gzip security update;
  Rocky 9 requires the reviewed glib2, expat and PAM updates. Exact floors are in
  `runtime-images.json`, shared across all KV versions, OTPs and architectures.
  Newer vendor updates are accepted; stale mirrors fail the build. Debian uses
  dpkg version comparisons; RPM uses its native versioned-provider checks before
  exporting the runtime filesystem. Rocky 9 exports a cleaned filesystem so
  superseded base-layer packages are not retained in the downloadable image.
- `remove_tar` removes tar after all package installation. Ubuntu Jammy and
  Noble export a filesystem without Perl or tar. Jammy uses
  `perl_removal: "dpkg"` to remove only Perl while retaining PAM/login; Noble uses apt to
  remove Perl and dependent administration tools. Jammy's final package database
  deliberately retains installation-tool dependencies on the removed Perl,
  just as dpkg depends on the removed tar. These images must be maintained by
  rebuilding; restore the missing installation tools before using apt in a
  derived image.

These settings apply to every metadata-backed KV version, OTP and architecture
for the configured OS release. See the [Medium CVE validation results](reports/medium-fixes-validation-2026-09-10.md)
for the amd64 tests and remaining findings. Updating the generator does not
replace existing approved downloads or registry images: use `refresh` to
regenerate and test changed inputs, then `push` for publication and fresh scans.
`--do-not-test` reuses approved Dockerfiles and cannot adopt these changes.

Debian 12 uses the reusable base image
`{namespace}/debian:bookworm-slim-for-openriak`, selected by the `base_image` and
`openssl_backport` settings in `runtime-images.json`. Its Dockerfile builds
OpenSSL 3.0.22 from checksum-pinned upstream source using checksum-pinned
Bookworm packaging. Debian configuration, shared-library names, symbol checks,
and both upstream test suites are retained. Both suites must pass before the
packages can reach the patched base; compiler and source files stay in discarded
build stages. The base contains no OpenRiak KV package, Erlang cookie or node
configuration. It retains Debian's package-management tools for reuse.

OpenRiak KV Dockerfiles use that base by immutable digest, with the namespace
selected for the KV image. They install the official OpenRiak KV package and
bundled OTP without compiling OpenSSL themselves. Existing runtime cleanup,
including Perl removal and export of the cleaned filesystem, remains in place.
All metadata-backed Debian 12 KV/OTP variants use the same rule. The cleaned
KV filesystem is still flattened, so removed files from the reusable base do
not remain in lower KV image layers.

A test-only patch checks actual loopback connectivity before running host-dependent
IPv6 tests: some builders allow binding an IPv6 socket but block its traffic.
The library keeps IPv6 enabled. For this backport, the upstream suites also
passed without that test-only patch in a separate container. The compatibility
probe exercises the packaged OTP over IPv4 and IPv6.

The package version is `3.0.22-0openriak1~deb12u1`, identifying an OpenRiak-maintained
backport, not an official Debian security update. A newer installed Debian package
is retained. Revisit this override when Bookworm provides equivalent fixes; the
upstream 3.0 public-support lifecycle ended on 7 September 2026. This update fixes
known issues but does not provide ongoing upstream support. Source hashes and the
retained Debian patches are recorded in `openriak_minimal.py` and the base Dockerfile.
See the [Debian 12 OpenSSL compatibility results](reports/openssl-backport-validation-2026-09-08.md)
for the three validated amd64 variants, crypto/TLS coverage and Scout caveat.

### Reusable patched Debian base

The [shared-base validation report](reports/patched-base-validation-2026-09-08.md)
records the approved base and successful tests of all three Debian 12 amd64 KV variants.

Build and publish the base **before** refreshing dependent Debian 12 KV images:

```sh
tools/openriak-docker/openriak-docker base refresh --namespace tiotjp
tools/openriak-docker/openriak-docker base push --namespace tiotjp --whatif
tools/openriak-docker/openriak-docker base push --namespace tiotjp
```

Then run the normal KV `refresh --force` with the same `--namespace`, followed
by the normal KV `push`. The base is an independent image: `push --all` selects
KV approvals only. Base publication is explicit through `base push`.

`base refresh` pulls and pins `debian:bookworm-slim`, generates its Dockerfile,
builds and checks every selected platform, saves an approved OCI archive, and
applies the tags locally for the host platform. It preserves a matching passed
cache. `base refresh --force` pulls the upstream release again and builds without
cached layers, including package upgrades and the OpenSSL tests. Changed files,
identity, platform selection or rendered content require `--force`.

The base also backports the upstream CVE-2026-13595 partition-pointer fix into
Bookworm's `libblkid1`, with version `2.38.1-5+deb12u3+openriak1`. Source,
Debian packaging and upstream patch downloads are checksum-pinned. Debian's
symbol checks, upstream blkid tests and a Valgrind regression run before export;
the regression must also reject the unpatched source. Other util-linux packages
retain Debian's versions: this backport does not claim to fix unrelated CVEs.

GNU tar is removed from the final base and final Debian 12 KV filesystems.
**This makes the base a runtime image, not a general-purpose Debian administration
image:** dpkg's tar dependency is intentionally absent, and ordinary apt/dpkg
installation needs tar bootstrapping first. The KV generator handles this by
temporarily mounting `/usr/bin/tar` from the immutable `package_tools_image`
configured for Debian 12 in `runtime-images.json`, installing tar for the package
installation phase, and purging it again before flattening the runtime. The tools
stage and mounted binary do not become runtime layers. Custom child Dockerfiles
must follow the same pattern; do not use a mutable tools-image tag.

Maintain the libblkid backport alongside the OpenSSL backport: review new Debian
updates, rebase on newer Bookworm packaging when appropriate, update pinned source
hashes and the tools-image digest deliberately, and rerun base and KV integration
tests. A new base digest requires `refresh --force` for otherwise unchanged,
already-passed KV images. Publication still requires explicit base and KV pushes.

`base push` validates the saved Dockerfile, archive, and tested platform image
IDs, then uses the same digest-preserving Skopeo upload and Docker Scout reporting
as KV pushes. Failed, interrupted, generated-only or modified bases cannot be
pushed. `base push --whatif` is read-only and does not contact Docker Hub.

To generate files for review without building or publishing:

```sh
tools/openriak-docker/openriak-docker base generate \
  --namespace tiotjp --vendor "TI Tokyo" \
  --source "https://github.com/TI-Tokyo/openriak-docs" \
  --url "https://www.tiot.jp/openriak-docs/" \
  --output "$HOME/openriak-patched-bases"
```

Use `base refresh --force` with the same options to replace generated-only
output with a built/tested approval. No base action updates documentation
metadata or published KV downloads. Base reports are separate from the KV
matrix, under `tools/cache/openriak-docker-bases/{namespace}/debian/bookworm-slim-for-openriak/`.
Each run retains a report, Dockerfile and OCI archive; detailed logs and archive
bytes are local diagnostics. Both refresh and push retain historical evidence.

| Option | Applies to | Meaning |
| --- | --- | --- |
| `--namespace NAME` | All base actions | Primary namespace; default `openriak`. |
| `--extra-namespace NAME` | All base actions | Additional namespaces for the same base tag; repeatable. |
| `--vendor`, `--source`, `--url` | Generate/refresh | Same label defaults as KV images. Push uses the approved labels. |
| `--platform PLATFORM` | Generate/refresh | Select a platform; repeatable. Defaults to the distinct Debian 12 platforms found in OpenRiak KV metadata. |
| `--cache-root PATH`, `--output PATH` | All base actions | Alternate cache/output parent; namespace/repository/tag subdirectories are added. |
| `--force` | Generate/refresh | Regenerate existing output; refresh also rebuilds/retests without cached layers. |
| `--whatif` | All base actions | Inspect cache decisions or push preflight without network calls or writes. |
| `--nohup` | All base actions | Run detached, printing the worker PID and timestamped log path. Ignored with `--whatif`. |
| `--timeout SECONDS` | All base actions | Per-command timeout; default `1800`. |
| `--wait-seconds SECONDS` | Push | Wait after uploads before Scout scans; default `5`. |
| `--scan-retries N`, `--scan-retry-delay SECONDS` | Push | Retry failed Scout calls; defaults `3` retries and `5` seconds. |
| `--reports-dir PATH` | Push | Alternate parent for timestamped push/CVE reports. |

Later base updates do not change already pinned KV Dockerfiles. Publish the new
base, then explicitly refresh/retest and push the dependent KV images. The
OpenSSL maintenance and CVE-status caveats above still apply.

Changes to the runtime strategy or renderer invalidate cached generation inputs.
Existing approvals and downloads remain intact until an explicit refresh. The
[prototype harness](experiments/README.md) tests only amd64, runs both the
single-node and five-node suites, and saves full compressed Scout evidence
without publishing images or replacing approved caches. These tests establish
runtime compatibility; they do not prove that every reported CVE is exploitable
or fixed. Vendor backports and absent affected components are assessed separately
in [the Markdown CVE assessments](../../content/openriak-kv/docker/README.md), with evidence under `reports/`.

### KV image aliases

Image tag aliases are selected from the entire metadata set, independent of
build order. For example:

- `openriak/openriak-kv:3.4.0-ubuntu-noble-otp26` selects that OS release and OTP.
- `openriak/openriak-kv:3.4.0-ubuntu-noble` selects its highest OTP.
- `openriak/openriak-kv:3.4.0-ubuntu` selects the most recent Ubuntu release and its highest OTP.
- `openriak/openriak-kv:3.4.0` selects the most recent Alpine release and its highest OTP.
- `openriak/openriak-kv:latest` selects that Alpine default for the highest OpenRiak KV version.

OS ordering uses numeric `release_version` metadata when present (for example,
Ubuntu 22.04/24.04), otherwise the numeric release. Aliases have exactly the
architecture coverage of their selected OTP group: currently 3.4.0's Alpine
OTP26 package exists only for ARM64, so its `:3.4.0` default is ARM64-only.
The `latest` tag is an OpenRiak KV output alias; OS base tags remain release-specific.

`refresh` does not push images to a registry. After all platform tests pass, Buildx exports
an OCI image archive containing the group's platforms and tags. On this host's
classic Docker image store, the script also loads the host architecture under
those tags. A local tag in that store represents one platform; the OCI archive
retains the multi-platform image. Building a downloaded Dockerfile with
`docker buildx build --platform linux/amd64,linux/arm64 --output type=oci,dest=image.oci.tar .`
requires a builder and an OS/OTP group supporting those platforms. See
[Docker's multi-platform build documentation](https://docs.docker.com/build/building/multi-platform/).

Shared caches use a separate schema (4) and directory:

```text
tools/cache/openriak-docker-multiarch/{version}/{image-tag}/
  Dockerfile
  compose.single.yaml
  compose.cluster.yaml
  example.env
  report.json
  platforms/{linux-amd64,linux-arm64}/report.json
  platforms/{platform}/runs/{run-id}/report.json
  runs/{run-id}/report.json
  runs/{run-id}/image.oci.tar
```

Current artifacts and compact reports are retained. Historical artifact copies,
command logs, and large OCI archives stay local and are ignored by Git. Each
platform tests the exact same shared files. A group is published only after all
its platforms pass, and its metadata contains one entry with all supported OS
IDs, architectures, and image aliases. Older architecture-specific downloads
remain available until their shared replacements pass; their cache evidence is
preserved, but does not count as testing the new runtime. Normal docs builds
only read these reports and never start Docker work.

OS aliases are defined once in `content/openriak-kv/metadata/os-aliases.json`,
shared with the Downloads page metadata adapter. An alias reuses its source OS's
package URL and checksum, but has its own OS release, base image, image tag,
cache directory, and integration test results. Native packages take precedence
when a native OS family exists. Duplicate packages within the same image target
are still deduplicated; different target OS families are not.

For example, `suse-16.0-x86_64` reuses the RHEL 9 package in a SUSE Linux
Enterprise 16.0 container (`registry.suse.com/bci/bci-base:16.0`), not a RHEL
container. Rocky Linux uses `rockylinux:{release}` and CentOS uses
`quay.io/centos/centos:stream{release}`. The SUSE installer uses `zypper` for
runtime dependencies and the package-bundled OTP runtime. These base mappings
follow the [SUSE container guide](https://documentation.suse.com/container/all/pdf/Container-guide_en.pdf),
[Rocky Linux container guide](https://docs.rockylinux.org/uk/guides/containers/podman_guide/),
and [CentOS container documentation](https://docs.centos.org/cloud-sig-documentation/rdo_on_okd/container_images_with_tcib/).

An alias is published only after its own single-node and cluster tests pass.
Reusing a package does not establish compatibility on the new OS. Existing
passed native caches remain as historical evidence; the shared runtime requires its own platform tests.

Current OpenRiak KV aliases select OS releases for runtime compatibility, rather
than release ancestry: RHEL 8 packages use Fedora 29 or SUSE 15 SP4; RHEL 9
packages use Fedora 43 or SUSE 16.0. These mappings live in `modernReleases`
in the shared alias manifest; legacy documentation retains its previous mappings.
Each target still requires its own passing integration tests before publication.

The metadata-derived 3.4.0/3.4.1 matrix includes package-backed SUSE,
Rocky Linux, CentOS, and Fedora targets. To build and test just SUSE 16.0 explicitly:

```sh
tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 --os-id suse-16.0-x86_64 \
  --timeout 1800 --retry-failed
```

`refresh` is the only operation that pulls an OS image or runs containers. A
complete cached target is skipped by default. Pass `--force` to pull the
release-specific base tag again, pin its newly resolved digest, regenerate the
files, build the image, and rerun the tests. Pass `--retry-failed` to retain
passed caches while regenerating failed, interrupted, or incompatible targets.
An incomplete or incompatible cache is reported as an error unless
`--retry-failed` or `--force` is present. A refresh checks that:

- `/etc/riak`, `/var/lib/riak`, and `/var/log/riak` use bind mounts and are populated;
- `nodename`, `ring_size = 8`, `storage_backend = leveled`, TicTac AAE, and storeheads can be configured;
- the node starts and `riak ping` returns `pong`;
- `GET /ping` returns HTTP 200 with the body `OK`;
- `riak admin test` exits successfully and confirms a read/write cycle on the
  single node and on every cluster node, with the selected phase timeout;
- the image healthcheck sees both `beam.smp` and a `pong` response;
- daemon startup, service readiness, transfer completion, monitoring, and
  graceful shutdown are reported in the container log;
- Protocol Buffers and HTTP are published on ports 8087 and 8098 by default.
- the generated cluster Compose file forms one stable cluster, with the same
  membership on every node, ready rings, completed transfers, healthy
  containers, and working CLI and HTTP pings.

## Runtime options and identification

Copy `example.env` to `.env` and edit the values before creating containers.
Both Compose examples pass these options to every node:

| Variable | Default | Purpose |
| --- | --- | --- |
| `TZ` | `Etc/UTC` | Named timezone, such as `Asia/Tokyo` or `America/New_York`. |
| `RIAK_UID` / `RIAK_GID` | empty | Retain packaged IDs, or supply nonzero numeric IDs for the `riak` account. |
| `RIAK_LOG_MAX_FILE_SIZE` | `1MB` | Initialize `logger.max_file_size` in a new configuration. |
| `RIAK_LOG_MAX_FILES` | `10` | Initialize `logger.max_files` in a new configuration. |
| `OPENRIAK_DOCKER_LOG_MAX_SIZE` | `10m` | Rotate Docker's JSON stdout/stderr logs at this size. |
| `OPENRIAK_DOCKER_LOG_MAX_FILES` | `3` | Retain this many Docker JSON log files per container. |
| `OPENRIAK_CPUS` | `0` | Per-node CPU limit, such as `2.0`; zero means unrestricted. |
| `OPENRIAK_MEMORY_LIMIT` | `0` | Per-node memory limit, such as `4g`; zero means unrestricted. |

For example:

```dotenv
TZ=Asia/Tokyo
RIAK_UID=1000
RIAK_GID=1000
RIAK_LOG_MAX_FILE_SIZE=5MB
RIAK_LOG_MAX_FILES=4
OPENRIAK_DOCKER_LOG_MAX_SIZE=10m
OPENRIAK_DOCKER_LOG_MAX_FILES=3
OPENRIAK_CPUS=2.0
OPENRIAK_MEMORY_LIMIT=4g
```

The CPU/memory example is illustrative, not a sizing recommendation. Limits
apply separately to each node, rather than to the five-node cluster as a whole.
Compose changes require recreating containers to change their Docker settings.
For `docker run`, use `--cpus`, `--memory`, and `--log-opt`; `OPENRIAK_*` resource
and Docker logging variables are Compose substitutions, not runtime controls.

Timezone data is installed in each image. Startup rejects unknown or unsafe
zone names. `TZ` is exported to the daemon, and entrypoint timestamps include
an offset, for example `2026-09-06T15:30:00+09:00`. OpenRiak KV's own log
formatter remains under its configuration's control. Changing the timezone
does not change the system clock or stored timestamps.

UID/GID overrides change only the container's `riak` account. An ID already
owned by another container account is rejected before account changes. Startup
runs as root to configure the account and recursively adjust ownership of the
config/data/log bind mounts, then invokes OpenRiak KV as `riak`. Consequently,
these ownership changes are visible on the host; changing IDs on a populated
volume can take time. Leave IDs empty to retain the package defaults. Do not
set Compose `user:` when using this initialization flow.

For an empty config volume, startup seeds packaged defaults and applies the
image/environment settings. A marker lets interrupted initialization finish on
the next start. For an existing `riak.conf`, live and disabled settings are
preserved, including nodename, ring size, backend, listeners, and logger limits.
Edit that mounted file deliberately to change an established node; changing an
ENV default does not overwrite it. The nodename must remain resolvable through
Docker DNS. Existing cookies remain authoritative; fresh followers still adopt
the coordinator cookie before starting OpenRiak KV.

`logger.max_file_size` and `logger.max_files` are the active settings in both
3.4.0 and 3.4.1. Limits apply per enabled logger handler. Docker log rotation is
separate from these file logs; neither limit covers arbitrary crash dumps or
other files written by applications.

The generated image carries these [OCI labels](https://github.com/opencontainers/image-spec/blob/main/annotations.md):

| Label | Value |
| --- | --- |
| `org.opencontainers.image.title` | `OpenRiak KV` |
| `org.opencontainers.image.description` | Package-backed OpenRiak KV with single-node and cluster startup support |
| `org.opencontainers.image.version` | OpenRiak KV version, e.g. `3.4.1` |
| `org.opencontainers.image.vendor` | `OpenRiak` by default; configurable with `--vendor` |
| `org.opencontainers.image.url` | `https://openriak.org` by default; configurable with `--url` |
| `org.opencontainers.image.source` | `https://github.com/OpenRiak/openriak-docs` by default; configurable with `--source` |
| `org.openriak.otp.version` | OTP version, e.g. `26` |
| `org.openriak.os.name` | OS family, e.g. `ubuntu` |
| `org.openriak.os.release` | OS release identifier or codename, e.g. `noble` |
| `org.openriak.os.version` | Numeric `release_version` from metadata, e.g. `24.04`; falls back to the release identifier when absent |
| `org.openriak.image.tag` | Original canonical image reference, before aliases or extra namespaces |

Inspect them with `docker image inspect IMAGE --format '{{json .Config.Labels}}'`.
Architecture is already part of Docker's image metadata. Saved Dockerfiles do
not invent build timestamps, source revisions, or an aggregate license for the
OS and bundled packages. Rebuilding approved files retains their identification.

The integration harness tests a non-default timezone and UID/GID, checks mount
ownership, image labels, and Docker log limits on every node, and checks that
an operator-edited single-node configuration survives startup unchanged.

List targets without changing anything:

```sh
tools/openriak-docker/openriak-docker matrix --version 3.4.0
```

Manually refresh one target:

```sh
tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 \
  --os-id alpine-3.21-x86_64 \
  --download-id otp24-x86_64-r1 \
  --force
```

The generated cluster contains five nodes by default. To generate another
size, pass `--cluster-nodes N` (2 through 253). This changes only how many
services are written to `compose.cluster.yaml`; no configured node count is
passed to the containers or used by the coordination protocol.

The complete OpenRiak KV matrix (3.4.0 and newer) is deliberately guarded
because it is large:

```sh
tools/openriak-docker/openriak-docker refresh --all --yes
```

Legacy architecture-specific runs remain under:

```text
tools/cache/openriak-docker/{version}/{os-id}/{download-id}/runs/{UTC-run-id}/
```

New group and platform runs use the multiarch layout above.

The same target directory contains the current `Dockerfile`,
`compose.single.yaml`, `compose.cluster.yaml`, `example.env`, and
`report.json`. Per-command output is kept under the run's `logs/` directory. A passed run is copied to
`content/static/openriak-kv/downloads/docker/` so Hugo can publish the
Dockerfile, both Compose files, and the sample environment file. Failed runs
remain cached but are not advertised on the downloads page.

Git retains the current target artifacts and every historical run's compact
`report.json`. Historical `logs/`, `Dockerfile`, `compose.single.yaml`, and
`compose.cluster.yaml`, and `example.env` copies are local diagnostics and are
ignored by Git. CI systems that require full audit logs should upload those
ignored files as workflow artifacts rather than add them to the repository.

To restore static copies from already-tested cache entries without pulling,
building, or testing anything:

```sh
tools/openriak-docker/openriak-docker sync-static
```

The generated `compose.single.yaml` names its one container after the full
target and uses a matching relative directory containing `config`, `data`, and
`logs`. Copy `example.env` to `.env` to see and edit every supported Compose
variable. The single-node file uses `OPENRIAK_CONTAINER_NAME`,
`OPENRIAK_PB_PORT`, `OPENRIAK_HTTP_PORT`, and
`OPENRIAK_{CONFIG,DATA,LOGS}_PATH`. Both Compose files use
`OPENRIAK_NODE_1_HOST`, whose default is `node-01.cluster-a.openriak`. The
network alias, container hostname, and default Erlang nodename all derive from
that one value; the resulting nodename is
`openriak-kv@node-01.cluster-a.openriak`.

`compose.cluster.yaml` gives each node a distinct stable Docker DNS alias and
uses it for the Erlang nodename. Docker assigns addresses without a hard-coded
subnet. The file mounts a shared cluster-control directory and
sets `role=coordinator` on exactly one service; an omitted or empty `role`
means follower. Both roles are logged at startup. Followers remove their own
stale control files, discover their current IPv4 address, and advertise their
nodename and address for discovered coordinator markers. The coordinator
removes all stale coordinator markers, publishes its stable nodename and
current address under a new random suffix, and verifies that each advertised
nodename resolves to its advertised address before approval. Followers then
run their own join command, and the coordinator continuously plans and commits
non-empty joined batches. Coordination progresses through `ready`, `approved`,
`joined`, and `complete` files. Each file contains the node's stable nodename,
current IPv4 address, coordinator, and suffix. Riak's ring state remains
authoritative after restarts, and any bootstrap failure is published so
participating nodes stop cleanly.

Every regenerated group gets a new public `openriak-` cookie followed by 32
lowercase hexadecimal characters. The same initial default is documented in
its Dockerfile, Compose files, and `example.env`. Startup preserves an existing
live `distributed_cookie` setting in the mounted `riak.conf`, even when the
image or environment supplies a different cookie. To rotate an established
cookie, deliberately change the persisted configuration on all cluster members.

A fresh follower waits for exactly one valid `*-coordinator` file and adopts its
`cookie` value before running `riak chkconfig` or starting the daemon. The marker
also carries nodename, IPv4 address, coordinator identity, and session suffix;
contents and DNS must match. Missing, invalid, or ambiguous markers prevent
startup. New coordinators use their image/environment cookie; restarted
coordinators publish their preserved cookie. An initialization marker prevents
an interrupted first startup from treating the package's default cookie as an
established cluster cookie. The effective cookie is logged at startup.

For an image upgrade, retain the node's existing config/data/log mounts and
nodename. New Compose defaults have architecture-free image/container names;
point their path variables at your existing directories when migrating from
older examples. Fresh followers require a coordinator using the new cookie
marker format: upgrade the coordinator first when migrating this bootstrap
protocol. Already-clustered nodes with persisted configuration keep their cookie
and can restart without waiting for a marker. The shared control directory
contains the cluster cookie and belongs to the participating nodes.

The integration harness sets a persisted single-node cookie different from the
new image default, and supplies different defaults to fresh followers. It checks
that the former is preserved and every follower adopts the coordinator cookie.

The image entrypoint starts OpenRiak with `riak daemon`, waits for BEAM and `riak
ping`, waits for the `riak_kv` service and all Riak transfers, and then monitors
the BEAM process at the interval set by `RIAK_MONITOR_INTERVAL_SECONDS`. It
logs every lifecycle stage to standard output. `SIGTERM`, `SIGINT`, and
`SIGHUP` trigger `riak stop` followed by a wait for BEAM to exit. `SIGKILL`
cannot be trapped or handled by any container entrypoint; use `docker stop` or
send `SIGTERM` when graceful shutdown is required.

Run the unit tests with:

```sh
python3 -m unittest discover -s tools/openriak-docker/tests -v
```

`refresh` updates the version's `dockerImages` metadata after publishing each
target, including removing failed entries. It also updates metadata when every
selected target is skipped. `sync-static` republishes the files and updates
metadata without retesting. These commands require Node.js for the metadata
adapter; a metadata error preserves completed test reports for retry.

To update only the tested Docker lists in existing version adapters, preserving
OS aliases and other metadata without Docker work or a full metadata rebuild:

```sh
node tools/scripts/sync-product-metadata.js --docker-only \
  --include-version openriak-kv=3.4.0 \
  --include-version openriak-kv=3.4.1
```

The development Hugo container uses a separate copy under
`/tmp/openriak-development-data`. Its Docker metadata watcher propagates changed
`dockerImages` arrays from the repository adapters within about one second,
preserving the preview's other fields. Hugo then reloads the changed data.
Unchanged files cause no rebuild; the watcher does not pull, build, or test images.

Alias compatibility fixes (2026-09-05): Fedora 28 lacks the `OPENSSL_1_1_1`
symbols needed by the RHEL 8 OTP26 runtime. Fedora 34 and SUSE 15 SP4 lack
`GLIBC_2.34` required by the RHEL 9 runtime. The crypto NIF additionally requires
`OPENSSL_3.4.0`, so Fedora 36 and SUSE 15 SP6 cannot satisfy that requirement.
Fedora 43 and SUSE 16.0 supply OpenSSL 3.5. The SUSE installer selects
`libopenssl1_1` for RHEL 8 packages and `libopenssl3` for RHEL 9 packages. See the
[Fedora 43 OpenSSL package](https://packages.fedoraproject.org/pkgs/openssl/openssl/fedora-43.html) and
[SUSE 16.0 base image](https://registry.suse.com/repositories/bci-bci-base-16-0).
RPM image builds check the bundled Erlang runtime and crypto NIF before starting
integration tests. Service startup exits immediately if BEAM dies. Test runs
retain node log files under `runs/.../logs/riak-runtime/`, including on failure.
SIGTERM and Ctrl-C interrupt the matrix, clean up the active test, and save an
interrupted report. Passed caches remain reusable.

SUSE installs `gawk` explicitly. CentOS Stream 8 uses its release archive at
`https://vault.centos.org/8-stream/` with RPM signature checking retained.

If integration tests pass but static publishing fails on permissions, the
passed reports and current cache files are retained. Correct ownership of the
reported static download directory, then use `sync-static` and the
`--docker-only` metadata update above; successful tests need not be repeated.

Generated Dockerfiles and Compose files identify TI Tokyo, the OpenRiak project,
and the original image tag, and include an editing warning. Each environment
setting has a short explanatory comment. Dockerfile comments precede `ENV`
instructions so they cannot accidentally become part of an environment value.
Copy the downloaded `example.env` to `.env` before using Compose. Historical
reports using `.env.example` remain readable and their passed caches reusable.

The 2026-09-05 presentation update adds comments and renames the example file
without changing executable configuration, cookies, or pinned images. Legacy current
reports record the original tested hashes in `presentation_update`, retain their
test timestamps, and link to the unchanged historical run reports. Published
hashes describe the updated files; these documentation changes do not claim a
new integration run.

`riak admin test` output is retained in `logs/admin-test.log` for the single node
and `logs/cluster-node-N-admin-test.log` for each cluster member. New runs record
these checks in the report. Existing passed reports without this check remain
cached; use an explicit `refresh --force` selection to include it in a new test
run. The comment and filename update does not add test results to old reports.

## Push images and collect Docker Scout reports

### CVEs on the Downloads page

The CVE column between Image tag and Downloads shows one clickable badge per
image, displaying its highest reported CVSS score and severity (for example,
`6.5 M`). Clicking it opens the image's Scout findings. An asterisk marks
incomplete scans; unscanned images show `Not scanned` or `Pending`, and completed
scans without findings show `None`.
Rows show the CVE ID with a copy button, the numeric CVSS score and severity
letter (C/H/M/L; U means unspecified), our status, and details links. Duplicate
findings across packages/architectures are combined, using the highest reported
severity and score and listing the affected architectures. The information icon
opens Docker Scout's CVE page (the destination used by Docker Hub's CVE details);
the external-link icon opens the affected image digest on Docker Hub.

Edit the Markdown assessments under
`content/openriak-kv/docker/{version}/{docker-tag}/cve-{year}-{number}.md`.
See [the assessment editing guide](../../content/openriak-kv/docker/README.md).
The image field omits the namespace, so the same assessment applies to all
registries and namespaces for that image tag. YAML frontmatter holds flags,
an optional status, and evidence conditions; the Markdown body explains them.

For example, `3.4.1/3.4.1-rhel-9-otp26/cve-2026-40356.md`:

```markdown
---
cve-id: CVE-2026-40356
image: openriak-kv:3.4.1-rhel-9-otp26
flags:
  falsePositive: true
appliesTo:
  packageVersions:
    krb5:
      - "1.21.1-10.el9_8"
---

Fixed in vendor package `krb5-libs 1.21.1-10.el9_8`.
See [RHSA-2026:19357](https://access.redhat.com/errata/RHSA-2026:19357).
```

| Flag | Displayed status | Included in the overall image rating? |
| --- | --- | --- |
| `mitigated` | Mitigated | Yes; reduced exposure is not proof that the CVE no longer applies. |
| `fixedByBackporting` | Fixed by backporting | No, when the evidence conditions match. |
| `notRelevant` | Not relevant | No, when the evidence conditions match. |
| `falsePositive` | False positive | No, when the evidence conditions match. |
| `unfixable` | Unfixable | Yes; lack of a fix does not remove the vulnerability. |

Use the Markdown body to explain the affected component, why the assessment applies,
and the package version, advisory or runtime evidence supporting it. Do not mark
an issue unfixable merely because no vendor fix is available yet. If no flags
are true, `status` may supply a short label; otherwise it defaults to
`Under investigation`. Unfixable takes precedence over exclusion flags.

Omitted flags default to false. Missing assessments display `Under investigation`.
Explanations render as Markdown, including links, lists and inline code. These
files enrich the shared generated metadata; they do not become documentation
pages or search entries. The preview watcher detects added, changed and deleted
assessment files without another build, push or scan. Malformed assessments
produce an error; they are never silently used to suppress findings.

`appliesTo.packageVersions` maps Scout package names to exact reviewed versions.
Every reported package and architecture for that CVE must match. This prevents
a newer amd64 package from hiding an older arm64 package. No version comparison
or automatic acceptance of later versions is performed. For assessments about
files absent from a particular image, use `appliesTo.imageDigests`, a list of
reviewed OCI image/index SHA-256 digests. If both conditions are present, both
must match. Unmatched or missing evidence displays `Needs review` and retains
the Scout rating. An entry without `appliesTo` is an explicit assessment for
all reports for that namespace-independent image tag. Use a scope whenever the
assessment depends on particular package versions or image contents.

The panel always retains Scout's original severity and score. Excluded findings
have their rating crossed out and do not contribute to the image badge. A
complete scan with only excluded findings displays `None`; a partial scan still
displays `Incomplete` or marks its remaining rating with an asterisk. Editing
assessments never modifies the saved Scout evidence.

Only reports matching the current passed image's approval run and artifact
checksums are used. Each platform's scan digest must match the archive from a
verified registry upload. Missing, pending, and partial scans are labelled;
only a complete scan with no findings says that no CVEs were reported.

Normal metadata generation reads the saved reports without running Docker or
Scout. The development preview watcher also notices new reports and status
edits automatically. Restart an already-running preview once after installing
this watcher change. To refresh the generated repository data manually:

```sh
node tools/scripts/sync-product-metadata.js --docker-only \
  --include-version openriak-kv=3.4.0 \
  --include-version openriak-kv=3.4.1
```

The logo is the [CVE logo supplied via Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Common_Vulnerabilities_and_Exposures_logo.svg),
stored locally at `layouts/docs-theme/static/images/cve.svg`.

### Upload and scan

`push` uploads the saved OCI archive from each selected **passed refresh run**.
It does not rebuild, test, change approved files, or update documentation.
Both the primary image tag and all recorded secondary tags are uploaded,
including recorded extra namespaces. All architectures and image attestations
are preserved using [Skopeo's `copy --all --preserve-digests`](https://github.com/containers/skopeo/blob/main/docs/skopeo-copy.1.md).
The host-only Docker image store is not used as the upload source.
Archives may contain a multiarchitecture index or a direct single-architecture
manifest. Both formats are accepted, with the original digest preserved and the
contained platforms checked against the passed approval.

Install Skopeo once (Ubuntu/WSL), and log in to Docker Hub as your normal user
if you have not already done so:

```sh
sudo apt-get install skopeo
docker login
```

Skopeo must support `skopeo copy --preserve-digests`. Older Ubuntu repositories
may install Skopeo 1.4.1, which lacks this option and cannot copy the image
attestations correctly. If `skopeo copy --help` does not list the option, use the
[current Skopeo installation instructions](https://github.com/containers/skopeo/blob/main/install.md)
to install a newer release. Uploads check this requirement before accessing
credentials or pushing anything; `--whatif` only validates the cached files.

Docker Scout must also be installed (`docker scout version`). The command uses
your Docker Hub login from `DOCKER_CONFIG` or `~/.docker/config.json`. Docker
credential helpers, including Docker Desktop's global `credsStore`, are supported.
Credentials are passed to Skopeo through a temporary file with mode 0600, removed
on normal completion or interruption. Credentials are never included in command
arguments or reports. Temporary files follow the machine's `TMPDIR` setting.

Preview all eligible images and tags without accessing the registry or writing files:

```sh
tools/openriak-docker/openriak-docker push --all --whatif
```

Push all passed images and scan them:

```sh
tools/openriak-docker/openriak-docker push --all --yes
```

Or select versions and optionally add another namespace:

```sh
tools/openriak-docker/openriak-docker push \
  --version 3.4.0 --version 3.4.1 \
  --extra-namespace tiotjp --wait-seconds 5
```

The recorded primary namespace is used automatically. `--namespace tiotjp`
filters to approvals whose primary namespace is `tiotjp`; it does not rename
images or change their labels. Use `--cache-root "$HOME/openriak-docker-tiotjp"`
to publish a standalone company cache. The command never falls back to another
cache or an unapproved local image.

Before uploading anything, the command checks every selected passed approval,
the four approved artifact hashes, each platform's test evidence, the saved run
report, and OCI blob hashes/platforms. Missing, changed, or conflicting approved
assets block the invocation. Failed/running/missing approvals are skipped.
The archive must belong to that passed refresh run: untested `rebuilds/` exports
are excluded. If cleanup removed an archive, regenerate it with `refresh` and
tests before publishing. Generator changes do not modify historical approvals;
run `refresh --force` first when the new image must include those changes.

Each tag is checked against the expected image manifest or index digest. If it already matches,
uploading is skipped and scanning still runs. After a copy, the registry digest
must match exactly. Copy failures and digest mismatches are recorded separately;
remaining tags/images continue. A successful digest check after a failed copy is
recorded as `verified_after_copy_error`, not silently treated as a clean upload.
Re-running `push` reconciles partially completed uploads by digest.

After **all uploads**, the command waits once for `--wait-seconds` (default 5),
then scans each architecture using its immutable registry manifest digest.
Aliases sharing that content reuse the same report. Only images with at least
one verified registry tag are scanned. The wait is a settling period, not a
guarantee that Docker Hub's asynchronous scan has completed: Scout CLI requests
its own analysis. Failed or malformed Scout responses are retried and retained;
a failed scan is never recorded as zero vulnerabilities.

Each invocation writes a new directory, printed at startup:

```text
tools/cache/openriak-docker-multiarch/pushes/{UTC-run-id}/
├── report.json
└── {version}/{image-tag}/
    ├── cve-report.json
    └── scout-output/{sha256}.gz
```

Each `cve-report.json` contains:

- Primary/secondary tags, expected and observed registry digests, and every upload outcome.
- Archive path, SHA-256 and size, full OCI index, architecture/attestation manifests,
  layer digests and image configurations/labels.
- The original approval and each platform's full test report, including tested
  timestamps, base-image digests, package URLs/checksums and artifact hashes.
- Per-platform immutable scan references, timestamps, and references to full Scout SARIF (CVE IDs,
  severities, scores, package identifiers, affected/fixed versions, locations and
  all other fields Scout returns), the complete JSON SBOM, and detailed text/EPSS output.
- Tool versions, settings, command arguments, complete stdout/stderr, durations,
  exit codes, retry attempts and errors. Large stdout is referenced rather than embedded.

Per-image report schema 2 stores Scout payloads once in gzip files alongside the
report. `data_file` and `stdout_file` references include their relative path,
uncompressed SHA-256, byte length, compression and format. Successful parsed data
and its exact raw stdout share one payload; failed attempts are also retained.
No Scout fields, file locations, or original output text are discarded. Keep
the JSON and its `scout-output` directory together when copying or committing
evidence. Use `gzip -dc PATH/scout-output/HASH.gz` to read a payload.

The Downloads metadata reader accepts both historical inline reports and schema
2 reports, verifies payload hashes, and treats missing/corrupt payloads as
incomplete scans. The preview watcher detects changes to payload files as well
as the report. Restart an already-running preview once when installing this
reader update.

Compact existing completed, failed, or interrupted reports without Docker,
uploads, scans, or changes to their findings:

```sh
python3 tools/openriak-docker/openriak_cve_storage.py compact \
  tools/cache/openriak-docker-multiarch/pushes
```

Pass one or more individual `cve-report.json` paths or report directories; add
`--whatif` to list candidates without changes. Conversion verifies a lossless
round-trip before atomically replacing each JSON index, records its original
SHA-256 and byte size, refuses active reports, and leaves schema 2 reports alone.
For Python audit code, `openriak_cve_storage.hydrate_report(path)` restores the
full `data` and `stdout` fields from either storage format.

Reports are written atomically throughout the run. An interruption leaves useful
partial reports; rerunning creates a new history directory. CVE findings do not
make the command fail: exit 0 means uploads and report collection completed,
**not** that the images have no CVEs. Upload/scan failures return 1; selection or
preflight errors return 2; interruption returns 130. No images are published to
Docker Hub by `refresh`, `generate`, `sync-static`, or normal docs builds.

See the [Scout CVE](https://docs.docker.com/reference/cli/docker/scout/cves/) and
[SBOM](https://docs.docker.com/reference/cli/docker/scout/sbom/) command references
for the upstream report formats.

## Command reference

Run from the repository root:

```sh
tools/openriak-docker/openriak-docker COMMAND [OPTIONS]
```

All commands apply exclusively to **OpenRiak KV 3.4.0 and newer**.

| Command | Purpose |
| --- | --- |
| `matrix` | List metadata-derived targets, platforms, tags and cache status. Makes no changes. |
| `refresh` | Generate files, build images, test, cache results and publish passed downloads to the docs. |
| `generate` | Generate standalone files without building, testing or updating the docs. May pull base images to resolve digests. |
| `sync-static` | Republish existing passed caches and update Docker download metadata. No pulling, building or testing. |
| `cleanup` | Preview or remove older generator artifacts and, optionally, associated Docker resources. |
| `push` | Push passed OCI exports and all recorded aliases to Docker Hub, then save Scout CVE reports for every platform. |
| `base generate`, `base refresh`, `base push` | Manage the reusable patched Debian base independently; see [base commands and options](#reusable-patched-debian-base). |

`-h` or `--help` works globally and after every command:

```sh
tools/openriak-docker/openriak-docker refresh --help
```

### Selection options

| Option | Commands | Explanation |
| --- | --- | --- |
| `--version VERSION` | `matrix`, `refresh`, `generate`, `push` | Select a version. Repeat to select several. |
| `--all` | `refresh`, `generate`, `push` | Select every eligible version in metadata. Mutually exclusive with `--version`. |
| `--yes` | `refresh`, `generate`, `push` | Required with `--all`, except with `--whatif`. |
| `--os-id PATTERN` | `matrix`, `refresh`, `generate`, `push` | Filter by exact metadata OS ID or a case-sensitive wildcard pattern such as `'oracle*'`. Repeat to select matches from any pattern. |
| `--otp VERSION` | `matrix`, `refresh`, `generate`, `push` | Filter by OTP version. |
| `--download-id ID` | `matrix`, `refresh`, `generate` | Filter by package download ID. |
| `--json` | `matrix` | Output structured JSON. |

Without `--version`, `matrix` lists all eligible versions. `refresh`, `generate` and `push`
require either `--version` or `--all`. For generation/builds, an
architecture-specific selection includes the other architectures belonging to
the same shared OS-release/OTP image.

OS patterns support `*` (any sequence), `?` (one character), and character sets
such as `[89]`. Quote patterns to prevent expansion by your shell. A selection
that matches no metadata targets is an error. Other filters and cache rules
still apply; selecting an OS does not force a passed cache to rebuild.

Preview all Oracle images, then force regeneration, building and testing of them:

```sh
tools/openriak-docker/openriak-docker matrix --os-id 'oracle*'
tools/openriak-docker/openriak-docker refresh --all --yes --os-id 'oracle*' --force
```

Use `--version` instead of `--all --yes` to restrict the versions, and include
your usual namespace/vendor options when rebuilding branded images.

Repeat `--os-id` to select multiple OS families in one run. Matches are combined
without duplicating targets, even when patterns overlap:

```sh
tools/openriak-docker/openriak-docker matrix --os-id 'fedora*' --os-id 'oracle*'
tools/openriak-docker/openriak-docker refresh --all --yes \
  --os-id 'fedora*' --os-id 'oracle*' --force
```

### Shared refresh and generate options

| Option | Default | Explanation |
| --- | --- | --- |
| `--timeout SECONDS` | `1800` | Maximum time per operation or readiness wait, not the whole run. |
| `--cluster-nodes N` | `5` | Number of services in the generated cluster example; accepts 2–253. |
| `--nohup` | Off | Run in the background; print PID, timestamped log path and monitoring commands. |
| `--force` | Off | Regenerate even existing output, pulling fresh release-image digests. `refresh` also rebuilds and retests. |
| `--vendor TEXT` | `OpenRiak` | Image vendor label. |
| `--source URL` | `https://github.com/OpenRiak/openriak-docs` | Image source label. |
| `--url URL` | `https://openriak.org` | Image project URL label. |
| `--namespace NAME` | `openriak` | Primary image-tag namespace. |
| `--output PATH` / `--output-dir PATH` | Docs cache for `refresh` | Use a separate output/cache directory and disable docs publication. **Required for `generate`.** |
| `--no-docs` | Off | Explicitly disable docs updates. Requires `--output`, which already implies this behavior. |

### Generated healthcheck and shutdown options

These options are available on both `refresh` and `generate`.

| Option | Default | Explanation |
| --- | --- | --- |
| `--healthcheck-interval DURATION` | `10s` | Interval between health probes. |
| `--healthcheck-timeout DURATION` | `60s` | Maximum duration of one probe. |
| `--healthcheck-start-period DURATION` | `120s` | Startup allowance before failures count. Accepts `0`. |
| `--healthcheck-retries N` | `3` | Consecutive failures before Docker marks the container unhealthy. |
| `--stop-grace-period DURATION` | `120s` | Compose shutdown allowance before Docker sends SIGKILL. |

Durations accept whole seconds or `s`, `m`, and `h` suffixes: `90`, `90s`, `2m`,
`1h`. Except for the start period, these settings must be positive. Healthcheck
and shutdown settings are separate from the command's operation timeout.

### Additional refresh options

| Option | Explanation |
| --- | --- |
| `--retry-failed` | Retry failed, interrupted or incompatible caches while preserving unchanged, complete passed caches. |
| `--do-not-test` | Rebuild approved cached Dockerfiles and apply their tags without regeneration or testing. |
| `--extra-namespace NAME` | Also apply every image tag under another namespace. Repeatable; does not push images. |
| `--whatif` | Show what would rebuild, skip or be blocked, and why. No Docker operations or file changes. |
| `--keep-test-workdir` | Retain temporary integration-test directories for inspection. |

`--force`, `--retry-failed` and `--do-not-test` are mutually exclusive.

Without those switches, `refresh` builds missing caches, skips compatible passed
caches, and reports existing failed/incompatible caches as errors.
`--do-not-test` rejects vendor/source/URL and healthcheck/shutdown overrides
because approved files must remain unchanged.

### Push and Scout options

`push` accepts `--version` (repeatable) or `--all`, plus `--yes`, `--os-id`, and
`--otp` as described above. It has no automatic default selection.

| Option | Default | Explanation |
| --- | --- | --- |
| `--namespace NAME` | Any recorded namespace | Filter by the approved primary namespace. Does not retag. |
| `--extra-namespace NAME` | None | Also push every approved alias under this namespace. Repeatable. |
| `--cache-root PATH` | `tools/cache/openriak-docker-multiarch` | Read existing approvals and OCI archives from this cache/output directory. |
| `--reports-dir PATH` | `CACHE_ROOT/pushes` | Parent directory for timestamped push/CVE reports. |
| `--wait-seconds N` | `5` | Wait once after all uploads before scanning; zero disables the wait. |
| `--scan-retries N` | `3` | Additional attempts after a failed or malformed Scout response. |
| `--scan-retry-delay N` | `5` | Seconds between failed Scout attempts. |
| `--timeout SECONDS` | `1800` | Timeout for each upload, registry inspection, or Scout command. |
| `--whatif` | Off | Validate saved evidence and list intended tags/digests; no network, credentials, or file changes. |

### Cleanup options

| Option | Default | Explanation |
| --- | --- | --- |
| `--before DATE_OR_TIMESTAMP` | Now | Remove only eligible activity older than this cutoff. Logs the exact resolved timestamp. |
| `--remove-all` | Off | Also include older current caches, Docker download metadata, published files, associated images and dedicated builder cache; stop eligible older workers. |
| `--delete` | Off | Apply the cleanup. Without it, only preview. |
| `--timeout SECONDS` | `1800` | Timeout per Docker operation or worker-shutdown wait. |

Accepted cutoff examples:

- `2026-09-06` — midnight in the machine's local timezone.
- `2026-09-06T15:30:00` — local date and time.
- `2026-09-06T15:30:00+09:00` — explicit timezone.
- `2026-09-06T06:30:00Z` — UTC.

`sync-static` has no additional options beyond help. Base-image mappings are
configured in [base-images.json](base-images.json), rather than through
command-line switches.
