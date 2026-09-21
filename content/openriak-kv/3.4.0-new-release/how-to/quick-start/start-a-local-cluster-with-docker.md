---
title: Start a local cluster with Docker
weight: 20
product: OpenRiak KV
product_version: 3.4.0
diataxis: how-to
draft: true
status: editorially-rewritten
editorial_review: complete
technical_review: required
last_reviewed: '2026-09-22'
review_scope: diataxis-content-and-navigation
description: Start a local development cluster using the published cluster Compose file and verify that its nodes
  form one cluster.
related:
- how-to/quick-start/start-a-local-node-with-docker
- tutorials/first-cluster/build-and-explore-a-docker-cluster
- how-to/monitoring-and-diagnostics/inspect-node-and-cluster-health
- how-to/installation/run-openriak-with-persistent-docker-storage
---

Start a local development cluster using the published cluster Compose file and verify that its nodes form one cluster.

## Download the environment

Use a fresh directory and download the **Cluster Compose File** and **Example Environment File** for the same image below. Save them as `compose.yaml` and `.env`.

{{< download-os-picker >}}

{{< docker-downloads >}}

Review `.env`, give the cluster a unique set of container names, and keep its config, data, logs, and shared control directory separate from other clusters. For local-only access, prefix each published host port with `127.0.0.1:`. The supplied services are `node1` through `node5`; exactly one is the coordinator.

## Start and check membership

```sh
docker compose config
docker compose pull
docker compose up -d --no-build
docker compose logs --tail=50
```

The entrypoint coordinates initial discovery and joining. After startup, inspect membership on the first node:

{{< cli-example key="shell:riak admin member-status" prefix="docker compose exec node1" >}}

Confirm all five intended nodes are valid and that pending transfers settle. Use the configured HTTP port for a write/read check as in the single-node quick start.

## Stop and resume

Run `docker compose down` in this directory to stop its services. Retain the bind mounts and control directory to resume the same cluster. For a fresh disposable cluster, remove only that project's retained state after stopping it.
