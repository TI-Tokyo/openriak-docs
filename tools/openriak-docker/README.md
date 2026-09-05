# OpenRiak KV Docker cache

This tool derives Docker targets from the authoritative release records in
`content/openriak-kv/metadata/{version}/supported-os.json` and
`downloads.json`. It accepts OpenRiak KV 3.4.0 and newer only; legacy Riak KV
releases are rejected. It does not run as part of a normal documentation build.

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
passed native caches remain reusable without a schema bump or retest.

Current OpenRiak KV aliases select OS releases for runtime compatibility, rather
than release ancestry: RHEL 8 packages use Fedora 29 or SUSE 15 SP4; RHEL 9
packages use Fedora 43 or SUSE 16.0. These mappings live in `modernReleases`
in the shared alias manifest; legacy documentation retains its previous mappings.
Each target still requires its own passing integration tests before publication.

The 3.4.0/3.4.1 matrix now contains 44 targets, including twelve new SUSE,
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

Each run is retained under:

```text
tools/cache/openriak-docker/{version}/{os-id}/{download-id}/runs/{UTC-run-id}/
```

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

Every refresh generates a new `openriak-` cookie followed by 32 lowercase hex
characters. The same cookie is baked into that target's Dockerfile and written
to `example.env`, so all services generated together can communicate while
unrelated generated images do not mix accidentally. OpenRiak logs the
effective cookie during startup. The cookie is public image configuration, not
a secret. For intentional rolling upgrades or mixed-image clusters, set the
same `OPENRIAK_DISTRIBUTED_COOKIE` value for every node.

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
without changing executable configuration, cookies, or pinned images. Current
reports record the original tested hashes in `presentation_update`, retain their
test timestamps, and link to the unchanged historical run reports. Published
hashes describe the updated files; these documentation changes do not claim a
new integration run.

`riak admin test` output is retained in `logs/admin-test.log` for the single node
and `logs/cluster-node-N-admin-test.log` for each cluster member. New runs record
these checks in the report. Existing passed reports without this check remain
cached; use an explicit `refresh --force` selection to include it in a new test
run. The comment and filename update does not add test results to old reports.
