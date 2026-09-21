---
title: Replicate data between two clusters
description: Replicate a new object from cluster A to cluster B, then seed an older object and verify convergence.
  Each cluster in this exercise has one node to keep resource use small; this arrangement provides no host-level
  fault t
weight: 320
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- new-operators
source_material:
- legacy-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\tutorials\clusterTicTac.md
legacy_3_2_5_sources:
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v2-multi-datacenter\quick-start.md
- C:\Users\pjacl\Downloads\riak-docs-fork\kv\3.2.5\configuring\v3-multi-datacenter\quick-start.md
- Legacy multi-datacenter replication terminology and commands require compatibility review.
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/replication/two-cluster-replication.md
related:
- how-to/replication-and-reconciliation/connect-clusters-with-next-generation-replication
- how-to/replication-and-reconciliation/enable-real-time-replication
- how-to/replication-and-reconciliation/configure-and-schedule-fullsync
- how-to/replication-and-reconciliation/secure-next-generation-replication-connections
- reference/replication-interfaces/next-generation-replication-runtime-controls
- foundations/replication-and-repair/replication-sources-queues-and-sinks
- foundations/replication-and-repair/real-time-replication-and-fullsync
- foundations/replication-and-repair/targeted-reconciliation-and-aae-folds
next_page: tutorials/replication-and-reconciliation/catch-up-after-a-replication-interruption
---

Replicate a new object from cluster A to cluster B, then seed an older object and verify convergence. Each cluster in this exercise has one node to keep resource use small; this arrangement provides no host-level fault tolerance.

## Create two isolated environments

You need Docker Compose and `curl`. Create directories `replication-a` and `replication-b`. Download these files into each directory:

{{< learning-cluster-files mode="single" >}}

Edit the existing assignments in each `.env`:

- A: `COMPOSE_PROJECT_NAME=learning-a`, `OPENRIAK_CONTAINER_NAME=learning-a`, `OPENRIAK_NODE_1_HOST=node-a.openriak`, `OPENRIAK_HTTP_PORT=127.0.0.1:19098`, and `OPENRIAK_PB_PORT=127.0.0.1:19087`.
- B: `COMPOSE_PROJECT_NAME=learning-b`, `OPENRIAK_CONTAINER_NAME=learning-b`, `OPENRIAK_NODE_1_HOST=node-b.openriak`, `OPENRIAK_HTTP_PORT=127.0.0.1:19198`, and `OPENRIAK_PB_PORT=127.0.0.1:19187`.

Give each cluster a different `OPENRIAK_DISTRIBUTED_COOKIE`; `openssl rand -hex 24` produces a suitable lab value. Keep the relative data, configuration, and log paths in their separate working directories. Never join the nodes together.

Run `docker compose up -d --no-build` in each directory. Before storing data, edit each bind-mounted `config/riak.conf`, replacing any existing values for these settings:

{{< settings-example >}}
storage_backend = leveled
tictacaae_active = active
delete_mode = keep
{{< /settings-example >}}

Run `docker compose restart` in each directory and wait for both `/ping` endpoints to return `OK`.

## Connect the replication network

Create a private Docker bridge and attach both containers:

```sh
docker network create learning-replication
docker network connect learning-replication learning-a
docker network connect learning-replication learning-b
docker inspect --format '{{ index .NetworkSettings.Networks "learning-replication" }}' learning-a
docker inspect --format '{{ index .NetworkSettings.Networks "learning-replication" }}' learning-b
```

Record the IPv4 address shown for each container as `A_IP` and `B_IP`. These addresses are for container-to-container traffic, not the published loopback ports. This exercise uses unencrypted HTTP on an isolated bridge; use [Secure next-generation replication connections]({{< product-version-root >}}how-to/replication-and-reconciliation/secure-next-generation-replication-connections/) for protected connections outside this lab.

Write an object before enabling replication:

```sh
export A=http://127.0.0.1:19098
export B=http://127.0.0.1:19198
curl --fail -X PUT "$A/buckets/repl-demo/keys/before" -H 'Content-Type: text/plain' --data-binary 'written before replication'
```

## Enable source and sink

On A, add or replace these settings in `riak.conf`:

{{< settings-example >}}
replrtq_enablesrc = enabled
replrtq_srcqueue = cluster_b:any
repl_reap = enabled
replrtq_vnodecheck = quorum
{{< /settings-example >}}

On B, substitute A's actual bridge IPv4 address for `A_IP`:

{{< settings-example >}}
replrtq_enablesink = enabled
replrtq_sinkqueue = cluster_b
replrtq_sinkpeers = A_IP:8098:http
replrtq_sinkworkers = 2
replrtq_peer_discovery = disabled
repl_reap = enabled
replrtq_vnodecheck = quorum
{{< /settings-example >}}

Restart A and B from their respective directories. If you recreate rather than restart a container, reconnect its extra bridge and recheck its address. Once both endpoints respond, write a new object and poll the sink:

```sh
curl --fail -X PUT "$A/buckets/repl-demo/keys/after" -H 'Content-Type: text/plain' --data-binary 'written after replication'
curl -i "$B/buckets/repl-demo/keys/after"
```

Repeat the read until it returns `written after replication`. A short initial `404` is possible because delivery is asynchronous. Persistent absence requires checking the sink peer, queue name, listeners, and logs.

## Seed the older object

The earlier `before` object was never queued by real-time replication. In A's directory, prepare the shell helper from [Build and explore a Docker cluster]({{< product-version-root >}}tutorials/first-cluster/build-and-explore-a-docker-cluster/); the service here is `node`, not `node1`. Open the interactive remote console using that helper's environment:

{{< cli-example key="shell:riak remote_console" prefix="kvi node" >}}

Submit the bucket to A's source queue:

{{< cli-example key="erlang:riak_client:aae_fold:repl_keys_range" args=`{repl_keys_range, <<"repl-demo">>, all, all, cluster_b}` >}}

Wait for delivery and read `before` on B. Expect `written before replication`. Detach from the Erlang console with `Ctrl-G`, then `q`.

## Check reconciliation

On A, add this one-way fullsync relationship, substituting B's bridge IPv4 address. Both lab clusters use the unchanged bucket replication value of three:

{{< settings-example >}}
ttaaefs_scope = all
ttaaefs_queuename = cluster_b
ttaaefs_queuename_peer = disabled
ttaaefs_localnval = 3
ttaaefs_remotenval = 3
ttaaefs_peerip = B_IP
ttaaefs_peerport = 8098
ttaaefs_peerprotocol = http
ttaaefs_autocheck = 24
ttaaefs_allcheck.policy = always
{{< /settings-example >}}

Restart A. Wait for its AAE trees to be ready, then open its remote console and prompt a check:

{{< cli-example key="erlang:riak_client:ttaaefs_fullsync" args="all_check" >}}

Inspect A's logs for the completed exchange. A successful submission is not a successful exchange; look for `in_sync=true`. If a first exchange submits repairs, allow delivery and run another check.

## Continue or clean up

Keep both clusters for the next replication lessons. When finished, run `docker compose down` in each directory, then `docker network rm learning-replication`. The bind-mounted files remain; remove only these lab directories if you want to discard their data.
