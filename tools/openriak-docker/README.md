# OpenRiak KV Docker cache

This tool derives Docker targets from the authoritative release records in
`content/openriak-kv/metadata/{version}/supported-os.json` and
`downloads.json`. It accepts OpenRiak KV 3.4.0 and newer only; legacy Riak KV
releases are rejected. It does not run as part of a normal documentation build.

`refresh` is the only operation that pulls an OS image or runs containers. It
pulls the release-specific base tag, pins the resolved digest in the generated
Dockerfile, verifies the package's recorded SHA-256 checksum, builds the image,
and exercises the generated Compose file. A refresh checks that:

- `/etc/riak`, `/var/lib/riak`, and `/var/log/riak` use bind mounts and are populated;
- `nodename`, `ring_size = 8`, `storage_backend = leveled`, TicTac AAE, and storeheads can be configured;
- the node starts and `riak ping` returns `pong`;
- `GET /ping` returns HTTP 200 with the body `OK`;
- the image healthcheck sees both `beam.smp` and a `pong` response;
- daemon startup, service readiness, transfer completion, monitoring, and
  graceful shutdown are reported in the container log;
- Protocol Buffers and HTTP are published on ports 8087 and 8098 by default.

List targets without changing anything:

```sh
tools/openriak-docker/openriak-docker matrix --version 3.4.0
```

Manually refresh one target:

```sh
tools/openriak-docker/openriak-docker refresh \
  --version 3.4.0 \
  --os-id alpine-3.21-x86_64 \
  --download-id otp24-x86_64-r1
```

The complete OpenRiak KV matrix (3.4.0 and newer) is deliberately guarded
because it is large:

```sh
tools/openriak-docker/openriak-docker refresh --all --yes
```

Each run is retained under:

```text
tools/cache/openriak-docker/{version}/{os-id}/{download-id}/runs/{UTC-run-id}/
```

The same target directory contains the current `Dockerfile`, `compose.yaml`,
and `report.json`. Per-command output is kept under the run's `logs/`
directory. A passed run is copied to
`content/static/openriak-kv/downloads/docker/` so Hugo can publish the
Dockerfile and Compose file. Failed runs remain cached but are not advertised
on the downloads page.

Git retains the current target artifacts and every historical run's compact
`report.json`. Historical `logs/`, `Dockerfile`, and `compose.yaml` copies are
local diagnostics and are ignored by Git. CI systems that require full audit
logs should upload those ignored files as workflow artifacts rather than add
them to the repository.

To restore static copies from already-tested cache entries without pulling,
building, or testing anything:

```sh
tools/openriak-docker/openriak-docker sync-static
```

The generated Compose file names its one container after the full target and
uses a matching relative directory containing `config`, `data`, and `logs`.
Set `OPENRIAK_CONTAINER_NAME`, `OPENRIAK_NODE_NAME`, `OPENRIAK_PB_PORT`, or
`OPENRIAK_HTTP_PORT` to override its container name, full Erlang node name, or
host-side ports. The single-node example uses the `172.16.0.0/24` bridge
network, assigns `172.16.0.1` to OpenRiak, reserves `172.16.0.254` as the
gateway, and sets the default Erlang node name to `riak@172.16.0.1`. Override
`OPENRIAK_NODE_IPV4`, `OPENRIAK_NETWORK_SUBNET`, and
`OPENRIAK_NETWORK_GATEWAY` together with `OPENRIAK_NODE_NAME` when changing
the network. `RIAK_NODE_NAME` remains the image runtime setting, so a later
cluster Compose file can assign a distinct IP-based Erlang node name directly
to every container.

The entrypoint starts OpenRiak with `riak daemon`, waits for BEAM and `riak
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
