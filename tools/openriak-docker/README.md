# OpenRiak KV Docker cache

This tool derives Docker targets from the authoritative release records in
`content/openriak-kv/metadata/{version}/supported-os.json` and
`downloads.json`. It accepts OpenRiak KV 3.4.0 and newer only; legacy Riak KV
releases are rejected. It does not run as part of a normal documentation build.

`refresh` is the only operation that pulls an OS image or runs containers. A
complete cached target is skipped by default. Pass `--force` to pull the
release-specific base tag again, pin its newly resolved digest, regenerate the
files, build the image, and rerun the tests. An incomplete or incompatible
cache is reported as an error unless `--force` is present. A refresh checks that:

- `/etc/riak`, `/var/lib/riak`, and `/var/log/riak` use bind mounts and are populated;
- `nodename`, `ring_size = 8`, `storage_backend = leveled`, TicTac AAE, and storeheads can be configured;
- the node starts and `riak ping` returns `pong`;
- `GET /ping` returns HTTP 200 with the body `OK`;
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
`compose.single.yaml`, `compose.cluster.yaml`, and `report.json`. Per-command
output is kept under the run's `logs/`
directory. A passed run is copied to
`content/static/openriak-kv/downloads/docker/` so Hugo can publish the
Dockerfile and both Compose files. Failed runs remain cached but are not
advertised on the downloads page.

Git retains the current target artifacts and every historical run's compact
`report.json`. Historical `logs/`, `Dockerfile`, `compose.single.yaml`, and
`compose.cluster.yaml` copies are local diagnostics and are ignored by Git. CI
systems that require full audit logs should upload those ignored files as
workflow artifacts rather than add them to the repository.

To restore static copies from already-tested cache entries without pulling,
building, or testing anything:

```sh
tools/openriak-docker/openriak-docker sync-static
```

The generated `compose.single.yaml` names its one container after the full target and
uses a matching relative directory containing `config`, `data`, and `logs`.
Set `OPENRIAK_CONTAINER_NAME`, `OPENRIAK_NODE_NAME`, `OPENRIAK_PB_PORT`, or
`OPENRIAK_HTTP_PORT` to override its container name, full Erlang node name, or
host-side ports. The single-node example uses the `172.16.0.0/24` bridge
network, assigns `172.16.0.1` to OpenRiak, reserves `172.16.0.254` as the
gateway, and sets the default Erlang node name to `riak@172.16.0.1`. Override
`OPENRIAK_NODE_IPV4`, `OPENRIAK_NETWORK_SUBNET`, and
`OPENRIAK_NETWORK_GATEWAY` together with `OPENRIAK_NODE_NAME` when changing
the network.

`compose.cluster.yaml` assigns sequential static IP addresses and distinct
IP-based Erlang node names. It mounts a shared cluster-control directory and
sets `role=coordinator` on exactly one service; an omitted or empty `role`
means follower. Both roles are logged at startup. Followers remove their own
stale control files, advertise readiness for discovered coordinator markers,
wait for approval, and then run their own join command. The coordinator removes
all stale coordinator markers, publishes a new random-suffix marker, approves
followers for that suffix, and continuously plans and commits non-empty joined
batches. Coordination progresses through `ready`, `approved`, `joined`, and
`complete` files. Riak's ring state remains authoritative after restarts, and
any bootstrap failure is published so participating nodes stop cleanly.

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
