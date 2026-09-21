---
title: Build and explore a Docker cluster
description: Build a five-node learning cluster, store a greeting, and read it through another node. You will use
  the same disposable cluster for the data and query exercises that follow.
weight: 10
diataxis: tutorial
product: OpenRiak KV
product_version: 3.4.0
status: editorially-rewritten
draft: true
audience:
- new-operators
source_material:
- live-3.2.5
- proposed-kv
migration_source_root: \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv
migration_sources:
- \\wsl.localhost\Ubuntu\home\peter\GitHub\TI-Tokyo\openriak-docs\content\kv\tutorials_howto\quickstart\docker.md
tags:
- diataxis
- kv
- tutorial
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
restructured_from:
- tutorials/first-cluster/docker.md
related:
- tutorials/data-and-concurrency/explore-objects-buckets-and-metadata-with-http
- how-to/quick-start/start-a-local-node-with-docker
- how-to/quick-start/start-a-local-cluster-with-docker
- reference/orientation-and-compatibility/backend-capability-matrix
- foundations/overview/what-openriak-kv-is
- foundations/cluster-architecture/rings-partitions-and-virtual-nodes
---

Build a five-node learning cluster, store a greeting, and read it through another node. You will use the same disposable cluster for the data and query exercises that follow.

## Prepare the working directory

You need Docker with Compose, `curl`, and enough memory and disk space for five local containers. Create an empty directory named `openriak-learning` and open a terminal there. Do not reuse a production node's files.

{{< learning-cluster-files >}}

Open `.env`. For local-only access, set each HTTP and Protocol Buffers host port to a loopback binding: for example, node1's HTTP binding is `127.0.0.1:18098`, node2's is `127.0.0.1:18198`, and the following nodes continue the pattern. Prefix the existing PB host ports with `127.0.0.1:` too. These are deliberate lab bindings.

## Start the cluster

```sh
docker compose config
docker compose pull
docker compose up -d --no-build
docker compose logs --tail=50
```

The coordinator and followers discover one another using the supplied control directory. Wait for startup.

## Prepare the learning shell

Save the following in `learning-env.sh` and run `source learning-env.sh` in your Bash terminal. The `kv` helper runs a command on the chosen service using the running node’s configuration. It also avoids the Alpine system wrapper’s handling of quoted JSON arguments. Use this helper in the following lessons.

{{< learning-cluster-shell >}}

Inspect membership:

{{< cli-example key="shell:riak admin member-status" prefix="kv node1" >}}

You should see five valid nodes. If a node is missing, inspect its service logs before continuing.

## Select storage for the exercises

Before writing any objects, select Leveled so this lab can also run the Query API exercises. This is an explicit learning-environment choice, not a backend migration procedure for existing data.

```sh
for node in node1 node2 node3 node4 node5; do
  docker compose exec -T "$node" sed -i     's/^storage_backend = .*/storage_backend = leveled/' /etc/riak/riak.conf
done
docker compose restart
```

Wait for the nodes to return, then repeat the membership check. Inspect `storage_backend` in each node's effective configuration if a query later reports unsupported backend capabilities.

## Write and read

```sh
export RIAK_HTTP=http://127.0.0.1:18098
curl --fail "$RIAK_HTTP/ping"
curl --fail -i -X PUT "$RIAK_HTTP/buckets/learning/keys/greeting"   -H 'Content-Type: text/plain' --data-binary 'Hello OpenRiak'
curl --fail http://127.0.0.1:18198/buckets/learning/keys/greeting
```

The ping returns `OK`. The read through node2 returns `Hello OpenRiak`, showing that the client need not address only the node that received the write.

## Keep or stop the lab

Keep the cluster running for the next exercise. To stop it, run `docker compose down` in this directory. The bind-mounted configuration, data, logs, and control directory remain so you can resume. To discard the lab permanently, stop it first and remove only those exercise directories. `down --volumes` does not remove these bind mounts.
