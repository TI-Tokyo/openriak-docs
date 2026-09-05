# OpenRiak KV Docker generator and test cache — project handoff

You are continuing an in-progress feature in the OpenRiak documentation repository. Read this note completely, then inspect the repository before changing anything. Preserve all existing uncommitted work and cached test evidence. Do not reset, discard, or broadly regenerate unrelated documentation.

## Repository and current checkout

- WSL distribution: `Ubuntu`
- Repository: `/home/peter/GitHub/TI-Tokyo/openriak-docs`
- Branch: `titokyo-PJAC-new-site-wip`
- Current HEAD when this note was written: `5a21aec8` (`More tested Docker files`)
- Date of this handoff: 2026-09-05 (Asia/Tokyo)
- The working tree is intentionally dirty. It contains generator changes, tests, generated/cache artifacts, reports, logs, and static download copies. Treat all of them as user work.
- No matrix worker was running when this note was written. The old PID file had been removed. Docker itself requires `sudo` in this WSL environment; a non-interactive Docker status check could not be made because the sudo credential had expired.

The project is exclusively for **OpenRiak KV**, never legacy Riak KV and never OpenRiak TS. Accept OpenRiak KV 3.4.0 and newer only. Some metadata-sync commands elsewhere in the docs repository print `openriak-ts` progress because they synchronize every product; that output is unrelated to this Docker generator and must not be allowed to expand this feature's scope.

## Objective

Generate, build, test, cache, and publish downloadable Docker assets for every package-backed OpenRiak KV combination present in the documentation metadata:

- OpenRiak KV version
- supported operating-system release
- OTP version
- architecture

Normal docs builds must not perform this expensive work. Results are cached and are retested only by an explicit manual command. A forced refresh pulls the current image for the specific OS release tag, resolves and records its immutable digest, regenerates the assets, builds, and retests.

The immediate matrix requested by the user is every metadata-derived combination for OpenRiak KV 3.4.0 and 3.4.1. It currently contains 32 targets. ARM64/aarch64 builds run under emulation and may be slow; use 1,800 seconds for each expensive phase. The user is happy to let this run overnight and cares more about eventual completion than speed.

## Authoritative input and target discovery

For each version, derive targets only from:

```text
content/openriak-kv/metadata/{version}/supported-os.json
content/openriak-kv/metadata/{version}/downloads.json
```

These records originate from the TI Tokyo `files.tiot.jp` package server. Do not maintain a second hand-written OS list and do not filter by OS family. Aliased metadata entries must not create duplicate package targets. The definitive command-line view is:

```sh
tools/openriak-docker/openriak-docker matrix --version 3.4.0
tools/openriak-docker/openriak-docker matrix --version 3.4.1
```

The generator rejects pre-3.4.0 versions.

## Main implementation files

```text
tools/openriak-docker/openriak_docker.py
tools/openriak-docker/openriak-docker
tools/openriak-docker/README.md
tools/openriak-docker/tests/test_openriak_docker.py
```

The Python file contains target discovery, Dockerfile/Compose/environment rendering, cache/report handling, Docker orchestration, single-node tests, five-node cluster tests, and static publishing. The shell wrapper is the normal entry point.

Run the unit suite with:

```sh
python3 -m unittest discover -s tools/openriak-docker/tests -v
```

At handoff, all **25 unit tests pass**. This is not a substitute for the Docker integration matrix.

## Generated target layout and cache rules

Each target uses:

```text
tools/cache/openriak-docker/{version}/{os-id}/{download-id}/
├── Dockerfile
├── compose.single.yaml
├── compose.cluster.yaml
├── .env.example
├── report.json
└── runs/{UTC-run-id}/
    ├── report.json
    ├── Dockerfile
    ├── compose.single.yaml
    ├── compose.cluster.yaml
    ├── .env.example
    └── logs/*.log
```

The current target artifacts and current `report.json` are retained. Every historical run keeps a compact `runs/.../report.json`. Historical Docker/Compose/environment copies and detailed command logs are intentionally ignored by Git and are local diagnostics; CI should upload them as workflow artifacts rather than commit them. Do not delete the existing run directories while diagnosing failures.

Cache behavior:

- Default: skip a complete passed cache; report incomplete/incompatible caches as errors.
- `--retry-failed`: keep passed caches and regenerate/retest failed, interrupted, stale-running, or incompatible targets.
- `--force`: pull the release tag again, resolve its newest digest at test time, generate a new cookie and all files, rebuild, and retest even a passed cache.
- `sync-static`: publish existing passed cache entries without pulling, building, or testing.
- `--all` is deliberately guarded and requires `--yes`; explicit `--version` arguments do not require `--yes`.

`SCHEMA_VERSION` is currently 3. Be deliberate about changing it because incompatibility affects cache reuse.

## Docker image requirements and implementation

The build tag format is:

```text
openriak/openriak-kv:{version}-{os-name-and-release}-otp{otp}-{architecture}
```

For example:

```text
openriak/openriak-kv:3.4.0-alpine-3.21-otp24-x86_64
```

The image is built locally; this feature does not push images to a registry.

Dockerfile behavior:

- Uses a release-specific OS base tag, never `latest`.
- A refresh pulls that tag for the target platform and pins the generated Dockerfile to the resolved SHA-256 digest.
- Downloads the matching prebuilt OpenRiak KV package from the metadata URL on `files.tiot.jp`; it does not compile OpenRiak KV.
- Verifies the package checksum from metadata.
- Installs all OS dependencies needed by OpenRiak KV.
- Keeps Dockerfile operations readable, with one shell command per line and no chains of commands joined by `&&` or `;`. Defaults have a clearly marked configuration area.
- Declares `/etc/riak`, `/var/lib/riak`, and `/var/log/riak` as volumes.
- Exposes PB port 8087 and HTTP port 8098.
- Uses a daemon-oriented entrypoint, healthcheck, `STOPSIGNAL SIGTERM`, and a two-minute Compose stop grace period.
- Generates a different public Erlang cookie for each regenerated target: `openriak-` followed by 32 lowercase hexadecimal characters. The same default is put in the Dockerfile and `.env.example`, and startup logs the effective cookie. Users must deliberately override it with a common value for mixed-image or rolling-upgrade clusters.

Important package-family fixes already present in the source:

- Alpine installs `coreutils` in addition to its other runtime dependencies.
- Debian/Ubuntu use apt and install the package from the downloaded `.deb`.
- Amazon Linux, Oracle Linux, and RHEL explicitly install runtime RPM dependencies, retain an existing `curl` where present, install the package with `rpm -Uvh --replacepkgs --nodeps`, locate the package-bundled `escript`, and symlink it to `/usr/bin/escript` when needed.
- RHEL UBI base mappings are release-specific: RHEL 8 -> UBI 8.10; RHEL 9 -> UBI 9.8.
- The generated healthcheck currently uses a 60-second timeout and 120-second start period because emulated nodes are slow.

## OpenRiak runtime configuration and lifecycle

At startup, configuration replacement must find both live settings and disabled `##` settings. Leading/trailing whitespace and whitespace around `=` are ignored. For example, all of these represent a disabled setting that can be replaced:

```text
## ring_size = 64
##ring_size=64
    ##          ring_size  =        64
```

A single `#` is not treated as the OpenRiak disabled-setting marker.

The runtime sets or enables:

- a configurable nodename
- `ring_size = 8`
- `storage_backend = leveled`
- TicTac AAE
- storeheads
- HTTP/PB listeners suitable for containers

The entrypoint:

1. Logs whether the node is a Follower or Coordinator and logs the effective cookie.
2. Starts OpenRiak with `riak daemon`, not `riak console`.
3. Polls at one-second intervals until the BEAM process exists and `riak ping` returns `pong`.
4. Waits until `riak admin services` reports `riak_kv` up.
5. Waits for transfers to finish.
6. Enters a monitor/sleep loop instead of exiting. The node is supposed to stay alive.
7. On `SIGTERM`, `SIGINT`, or `SIGHUP`, logs shutdown, calls `riak stop`, waits for BEAM to exit, and then exits. `SIGKILL` cannot be trapped. Host Ctrl-C reaches Compose, which sends the normal stop signal; use `docker stop`/SIGTERM when graceful shutdown matters.

The image healthcheck verifies both that `beam.smp` exists and `riak ping` returns `pong`.

## Single-node Compose file

`compose.single.yaml` builds with `Dockerfile` in the same directory and also names the built image. Its default container name is:

```text
openriak-kv-{version}-{os-release}-otp{otp}-{architecture}-node
```

It uses a bridge network with a stable Docker DNS alias. The default host is controlled by the same variable used for the container hostname and OpenRiak nodename:

```yaml
hostname: "${OPENRIAK_NODE_1_HOST:-node-01.cluster-a.openriak}"
```

The resulting default nodename is:

```text
openriak-kv@node-01.cluster-a.openriak
```

Dots are intentional; the hostname acts like an easy-to-edit FQDN-style Docker DNS alias. The single-node file publishes 8087 and 8098 by default and supports:

- `OPENRIAK_CONTAINER_NAME`
- `OPENRIAK_NODE_1_HOST`
- `OPENRIAK_PB_PORT`
- `OPENRIAK_HTTP_PORT`
- `OPENRIAK_CONFIG_PATH`
- `OPENRIAK_DATA_PATH`
- `OPENRIAK_LOGS_PATH`
- `OPENRIAK_DISTRIBUTED_COOKIE`
- `OPENRIAK_MONITOR_INTERVAL_SECONDS`

Default bind-mount directories are relative to the Compose file, beneath the node name, and are called `config`, `data`, and `logs`.

## Cluster Compose file and discovery protocol

`compose.cluster.yaml` generates five services by default. `--cluster-nodes N` can generate 2 through 253 services. This value controls generation only; there is intentionally no runtime `configured-node-count`, because the user considered that more likely to cause operator error than provide safety.

Each node has:

- a configurable container name and host/DNS alias (`OPENRIAK_NODE_N_CONTAINER_NAME`, `OPENRIAK_NODE_N_HOST`)
- a stable default hostname such as `node-03.cluster-a.openriak`
- the matching default nodename `openriak-kv@node-03.cluster-a.openriak`
- its own config/data/log bind mounts
- the shared `OPENRIAK_CLUSTER_CONTROL_PATH` bind mount
- the same Erlang cookie
- PB/HTTP host-port variables

All containers still listen on 8087/8098 internally. The generated five-node example maps distinct host defaults (18087/18098, 18187/18198, and so on) because one host cannot bind the same port for five containers. Inter-node traffic uses the bridge network and Docker DNS aliases, not these host-port mappings. Users may override the variables in `.env`.

Exactly one service gets the environment value `role: coordinator`; a missing or empty `role` means follower. Both roles are logged.

The shared-volume protocol is intentionally open-ended and does not wait for a configured number of nodes:

- A coordinator removes every stale `*-coordinator` file and stale status file on startup, generates a random 16-hex suffix, then writes `{coordinator-nodename}-{suffix}-coordinator`.
- A follower removes all files it owns on startup, discovers a valid coordinator marker, resolves its current IPv4 address, and writes `{follower-nodename}-{suffix}-ready`.
- The current implementation stores `nodename`, `ip`, `coordinator`, and `suffix` inside each control file. The IP is not part of the filename.
- The coordinator validates file contents and verifies the advertised nodename resolves to the advertised IP before atomically renaming `ready` to `approved`.
- A follower waits for exactly one valid approval, performs `riak admin cluster join {coordinator-nodename}`, then records `joined`.
- The coordinator batches available joined nodes, runs cluster plan and commit, waits for ring readiness and transfers, and publishes `complete`.
- Followers wait for completion, clean their own files, and enter the final health-monitor loop.
- Failure files propagate a bootstrap failure so participating nodes shut down cleanly.
- Existing Riak ring membership remains authoritative on restart; already-clustered nodes wait for ring readiness/transfers and resume monitoring.

Do not reintroduce hard-coded container IPs. The point of the shared control file is to carry the dynamically assigned IPv4 address while the nodename remains stable through Docker DNS.

## Integration tests performed by `refresh`

For every target, the integration harness must verify:

- Compose initializes the three bind mounts and `config`, `data`, and `logs` become populated.
- Commented/live settings are replaced as described above.
- The configured nodename, ring size 8, leveled backend, TicTac AAE, and storeheads are present.
- OpenRiak starts and reaches the logged keep-alive/monitor phase.
- CLI `riak ping` returns `pong`.
- HTTP `GET /ping` returns status 200 and body `OK`.
- The Docker healthcheck becomes healthy.
- Graceful Compose shutdown produces the expected stop logs and waits for BEAM.
- The five-node Compose file forms exactly one consistent cluster.
- Every node agrees on membership, reports a ready ring, finishes transfers, passes CLI and HTTP pings, is healthy, has populated bind mounts, and logs its role/lifecycle.
- Cleanup runs even after partial startup or a failed test.

The wait helpers now fail immediately if a single-node or cluster container exits, rather than burning the full 1,800-second timeout while no containers are alive.

## Static downloads and docs-page integration

Only passed targets are published under:

```text
content/static/openriak-kv/downloads/docker/{version}/{image-tag-without-repository}/
```

Each published directory contains:

```text
Dockerfile
compose.single.yaml
compose.cluster.yaml
.env.example
```

The version data file contains a `dockerImages` array with filenames, SHA-256 values, URLs, tested timestamp, base image, cluster size, image tag, and node name:

```text
tools/generated/openriak-kv/data/versions/{version}.json
```

The existing downloads page consumes that generated data. For 3.4.0 the route is:

```text
http://localhost:1410/docs/openriak-kv/3.4.0/downloads/
```

Failed or incomplete cache entries must not appear on the downloads page. To reconstruct static copies from passed reports without Docker work, run:

```sh
tools/openriak-docker/openriak-docker sync-static
```

## Latest fixes and why the last Amazon attempt failed

Several earlier failures were caused by harness and generated-image bugs, not by unsupported OpenRiak packages:

1. Initial broad runs were invoked without effective Docker permission; old 3.4.1 reports from that run often show base-image pull failures. The matrix is intended to run through `sudo` in this WSL environment.
2. RPM images initially lacked dependencies and failed package installation. The explicit RPM dependency, `--nodeps`, and bundled-escript handling described above was added.
3. RHEL initially used broad UBI tags. The release-specific 8.10/9.8 mapping was added.
4. Slow emulated healthchecks were too aggressive. Their timeout/start period was increased.
5. Test waits continued until timeout after containers had already exited. Immediate exit detection was added to single-node log waits and cluster waits.
6. The newest canary run, `3.4.0/amazon-linux-2023-aarch64/otp24-aarch64-1`, successfully built and passed all single-node tests. Its cluster followers then rejected the coordinator because glibc `getent hosts` returned an IPv4-mapped IPv6 value such as `::ffff:172.25.0.6`, while validation accepted only plain `172.25.0.6`. The coordinator eventually timed out and stopped every node. `nodename_resolves_to_ip` now accepts both the plain IPv4 and `::ffff:{IPv4}` forms, and a regression unit test covers it.

The final resolver fix and the new progress logging have **not yet received a complete Docker integration rerun**. The next Linux session should not claim they are integration-verified until the canary and/or matrix passes.

## New matrix progress logging

The source now prints a run header with local timestamps and selection details, timestamps every target line, includes phase timeouts, indents substeps, and prints final duration. A newly started run should resemble:

```text
================================================================
Docker script started at 2026-09-05 11:01:22
Version:       3.4.0, 3.4.1
OS:            all
Architecture:  all
Timeout:       1800s per task
Cluster nodes: 5
================================================================
[1/32] 2026-09-05 11:01:22 SKIPPED openriak/openriak-kv:3.4.0-alpine-3.21-otp24-aarch64 (complete cache exists)
[4/32] 2026-09-05 11:01:22 Refreshing openriak/openriak-kv:3.4.0-amazon-linux-2023-otp24-aarch64
[4/32] 2026-09-05 11:01:22   - Pulling and pinning base image (timeout 1800s)
[4/32] 2026-09-05 11:02:00   - Creating Dockerfile, compose YAML files and .env for this run
[4/32] 2026-09-05 11:02:01   - Building image (timeout 1800s)
[4/32] 2026-09-05 11:05:00   - Testing single node (timeout 1800s)
[4/32] 2026-09-05 11:15:00   - Testing 5-node cluster (timeout 1800s)
[4/32] 2026-09-05 11:41:37   - PASSED (duration 2415s)
```

Pull and image-build subprocesses now enforce and log their timeout. The run report records command timing/errors. Because the existing matrix log predates this change, it still contains old-format lines; the new header appears only when a new invocation begins.

## Cache state at handoff

The 3.4.0 top-level reports currently show nine passed targets:

```text
alpine-3.21-aarch64/otp24-aarch64-r1
alpine-3.21-aarch64/otp26-aarch64-r1
alpine-3.21-x86_64/otp24-x86_64-r1
debian-12-amd64/otp24-amd64
debian-12-amd64/otp26-amd64
ubuntu-jammy-amd64/otp24-amd64
ubuntu-jammy-amd64/otp26-amd64
ubuntu-noble-amd64/otp24-amd64
ubuntu-noble-amd64/otp26-amd64
```

The other nine 3.4.0 targets are currently marked failed and should be retried after the fixes:

```text
amazon-linux-2023-aarch64/otp24-aarch64-1
amazon-linux-2023-aarch64/otp26-aarch64-1
amazon-linux-2023-x86_64/otp24-x86_64-1
amazon-linux-2023-x86_64/otp26-x86_64-1
oracle-linux-9-x86_64/otp24-x86_64-1
oracle-linux-9-x86_64/otp26-x86_64-1
rhel-9-x86_64/otp26-x86_64-1
ubuntu-noble-arm64/otp24-arm64
ubuntu-noble-arm64/otp26-arm64
```

No 3.4.1 top-level report is currently passed. Most are failed from earlier runs; `3.4.1/alpine-3.21-x86_64/otp24-x86_64-r1` says `running`, but that is stale persisted state—there is no corresponding live matrix worker. `--retry-failed` is intended to recover interrupted/stale-running entries.

The working tree at handoff includes many modified current cache artifacts/reports, untracked historical run directories, a new static Alpine aarch64 OTP26 download directory, and changes to:

```text
tools/openriak-docker/openriak_docker.py
tools/openriak-docker/tests/test_openriak_docker.py
tools/generated/openriak-kv/data/versions/3.4.0.json
tools/cache/openriak-docker/refresh-3.4.0-3.4.1.log
```

There are also modified/untracked RPM target assets and reports. Inspect `git status --short` before making any change. Do not assume that generated files are disposable merely because they are generated; the user wants passed current artifacts and compact reports in Git.

## Recommended continuation

First re-run the unit tests and inspect the latest diff. Then validate the specific Amazon canary that exposed the mapped-IPv4 bug before committing to another overnight matrix if practical:

```sh
sudo -v
sudo -n tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 \
  --os-id amazon-linux-2023-aarch64 \
  --download-id otp24-aarch64-1 \
  --timeout 1800 \
  --retry-failed
```

If it passes, the user's intended manual overnight restart is:

```sh
sudo -v
nohup sudo -n tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 \
  --version 3.4.1 \
  --timeout 1800 \
  --retry-failed \
  >> tools/cache/openriak-docker/refresh-3.4.0-3.4.1.log 2>&1 &
```

Follow it with:

```sh
tail -f tools/cache/openriak-docker/refresh-3.4.0-3.4.1.log
```

To stop only the matrix worker cleanly:

```sh
sudo pkill -TERM -f '[o]penriak_docker.py refresh'
```

After a stopped/failed run, also inspect for leftover containers and clean only containers/networks created by this harness. Do not issue broad destructive Docker cleanup commands.

Once the matrix finishes:

1. Review every failed report and its newest `runs/.../logs/` files rather than guessing from the one-line matrix status.
2. Confirm no passed target is missing current Dockerfile, both Compose files, `.env.example`, and `report.json`.
3. Run `sync-static` if necessary.
4. Confirm `dockerImages` in each generated version JSON exactly matches passed cache entries.
5. Build/serve the docs and check each version's downloads page and all four artifact links.
6. Re-run the 25 unit tests.
7. Review `git status` and diffs carefully. No commit was requested or made as part of this handoff.

## User preferences and non-negotiable decisions

- Say **OpenRiak KV**, never Riak KV, for this feature.
- Supported versions begin at 3.4.0.
- Do not build OpenRiak from source; install the official package from `files.tiot.jp`.
- Do not use OS image tag `latest`; use the release tag and pin the resolved digest.
- Do not automatically rerun successful cache entries.
- A manual forced regeneration is what refreshes the OS release image/digest.
- Do not filter the overnight matrix by OS family.
- Keep a reusable, configurable image as the primary artifact; Compose examples demonstrate one node and a cluster.
- Keep the default host/nodename template branded as `openriak-kv@node-01.cluster-a.openriak`.
- Keep the random per-generated-image cookie and log it at startup.
- Keep the daemon-plus-monitor lifecycle and graceful stop trap.
- Keep one coordinator selected by `role`; missing role means follower.
- Do not add a configured node count to the runtime discovery protocol.
- Keep IP assignment dynamic and transport current IPs through shared control-file contents.
- Report every lifecycle and coordination stage to Docker logs.
- Keep expensive work manual and cache-driven. The normal documentation build must remain cheap.

Begin by reporting the repository state and whether the unit tests still pass. Do not restart the expensive matrix unless the user explicitly asks you to do so in the new session.
